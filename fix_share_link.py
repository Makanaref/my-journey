import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''            if (newCollectionAddress) {
                const shareUrl = window.location.origin + "/mint-nft?net=" + currentNet + "&collection=" + newCollectionAddress;
                const shareBox = document.getElementById("share-link-box");
                shareBox.innerText = "Share this link so others can mint: " + shareUrl;
                shareBox.style.display = "block";
            }'''

new_block = '''            if (newCollectionAddress) {
                const shareUrl = window.location.origin + "/mint-nft?net=" + currentNet + "&collection=" + newCollectionAddress + "&meta=" + encodeURIComponent(metaData.metadata_url);
                const shareBox = document.getElementById("share-link-box");
                shareBox.innerText = "Share this link so others can mint: " + shareUrl;
                shareBox.style.display = "block";
            }'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Share link now includes metadata URL.")
