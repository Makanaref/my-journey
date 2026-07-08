import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = "from functools import wraps"
new1 = "from functools import wraps\nfrom werkzeug.utils import secure_filename\nimport uuid\nimport json"

if old1 not in content:
    print("ERROR: import anchor not found!")
else:
    content = content.replace(old1, new1, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: NFT imports added.")
