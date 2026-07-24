import re

with open("templates/mint_nft.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add the shared script tag right after the ethers.js script tag
old_script_tag = '<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>'
if "/static/js/dapp-common.js" not in content:
    if old_script_tag not in content:
        raise SystemExit("ERROR: ethers.js script tag not found, aborting.")
    new_script_tag = old_script_tag + '\n<script src="/static/js/dapp-common.js"></script>'
    content = content.replace(old_script_tag, new_script_tag, 1)

# 2. Remove the duplicated getFriendlyError function using regex (now provided by dapp-common.js)
fn_pattern = re.compile(
    r"\n\s*function getFriendlyError\(err\) \{.*?\n\s*\}\n",
    re.DOTALL
)
fn_match = fn_pattern.search(content)
if not fn_match:
    raise SystemExit("ERROR: getFriendlyError function not found via regex, aborting.")
content = content[:fn_match.start()] + "\n" + content[fn_match.end():]

# 3. Find and replace the "const networks = { ... };" block using regex
net_pattern = re.compile(r"    const networks = \{.*?\n    \};", re.DOTALL)
net_match = net_pattern.search(content)
if not net_match:
    raise SystemExit("ERROR: networks block not found via regex, aborting.")

new_networks_block = '''    // networks object now provided by /static/js/dapp-common.js (as NETWORKS),
    // filtered to only the networks this page actually supports.
    const networks = Object.fromEntries(
        Object.entries(NETWORKS).filter(([key]) => ["lamina1","nexus","ink","base","robinhood","avax","plume","zetachain","optimism"].includes(key))
    );'''

content = content[:net_match.start()] + new_networks_block + content[net_match.end():]

with open("templates/mint_nft.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. mint_nft.html now uses shared dapp-common.js for networks and getFriendlyError.")
