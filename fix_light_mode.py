import io

path = "templates/base.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """body.light input, body.light textarea, body.light select { background: #e5dfd8; color: #2a2015; border-color: #cfc8c0; }"""

new_block = """body.light input, body.light textarea, body.light select { background: #e5dfd8; color: #2a2015; border-color: #cfc8c0; }
body.light .content { filter: invert(1) hue-rotate(180deg); transition: filter 0.3s ease; }
body.light .content img, body.light .content video { filter: invert(1) hue-rotate(180deg); }"""

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Light mode content inversion applied.")
