import io

path = "templates/index.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''                <div class="hero-card-icon hero-card-icon-teal">
                    <span class="hero-emoji hero-emoji-coin">🪙</span>
                </div>'''

new_block = '''                <div class="hero-card-icon hero-card-icon-teal">
                    <span class="hero-emoji hero-emoji-coin">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="9.5" stroke="#2dd4bf" stroke-width="1.5" fill="rgba(45,212,191,0.1)"/>
                            <circle cx="12" cy="12" r="6.5" stroke="#2dd4bf" stroke-width="1" opacity="0.5"/>
                            <text x="12" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#2dd4bf" font-family="Georgia, serif">$</text>
                        </svg>
                    </span>
                </div>'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Homepage coin icon replaced with SVG.")
