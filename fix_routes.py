import io

path = "app.py"

old_block = """@app.route("/oracle")
def oracle():
@app.route("/games")
def games():
    return render_template("games.html")
    return render_template("oracle.html")
@app.route("/games")
def games():
    return render_template("games.html")
@app.route("/gm")"""

new_block = """@app.route("/oracle")
def oracle():
    return render_template("oracle.html")
@app.route("/games")
def games():
    return render_template("games.html")
@app.route("/gm")"""

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_block not in content:
    print("ERROR: old_block not found! No changes made.")
else:
    content = content.replace(old_block, new_block)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Routes cleaned up.")
