import io

path = "templates/gm.html"

old_block = """    async function loadLeaderboard() {
        try {
            const result = await contract.getLeaderboard();
            const addrs = result[0], streaks = result[1], scores = result[2];
            let rows = [];
            for (let i = 0; i < addrs.length; i++) {
                rows.push({ addr: addrs[i], streak: Number(streaks[i]), score: Number(scores[i]) / 100 });
            }
            rows.sort((a, b) => b.score - a.score);
            const listEl = document.getElementById("leaderboard-list");
            if (rows.length === 0) {
                listEl.innerHTML = "<p style='color:#666;text-align:center;font-size:0.85em;'>No GMs yet. Be the first.</p>";
                return;
            }
            listEl.innerHTML = rows.slice(0, 10).map((r, i) => `
                <div class="lb-row ${i === 0 ? 'top1' : ''}">
                    <span class="lb-rank">#${i+1}</span>
                    <span class="lb-addr">${r.addr.slice(0,6)}...${r.addr.slice(-4)}</span>
                    <span class="lb-score">${r.score.toFixed(2)}</span>
                </div>
            `).join("");
        } catch (err) { console.log(err); }
    }"""

new_block = """    let leaderboardRows = [];
    let leaderboardPage = 0;
    const LB_PAGE_SIZE = 10;

    async function loadLeaderboard() {
        try {
            const result = await contract.getLeaderboard();
            const addrs = result[0], streaks = result[1], scores = result[2];
            let rows = [];
            for (let i = 0; i < addrs.length; i++) {
                rows.push({ addr: addrs[i], streak: Number(streaks[i]), score: Number(scores[i]) / 100 });
            }
            rows.sort((a, b) => b.score - a.score);
            leaderboardRows = rows;
            leaderboardPage = 0;
            renderLeaderboardPage();
        } catch (err) { console.log(err); }
    }

    function renderLeaderboardPage() {
        const listEl = document.getElementById("leaderboard-list");
        const paginationEl = document.getElementById("lb-pagination");

        if (leaderboardRows.length === 0) {
            listEl.innerHTML = "<p style='color:#666;text-align:center;font-size:0.85em;'>No GMs yet. Be the first.</p>";
            paginationEl.style.display = "none";
            return;
        }

        const totalPages = Math.ceil(leaderboardRows.length / LB_PAGE_SIZE);
        const start = leaderboardPage * LB_PAGE_SIZE;
        const pageRows = leaderboardRows.slice(start, start + LB_PAGE_SIZE);

        listEl.innerHTML = pageRows.map((r, i) => `
            <div class="lb-row ${start + i === 0 ? 'top1' : ''}">
                <span class="lb-rank">#${start + i + 1}</span>
                <span class="lb-addr">${r.addr.slice(0,6)}...${r.addr.slice(-4)}</span>
                <span class="lb-score">${r.score.toFixed(2)}</span>
            </div>
        `).join("");

        if (totalPages > 1) {
            paginationEl.style.display = "flex";
            document.getElementById("lb-page-indicator").innerText = `Page ${leaderboardPage + 1} of ${totalPages}`;
            document.getElementById("lb-prev").disabled = leaderboardPage === 0;
            document.getElementById("lb-next").disabled = leaderboardPage >= totalPages - 1;
        } else {
            paginationEl.style.display = "none";
        }
    }

    function leaderboardPrevPage() {
        if (leaderboardPage > 0) {
            leaderboardPage -= 1;
            renderLeaderboardPage();
        }
    }

    function leaderboardNextPage() {
        const totalPages = Math.ceil(leaderboardRows.length / LB_PAGE_SIZE);
        if (leaderboardPage < totalPages - 1) {
            leaderboardPage += 1;
            renderLeaderboardPage();
        }
    }"""

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if old_block not in content:
    print("ERROR js: old_block not found!")
else:
    content = content.replace(old_block, new_block)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Pagination JS added.")
