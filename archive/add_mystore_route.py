import io

path = "app.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find('@app.route("/my-nfts")')
if idx == -1:
    print("ERROR: /my-nfts route not found as anchor!")
else:
    close_idx = content.find("\n", content.find("return render_template", idx))
    new_route = '''
@app.route("/my-store")
def my_store():
    return render_template("my_store.html")'''
    content = content[:close_idx+1] + new_route + content[close_idx+1:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: /my-store route added.")
