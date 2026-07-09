import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = '    image_url = request.host_url.rstrip("/") + "/nft-image/" + unique_name'
new1 = '''    scheme = "https" if request.headers.get("X-Forwarded-Proto", "http") == "https" else request.scheme
    image_url = f"{scheme}://{request.host}/nft-image/{unique_name}"'''

old2 = '    metadata_url = request.host_url.rstrip("/") + "/nft-metadata/" + unique_name'
new2 = '''    scheme2 = "https" if request.headers.get("X-Forwarded-Proto", "http") == "https" else request.scheme
    metadata_url = f"{scheme2}://{request.host}/nft-metadata/{unique_name}"'''

errors = []
if old1 not in content: errors.append("part1 (image_url)")
if old2 not in content: errors.append("part2 (metadata_url)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: image_url and metadata_url now always use https.")
