#!/usr/bin/env python3
"""Download OSHB WLC XML files into data/raw/oshb/wlc."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path


API_URL = "https://api.github.com/repos/openscriptures/morphhb/contents/wlc?ref=master"
OUT_DIR = Path("data/raw/oshb/wlc")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = load_api_listing()
    for item in files:
        if item.get("type") != "file" or not item.get("name", "").endswith(".xml"):
            continue
        out_path = OUT_DIR / item["name"]
        with urllib.request.urlopen(item["download_url"]) as response:
            out_path.write_bytes(response.read())
        print(out_path)
    return 0


def load_api_listing() -> list[dict[str, object]]:
    with urllib.request.urlopen(API_URL) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("OSHB WLC GitHub API listing JSON root must be a list")
    files: list[dict[str, object]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise SystemExit(f"OSHB WLC GitHub API listing item {index} must be an object")
        files.append(item)
    return files


if __name__ == "__main__":
    raise SystemExit(main())
