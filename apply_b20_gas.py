"""
apply_b20_gas.py
Applies the tuned 85% Base gas price multiplier to all 5 transactions
in b20.html, replacing the full (100%) feeData.gasPrice with 85% of it.
"""

import os

FILE = "templates/b20.html"
OLD = "feeData.gasPrice"
NEW = "(feeData.gasPrice * 85n / 100n)"


def main():
    if not os.path.exists(FILE):
        print(f"[ERROR] Not found: {FILE}")
        return

    with open(FILE, "r", encoding="utf-8") as f:
        content = f.read()

    count = content.count(OLD)
    if count == 0:
        print("[SKIPPED] Pattern not found")
        return

    content = content.replace(OLD, NEW)

    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Replaced {count} occurrence(s) in {FILE}")
    print("Check with: git diff templates/b20.html | cat")


if __name__ == "__main__":
    main()
