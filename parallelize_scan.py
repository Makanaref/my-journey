import io

path = "indexer.py"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''def scan_all(account):
    nfts = []
    tokens = []
    ranks = []
    for net_key in RPC_URLS:
        nfts.extend(scan_nfts_for_network(net_key, account))
        tokens.extend(scan_tokens_for_network(net_key, account))
        rank = scan_ranks_for_network(net_key, account)
        if rank:
            ranks.append(rank)
    return {"nfts": nfts, "tokens": tokens, "ranks": ranks}'''

new_block = '''def _scan_one_network(net_key, account):
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

    return {"nfts": nfts, "tokens": tokens, "ranks": ranks}'''

if old_block not in content:
    print("ERROR: old_block not found!")
else:
    content = content.replace(old_block, new_block, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: scan_all is now parallelized across all networks.")
