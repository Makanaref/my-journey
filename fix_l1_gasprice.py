import io

path = "templates/gm.html"

old_block = """            const gasPriceHex = await provider.send("eth_gasPrice", []);
            const networkGasPrice = BigInt(gasPriceHex);
            const gasPrice = networkGasPrice * 25n / 100n;
            const txOverrides = { gasPrice: gasPrice };
            if (currentNet === "lamina1") {
                txOverrides.gasLimit = 150000;
            }
            const tx = await contract.sayGM(txOverrides);"""

new_block = """            const gasPriceHex = await provider.send("eth_gasPrice", []);
            const networkGasPrice = BigInt(gasPriceHex);
            const gasPrice = currentNet === "lamina1"
                ? networkGasPrice
                : networkGasPrice * 25n / 100n;
            const txOverrides = { gasPrice: gasPrice };
            if (currentNet === "lamina1") {
                txOverrides.gasLimit = 150000;
            }
            const tx = await contract.sayGM(txOverrides);"""

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_block not in content:
    print("ERROR: old_block not found! No changes made.")
else:
    content = content.replace(old_block, new_block)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Full gasPrice restored for Lamina1 only.")
