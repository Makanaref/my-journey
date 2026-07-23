import io

path = "templates/base.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_line = '            <a href="/b20">B20</a>'
new_line = '            <a href="/b20">B20</a>\n            <a href="/my-store">My Store</a>'

if old_line not in content:
    print("ERROR: old_line not found!")
else:
    content = content.replace(old_line, new_line, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: My Store nav link added.")
