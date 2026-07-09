import io

path = "templates/mint_nft.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add mint-only view HTML, right before the closing </div> of .nft-wrap and before the script tag
old1 = '''</div>

<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>'''

new1 = '''    <div id="mint-view-panel" class="panel" style="display:none; text-align:center;">
        <img id="mv-image" style="width:100%; max-width:280px; border-radius:14px; margin-bottom:16px;">
        <h2 id="mv-name" style="margin-bottom:6px;">—</h2>
        <p id="mv-description" style="color:rgba(255,255,255,0.5); font-size:0.85em; margin-bottom:16px;"></p>
        <div class="nft-info-row"><span>Minted</span><span id="mv-minted">—</span></div>
        <div class="nft-info-row"><span>Price</span><span id="mv-price">—</span></div>
        <div id="mv-connect-wrap" style="margin-top:18px;">
            <button class="btn" onclick="connectWallet()" style="padding:12px 32px;">Connect wallet to mint</button>
        </div>
        <button class="action-btn" id="mv-mint-btn" style="display:none; margin-top:18px;" onclick="mintFromMintView()">Mint one</button>
        <p class="status-msg" id="mv-status"></p>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/ethers@6.13.0/dist/ethers.umd.min.js"></script>'''

# 2. Modify connectWallet to auto-switch network when URL params exist
old2 = '''    async function connectWallet() {
        if (!window.ethereum) { alert("Please install MetaMask!"); return; }
        try {
            provider = new ethers.BrowserProvider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            signer = await provider.getSigner();
            account = await signer.getAddress();
            document.getElementById("connect-section").style.display = "none";
            document.getElementById("wallet-info").style.display = "block";
            document.getElementById("wallet-addr").innerText = account.slice(0,6) + "..." + account.slice(-4);
            document.getElementById("network-card").style.display = "block";
        } catch (err) { alert("Connection failed: " + err.message); }
    }'''

new2 = '''    function getUrlParams() {
        const params = new URLSearchParams(window.location.search);
        return { net: params.get("net"), collection: params.get("collection"), meta: params.get("meta") };
    }

    async function connectWallet() {
        if (!window.ethereum) { alert("Please install MetaMask!"); return; }
        try {
            provider = new ethers.BrowserProvider(window.ethereum);
            await provider.send("eth_requestAccounts", []);
            signer = await provider.getSigner();
            account = await signer.getAddress();
            document.getElementById("wallet-info").style.display = "block";
            document.getElementById("wallet-addr").innerText = account.slice(0,6) + "..." + account.slice(-4);

            const urlParams = getUrlParams();
            if (urlParams.net && urlParams.collection && networks[urlParams.net]) {
                document.getElementById("connect-section").style.display = "none";
                document.getElementById("mv-connect-wrap").style.display = "none";
                await switchNetwork(urlParams.net);
            } else {
                document.getElementById("connect-section").style.display = "none";
                document.getElementById("network-card").style.display = "block";
            }
        } catch (err) { alert("Connection failed: " + err.message); }
    }

    async function loadMintView(addr, metaUrl) {
        currentCollectionAddress = addr;
        collectionContract = new ethers.Contract(addr, COLLECTION_ABI, signer);

        document.getElementById("network-card").style.display = "none";
        document.getElementById("create-panel").style.display = "none";
        document.getElementById("mycollections-panel").style.display = "none";
        document.getElementById("manage-panel").style.display = "none";
        document.getElementById("mint-view-panel").style.display = "block";

        if (metaUrl) {
            try {
                const metaRes = await fetch(metaUrl);
                const meta = await metaRes.json();
                document.getElementById("mv-image").src = meta.image || "";
                document.getElementById("mv-description").innerText = meta.description || "";
            } catch (e) {}
        }

        try {
            const [name, maxSupply, mintPrice, totalMinted] = await Promise.all([
                collectionContract.name(),
                collectionContract.maxSupply(),
                collectionContract.mintPrice(),
                collectionContract.totalMinted()
            ]);
            document.getElementById("mv-name").innerText = name;
            document.getElementById("mv-minted").innerText = totalMinted.toString() + " / " + maxSupply.toString();
            document.getElementById("mv-price").innerText = mintPrice === 0n ? "Free" : ethers.formatEther(mintPrice) + " " + networks[currentNet].nativeCurrency.symbol;

            const mintBtn = document.getElementById("mv-mint-btn");
            mintBtn.style.display = "inline-block";
            mintBtn.disabled = Number(totalMinted) >= Number(maxSupply);
            mintBtn.innerText = Number(totalMinted) >= Number(maxSupply) ? "Sold out" : "Mint one";
        } catch (err) {
            document.getElementById("mv-status").innerText = "Failed to load collection info.";
        }
    }

    async function mintFromMintView() {
        if (!collectionContract) return;
        const btn = document.getElementById("mv-mint-btn");
        const statusEl = document.getElementById("mv-status");
        btn.disabled = true;
        statusEl.innerText = "Sending...";
        try {
            const mintPrice = await collectionContract.mintPrice();
            const overrides = await getTxOverrides();
            overrides.value = mintPrice;
            const tx = await collectionContract.mint(overrides);
            statusEl.innerText = "Confirming...";
            await tx.wait();
            statusEl.innerText = "Minted ✅";
            const urlParams = getUrlParams();
            await loadMintView(currentCollectionAddress, urlParams.meta);
        } catch (err) {
            statusEl.innerText = "Failed: " + (err.reason || err.message || "unknown error");
            btn.disabled = false;
        }
    }'''

# 3. Modify switchNetwork to call loadMintView when URL params are present, instead of the normal creator flow
old3 = '''            factoryContract = new ethers.Contract(FACTORY_ADDRESSES[net], FACTORY_ABI, signer);
            document.getElementById("create-panel").style.display = "block";
            document.getElementById("mycollections-panel").style.display = "block";
            document.getElementById("manage-panel").style.display = "none";
            document.getElementById("create-nft-status").innerText = "";
            document.getElementById("share-link-box").style.display = "none";
            await loadMyCollections();
            await maybeLoadFromUrl();'''

new3 = '''            factoryContract = new ethers.Contract(FACTORY_ADDRESSES[net], FACTORY_ABI, signer);

            const urlParams = getUrlParams();
            if (urlParams.net && urlParams.collection) {
                await loadMintView(urlParams.collection, urlParams.meta);
            } else {
                document.getElementById("create-panel").style.display = "block";
                document.getElementById("mycollections-panel").style.display = "block";
                document.getElementById("manage-panel").style.display = "none";
                document.getElementById("create-nft-status").innerText = "";
                document.getElementById("share-link-box").style.display = "none";
                await loadMyCollections();
            }'''

errors = []
if old1 not in content: errors.append("part1 (mint view html)")
if old2 not in content: errors.append("part2 (connectWallet + loadMintView)")
if old3 not in content: errors.append("part3 (switchNetwork branch)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    content = content.replace(old3, new3, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Mint-only view added for shared links.")
