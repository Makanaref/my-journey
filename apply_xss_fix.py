with open("templates/my_store.html", "r", encoding="utf-8") as f:
    content = f.read()

old_render_nfts = '''    function renderNfts(nfts) {
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
    }'''

new_render_nfts = '''    function renderNfts(nfts) {
        const grid = document.getElementById("nft-grid");
        grid.innerHTML = "";
        nfts.forEach(n => {
            const card = document.createElement("div");
            card.className = "nft-card";

            let imageEl;
            if (n.image) {
                imageEl = document.createElement("img");
                imageEl.className = "nft-card-image";
                imageEl.loading = "lazy";
                imageEl.src = n.image; // set via property, not HTML string, to avoid attribute injection
            } else {
                imageEl = document.createElement("div");
                imageEl.className = "nft-card-image";
                imageEl.style.display = "flex";
                imageEl.style.alignItems = "center";
                imageEl.style.justifyContent = "center";
                imageEl.style.color = "#444";
                imageEl.style.fontSize = "0.75em";
                imageEl.innerText = "No image";
            }

            const body = document.createElement("div");
            body.className = "nft-card-body";

            const nameEl = document.createElement("div");
            nameEl.className = "nft-card-name";
            nameEl.innerText = n.name || "Untitled";

            const metaEl = document.createElement("div");
            metaEl.className = "nft-card-meta";

            const netEl = document.createElement("span");
            netEl.className = "nft-card-net";
            netEl.innerText = n.network_label || "";
            metaEl.appendChild(netEl);

            if (n.is_creator) {
                const badgeEl = document.createElement("span");
                badgeEl.className = "nft-card-badge";
                badgeEl.innerText = "Created by you";
                metaEl.appendChild(badgeEl);
            }

            const linkEl = document.createElement("a");
            linkEl.className = "nft-card-btn";
            linkEl.innerText = "View / Manage";
            // Build the URL with URLSearchParams so values are properly encoded,
            // preventing attribute/HTML injection from malicious contract data.
            const params = new URLSearchParams({ net: n.network || "", collection: n.collection || "" });
            linkEl.href = "/mint-nft?" + params.toString();

            body.appendChild(nameEl);
            body.appendChild(metaEl);
            body.appendChild(linkEl);

            card.appendChild(imageEl);
            card.appendChild(body);
            grid.appendChild(card);
        });
        document.getElementById("nft-empty").style.display = nfts.length ? "none" : "block";
    }'''

if old_render_nfts not in content:
    raise SystemExit("ERROR: renderNfts function not found, aborting.")
content = content.replace(old_render_nfts, new_render_nfts, 1)

with open("templates/my_store.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. XSS fix applied to my_store.html (renderNfts).")
