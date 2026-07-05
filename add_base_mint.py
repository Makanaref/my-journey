import io

path = "templates/mint.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add network card to HTML
old1 = '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
            </div>
        </div>
    </div>'''
new1 = '''            <div class="net-card" id="net-base" onclick="switchNetwork('base')">
                <div class="symbol">BASE</div>
                <div class="name">Base</div>
            </div>
            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
            </div>
        </div>
    </div>'''

# 2. Add factory address
old2 = '''    const FACTORY_ADDRESSES = {
        lamina1:   "0x4d860020dc84f9AA1e24EF55f44859bc8CF55a8B",
        nexus:     "0x63f76204e323Be28E1e89dCedf6E3717deF1C73F",
        ink:       "0x472057828170D4Ac2CEa6B07D30A9b33B7d714d1",
        robinhood: "0x8D9bEa1253501Bb5657e9Bb0B5f39807bAE7C47b"
    };'''
new2 = '''    const FACTORY_ADDRESSES = {
        lamina1:   "0x4d860020dc84f9AA1e24EF55f44859bc8CF55a8B",
        nexus:     "0x63f76204e323Be28E1e89dCedf6E3717deF1C73F",
        ink:       "0x472057828170D4Ac2CEa6B07D30A9b33B7d714d1",
        base:      "0xFae8Fb8327A908120Ec2C46Cfc985CCF926821AA",
        robinhood: "0x8D9bEa1253501Bb5657e9Bb0B5f39807bAE7C47b"
    };'''

# 3. Add network config
old3 = '''        robinhood: { chainIdHex: "0x" + (4663).toString(16), chainName: "Robinhood Chain", rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] }
    };'''
new3 = '''        base:      { chainIdHex: "0x" + (8453).toString(16), chainName: "Base", rpcUrls: ["https://mainnet.base.org"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://basescan.org"] },
        robinhood: { chainIdHex: "0x" + (4663).toString(16), chainName: "Robinhood Chain", rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] }
    };'''

# 4. Update gas price percent map in createToken()
old4 = '''            const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, robinhood: 100 };'''
new4 = '''            const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100 };'''

# 5. Update gas price percent map in getTxOverrides()
old5 = '''        const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, robinhood: 100 };'''
new5 = '''        const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100 };'''

errors = []
if old1 not in content: errors.append("part1 (html card)")
if old2 not in content: errors.append("part2 (factory address)")
if old3 not in content: errors.append("part3 (network config)")
if old4 not in content: errors.append("part4 (createToken gas)")
if old5 not in content: errors.append("part5 (getTxOverrides gas)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    content = content.replace(old3, new3, 1)
    content = content.replace(old4, new4, 1)
    content = content.replace(old5, new5, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Base network added to Mint Token page.")
