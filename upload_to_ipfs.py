#!/usr/bin/env python3
"""
Upload NFT collection (images/ + metadata/) to local IPFS
and replace <IMAGES_CID> placeholder in JSON files with the real CID.

Expected structure:
    <PROJECT_DIR>/
        images/
            1.png ... 500.png
        metadata/
            1.json ... 500.json   (each has "image": "ipfs://<IMAGES_CID>/N.png")

Run:
    python upload_to_ipfs.py
"""

import subprocess
import json
import os
import re
import sys

# ---- config ----
IPFS_BIN = r"C:\Users\Donk\kubo\ipfs.exe"
PROJECT_DIR = r"C:\Users\Donk\my-journey\nft_uploads\sgm_collection"
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
METADATA_DIR = os.path.join(PROJECT_DIR, "metadata")
PLACEHOLDER = "<IMAGES_CID>"
NUM_ITEMS = 500
# -----------------


def run_ipfs_add(target_dir: str) -> str:
    """Add target_dir to IPFS and return the root folder CID."""
    if not os.path.isdir(target_dir):
        print(f"Error: folder not found: {target_dir}")
        sys.exit(1)

    cmd = [IPFS_BIN, "add", "-r", "--cid-version", "1", target_dir]
    print(f"\n>>> Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running ipfs add:")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)

    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    last_line = lines[-1]
    match = re.match(r"added (\S+) (.+)", last_line)
    if not match:
        print("Could not extract CID from ipfs output.")
        sys.exit(1)

    cid = match.group(1)
    folder_name = match.group(2).strip()

    expected_name = os.path.basename(target_dir.rstrip("\\/"))
    if folder_name != expected_name:
        for l in lines:
            m = re.match(r"added (\S+) (.+)", l)
            if m and m.group(2).strip() == expected_name:
                cid = m.group(1)
                break

    return cid


def update_json_files(images_cid: str):
    print(f"\n>>> Replacing {PLACEHOLDER} with real CID: {images_cid}\n")
    updated = 0
    missing = []

    for i in range(1, NUM_ITEMS + 1):
        json_path = os.path.join(METADATA_DIR, f"{i}.json")
        if not os.path.isfile(json_path):
            missing.append(json_path)
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read()

        if PLACEHOLDER not in content:
            try:
                data = json.loads(content)
                if "image" in data and images_cid in data["image"]:
                    continue
            except json.JSONDecodeError:
                pass

        new_content = content.replace(PLACEHOLDER, images_cid)

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        updated += 1

    print(f"Updated: {updated} files")
    if missing:
        print(f"Warning: {len(missing)} files missing, e.g.: {missing[:5]}")


def main():
    print("=" * 60)
    print("Step 1: Upload images folder to IPFS")
    print("=" * 60)
    images_cid = run_ipfs_add(IMAGES_DIR)
    print(f"\nImages CID: {images_cid}")
    print(f"  Example: ipfs://{images_cid}/1.png")

    print("\n" + "=" * 60)
    print("Step 2: Replace CID placeholder in JSON files")
    print("=" * 60)
    update_json_files(images_cid)

    print("\n" + "=" * 60)
    print("Step 3: Upload metadata folder to IPFS")
    print("=" * 60)
    metadata_cid = run_ipfs_add(METADATA_DIR)
    print(f"\nMetadata CID: {metadata_cid}")

    print("\n" + "=" * 60)
    print("Final result")
    print("=" * 60)
    print(f"Images CID:   {images_cid}")
    print(f"Metadata CID: {metadata_cid}")
    print(f"\nBase URI for contract (if using {{baseURI}}{{tokenId}}.json pattern):")
    print(f"  ipfs://{metadata_cid}/")
    print(f"\nExample tokenURI for token #1:")
    print(f"  ipfs://{metadata_cid}/1.json")
    print(f"\nCheck via local gateway:")
    print(f"  http://127.0.0.1:8081/ipfs/{metadata_cid}/1.json")


if __name__ == "__main__":
    main()
