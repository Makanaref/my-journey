import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''        <p class="status-msg" id="manage-nft-status"></p>
    </div>
        <p class="status-msg" id="manage-nft-status"></p>
        <div class="my-tokens-title">Your tokens in this collection</div>
        <div id="my-tokens-list"><p style="color:#666;font-size:0.8em;">Select a collection to see your tokens.</p></div>
    </div>'''

new_block = '''        <p class="status-msg" id="manage-nft-status"></p>
        <div class="my-tokens-title">Your tokens in this collection</div>
        <div id="my-tokens-list"><p style="color:#666;font-size:0.8em;">Select a collection to see your tokens.</p></div>
    </div>'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: removed extra closing div and duplicate status paragraph.")
