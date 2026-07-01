import io

path = "templates/gm.html"

old_block = """    <div id="leaderboard-card" style="display:none;">
        <div class="lb-wrap">
            <p class="lb-title">LEADERBOARD</p>
            <div id="leaderboard-list"></div>
        </div>
    </div>"""

new_block = """    <div id="leaderboard-card" style="display:none;">
        <div class="lb-wrap">
            <p class="lb-title">LEADERBOARD</p>
            <div id="leaderboard-list"></div>
            <div id="lb-pagination" style="display:none; align-items:center; justify-content:center; gap:16px; margin-top:16px;">
                <button id="lb-prev" onclick="leaderboardPrevPage()" class="lb-page-btn">← Prev</button>
                <span id="lb-page-indicator" style="color:#999; font-size:0.85em;"></span>
                <button id="lb-next" onclick="leaderboardNextPage()" class="lb-page-btn">Next →</button>
            </div>
        </div>
    </div>

    <style>
        .lb-page-btn {
            padding:7px 16px; border-radius:8px; font-size:0.85em; font-weight:600;
            border:1px solid rgba(233,69,96,0.35); background:rgba(233,69,96,0.08);
            color:#e94560; cursor:pointer;
            transition:background 0.2s ease, transform 0.2s ease;
        }
        .lb-page-btn:hover:not(:disabled) {
            background:rgba(233,69,96,0.18);
            transform:translateY(-1px);
        }
        .lb-page-btn:disabled {
            opacity:0.35; cursor:not-allowed;
        }
    </style>"""

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_block not in content:
    print("ERROR html: old_block not found!")
else:
    content = content.replace(old_block, new_block)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Pagination HTML added.")
