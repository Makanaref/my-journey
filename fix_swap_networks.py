"""
fix_swap_networks.py
Fixes incorrect/placeholder token addresses and network config in swap.html:
1. Ink USDC address (was a fake placeholder, now the real Circle-verified address)
2. Robinhood Chain ID, RPC, and native currency (was completely wrong / fake RPC)
3. Temporarily disables Robinhood and ZetaChain from swap APIs since their
   real USDC addresses / API support could not be verified
"""

import os

TARGET_FILE = "templates/swap.html"

REPLACEMENTS = [
    (
        '"0x6900000000000000000000000000000000000001"',
        '"0x2D270e6886d130D724215A266106e6832161EAEd"',
        "Fix Ink USDC address"
    ),
    (
        '''        { 
            id: "999",   name: "Robinhood", chainId: "0x3e7",  
            logo: "https://raw.githubusercontent.com/lifinance/brand/main/src/assets/icons/chains/robinhood.svg",
            rpc: "https://robinhood.rpc.url",
            nativeCurrency: { name: "Robinhood", symbol: "HOOD", decimals: 18 }
        },''',
        '''        { 
            id: "4663",  name: "Robinhood", chainId: "0x1237",  
            logo: "https://raw.githubusercontent.com/lifinance/brand/main/src/assets/icons/chains/robinhood.svg",
            rpc: "https://rpc.mainnet.chain.robinhood.com",
            nativeCurrency: { name: "Ethereum", symbol: "ETH", decimals: 18 }
        },''',
        "Fix Robinhood chain ID, RPC and native currency"
    ),
    (
        '''        "999": [
            { symbol: "HOOD", addr: "0x0000000000000000000000000000000000000000", logo: TOKEN_LOGO_MAP["HOOD"], decimals: 18, isNative: true },
            { symbol: "USDC", addr: "0x0c6f6e5b0b4e5c5b0b0b0b0b0b0b0b0b0b0b0b0b", logo: TOKEN_LOGO_MAP["USDC"], decimals: 6 },
        ],''',
        '''        "4663": [
            { symbol: "ETH", addr: "0x0000000000000000000000000000000000000000", logo: TOKEN_LOGO_MAP["ETH"], decimals: 18, isNative: true },
        ],''',
        "Update Robinhood token list (id + remove unverified USDC)"
    ),
    (
        '''        "7000": [
            { symbol: "ZETA", addr: "0x0000000000000000000000000000000000000000", logo: TOKEN_LOGO_MAP["ZETA"], decimals: 18, isNative: true },
            { symbol: "USDC", addr: "0x0c6f6e5b0b4e5c5b0b0b0b0b0b0b0b0b0b0b0b0b", logo: TOKEN_LOGO_MAP["USDC"], decimals: 6 },
        ],''',
        '''        "7000": [
            { symbol: "ZETA", addr: "0x0000000000000000000000000000000000000000", logo: TOKEN_LOGO_MAP["ZETA"], decimals: 18, isNative: true },
        ],''',
        "Remove unverified ZetaChain USDC entry"
    ),
    (
        '''        "43114": "avalanche",
        "57073": "ink",
        "999": "robinhood"
    };''',
        '''        "43114": "avalanche",
        "57073": "ink"
    };''',
        "Remove Robinhood from LIFI_SUPPORTED"
    ),
    (
        '''        "10": "optimism",
        "7000": "zetachain",
        "999": "robinhood"
    };''',
        '''        "10": "optimism"
    };''',
        "Remove Robinhood and ZetaChain from RELAY_SUPPORTED"
    ),
]


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"[ERROR] File not found: {TARGET_FILE}")
        print("Make sure you're running this from the project root (~/my-journey)")
        return

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    total_changes = 0
    for old, new, description in REPLACEMENTS:
        count = content.count(old)
        if count == 0:
            print(f"  [SKIPPED] Not found: {description}")
            continue
        if count > 1:
            print(f"  [WARNING] '{description}' matched {count} times, replacing all")
        content = content.replace(old, new)
        total_changes += count
        print(f"  [OK] {description} ({count} change{'s' if count > 1 else ''})")

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nDone. {total_changes} total changes applied to {TARGET_FILE}")
    print("Now check the file with: git diff templates/swap.html | cat")


if __name__ == "__main__":
    main()
