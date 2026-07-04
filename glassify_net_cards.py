import io

files = ["templates/gm.html", "templates/oracle.html", "templates/mint.html"]

old_block = """    .net-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px; padding: 16px;
        cursor: pointer; transition: all 0.2s; text-align: left;
    }
    .net-card:hover { border-color: rgba(233,69,96,0.4); background: rgba(255,255,255,0.04); }
    .net-card.active { border-color: #e94560; background: rgba(233,69,96,0.07); }
    .net-card .symbol { font-size: 1.1em; font-weight: 600; color: #fff; }
    .net-card .name { color: #777; font-size: 0.8em; margin-top: 2px; }"""

new_block = """    .net-card {
        position: relative;
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px; padding: 16px 18px;
        cursor: pointer; transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
        text-align: left;
        overflow: hidden;
    }
    .net-card::before {
        content: "";
        position: absolute; inset: 0;
        background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.06), rgba(0,0,0,0) 60%);
        pointer-events: none;
    }
    .net-card:hover {
        border-color: rgba(233,69,96,0.45);
        background: linear-gradient(160deg, rgba(233,69,96,0.08), rgba(255,255,255,0.02));
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(233,69,96,0.12);
    }
    .net-card.active {
        border-color: #e94560;
        background: linear-gradient(160deg, rgba(233,69,96,0.14), rgba(233,69,96,0.03));
        box-shadow: 0 8px 20px rgba(233,69,96,0.18);
    }
    .net-card .symbol {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 1.2em; font-weight: 700; color: #fff;
        letter-spacing: 0.03em;
        position: relative;
    }
    .net-card .name {
        color: rgba(255,255,255,0.4); font-size: 0.78em;
        margin-top: 3px; letter-spacing: 0.02em;
        position: relative;
    }"""

for path in files:
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old_block not in content:
        print(f"ERROR: block not found in {path}")
        continue
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"SUCCESS: {path} updated.")
