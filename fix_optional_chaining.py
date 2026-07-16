import io

replacements = {
    "templates/swap.html": [
        (
            "statusMsg.innerText = `⚠️ ${getNetworkByChainId(selectedChain)?.name || 'This network'} is not supported for swaps yet`;",
            "const _net = getNetworkByChainId(selectedChain);\n            statusMsg.innerText = `⚠️ ${(_net && _net.name) || 'This network'} is not supported for swaps yet`;"
        ),
        (
            "routeDisplay.textContent = data.toolDetails?.name || data.tool || apiUsed;",
            "routeDisplay.textContent = (data.toolDetails && data.toolDetails.name) || data.tool || apiUsed;"
        ),
        (
            "const duration = data.estimate?.executionDuration || data.executionDuration || 30;",
            "const duration = (data.estimate && data.estimate.executionDuration) || data.executionDuration || 30;"
        ),
        (
            "const fee = data.estimate?.fee || data.fee || {};",
            "const fee = (data.estimate && data.estimate.fee) || data.fee || {};"
        ),
        (
            "const gasCost = data.estimate?.gasCost || data.gasCost || 0;",
            "const gasCost = (data.estimate && data.estimate.gasCost) || data.gasCost || 0;"
        ),
        (
            "const protocolFee = data.estimate?.protocolFee || data.protocolFee || 0;",
            "const protocolFee = (data.estimate && data.estimate.protocolFee) || data.protocolFee || 0;"
        ),
    ],
    "templates/b20.html": [
        (
            "if (error.code === 'CALL_EXCEPTION' || error.message?.includes('execution reverted')) {",
            "if (error.code === 'CALL_EXCEPTION' || (error.message && error.message.includes('execution reverted'))) {"
        ),
        (
            "if (error.message?.includes('insufficient funds') ||\n                error.message?.includes('gas') ||\n                error.data?.includes('4b344b11')) { // این هگز مخصوص ارور گازه",
            "if ((error.message && error.message.includes('insufficient funds')) ||\n                (error.message && error.message.includes('gas')) ||\n                (error.data && error.data.includes('4b344b11'))) { // این هگز مخصوص ارور گازه"
        ),
        (
            "if (error.message?.includes('user rejected')) {",
            "if (error.message && error.message.includes('user rejected')) {"
        ),
        (
            "if (error.code === 'NETWORK_ERROR' || error.message?.includes('network')) {",
            "if (error.code === 'NETWORK_ERROR' || (error.message && error.message.includes('network'))) {"
        ),
        (
            'const currency = document.getElementById("deploy-currency")?.value.trim() || "USD";',
            'const _curEl = document.getElementById("deploy-currency");\n        const currency = (_curEl && _curEl.value.trim()) || "USD";'
        ),
        (
            '''const tokenAddress = receipt.logs.find(log =>
                log.address.toLowerCase().startsWith("0xb20")
            )?.address || "Check explorer";''',
            '''const _foundLog = receipt.logs.find(log =>
                log.address.toLowerCase().startsWith("0xb20")
            );
            const tokenAddress = (_foundLog && _foundLog.address) || "Check explorer";'''
        ),
    ],
}

for path, pairs in replacements.items():
    with io.open(path, "r", encoding="utf-8") as f:
        content = f.read()
    fixed_count = 0
    missing = []
    for old, new in pairs:
        if old in content:
            content = content.replace(old, new, 1)
            fixed_count += 1
        else:
            missing.append(old[:60])
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{path}: fixed {fixed_count}/{len(pairs)}")
    if missing:
        print(f"  MISSING: {missing}")
