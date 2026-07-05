import io

path = "templates/flip.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = '''            <div class="coin-face heads">🪙</div>
            <div class="coin-face tails">⭐</div>'''
new1 = '''            <div class="coin-face heads">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="9.5" stroke="#e94560" stroke-width="1.5" fill="rgba(233,69,96,0.1)"/>
                    <circle cx="12" cy="12" r="6.5" stroke="#e94560" stroke-width="1" opacity="0.5"/>
                    <text x="12" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#e94560" font-family="Georgia, serif">H</text>
                </svg>
            </div>
            <div class="coin-face tails">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="9.5" stroke="#f7b32b" stroke-width="1.5" fill="rgba(247,179,43,0.1)"/>
                    <circle cx="12" cy="12" r="6.5" stroke="#f7b32b" stroke-width="1" opacity="0.5"/>
                    <text x="12" y="16" text-anchor="middle" font-size="9" font-weight="700" fill="#f7b32b" font-family="Georgia, serif">T</text>
                </svg>
            </div>'''

old2 = '''            <button class="guess-btn" id="btn-heads" onclick="doFlip(true)">🪙 Heads</button>
            <button class="guess-btn" id="btn-tails" onclick="doFlip(false)">⭐ Tails</button>'''
new2 = '''            <button class="guess-btn" id="btn-heads" onclick="doFlip(true)">Heads</button>
            <button class="guess-btn" id="btn-tails" onclick="doFlip(false)">Tails</button>'''

errors = []
if old1 not in content: errors.append("part1 (coin faces)")
if old2 not in content: errors.append("part2 (guess buttons)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Flip icons replaced with SVG.")
