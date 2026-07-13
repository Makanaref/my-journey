import requests
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

NETWORK_LABELS = {
    "lamina1": "Lamina1", "nexus": "Nexus", "ink": "Ink", "base": "Base",
    "robinhood": "Robinhood", "avax": "Avalanche", "plume": "Plume", "zetachain": "ZetaChain"
}

EXPLORER_APIS = {
    "nexus":     "https://explorer.nexus.xyz/api/v2",
    "ink":       "https://explorer.inkonchain.com/api/v2",
    "base":      "https://base.blockscout.com/api/v2",
    "robinhood": "https://robinhoodchain.blockscout.com/api/v2",
}

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

NFT_FACTORY_ADDRESSES = {
    "lamina1": "0x02fFD8C9D9c6ea769cdFd530625eE9154a719786",
    "avax":    "0x01d85BF4fb62c2Ba5746e4BC9821E6a7E05d68f4",
}

NFT_FACTORY_ABI = [{"anonymous":False,"inputs":[{"indexed":True,"name":"collectionAddress","type":"address"},{"indexed":True,"name":"creator","type":"address"},{"indexed":False,"name":"name","type":"string"},{"indexed":False,"name":"symbol","type":"string"},{"indexed":False,"name":"maxSupply","type":"uint256"},{"indexed":False,"name":"mintPrice","type":"uint256"}],"name":"CollectionCreated","type":"event"}]
NFT_COLLECTION_ABI = [{"constant":True,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":True,"inputs":[],"name":"totalMinted","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":True,"inputs":[],"name":"metadataURI","outputs":[{"name":"","type":"string"}],"type":"function"}]


def rpc_call(url, method, params):
    try:
        res = requests.post(url, json={"jsonrpc":"2.0","id":1,"method":method,"params":params}, timeout=4)
        return res.json().get("result")
    except Exception:
        return None


def eth_call(rpc_url, to, data):
    return rpc_call(rpc_url, "eth_call", [{"to": to, "data": data}, "latest"])


def encode_address(addr):
    return "000000000000000000000000" + addr[2:].lower()


def decode_uint(hex_str):
    if not hex_str or hex_str == "0x":
        return 0
    return int(hex_str, 16)


def decode_string(hex_str):
    try:
        if not hex_str or len(hex_str) < 10:
            return ""
        b = bytes.fromhex(hex_str[2:])
        offset = int.from_bytes(b[0:32], 'big')
        length = int.from_bytes(b[offset:offset+32], 'big')
        return b[offset+32:offset+32+length].decode('utf-8', errors='ignore')
    except Exception:
        return ""


def get_gm_stats(rpc_url, contract_addr, account):
    sig = "0x" + "getStats(address)".encode().hex()
    from Crypto.Hash import keccak
    k = keccak.new(digest_bits=256)
    k.update(b"getStats(address)")
    selector = k.hexdigest()[:8]
    data = "0x" + selector + encode_address(account)
    result = rpc_call(rpc_url, "eth_call", [{"to": contract_addr, "data": data}, "latest"])
    if not result or result == "0x":
        return None
    b = bytes.fromhex(result[2:])
    streak = int.from_bytes(b[0:32], 'big')
    score = int.from_bytes(b[32:64], 'big')
    return {"streak": streak, "score": round(score / 100, 2)}


def get_flip_stats(rpc_url, contract_addr, account):
    from Crypto.Hash import keccak
    k = keccak.new(digest_bits=256)
    k.update(b"getStats(address)")
    selector = k.hexdigest()[:8]
    data = "0x" + selector + encode_address(account)
    result = rpc_call(rpc_url, "eth_call", [{"to": contract_addr, "data": data}, "latest"])
    if not result or result == "0x":
        return None
    b = bytes.fromhex(result[2:])
    best = int.from_bytes(b[32:64], 'big')
    wins = int.from_bytes(b[64:96], 'big')
    flips = int.from_bytes(b[96:128], 'big')
    if flips == 0:
        return None
    return {"best": best, "wins": wins, "total": flips}


def get_oracle_stats(rpc_url, contract_addr, account):
    from Crypto.Hash import keccak
    def call_fn(fn_sig):
        k = keccak.new(digest_bits=256)
        k.update(fn_sig.encode())
        selector = k.hexdigest()[:8]
        data = "0x" + selector + encode_address(account)
        result = rpc_call(rpc_url, "eth_call", [{"to": contract_addr, "data": data}, "latest"])
        return decode_uint(result) if result else 0
    correct = call_fn("correctPredictions(address)")
    total = call_fn("totalPredictions(address)")
    if total == 0:
        return None
    return {"correct": correct, "total": total}


def scan_nfts_via_explorer(net_key, account):
    results = []
    try:
        api = EXPLORER_APIS[net_key]
        res = requests.get(f"{api}/addresses/{account}/nft?type=ERC-721", timeout=5)
        if not res.ok:
            return results
        data = res.json()
        items = data if isinstance(data, list) else data.get("items", [])
        seen = set()
        for item in items:
            try:
                meta = item.get("metadata") or {}
                if isinstance(meta, str):
                    try:
                        meta = json.loads(meta)
                    except Exception:
                        meta = {}
                attrs = {a.get("trait_type"): a.get("value") for a in meta.get("attributes", []) if a.get("trait_type")}
                collection_addr = attrs.get("Collection Address") or (item.get("token") or {}).get("address") or ""
                if not collection_addr or collection_addr in seen:
                    continue
                seen.add(collection_addr)
                name = attrs.get("Collection Name") or (item.get("token") or {}).get("name") or item.get("name") or "Unknown"
                image = item.get("image_url") or meta.get("image") or ""
                results.append({
                    "network": net_key,
                    "network_label": NETWORK_LABELS[net_key],
                    "collection": collection_addr,
                    "name": name,
                    "image": image,
                    "is_creator": False
                })
            except Exception:
                pass
    except Exception as e:
        print(f"NFT explorer scan failed for {net_key}: {e}")
    return results


def scan_nfts_via_rpc(net_key, account):
    results = []
    try:
        from web3 import Web3
        factory_addr = NFT_FACTORY_ADDRESSES.get(net_key)
        if not factory_addr:
            return results
        w3 = Web3(Web3.HTTPProvider(RPC_URLS[net_key], request_kwargs={"timeout": 8}))
        factory = w3.eth.contract(address=Web3.to_checksum_address(factory_addr), abi=NFT_FACTORY_ABI)
        latest = w3.eth.block_number
        chunk = 2000
        max_blocks = 200000
        all_events = []
        to_block = latest
        while to_block > max(0, latest - max_blocks):
            from_block = max(0, to_block - chunk)
            try:
                events = factory.events.CollectionCreated().get_logs(from_block=from_block, to_block=to_block)
                all_events.extend(events)
            except Exception:
                pass
            to_block = from_block - 1
        for ev in all_events:
            try:
                collection_addr = ev["args"]["collectionAddress"]
                creator = ev["args"]["creator"]
                collection = w3.eth.contract(address=collection_addr, abi=NFT_COLLECTION_ABI)
                balance = collection.functions.balanceOf(Web3.to_checksum_address(account)).call()
                is_creator = creator.lower() == account.lower()
                if balance == 0 and not is_creator:
                    continue
                name = ev["args"]["name"]
                image = ""
                try:
                    uri = collection.functions.metadataURI().call()
                    with urllib.request.urlopen(uri, timeout=4) as resp:
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
            except Exception:
                pass
    except Exception as e:
        print(f"NFT RPC scan failed for {net_key}: {e}")
    return results


def scan_tokens_via_explorer(net_key, account):
    results = []
    try:
        api = EXPLORER_APIS[net_key]
        res = requests.get(f"{api}/addresses/{account}/token-balances", timeout=5)
        if not res.ok:
            return results
        data = res.json()
        items = data if isinstance(data, list) else data.get("items", [])
        for item in items:
            try:
                token = item.get("token") or item
                if token.get("type") != "ERC-20":
                    continue
                balance_raw = int(item.get("value") or "0")
                if balance_raw == 0:
                    continue
                decimals = int(token.get("decimals") or 18)
                results.append({
                    "network": net_key,
                    "network_label": NETWORK_LABELS[net_key],
                    "name": token.get("name") or "Unknown",
                    "symbol": token.get("symbol") or "?",
                    "balance": balance_raw / (10 ** decimals)
                })
            except Exception:
                pass
    except Exception as e:
        print(f"Token explorer scan failed for {net_key}: {e}")
    return results


def scan_ranks_for_network(net_key, account):
    result = {"network": net_key, "network_label": NETWORK_LABELS[net_key]}
    has_data = False
    rpc_url = RPC_URLS[net_key]

    if GM_ADDRESSES.get(net_key):
        try:
            stats = get_gm_stats(rpc_url, GM_ADDRESSES[net_key], account)
            if stats and (stats["streak"] > 0 or stats["score"] > 0):
                result["gm_streak"] = stats["streak"]
                result["gm_score"] = stats["score"]
                has_data = True
        except Exception:
            pass

    if FLIP_ADDRESSES.get(net_key):
        try:
            stats = get_flip_stats(rpc_url, FLIP_ADDRESSES[net_key], account)
            if stats:
                result["flip_best"] = stats["best"]
                result["flip_wins"] = stats["wins"]
                result["flip_total"] = stats["total"]
                has_data = True
        except Exception:
            pass

    if ORACLE_ADDRESSES.get(net_key):
        try:
            stats = get_oracle_stats(rpc_url, ORACLE_ADDRESSES[net_key], account)
            if stats:
                result["oracle_correct"] = stats["correct"]
                result["oracle_total"] = stats["total"]
                has_data = True
        except Exception:
            pass

    return result if has_data else None


def scan_all(account):
    nfts = []
    tokens = []
    ranks = []

    tasks = []

    for net_key in EXPLORER_APIS:
        tasks.append(("nft_api", net_key))
        tasks.append(("token_api", net_key))

    for net_key in NFT_FACTORY_ADDRESSES:
        tasks.append(("nft_rpc", net_key))

    for net_key in RPC_URLS:
        tasks.append(("rank", net_key))

    def run_task(task):
        kind, net_key = task
        if kind == "nft_api":
            return ("nft", scan_nfts_via_explorer(net_key, account))
        elif kind == "token_api":
            return ("token", scan_tokens_via_explorer(net_key, account))
        elif kind == "nft_rpc":
            return ("nft", scan_nfts_via_rpc(net_key, account))
        elif kind == "rank":
            return ("rank", scan_ranks_for_network(net_key, account))

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(run_task, t) for t in tasks]
        for future in as_completed(futures, timeout=15):
            try:
                kind, data = future.result()
                if kind == "nft":
                    nfts.extend(data)
                elif kind == "token":
                    tokens.extend(data)
                elif kind == "rank" and data:
                    ranks.append(data)
            except Exception:
                pass

    return {"nfts": nfts, "tokens": tokens, "ranks": ranks}