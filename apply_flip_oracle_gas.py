"""
apply_flip_oracle_gas.py
1. Applies the tuned gasPricePercent object (from GM page testing) to flip.html
2. Adds an explicit gasPricePercent object to oracle.html, replacing its
   crude "full fee vs 25%" logic
3. Adds "optimism: 85" to all tuned objects (Base and Optimism are both
   OP-Stack L2s, so 85% is a reasonable starting point to test)
4. Keeps avax at 700% everywhere (including mint.html / mint_nft.html,
   reverting the earlier 2800% experiment there per user's decision)
"""

import os

TUNED_PERCENT_STR = "{ lamina1: 40, nexus: 8, ink: 13, base: 85, robinhood: 100, avax: 700, plume: 25, zetachain: 100, optimism: 85 }"

FLIP_FILE = "templates/flip.html"
FLIP_OLD = "const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100, avax: 25, plume: 25, zetachain: 100 };"
FLIP_NEW = f"const gasPricePercent = {TUNED_PERCENT_STR};"

ORACLE_FILE = "templates/oracle.html"
ORACLE_OLD_1 = '''                const isFullFee = ["lamina1", "zetachain"].includes(currentNet);
                const gasPrice = isFullFee ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;'''
ORACLE_NEW_1 = f'''                const gasPricePercent = {TUNED_PERCENT_STR};
                const percent = BigInt(gasPricePercent[currentNet] !== undefined ? gasPricePercent[currentNet] : 25);
                const gasPrice = feeData.gasPrice * percent / 100n;'''

ORACLE_OLD_2 = '''                const isFullFeeMain = ["lamina1", "zetachain"].includes(currentNet);
                const gasPriceMain = isFullFeeMain ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;'''
ORACLE_NEW_2 = f'''                const gasPricePercentMain = {TUNED_PERCENT_STR};
                const percentMain = BigInt(gasPricePercentMain[currentNet] !== undefined ? gasPricePercentMain[currentNet] : 25);
                const gasPriceMain = feeData.gasPrice * percentMain / 100n;'''


def replace_in_file(path, replacements):
    if not os.path.exists(path):
        print(f"[ERROR] Not found: {path}")
        return 0
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    changed = 0
    for old, new in replacements:
        count = content.count(old)
        if count == 0:
            print(f"  [SKIPPED] Pattern not found in {path}")
            continue
        content = content.replace(old, new)
        changed += count
        print(f"  [OK] {path}: {count} replacement(s)")
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return changed


GM_FILE = "templates/gm.html"
GM_OLD = "{ lamina1: 40, nexus: 8, ink: 13, base: 85, robinhood: 100, avax: 700, plume: 25, zetachain: 100 }"
GM_NEW = TUNED_PERCENT_STR

MINT_FILE = "templates/mint.html"
MINT_NFT_FILE = "templates/mint_nft.html"
MINT_OLD = "{ lamina1: 40, nexus: 8, ink: 13, base: 85, robinhood: 100, avax: 2800, plume: 25, zetachain: 100 }"
MINT_NEW = TUNED_PERCENT_STR


def main():
    total = 0
    total += replace_in_file(FLIP_FILE, [(FLIP_OLD, FLIP_NEW)]) or 0
    total += replace_in_file(ORACLE_FILE, [(ORACLE_OLD_1, ORACLE_NEW_1), (ORACLE_OLD_2, ORACLE_NEW_2)]) or 0
    total += replace_in_file(GM_FILE, [(GM_OLD, GM_NEW)]) or 0
    total += replace_in_file(MINT_FILE, [(MINT_OLD, MINT_NEW)]) or 0
    total += replace_in_file(MINT_NFT_FILE, [(MINT_OLD, MINT_NEW)]) or 0
    print(f"\nDone. {total} total replacements.")
    print("Check with: git diff templates/flip.html templates/oracle.html templates/gm.html templates/mint.html templates/mint_nft.html | cat")


if __name__ == "__main__":
    main()
