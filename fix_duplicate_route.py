import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''@app.route("/my-nfts")
def my_nfts():
    return render_template("my_nfts.html")
@app.route("/my-nfts")
def my_nfts():
    return render_template("my_nfts.html")'''

new_block = '''@app.route("/my-nfts")
def my_nfts():
    return render_template("my_nfts.html")'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: duplicate route removed.")
