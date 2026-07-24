with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import right after the other imports (after "import json")
old_imports = "import json\nimport hmac"
new_imports = "import json\nimport hmac\nimport paper_trading"
if old_imports not in content:
    raise SystemExit("ERROR: imports anchor not found, aborting.")
content = content.replace(old_imports, new_imports, 1)

# 2. Initialize paper trading right after init_db() is called
old_init = "init_db()"
new_init = """init_db()

paper_trading.init_paper_trading(DB_PATH)
paper_trading.init_paper_tables()
paper_trading.start_background_checker()"""
if old_init not in content:
    raise SystemExit("ERROR: init_db() anchor not found, aborting.")
content = content.replace(old_init, new_init, 1)

# 3. Add the page route and all API routes right before the 404 handler
old_404_anchor = "@app.errorhandler(404)\ndef not_found(e):"
new_routes_and_404 = '''@app.route("/paper-trade")
def paper_trade():
    return render_template("paper_trade.html")


@app.route("/api/paper/price")
@limiter.limit("60 per minute")
def api_paper_price():
    symbol = request.args.get("symbol", "").strip().upper()
    if symbol not in paper_trading.SYMBOL_TO_COINGECKO:
        return jsonify({"error": "Unsupported symbol"}), 400
    price = paper_trading.get_price(symbol)
    if price is None:
        return jsonify({"error": "Price unavailable"}), 503
    return jsonify({"symbol": symbol, "price": price})


@app.route("/api/paper/start", methods=["POST"])
@csrf.exempt
@limiter.limit("10 per minute")
def api_paper_start():
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    try:
        starting_balance = float(data.get("starting_balance", 1000))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid starting balance"}), 400
    account = paper_trading.get_or_create_account(wallet, starting_balance)
    return jsonify(account)


@app.route("/api/paper/account")
@limiter.limit("60 per minute")
def api_paper_account():
    wallet = (request.args.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    paper_trading.process_wallet_positions(wallet)
    snapshot = paper_trading.get_account_snapshot(wallet)
    if snapshot is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(snapshot)


@app.route("/api/paper/balance/adjust", methods=["POST"])
@csrf.exempt
@limiter.limit("20 per minute")
def api_paper_balance_adjust():
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    try:
        delta = float(data.get("delta"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid delta"}), 400
    paper_trading.get_or_create_account(wallet)
    result, status = paper_trading.adjust_balance(wallet, delta)
    return jsonify(result), status


@app.route("/api/paper/position", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per minute")
def api_paper_open_position():
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400

    symbol = (data.get("symbol") or "").strip()
    direction = (data.get("direction") or "").strip()
    entry_type = (data.get("entry_type") or "").strip()
    network = (data.get("network") or "").strip()
    fee_tx_hash = (data.get("fee_tx_hash") or "").strip()

    try:
        size_usd = float(data.get("size_usd"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid position size"}), 400

    entry_price = data.get("entry_price")
    entry_price = float(entry_price) if entry_price not in (None, "") else None
    take_profit = data.get("take_profit")
    take_profit = float(take_profit) if take_profit not in (None, "") else None
    stop_loss = data.get("stop_loss")
    stop_loss = float(stop_loss) if stop_loss not in (None, "") else None

    if not fee_tx_hash or not fee_tx_hash.startswith("0x") or len(fee_tx_hash) != 66:
        return jsonify({"error": "Valid fee transaction hash required"}), 400

    result, status = paper_trading.open_position(
        wallet, symbol, direction, size_usd, entry_type,
        entry_price=entry_price, take_profit=take_profit, stop_loss=stop_loss,
        network=network, fee_tx_hash=fee_tx_hash
    )
    return jsonify(result), status


@app.route("/api/paper/position/<int:position_id>/close", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per minute")
def api_paper_close_position(position_id):
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    result, status = paper_trading.close_position(wallet, position_id)
    return jsonify(result), status


@app.route("/api/paper/position/<int:position_id>/cancel", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per minute")
def api_paper_cancel_position(position_id):
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    result, status = paper_trading.cancel_pending_position(wallet, position_id)
    return jsonify(result), status


@app.route("/api/paper/positions")
@limiter.limit("60 per minute")
def api_paper_positions():
    wallet = (request.args.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    return jsonify(paper_trading.get_positions(wallet))


@app.route("/api/paper/alert", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per minute")
def api_paper_create_alert():
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    symbol = (data.get("symbol") or "").strip()
    try:
        target_price = float(data.get("target_price"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid target price"}), 400
    result, status = paper_trading.create_alert(wallet, symbol, target_price)
    return jsonify(result), status


@app.route("/api/paper/alerts")
@limiter.limit("60 per minute")
def api_paper_alerts():
    wallet = (request.args.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    return jsonify(paper_trading.get_alerts(wallet))


@app.route("/api/paper/alert/<int:alert_id>/dismiss", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per minute")
def api_paper_dismiss_alert(alert_id):
    data = request.get_json(silent=True) or {}
    wallet = (data.get("wallet") or "").strip().lower()
    if not wallet or len(wallet) != 42 or not wallet.startswith("0x"):
        return jsonify({"error": "Invalid wallet"}), 400
    result, status = paper_trading.dismiss_alert(wallet, alert_id)
    return jsonify(result), status


@app.errorhandler(404)
def not_found(e):'''

if old_404_anchor not in content:
    raise SystemExit("ERROR: 404 handler anchor not found, aborting.")
content = content.replace(old_404_anchor, new_routes_and_404, 1)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. app.py wired up with paper trading routes.")
