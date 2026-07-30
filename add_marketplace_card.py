import re

path = "templates/index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1) Insert the MarketPlace card right after the "Mint NFT" card
mint_nft_card_end = '''<div class="hero-card-title hero-card-title-blue">Mint NFT</div>
                <div class="hero-card-desc">Create and mint your own NFT</div>
                <div class="hero-card-arrow hero-card-arrow-blue">→</div>
            </a>'''

marketplace_card = mint_nft_card_end + '''

            <a href="/marketplace" class="hero-card hero-card-purple">
                <div class="hero-card-icon hero-card-icon-purple">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M4 8l1.5-4h13L20 8" stroke="#c084fc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="rgba(192,132,252,0.1)"/>
                        <path d="M4 8h16v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V8z" stroke="#c084fc" stroke-width="1.5" fill="rgba(192,132,252,0.08)"/>
                        <path d="M9 12a3 3 0 0 0 6 0" stroke="#c084fc" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="hero-card-title hero-card-title-purple">MarketPlace</div>
                <div class="hero-card-desc">Buy, sell and trade onchain items</div>
                <div class="hero-card-arrow hero-card-arrow-purple">→</div>
            </a>'''

if mint_nft_card_end not in content:
    raise SystemExit("❌ الگوی کارت Mint NFT پیدا نشد. فایل index.html تغییر کرده؟")

content = content.replace(mint_nft_card_end, marketplace_card, 1)

# 2) Add the purple color-variant CSS, right before the closing </style> of the hero-card styles
purple_css = '''
        .hero-card-purple:hover {
            border-color: rgba(192,132,252,0.5);
            box-shadow: 0 16px 34px rgba(192,132,252,0.18);
        }
        .hero-card-icon-purple {
            background: rgba(192,132,252,0.1);
            border-color: rgba(192,132,252,0.25);
        }
        .hero-card-title-purple { color:#d8b4fe; }
        .hero-card-arrow-purple {
            color:#c084fc;
            border-color: rgba(192,132,252,0.3);
            background: rgba(192,132,252,0.06);
        }
        .hero-card:hover .hero-card-arrow-purple {
            background: rgba(192,132,252,0.16);
        }
'''

marker = '''        @media (max-width: 560px) {
            .hero-card { width:100%; max-width:320px; }
        }
    </style>'''

if marker not in content:
    raise SystemExit("❌ الگوی انتهای استایل hero-card پیدا نشد.")

content = content.replace(marker, purple_css + marker, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ کارت MarketPlace با موفقیت به templates/index.html اضافه شد.")