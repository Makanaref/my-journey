import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''@app.route("/mint")
def mint():
    return render_template("mint.html")'''

new_block = '''@app.route("/mint")
def mint():
    return render_template("mint.html")
@app.route("/flip")
def flip():
    return render_template("flip.html")'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: /flip route added.")
