import io

path = "templates/flip.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''        try {
            const overrides = await getTxOverrides();
            const tx = await contract.flip(guessHeads, overrides);
            document.getElementById("flip-status").innerText = "Confirming...";
            const receipt = await tx.wait();

            let won = null, result = null;
            for (const log of receipt.logs) {
                try {
                    const parsed = contract.interface.parseLog(log);
                    if (parsed && parsed.name === "Flip") {
                        won = parsed.args.won;
                        result = parsed.args.result;
                        break;
                    }
                } catch (e) {}
            }

            coin.classList.add(result ? "result-heads" : "result-tails");'''

new_block = '''        try {
            const statsBefore = await contract.getStats(account);
            const winsBefore = Number(statsBefore[2]);

            const overrides = await getTxOverrides();
            const tx = await contract.flip(guessHeads, overrides);
            document.getElementById("flip-status").innerText = "Confirming...";
            const receipt = await tx.wait();

            let won = null, result = null;
            const iface = new ethers.Interface(CONTRACT_ABI.concat([
                "event Flip(address indexed player, bool guessedHeads, bool result, bool won, uint64 currentStreak)"
            ]));
            for (const log of receipt.logs) {
                try {
                    const parsed = iface.parseLog(log);
                    if (parsed && parsed.name === "Flip") {
                        won = parsed.args.won;
                        result = parsed.args.result;
                        break;
                    }
                } catch (e) {}
            }

            if (won === null) {
                const statsAfter = await contract.getStats(account);
                const winsAfter = Number(statsAfter[2]);
                won = winsAfter > winsBefore;
                result = won ? guessHeads : !guessHeads;
            }

            coin.classList.add(result ? "result-heads" : "result-tails");'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Flip result detection made more reliable.")
