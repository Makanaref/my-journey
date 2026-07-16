"""
fix_friendly_errors.py
Replaces long raw error messages (like RPC errors) with short,
user-friendly messages.

Target files: mint_nft.html, mint.html, gm.html, swap.html
"""

import re
import os

TARGET_FILES = [
    "templates/mint_nft.html",
    "templates/mint.html",
    "templates/gm.html",
    "templates/swap.html",
]

FRIENDLY_ERROR_FUNCTION = """
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
"""

REPLACEMENT_PATTERNS = [
    (re.compile(r'err\.reason\s*\|\|\s*err\.message\s*\|\|\s*["\'][^"\']*["\']'),
     "getFriendlyError(err)"),
    (re.compile(r'err\.reason\s*\|\|\s*err\.message(?!\s*\|\|)'),
     "getFriendlyError(err)"),
    (re.compile(r'err\.message\s*\|\|\s*["\'][^"\']*["\']'),
     "getFriendlyError(err)"),
]


def process_file(path):
    if not os.path.exists(path):
        print(f"  [SKIPPED] Not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = 0

    for pattern, replacement in REPLACEMENT_PATTERNS:
        content, n = pattern.subn(replacement, content)
        changes += n

    if "function getFriendlyError" not in content:
        content = content.replace("<script>", "<script>\n" + FRIENDLY_ERROR_FUNCTION, 1)
        changes += 1

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [UPDATED] {path}  ({changes} changes)")
    else:
        print(f"  [NO CHANGE] {path}")


def main():
    print("Fixing error messages...\n")
    for filepath in TARGET_FILES:
        process_file(filepath)
    print("\nDone. Now check the files with git diff.")


if __name__ == "__main__":
    main()
