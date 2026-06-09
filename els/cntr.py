"""Loader for the CNTR full-text Greek editions (KJTR, RP, WH, SR).

The editions live under data/raw/cntr as MES-format text files: one verse per
line, an eight-digit BBCCCVVV code, a space, then the verse text. This loader
was previously defined inside analyze_heptadic_counts and imported by its
siblings; it lives here so the path convention is stated once.
"""

from __future__ import annotations

import glob
from pathlib import Path

CNTR_ROOT = Path("data/raw/cntr")


def load_edition(siglum: str, root: Path = CNTR_ROOT) -> dict[str, str]:
    """Load a CNTR full-text edition (KJTR/RP/WH/SR) as code -> verse text."""
    for path in glob.glob(f"{root}/**/{siglum}.txt", recursive=True):
        out: dict[str, str] = {}
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if len(line) >= 8 and line[:8].isdigit():
                    out[line[:8]] = line[9:].rstrip("\n")
        return out
    return {}
