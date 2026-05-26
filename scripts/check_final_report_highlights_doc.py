#!/usr/bin/env python3
"""Validate generated final-report highlights markdown freshness."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

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
    for path in (
        args.centered_summary,
        args.claim_catalog,
        args.out,
        args.markdown_out,
        args.manifest_out,
    ):
        if not path.exists():
            return [f"{path} is missing"]
    centered_rows = builder.read_rows(args.centered_summary)
    claim_rows = builder.read_rows(args.claim_catalog)
    highlights = builder.build_highlights(centered_rows, limit=args.limit)
    failures: list[str] = []
    failures.extend(validate_highlights_csv(args.out, highlights))
    failures.extend(validate_manifest(args.manifest_out, args, highlights, claim_rows))
    expected = builder.render_markdown(
        highlights,
        claim_rows,
        args,
    )
    actual = args.markdown_out.read_text(encoding="utf-8")
    if actual != expected:
        failures.append(
            f"{args.markdown_out} is stale; rerun python3 -m scripts.build_final_report_highlights"
        )
    return failures


def validate_highlights_csv(
    path: Path,
    highlights: list[dict[str, object]],
) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected = [_string_row(row, builder.FIELDNAMES) for row in highlights]
    if rows != expected:
        failures.append(f"{path} highlight rows drifted")
    return failures


def validate_manifest(
    path: Path,
    args: argparse.Namespace,
    highlights: list[dict[str, object]],
    claim_rows: list[dict[str, str]],
) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    checks: dict[str, Any] = {
        "tool": "build_final_report_highlights",
        "inputs": {
            "centered_summary": str(args.centered_summary),
            "claim_catalog": str(args.claim_catalog),
        },
        "outputs": {
            "highlights": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "highlight_rows": len(highlights),
        "claim_catalog_rows": len(claim_rows),
    }
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def _string_row(row: dict[str, object], fieldnames: list[str]) -> dict[str, str]:
    return {field: str(row.get(field, "")) for field in fieldnames}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
