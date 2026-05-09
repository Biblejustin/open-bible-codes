#!/usr/bin/env python3
"""Download MorphGNT SBLGNT files into data/raw/morphgnt/sblgnt."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path


API_URL = "https://api.github.com/repos/morphgnt/sblgnt/contents?ref=master"
OUT_DIR = Path("data/raw/morphgnt/sblgnt")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(API_URL) as response:
        files = json.loads(response.read().decode("utf-8"))
    for item in files:
        name = item.get("name", "")
        if item.get("type") != "file" or not name.endswith("-morphgnt.txt"):
            continue
        out_path = OUT_DIR / name
        with urllib.request.urlopen(item["download_url"]) as response:
            out_path.write_bytes(response.read())
        print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
