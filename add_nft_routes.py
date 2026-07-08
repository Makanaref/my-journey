import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''@app.route("/api/contact", methods=["POST"])'''

new_block = '''UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "nft_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "metadata"), exist_ok=True)

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXT

@app.route("/api/nft/upload-image", methods=["POST"])
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

    image_url = request.host_url.rstrip("/") + "/nft-image/" + unique_name
    return jsonify({"image_url": image_url})

@app.route("/nft-image/<filename>")
def serve_nft_image(filename):
    safe_name = secure_filename(filename)
    filepath = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.isfile(filepath):
        abort(404)
    from flask import send_file
    return send_file(filepath)

@app.route("/api/nft/create-metadata", methods=["POST"])
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

    metadata_url = request.host_url.rstrip("/") + "/nft-metadata/" + unique_name
    return jsonify({"metadata_url": metadata_url})

@app.route("/nft-metadata/<filename>")
def serve_nft_metadata(filename):
    safe_name = secure_filename(filename)
    filepath = os.path.join(UPLOAD_DIR, "metadata", safe_name)
    if not os.path.isfile(filepath):
        abort(404)
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    return app.response_class(data, mimetype="application/json")

@app.route("/api/contact", methods=["POST"])'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: NFT upload/metadata routes added.")
