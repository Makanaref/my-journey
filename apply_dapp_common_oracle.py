with open("templates/oracle.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add the shared script tag right after the ethers.js script tag
old_script_tag = '<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>'
new_script_tag = old_script_tag + '\n<script src="/static/js/dapp-common.js"></script>'
if old_script_tag not in content:
    raise SystemExit("ERROR: ethers.js script tag not found, aborting.")
content = content.replace(old_script_tag, new_script_tag, 1)

# 2. Remove the duplicated `networks` object (oracle.html only has 7 networks, no base/robinhood)
# We keep it as a filtered subset of the shared NETWORKS, so no page behavior changes at all.
old_networks_block = '''    const networks = {
        lamina1: { chainIdHex: "0x" + (10849).toString(16), chainName: "Lamina1", rpcUrls: ["https://subnets.avax.network/lamina1/mainnet/rpc"], nativeCurrency: { name: "L1", symbol: "L1", decimals: 18 }, blockExplorerUrls: ["https://subnets.avax.network/lamina1"] },
        nexus: { chainIdHex: "0x" + (3946).toString(16), chainName: "Nexus", rpcUrls: ["https://mainnet.rpc.nexus.xyz"], nativeCurrency: { name: "NEX", symbol: "NEX", decimals: 18 }, blockExplorerUrls: ["https://explorer.nexus.xyz"] },
        ink: { chainIdHex: "0x" + (57073).toString(16), chainName: "Ink", rpcUrls: ["https://rpc-gel.inkonchain.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://explorer.inkonchain.com"] },
        avax: { chainIdHex: "0x" + (43114).toString(16), chainName: "Avalanche", rpcUrls: ["https://api.avax.network/ext/bc/C/rpc"], nativeCurrency: { name: "AVAX", symbol: "AVAX", decimals: 18 }, blockExplorerUrls: ["https://snowtrace.io"] },
        plume: { chainIdHex: "0x" + (98866).toString(16), chainName: "Plume", rpcUrls: ["https://rpc.plume.org"], nativeCurrency: { name: "PLUME", symbol: "PLUME", decimals: 18 }, blockExplorerUrls: ["https://explorer.plume.org"] },
        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },
        optimism: { chainIdHex: "0x" + (10).toString(16), chainName: "Optimism", rpcUrls: ["https://mainnet.optimism.io"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://optimistic.etherscan.io"] }
    };'''
if old_networks_block not in content:
    raise SystemExit("ERROR: networks block not found, aborting.")
new_networks_block = '''    // networks object now provided by /static/js/dapp-common.js (as NETWORKS),
    // filtered to only the networks this page actually supports (no base/robinhood).
    const networks = Object.fromEntries(
        Object.entries(NETWORKS).filter(([key]) => ["lamina1","nexus","ink","avax","plume","zetachain","optimism"].includes(key))
    );'''
content = content.replace(old_networks_block, new_networks_block, 1)

with open("templates/oracle.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. oracle.html now uses shared dapp-common.js for networks (filtered subset).")
