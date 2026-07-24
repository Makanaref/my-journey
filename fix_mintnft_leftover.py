with open("templates/mint_nft.html", "r", encoding="utf-8") as f:
    content = f.read()

old_leftover = '''<script>
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

    let provider, signer, account, factoryContract, collectionContract, currentNet, currentCollectionAddress;'''

new_content = '''<script>
    let provider, signer, account, factoryContract, collectionContract, currentNet, currentCollectionAddress;'''

if old_leftover not in content:
    raise SystemExit("ERROR: leftover block not found exactly, aborting. Need manual inspection.")

content = content.replace(old_leftover, new_content, 1)

with open("templates/mint_nft.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. Removed leftover broken getFriendlyError fragment from mint_nft.html.")
