import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''        let debugMsg = "";
        let resolvedMetaUrl = metaUrl;
        if (!resolvedMetaUrl) {
            try {
                resolvedMetaUrl = await collectionContract.metadataURI();
            } catch(e) {}
        }
        if (!resolvedMetaUrl) {
            try {
                const total = await collectionContract.totalMinted();
                if (Number(total) > 0) {
                    resolvedMetaUrl = await collectionContract.tokenURI(1);
                }
            } catch(e) {}
        }

        if (resolvedMetaUrl) {
            try {
                const metaRes = await fetch(resolvedMetaUrl);
                debugMsg += "fetchStatus=" + metaRes.status + " | ";
                const meta = await metaRes.json();
                document.getElementById("mv-image").src = meta.image || "";
                document.getElementById("mv-description").innerText = meta.description || ("DEBUG: " + debugMsg);
            } catch (e) {
                document.getElementById("mv-description").innerText = "DEBUG: " + debugMsg + "ERROR(fetch): " + e.message;
            }
        } else {
            document.getElementById("mv-description").innerText = "DEBUG: " + debugMsg + "(resolvedMetaUrl still empty)";
        }'''

new_block = '''        let resolvedMetaUrl = metaUrl;
        if (!resolvedMetaUrl) {
            try {
                resolvedMetaUrl = await collectionContract.metadataURI();
            } catch(e) {}
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
    print("SUCCESS: Debug code cleaned up.")
