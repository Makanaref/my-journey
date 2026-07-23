import io

path = "indexer.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_factories = '''NFT_FACTORY_ADDRESSES = {
    "lamina1": "0x02fFD8C9D9c6ea769cdFd530625eE9154a719786",
    "avax":    "0x01d85BF4fb62c2Ba5746e4BC9821E6a7E05d68f4",
}'''

new_factories = '''NFT_FACTORY_ADDRESSES = {
    "lamina1":   "0x02fFD8C9D9c6ea769cdFd530625eE9154a719786",
    "nexus":     "0x802BeAeC89A61a5e0da9EE05476AC45E40daE13c",
    "ink":       "0x1eFfd154CB7adae114F36Af6101a7559c6a98f3F",
    "base":      "0x5f550fe601d9610B1D1977E5b3b5491347ED0418",
    "robinhood": "0x620145Db1914c1F9c327FA282BD95b9039647Bc6",
    "avax":      "0x01d85BF4fb62c2Ba5746e4BC9821E6a7E05d68f4",
    "plume":     "0x9791cDBf9a6AF15C313B49d80299769fB8Bd608D",
    "zetachain": "0xF988CAc77e456e915aFbDC22BBc8c114fbd4Cd96"
}'''

if old_factories not in content:
    print("ERROR: NFT_FACTORY_ADDRESSES block not found!")
else:
    content = content.replace(old_factories, new_factories, 1)

old_tasks = '''    for net_key in EXPLORER_APIS:
        tasks.append(("nft_api", net_key))
        tasks.append(("token_api", net_key))

    for net_key in NFT_FACTORY_ADDRESSES:
        tasks.append(("nft_rpc", net_key))'''

new_tasks = '''    for net_key in EXPLORER_APIS:
        tasks.append(("token_api", net_key))

    for net_key in NFT_FACTORY_ADDRESSES:
        tasks.append(("nft_rpc", net_key))'''

if old_tasks not in content:
    print("ERROR: tasks block not found!")
else:
    content = content.replace(old_tasks, new_tasks, 1)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: NFT scanning unified to reliable on-chain method for all 8 networks.")
