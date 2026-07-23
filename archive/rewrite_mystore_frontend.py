import io

path = "templates/my_store.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

script_start = content.find("<script src=")
if script_start == -1:
    print("ERROR: could not find <script src= tag!")
else:
    head = content[:script_start]

    new_script = '''<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>
<script>
    async function connectAndScanAll() {
        if (!window.ethereum) { alert("Please install MetaMask!"); return; }
        try {
            const tempProvider = new ethers.BrowserProvider(window.ethereum);
            await tempProvider.send("eth_requestAccounts", []);
            const signer = await tempProvider.getSigner();
            const account = await signer.getAddress();

            document.getElementById("connect-section").style.display = "none";
            document.getElementById("wallet-info").style.display = "block";
            document.getElementById("wallet-addr").innerText = account.slice(0,6) + "..." + account.slice(-4);
            document.getElementById("scan-area").style.display = "block";

            const res = await fetch("/api/scan-wallet?account=" + account);
            const data = await res.json();

            document.getElementById("scan-spinner").style.display = "none";
            document.getElementById("scan-status").innerText = "";

            if (!res.ok) {
                document.getElementById("scan-status").innerText = "Failed to scan: " + (data.error || "unknown error");
                return;
            }

            renderNfts(data.nfts || []);
            renderTokens(data.tokens || []);
            renderRanks(data.ranks || []);

            document.getElementById("tab-nav").style.display = "flex";
        } catch (err) {
            alert("Connection failed: " + err.message);
        }
    }

    function switchStoreTab(tab) {
        ["nft", "token", "rank"].forEach(t => {
            document.getElementById("tab-" + t).classList.toggle("active", t === tab);
            document.getElementById("pane-" + t).style.display = (t === tab) ? "block" : "none";
        });
    }

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.innerText = str || "Untitled";
        return div.innerHTML;
    }

    function renderNfts(nfts) {
        const grid = document.getElementById("nft-grid");
        grid.innerHTML = "";
        nfts.forEach(n => {
            const card = document.createElement("div");
            card.className = "nft-card";
            const badge = n.is_creator ? '<span class="nft-card-badge">Created by you</span>' : "";
            const imageHtml = n.image
                ? `<img class="nft-card-image" src="${n.image}" loading="lazy">`
                : `<div class="nft-card-image" style="display:flex;align-items:center;justify-content:center;color:#444;font-size:0.75em;">No image</div>`;
            card.innerHTML = `
                ${imageHtml}
                <div class="nft-card-body">
                    <div class="nft-card-name">${escapeHtml(n.name)}</div>
                    <div class="nft-card-meta">
                        <span class="nft-card-net">${n.network_label}</span>
                        ${badge}
                    </div>
                    <a class="nft-card-btn" href="/mint-nft?net=${n.network}&collection=${n.collection}">View / Manage</a>
                </div>
            `;
            grid.appendChild(card);
        });
        document.getElementById("nft-empty").style.display = nfts.length ? "none" : "block";
    }

    function renderTokens(tokens) {
        const grid = document.getElementById("token-grid");
        grid.innerHTML = "";
        tokens.forEach(t => {
            const card = document.createElement("div");
            card.className = "token-card";
            card.innerHTML = `
                <div class="token-card-symbol">${escapeHtml(t.symbol)}</div>
                <div class="token-card-name">${escapeHtml(t.name)}</div>
                <div class="token-card-row"><span>Network</span><span>${t.network_label}</span></div>
                <div class="token-card-row"><span>Balance</span><span>${Number(t.balance).toLocaleString(undefined, {maximumFractionDigits: 4})} ${escapeHtml(t.symbol)}</span></div>
            `;
            grid.appendChild(card);
        });
        document.getElementById("token-empty").style.display = tokens.length ? "none" : "block";
    }

    function renderRanks(ranks) {
        const grid = document.getElementById("rank-grid");
        grid.innerHTML = "";
        ranks.forEach(r => {
            let rowsHtml = "";
            if (r.gm_streak !== undefined) {
                rowsHtml += `<div class="rank-stat-row"><span>GM streak</span><span class="rank-value">${r.gm_streak}</span></div>`;
                rowsHtml += `<div class="rank-stat-row"><span>GM score</span><span class="rank-value">${r.gm_score}</span></div>`;
            }
            if (r.flip_total !== undefined) {
                rowsHtml += `<div class="rank-stat-row"><span>Coin Flip best streak</span><span class="rank-value">${r.flip_best}</span></div>`;
                rowsHtml += `<div class="rank-stat-row"><span>Coin Flip wins</span><span class="rank-value">${r.flip_wins} / ${r.flip_total}</span></div>`;
            }
            if (r.oracle_total !== undefined) {
                rowsHtml += `<div class="rank-stat-row"><span>Oracle correct</span><span class="rank-value">${r.oracle_correct} / ${r.oracle_total}</span></div>`;
            }
            const card = document.createElement("div");
            card.className = "rank-card";
            card.innerHTML = `<div class="rank-card-title">🏆 ${r.network_label}</div>${rowsHtml}`;
            grid.appendChild(card);
        });
        document.getElementById("rank-empty").style.display = ranks.length ? "none" : "block";
    }
</script>
{% endblock %}
'''

    new_content = head + new_script
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS: my_store.html frontend rewritten to use fast server-side API.")
