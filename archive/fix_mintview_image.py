import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''    async function loadMintView(addr, metaUrl) {
        currentCollectionAddress = addr;
        collectionContract = new ethers.Contract(addr, COLLECTION_ABI, signer);

        document.getElementById("network-card").style.display = "none";
        document.getElementById("create-panel").style.display = "none";
        document.getElementById("mycollections-panel").style.display = "none";
        document.getElementById("manage-panel").style.display = "none";
        document.getElementById("mint-view-panel").style.display = "block";

        if (metaUrl) {
            try {
                const metaRes = await fetch(metaUrl);
                const meta = await metaRes.json();
                document.getElementById("mv-image").src = meta.image || "";
                document.getElementById("mv-description").innerText = meta.description || "";
            } catch (e) {}
        }'''

new_block = '''    async function loadMintView(addr, metaUrl) {
        currentCollectionAddress = addr;
        collectionContract = new ethers.Contract(addr, COLLECTION_ABI, signer);

        document.getElementById("network-card").style.display = "none";
        document.getElementById("create-panel").style.display = "none";
        document.getElementById("mycollections-panel").style.display = "none";
        document.getElementById("manage-panel").style.display = "none";
        document.getElementById("mint-view-panel").style.display = "block";

        let resolvedMetaUrl = metaUrl;
        if (!resolvedMetaUrl) {
            try {
                const totalMintedForUri = await collectionContract.totalMinted();
                if (Number(totalMintedForUri) > 0) {
                    resolvedMetaUrl = await collectionContract.tokenURI(1);
                }
            } catch (e) {}
        }

        if (resolvedMetaUrl) {
            try {
                const metaRes = await fetch(resolvedMetaUrl);
                const meta = await metaRes.json();
                document.getElementById("mv-image").src = meta.image || "";
                document.getElementById("mv-description").innerText = meta.description || "";
            } catch (e) {}
        }'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Mint view now fetches image directly from contract as fallback.")
