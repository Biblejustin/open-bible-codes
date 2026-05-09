#!/usr/bin/env python3
"""Download SBLGNT text files into data/raw/sblgnt/text."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path


API_URL = "https://api.github.com/repos/Faithlife/SBLGNT/contents/data/sblgnt/text?ref=master"
OUT_DIR = Path("data/raw/sblgnt/text")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(API_URL) as response:
        files = json.loads(response.read().decode("utf-8"))
    for item in files:
        if item.get("type") != "file" or not item.get("name", "").endswith(".txt"):
            continue
        out_path = OUT_DIR / item["name"]
        with urllib.request.urlopen(item["download_url"]) as response:
            out_path.write_bytes(response.read())
        print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
