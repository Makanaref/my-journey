import io

path = "templates/games.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''        <div class="game-card game-card-disabled">
            <div style="font-size:2.6em; margin-bottom:12px;">➕</div>
            <div style="font-weight:700; font-size:1.15em; color:#fff;">More Soon</div>
            <div style="color:rgba(255,255,255,0.45); font-size:0.85em; margin-top:8px;">New games coming</div>
        </div>'''

new_block = '''        <a href="/flip" class="game-card">
            <div style="font-size:2.6em; margin-bottom:12px;">🪙</div>
            <div style="font-weight:700; font-size:1.15em; color:#fff;">Coin Flip</div>
            <div style="color:rgba(255,255,255,0.45); font-size:0.85em; margin-top:8px;">Guess heads or tails, onchain</div>
        </a>

        <div class="game-card game-card-disabled">
            <div style="font-size:2.6em; margin-bottom:12px;">➕</div>
            <div style="font-weight:700; font-size:1.15em; color:#fff;">More Soon</div>
            <div style="color:rgba(255,255,255,0.45); font-size:0.85em; margin-top:8px;">New games coming</div>
        </div>'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Coin Flip card added to games page.")
