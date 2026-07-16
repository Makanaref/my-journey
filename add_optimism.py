import io

def process(path, edits):
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for label, old, new in edits:
        if old not in content:
            print(f"  ERROR [{path}] pattern not found: {label}")
            continue
        if content.count(old) > 1:
            print(f"  WARNING [{path}] pattern appears {content.count(old)}x: {label} (replacing all)")
        content = content.replace(old, new)
        print(f"  OK [{path}]: {label}")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)

OPT_NET_CARD_FULL = '''            <div class="net-card" id="net-zetachain" onclick="switchNetwork('zetachain')">
                <div class="symbol">ZETA</div>
                <div class="name">ZetaChain</div>
            </div>
            <div class="net-card" id="net-optimism" onclick="switchNetwork('optimism')">
                <div class="symbol">OP</div>
                <div class="name">Optimism</div>
            </div>'''

OPT_NET_CARD_OLD_FULL = '''            <div class="net-card" id="net-zetachain" onclick="switchNetwork('zetachain')">
                <div class="symbol">ZETA</div>
                <div class="name">ZetaChain</div>
            </div>'''

OPT_NET_CARD_INLINE_OLD = '''            <div class="net-card" id="net-zetachain" onclick="switchNetwork('zetachain')"><div class="symbol">ZETA</div><div class="name">ZetaChain</div></div>'''
OPT_NET_CARD_INLINE_NEW = '''            <div class="net-card" id="net-zetachain" onclick="switchNetwork('zetachain')"><div class="symbol">ZETA</div><div class="name">ZetaChain</div></div>
            <div class="net-card" id="net-optimism" onclick="switchNetwork('optimism')"><div class="symbol">OP</div><div class="name">Optimism</div></div>'''

OPT_NETWORKS_ENTRY = '        optimism: { chainIdHex: "0x" + (10).toString(16), chainName: "Optimism", rpcUrls: ["https://mainnet.optimism.io"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://optimistic.etherscan.io"] }'

# ---------------- gm.html ----------------
process("templates/gm.html", [
    ("net-card list", OPT_NET_CARD_OLD_FULL, OPT_NET_CARD_FULL),
    ("CONTRACT_ADDRESSES",
     '        zetachain: "0xdA8F4Da59a24b4F5ab1F1f2bd6D000F069F54080"\n    };',
     '        zetachain: "0xdA8F4Da59a24b4F5ab1F1f2bd6D000F069F54080",\n        optimism:  "0xc766525C577055bd918d257a0A09E45B859f139D"\n    };'),
    ("networks dict",
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }\n    };',
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },\n' + OPT_NETWORKS_ENTRY + '\n    };'),
])

# ---------------- flip.html ----------------
process("templates/flip.html", [
    ("net-card list", OPT_NET_CARD_OLD_FULL, OPT_NET_CARD_FULL),
    ("CONTRACT_ADDRESSES",
     '        zetachain: "0x01447Fa5e71ae03449f5F7ae67D9Bf047A9d6C4F"\n    };',
     '        zetachain: "0x01447Fa5e71ae03449f5F7ae67D9Bf047A9d6C4F",\n        optimism: "0xDefE151DA2D125E0F85E43f49F82a0d01BD4Ef5E"\n    };'),
    ("networks dict",
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }\n    };',
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },\n' + OPT_NETWORKS_ENTRY + '\n    };'),
])

# ---------------- mint.html ----------------
process("templates/mint.html", [
    ("net-card list", OPT_NET_CARD_OLD_FULL, OPT_NET_CARD_FULL),
    ("FACTORY_ADDRESSES",
     '        zetachain: "0x2ACc1E37Ce6C219c9Fc4Cb5b74c9539fA202471a"\n    };',
     '        zetachain: "0x2ACc1E37Ce6C219c9Fc4Cb5b74c9539fA202471a",\n        optimism: "0x9De98bf808154E247BD588E1cbb873495fb60424"\n    };'),
    ("networks dict",
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }\n    };',
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },\n' + OPT_NETWORKS_ENTRY + '\n    };'),
])

# ---------------- mint_nft.html ----------------
process("templates/mint_nft.html", [
    ("net-card list (inline)", OPT_NET_CARD_INLINE_OLD, OPT_NET_CARD_INLINE_NEW),
    ("FACTORY_ADDRESSES",
     '        zetachain: "0xF988CAc77e456e915aFbDC22BBc8c114fbd4Cd96"\n    };',
     '        zetachain: "0xF988CAc77e456e915aFbDC22BBc8c114fbd4Cd96",\n        optimism: "0xCA49ab409836c8301831f9908A86AfcFE20dE6e6"\n    };'),
    ("networks dict",
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16),  chainName: "ZetaChain",       rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }\n    };',
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16),  chainName: "ZetaChain",       rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },\n' + OPT_NETWORKS_ENTRY + '\n    };'),
])

# ---------------- oracle.html ----------------
process("templates/oracle.html", [
    ("net-card list", OPT_NET_CARD_OLD_FULL, OPT_NET_CARD_FULL),
    ("CONTRACTS (predict)",
     '        zetachain: "0x5A80759a9Ad738c75b3d0aB5335Ef0357231526a"\n    };',
     '        zetachain: "0x5A80759a9Ad738c75b3d0aB5335Ef0357231526a",\n        optimism: "0xEC76D7a9801Fd7De132b299a36B6E0125802430B"\n    };'),
    ("BTC_CONTRACTS (up/down)",
     '        zetachain: "0x1F5fE1cF942a179DA977d4321a20550F85CfC766"\n    };',
     '        zetachain: "0x1F5fE1cF942a179DA977d4321a20550F85CfC766",\n        optimism: "0x68B33a0Dca3Fe084a85A1aB7EAFA34D9F4aB5400"\n    };'),
    ("networks dict",
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }\n    };',
     '        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] },\n' + OPT_NETWORKS_ENTRY + '\n    };'),
    ("forEach reset-active array",
     '["lamina1","nexus","ink","avax","plume","zetachain"].forEach(n => document.getElementById("net-" + n).classList.remove("active"));',
     '["lamina1","nexus","ink","avax","plume","zetachain","optimism"].forEach(n => document.getElementById("net-" + n).classList.remove("active"));'),
])

print("\nDone. Review the OK/ERROR/WARNING lines above before committing.")
