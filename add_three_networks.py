import io

files_config = [
    {
        "path": "templates/gm.html",
        "html_anchor": '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
            </div>''',
        "html_new_cards": '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
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
            </div>''',
        "addr_anchor": '        robinhood: "0xEC76D7a9801Fd7De132b299a36B6E0125802430B"\n    };',
        "addr_new": '''        robinhood: "0xEC76D7a9801Fd7De132b299a36B6E0125802430B",
        avax: "0x4DF798fD9F5Ff9109e6D42B67D3eE86FE09D3bf1",
        plume: "0xB72b9D6BF3a0d20a5A3152bcDD627A67eaDad56C",
        zetachain: "0xdA8F4Da59a24b4F5ab1F1f2bd6D000F069F54080"
    };''',
        "net_anchor": '        robinhood: { chainIdHex: "0x" + (4663).toString(16),  chainName: "Robinhood Chain",  rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],          nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] }\n    };',
        "net_new": '''        robinhood: { chainIdHex: "0x" + (4663).toString(16),  chainName: "Robinhood Chain",  rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],          nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] },
        avax: { chainIdHex: "0x" + (43114).toString(16), chainName: "Avalanche", rpcUrls: ["https://api.avax.network/ext/bc/C/rpc"], nativeCurrency: { name: "AVAX", symbol: "AVAX", decimals: 18 }, blockExplorerUrls: ["https://snowtrace.io"] },
        plume: { chainIdHex: "0x" + (98866).toString(16), chainName: "Plume", rpcUrls: ["https://rpc.plume.org"], nativeCurrency: { name: "PLUME", symbol: "PLUME", decimals: 18 }, blockExplorerUrls: ["https://explorer.plume.org"] },
        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }
    };''',
        "gas_anchor": 'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100 };',
        "gas_new": 'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100, avax: 25, plume: 25, zetachain: 25 };',
    },
    {
        "path": "templates/mint.html",
        "html_anchor": '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
            </div>''',
        "html_new_cards": '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
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
            </div>''',
        "addr_anchor": '        robinhood: "0x8D9bEa1253501Bb5657e9Bb0B5f39807bAE7C47b"\n    };',
        "addr_new": '''        robinhood: "0x8D9bEa1253501Bb5657e9Bb0B5f39807bAE7C47b",
        avax: "0x5ecDA25Bd340b8684F8A97518F7f9892eC5712CB",
        plume: "0xf74fcdFc71a1B7d493a263E25766223004Bf20f7",
        zetachain: "0x2ACc1E37Ce6C219c9Fc4Cb5b74c9539fA202471a"
    };''',
        "net_anchor": '        robinhood: { chainIdHex: "0x" + (4663).toString(16), chainName: "Robinhood Chain", rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] }\n    };',
        "net_new": '''        robinhood: { chainIdHex: "0x" + (4663).toString(16), chainName: "Robinhood Chain", rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"], nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] },
        avax: { chainIdHex: "0x" + (43114).toString(16), chainName: "Avalanche", rpcUrls: ["https://api.avax.network/ext/bc/C/rpc"], nativeCurrency: { name: "AVAX", symbol: "AVAX", decimals: 18 }, blockExplorerUrls: ["https://snowtrace.io"] },
        plume: { chainIdHex: "0x" + (98866).toString(16), chainName: "Plume", rpcUrls: ["https://rpc.plume.org"], nativeCurrency: { name: "PLUME", symbol: "PLUME", decimals: 18 }, blockExplorerUrls: ["https://explorer.plume.org"] },
        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }
    };''',
        "gas_anchor": 'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100 };',
        "gas_new": 'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100, avax: 25, plume: 25, zetachain: 25 };',
    },
    {
        "path": "templates/flip.html",
        "html_anchor": '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
            </div>''',
        "html_new_cards": '''            <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
                <div class="symbol">HOOD</div>
                <div class="name">Robinhood</div>
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
            </div>''',
        "addr_anchor": '        robinhood: "0x033947CB876A2A5175d6EBe3058c9258e0c2231A"\n    };',
        "addr_new": '''        robinhood: "0x033947CB876A2A5175d6EBe3058c9258e0c2231A",
        avax: "0xCbF9e3DD39edb8E39328135b1131d7c70956eF6b",
        plume: "0x103e0F501530DaF1b99F66843CF86d516FfD3FB0",
        zetachain: "0x01447Fa5e71ae03449f5F7ae67D9Bf047A9d6C4F"
    };''',
        "net_anchor": '        robinhood: { chainIdHex: "0x" + (4663).toString(16),  chainName: "Robinhood Chain", rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],          nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] }\n    };',
        "net_new": '''        robinhood: { chainIdHex: "0x" + (4663).toString(16),  chainName: "Robinhood Chain", rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],          nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 }, blockExplorerUrls: ["https://robinhoodchain.blockscout.com"] },
        avax: { chainIdHex: "0x" + (43114).toString(16), chainName: "Avalanche", rpcUrls: ["https://api.avax.network/ext/bc/C/rpc"], nativeCurrency: { name: "AVAX", symbol: "AVAX", decimals: 18 }, blockExplorerUrls: ["https://snowtrace.io"] },
        plume: { chainIdHex: "0x" + (98866).toString(16), chainName: "Plume", rpcUrls: ["https://rpc.plume.org"], nativeCurrency: { name: "PLUME", symbol: "PLUME", decimals: 18 }, blockExplorerUrls: ["https://explorer.plume.org"] },
        zetachain: { chainIdHex: "0x" + (7000).toString(16), chainName: "ZetaChain", rpcUrls: ["https://zetachain-evm.blockpi.network/v1/rpc/public"], nativeCurrency: { name: "ZETA", symbol: "ZETA", decimals: 18 }, blockExplorerUrls: ["https://zetachain.blockscout.com"] }
    };''',
        "gas_anchor": 'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100 };',
        "gas_new": 'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100, avax: 25, plume: 25, zetachain: 25 };',
    },
]

for cfg in files_config:
    path = cfg["path"]
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()

    missing = []
    if cfg["html_anchor"] not in content: missing.append("html")
    if cfg["addr_anchor"] not in content: missing.append("addr")
    if cfg["net_anchor"] not in content: missing.append("net")
    if content.count(cfg["gas_anchor"]) == 0: missing.append("gas")

    if missing:
        print(f"ERROR in {path}: missing {missing}")
        continue

    content = content.replace(cfg["html_anchor"], cfg["html_new_cards"], 1)
    content = content.replace(cfg["addr_anchor"], cfg["addr_new"], 1)
    content = content.replace(cfg["net_anchor"], cfg["net_new"], 1)
    content = content.replace(cfg["gas_anchor"], cfg["gas_new"])

    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"SUCCESS: {path} updated with 3 new networks.")
