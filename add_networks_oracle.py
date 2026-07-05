import io

path = "templates/oracle.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. HTML cards
old1 = '''            <div class="net-card" id="net-ink" onclick="switchNetwork('ink')">
                <div class="symbol">ETH</div>
                <div class="name">Ink</div>
            </div>
        </div>
    </div>'''
new1 = '''            <div class="net-card" id="net-ink" onclick="switchNetwork('ink')">
                <div class="symbol">ETH</div>
                <div class="name">Ink</div>
            </div>
            <div class="net-card" id="net-avax" onclick="switchNetwork('avax')">
                <div class="symbol">AVAX</div>
                <div class="name">Avalanche</div>
            </div>
            <div class="net-card" id="net-plume" onclick="switchNetwork('plume')">
                <div class="symbol">PLUME</div>
                <div class="name">Plume</div>
            </div>
            <div class="net-card" id="net-zetachain" onclick="switchNetwork('zetachain')">
                <div class="symbol">ZETA</div>
                <div class="name">ZetaChain</div>
            </div>
        </div>
    </div>'''

# 2. CONTRACTS map
old2 = '''    const CONTRACTS = {
        lamina1: "0xcf2B368dA4D785C45C4Cf72bAeB8ef4f52600B5D",
        nexus: "0xcf2B368dA4D785C45C4Cf72bAeB8ef4f52600B5D",
        ink: "0x0eea7AbDdeDD3Ae52B37Db2e041CC5446D40b5B1"
    };'''
new2 = '''    const CONTRACTS = {
        lamina1: "0xcf2B368dA4D785C45C4Cf72bAeB8ef4f52600B5D",
        nexus: "0xcf2B368dA4D785C45C4Cf72bAeB8ef4f52600B5D",
        ink: "0x0eea7AbDdeDD3Ae52B37Db2e041CC5446D40b5B1",
        avax: "0xD00C4A6854da53E321c3FEca1c10E5F3F59a0d31",
        plume: "0xe8E2F8133d40a20eA030A44f7b8A5eee1519Dc2e",
        zetachain: "0x5A80759a9Ad738c75b3d0aB5335Ef0357231526a"
    };'''

# 3. BTC_CONTRACTS map
old3 = '''    const BTC_CONTRACTS = {
        lamina1: "0x537F8d93048BCd10A9100C30c822FF33331696c4",
        nexus: "0x1c543Ee670D5E4C77C4143A2d5Cb3b67459fCBe5",
        ink: "0xD3864216053A9542293eA747172226967c2c6582"
    };'''
new3 = '''    const BTC_CONTRACTS = {
        lamina1: "0x537F8d93048BCd10A9100C30c822FF33331696c4",
        nexus: "0x1c543Ee670D5E4C77C4143A2d5Cb3b67459fCBe5",
        ink: "0xD3864216053A9542293eA747172226967c2c6582",
        avax: "0x8824d39768008611DDd761c70e4217Bc081D5383",
        plume: "0x714afCfd73D9da6A2f5f3Ba1B31Fe818933e29Aa",
        zetachain: "0x1F5fE1cF942a179DA977d4321a20550F85CfC766"
    };'''

# 4. networks config
old4 = '''    const networks = {
        lamina1: { chainIdHex: "0x" + (10849).toString(16), chainName: "Lamina1", rpcUrls: ["https://subnets.avax.network/lamina1/mainnet/rpc"], nativeCurrency: { name: "L1", symbol: "L1", decimals: 18 }, blockExplorerUrls: ["https://subnets.avax.network/lamina1"] },
        nexus: { chainIdHex: "0x" + (3946).toString(16), chainName: "Nexus", rpcUrls: ["https://mainnet.rpc.nexus.xyz"], nativeCurrency: { name: "NEX", symbol: "NEX", decimals: 18 }, blockExplorerUrls: ["https://explorer.nexus.xyz"] },
        ink: { chainIdHex: "0x" + (57073).toString(16), chainName: "Ink", rpcUrls: ["https://rpc-gel.inkonchain.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://explorer.inkonchain.com"] }
    };'''
new4 = '''    const networks = {
        lamina1: { chainIdHex: "0x" + (10849).toString(16), chainName: "Lamina1", rpcUrls: ["https://subnets.avax.network/lamina1/mainnet/rpc"], nativeCurrency: { name: "L1", symbol: "L1", decimals: 18 }, blockExplorerUrls: ["https://subnets.avax.network/lamina1"] },
        nexus: { chainIdHex: "0x" + (3946).toString(16), chainName: "Nexus", rpcUrls: ["https://mainnet.rpc.nexus.xyz"], nativeCurrency: { name: "NEX", symbol: "NEX", decimals: 18 }, blockExplorerUrls: ["https://explorer.nexus.xyz"] },
        ink: { chainIdHex: "0x" + (57073).toString(16), chainName: "Ink", rpcUrls: ["https://rpc-gel.inkonchain.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://explorer.inkonchain.com"] },
        avax: { chainIdHex: "0x" + (43114).toString(16), chainName: "Avalanche", rpcUrls: ["https://api.avax.network/ext/bc/C/rpc"], nativeCurrency: { name: "AVAX", symbol: "AVAX", decimals: 18 }, blockExplorerUrls: ["https://snowtrace.io"] },
        plume: { chainIdHex: "0x" + (98866).toString(16), chainName: "Plume", rpcUrls: ["https://rpc.plume.org"], nativeCurrency: { name: "PLUME", symbol: "PLUME", decimals: 18 }, blockExplorerUrls: ["https://explorer.plume.org"] },
        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }
    };'''

# 5. hardcoded array for classList remove
old5 = '''["lamina1","nexus","ink"].forEach(n => document.getElementById("net-" + n).classList.remove("active"));'''
new5 = '''["lamina1","nexus","ink","avax","plume","zetachain"].forEach(n => document.getElementById("net-" + n).classList.remove("active"));'''

errors = []
if old1 not in content: errors.append("part1 (html)")
if old2 not in content: errors.append("part2 (CONTRACTS)")
if old3 not in content: errors.append("part3 (BTC_CONTRACTS)")
if old4 not in content: errors.append("part4 (networks)")
if old5 not in content: errors.append("part5 (forEach array)")

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
    print("SUCCESS: oracle.html updated with 3 new networks.")
