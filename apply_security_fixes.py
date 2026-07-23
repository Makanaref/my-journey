import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add hmac import after "import json"
content = content.replace(
    "import json\n",
    "import json\nimport hmac\n",
    1
)

# 2. Replace admin_login route: add rate limit + timing-safe comparison
old_login = '''@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        error = "Invalid username or password"
    return render_template("admin_login.html", error=error)'''

new_login = '''@app.route("/admin/login", methods=["GET", "POST"])
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
    return render_template("admin_login.html", error=error)'''

if old_login not in content:
    raise SystemExit("ERROR: admin_login block not found, aborting.")
content = content.replace(old_login, new_login, 1)

# 3. Replace upload_nft_image route: verify actual image content
old_upload = '''@app.route("/api/nft/upload-image", methods=["POST"])
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

    scheme = "https" if request.headers.get("X-Forwarded-Proto", "http") == "https" else request.scheme
    image_url = f"{scheme}://{request.host}/nft-image/{unique_name}"
    return jsonify({"image_url": image_url})'''

new_upload = '''@app.route("/api/nft/upload-image", methods=["POST"])
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

    # Verify the uploaded file is actually a valid image
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            img.verify()
    except Exception:
        os.remove(filepath)
        return jsonify({"error": "Invalid image file"}), 400

    scheme = "https" if request.headers.get("X-Forwarded-Proto", "http") == "https" else request.scheme
    image_url = f"{scheme}://{request.host}/nft-image/{unique_name}"
    return jsonify({"image_url": image_url})'''

if old_upload not in content:
    raise SystemExit("ERROR: upload_nft_image block not found, aborting.")
content = content.replace(old_upload, new_upload, 1)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. app.py updated successfully.")
