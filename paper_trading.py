"""
Paper trading backend module.

Provides a simple simulated ("paper") trading system backed by SQLite:
- per-wallet virtual accounts with a USD balance
- opening/closing long/short positions on a fixed set of symbols
- price fetching from CoinGecko with a small in-memory cache
- candles built server-side from CoinGecko price history so the chart works
  even where exchange APIs (e.g. Binance) block the server's IP
- take-profit / stop-loss checking via a background thread
- price alerts

This module is intentionally dependency-light (stdlib + requests) so it
drops into an existing Flask app without adding new services.
"""

import os
import sqlite3
import threading
import time
import datetime

import requests

SYMBOL_TO_COINGECKO = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "MATIC": "matic-network",
    "AVAX": "avalanche-2",
    "ARB": "arbitrum",
    "OP": "optimism",
}

INTERVAL_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "4h": 14400,
    "1d": 86400,
}

_klines_cache = {}
_klines_cache_lock = threading.Lock()
_KLINES_CACHE_TTL = 15


def get_klines(symbol, interval="1m", limit=200):
    symbol = symbol.upper()
    coingecko_id = SYMBOL_TO_COINGECKO.get(symbol)
    if not coingecko_id:
        return None
    if interval not in INTERVAL_SECONDS:
        interval = "1m"
    interval_s = INTERVAL_SECONDS[interval]

    cache_key = f"{symbol}:{interval}"
    now = time.time()
    with _klines_cache_lock:
        cached = _klines_cache.get(cache_key)
        if cached and (now - cached[1]) < _KLINES_CACHE_TTL:
            return cached[0]

    to_ts = int(now)
    from_ts = to_ts - interval_s * limit

    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/market_chart/range",
            params={"vs_currency": "usd", "from": from_ts, "to": to_ts},
            timeout=8,
        )
        data = resp.json()
        prices = data.get("prices", [])
        if not prices:
            raise ValueError("empty price series")

        buckets = {}
        for ts_ms, price in prices:
            ts = int(ts_ms // 1000)
            bucket_start = (ts // interval_s) * interval_s
            b = buckets.get(bucket_start)
            if b is None:
                buckets[bucket_start] = {"o": price, "h": price, "l": price, "c": price}
            else:
                b["c"] = price
                if price > b["h"]:
                    b["h"] = price
                if price < b["l"]:
                    b["l"] = price

        candles = [
            {"t": bucket_start * 1000, "o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"], "v": 0}
            for bucket_start, b in sorted(buckets.items())
        ]
        candles = candles[-limit:]
    except Exception:
        with _klines_cache_lock:
            cached = _klines_cache.get(cache_key)
            if cached:
                return cached[0]
        return None

    with _klines_cache_lock:
        _klines_cache[cache_key] = (candles, now)
    return candles


def get_live_ticker_price(symbol):
    return get_price(symbol)


_DB_PATH = None

_price_cache = {}
_price_cache_lock = threading.Lock()
_PRICE_CACHE_TTL = 15

_checker_thread = None
_checker_started = False


def init_paper_trading(db_path):
    global _DB_PATH
    _DB_PATH = db_path


def _get_db():
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_paper_tables():
    conn = _get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_accounts (
            wallet TEXT PRIMARY KEY,
            balance REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            entry_type TEXT NOT NULL,
            size_usd REAL NOT NULL,
            entry_price REAL,
            take_profit REAL,
            stop_loss REAL,
            status TEXT NOT NULL DEFAULT 'pending',
            network TEXT,
            fee_tx_hash TEXT,
            close_price REAL,
            pnl REAL,
            created_at TEXT NOT NULL,
            closed_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            symbol TEXT NOT NULL,
            target_price REAL NOT NULL,
            triggered INTEGER NOT NULL DEFAULT 0,
            dismissed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_price(symbol):
    symbol = symbol.upper()
    coingecko_id = SYMBOL_TO_COINGECKO.get(symbol)
    if not coingecko_id:
        return None

    now = time.time()
    with _price_cache_lock:
        cached = _price_cache.get(symbol)
        if cached and (now - cached[1]) < _PRICE_CACHE_TTL:
            return cached[0]

    try:
        resp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coingecko_id, "vs_currencies": "usd"},
            timeout=5,
        )
        data = resp.json()
        price = data.get(coingecko_id, {}).get("usd")
        if price is None:
            return None
        price = float(price)
    except Exception:
        with _price_cache_lock:
            cached = _price_cache.get(symbol)
            if cached:
                return cached[0]
        return None

    with _price_cache_lock:
        _price_cache[symbol] = (price, now)
    return price


def get_or_create_account(wallet, starting_balance=1000):
    conn = _get_db()
    row = conn.execute(
        "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
    ).fetchone()
    if row is None:
        conn.execute(
            "INSERT INTO paper_accounts (wallet, balance, created_at) VALUES (?, ?, ?)",
            (wallet, starting_balance, datetime.datetime.utcnow().isoformat()),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
        ).fetchone()
    conn.close()
    return {"wallet": row["wallet"], "balance": row["balance"], "created_at": row["created_at"]}


def adjust_balance(wallet, delta):
    conn = _get_db()
    row = conn.execute(
        "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
    ).fetchone()
    if row is None:
        conn.close()
        return {"error": "Account not found"}, 404

    new_balance = row["balance"] + delta
    if new_balance < 0:
        conn.close()
        return {"error": "Insufficient balance"}, 400

    conn.execute(
        "UPDATE paper_accounts SET balance = ? WHERE wallet = ?", (new_balance, wallet)
    )
    conn.commit()
    conn.close()
    return {"wallet": wallet, "balance": new_balance}, 200


def get_account_snapshot(wallet):
    conn = _get_db()
    account = conn.execute(
        "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
    ).fetchone()
    if account is None:
        conn.close()
        return None

    open_positions = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? AND status = 'open' ORDER BY id DESC",
        (wallet,),
    ).fetchall()
    conn.close()

    unrealized_pnl = 0.0
    positions_out = []
    for pos in open_positions:
        current_price = get_price(pos["symbol"])
        pnl = _calc_pnl(pos, current_price) if current_price else 0.0
        unrealized_pnl += pnl
        positions_out.append(_position_to_dict(pos, current_price=current_price, pnl=pnl))

    return {
        "wallet": account["wallet"],
        "balance": account["balance"],
        "unrealized_pnl": round(unrealized_pnl, 2),
        "equity": round(account["balance"] + unrealized_pnl, 2),
        "open_positions": positions_out,
    }


def _position_to_dict(row, current_price=None, pnl=None):
    return {
        "id": row["id"],
        "wallet": row["wallet"],
        "symbol": row["symbol"],
        "direction": row["direction"],
        "entry_type": row["entry_type"],
        "size_usd": row["size_usd"],
        "entry_price": row["entry_price"],
        "take_profit": row["take_profit"],
        "stop_loss": row["stop_loss"],
        "status": row["status"],
        "network": row["network"],
        "fee_tx_hash": row["fee_tx_hash"],
        "close_price": row["close_price"],
        "pnl": row["pnl"] if row["pnl"] is not None else pnl,
        "current_price": current_price,
        "created_at": row["created_at"],
        "closed_at": row["closed_at"],
    }


def _calc_pnl(row, current_price):
    if row["entry_price"] in (None, 0):
        return 0.0
    change = (current_price - row["entry_price"]) / row["entry_price"]
    if row["direction"] == "short":
        change = -change
    return row["size_usd"] * change


def open_position(wallet, symbol, direction, size_usd, entry_type,
                   entry_price=None, take_profit=None, stop_loss=None,
                   network=None, fee_tx_hash=None):
    symbol = symbol.upper()
    if symbol not in SYMBOL_TO_COINGECKO:
        return {"error": "Unsupported symbol"}, 400
    if direction not in ("long", "short"):
        return {"error": "Direction must be 'long' or 'short'"}, 400
    if entry_type not in ("market", "limit", "stop"):
        return {"error": "entry_type must be 'market', 'limit', or 'stop'"}, 400
    if size_usd is None or size_usd <= 0:
        return {"error": "Invalid position size"}, 400

    conn = _get_db()
    account = conn.execute(
        "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
    ).fetchone()
    if account is None:
        conn.close()
        return {"error": "Account not found"}, 404
    if account["balance"] < size_usd:
        conn.close()
        return {"error": "Insufficient balance"}, 400

    status = "pending"
    resolved_entry_price = entry_price

    if entry_type == "market":
        resolved_entry_price = get_price(symbol)
        if resolved_entry_price is None:
            conn.close()
            return {"error": "Price unavailable, try again"}, 503
        status = "open"
    else:
        if entry_price is None or entry_price <= 0:
            conn.close()
            return {"error": "Limit/stop orders require a valid entry_price"}, 400

    now = datetime.datetime.utcnow().isoformat()
    conn.execute(
        """INSERT INTO paper_positions
           (wallet, symbol, direction, entry_type, size_usd, entry_price,
            take_profit, stop_loss, status, network, fee_tx_hash, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (wallet, symbol, direction, entry_type, size_usd, resolved_entry_price,
         take_profit, stop_loss, status, network, fee_tx_hash, now),
    )
    new_balance = account["balance"] - size_usd
    conn.execute(
        "UPDATE paper_accounts SET balance = ? WHERE wallet = ?", (new_balance, wallet)
    )
    conn.commit()
    position_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    row = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ?", (position_id,)
    ).fetchone()
    conn.close()

    return _position_to_dict(row, current_price=resolved_entry_price, pnl=0.0), 201


def close_position(wallet, position_id):
    conn = _get_db()
    pos = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ? AND wallet = ?",
        (position_id, wallet),
    ).fetchone()
    if pos is None:
        conn.close()
        return {"error": "Position not found"}, 404
    if pos["status"] != "open":
        conn.close()
        return {"error": "Position is not open"}, 400

    current_price = get_price(pos["symbol"])
    if current_price is None:
        conn.close()
        return {"error": "Price unavailable, try again"}, 503

    pnl = _calc_pnl(pos, current_price)
    payout = pos["size_usd"] + pnl
    now = datetime.datetime.utcnow().isoformat()

    conn.execute(
        """UPDATE paper_positions
           SET status = 'closed', close_price = ?, pnl = ?, closed_at = ?
           WHERE id = ?""",
        (current_price, pnl, now, position_id),
    )
    account = conn.execute(
        "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
    ).fetchone()
    new_balance = account["balance"] + max(payout, 0.0)
    conn.execute(
        "UPDATE paper_accounts SET balance = ? WHERE wallet = ?", (new_balance, wallet)
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ?", (position_id,)
    ).fetchone()
    conn.close()

    return _position_to_dict(row, current_price=current_price, pnl=pnl), 200


def cancel_pending_position(wallet, position_id):
    conn = _get_db()
    pos = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ? AND wallet = ?",
        (position_id, wallet),
    ).fetchone()
    if pos is None:
        conn.close()
        return {"error": "Position not found"}, 404
    if pos["status"] != "pending":
        conn.close()
        return {"error": "Only pending positions can be cancelled"}, 400

    now = datetime.datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE paper_positions SET status = 'cancelled', closed_at = ? WHERE id = ?",
        (now, position_id),
    )
    account = conn.execute(
        "SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)
    ).fetchone()
    new_balance = account["balance"] + pos["size_usd"]
    conn.execute(
        "UPDATE paper_accounts SET balance = ? WHERE wallet = ?", (new_balance, wallet)
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ?", (position_id,)
    ).fetchone()
    conn.close()
    return _position_to_dict(row), 200


def get_positions(wallet):
    conn = _get_db()
    rows = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? ORDER BY id DESC", (wallet,)
    ).fetchall()
    conn.close()
    out = []
    for row in rows:
        if row["status"] == "open":
            current_price = get_price(row["symbol"])
            pnl = _calc_pnl(row, current_price) if current_price else None
            out.append(_position_to_dict(row, current_price=current_price, pnl=pnl))
        else:
            out.append(_position_to_dict(row))
    return out


def process_wallet_positions(wallet):
    conn = _get_db()
    positions = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? AND status IN ('pending', 'open')",
        (wallet,),
    ).fetchall()
    conn.close()
    for pos in positions:
        _process_position(pos)


def _process_position(pos):
    current_price = get_price(pos["symbol"])
    if current_price is None:
        return

    if pos["status"] == "pending":
        entry_type = pos["entry_type"]
        if entry_type == "limit":
            should_fill = (
                (pos["direction"] == "long" and current_price <= pos["entry_price"]) or
                (pos["direction"] == "short" and current_price >= pos["entry_price"])
            )
        elif entry_type == "stop":
            should_fill = (
                (pos["direction"] == "long" and current_price >= pos["entry_price"]) or
                (pos["direction"] == "short" and current_price <= pos["entry_price"])
            )
        else:
            should_fill = False
        if should_fill:
            conn = _get_db()
            conn.execute(
                "UPDATE paper_positions SET status = 'open' WHERE id = ?", (pos["id"],)
            )
            conn.commit()
            conn.close()
        return

    if pos["status"] == "open":
        hit_tp = pos["take_profit"] is not None and (
            (pos["direction"] == "long" and current_price >= pos["take_profit"]) or
            (pos["direction"] == "short" and current_price <= pos["take_profit"])
        )
        hit_sl = pos["stop_loss"] is not None and (
            (pos["direction"] == "long" and current_price <= pos["stop_loss"]) or
            (pos["direction"] == "short" and current_price >= pos["stop_loss"])
        )
        if hit_tp or hit_sl:
            close_position(pos["wallet"], pos["id"])


def create_alert(wallet, symbol, target_price):
    symbol = symbol.upper()
    if symbol not in SYMBOL_TO_COINGECKO:
        return {"error": "Unsupported symbol"}, 400
    if target_price is None or target_price <= 0:
        return {"error": "Invalid target price"}, 400

    conn = _get_db()
    now = datetime.datetime.utcnow().isoformat()
    conn.execute(
        "INSERT INTO paper_alerts (wallet, symbol, target_price, created_at) VALUES (?, ?, ?, ?)",
        (wallet, symbol, target_price, now),
    )
    conn.commit()
    alert_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    row = conn.execute("SELECT * FROM paper_alerts WHERE id = ?", (alert_id,)).fetchone()
    conn.close()
    return _alert_to_dict(row), 201


def get_alerts(wallet):
    conn = _get_db()
    rows = conn.execute(
        "SELECT * FROM paper_alerts WHERE wallet = ? AND dismissed = 0 ORDER BY id DESC",
        (wallet,),
    ).fetchall()
    conn.close()
    return [_alert_to_dict(row) for row in rows]


def dismiss_alert(wallet, alert_id):
    conn = _get_db()
    row = conn.execute(
        "SELECT * FROM paper_alerts WHERE id = ? AND wallet = ?", (alert_id, wallet)
    ).fetchone()
    if row is None:
        conn.close()
        return {"error": "Alert not found"}, 404
    conn.execute("UPDATE paper_alerts SET dismissed = 1 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
    return {"success": True}, 200


def _alert_to_dict(row):
    return {
        "id": row["id"],
        "wallet": row["wallet"],
        "symbol": row["symbol"],
        "target_price": row["target_price"],
        "triggered": bool(row["triggered"]),
        "created_at": row["created_at"],
    }


def _check_all_alerts():
    conn = _get_db()
    rows = conn.execute(
        "SELECT * FROM paper_alerts WHERE dismissed = 0 AND triggered = 0"
    ).fetchall()
    conn.close()
    for row in rows:
        price = get_price(row["symbol"])
        if price is None:
            continue
        if price >= row["target_price"]:
            conn = _get_db()
            conn.execute(
                "UPDATE paper_alerts SET triggered = 1 WHERE id = ?", (row["id"],)
            )
            conn.commit()
            conn.close()


def _background_loop():
    while True:
        try:
            conn = _get_db()
            rows = conn.execute(
                "SELECT * FROM paper_positions WHERE status IN ('pending', 'open')"
            ).fetchall()
            conn.close()
            for pos in rows:
                _process_position(pos)
            _check_all_alerts()
        except Exception:
            pass
        time.sleep(20)


def start_background_checker():
    global _checker_thread, _checker_started
    if _checker_started:
        return
    _checker_started = True
    _checker_thread = threading.Thread(target=_background_loop, daemon=True)
    _checker_thread.start()
