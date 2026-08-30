from flask import Flask, render_template, request, jsonify, abort, session, redirect, url_for
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
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
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.secret_key = require_env("SECRET_KEY")

csp = {
    'default-src': "'self'",
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],
    'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'", "blob:", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://binaries.soliditylang.org", "https://static.cloudflareinsights.com"],
    'worker-src': ["'self'", "blob:"],
    'img-src': ["'self'", "data:", "blob:", "https:"],
    'font-src': ["'self'", "https:", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
    'connect-src': ["'self'", "https:", "https://cloudflareinsights.com"],
    'frame-src': ["'self'", "https://transferto.xyz", "https://li.fi", "https://jumper.exchange"],
}
Talisman(app, content_security_policy=csp, force_https=False)

csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

WEATHER_API_KEY = require_env("WEATHER_API_KEY")
PINATA_API_KEY = require_env("PINATA_API_KEY")
PINATA_SECRET_KEY = require_env("PINATA_SECRET_KEY")

IPFS_API_URL = os.environ.get("IPFS_API_URL", "http://127.0.0.1:5001")
IPFS_GATEWAY_URL = os.environ.get("IPFS_GATEWAY_URL", "http://127.0.0.1:8080")

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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            display_name TEXT NOT NULL,
            text TEXT NOT NULL,
            signature TEXT NOT NULL,
            signed_timestamp TEXT NOT NULL,
            created_at TEXT NOT NULL,
            reply_to_name TEXT,
            reply_to_text TEXT,
            reply_to_address TEXT
        )
    """)
    for stmt in [
        "ALTER TABLE chat_messages ADD COLUMN signature TEXT",
        "ALTER TABLE chat_messages ADD COLUMN signed_timestamp TEXT",
        "ALTER TABLE chat_messages ADD COLUMN reply_to_name TEXT",
        "ALTER TABLE chat_messages ADD COLUMN reply_to_text TEXT",
        "ALTER TABLE chat_messages ADD COLUMN reply_to_address TEXT"
    ]:
        try:
            conn.execute(stmt)
        except sqlite3.OperationalError:
            pass
    try:
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_chat_signature ON chat_messages(signature)")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

init_db()

paper_trading.init_paper_trading(DB_PATH)
paper_trading.init_paper_tables()
paper_trading.start_background_checker()

ADMIN_USERNAME = require_env("ADMIN_USERNAME")
ADMIN_PASSWORD = require_env("ADMIN_PASSWORD")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/api/bid/place", methods=["POST"])
@csrf.exempt
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
     (network, nft_contract.lower(), token_id, bidder_address.lower(), amount, "pending", datetime.datetime.now(datetime.timezone.utc).isoformat())
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
@csrf.exempt
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
@app.route("/deploy-contract")
def deploy_contract():
    return render_template("deploy_contract.html")
@app.route("/flip")
def flip():
    return render_template("flip.html")
@app.route("/mint-nft")
def mint_nft():
    return render_template("mint_nft.html")
@app.route("/sgm-drop")
def sgm_drop():
    return render_template("sgm_drop.html")
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
ALLOWED_ANIMATION_EXT = {"html", "htm"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXT

def allowed_animation(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_ANIMATION_EXT

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

@app.route("/api/nft/upload-animation", methods=["POST"])
@csrf.exempt
@limiter.limit("20 per hour")
def upload_nft_animation():
    if "animation" not in request.files:
        return jsonify({"error": "No animation file provided"}), 400
    file = request.files["animation"]
    if file.filename == "" or not allowed_animation(file.filename):
        return jsonify({"error": "Invalid animation file"}), 400

    unique_name = f"{uuid.uuid4().hex}.html"
    filepath = os.path.join(UPLOAD_DIR, unique_name)
    file.save(filepath)

    scheme = "https"
    animation_url = f"{scheme}://{request.host}/nft-animation/{unique_name}"
    return jsonify({"animation_url": animation_url})

@app.route("/nft-animation/<filename>")
@limiter.limit("300 per minute")
def serve_nft_animation(filename):
    safe_name = secure_filename(filename)
    filepath = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.isfile(filepath):
        abort(404)
    from flask import Response
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        html_content = f.read()
    response = Response(html_content, mimetype="text/html")
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; "
        "img-src data: blob: https: http:; "
        "media-src data: blob: https: http:; "
        "style-src 'unsafe-inline' https: http:; "
        "font-src data: https: http:; "
        "script-src 'unsafe-inline' 'unsafe-eval' blob: https: http:; "
        "connect-src https: http: data: blob:; "
        "frame-ancestors 'self'"
    )
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

import ipaddress
import socket
from urllib.parse import urlparse

ALLOWED_PROXY_SCHEMES = {"http", "https"}

def is_public_host(hostname):
    try:
        infos = socket.getaddrinfo(hostname, None)
    except Exception:
        return False
    for info in infos:
        ip = info[4][0]
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False
        if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved or addr.is_multicast:
            return False
    return True

SELF_HOSTED_DOMAINS = {"sgmhub.ir", "www.sgmhub.ir"}

@app.route("/api/image-proxy")
@limiter.limit("120 per minute")
def image_proxy():
    target_url = (request.args.get("url") or "").strip()
    if not target_url or len(target_url) > 2000:
        return jsonify({"error": "Invalid URL"}), 400
    parsed = urlparse(target_url)
    if parsed.scheme not in ALLOWED_PROXY_SCHEMES or not parsed.hostname:
        return jsonify({"error": "Invalid URL"}), 400

    host_lower = parsed.hostname.lower()
    site_host = request.host.split(":")[0].lower()
    is_self_hosted = host_lower in SELF_HOSTED_DOMAINS or host_lower == site_host
    if is_self_hosted:
        path = parsed.path
        if path.startswith("/nft-image/"):
            filename = secure_filename(path[len("/nft-image/"):])
            filepath = os.path.join(UPLOAD_DIR, filename)
        elif path.startswith("/nft-metadata/"):
            filename = secure_filename(path[len("/nft-metadata/"):])
            filepath = os.path.join(UPLOAD_DIR, "metadata", filename)
        else:
            return jsonify({"error": "Unknown self-hosted path", "path": path}), 400
        if not os.path.isfile(filepath):
            return jsonify({"error": "Not found"}), 404
        from flask import send_file
        resp = send_file(filepath)
        resp.headers["Cache-Control"] = "public, max-age=86400"
        resp.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        return resp

    if not is_public_host(parsed.hostname):
        return jsonify({"error": "Invalid URL"}), 400
    try:
        upstream = requests.get(
            target_url, timeout=8, stream=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "image/*,*/*;q=0.8"
            }
        )
    except Exception:
        return jsonify({"error": "Fetch failed"}), 502
    content_type = upstream.headers.get("Content-Type", "").split(";")[0].strip().lower()
    max_bytes = 8 * 1024 * 1024
    chunks = []
    total = 0
    for chunk in upstream.iter_content(chunk_size=65536):
        total += len(chunk)
        if total > max_bytes:
            upstream.close()
            return jsonify({"error": "Image too large"}), 413
        chunks.append(chunk)
    upstream.close()
    body = b"".join(chunks)

    def sniff_image_type(data):
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if data.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
            return "image/gif"
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            return "image/webp"
        head = data[:512].lstrip().lower()
        if head.startswith(b"<svg") or (head.startswith(b"<?xml") and b"<svg" in data[:2048].lower()):
            return "image/svg+xml"
        return None

    if content_type.startswith("image/"):
        final_type = content_type
    else:
        final_type = sniff_image_type(body)
        if not final_type:
            return jsonify({
                "error": "Not an image",
                "content_type": content_type,
                "status": upstream.status_code,
                "fetched_url": target_url,
                "body_preview": body[:200].decode("utf-8", errors="replace")
            }), 415

    from flask import Response
    resp = Response(body, mimetype=final_type)
    resp.headers["Cache-Control"] = "public, max-age=86400"
    resp.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return resp

@app.route("/b20")
def b20():
    return render_template("b20.html")

@app.route("/api/ipfs/upload-file", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per hour")
def ipfs_upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    try:
        files = {"file": (secure_filename(file.filename), file.stream, file.mimetype)}
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_KEY
        }
        response = requests.post(
            "https://api.pinata.cloud/pinning/pinFileToIPFS",
            files=files, headers=headers, timeout=30
        )
        if response.status_code != 200:
            return jsonify({"error": "IPFS upload failed"}), 502
        return jsonify({"ipfs_hash": response.json().get("IpfsHash")})
    except Exception:
        return jsonify({"error": "IPFS upload failed"}), 502

@app.route("/api/ipfs/upload-json", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per hour")
def ipfs_upload_json():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    try:
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_KEY,
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://api.pinata.cloud/pinning/pinJSONToIPFS",
            json=data, headers=headers, timeout=30
        )
        if response.status_code != 200:
            return jsonify({"error": "IPFS upload failed"}), 502
        return jsonify({"ipfs_hash": response.json().get("IpfsHash")})
    except Exception:
        return jsonify({"error": "IPFS upload failed"}), 502

@app.route("/api/ipfs-local/upload-file", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per hour")
def ipfs_local_upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    try:
        files = {"file": (secure_filename(file.filename), file.stream, file.mimetype)}
        response = requests.post(
            f"{IPFS_API_URL}/api/v0/add",
            files=files,
            params={"pin": "true", "cid-version": "1"},
            timeout=60
        )
        if response.status_code != 200:
            return jsonify({"error": "Local IPFS upload failed"}), 502
        result = response.json()
        return jsonify({"ipfs_hash": result.get("Hash")})
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Local IPFS daemon unreachable"}), 503
    except Exception:
        return jsonify({"error": "Local IPFS upload failed"}), 502

@app.route("/api/ipfs-local/upload-json", methods=["POST"])
@csrf.exempt
@limiter.limit("30 per hour")
def ipfs_local_upload_json():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    try:
        json_bytes = json.dumps(data).encode("utf-8")
        files = {"file": ("metadata.json", json_bytes, "application/json")}
        response = requests.post(
            f"{IPFS_API_URL}/api/v0/add",
            files=files,
            params={"pin": "true", "cid-version": "1"},
            timeout=60
        )
        if response.status_code != 200:
            return jsonify({"error": "Local IPFS upload failed"}), 502
        result = response.json()
        return jsonify({"ipfs_hash": result.get("Hash")})
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Local IPFS daemon unreachable"}), 503
    except Exception:
        return jsonify({"error": "Local IPFS upload failed"}), 502

@app.route("/api/ipfs-local/status")
@limiter.limit("30 per minute")
def ipfs_local_status():
    try:
        response = requests.post(f"{IPFS_API_URL}/api/v0/version", timeout=5)
        if response.status_code == 200:
            return jsonify({"online": True, "version": response.json().get("Version")})
        return jsonify({"online": False}), 503
    except Exception:
        return jsonify({"online": False}), 503

@app.route("/ipfs-local/<cid>")
@limiter.limit("120 per minute")
def ipfs_local_gateway_proxy(cid):
    safe_cid = secure_filename(cid)
    try:
        response = requests.get(f"{IPFS_GATEWAY_URL}/ipfs/{safe_cid}", timeout=15, stream=True)
    except Exception:
        return jsonify({"error": "Local IPFS gateway unreachable"}), 502
    if response.status_code != 200:
        return jsonify({"error": "Not found on local IPFS"}), 404
    from flask import Response
    content_type = response.headers.get("Content-Type", "application/octet-stream")
    resp = Response(response.content, mimetype=content_type)
    resp.headers["Cache-Control"] = "public, max-age=86400"
    resp.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return resp

@app.route("/nft-image/<filename>")
@limiter.limit("300 per minute")
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
    animation_url = (data.get("animation_url") or "").strip()

    if not name or not image_url:
        return jsonify({"error": "Name and image are required"}), 400
    if len(name) > 100 or len(description) > 1000:
        return jsonify({"error": "Input too long"}), 400
    if len(animation_url) > 2000:
        return jsonify({"error": "Input too long"}), 400

    metadata = {
        "name": name,
        "description": description,
        "image": image_url
    }
    if animation_url:
        metadata["animation_url"] = animation_url

    unique_name = f"{uuid.uuid4().hex}.json"
    filepath = os.path.join(UPLOAD_DIR, "metadata", unique_name)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    scheme2 = "https"
    metadata_url = f"{scheme2}://{request.host}/nft-metadata/{unique_name}"
    return jsonify({"metadata_url": metadata_url})

@app.route("/nft-metadata/<filename>")
@limiter.limit("300 per minute")
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
        (code, target_url, datetime.datetime.now(datetime.timezone.utc).isoformat())
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
        (name, email, message, datetime.datetime.now(datetime.timezone.utc).isoformat())
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


def is_valid_address(addr):
    if not addr or len(addr) != 42 or not addr.startswith("0x"):
        return False
    try:
        int(addr[2:], 16)
        return True
    except ValueError:
        return False


def build_chat_signed_message(text, timestamp):
    return f"SGMHub Chat\n{text}\nTimestamp: {timestamp}"


def verify_chat_signature(address, text, timestamp, signature):
    try:
        message_text = build_chat_signed_message(text, timestamp)
        encoded = encode_defunct(text=message_text)
        recovered = Account.recover_message(encoded, signature=signature)
        return recovered.lower() == address.lower()
    except Exception:
        return False


@app.route("/api/chat/messages", methods=["GET"])
@limiter.limit("120 per minute")
def api_chat_get_messages():
    conn = get_db()
    rows = conn.execute(
        "SELECT address, display_name, text, created_at, reply_to_name, reply_to_text FROM chat_messages ORDER BY id DESC LIMIT 200"
    ).fetchall()
    conn.close()
    messages = [
        {
            "address": row["address"],
            "display_name": row["display_name"],
            "text": row["text"],
            "created_at": row["created_at"],
            "reply_to_name": row["reply_to_name"],
            "reply_to_text": row["reply_to_text"]
        }
        for row in reversed(rows)
    ]
    return jsonify({"messages": messages})


@app.route("/api/chat/replies", methods=["GET"])
@limiter.limit("60 per minute")
def api_chat_get_replies():
    address = (request.args.get("address") or "").strip().lower()
    if not is_valid_address(address):
        return jsonify({"error": "Invalid wallet address"}), 400
    conn = get_db()
    rows = conn.execute(
        "SELECT display_name, text, created_at FROM chat_messages WHERE reply_to_address = ? ORDER BY id DESC LIMIT 50",
        (address,)
    ).fetchall()
    conn.close()
    replies = [
        {"display_name": row["display_name"], "text": row["text"], "created_at": row["created_at"]}
        for row in rows
    ]
    return jsonify({"replies": replies})


@app.route("/api/chat/messages", methods=["POST"])
@csrf.exempt
@limiter.limit("15 per minute")
def api_chat_post_message():
    data = request.get_json(silent=True) or {}
    address = (data.get("address") or "").strip()
    display_name = (data.get("display_name") or "").strip()
    text = (data.get("text") or "").strip()
    signature = (data.get("signature") or "").strip()
    timestamp = (data.get("timestamp") or "").strip()
    reply_to_name = (data.get("reply_to_name") or "").strip()
    reply_to_text = (data.get("reply_to_text") or "").strip()
    reply_to_address = (data.get("reply_to_address") or "").strip()

    if not is_valid_address(address):
        return jsonify({"error": "Invalid wallet address"}), 400
    if not display_name:
        display_name = address[:6] + "..." + address[-4:]
    if not text:
        return jsonify({"error": "Message is empty"}), 400
    if len(text) > 300:
        return jsonify({"error": "Message must be 300 characters or fewer"}), 400
    if not signature or not timestamp:
        return jsonify({"error": "Missing signature"}), 400

    reply_to_name = reply_to_name[:60] if reply_to_name else None
    reply_to_text = reply_to_text[:120] if reply_to_text else None
    reply_to_address = reply_to_address.lower() if is_valid_address(reply_to_address) else None

    try:
        timestamp_ms = int(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400
    now_ms = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    if abs(now_ms - timestamp_ms) > 5 * 60 * 1000:
        return jsonify({"error": "Signature expired, please try again"}), 400

    if not verify_chat_signature(address, text, timestamp, signature):
        return jsonify({"error": "Invalid signature"}), 400

    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO chat_messages (address, display_name, text, signature, signed_timestamp, created_at, reply_to_name, reply_to_text, reply_to_address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (address.lower(), display_name, text, signature, timestamp, created_at, reply_to_name, reply_to_text, reply_to_address)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Duplicate message"}), 400
    conn.close()

    return jsonify({
        "address": address.lower(),
        "display_name": display_name,
        "text": text,
        "created_at": created_at,
        "reply_to_name": reply_to_name,
        "reply_to_text": reply_to_text
    })


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
