#!/usr/bin/env python3
"""Build Markdown and JSON indexes for generated reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from els.report_index import scan_reports, write_json_index, write_markdown_index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--out", default="reports/INDEX.md")
    parser.add_argument("--json-out", default="reports/index.json")
    parser.add_argument("--sample-limit", type=int, default=3)
    parser.add_argument("--db", default=None, help="Optional DuckDB report database for current CSV row counts.")
    parser.add_argument("--cache", default=None, help="Optional row-count cache path for medium CSV reports.")
    args = parser.parse_args()

    reports_dir = Path(args.reports_dir)
    entries = scan_reports(reports_dir, sample_limit=args.sample_limit, db_path=args.db, cache_path=args.cache)
    write_markdown_index(entries, args.out, reports_root=reports_dir)
    write_json_index(entries, args.json_out)
    print(args.out)
    print(args.json_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
