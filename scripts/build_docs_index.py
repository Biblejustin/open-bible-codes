#!/usr/bin/env python3
"""Build a deterministic Markdown index for repository documentation."""

from __future__ import annotations

import argparse
from pathlib import Path

from els.project_index import scan_markdown_docs, write_docs_index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--out", default="docs/INDEX.md")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    entries = scan_markdown_docs(docs_dir)
    write_docs_index(entries, args.out, docs_root=docs_dir)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
