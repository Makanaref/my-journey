import io

path = "templates/index.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''                <div class="hero-card-title hero-card-title-teal">Mint Token</div>
                <div class="hero-card-desc">Create and manage your own token</div>
                <div class="hero-card-arrow hero-card-arrow-teal">→</div>
            </a>
        </div>
    </div>'''

new_block = '''                <div class="hero-card-title hero-card-title-teal">Mint Token</div>
                <div class="hero-card-desc">Create and manage your own token</div>
                <div class="hero-card-arrow hero-card-arrow-teal">→</div>
            </a>

            <a href="/mint-nft" class="hero-card hero-card-blue">
                <div class="hero-card-icon hero-card-icon-blue">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="3" width="18" height="18" rx="3" stroke="#7ec8e3" stroke-width="1.5" fill="rgba(126,200,227,0.1)"/>
                        <circle cx="9" cy="9" r="2" stroke="#7ec8e3" stroke-width="1.3"/>
                        <path d="M3 16l5-5 4 4 3-3 6 6" stroke="#7ec8e3" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="hero-card-title hero-card-title-blue">Mint NFT</div>
                <div class="hero-card-desc">Create and mint your own NFT</div>
                <div class="hero-card-arrow hero-card-arrow-blue">→</div>
            </a>
        </div>
    </div>'''

old_css = '''        @media (max-width: 560px) {
            .hero-card { width:100%; max-width:320px; }
        }
    </style>'''

new_css = '''        .hero-card-blue:hover {
            border-color: rgba(126,200,227,0.5);
            box-shadow: 0 16px 34px rgba(126,200,227,0.18);
        }
        .hero-card-icon-blue {
            background: rgba(126,200,227,0.1);
            border-color: rgba(126,200,227,0.25);
        }
        .hero-card-title-blue { color:#9adcf2; }
        .hero-card-arrow-blue {
            color:#7ec8e3;
            border-color: rgba(126,200,227,0.3);
            background: rgba(126,200,227,0.06);
        }
        .hero-card:hover .hero-card-arrow-blue {
            background: rgba(126,200,227,0.16);
        }
        @media (max-width: 560px) {
            .hero-card { width:100%; max-width:320px; }
        }
    </style>'''

errors = []
if old_block not in content: errors.append("part1 (card html)")
if old_css not in content: errors.append("part2 (css)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old_block, new_block, 1)
    content = content.replace(old_css, new_css, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Mint NFT card added to homepage.")
