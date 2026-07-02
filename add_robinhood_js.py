import io

path = "templates/gm.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add contract address
old1 = """    base: "0x0d246A70E2c9ddCDacF690E854E9a528aaE9c3f6"
};"""
new1 = """    base: "0x0d246A70E2c9ddCDacF690E854E9a528aaE9c3f6",
    robinhood: "0xEC76D7a9801Fd7De132b299a36B6E0125802430B"
};"""

# 2. Add network config (right after the base network block)
old2 = """    ,base: {
        chainIdHex: "0x" + (8453).toString(16), chainName: "Base",
        rpcUrls: ["https://mainnet.base.org"],
        nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
        blockExplorerUrls: ["https://basescan.org"]
    }
};"""
new2 = """    ,base: {
        chainIdHex: "0x" + (8453).toString(16), chainName: "Base",
        rpcUrls: ["https://mainnet.base.org"],
        nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
        blockExplorerUrls: ["https://basescan.org"]
    }
    ,robinhood: {
        chainIdHex: "0x" + (4663).toString(16), chainName: "Robinhood Chain",
        rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],
        nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
        blockExplorerUrls: ["https://robinhoodchain.blockscout.com"]
    }
};"""

# 3. Add to the classList.remove list when switching networks
old3 = """            document.getElementById("net-lamina1").classList.remove("active");
            document.getElementById("net-nexus").classList.remove("active");
            document.getElementById("net-ink").classList.remove("active");
            document.getElementById("net-base").classList.remove("active");
            document.getElementById("net-base").classList.remove("active");"""
new3 = """            document.getElementById("net-lamina1").classList.remove("active");
            document.getElementById("net-nexus").classList.remove("active");
            document.getElementById("net-ink").classList.remove("active");
            document.getElementById("net-base").classList.remove("active");
            document.getElementById("net-robinhood").classList.remove("active");"""

# 4. Add conservative gas price percentage from the start
old4 = """            const gasPricePercent = {
                lamina1: 100,
                nexus: 25,
                ink: 25,
                base: 15
            };"""
new4 = """            const gasPricePercent = {
                lamina1: 100,
                nexus: 25,
                ink: 25,
                base: 15,
                robinhood: 20
            };"""

errors = []
if old1 not in content: errors.append("part1 (contract address)")
if old2 not in content: errors.append("part2 (network config)")
if old3 not in content: errors.append("part3 (classList remove)")
if old4 not in content: errors.append("part4 (gas percent)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    content = content.replace(old3, new3, 1)
    content = content.replace(old4, new4, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Robinhood network fully wired in.")
