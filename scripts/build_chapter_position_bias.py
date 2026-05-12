#!/usr/bin/env python3
"""Summarize chapter/book position strata from the match-strata index."""

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
DEFAULT_OUT = Path("reports/chapter_position_bias/summary.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/CHAPTER_POSITION_BIAS.md")
DEFAULT_MANIFEST_OUT = Path("reports/chapter_position_bias/manifest.json")

FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "bucket",
    "rows",
    "distinct_terms",
    "share_of_group",
]

POSITION_BUCKETS = (
    "center_verse_first_in_chapter",
    "center_verse_last_in_chapter",
    "center_verse_first_in_book",
    "center_verse_last_in_book",
    "interior_or_unmapped",
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.strata)
    summary_rows = summarize_position_bias(input_rows)
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


def summarize_position_bias(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (row.get("source_family", ""), row.get("corpus_class", ""), row.get("corpus", ""))
        groups.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for key, group_rows in sorted(groups.items()):
        total = len(group_rows)
        bucket_rows = {bucket: rows_for_bucket(group_rows, bucket) for bucket in POSITION_BUCKETS}
        for bucket in POSITION_BUCKETS:
            matching = bucket_rows[bucket]
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
    if bucket == "interior_or_unmapped":
        return [row for row in rows if not row.get("center_position_strata", "")]
    return [row for row in rows if bucket in row.get("center_position_strata", "").split(";")]


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
    position_totals = Counter(str(row["bucket"]) for row in summary_rows for _ in range(int(row["rows"])))
    lines = [
        "# Chapter Position Bias",
        "",
        "Status: post-search review aid, not claim promotion.",
        "",
        "This report summarizes whether centered occurrence rows land in verses",
        "that are first or last in their chapter or book. It depends on the",
        "already-built match-strata index and does not perform a new ELS search.",
        "",
        "## Settings",
        "",
        f"- Strata input: `{args.strata}`",
        f"- Input rows: `{len(input_rows)}`",
        "",
        "## Overall Position Counts",
        "",
        "| Bucket | Rows |",
        "| --- | ---: |",
    ]
    for bucket in POSITION_BUCKETS:
        lines.append(f"| `{bucket}` | {position_totals[bucket]:,} |")

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
            "- `interior_or_unmapped` includes ordinary interior verses and rows whose",
            "  corpus/ref could not be mapped to a loaded boundary index.",
            "- This is a distribution summary. It does not decide whether a position",
            "  is meaningful without matched controls and a locked comparison rule.",
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
        "script": "scripts/build_chapter_position_bias.py",
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
