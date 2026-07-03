import io

path = "templates/gm.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = """            leaderboardPage = 0;
            updateLamps(Math.min(rows.length, LAMP_CFG.length));
            renderLeaderboardPage();"""
new1 = """            leaderboardPage = 0;

            const today = todayDayNumber();
            const statsResults = await Promise.all(
                addrs.map(addr => contract.getStats(addr).catch(() => null))
            );
            const todayCount = statsResults.filter(s => s && Number(s[2]) === today).length;
            updateLamps(Math.min(todayCount, LAMP_CFG.length));

            renderLeaderboardPage();"""

old2 = """    function leaderboardPrevPage() { if (leaderboardPage > 0) { leaderboardPage--; renderLeaderboardPage(); } }
    function leaderboardNextPage() { const t = Math.ceil(leaderboardRows.length / LB_PAGE_SIZE); if (leaderboardPage < t - 1) { leaderboardPage++; renderLeaderboardPage(); } }"""
new2 = """    function leaderboardPrevPage() { if (leaderboardPage > 0) { leaderboardPage--; renderLeaderboardPage(); } }
    function leaderboardNextPage() { const t = Math.ceil(leaderboardRows.length / LB_PAGE_SIZE); if (leaderboardPage < t - 1) { leaderboardPage++; renderLeaderboardPage(); } }

    // Keep lamps in sync with Tehran midnight reset even if the page stays open
    setInterval(() => {
        if (contract) loadLeaderboard();
    }, 120000);"""

errors = []
if old1 not in content: errors.append("part1 (today count logic)")
if old2 not in content: errors.append("part2 (auto-refresh timer)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Lamps now track today-only GMs with auto-refresh.")
