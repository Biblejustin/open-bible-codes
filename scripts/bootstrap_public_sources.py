#!/usr/bin/env python3
"""Download public study sources and print corpus stats."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DOWNLOADS = [
    ("MT OSHB WLC", ["-m", "scripts.download_oshb_wlc"], ["data/raw/oshb/wlc/Gen.xml"]),
    ("MT UXLC", ["-m", "scripts.download_uxlc"], ["data/raw/uxlc/books/Genesis.xml"]),
    ("MT MAM", ["-m", "scripts.download_mam"], ["data/raw/mam/html/A1-Genesis.html"]),
    ("eBible Hebrew WLC", ["-m", "scripts.download_ebible_hebwlc"], ["data/processed/ebible/hebwlc.csv"]),
    ("UHB Hebrew", ["-m", "scripts.download_uhb"], ["data/processed/unfoldingword/hbo_uhb.csv"]),
    ("Critical SBLGNT", ["-m", "scripts.download_sblgnt"], ["data/raw/sblgnt/text/Matt.txt"]),
    (
        "LXX GRCLXX",
        ["-m", "scripts.download_ebible_grclxx", "--skip-download"],
        ["data/processed/ebible/grclxx.csv"],
    ),
    (
        "TR GRCTR",
        ["-m", "scripts.download_ebible_grctr", "--skip-download"],
        ["data/processed/ebible/grctr.csv"],
    ),
    (
        "Byzantine GRCMT",
        ["-m", "scripts.download_ebible_grcmt", "--skip-download"],
        ["data/processed/ebible/grcmt.csv"],
    ),
    (
        "Text-Critical GRCTCGNT",
        ["-m", "scripts.download_ebible_grctcgnt", "--skip-download"],
        ["data/processed/ebible/grctcgnt.csv"],
    ),
    (
        "English KJV",
        ["-m", "scripts.download_ebible_engkjv", "--skip-download"],
        ["data/processed/ebible/eng-kjv2006.csv"],
    ),
    (
        "English KJV + Apocrypha",
        ["-m", "scripts.download_ebible_engkjv_apocrypha", "--skip-download"],
        ["data/processed/ebible/eng-kjv.csv"],
    ),
]

STATS = [
    ("MT stats", ["-m", "els", "stats", "--config", "configs/example_oshb_wlc.toml"]),
    ("UXLC stats", ["-m", "els", "stats", "--config", "configs/example_uxlc.toml"]),
    ("MAM stats", ["-m", "els", "stats", "--config", "configs/example_mam.toml"]),
    ("eBible Hebrew WLC stats", ["-m", "els", "stats", "--config", "configs/example_ebible_hebwlc.toml"]),
    ("UHB stats", ["-m", "els", "stats", "--config", "configs/example_uhb.toml"]),
    ("LXX stats", ["-m", "els", "stats", "--config", "configs/example_ebible_grclxx.toml"]),
    ("TR stats", ["-m", "els", "stats", "--config", "configs/example_ebible_grctr.toml"]),
    ("GRCMT stats", ["-m", "els", "stats", "--config", "configs/example_ebible_grcmt.toml"]),
    ("GRCTCGNT stats", ["-m", "els", "stats", "--config", "configs/example_ebible_grctcgnt.toml"]),
    ("SBLGNT stats", ["-m", "els", "stats", "--config", "configs/example_sblgnt.toml"]),
    ("KJV stats", ["-m", "els", "stats", "--config", "configs/example_ebible_engkjv.toml"]),
    (
        "KJV + Apocrypha stats",
        ["-m", "els", "stats", "--config", "configs/example_ebible_engkjv_apocrypha.toml"],
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--no-stats", action="store_true")
    args = parser.parse_args()

    for label, command, outputs in DOWNLOADS:
        print(f"== {label} ==", flush=True)
        if not args.refresh and outputs_exist(outputs):
            print("cached", flush=True)
            continue
        subprocess.run([sys.executable, *command], cwd=ROOT, check=True)

    if not args.no_stats:
        for label, command in STATS:
            print(f"== {label} ==", flush=True)
            subprocess.run([sys.executable, *command], cwd=ROOT, check=True)
    return 0


def outputs_exist(outputs: list[str]) -> bool:
    return all((ROOT / output).exists() for output in outputs)


if __name__ == "__main__":
    raise SystemExit(main())
