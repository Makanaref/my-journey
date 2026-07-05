import io

path = "templates/mint.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add tab button
old1 = '''        <div class="tab-row" style="margin-top:18px;">
            <button class="tab-btn active" id="tab-transfer" onclick="switchTab('transfer')">Transfer</button>
            <button class="tab-btn" id="tab-mint" onclick="switchTab('mint')">Mint</button>
            <button class="tab-btn" id="tab-burn" onclick="switchTab('burn')">Burn</button>
        </div>'''
new1 = '''        <div class="tab-row" style="margin-top:18px;">
            <button class="tab-btn active" id="tab-transfer" onclick="switchTab('transfer')">Transfer</button>
            <button class="tab-btn" id="tab-mint" onclick="switchTab('mint')">Mint</button>
            <button class="tab-btn" id="tab-burn" onclick="switchTab('burn')">Burn</button>
            <button class="tab-btn" id="tab-airdrop" onclick="switchTab('airdrop')">Airdrop</button>
        </div>'''

# 2. Add pane-airdrop after pane-burn, before status message
old2 = '''        <div id="pane-burn" style="display:none;">
            <div class="field">
                <label>Amount to burn</label>
                <input type="number" id="burn-amount" placeholder="0" min="0">
            </div>
            <button class="action-btn-outline" onclick="doBurn()">Burn</button>
        </div>

        <p class="status-msg" id="manage-status"></p>'''
new2 = '''        <div id="pane-burn" style="display:none;">
            <div class="field">
                <label>Amount to burn</label>
                <input type="number" id="burn-amount" placeholder="0" min="0">
            </div>
            <button class="action-btn-outline" onclick="doBurn()">Burn</button>
        </div>

        <div id="pane-airdrop" style="display:none;">
            <p style="color:rgba(255,255,255,0.55); font-size:0.82em; line-height:1.7; margin-bottom:14px;">
                1. Download the Example csv file<br>
                2. Enter your wallet addresses and Enter your amount
            </p>
            <button class="action-btn-outline" style="margin-bottom:16px;" onclick="downloadExampleCsv()">Download Example CSV</button>
            <div class="field">
                <label>Upload CSV file</label>
                <input type="file" id="airdrop-file" accept=".csv" onchange="handleAirdropFile(event)">
            </div>
            <p id="airdrop-preview" style="color:rgba(255,255,255,0.5); font-size:0.8em; margin-bottom:14px;"></p>
            <button class="action-btn" id="airdrop-btn" onclick="doAirdrop()" disabled>Airdrop</button>
            <div id="airdrop-progress" style="margin-top:12px;"></div>
        </div>

        <p class="status-msg" id="manage-status"></p>'''

# 3. Update switchTab function to include airdrop
old3 = '''    function switchTab(tab) {
        ["transfer","mint","burn"].forEach(t => {
            document.getElementById("tab-"+t).classList.toggle("active", t === tab);
            document.getElementById("pane-"+t).style.display = (t === tab) ? "block" : "none";
        });
        document.getElementById("manage-status").innerText = "";
    }'''
new3 = '''    function switchTab(tab) {
        ["transfer","mint","burn","airdrop"].forEach(t => {
            document.getElementById("tab-"+t).classList.toggle("active", t === tab);
            document.getElementById("pane-"+t).style.display = (t === tab) ? "block" : "none";
        });
        document.getElementById("manage-status").innerText = "";
    }

    let airdropRows = [];

    function downloadExampleCsv() {
        const csvContent = "address,amount\\n0xEe90768365f85b85FD5b58b0a076f384920cB7b9,5\\n0xf4c5e6d159b8789fbf384735B010C0129Cae0D6b,3\\n";
        const blob = new Blob([csvContent], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "example-airdrop.csv";
        a.click();
        URL.revokeObjectURL(url);
    }

    function handleAirdropFile(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(e) {
            const text = e.target.result;
            const lines = text.split(/\\r?\\n/).map(l => l.trim()).filter(l => l.length > 0);
            const rows = [];
            let invalidCount = 0;
            for (const line of lines) {
                const parts = line.split(",").map(p => p.trim());
                if (parts.length < 2) continue;
                const [addr, amt] = parts;
                if (addr.toLowerCase() === "address") continue;
                if (!ethers.isAddress(addr) || isNaN(Number(amt)) || Number(amt) <= 0) {
                    invalidCount++;
                    continue;
                }
                rows.push({ address: addr, amount: Number(amt) });
            }
            airdropRows = rows;
            const previewEl = document.getElementById("airdrop-preview");
            const btn = document.getElementById("airdrop-btn");
            if (rows.length === 0) {
                previewEl.innerText = "No valid rows found in this file.";
                btn.disabled = true;
            } else {
                previewEl.innerText = rows.length + " valid recipient(s) found" + (invalidCount > 0 ? ", " + invalidCount + " invalid row(s) skipped." : ".");
                btn.disabled = false;
            }
        };
        reader.readAsText(file);
    }

    async function doAirdrop() {
        if (airdropRows.length === 0) return;
        const btn = document.getElementById("airdrop-btn");
        const progressEl = document.getElementById("airdrop-progress");
        btn.disabled = true;
        let successCount = 0, failCount = 0;

        for (let i = 0; i < airdropRows.length; i++) {
            const row = airdropRows[i];
            progressEl.innerText = "Sending " + (i + 1) + " of " + airdropRows.length + " to " + row.address.slice(0,6) + "..." + row.address.slice(-4) + "...";
            try {
                const overrides = await getTxOverrides();
                const scaled = BigInt(Math.floor(row.amount * 1e18));
                const tx = await tokenContract.transfer(row.address, scaled, overrides);
                await tx.wait();
                successCount++;
            } catch (err) {
                failCount++;
            }
        }

        progressEl.innerText = "Done: " + successCount + " succeeded, " + failCount + " failed.";
        btn.disabled = false;
        await loadSelectedToken();
    }'''

errors = []
if old1 not in content: errors.append("part1 (tab button)")
if old2 not in content: errors.append("part2 (pane html)")
if old3 not in content: errors.append("part3 (switchTab js)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    content = content.replace(old3, new3, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Airdrop feature added to Mint Token page.")
