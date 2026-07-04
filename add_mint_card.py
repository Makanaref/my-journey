import io

path = "templates/index.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''            <a href="/games" class="hero-card hero-card-gold">
                <div class="hero-card-icon hero-card-icon-gold">
                    <span class="hero-emoji hero-emoji-game">🎮</span>
                </div>
                <div class="hero-card-title hero-card-title-gold">Onchain Game</div>
                <div class="hero-card-desc">Play small onchain experiments</div>
                <div class="hero-card-arrow hero-card-arrow-gold">→</div>
            </a>

        </div>
    </div>'''

new_block = '''            <a href="/games" class="hero-card hero-card-gold">
                <div class="hero-card-icon hero-card-icon-gold">
                    <span class="hero-emoji hero-emoji-game">🎮</span>
                </div>
                <div class="hero-card-title hero-card-title-gold">Onchain Game</div>
                <div class="hero-card-desc">Play small onchain experiments</div>
                <div class="hero-card-arrow hero-card-arrow-gold">→</div>
            </a>

            <a href="/mint" class="hero-card hero-card-teal">
                <div class="hero-card-icon hero-card-icon-teal">
                    <span class="hero-emoji hero-emoji-coin">🪙</span>
                </div>
                <div class="hero-card-title hero-card-title-teal">Mint Token</div>
                <div class="hero-card-desc">Create and manage your own token</div>
                <div class="hero-card-arrow hero-card-arrow-teal">→</div>
            </a>

        </div>
    </div>'''

old_css = '''        @media (max-width: 560px) {
            .hero-card { width:100%; max-width:320px; }
        }
    </style>'''

new_css = '''        .hero-card-teal:hover {
            border-color: rgba(45,212,191,0.5);
            box-shadow: 0 16px 34px rgba(45,212,191,0.18);
        }
        .hero-card-icon-teal {
            background: rgba(45,212,191,0.1);
            border-color: rgba(45,212,191,0.25);
        }
        .hero-card-title-teal { color:#5eead4; }
        .hero-card-arrow-teal {
            color:#2dd4bf;
            border-color: rgba(45,212,191,0.3);
            background: rgba(45,212,191,0.06);
        }
        .hero-card:hover .hero-card-arrow-teal {
            background: rgba(45,212,191,0.16);
        }
        .hero-emoji-coin {
            display:inline-block;
            animation: floaty 2.6s ease-in-out infinite;
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
    print("SUCCESS: Mint Token card added to homepage.")
