import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_line = '            document.getElementById("nc-share-link").innerText = "Share link: " + shareUrl;'

new_line = '''            const ncShareBox = document.getElementById("nc-share-link");
            ncShareBox.innerHTML = ''
                + '<div class="share-box-label">🔗 Mint link</div>'
                + '<button class="share-copy-btn" onclick="copyShareLink(\\'' + shareUrl + '\\', this)">'
                + '<svg width="15" height="15" viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M5 15V5a2 2 0 012-2h10" stroke="currentColor" stroke-width="1.6"/></svg>'
                + 'Copy mint link</button>';'''

if old_line not in content:
    print("ERROR: old_line not found!")
else:
    content = content.replace(old_line, new_line, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: manage panel share link updated to match new style.")
