import re

with open("templates/domain.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add the shared script tag right after the ethers.js script tag (only if not already added)
old_script_tag = '<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>'
if "/static/js/dapp-common.js" not in content:
    if old_script_tag not in content:
        raise SystemExit("ERROR: ethers.js script tag not found, aborting.")
    new_script_tag = old_script_tag + '\n<script src="/static/js/dapp-common.js"></script>'
    content = content.replace(old_script_tag, new_script_tag, 1)

# 2. Find and replace the "const networks = { ... };" block using regex,
# regardless of internal whitespace differences.
pattern = re.compile(r"    const networks = \{.*?\n    \};", re.DOTALL)
match = pattern.search(content)
if not match:
    raise SystemExit("ERROR: networks block not found via regex, aborting.")

new_networks_block = '''    // networks object now provided by /static/js/dapp-common.js (as NETWORKS),
    // filtered to only the networks this page actually supports.
    const networks = Object.fromEntries(
        Object.entries(NETWORKS).filter(([key]) => ["lamina1","nexus","ink","plume","zetachain","optimism","base"].includes(key))
    );'''

content = content[:match.start()] + new_networks_block + content[match.end():]

with open("templates/domain.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. domain.html now uses shared dapp-common.js for networks (filtered subset).")
