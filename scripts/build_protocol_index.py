#!/usr/bin/env python3
"""Build a deterministic Markdown index for protocol TOML files."""

from __future__ import annotations

import argparse
from pathlib import Path

from els.project_index import scan_protocols, write_protocol_index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocols-dir", default="protocols")
    parser.add_argument("--out", default="protocols/INDEX.md")
    args = parser.parse_args()

    protocols_dir = Path(args.protocols_dir)
    entries = scan_protocols(protocols_dir)
    write_protocol_index(entries, args.out, protocols_root=protocols_dir)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
