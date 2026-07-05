import io

path = "templates/games.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''        <a href="/flip" class="game-card">
            <div style="font-size:2.6em; margin-bottom:12px;">🪙</div>'''

new_block = '''        <a href="/flip" class="game-card">
            <div style="margin-bottom:12px; display:flex; justify-content:center;">
                <svg width="42" height="42" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="9.5" stroke="#e94560" stroke-width="1.5" fill="rgba(233,69,96,0.1)"/>
                    <circle cx="12" cy="12" r="6.5" stroke="#e94560" stroke-width="1" opacity="0.5"/>
                    <text x="12" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#e94560" font-family="Georgia, serif">H</text>
                </svg>
            </div>'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Games page Coin Flip card icon replaced with SVG.")
