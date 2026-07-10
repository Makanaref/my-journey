import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''            statusEl.innerText = "Sending transaction...";
            const overrides = await getTxOverrides();
            const priceWei = priceType === "paid" ? ethers.parseEther(priceInput) : 0n;
            const tx = await factoryContract.createCollection(name, symbol, BigInt(supply), priceWei, metaData.metadata_url, overrides);'''

new_block = '''            statusEl.innerText = "Sending transaction...";
            const overrides = await getTxOverrides();
            overrides.gasLimit = 2500000;
            const priceWei = priceType === "paid" ? ethers.parseEther(priceInput) : 0n;
            const tx = await factoryContract.createCollection(name, symbol, BigInt(supply), priceWei, metaData.metadata_url, overrides);'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: createCollection gasLimit increased.")
