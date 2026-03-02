"""
scripts/download_data.py
Downloads the American Gut Project fixed dataset from Zenodo mirror.
Source: McDonald et al. 2018, mSystems. DOI: 10.1128/mSystems.00031-18
Original data: ftp://ftp.microbio.me/AmericanGut/ag-2017-12-04
"""

import urllib.request
import os

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# These are the exact same files from ag-2017-12-04, mirrored on Zenodo
ZENODO_BASE = "https://zenodo.org/record/6652711/files"

files = {
    "otu_table.biom": f"{ZENODO_BASE}/otu_table__BODY_HABITAT_UBERON_feces_json.biom",
    "metadata.txt":   f"{ZENODO_BASE}/metadata__BODY_HABITAT_UBERON_feces__.txt",
    "ag.genus.rds":   f"{ZENODO_BASE}/ag.genus.rds"
}

for filename, url in files.items():
    out_path = os.path.join(RAW_DIR, filename)
    if os.path.exists(out_path):
        print(f"  Already exists: {out_path}")
        continue
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, out_path)
    size_mb = os.path.getsize(out_path) / 1e6
    print(f"  Saved to {out_path} ({size_mb:.1f} MB)")

print("\nDone.")