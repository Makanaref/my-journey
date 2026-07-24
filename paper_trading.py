import sqlite3
import time
import datetime
import threading
import requests

DB_PATH = None

SYMBOL_TO_COINGECKO = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "AVAX": "avalanche-2",
    "OP": "optimism",
}

_price_cache = {}          # symbol -> (price, fetched_at_epoch)
_last_seen_price = {}      # symbol -> last price observed, used for alert crossing detection
PRICE_CACHE_SECONDS = 15

MAX_BALANCE = 1_000_000
MAX_BALANCE_ADJUSTMENT = 1_000_000


def init_paper_trading(db_path):
    global DB_PATH
    DB_PATH = db_path


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_paper_tables():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_accounts (
            wallet TEXT PRIMARY KEY,
            balance_usd REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            symbol TEXT NOT NULL,
            direction TEXT NOT NULL,
            size_usd REAL NOT NULL,
            entry_type TEXT NOT NULL,      -- 'market' | 'limit' | 'stop'
            entry_price REAL,
            take_profit REAL,
            stop_loss REAL,
            status TEXT NOT NULL,          -- 'pending_entry' | 'open' | 'closed' | 'cancelled'
            close_price REAL,
            pnl_usd REAL,
            network TEXT,
            fee_tx_hash TEXT,
            created_at TEXT NOT NULL,
            opened_at TEXT,
            closed_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paper_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT NOT NULL,
            symbol TEXT NOT NULL,
            target_price REAL NOT NULL,
            status TEXT NOT NULL,          -- 'active' | 'triggered' | 'dismissed'
            created_at TEXT NOT NULL,
            triggered_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# --- Price fetching -----------------------------------------------------------

def get_price(symbol):
    symbol = symbol.upper()
    if symbol not in SYMBOL_TO_COINGECKO:
        return None
    cached = _price_cache.get(symbol)
    if cached and (time.time() - cached[1]) < PRICE_CACHE_SECONDS:
        return cached[0]
    try:
        cg_id = SYMBOL_TO_COINGECKO[symbol]
        res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": cg_id, "vs_currencies": "usd"},
            timeout=5
        )
        data = res.json()
        price = data.get(cg_id, {}).get("usd")
        if price is None:
            return cached[0] if cached else None
        _price_cache[symbol] = (price, time.time())
        return price
    except Exception:
        return cached[0] if cached else None


# --- Account -------------------------------------------------------------------

def get_or_create_account(wallet, starting_balance=None):
    conn = get_db()
    row = conn.execute("SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)).fetchone()
    if row:
        conn.close()
        return dict(row)
    balance = starting_balance if starting_balance and starting_balance > 0 else 1000.0
    balance = min(balance, MAX_BALANCE)
    conn.execute(
        "INSERT INTO paper_accounts (wallet, balance_usd, created_at) VALUES (?, ?, ?)",
        (wallet, balance, datetime.datetime.now(datetime.timezone.utc).isoformat())
    )
    conn.commit()
    row = conn.execute("SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)).fetchone()
    conn.close()
    return dict(row)


def adjust_balance(wallet, delta):
    """Add or remove virtual USDT from the paper account at any time.
    delta can be positive (top-up) or negative (withdraw)."""
    if delta == 0:
        return {"error": "Delta cannot be zero"}, 400
    if abs(delta) > MAX_BALANCE_ADJUSTMENT:
        return {"error": "Adjustment too large"}, 400

    account = get_or_create_account(wallet)
    new_balance = account["balance_usd"] + delta
    if new_balance < 0:
        return {"error": "Balance cannot go negative"}, 400
    if new_balance > MAX_BALANCE:
        return {"error": f"Balance cannot exceed {MAX_BALANCE}"}, 400

    conn = get_db()
    conn.execute("UPDATE paper_accounts SET balance_usd = ? WHERE wallet = ?", (new_balance, wallet))
    conn.commit()
    conn.close()
    return {"balance_usd": new_balance}, 200


def _calc_pnl(direction, entry_price, close_price, size_usd):
    if not entry_price or entry_price <= 0:
        return 0
    change_pct = (close_price - entry_price) / entry_price
    if direction == "short":
        change_pct = -change_pct
    return size_usd * change_pct


def get_account_snapshot(wallet):
    conn = get_db()
    account = conn.execute("SELECT * FROM paper_accounts WHERE wallet = ?", (wallet,)).fetchone()
    if not account:
        conn.close()
        return None
    open_positions = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? AND status = 'open'", (wallet,)
    ).fetchall()
    pending_positions = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? AND status = 'pending_entry'", (wallet,)
    ).fetchall()
    conn.close()

    positions = []
    unrealized_pnl = 0.0
    for p in open_positions:
        price = get_price(p["symbol"]) or p["entry_price"]
        pnl = _calc_pnl(p["direction"], p["entry_price"], price, p["size_usd"])
        unrealized_pnl += pnl
        positions.append({
            "id": p["id"], "symbol": p["symbol"], "direction": p["direction"],
            "size_usd": p["size_usd"], "entry_price": p["entry_price"], "current_price": price,
            "take_profit": p["take_profit"], "stop_loss": p["stop_loss"],
            "pnl_usd": pnl, "opened_at": p["opened_at"],
        })

    pending = [{
        "id": p["id"], "symbol": p["symbol"], "direction": p["direction"],
        "size_usd": p["size_usd"], "entry_type": p["entry_type"], "entry_price": p["entry_price"],
        "take_profit": p["take_profit"], "stop_loss": p["stop_loss"], "created_at": p["created_at"],
    } for p in pending_positions]

    return {
        "wallet": wallet,
        "balance_usd": account["balance_usd"],
        "open_positions": positions,
        "pending_positions": pending,
        "unrealized_pnl_usd": unrealized_pnl,
        "total_equity_usd": account["balance_usd"] + unrealized_pnl,
    }


# --- Opening / closing positions -----------------------------------------------

def open_position(wallet, symbol, direction, size_usd, entry_type, entry_price=None,
                   take_profit=None, stop_loss=None, network=None, fee_tx_hash=None):
    symbol = symbol.upper()
    direction = direction.lower()
    entry_type = entry_type.lower()

    if symbol not in SYMBOL_TO_COINGECKO:
        return {"error": "Unsupported symbol"}, 400
    if direction not in ("long", "short"):
        return {"error": "Invalid direction"}, 400
    if entry_type not in ("market", "limit", "stop"):
        return {"error": "Invalid entry type"}, 400
    if not size_usd or size_usd <= 0:
        return {"error": "Invalid position size"}, 400
    if entry_type in ("limit", "stop") and (not entry_price or entry_price <= 0):
        return {"error": "Entry price required"}, 400
    if not fee_tx_hash:
        return {"error": "Fee transaction hash required"}, 400

    account = get_or_create_account(wallet)
    if account["balance_usd"] < size_usd:
        return {"error": "Insufficient paper balance"}, 400

    conn = get_db()
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if entry_type == "market":
        price = get_price(symbol)
        if price is None:
            conn.close()
            return {"error": "Price unavailable, try again"}, 503
        conn.execute("UPDATE paper_accounts SET balance_usd = balance_usd - ? WHERE wallet = ?", (size_usd, wallet))
        cur = conn.execute(
            """INSERT INTO paper_positions
               (wallet, symbol, direction, size_usd, entry_type, entry_price, take_profit, stop_loss,
                status, network, fee_tx_hash, created_at, opened_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', ?, ?, ?, ?)""",
            (wallet, symbol, direction, size_usd, entry_type, price, take_profit, stop_loss,
             network, fee_tx_hash, created_at, created_at)
        )
        position_id = cur.lastrowid
        conn.commit()
        conn.close()
        return {"position_id": position_id, "status": "open", "entry_price": price}, 200

    # limit or stop: wait for price to reach the trigger before opening
    conn.execute("UPDATE paper_accounts SET balance_usd = balance_usd - ? WHERE wallet = ?", (size_usd, wallet))
    cur = conn.execute(
        """INSERT INTO paper_positions
           (wallet, symbol, direction, size_usd, entry_type, entry_price, take_profit, stop_loss,
            status, network, fee_tx_hash, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending_entry', ?, ?, ?)""",
        (wallet, symbol, direction, size_usd, entry_type, entry_price, take_profit, stop_loss,
         network, fee_tx_hash, created_at)
    )
    position_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"position_id": position_id, "status": "pending_entry"}, 200


def close_position(wallet, position_id, reason="manual"):
    conn = get_db()
    p = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ? AND wallet = ? AND status = 'open'", (position_id, wallet)
    ).fetchone()
    if not p:
        conn.close()
        return {"error": "Open position not found"}, 404

    price = get_price(p["symbol"])
    if price is None:
        conn.close()
        return {"error": "Price unavailable, try again"}, 503

    pnl = _calc_pnl(p["direction"], p["entry_price"], price, p["size_usd"])
    returned_amount = p["size_usd"] + pnl

    conn.execute("UPDATE paper_accounts SET balance_usd = balance_usd + ? WHERE wallet = ?", (returned_amount, wallet))
    conn.execute(
        "UPDATE paper_positions SET status = 'closed', close_price = ?, pnl_usd = ?, closed_at = ? WHERE id = ?",
        (price, pnl, datetime.datetime.now(datetime.timezone.utc).isoformat(), position_id)
    )
    conn.commit()
    conn.close()
    return {"status": "closed", "close_price": price, "pnl_usd": pnl, "reason": reason}, 200


def cancel_pending_position(wallet, position_id):
    conn = get_db()
    p = conn.execute(
        "SELECT * FROM paper_positions WHERE id = ? AND wallet = ? AND status = 'pending_entry'", (position_id, wallet)
    ).fetchone()
    if not p:
        conn.close()
        return {"error": "Pending position not found"}, 404
    conn.execute("UPDATE paper_accounts SET balance_usd = balance_usd + ? WHERE wallet = ?", (p["size_usd"], wallet))
    conn.execute("UPDATE paper_positions SET status = 'cancelled' WHERE id = ?", (position_id,))
    conn.commit()
    conn.close()
    return {"status": "cancelled"}, 200


def get_positions(wallet):
    """Full order/position history for the wallet, newest first."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? ORDER BY id DESC LIMIT 200", (wallet,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Price alerts ("timer" lines on the chart) ---------------------------------

def create_alert(wallet, symbol, target_price):
    symbol = symbol.upper()
    if symbol not in SYMBOL_TO_COINGECKO:
        return {"error": "Unsupported symbol"}, 400
    if not target_price or target_price <= 0:
        return {"error": "Invalid target price"}, 400

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO paper_alerts (wallet, symbol, target_price, status, created_at) VALUES (?, ?, ?, 'active', ?)",
        (wallet, symbol, target_price, datetime.datetime.now(datetime.timezone.utc).isoformat())
    )
    alert_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"alert_id": alert_id, "status": "active"}, 200


def get_alerts(wallet):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM paper_alerts WHERE wallet = ? AND status != 'dismissed' ORDER BY id DESC", (wallet,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def dismiss_alert(wallet, alert_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM paper_alerts WHERE id = ? AND wallet = ?", (alert_id, wallet)).fetchone()
    if not row:
        conn.close()
        return {"error": "Alert not found"}, 404
    conn.execute("UPDATE paper_alerts SET status = 'dismissed' WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
    return {"status": "dismissed"}, 200


def _check_alerts_for_symbol(conn, symbol, new_price):
    """Fires alerts whose target price was crossed between the last observed
    price and this new price (in either direction), so the frontend can beep."""
    prev_price = _last_seen_price.get(symbol)
    _last_seen_price[symbol] = new_price
    if prev_price is None or new_price is None:
        return

    lo, hi = (prev_price, new_price) if prev_price <= new_price else (new_price, prev_price)
    if lo == hi:
        return

    active_alerts = conn.execute(
        "SELECT * FROM paper_alerts WHERE symbol = ? AND status = 'active' AND target_price BETWEEN ? AND ?",
        (symbol, lo, hi)
    ).fetchall()
    for a in active_alerts:
        conn.execute(
            "UPDATE paper_alerts SET status = 'triggered', triggered_at = ? WHERE id = ?",
            (datetime.datetime.now(datetime.timezone.utc).isoformat(), a["id"])
        )
    if active_alerts:
        conn.commit()


# --- Background monitoring: pending entries, TP/SL, alerts ---------------------

def process_wallet_positions(wallet):
    conn = get_db()

    pending = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? AND status = 'pending_entry'", (wallet,)
    ).fetchall()
    for p in pending:
        price = get_price(p["symbol"])
        if price is None:
            continue
        triggered = False
        if p["entry_type"] == "limit":
            # Limit: long buys the dip (price falls to/below target), short sells the rally (price rises to/above target)
            if p["direction"] == "long" and price <= p["entry_price"]:
                triggered = True
            elif p["direction"] == "short" and price >= p["entry_price"]:
                triggered = True
        elif p["entry_type"] == "stop":
            # Stop: long enters on a breakout up, short enters on a breakdown down
            if p["direction"] == "long" and price >= p["entry_price"]:
                triggered = True
            elif p["direction"] == "short" and price <= p["entry_price"]:
                triggered = True
        if triggered:
            conn.execute(
                "UPDATE paper_positions SET status = 'open', entry_price = ?, opened_at = ? WHERE id = ?",
                (price, datetime.datetime.now(datetime.timezone.utc).isoformat(), p["id"])
            )
            conn.commit()

    open_positions = conn.execute(
        "SELECT * FROM paper_positions WHERE wallet = ? AND status = 'open'", (wallet,)
    ).fetchall()
    for p in open_positions:
        price = get_price(p["symbol"])
        if price is None:
            continue
        hit_tp = p["take_profit"] and (
            (p["direction"] == "long" and price >= p["take_profit"]) or
            (p["direction"] == "short" and price <= p["take_profit"])
        )
        hit_sl = p["stop_loss"] and (
            (p["direction"] == "long" and price <= p["stop_loss"]) or
            (p["direction"] == "short" and price >= p["stop_loss"])
        )
        if hit_tp or hit_sl:
            pnl = _calc_pnl(p["direction"], p["entry_price"], price, p["size_usd"])
            returned_amount = p["size_usd"] + pnl
            conn.execute("UPDATE paper_accounts SET balance_usd = balance_usd + ? WHERE wallet = ?",
                         (returned_amount, wallet))
            conn.execute(
                "UPDATE paper_positions SET status = 'closed', close_price = ?, pnl_usd = ?, closed_at = ? WHERE id = ?",
                (price, pnl, datetime.datetime.now(datetime.timezone.utc).isoformat(), p["id"])
            )
            conn.commit()

    conn.close()


def process_all_wallets():
    conn = get_db()
    wallets = [r["wallet"] for r in conn.execute(
        "SELECT DISTINCT wallet FROM paper_positions WHERE status IN ('pending_entry', 'open')"
    ).fetchall()]

    # Update alert crossing state for every symbol currently in use
    for symbol in SYMBOL_TO_COINGECKO:
        price = get_price(symbol)
        if price is not None:
            _check_alerts_for_symbol(conn, symbol, price)
    conn.close()

    for w in wallets:
        try:
            process_wallet_positions(w)
        except Exception:
            pass


def start_background_checker(interval_seconds=15):
    def loop():
        while True:
            time.sleep(interval_seconds)
            try:
                process_all_wallets()
            except Exception:
                pass
    t = threading.Thread(target=loop, daemon=True)
    t.start()
