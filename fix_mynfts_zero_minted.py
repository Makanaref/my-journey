import io

path = "templates/my_nfts.html"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old1 = '''    const COLLECTION_ABI = [
        "function name() public view returns (string)",
        "function symbol() public view returns (string)",
        "function balanceOf(address owner) public view returns (uint256)",
        "function tokenURI(uint256 tokenId) public view returns (string)"
    ];'''

new1 = '''    const COLLECTION_ABI = [
        "function name() public view returns (string)",
        "function symbol() public view returns (string)",
        "function balanceOf(address owner) public view returns (uint256)",
        "function tokenURI(uint256 tokenId) public view returns (string)",
        "function totalMinted() public view returns (uint256)"
    ];'''

old2 = '''                        let meta = { name: ev.args.name, image: "", description: "" };
                        try {
                            const uri = await collection.tokenURI(1);
                            const metaRes = await fetch(uri);
                            const metaJson = await metaRes.json();
                            meta = { name: metaJson.name || ev.args.name, image: metaJson.image || "", description: metaJson.description || "" };
                        } catch (e) {}'''

new2 = '''                        let meta = { name: ev.args.name, image: "", description: "" };
                        try {
                            const totalMinted = await collection.totalMinted();
                            if (Number(totalMinted) > 0) {
                                const uri = await collection.tokenURI(1);
                                const metaRes = await fetch(uri);
                                const metaJson = await metaRes.json();
                                meta = { name: metaJson.name || ev.args.name, image: metaJson.image || "", description: metaJson.description || "" };
                            }
                        } catch (e) {}'''

errors = []
if old1 not in content: errors.append("part1 (ABI)")
if old2 not in content: errors.append("part2 (meta fetch)")

if errors:
    print("ERROR: blocks not found: " + ", ".join(errors))
else:
    content = content.replace(old1, new1, 1)
    content = content.replace(old2, new2, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: totalMinted check added before fetching image.")
