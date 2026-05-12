#!/usr/bin/env python3
"""Summarize cross-skip pair strata from the match-strata index."""

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
DEFAULT_OUT = Path("reports/cross_skip_summary/summary.csv")
DEFAULT_CANDIDATE_OUT = Path("reports/cross_skip_summary/candidate_rows.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/CROSS_SKIP_SUMMARY.md")
DEFAULT_MANIFEST_OUT = Path("reports/cross_skip_summary/manifest.json")

SUMMARY_FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "bucket",
    "rows",
    "distinct_terms",
    "share_of_group",
]

CANDIDATE_FIELDNAMES = [
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
    "cross_skip_pair_at_word",
    "cross_skip_pair_count",
    "cross_skip_pair_terms",
    "cross_skip_pair_skips",
    "cross_skip_pair_at_letter",
    "cross_skip_pair_at_letter_count",
    "cross_skip_pair_at_letter_terms",
    "cross_skip_pair_within_N_letters",
    "cross_skip_pair_within_letter_distance",
    "cross_skip_pair_within_letter_min_distance",
    "cross_skip_pair_within_letter_count",
    "cross_skip_pair_within_letter_terms",
]

CROSS_SKIP_BUCKETS = (
    "cross_skip_pair_at_word",
    "cross_skip_pair_at_letter",
    "cross_skip_pair_within_N_letters",
    "no_cross_skip_pair_data",
)

CROSS_SKIP_FLAGS = (
    "cross_skip_pair_at_word",
    "cross_skip_pair_at_letter",
    "cross_skip_pair_within_N_letters",
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.strata)
    summary_rows = summarize_cross_skip(input_rows)
    candidate_rows = cross_skip_candidate_rows(input_rows)
    write_rows(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.candidate_out, CANDIDATE_FIELDNAMES, candidate_rows)
    write_markdown(args.markdown_out, args, input_rows, summary_rows, candidate_rows)
    write_manifest(args.manifest_out, args, input_rows, summary_rows, candidate_rows, started)
    print(args.out)
    print(args.candidate_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strata", type=Path, default=DEFAULT_STRATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--candidate-out", type=Path, default=DEFAULT_CANDIDATE_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def summarize_cross_skip(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (row.get("source_family", ""), row.get("corpus_class", ""), row.get("corpus", ""))
        groups.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for key, group_rows in sorted(groups.items()):
        total = len(group_rows)
        for bucket in CROSS_SKIP_BUCKETS:
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
    if bucket == "no_cross_skip_pair_data":
        return [row for row in rows if not has_cross_skip_pair(row)]
    return [row for row in rows if row.get(bucket, "") == "yes"]


def has_cross_skip_pair(row: dict[str, str]) -> bool:
    return any(row.get(field, "") == "yes" for field in CROSS_SKIP_FLAGS)


def cross_skip_candidate_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {field: row.get(field, "") for field in CANDIDATE_FIELDNAMES}
        for row in rows
        if has_cross_skip_pair(row)
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
    candidate_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bucket_totals = Counter(str(row["bucket"]) for row in summary_rows for _ in range(int(row["rows"])))
    lines = [
        "# Cross-Skip Summary",
        "",
        "Status: post-search review aid, not claim promotion.",
        "",
        "This report summarizes centered rows where another declared term appears",
        "at the same center word, at a shared hidden-letter position, or within",
        "the configured endpoint-letter distance at a different skip. It depends",
        "on the already-built match-strata index and does not perform a new ELS",
        "search.",
        "",
        "## Settings",
        "",
        f"- Strata input: `{args.strata}`",
        f"- Input rows: `{len(input_rows)}`",
        f"- Candidate rows: `{len(candidate_rows)}`",
        "",
        "## Overall Counts",
        "",
        "Buckets may overlap. Candidate rows are the union of rows with any",
        "cross-skip pair flag.",
        "",
        "| Bucket | Rows |",
        "| --- | ---: |",
    ]
    for bucket in CROSS_SKIP_BUCKETS:
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
            "## Candidate Rows",
            "",
            "| Source family | Corpus | Term | Center ref | Center word | Skip | Pair types | Pair terms |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in candidate_rows[: args.markdown_row_limit]:
        pair_types = ";".join(field for field in CROSS_SKIP_FLAGS if row.get(field, "") == "yes")
        pair_terms = first_nonempty(
            row.get("cross_skip_pair_terms", ""),
            row.get("cross_skip_pair_at_letter_terms", ""),
            row.get("cross_skip_pair_within_letter_terms", ""),
        )
        lines.append(
            "| "
            f"`{row['source_family']}` | `{row['corpus']}` | `{row['term_id']}` | "
            f"`{row['center_ref']}` | `{row['center_word']}` | `{row['skip']}` | "
            f"{md_cell(pair_types)} | {md_cell(pair_terms)} |"
        )
    if len(candidate_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | ... | {len(candidate_rows) - args.markdown_row_limit:,} more rows in CSV |")

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- Cross-skip rows are useful for pair review and audit packets.",
            "- They are not stronger by default; paired controls define whether",
            "  a cross-skip relationship is unusual.",
            "- Claim-grade use needs the pair metric and correction family locked",
            "  before looking at candidate rows.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def first_nonempty(*values: object) -> str:
    for value in values:
        text = str(value).strip()
        if text:
            return text
    return ""


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_cross_skip_summary.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "input_rows": len(input_rows),
        "summary_rows": len(summary_rows),
        "candidate_rows": len(candidate_rows),
        "inputs": {"strata": str(args.strata)},
        "outputs": {
            "out": str(args.out),
            "candidate_out": str(args.candidate_out),
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
