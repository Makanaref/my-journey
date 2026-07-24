with open("templates/gm.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add the shared script tag right after the ethers.js script tag
old_script_tag = '<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>'
new_script_tag = old_script_tag + '\n<script src="/static/js/dapp-common.js"></script>'
if old_script_tag not in content:
    raise SystemExit("ERROR: ethers.js script tag not found, aborting.")
content = content.replace(old_script_tag, new_script_tag, 1)

# 2. Remove the duplicated getFriendlyError function (now provided by dapp-common.js)
old_get_friendly_error = '''
        function getFriendlyError(err) {
            const raw = ((err && (err.reason || err.message)) || "").toString();
            const msg = raw.toLowerCase();

            if (msg.includes("already known") || msg.includes("nonce too low")) {
                return "This transaction was already submitted. Please wait a moment.";
            }
            if (msg.includes("insufficient funds")) {
                return "Insufficient balance to complete this transaction.";
            }
            if (msg.includes("user rejected") || msg.includes("user denied") || msg.includes("action_rejected")) {
                return "Transaction was rejected.";
            }
            if (msg.includes("gas required exceeds") || msg.includes("out of gas")) {
                return "Estimated gas cost is too high. Please try again.";
            }
            if (msg.includes("execution reverted")) {
                return "Transaction was reverted by the contract.";
            }
            if (msg.includes("network") || msg.includes("timeout")) {
                return "Network connection issue. Please check your connection and try again.";
            }
            return "Something went wrong. Please try again.";
        }
'''
if old_get_friendly_error not in content:
    raise SystemExit("ERROR: getFriendlyError function not found, aborting.")
content = content.replace(old_get_friendly_error, "\n", 1)

# 3. Remove the duplicated `networks` object (now provided by dapp-common.js as NETWORKS)
old_networks_block = '''    const networks = {
        lamina1:   { chainIdHex: "0x" + (10849).toString(16), chainName: "Lamina1",         rpcUrls: ["https://subnets.avax.network/lamina1/mainnet/rpc"], nativeCurrency: { name: "L1",  symbol: "L1",  decimals: 18 }, blockExplorerUrls: ["https://subnets.avax.network/lamina1"] },
        nexus:     { chainIdHex: "0x" + (3946).toString(16),  chainName: "Nexus",            rpcUrls: ["https://mainnet.rpc.nexus.xyz"],                    nativeCurrency: { name: "NEX", symbol: "NEX", decimals: 18 }, blockExplorerUrls: ["https://explorer.nexus.xyz"] },
        ink:       { chainIdHex: "0x" + (57073).toString(16), chainName: "Ink",              rpcUrls: ["https://rpc-gel.inkonchain.com"],                   nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://explorer.inkonchain.com"] },
        base:      { chainIdHex: "0x" + (8453).toString(16),  chainName: "Base",             rpcUrls: ["https://mainnet.base.org"],                        nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://basescan.org"] },
        robinhood: { chainIdHex: "0x" + (4663).toString(16),  chainName: "Robinhood Chain",  rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],          nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] },
        avax: { chainIdHex: "0x" + (43114).toString(16), chainName: "Avalanche", rpcUrls: ["https://api.avax.network/ext/bc/C/rpc"], nativeCurrency: { name: "AVAX", symbol: "AVAX", decimals: 18 }, blockExplorerUrls: ["https://snowtrace.io"] },
        plume: { chainIdHex: "0x" + (98866).toString(16), chainName: "Plume", rpcUrls: ["https://rpc.plume.org"], nativeCurrency: { name: "PLUME", symbol: "PLUME", decimals: 18 }, blockExplorerUrls: ["https://explorer.plume.org"] },
        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },
        optimism: { chainIdHex: "0x" + (10).toString(16), chainName: "Optimism", rpcUrls: ["https://mainnet.optimism.io"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://optimistic.etherscan.io"] }
    };'''
if old_networks_block not in content:
    raise SystemExit("ERROR: networks block not found, aborting.")
content = content.replace(old_networks_block, "    // networks object now provided by /static/js/dapp-common.js (as NETWORKS)\n    const networks = NETWORKS;", 1)

with open("templates/gm.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. gm.html now uses shared dapp-common.js for networks and getFriendlyError.")
