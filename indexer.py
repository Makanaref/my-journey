from web3 import Web3
import json

RPC_URLS = {
    "lamina1":   "https://subnets.avax.network/lamina1/mainnet/rpc",
    "nexus":     "https://mainnet.rpc.nexus.xyz",
    "ink":       "https://rpc-gel.inkonchain.com",
    "base":      "https://mainnet.base.org",
    "robinhood": "https://rpc.mainnet.chain.robinhood.com",
    "avax":      "https://api.avax.network/ext/bc/C/rpc",
    "plume":     "https://rpc.plume.org",
    "zetachain": "https://zetachain-evm.blockpi.network/v1/rpc/public"
}

NETWORK_LABELS = {
    "lamina1": "Lamina1", "nexus": "Nexus", "ink": "Ink", "base": "Base",
    "robinhood": "Robinhood", "avax": "Avalanche", "plume": "Plume", "zetachain": "ZetaChain"
}

NFT_FACTORY_ADDRESSES = {
    "lamina1":   "0x02fFD8C9D9c6ea769cdFd530625eE9154a719786",
    "nexus":     "0x802BeAeC89A61a5e0da9EE05476AC45E40daE13c",
    "ink":       "0x1eFfd154CB7adae114F36Af6101a7559c6a98f3F",
    "base":      "0x5f550fe601d9610B1D1977E5b3b5491347ED0418",
    "robinhood": "0x620145Db1914c1F9c327FA282BD95b9039647Bc6",
    "avax":      "0x01d85BF4fb62c2Ba5746e4BC9821E6a7E05d68f4",
    "plume":     "0x9791cDBf9a6AF15C313B49d80299769fB8Bd608D",
    "zetachain": "0xF988CAc77e456e915aFbDC22BBc8c114fbd4Cd96"
}

TOKEN_FACTORY_ADDRESSES = {
    "lamina1":   "0x4d860020dc84f9AA1e24EF55f44859bc8CF55a8B",
    "nexus":     "0x63f76204e323Be28E1e89dCedf6E3717deF1C73F",
    "ink":       "0x472057828170D4Ac2CEa6B07D30A9b33B7d714d1",
    "base":      "0xFae8Fb8327A908120Ec2C46Cfc985CCF926821AA",
    "robinhood": "0x8D9bEa1253501Bb5657e9Bb0B5f39807bAE7C47b",
    "avax":      "0x5ecDA25Bd340b8684F8A97518F7f9892eC5712CB",
    "plume":     "0xf74fcdFc71a1B7d493a263E25766223004Bf20f7",
    "zetachain": "0x2ACc1E37Ce6C219c9Fc4Cb5b74c9539fA202471a"
}

GM_ADDRESSES = {
    "lamina1":   "0x91A68410C13866d1c4262C012680A623B79BeF20",
    "nexus":     "0x91A68410C13866d1c4262C012680A623B79BeF20",
    "ink":       "0xc5B1Bb3e6CE937F64440895a6b976455F64dbaAE",
    "base":      "0x0d246A70E2c9ddCDacF690E854E9a528aaE9c3f6",
    "robinhood": "0xEC76D7a9801Fd7De132b299a36B6E0125802430B",
    "avax":      "0x4DF798fD9F5Ff9109e6D42B67D3eE86FE09D3bf1",
    "plume":     "0xB72b9D6BF3a0d20a5A3152bcDD627A67eaDad56C",
    "zetachain": "0xdA8F4Da59a24b4F5ab1F1f2bd6D000F069F54080"
}

FLIP_ADDRESSES = {
    "lamina1":   "0x61EeEaf07149d2F42d6eB66D80C8C13Ef9d1ecCD",
    "nexus":     "0x4d860020dc84f9AA1e24EF55f44859bc8CF55a8B",
    "ink":       "0xa0DD2BF6509FA667df2CC409017841871132DEE7",
    "base":      "0xc9cBB32684C961dcEEd0f2f3e94e5cD4E6339308",
    "robinhood": "0x033947CB876A2A5175d6EBe3058c9258e0c2231A",
    "avax":      "0xCbF9e3DD39edb8E39328135b1131d7c70956eF6b",
    "plume":     "0x103e0F501530DaF1b99F66843CF86d516FfD3FB0",
    "zetachain": "0x01447Fa5e71ae03449f5F7ae67D9Bf047A9d6C4F"
}

ORACLE_ADDRESSES = {
    "lamina1":   "0xcf2B368dA4D785C45C4Cf72bAeB8ef4f52600B5D",
    "nexus":     "0xcf2B368dA4D785C45C4Cf72bAeB8ef4f52600B5D",
    "ink":       "0x0eea7AbDdeDD3Ae52B37Db2e041CC5446D40b5B1",
    "avax":      "0xD00C4A6854da53E321c3FEca1c10E5F3F59a0d31",
    "plume":     "0xe8E2F8133d40a20eA030A44f7b8A5eee1519Dc2e",
    "zetachain": "0x5A80759a9Ad738c75b3d0aB5335Ef0357231526a"
}

NFT_FACTORY_ABI = json.loads('''[
    {"anonymous": false, "inputs": [
        {"indexed": true, "name": "collectionAddress", "type": "address"},
        {"indexed": true, "name": "creator", "type": "address"},
        {"indexed": false, "name": "name", "type": "string"},
        {"indexed": false, "name": "symbol", "type": "string"},
        {"indexed": false, "name": "maxSupply", "type": "uint256"},
        {"indexed": false, "name": "mintPrice", "type": "uint256"}
    ], "name": "CollectionCreated", "type": "event"}
]''')

NFT_COLLECTION_ABI = json.loads('''[
    {"constant": true, "inputs": [{"name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [], "name": "totalMinted", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [], "name": "metadataURI", "outputs": [{"name": "", "type": "string"}], "type": "function"}
]''')

TOKEN_FACTORY_ABI = json.loads('''[
    {"anonymous": false, "inputs": [
        {"indexed": true, "name": "tokenAddress", "type": "address"},
        {"indexed": true, "name": "creator", "type": "address"},
        {"indexed": false, "name": "name", "type": "string"},
        {"indexed": false, "name": "symbol", "type": "string"},
        {"indexed": false, "name": "initialSupply", "type": "uint256"}
    ], "name": "TokenCreated", "type": "event"}
]''')

TOKEN_ABI = json.loads('''[
    {"constant": true, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": true, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "type": "function"}
]''')

GM_ABI = json.loads('''[
    {"constant": true, "inputs": [{"name": "user", "type": "address"}], "name": "getStats",
     "outputs": [{"name": "streak", "type": "uint256"}, {"name": "totalScoreX100", "type": "uint256"}, {"name": "lastGmDay", "type": "uint256"}],
     "type": "function"}
]''')

FLIP_ABI = json.loads('''[
    {"constant": true, "inputs": [{"name": "user", "type": "address"}], "name": "getStats",
     "outputs": [{"name": "currentStreak", "type": "uint256"}, {"name": "bestStreak", "type": "uint256"}, {"name": "totalWins", "type": "uint256"}, {"name": "totalFlips", "type": "uint256"}],
     "type": "function"}
]''')

ORACLE_ABI = json.loads('''[
    {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "correctPredictions", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "totalPredictions", "outputs": [{"name": "", "type": "uint256"}], "type": "function"}
]''')


def get_w3(net_key):
    return Web3(Web3.HTTPProvider(RPC_URLS[net_key], request_kwargs={"timeout": 12}))


def scan_nfts_for_network(net_key, account):
    results = []
    try:
        w3 = get_w3(net_key)
        factory_addr = NFT_FACTORY_ADDRESSES.get(net_key)
        if not factory_addr:
            return results
        factory = w3.eth.contract(address=Web3.to_checksum_address(factory_addr), abi=NFT_FACTORY_ABI)
        events = factory.events.CollectionCreated().get_logs(from_block=0, to_block="latest")
        for ev in events:
            collection_addr = ev["args"]["collectionAddress"]
            creator = ev["args"]["creator"]
            collection = w3.eth.contract(address=collection_addr, abi=NFT_COLLECTION_ABI)
            try:
                balance = collection.functions.balanceOf(Web3.to_checksum_address(account)).call()
            except Exception:
                balance = 0
            is_creator = creator.lower() == account.lower()
            if balance == 0 and not is_creator:
                continue

            name = ev["args"]["name"]
            image = ""
            try:
                total_minted = collection.functions.totalMinted().call()
                if total_minted > 0:
                    uri = collection.functions.metadataURI().call()
                    import urllib.request
                    with urllib.request.urlopen(uri, timeout=8) as resp:
                        meta = json.loads(resp.read().decode())
                        name = meta.get("name", name)
                        image = meta.get("image", "")
            except Exception:
                pass

            results.append({
                "network": net_key,
                "network_label": NETWORK_LABELS[net_key],
                "collection": collection_addr,
                "name": name,
                "image": image,
                "is_creator": is_creator
            })
    except Exception as e:
        print(f"NFT scan failed for {net_key}: {e}")
    return results


def scan_tokens_for_network(net_key, account):
    results = []
    try:
        w3 = get_w3(net_key)
        factory_addr = TOKEN_FACTORY_ADDRESSES.get(net_key)
        if not factory_addr:
            return results
        factory = w3.eth.contract(address=Web3.to_checksum_address(factory_addr), abi=TOKEN_FACTORY_ABI)
        events = factory.events.TokenCreated().get_logs(from_block=0, to_block="latest")
        for ev in events:
            token_addr = ev["args"]["tokenAddress"]
            token = w3.eth.contract(address=token_addr, abi=TOKEN_ABI)
            try:
                balance = token.functions.balanceOf(Web3.to_checksum_address(account)).call()
            except Exception:
                balance = 0
            if balance == 0:
                continue
            name = token.functions.name().call()
            symbol = token.functions.symbol().call()
            results.append({
                "network": net_key,
                "network_label": NETWORK_LABELS[net_key],
                "token": token_addr,
                "name": name,
                "symbol": symbol,
                "balance": balance / 1e18
            })
    except Exception as e:
        print(f"Token scan failed for {net_key}: {e}")
    return results


def scan_ranks_for_network(net_key, account):
    result = {"network": net_key, "network_label": NETWORK_LABELS[net_key]}
    has_data = False
    try:
        w3 = get_w3(net_key)
        acc = Web3.to_checksum_address(account)

        if GM_ADDRESSES.get(net_key):
            try:
                gm = w3.eth.contract(address=Web3.to_checksum_address(GM_ADDRESSES[net_key]), abi=GM_ABI)
                streak, score, _ = gm.functions.getStats(acc).call()
                if streak > 0 or score > 0:
                    result["gm_streak"] = streak
                    result["gm_score"] = round(score / 100, 2)
                    has_data = True
            except Exception:
                pass

        if FLIP_ADDRESSES.get(net_key):
            try:
                flip = w3.eth.contract(address=Web3.to_checksum_address(FLIP_ADDRESSES[net_key]), abi=FLIP_ABI)
                current, best, wins, flips = flip.functions.getStats(acc).call()
                if flips > 0:
                    result["flip_best"] = best
                    result["flip_wins"] = wins
                    result["flip_total"] = flips
                    has_data = True
            except Exception:
                pass

        if ORACLE_ADDRESSES.get(net_key):
            try:
                oracle = w3.eth.contract(address=Web3.to_checksum_address(ORACLE_ADDRESSES[net_key]), abi=ORACLE_ABI)
                correct = oracle.functions.correctPredictions(acc).call()
                total = oracle.functions.totalPredictions(acc).call()
                if total > 0:
                    result["oracle_correct"] = correct
                    result["oracle_total"] = total
                    has_data = True
            except Exception:
                pass
    except Exception as e:
        print(f"Rank scan failed for {net_key}: {e}")

    return result if has_data else None


def _scan_one_network(net_key, account):
    nfts = scan_nfts_for_network(net_key, account)
    tokens = scan_tokens_for_network(net_key, account)
    rank = scan_ranks_for_network(net_key, account)
    return nfts, tokens, rank


def scan_all(account):
    from concurrent.futures import ThreadPoolExecutor, as_completed

    nfts = []
    tokens = []
    ranks = []

    with ThreadPoolExecutor(max_workers=len(RPC_URLS)) as executor:
        futures = {executor.submit(_scan_one_network, net_key, account): net_key for net_key in RPC_URLS}
        for future in as_completed(futures):
            try:
                net_nfts, net_tokens, net_rank = future.result()
                nfts.extend(net_nfts)
                tokens.extend(net_tokens)
                if net_rank:
                    ranks.append(net_rank)
            except Exception as e:
                print(f"Scan failed for {futures[future]}: {e}")

    return {"nfts": nfts, "tokens": tokens, "ranks": ranks}
