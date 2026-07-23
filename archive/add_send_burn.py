import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

changes_made = []

# 1) Extend COLLECTION_ABI with Transfer event, ownerOf, transferFrom, burn
abi_start = content.find("const COLLECTION_ABI = [")
if abi_start == -1:
    print("ERROR: COLLECTION_ABI not found!")
else:
    abi_close = content.find("];", abi_start)
    if abi_close == -1:
        print("ERROR: COLLECTION_ABI closing bracket not found!")
    else:
        extra_lines = ''',
        "function ownerOf(uint256 tokenId) public view returns (address)",
        "function transferFrom(address from, address to, uint256 tokenId) public",
        "function burn(uint256 tokenId) public",
        "event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)"'''
        content = content[:abi_close] + extra_lines + "\n    " + content[abi_close:]
        changes_made.append("ABI extended")

# 2) Insert "Your tokens" section HTML inside manage-panel, right after manage-nft-status paragraph
anchor = 'id="manage-nft-status"'
idx = content.find(anchor)
if idx == -1:
    print("ERROR: manage-nft-status anchor not found!")
else:
    close_p = content.find("</p>", idx)
    if close_p == -1:
        print("ERROR: closing </p> after manage-nft-status not found!")
    else:
        insert_pos = close_p + len("</p>")
        new_section = '''
        <div class="my-tokens-title">Your tokens in this collection</div>
        <div id="my-tokens-list"><p style="color:#666;font-size:0.8em;">Select a collection to see your tokens.</p></div>'''
        content = content[:insert_pos] + new_section + content[insert_pos:]
        changes_made.append("Your tokens section HTML added")

# 3) Add CSS for the new section, right before closing </style> tag (first occurrence)
style_close = content.find("</style>")
if style_close == -1:
    print("ERROR: </style> not found!")
else:
    css = '''
    .my-tokens-title { font-size:0.78em; color:#999; margin:18px 0 10px; letter-spacing:0.5px; border-top:1px solid rgba(255,255,255,0.06); padding-top:14px; }
    .token-row { display:flex; align-items:center; justify-content:space-between; padding:8px 12px; border-radius:8px; background:rgba(255,255,255,0.02); margin-bottom:6px; }
    .token-id { font-family:monospace; color:#ccc; font-size:0.85em; }
    .token-actions { display:flex; gap:6px; }
    .token-btn { padding:5px 12px; border-radius:6px; font-size:0.75em; font-weight:600; border:1px solid rgba(126,200,227,0.3); background:rgba(126,200,227,0.08); color:#7ec8e3; cursor:pointer; transition:background 0.2s ease; }
    .token-btn:hover { background:rgba(126,200,227,0.18); }
    .token-btn-danger { border-color:rgba(233,69,96,0.3); background:rgba(233,69,96,0.08); color:#e94560; }
    .token-btn-danger:hover { background:rgba(233,69,96,0.18); }
    '''
    content = content[:style_close] + css + content[style_close:]
    changes_made.append("CSS added")

# 4) Add JS functions: loadMyTokensInCollection, sendToken, burnToken - insert before the final </script>
last_script_close = content.rfind("</script>")
if last_script_close == -1:
    print("ERROR: no </script> found!")
else:
    js_funcs = '''
    async function loadMyTokensInCollection(addr) {
        const listEl = document.getElementById("my-tokens-list");
        if (!listEl) return;
        listEl.innerHTML = "<p style='color:#666;font-size:0.8em;'>Loading your tokens...</p>";
        try {
            const c = new ethers.Contract(addr, COLLECTION_ABI, signer);
            const events = await c.queryFilter(c.filters.Transfer(null, account), 0, "latest");
            const candidateIds = [...new Set(events.map(e => e.args.tokenId.toString()))];
            const owned = [];
            await Promise.all(candidateIds.map(async (id) => {
                try {
                    const owner = await c.ownerOf(id);
                    if (owner.toLowerCase() === account.toLowerCase()) owned.push(id);
                } catch (e) {}
            }));
            owned.sort((a,b) => Number(a) - Number(b));
            if (owned.length === 0) {
                listEl.innerHTML = "<p style='color:#666;font-size:0.8em;'>You don't own any tokens from this collection.</p>";
                return;
            }
            listEl.innerHTML = owned.map(id => `
                <div class="token-row">
                    <span class="token-id">#${id}</span>
                    <div class="token-actions">
                        <button class="token-btn" onclick="sendToken('${addr}', '${id}')">Send</button>
                        <button class="token-btn token-btn-danger" onclick="burnToken('${addr}', '${id}')">Burn</button>
                    </div>
                </div>
            `).join("");
        } catch (err) {
            listEl.innerHTML = "<p style='color:#666;font-size:0.8em;'>Couldn't load your tokens.</p>";
        }
    }

    async function sendToken(addr, tokenId) {
        const to = prompt("Enter the recipient wallet address:");
        if (!to) return;
        if (!ethers.isAddress(to)) { alert("Invalid address."); return; }
        try {
            const c = new ethers.Contract(addr, COLLECTION_ABI, signer);
            const overrides = await getTxOverrides();
            const tx = await c.transferFrom(account, to, tokenId, overrides);
            await tx.wait();
            alert("Sent!");
            await loadMyTokensInCollection(addr);
        } catch (err) {
            alert("Failed: " + (err.reason || err.message || "unknown error"));
        }
    }

    async function burnToken(addr, tokenId) {
        if (!confirm("Are you sure? Burning token #" + tokenId + " is permanent and cannot be undone.")) return;
        try {
            const c = new ethers.Contract(addr, COLLECTION_ABI, signer);
            const overrides = await getTxOverrides();
            const tx = await c.burn(tokenId, overrides);
            await tx.wait();
            alert("Burned!");
            await loadMyTokensInCollection(addr);
            await loadCollectionDetails(addr);
        } catch (err) {
            alert("Failed: " + (err.reason || err.message || "unknown error"));
        }
    }
    '''
    content = content[:last_script_close] + js_funcs + content[last_script_close:]
    changes_made.append("JS functions added")

# 5) Hook loadMyTokensInCollection into the collection-select flow
old_call = "await loadCollectionDetails(addr);"
if old_call in content:
    new_call = "await loadCollectionDetails(addr);\n        await loadMyTokensInCollection(addr);"
    content = content.replace(old_call, new_call, 1)
    changes_made.append("hooked into loadSelectedCollection")
else:
    print("WARNING: could not find call site to auto-load tokens; you'll need to select the collection again to refresh manually.")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: " + ", ".join(changes_made))
