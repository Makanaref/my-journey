import io

files = ["templates/gm.html", "templates/mint.html", "templates/flip.html"]

old_variants = [
    'if (currentNet === "lamina1") txOverrides.gasLimit = 150000;',
    'if (currentNet === "lamina1") overrides.gasLimit = 150000;',
    'if (currentNet === "lamina1") txOverrides.gasLimit = 2500000;',
    'if (currentNet === "lamina1" || currentNet === "robinhood") txOverrides.gasLimit = 150000;',
    'if (currentNet === "lamina1" || currentNet === "robinhood") overrides.gasLimit = 150000;',
    'if (currentNet === "lamina1" || currentNet === "robinhood") txOverrides.gasLimit = 2500000;',
]
new_variants = [
    'if (["lamina1", "plume", "avax"].includes(currentNet)) txOverrides.gasLimit = 150000;',
    'if (["lamina1", "plume", "avax"].includes(currentNet)) overrides.gasLimit = 150000;',
    'if (["lamina1", "plume", "avax"].includes(currentNet)) txOverrides.gasLimit = 2500000;',
    'if (["lamina1", "robinhood", "plume", "avax"].includes(currentNet)) txOverrides.gasLimit = 150000;',
    'if (["lamina1", "robinhood", "plume", "avax"].includes(currentNet)) overrides.gasLimit = 150000;',
    'if (["lamina1", "robinhood", "plume", "avax"].includes(currentNet)) txOverrides.gasLimit = 2500000;',
]

for path in files:
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()
    changed = False
    for old_v, new_v in zip(old_variants, new_variants):
        if old_v in content:
            content = content.replace(old_v, new_v)
            changed = True
    if changed:
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"SUCCESS: {path} gasLimit fixed.")
    else:
        print(f"WARNING: no match found in {path}")
