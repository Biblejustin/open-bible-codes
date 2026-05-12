#!/usr/bin/env python3
"""Annotate centered occurrences with post-search match strata."""

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
from els.match_strata import (
    canonical_first_keys,
    direction_strata_by_key,
    row_identity,
)
from els.term_display import display_term


DEFAULT_OCCURRENCES = Path("reports/centered_occurrence_index/centered_occurrences.csv")
DEFAULT_OUT = Path("reports/match_strata_index/occurrence_strata.csv")
DEFAULT_SUMMARY_OUT = Path("reports/match_strata_index/strata_summary.csv")
DEFAULT_MARKDOWN = Path("docs/MATCH_STRATA_INDEX.md")
DEFAULT_MANIFEST = Path("reports/match_strata_index/manifest.json")

GROUP_FIELDS = ("source_family", "source_queue", "corpus", "present_corpora", "term_id", "normalized_term")

FIELDNAMES = [
    "occurrence_rank",
    "source_family",
    "source_queue",
    "corpus_class",
    "corpus",
    "present_corpora",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "occurrence_type",
    "skip",
    "direction",
    "direction_stratum",
    "canonical_first_centered_occurrence",
    "canonical_first_group",
    "extended_strata",
    "review_note",
    "source_record",
]

SUMMARY_FIELDNAMES = ["stratum", "rows"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.occurrences)
    rows = build_strata_rows(input_rows)
    summary_rows = build_summary_rows(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--occurrences", type=Path, default=DEFAULT_OCCURRENCES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def build_strata_rows(input_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    direction_by_key = direction_strata_by_key(input_rows, key_fields=GROUP_FIELDS)
    canonical_first = canonical_first_keys(input_rows, group_fields=GROUP_FIELDS)
    output = []
    for row in input_rows:
        key = tuple(row.get(field, "") for field in GROUP_FIELDS)
        is_first = row_identity(row) in canonical_first
        strata = [
            row.get("occurrence_type", ""),
            direction_by_key.get(key, ""),
        ]
        if is_first:
            strata.append("canonical_first_occurrence")
        output.append(
            {
                "occurrence_rank": row.get("occurrence_rank", ""),
                "source_family": row.get("source_family", ""),
                "source_queue": row.get("source_queue", ""),
                "corpus_class": row.get("corpus_class", ""),
                "corpus": row.get("corpus", ""),
                "present_corpora": row.get("present_corpora", ""),
                "term_id": row.get("term_id", ""),
                "concept": row.get("concept", ""),
                "category": row.get("category", ""),
                "normalized_term": row.get("normalized_term", ""),
                "center_ref": row.get("center_ref", ""),
                "center_word": row.get("center_word", ""),
                "center_normalized_word": row.get("center_normalized_word", ""),
                "occurrence_type": row.get("occurrence_type", ""),
                "skip": row.get("skip", ""),
                "direction": row.get("direction", ""),
                "direction_stratum": direction_by_key.get(key, ""),
                "canonical_first_centered_occurrence": "yes" if is_first else "no",
                "canonical_first_group": "|".join(key),
                "extended_strata": ";".join(value for value in strata if value),
                "review_note": row.get("review_note", ""),
                "source_record": row.get("source_record", ""),
            }
        )
    return output


def build_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts: Counter[str] = Counter()
    for row in rows:
        for stratum in str(row.get("extended_strata", "")).split(";"):
            if stratum:
                counts[stratum] += 1
    return [{"stratum": key, "rows": value} for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Extended Match Strata Index",
        "",
        "This index annotates the current centered occurrence index with cheap",
        "post-search strata. It does not promote any row to claim status. The",
        "extra flags are review-prioritization metadata that still require the",
        "same preregistered controls described in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Bottom Line",
        "",
        f"- annotated occurrence rows: {len(rows):,}",
        "- materialized now: `forward_only`, `backward_only`, `bidirectional_present`, `canonical_first_occurrence`.",
        "- boundary endpoint strata are implemented as offset helpers in `els.match_strata`; they are not materialized from this centered index because the index does not retain every raw endpoint offset.",
        "",
        "## Strata Counts",
        "",
        "| Stratum | Rows |",
        "| --- | ---: |",
    ]
    for row in summary_rows:
        lines.append(f"| `{row['stratum']}` | {int(row['rows']):,} |")
    lines.extend(
        [
            "",
            "## Top Annotated Rows",
            "",
            "| Rank | Term | Center | Existing type | Direction stratum | Canonical first | Source |",
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows[: args.markdown_row_limit]:
        lines.append(markdown_row(row))
    if len(rows) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | {len(rows) - args.markdown_row_limit:,} more rows in CSV |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `canonical_first_occurrence` means first centered occurrence within the current indexed family, not first hidden occurrence in every raw hit export.",
            "- Direction strata are computed per source family / queue / corpus set / term group.",
            "- Boundary, matrix, cipher, cross-skip, and cohort-density strata widen the review surface and need separate locked controls before claim language.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"`{row.get('occurrence_type', '')}` | `{row.get('direction_stratum', '')}` | "
        f"{row.get('canonical_first_centered_occurrence', '')} | `{row.get('source_family', '')}` |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_match_strata_index.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "materialized_strata": [row["stratum"] for row in summary_rows],
        "inputs": {"occurrences": str(args.occurrences)},
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_match_strata_index "
        f"--occurrences {args.occurrences} "
        f"--out {args.out} "
        f"--summary-out {args.summary_out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
