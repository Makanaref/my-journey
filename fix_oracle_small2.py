import io, re

path = "templates/oracle.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

pattern2 = re.compile(
    r"const gasPriceMain = currentNet === 'lamina1'\s*\n\s*\? feeData\.gasPrice\s*\n\s*: feeData\.gasPrice \* 25n / 100n;\s*\n\s*tx = await contract\.predict\(currentQuestionId, isUp, \{ gasPrice: gasPriceMain \}\);"
)

replacement2 = '''const isFullFeeMain = ["lamina1", "zetachain"].includes(currentNet);
                const gasPriceMain = isFullFeeMain ? feeData.gasPrice : feeData.gasPrice * 25n / 100n;
                const overridesMain = { gasPrice: gasPriceMain };
                if (["lamina1", "plume", "avax"].includes(currentNet)) overridesMain.gasLimit = 150000;
                tx = await contract.predict(currentQuestionId, isUp, overridesMain);'''

new_content, count2 = pattern2.subn(replacement2, content, count=1)

if count2 == 0:
    print("ERROR: pattern2 (regex) still not found!")
else:
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS: part2 fixed using regex.")
