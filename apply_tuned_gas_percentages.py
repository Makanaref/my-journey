"""
apply_tuned_gas_percentages.py
Applies the gas price percentages tuned on the GM page to mint.html and
mint_nft.html, which use the exact same gasPricePercent pattern.
"""

import os

FILES_AND_REPLACEMENTS = {
    "templates/mint.html": [
        (
            'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100, avax: 25, plume: 25, zetachain: 100 };',
            'const gasPricePercent = { lamina1: 40, nexus: 8, ink: 13, base: 85, robinhood: 100, avax: 700, plume: 25, zetachain: 100 };'
        ),
    ],
    "templates/mint_nft.html": [
        (
            'const gasPricePercent = { lamina1: 100, nexus: 25, ink: 25, base: 15, robinhood: 100, avax: 150, plume: 25, zetachain: 100 };',
            'const gasPricePercent = { lamina1: 40, nexus: 8, ink: 13, base: 85, robinhood: 100, avax: 700, plume: 25, zetachain: 100 };'
        ),
    ],
}


def main():
    total_changes = 0
    for path, replacements in FILES_AND_REPLACEMENTS.items():
        if not os.path.exists(path):
            print(f"[ERROR] File not found: {path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        file_changes = 0
        for old, new in replacements:
            count = content.count(old)
            if count == 0:
                print(f"  [SKIPPED] Pattern not found in {path}")
                continue
            content = content.replace(old, new)
            file_changes += count
            print(f"  [OK] {path}: replaced {count} occurrence(s)")

        if file_changes > 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            total_changes += file_changes

    print(f"\nDone. {total_changes} total replacements applied.")
    print("Now check with: git diff templates/mint.html templates/mint_nft.html | cat")


if __name__ == "__main__":
    main()
