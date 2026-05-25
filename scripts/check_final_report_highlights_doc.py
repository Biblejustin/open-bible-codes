#!/usr/bin/env python3
"""Validate generated final-report highlights markdown freshness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_final_report_highlights as builder


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_highlights_doc(args)
    if failures:
        for failure in failures:
            print(f"final-report highlights doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"final-report highlights doc ok: {args.markdown_out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--centered-summary", type=Path, default=builder.DEFAULT_CENTERED_SUMMARY)
    parser.add_argument("--claim-catalog", type=Path, default=builder.DEFAULT_CLAIM_CATALOG)
    parser.add_argument("--out", type=Path, default=builder.DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=builder.DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=builder.DEFAULT_MANIFEST)
    parser.add_argument("--limit", type=int, default=40)
    return parser


def validate_highlights_doc(args: argparse.Namespace | None = None) -> list[str]:
    args = args or build_parser().parse_args([])
    for path in (args.centered_summary, args.claim_catalog, args.markdown_out):
        if not path.exists():
            return [f"{path} is missing"]
    highlights = builder.build_highlights(
        builder.read_rows(args.centered_summary),
        limit=args.limit,
    )
    expected = builder.render_markdown(
        highlights,
        builder.read_rows(args.claim_catalog),
        args,
    )
    actual = args.markdown_out.read_text(encoding="utf-8")
    if actual != expected:
        return [
            f"{args.markdown_out} is stale; rerun python3 -m scripts.build_final_report_highlights"
        ]
    return []


if __name__ == "__main__":
    raise SystemExit(main())
