import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''@app.route("/debug-env")
def debug_env():
    return {"username_set": ADMIN_USERNAME, "password_length": len(ADMIN_PASSWORD)}

@app.route("/admin/login", methods=["GET", "POST"])'''

new_block = '''@app.route("/admin/login", methods=["GET", "POST"])'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: debug route removed.")
