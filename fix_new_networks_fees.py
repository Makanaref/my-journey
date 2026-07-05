import io

files = ["templates/gm.html", "templates/mint.html", "templates/flip.html"]

for path in files:
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False

    # Fix 1: zetachain should use 100% (not 25%)
    old_gas = "avax: 25, plume: 25, zetachain: 25"
    new_gas = "avax: 25, plume: 25, zetachain: 100"
    if old_gas in content:
        content = content.replace(old_gas, new_gas)
        changed = True

    # Fix 2: add gasLimit override for plume and avax (alongside lamina1/robinhood)
    old_gaslimit_variants = [
        'if (currentNet === "lamina1" || currentNet === "robinhood") txOverrides.gasLimit = 150000;',
        'if (currentNet === "lamina1" || currentNet === "robinhood") overrides.gasLimit = 150000;',
        'if (currentNet === "lamina1" || currentNet === "robinhood") txOverrides.gasLimit = 2500000;',
    ]
    new_gaslimit_variants = [
        'if (["lamina1", "robinhood", "plume", "avax"].includes(currentNet)) txOverrides.gasLimit = 150000;',
        'if (["lamina1", "robinhood", "plume", "avax"].includes(currentNet)) overrides.gasLimit = 150000;',
        'if (["lamina1", "robinhood", "plume", "avax"].includes(currentNet)) txOverrides.gasLimit = 2500000;',
    ]
    for old_v, new_v in zip(old_gaslimit_variants, new_gaslimit_variants):
        if old_v in content:
            content = content.replace(old_v, new_v)
            changed = True

    if changed:
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"SUCCESS: {path} fee logic fixed.")
    else:
        print(f"WARNING: no matching patterns found in {path} (check manually).")
