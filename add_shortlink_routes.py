import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''@app.route("/api/contact", methods=["POST"])'''

new_block = '''@app.route("/api/shorten", methods=["POST"])
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

    scheme = "https" if request.headers.get("X-Forwarded-Proto", "http") == "https" else request.scheme
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

@app.route("/api/contact", methods=["POST"])'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: shortlink routes added.")
