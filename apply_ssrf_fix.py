with open("indexer.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add imports needed for SSRF validation, right after existing imports
old_imports = '''import requests
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed'''

new_imports = '''import requests
import json
import urllib.request
import ipaddress
import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed'''

if old_imports not in content:
    raise SystemExit("ERROR: imports block not found, aborting.")
content = content.replace(old_imports, new_imports, 1)

# 2. Add the safe fetch helper function right after decode_string (before get_gm_stats)
old_decode_string_end = '''def decode_string(hex_str):
    try:
        if not hex_str or len(hex_str) < 10:
            return ""
        b = bytes.fromhex(hex_str[2:])
        offset = int.from_bytes(b[0:32], 'big')
        length = int.from_bytes(b[offset:offset+32], 'big')
        return b[offset+32:offset+32+length].decode('utf-8', errors='ignore')
    except Exception:
        return ""'''

new_decode_string_with_helper = '''def decode_string(hex_str):
    try:
        if not hex_str or len(hex_str) < 10:
            return ""
        b = bytes.fromhex(hex_str[2:])
        offset = int.from_bytes(b[0:32], 'big')
        length = int.from_bytes(b[offset:offset+32], 'big')
        return b[offset+32:offset+32+length].decode('utf-8', errors='ignore')
    except Exception:
        return ""


def _is_private_or_reserved(hostname):
    """Resolve hostname and check if it points to a private/reserved/loopback IP,
    to prevent SSRF via NFT metadata URIs pointing at internal infrastructure."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except Exception:
        return True  # can't resolve -> treat as unsafe, fail closed
    for info in infos:
        ip_str = info[4][0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            return True
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_multicast or ip.is_reserved or ip.is_unspecified):
            return True
    return False


def safe_fetch_metadata(uri, timeout=4, max_bytes=262144):
    """Safely fetch NFT metadata JSON from an arbitrary URI supplied by a
    (potentially malicious) smart contract. Blocks non-http(s) schemes and
    requests to private/internal network addresses (SSRF protection), and
    caps the response size to avoid abuse."""
    try:
        parsed = urlparse(uri)
        if parsed.scheme not in ("http", "https"):
            return None
        if not parsed.hostname:
            return None
        if _is_private_or_reserved(parsed.hostname):
            return None

        res = requests.get(uri, timeout=timeout, stream=True, allow_redirects=True)
        if not res.ok:
            return None

        # Re-check the final URL after redirects (in case of redirect-based SSRF)
        final_parsed = urlparse(res.url)
        if final_parsed.scheme not in ("http", "https"):
            return None
        if not final_parsed.hostname or _is_private_or_reserved(final_parsed.hostname):
            return None

        content_bytes = b""
        for chunk in res.iter_content(chunk_size=4096):
            content_bytes += chunk
            if len(content_bytes) > max_bytes:
                return None  # response too large, bail out

        return json.loads(content_bytes.decode("utf-8", errors="ignore"))
    except Exception:
        return None'''

if old_decode_string_end not in content:
    raise SystemExit("ERROR: decode_string block not found, aborting.")
content = content.replace(old_decode_string_end, new_decode_string_with_helper, 1)

# 3. Replace usage #1 (scan_nfts_via_explorer)
old_usage_1 = '''                    if result and result != "0x":
                        uri = decode_string(result)
                        if uri:
                            meta_res = requests.get(uri, timeout=4)
                            if meta_res.ok:
                                meta_json = meta_res.json()
                                image = meta_json.get("image", "")
                                name = meta_json.get("name", name)'''

new_usage_1 = '''                    if result and result != "0x":
                        uri = decode_string(result)
                        if uri:
                            meta_json = safe_fetch_metadata(uri)
                            if meta_json:
                                image = meta_json.get("image", "")
                                name = meta_json.get("name", name)'''

if old_usage_1 not in content:
    raise SystemExit("ERROR: usage_1 block (scan_nfts_via_explorer) not found, aborting.")
content = content.replace(old_usage_1, new_usage_1, 1)

# 4. Replace usage #2 (scan_nfts_via_rpc, primary metadataURI attempt)
old_usage_2 = '''                try:
                    uri = collection.functions.metadataURI().call()
                    if uri:
                        meta_res = requests.get(uri, timeout=4)
                        if meta_res.ok:
                            meta_json = meta_res.json()
                            image = meta_json.get("image", "")
                            name = meta_json.get("name", name)
                except Exception:'''

new_usage_2 = '''                try:
                    uri = collection.functions.metadataURI().call()
                    if uri:
                        meta_json = safe_fetch_metadata(uri)
                        if meta_json:
                            image = meta_json.get("image", "")
                            name = meta_json.get("name", name)
                except Exception:'''

if old_usage_2 not in content:
    raise SystemExit("ERROR: usage_2 block (scan_nfts_via_rpc primary) not found, aborting.")
content = content.replace(old_usage_2, new_usage_2, 1)

# 5. Replace usage #3 (scan_nfts_via_rpc, tokenURI fallback)
old_usage_3 = '''                        uri = c2.functions.tokenURI(1).call()
                        if uri:
                            meta_res = requests.get(uri, timeout=4)
                            if meta_res.ok:
                                meta_json = meta_res.json()
                                image = meta_json.get("image", "")
                                name = meta_json.get("name", name)'''

new_usage_3 = '''                        uri = c2.functions.tokenURI(1).call()
                        if uri:
                            meta_json = safe_fetch_metadata(uri)
                            if meta_json:
                                image = meta_json.get("image", "")
                                name = meta_json.get("name", name)'''

if old_usage_3 not in content:
    raise SystemExit("ERROR: usage_3 block (tokenURI fallback) not found, aborting.")
content = content.replace(old_usage_3, new_usage_3, 1)

with open("indexer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done. SSRF protections applied to indexer.py (3 fetch sites now use safe_fetch_metadata).")
