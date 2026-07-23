import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_css = '''    .share-box {
        background: rgba(126,200,227,0.06); border: 1px solid rgba(126,200,227,0.25);
        border-radius: 10px; padding: 12px; margin-top: 14px; font-size: 0.78em;
        color: #9adcf2; word-break: break-all; text-align: left;
    }'''

new_css = '''    .share-box {
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

if old_css not in content:
    print("ERROR: css anchor not found!")
else:
    content = content.replace(old_css, new_css, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS part1: share box CSS updated.")

old_js1 = '''                    if (shortRes.ok && shortData.short_url) {
                        shareBox.innerText = "Share this link so others can mint: " + shortData.short_url;
                    } else {
                        shareBox.innerText = "Share this link so others can mint: " + fullUrl;
                    }
                } catch (e) {
                    shareBox.innerText = "Share this link so others can mint: " + fullUrl;
                }'''

new_js1 = '''                    const finalUrl = (shortRes.ok && shortData.short_url) ? shortData.short_url : fullUrl;
                    renderShareBox(finalUrl);
                } catch (e) {
                    renderShareBox(fullUrl);
                }'''

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_js1 not in content:
    print("ERROR: share callback JS not found!")
else:
    content = content.replace(old_js1, new_js1, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS part2: share callback simplified.")

old_js2 = '''    async function createCollection() {'''
new_js2 = '''    function renderShareBox(url) {
        const shareBox = document.getElementById("share-link-box");
        shareBox.innerHTML = 'Share this link so others can mint:<br><a href="' + url + '" target="_blank" rel="noopener">' + url + '</a><br><button class="share-copy-btn" onclick="copyShareLink(\\'' + url + '\\')">Copy link</button>';
    }

    function copyShareLink(url) {
        navigator.clipboard.writeText(url).then(() => {
            const btns = document.querySelectorAll(".share-copy-btn");
            btns.forEach(b => { b.innerText = "Copied ✅"; setTimeout(() => { b.innerText = "Copy link"; }, 1500); });
        });
    }

    async function createCollection() {'''

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_js2 not in content:
    print("ERROR: createCollection anchor not found!")
else:
    content = content.replace(old_js2, new_js2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS part3: renderShareBox and copyShareLink functions added.")
