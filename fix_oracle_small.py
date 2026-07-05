import io, re

path = "templates/oracle.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Use regex to be whitespace-tolerant
pattern1 = re.compile(
    r"const gasPrice = currentNet === 'lamina1'\s*\n\s*\? feeData\.gasPrice\s*\n\s*: feeData\.gasPrice \* 25n / 100n;\s*\n\s*tx = isUp\s*\n\s*\? await btcContract\.up\(\{ gasPrice \}\)\s*\n\s*: await btcContract\.down\(\{ gasPrice \}\);"
)

replacement1 = '''const isFullFee = ["lamina1", "zetachain"].includes(currentNet);
                const gasPrice = isFullFee ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;
                const overridesBtc = { gasPrice };
                if (["lamina1", "plume", "avax"].includes(currentNet)) overridesBtc.gasLimit = 150000;
                tx = isUp
                    ? await btcContract.up(overridesBtc)
                    : await btcContract.down(overridesBtc);'''

new_content, count1 = pattern1.subn(replacement1, content, count=1)

if count1 == 0:
    print("ERROR: pattern1 (regex) still not found!")
else:
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS: part1 fixed using regex.")
