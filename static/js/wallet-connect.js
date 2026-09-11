(function () {
    const WALLETCONNECT_PROJECT_ID = "e781601143322e98b2967cd4a531352d";

    const discovered = new Map();

    window.addEventListener("eip6963:announceProvider", (event) => {
        const { info, provider } = event.detail;
        discovered.set(info.uuid, { info, provider });
    });
    window.dispatchEvent(new Event("eip6963:requestProvider"));

    let wcProviderInstance = null;

    if (typeof window.process === "undefined") {
        window.process = { env: {}, version: "", browser: true, nextTick: (fn, ...args) => setTimeout(() => fn(...args), 0) };
    }
    if (typeof window.global === "undefined") {
        window.global = window;
    }
    if (typeof window.Buffer === "undefined") {
        window.Buffer = { isBuffer: () => false };
    }

    async function getWalletConnectProvider() {
        if (wcProviderInstance) return wcProviderInstance;
        if (typeof window.EthereumProvider === "undefined") {
            await new Promise((resolve, reject) => {
                const script = document.createElement("script");
                script.src = "https://cdn.jsdelivr.net/npm/@walletconnect/ethereum-provider@2.13.3/dist/index.umd.js";
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        }
        wcProviderInstance = await window.EthereumProvider.init({
            projectId: WALLETCONNECT_PROJECT_ID,
            chains: [1],
            showQrModal: true,
            optionalChains: [1, 8453, 10, 43114],
        });
        return wcProviderInstance;
    }

    function buildModal() {
        const overlay = document.createElement("div");
        overlay.id = "sgm-wallet-modal-overlay";
        overlay.style.cssText = `
            position: fixed; inset: 0; background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px); z-index: 10000;
            display: flex; align-items: center; justify-content: center;
        `;

        const box = document.createElement("div");
        box.style.cssText = `
            background: #16213e; border: 1px solid rgba(233,69,96,0.2);
            border-radius: 16px; width: 340px; max-width: 90vw;
            padding: 20px; font-family: 'Inter', sans-serif; color: #eee;
        `;

        const title = document.createElement("div");
        title.innerText = "Connect a wallet";
        title.style.cssText = "font-weight:700; font-size:1.1em; margin-bottom:14px;";
        box.appendChild(title);

        const list = document.createElement("div");
        list.style.cssText = "display:flex; flex-direction:column; gap:8px;";
        box.appendChild(list);

        overlay.appendChild(box);
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) overlay._resolve(null);
        });

        return { overlay, list };
    }

    function addOption(list, { name, iconHtml, badge, onClick }) {
        const row = document.createElement("button");
        row.style.cssText = `
            display:flex; align-items:center; justify-content:space-between; gap:12px;
            width:100%; padding:12px 14px; border-radius:12px; cursor:pointer;
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
            color:#eee; font-size:0.95em; font-weight:600; text-align:left;
            transition: background 0.2s, border-color 0.2s;
        `;
        row.onmouseenter = () => { row.style.borderColor = "rgba(233,69,96,0.4)"; };
        row.onmouseleave = () => { row.style.borderColor = "rgba(255,255,255,0.08)"; };
        row.innerHTML = `
            <span style="display:flex; align-items:center; gap:10px;">${iconHtml}${name}</span>
            ${badge ? `<span style="font-size:0.7em; color:#4ade80; border:1px solid rgba(74,222,128,0.3); padding:2px 8px; border-radius:10px;">${badge}</span>` : ""}
        `;
        row.onclick = onClick;
        list.appendChild(row);
    }

    window.SGMWallet = {
        activeProvider: null,

        selectProvider() {
            return new Promise((resolve) => {
                const { overlay, list } = buildModal();
                overlay._resolve = (result) => {
                    document.body.removeChild(overlay);
                    resolve(result);
                };

                for (const { info, provider } of discovered.values()) {
                    addOption(list, {
                        name: info.name,
                        iconHtml: `<img src="${info.icon}" style="width:24px;height:24px;border-radius:6px;">`,
                        badge: "Installed",
                        onClick: () => {
                            window.SGMWallet.activeProvider = provider;
                            overlay._resolve(provider);
                        },
                    });
                }

                if (discovered.size === 0 && window.ethereum) {
                    addOption(list, {
                        name: "Browser Wallet",
                        iconHtml: `<i class="fas fa-wallet" style="width:24px;text-align:center;color:#e94560;"></i>`,
                        badge: "Detected",
                        onClick: () => {
                            window.SGMWallet.activeProvider = window.ethereum;
                            overlay._resolve(window.ethereum);
                        },
                    });
                }

                addOption(list, {
                    name: "WalletConnect",
                    iconHtml: `<i class="fas fa-qrcode" style="width:24px;text-align:center;color:#3396ff;"></i>`,
                    badge: null,
                    onClick: async () => {
                        overlay._resolve(null);
                        try {
                            const wcProvider = await getWalletConnectProvider();
                            await wcProvider.enable();
                            window.SGMWallet.activeProvider = wcProvider;
                            if (window.SGMWallet._onWcConnected) window.SGMWallet._onWcConnected(wcProvider);
                        } catch (err) {
                            console.error("WalletConnect failed:", err);
                        }
                    },
                });

                document.body.appendChild(overlay);
            });
        },

        onWalletConnectConnected(cb) {
            this._onWcConnected = cb;
        },
    };
})();
