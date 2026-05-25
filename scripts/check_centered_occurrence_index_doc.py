#!/usr/bin/env python3
"""Validate generated centered-occurrence index markdown freshness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import build_centered_occurrence_index as builder


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_centered_occurrence_index_doc(args)
    if failures:
        for failure in failures:
            print(f"centered-occurrence index doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"centered-occurrence index doc ok: {args.markdown_out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all-codes-review", type=Path, default=builder.DEFAULT_ALL_CODES_REVIEW)
    parser.add_argument("--all-codes-selected", type=Path, default=builder.DEFAULT_ALL_CODES_SELECTED)
    parser.add_argument("--all-codes-context", type=Path, default=builder.DEFAULT_ALL_CODES_CONTEXT)
    parser.add_argument("--strong-queue", type=Path, default=builder.DEFAULT_STRONG_QUEUE)
    parser.add_argument("--strong-bundle", type=Path, default=builder.DEFAULT_STRONG_BUNDLE)
    parser.add_argument("--original-findings", type=Path, default=builder.DEFAULT_ORIGINAL_FINDINGS)
    parser.add_argument("--gog-source-review", type=Path, default=builder.DEFAULT_GOG_SOURCE_REVIEW)
    parser.add_argument("--gog-control-review", type=Path, default=builder.DEFAULT_GOG_CONTROL_REVIEW)
    parser.add_argument(
        "--apocrypha-bridge-context",
        type=Path,
        default=builder.DEFAULT_APOCRYPHA_BRIDGE_CONTEXT,
    )
    parser.add_argument(
        "--kjv-apocrypha-bridge-context",
        type=Path,
        default=builder.DEFAULT_KJV_APOCRYPHA_BRIDGE_CONTEXT,
    )
    parser.add_argument("--out", type=Path, default=builder.DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=builder.DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=builder.DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=builder.DEFAULT_MANIFEST)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def validate_centered_occurrence_index_doc(
    args: argparse.Namespace | None = None,
) -> list[str]:
    args = args or build_parser().parse_args([])
    inputs = [
        args.all_codes_review,
        args.all_codes_selected,
        args.all_codes_context,
        args.strong_queue,
        args.strong_bundle,
        args.original_findings,
        args.gog_source_review,
        args.gog_control_review,
        args.apocrypha_bridge_context,
        args.kjv_apocrypha_bridge_context,
        args.markdown_out,
    ]
    for path in inputs:
        if not path.exists():
            return [f"{path} is missing"]
    rows = builder.build_occurrences(args)
    summary_rows = builder.build_presence_summary(rows)
    expected = builder.render_markdown(rows, summary_rows, args)
    actual = args.markdown_out.read_text(encoding="utf-8")
    if actual != expected:
        return [
            f"{args.markdown_out} is stale; rerun python3 -m scripts.build_centered_occurrence_index"
        ]
    return []


if __name__ == "__main__":
    raise SystemExit(main())
