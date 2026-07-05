import io

path = "templates/oracle.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix gas price percent for zetachain (100%) and add gasLimit for plume/avax
old1 = '''                const gasPrice = currentNet === 'lamina1'
                    ? feeData.gasPrice
                    : feeData.gasPrice * 25n / 100n;
                tx = isUp
                    ? await btcContract.up({ gasPrice })
                    : await btcContract.down({ gasPrice });'''
new1 = '''                const isFullFee = ["lamina1", "zetachain"].includes(currentNet);
                const gasPrice = isFullFee ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;
                const overridesBtc = { gasPrice };
                if (["lamina1", "plume", "avax"].includes(currentNet)) overridesBtc.gasLimit = 150000;
                tx = isUp
                    ? await btcContract.up(overridesBtc)
                    : await btcContract.down(overridesBtc);'''

old2 = '''                const gasPriceMain = currentNet === 'lamina1'
                    ? feeData.gasPrice
                    : feeData.gasPrice * 25n / 100n;
                tx = await contract.predict(currentQuestionId, isUp, { gasPrice: gasPriceMain });'''
new2 = '''                const isFullFeeMain = ["lamina1", "zetachain"].includes(currentNet);
                const gasPriceMain = isFullFeeMain ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;
                const overridesMain = { gasPrice: gasPriceMain };
                if (["lamina1", "plume", "avax"].includes(currentNet)) overridesMain.gasLimit = 150000;
                tx = await contract.predict(currentQuestionId, isUp, overridesMain);'''

errors = []
if old1 not in content: errors.append("part1 (btc gas)")
if old2 not in content: errors.append("part2 (main gas)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: oracle.html fee logic fixed.")
