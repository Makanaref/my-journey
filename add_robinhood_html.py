import io

path = "templates/gm.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """          <div class="net-card" id="net-base" onclick="switchNetwork('base')">
    <div class="symbol">BASE</div>
    <div class="name">Base</div>
</div>
        </div>
    </div>"""

new_block = """          <div class="net-card" id="net-base" onclick="switchNetwork('base')">
    <div class="symbol">BASE</div>
    <div class="name">Base</div>
</div>
          <div class="net-card" id="net-robinhood" onclick="switchNetwork('robinhood')">
    <div class="symbol">HOOD</div>
    <div class="name">Robinhood</div>
</div>
        </div>
    </div>"""

if old_block not in content:
    print("ERROR html: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Robinhood card added to HTML.")
