import io

path = "templates/gm.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """            const gasPricePercent = {
                lamina1: 100,
                nexus: 25,
                ink: 25,
                base: 9
            };"""

new_block = """            const gasPricePercent = {
                lamina1: 100,
                nexus: 25,
                ink: 25,
                base: 15
            };"""

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Base percentage adjusted to 15%.")
