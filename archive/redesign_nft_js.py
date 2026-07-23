import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_toggle = '''    function toggleImageSource(mode) {
        document.getElementById("nft-image-url").style.display = mode === "url" ? "block" : "none";
        document.getElementById("nft-image-file").style.display = mode === "upload" ? "block" : "none";
        document.getElementById("nft-image-preview").style.display = "none";
        uploadedImageUrl = null;
    }

    function togglePriceType(mode) {
        document.getElementById("nft-price").style.display = mode === "paid" ? "block" : "none";
    }'''

new_toggle = '''    function toggleImageSource(mode) {
        document.getElementById("opt-url").classList.toggle("active", mode === "url");
        document.getElementById("opt-upload").classList.toggle("active", mode === "upload");
        document.getElementById("nft-image-url").style.display = mode === "url" ? "block" : "none";
        document.getElementById("upload-zone").style.display = mode === "upload" ? "block" : "none";
        document.getElementById("nft-image-preview").style.display = "none";
        uploadedImageUrl = null;
    }

    function togglePriceType(mode) {
        document.getElementById("opt-free").classList.toggle("active", mode === "free");
        document.getElementById("opt-paid").classList.toggle("active", mode === "paid");
        document.getElementById("nft-price").style.display = mode === "paid" ? "block" : "none";
    }'''

old_upload_listener = '''                    if (res.ok && data.image_url) {
                        uploadedImageUrl = data.image_url;
                        const preview = document.getElementById("nft-image-preview");
                        preview.src = data.image_url;
                        preview.style.display = "block";
                        statusEl.innerText = "Image uploaded ✅";
                    } else {'''

new_upload_listener = '''                    if (res.ok && data.image_url) {
                        uploadedImageUrl = data.image_url;
                        const preview = document.getElementById("nft-image-preview");
                        preview.src = data.image_url;
                        preview.style.display = "block";
                        document.getElementById("upload-zone-label").innerText = file.name;
                        statusEl.innerText = "Image uploaded ✅";
                    } else {'''

errors = []
if old_toggle not in content: errors.append("toggle functions")
if old_upload_listener not in content: errors.append("upload listener")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old_toggle, new_toggle, 1)
    content = content.replace(old_upload_listener, new_upload_listener, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: JS toggle and upload logic updated.")
