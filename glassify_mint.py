import io

path = "templates/mint.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """    .net-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px; padding: 14px;
        cursor: pointer; transition: all 0.2s; text-align: left;
    }
    .net-card:hover { border-color: rgba(247,179,43,0.4); background: rgba(255,255,255,0.04); }
    .net-card.active { border-color: #f7b32b; background: rgba(247,179,43,0.07); }
    .net-card .symbol { font-size: 1.05em; font-weight: 600; color: #fff; }
    .net-card .name { color: #777; font-size: 0.78em; margin-top: 2px; }"""

new_block = """    .net-card {
        position: relative;
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px; padding: 14px 16px;
        cursor: pointer; transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
        text-align: left; overflow: hidden;
    }
    .net-card::before {
        content: "";
        position: absolute; inset: 0;
        background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.06), rgba(0,0,0,0) 60%);
        pointer-events: none;
    }
    .net-card:hover {
        border-color: rgba(247,179,43,0.45);
        background: linear-gradient(160deg, rgba(247,179,43,0.08), rgba(255,255,255,0.02));
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(247,179,43,0.12);
    }
    .net-card.active {
        border-color: #f7b32b;
        background: linear-gradient(160deg, rgba(247,179,43,0.14), rgba(247,179,43,0.03));
        box-shadow: 0 8px 20px rgba(247,179,43,0.18);
    }
    .net-card .symbol {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 1.15em; font-weight: 700; color: #fff;
        letter-spacing: 0.03em; position: relative;
    }
    .net-card .name {
        color: rgba(255,255,255,0.4); font-size: 0.76em;
        margin-top: 3px; position: relative;
    }"""

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: mint.html updated.")
