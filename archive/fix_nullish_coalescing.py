import io

files = ["templates/flip.html", "templates/gm.html", "templates/mint.html", "templates/mint_nft.html"]

old_line = "const percent = BigInt(gasPricePercent[currentNet] ?? 25);"
new_line = "const percent = BigInt(gasPricePercent[currentNet] !== undefined ? gasPricePercent[currentNet] : 25);"

for path in files:
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()
    count = content.count(old_line)
    if count == 0:
        print(f"WARNING: no match in {path}")
        continue
    content = content.replace(old_line, new_line)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"SUCCESS: {path} fixed ({count} occurrence(s)).")
