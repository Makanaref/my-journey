import io

files_and_replacements = [
    ("templates/games.html", "Games — Makan 🎮", "Games 🎮"),
    ("templates/index.html", "Home — Makan 🚀", "Home 🚀"),
]

for path, old, new in files_and_replacements:
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        print(f"ERROR: '{old}' not found in {path}")
    else:
        content = content.replace(old, new, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"SUCCESS: {path} updated.")
