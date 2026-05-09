#!/usr/bin/env python3
"""Download Koren Torah Michigan-Claremont files used in common ELS tests."""

from __future__ import annotations

import urllib.request
from pathlib import Path


BASE_URL = "https://users.cecs.anu.edu.au/~bdm/dilugim/StatSci"
FILES = [
    "genesis.koren.gz",
    "exodus.koren.gz",
    "leviticus.koren.gz",
    "numbers.koren.gz",
    "deuteronomy.koren.gz",
]
OUT_DIR = Path("data/raw/koren")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        out_path = OUT_DIR / name
        with urllib.request.urlopen(f"{BASE_URL}/{name}") as response:
            out_path.write_bytes(response.read())
        print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
