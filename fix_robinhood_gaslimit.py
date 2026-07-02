import io

path = "templates/gm.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """            const txOverrides = { gasPrice: gasPrice };
            if (currentNet === "lamina1") {
                txOverrides.gasLimit = 150000;
            }
            const tx = await contract.sayGM(txOverrides);"""

new_block = """            const txOverrides = { gasPrice: gasPrice };
            if (currentNet === "lamina1" || currentNet === "robinhood") {
                txOverrides.gasLimit = 150000;
            }
            const tx = await contract.sayGM(txOverrides);"""

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Fixed gasLimit added for Robinhood too.")
