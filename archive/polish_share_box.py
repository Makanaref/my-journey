import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Better CSS for the share box
old_css = '''    .share-box {
        background: rgba(126,200,227,0.06); border: 1px solid rgba(126,200,227,0.25);
        border-radius: 10px; padding: 14px; margin-top: 14px; font-size: 0.78em;
        color: #ccc; text-align: left;
    }
    .share-box a {
        color: #7ec8e3; word-break: break-all; text-decoration: underline;
        text-decoration-color: rgba(126,200,227,0.4);
    }
    .share-box a:hover { color: #9adcf2; }
    .share-copy-btn {
        margin-top: 10px; padding: 6px 14px; border-radius: 7px; font-size: 0.75em;
        border: 1px solid rgba(126,200,227,0.3); background: rgba(126,200,227,0.08);
        color: #7ec8e3; cursor: pointer; transition: background 0.2s ease;
    }
    .share-copy-btn:hover { background: rgba(126,200,227,0.18); }'''

new_css = '''    .share-box {
        background: linear-gradient(160deg, rgba(126,200,227,0.08), rgba(126,200,227,0.02));
        border: 1px solid rgba(126,200,227,0.25);
        border-radius: 12px; padding: 16px; margin-top: 14px;
        text-align: center;
    }
    .share-box-label {
        display: flex; align-items: center; justify-content: center; gap: 6px;
        color: #9adcf2; font-size: 0.8em; font-weight: 600; margin-bottom: 12px;
    }
    .share-copy-btn {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 22px; border-radius: 9px; font-size: 0.85em; font-weight: 700;
        border: 1px solid rgba(126,200,227,0.35); background: rgba(126,200,227,0.1);
        color: #7ec8e3; cursor: pointer; transition: all 0.2s ease;
    }
    .share-copy-btn:hover {
        background: #7ec8e3; color: #0f1420; transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(126,200,227,0.25);
    }'''

if old_css not in content:
    print("ERROR: css anchor not found!")
else:
    content = content.replace(old_css, new_css, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS part1: share box CSS polished.")

# 2. Update renderShareBox to only show a label + icon copy button, no visible URL
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_render = '''    function renderShareBox(url) {
        const shareBox = document.getElementById("share-link-box");
        shareBox.innerHTML = 'Share this link so others can mint:<br><a href="' + url + '" target="_blank" rel="noopener">' + url + '</a><br><button class="share-copy-btn" onclick="copyShareLink(\\'' + url + '\\')">Copy link</button>';
    }

    function copyShareLink(url) {
        navigator.clipboard.writeText(url).then(() => {
            const btns = document.querySelectorAll(".share-copy-btn");
            btns.forEach(b => { b.innerText = "Copied ✅"; setTimeout(() => { b.innerText = "Copy link"; }, 1500); });
        });
    }'''

new_render = '''    function renderShareBox(url) {
        const shareBox = document.getElementById("share-link-box");
        shareBox.innerHTML = ''
            + '<div class="share-box-label">🔗 Ready to share</div>'
            + '<button class="share-copy-btn" onclick="copyShareLink(\\'' + url + '\\', this)">'
            + '<svg width="15" height="15" viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M5 15V5a2 2 0 012-2h10" stroke="currentColor" stroke-width="1.6"/></svg>'
            + 'Copy mint link</button>';
    }

    function copyShareLink(url, btnEl) {
        navigator.clipboard.writeText(url).then(() => {
            const original = btnEl.innerHTML;
            btnEl.innerHTML = '✅ Copied!';
            setTimeout(() => { btnEl.innerHTML = original; }, 1500);
        });
    }'''

if old_render not in content:
    print("ERROR: renderShareBox anchor not found!")
else:
    content = content.replace(old_render, new_render, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS part2: renderShareBox now icon-only copy button.")
