#!/usr/bin/env python3
"""Summarize ELS start/end boundary strata from the match-strata index."""

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
DEFAULT_OUT = Path("reports/boundary_alignment/summary.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/BOUNDARY_ALIGNMENT.md")
DEFAULT_MANIFEST_OUT = Path("reports/boundary_alignment/manifest.json")

FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "bucket",
    "rows",
    "distinct_terms",
    "share_of_group",
]

BOUNDARY_BUCKETS = (
    "boundary_start_verse",
    "boundary_start_chapter",
    "boundary_start_book",
    "boundary_end_verse",
    "boundary_end_chapter",
    "boundary_end_book",
    "boundary_both_endpoints",
    "no_boundary_data",
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.strata)
    summary_rows = summarize_boundary_alignment(input_rows)
    write_rows(args.out, summary_rows)
    write_markdown(args.markdown_out, args, input_rows, summary_rows)
    write_manifest(args.manifest_out, args, input_rows, summary_rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strata", type=Path, default=DEFAULT_STRATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def summarize_boundary_alignment(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (row.get("source_family", ""), row.get("corpus_class", ""), row.get("corpus", ""))
        groups.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for key, group_rows in sorted(groups.items()):
        total = len(group_rows)
        for bucket in BOUNDARY_BUCKETS:
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
    if bucket == "no_boundary_data":
        return [row for row in rows if not row.get("boundary_strata", "")]
    return [row for row in rows if bucket in row.get("boundary_strata", "").split(";")]


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    boundary_totals = Counter(str(row["bucket"]) for row in summary_rows for _ in range(int(row["rows"])))
    lines = [
        "# Boundary Alignment",
        "",
        "Status: post-search review aid, not claim promotion.",
        "",
        "This report summarizes whether ELS path starts and ends align with",
        "verse, chapter, or book boundaries. It depends on the already-built",
        "match-strata index and does not perform a new ELS search.",
        "",
        "## Settings",
        "",
        f"- Strata input: `{args.strata}`",
        f"- Input rows: `{len(input_rows)}`",
        "",
        "## Overall Boundary Counts",
        "",
        "| Bucket | Rows |",
        "| --- | ---: |",
    ]
    for bucket in BOUNDARY_BUCKETS:
        lines.append(f"| `{bucket}` | {boundary_totals[bucket]:,} |")

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
            "## Read",
            "",
            "- Boundary alignment is a review filter for path placement, not a",
            "  finding by itself.",
            "- `no_boundary_data` includes ordinary interior paths and rows whose",
            "  corpus/offsets could not be mapped to a loaded boundary index.",
            "- Claim-grade use needs matched controls with an equivalent structural",
            "  boundary definition.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_boundary_alignment.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "input_rows": len(input_rows),
        "summary_rows": len(summary_rows),
        "inputs": {"strata": str(args.strata)},
        "outputs": {
            "out": str(args.out),
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
