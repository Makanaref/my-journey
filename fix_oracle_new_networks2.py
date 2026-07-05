import io

path = "templates/oracle.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = """                const gasPrice = currentNet === 'lamina1' 
                    ? feeData.gasPrice
                    : feeData.gasPrice * 25n / 100n;
                tx = isUp
                    ? await btcContract.up({ gasPrice })
                    : await btcContract.down({ gasPrice });"""

new1 = """                const isFullFee = ["lamina1", "zetachain"].includes(currentNet);
                const gasPrice = isFullFee ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;
                const overridesBtc = { gasPrice };
                if (["lamina1", "plume", "avax"].includes(currentNet)) overridesBtc.gasLimit = 150000;
                tx = isUp
                    ? await btcContract.up(overridesBtc)
                    : await btcContract.down(overridesBtc);"""

if old1 not in content:
    print("ERROR: part1 still not found!")
else:
    content = content.replace(old1, new1, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS part1: btc gas fixed.")
