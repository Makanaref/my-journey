from flask import Flask, render_template, request, jsonify, abort, session, redirect, url_for
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
import requests
import os
import sqlite3
import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import uuid
import json
import hmac
import paper_trading

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")

csp = {
    'default-src': "'self'",
    'style-src': ["'self'", "'unsafe-inline'"],
    'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
    'img-src': ["'self'", "data:", "https:"],
    'font-src': ["'self'", "https:"],
    'connect-src': ["'self'", "https:"],
    'frame-src': ["https://transferto.xyz", "https://li.fi", "https://jumper.exchange"],
}
Talisman(app, content_security_policy=csp, force_https=False)

csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "d3dff36f2d219ec36f5c48b6c6bb4819")

DB_PATH = os.environ.get("DB_PATH", "messages.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS short_links (
            code TEXT PRIMARY KEY,
            target_url TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            network TEXT NOT NULL,
            nft_contract TEXT NOT NULL,
            token_id TEXT NOT NULL,
            bidder_address TEXT NOT NULL,
            amount TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

paper_trading.init_paper_trading(DB_PATH)
paper_trading.init_paper_tables()
paper_trading.start_background_checker()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-this-password")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated
@app.route("/api/bid/place", methods=["POST"])
@limiter.limit("30 per hour")
def place_bid():
    data = request.get_json(force=True, silent=True) or {}
    network = (data.get("network") or "").strip()
    nft_contract = (data.get("nft_contract") or "").strip()
    token_id = str(data.get("token_id") or "").strip()
    bidder_address = (data.get("bidder_address") or "").strip()
    amount = (data.get("amount") or "").strip()

    if not all([network, nft_contract, token_id, bidder_address, amount]):
        return jsonify({"error": "Missing fields"}), 400
    try:
        if float(amount) <= 0:
            return jsonify({"error": "Invalid amount"}), 400
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO bids (network, nft_contract, token_id, bidder_address, amount, status, created_at) VALUES (?,?,?,?,?,?,?)",
        (network, nft_contract.lower(), token_id, bidder_address.lower(), amount, "pending", datetime.datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/api/bid/list")
def list_bids():
    network = (request.args.get("network") or "").strip()
    nft_contract = (request.args.get("nft_contract") or "").strip().lower()
    token_id = str(request.args.get("token_id") or "").strip()

    conn = get_db()
    rows = conn.execute(
        "SELECT id, bidder_address, amount, status, created_at FROM bids WHERE network=? AND nft_contract=? AND token_id=? ORDER BY id DESC",
        (network, nft_contract, token_id)
    ).fetchall()
    conn.close()
    return jsonify({"bids": [dict(r) for r in rows]})

@app.route("/api/bid/respond", methods=["POST"])
@limiter.limit("30 per hour")
def respond_bid():
    data = request.get_json(force=True, silent=True) or {}
    bid_id = data.get("bid_id")
    action = (data.get("action") or "").strip()
    seller_address = (data.get("seller_address") or "").strip().lower()

    if not bid_id or action not in ("accept", "reject"):
        return jsonify({"error": "Invalid request"}), 400

    conn = get_db()
    bid = conn.execute("SELECT * FROM bids WHERE id=?", (bid_id,)).fetchone()
    if not bid:
        conn.close()
        return jsonify({"error": "Bid not found"}), 404

    new_status = "accepted" if action == "accept" else "rejected"
    conn.execute("UPDATE bids SET status=? WHERE id=?", (new_status, bid_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "status": new_status})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")

@app.route("/currency")
def currency():
    return render_template("currency.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

@app.route("/converter")
def converter():
    return render_template("converter.html")

@app.route("/reminder")
def reminder():
    return render_template("reminder.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/oracle")
def oracle():
    return render_template("oracle.html")
@app.route("/games")
def games():
    return render_template("games.html")
@app.route("/mint")
def mint():
    return render_template("mint.html")
@app.route("/domain")
def domain():
    return render_template("domain.html")
@app.route("/flip")
def flip():
    return render_template("flip.html")
@app.route("/mint-nft")
def mint_nft():
    return render_template("mint_nft.html")
@app.route("/marketplace")
def marketplace():
    return render_template("marketplace.html")
@app.route("/my-nfts")
def my_nfts():
    return render_template("my_nfts.html")

@app.route("/my-store")
def my_store():
    return render_template("my_store.html")
@app.route("/api/scan-wallet")
@limiter.limit("10 per minute")
def scan_wallet():
    account = request.args.get("account", "").strip()
    if not account or len(account) != 42 or not account.startswith("0x"):
        return jsonify({"error": "Invalid address"}), 400
    try:
        from indexer import scan_all
        result = scan_all(account)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/gm")
def gm():
    return render_template("gm.html")

@app.route("/get-weather")
@limiter.limit("30 per minute")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city or len(city) > 100:
        return jsonify({"error": "Invalid city name"}), 400
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
    except Exception:
        return jsonify({"error": "Service unavailable"}), 503
    if data.get("cod") == 200:
        return jsonify({
            "name": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        })
    else:
        return jsonify({"error": "City not found"}), 404

@app.route("/get-currency")
@limiter.limit("30 per minute")
def get_currency():
    base = request.args.get("base", "").strip().upper()
    target = request.args.get("target", "").strip().upper()
    try:
        amount = float(request.args.get("amount", 1))
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400
    if not base or not target or len(base) > 5 or len(target) > 5:
        return jsonify({"error": "Invalid currency"}), 400
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception:
        return jsonify({"error": "Service unavailable"}), 503
    if target in data.get("rates", {}):
        rate = data["rates"][target]
        result = round(amount * rate, 2)
        return jsonify({"rate": rate, "result": result})
    else:
        return jsonify({"error": "Currency not found"}), 404

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "nft_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "metadata"), exist_ok=True)

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXT

@app.route("/api/nft/upload-image", methods=["POST"])
@csrf.exempt
@limiter.limit("20 per hour")
def upload_nft_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    file = request.files["image"]
    if file.filename == "" or not allowed_image(file.filename):
        return jsonify({"error": "Invalid image file"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_name)
    file.save(filepath)

    try:
        from PIL import Image
        with Image.open(filepath) as img:
            img.verify()
    except Exception:
        os.remove(filepath)
        return jsonify({"error": "Invalid image file"}), 400

    scheme = "https"
    image_url = f"{scheme}://{request.host}/nft-image/{unique_name}"
    return jsonify({"image_url": image_url})

@app.route("/b20")
def b20():
    return render_template("b20.html")

@app.route("/nft-image/<filename>")
def serve_nft_image(filename):
    safe_name = secure_filename(filename)
    filepath = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.isfile(filepath):
        abort(404)
    from flask import send_file
    return send_file(filepath)

@app.route("/api/nft/create-metadata", methods=["POST"])
@csrf.exempt
@limiter.limit("20 per hour")
def create_nft_metadata():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    image_url = (data.get("image_url") or "").strip()

    if not name or not image_url:
        return jsonify({"error": "Name and image are required"}), 400
    if len(name) > 100 or len(description) > 1000:
        return jsonify({"error": "Input too long"}), 400

    metadata = {
        "name": name,
        "description": description,
        "image": image_url
    }

    unique_name = f"{uuid.uuid4().hex}.json"
    filepath = os.path.join(UPLOAD_DIR, "metadata", unique_name)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    scheme2 = "https"
    metadata_url = f"{scheme2}://{request.host}/nft-metadata/{unique_name}"
    return jsonify({"metadata_url": metadata_url})

@app.route("/nft-metadata/<filename>")
def serve_nft_metadata(filename):
    safe_name = secure_filename(filename)
    filepath = os.path.join(UPLOAD_DIR, "metadata", safe_name)
    if not os.path.isfile(filepath):
        abort(404)
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    response = app.response_class(data, mimetype="application/json")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/api/shorten", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per hour")
def api_shorten():
    data = request.get_json(silent=True) or {}
    target_url = (data.get("url") or "").strip()
    if not target_url or len(target_url) > 2000:
        return jsonify({"error": "Invalid URL"}), 400
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        return jsonify({"error": "Invalid URL"}), 400

    code = uuid.uuid4().hex[:8]
    conn = get_db()
    conn.execute(
        "INSERT INTO short_links (code, target_url, created_at) VALUES (?, ?, ?)",
        (code, target_url, datetime.datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

    scheme = "https"
    short_url = f"{scheme}://{request.host}/s/{code}"
    return jsonify({"short_url": short_url})

@app.route("/s/<code>")
def resolve_short_link(code):
    conn = get_db()
    row = conn.execute("SELECT target_url FROM short_links WHERE code = ?", (code,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    return redirect(row["target_url"])

@app.route("/api/contact", methods=["POST"])
@csrf.exempt
@limiter.limit("10 per hour")
def api_contact():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400
    if len(name) > 100 or len(email) > 150 or len(message) > 3000:
        return jsonify({"error": "Input too long"}), 400
    conn = get_db()
    conn.execute(
        "INSERT INTO messages (name, email, message, created_at, is_read) VALUES (?, ?, ?, ?, 0)",
        (name, email, message, datetime.datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        valid_user = hmac.compare_digest(username, ADMIN_USERNAME)
        valid_pass = hmac.compare_digest(password, ADMIN_PASSWORD)
        if valid_user and valid_pass:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        error = "Invalid username or password"
    return render_template("admin_login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
@login_required
def admin_panel():
    conn = get_db()
    rows = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", messages=rows)

@app.route("/admin/read/<int:msg_id>", methods=["POST"])
@login_required
def admin_mark_read(msg_id):
    conn = get_db()
    conn.execute("UPDATE messages SET is_read = 1 WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_panel"))

@app.route("/admin/delete/<int:msg_id>", methods=["POST"])
@login_required
def admin_delete(msg_id):
    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_panel"))

@app.route("/<page>")
def generic_page(page):
    allowed = [
        "todo", "timer", "stopwatch", "wordcount", "speedtest",
        "password", "color", "tip", "bmi", "age",
        "dice", "coin", "guess", "random", "quote", "counter",
        "blog", "skills", "timeline", "faq"
    ]
    if page in allowed:
        try:
            return render_template(f"{page}.html")
        except:
            abort(404)
    abort(404)


@app.route("/swap")
def swap():
    return render_template("swap.html")
@app.route("/networks")
def networks():
    return render_template("networks.html")
@app.route("/paper-trade")
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


@app.route("/api/paper/klines")
@limiter.limit("60 per minute")
def api_paper_klines():
    symbol = request.args.get("symbol", "").strip().upper()
    if symbol not in ("BTC", "ETH"):
        return jsonify({"error": "Unsupported symbol"}), 400
    candles = paper_trading.get_klines(symbol)
    if candles is None:
        return jsonify({"error": "Chart data unavailable"}), 503
    return jsonify({"symbol": symbol, "candles": candles})


@app.route("/api/paper/live-price")
@limiter.limit("120 per minute")
def api_paper_live_price():
    symbol = request.args.get("symbol", "").strip().upper()
    if symbol not in ("BTC", "ETH"):
        return jsonify({"error": "Unsupported symbol"}), 400
    price = paper_trading.get_live_ticker_price(symbol)
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



@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"error": "Too many requests, slow down!"}), 429

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    from waitress import serve
    serve(app, host="0.0.0.0", port=port, threads=16, connection_limit=100, channel_timeout=60, cleanup_interval=10)