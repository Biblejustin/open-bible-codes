#!/usr/bin/env python3
"""Summarize canonical-first centered occurrences from the match-strata index."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_STRATA = Path("reports/match_strata_index/occurrence_strata.csv")
DEFAULT_OUT = Path("reports/canonical_first_summary/summary.csv")
DEFAULT_FIRST_OUT = Path("reports/canonical_first_summary/first_occurrences.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/CANONICAL_FIRST_SUMMARY.md")
DEFAULT_MANIFEST_OUT = Path("reports/canonical_first_summary/manifest.json")

SUMMARY_FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "bucket",
    "rows",
    "distinct_terms",
    "share_of_group",
]

FIRST_FIELDNAMES = [
    "source_family",
    "source_queue",
    "corpus_class",
    "corpus",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "center_ref",
    "center_word",
    "skip",
    "direction",
    "canonical_first_group",
]

BUCKETS = ("canonical_first_centered_occurrence", "later_centered_occurrence", "no_canonical_first_data")


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.strata)
    summary_rows = summarize_canonical_first(input_rows)
    first_rows = canonical_first_rows(input_rows)
    write_rows(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.first_out, FIRST_FIELDNAMES, first_rows)
    write_markdown(args.markdown_out, args, input_rows, summary_rows, first_rows)
    write_manifest(args.manifest_out, args, input_rows, summary_rows, first_rows, started)
    print(args.out)
    print(args.first_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strata", type=Path, default=DEFAULT_STRATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--first-out", type=Path, default=DEFAULT_FIRST_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def summarize_canonical_first(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (row.get("source_family", ""), row.get("corpus_class", ""), row.get("corpus", ""))
        groups.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for key, group_rows in sorted(groups.items()):
        total = len(group_rows)
        for bucket in BUCKETS:
            matching = rows_for_bucket(group_rows, bucket)
            output.append(
                {
                    "source_family": key[0],
                    "corpus_class": key[1],
                    "corpus": key[2],
                    "bucket": bucket,
                    "rows": len(matching),
                    "distinct_terms": len({row.get("term_id", "") for row in matching if row.get("term_id", "")}),
                    "share_of_group": f"{len(matching) / total:.6f}" if total else "0.000000",
                }
            )
    return output


def rows_for_bucket(rows: list[dict[str, str]], bucket: str) -> list[dict[str, str]]:
    if bucket == "canonical_first_centered_occurrence":
        return [row for row in rows if row.get("canonical_first_centered_occurrence", "") == "yes"]
    if bucket == "later_centered_occurrence":
        return [row for row in rows if row.get("canonical_first_centered_occurrence", "") == "no"]
    return [row for row in rows if row.get("canonical_first_centered_occurrence", "") not in {"yes", "no"}]


def canonical_first_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {field: row.get(field, "") for field in FIRST_FIELDNAMES}
        for row in rows
        if row.get("canonical_first_centered_occurrence", "") == "yes"
    ]


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    first_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bucket_totals = Counter(str(row["bucket"]) for row in summary_rows for _ in range(int(row["rows"])))
    lines = [
        "# Canonical First Summary",
        "",
        "Status: post-search review aid, not claim promotion.",
        "",
        "This report lists and summarizes the first centered occurrence of each",
        "term/corpus group in canonical order, as already annotated by the",
        "match-strata index. It does not perform a new ELS search.",
        "",
        "## Settings",
        "",
        f"- Strata input: `{args.strata}`",
        f"- Input rows: `{len(input_rows)}`",
        f"- Canonical-first rows: `{len(first_rows)}`",
        "",
        "## Overall Counts",
        "",
        "| Bucket | Rows |",
        "| --- | ---: |",
    ]
    for bucket in BUCKETS:
        lines.append(f"| `{bucket}` | {bucket_totals[bucket]:,} |")

    lines.extend(
        [
            "",
            "## Source / Corpus Summary",
            "",
            "| Source family | Corpus class | Corpus | Bucket | Rows | Distinct terms | Share |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows[: args.markdown_row_limit]:
        lines.append(
            "| "
            f"`{row['source_family']}` | `{row['corpus_class']}` | `{row['corpus']}` | "
            f"`{row['bucket']}` | {row['rows']} | {row['distinct_terms']} | {row['share_of_group']} |"
        )
    if len(summary_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | {len(summary_rows) - args.markdown_row_limit:,} more rows in CSV |")

    lines.extend(
        [
            "",
            "## First Occurrence Rows",
            "",
            "| Source family | Corpus | Term | Center ref | Center word | Skip | Direction |",
            "| --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in first_rows[: args.markdown_row_limit]:
        lines.append(
            "| "
            f"`{row['source_family']}` | `{row['corpus']}` | `{row['term_id']}` | "
            f"`{row['center_ref']}` | `{row['center_word']}` | `{row['skip']}` | `{row['direction']}` |"
        )
    if len(first_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | {len(first_rows) - args.markdown_row_limit:,} more rows in CSV |")

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Canonical-first rows are useful for review ordering and audit packets.",
            "- This summary does not assert that a first occurrence is meaningful.",
            "- Claim-grade use needs a locked comparison rule and matched controls.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_canonical_first_summary.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "input_rows": len(input_rows),
        "summary_rows": len(summary_rows),
        "canonical_first_rows": len(first_rows),
        "inputs": {"strata": str(args.strata)},
        "outputs": {
            "out": str(args.out),
            "first_out": str(args.first_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
