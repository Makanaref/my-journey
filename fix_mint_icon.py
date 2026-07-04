import io

path = "templates/mint.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''    <div class="mint-orb">🪙</div>'''

new_block = '''    <div class="mint-orb">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9.5" stroke="#f7b32b" stroke-width="1.5" fill="rgba(247,179,43,0.08)"/>
            <circle cx="12" cy="12" r="6.5" stroke="#f7b32b" stroke-width="1" opacity="0.5"/>
            <text x="12" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#f7b32b" font-family="Georgia, serif">$</text>
        </svg>
    </div>'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Mint page icon replaced with SVG coin.")
