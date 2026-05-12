#!/usr/bin/env python3
"""Summarize meaningful-skip and rarity review flags from the match-strata index."""

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
DEFAULT_OUT = Path("reports/review_flag_summary/summary.csv")
DEFAULT_FLAG_OUT = Path("reports/review_flag_summary/flag_rows.csv")
DEFAULT_MARKDOWN_OUT = Path("docs/REVIEW_FLAG_SUMMARY.md")
DEFAULT_MANIFEST_OUT = Path("reports/review_flag_summary/manifest.json")

SUMMARY_FIELDNAMES = [
    "source_family",
    "corpus_class",
    "corpus",
    "flag_type",
    "flag_rows",
    "distinct_terms",
    "share_of_input_rows",
]

FLAG_FIELDNAMES = [
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
    "flag_type",
    "flag_value",
    "evidence",
    "min_count",
    "max_count",
]

BASE_FIELDS = [
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
]

FLAG_TYPES = (
    "skip_equals_meaningful_constant",
    "skip_equals_term_gematria",
    "skip_equals_center_word_gematria",
    "bigram_surprise",
    "letter_frequency_anomaly",
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.strata)
    flag_rows = build_flag_rows(input_rows)
    summary_rows = summarize_flags(input_rows, flag_rows)
    write_rows(args.out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.flag_out, FLAG_FIELDNAMES, flag_rows)
    write_markdown(args.markdown_out, args, input_rows, summary_rows, flag_rows)
    write_manifest(args.manifest_out, args, input_rows, summary_rows, flag_rows, started)
    print(args.out)
    print(args.flag_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strata", type=Path, default=DEFAULT_STRATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--flag-out", type=Path, default=DEFAULT_FLAG_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build_flag_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        base = {field: row.get(field, "") for field in BASE_FIELDS}
        if row.get("skip_equals_meaningful_constant", "") == "yes":
            output.append(
                {
                    **base,
                    "flag_type": "skip_equals_meaningful_constant",
                    "flag_value": row.get("meaningful_constant_skips", ""),
                    "evidence": row.get("meaningful_constant_labels", ""),
                    "min_count": "",
                    "max_count": "",
                }
            )
        if row.get("skip_equals_term_gematria", "") == "yes":
            output.append(
                {
                    **base,
                    "flag_type": "skip_equals_term_gematria",
                    "flag_value": row.get("term_gematria_matching_skips", ""),
                    "evidence": row.get("term_gematria_value", ""),
                    "min_count": "",
                    "max_count": "",
                }
            )
        if row.get("skip_equals_center_word_gematria", "") == "yes":
            output.append(
                {
                    **base,
                    "flag_type": "skip_equals_center_word_gematria",
                    "flag_value": row.get("center_word_gematria_matching_skips", ""),
                    "evidence": row.get("center_word_gematria_value", ""),
                    "min_count": "",
                    "max_count": "",
                }
            )
        if row.get("bigram_surprise_stratum", ""):
            output.append(
                {
                    **base,
                    "flag_type": "bigram_surprise",
                    "flag_value": row.get("bigram_surprise_stratum", ""),
                    "evidence": row.get("bigram_surprise_evidence", ""),
                    "min_count": row.get("bigram_min_count", ""),
                    "max_count": row.get("bigram_max_count", ""),
                }
            )
        if row.get("letter_frequency_stratum", ""):
            output.append(
                {
                    **base,
                    "flag_type": "letter_frequency_anomaly",
                    "flag_value": row.get("letter_frequency_stratum", ""),
                    "evidence": row.get("letter_frequency_evidence", ""),
                    "min_count": row.get("letter_frequency_min_count", ""),
                    "max_count": row.get("letter_frequency_max_count", ""),
                }
            )
    return output


def summarize_flags(input_rows: list[dict[str, str]], flag_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    totals = Counter((row.get("source_family", ""), row.get("corpus_class", ""), row.get("corpus", "")) for row in input_rows)
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = {}
    for row in flag_rows:
        key = (
            str(row.get("source_family", "")),
            str(row.get("corpus_class", "")),
            str(row.get("corpus", "")),
            str(row.get("flag_type", "")),
        )
        grouped.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for key, rows in sorted(grouped.items()):
        group_total = totals[(key[0], key[1], key[2])]
        output.append(
            {
                "source_family": key[0],
                "corpus_class": key[1],
                "corpus": key[2],
                "flag_type": key[3],
                "flag_rows": len(rows),
                "distinct_terms": len({str(row.get("term_id", "")) for row in rows if row.get("term_id", "")}),
                "share_of_input_rows": f"{len(rows) / group_total:.6f}" if group_total else "0.000000",
            }
        )
    return output


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
    flag_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flag_counts = Counter(str(row["flag_type"]) for row in flag_rows)
    lines = [
        "# Review Flag Summary",
        "",
        "Status: post-search review aid, not claim promotion.",
        "",
        "This report unpivots meaningful-skip, gematria-skip, bigram-surprise,",
        "and letter-frequency anomaly flags from the match-strata index. It does",
        "not run a new ELS search.",
        "",
        "## Settings",
        "",
        f"- Strata input: `{args.strata}`",
        f"- Input rows: `{len(input_rows)}`",
        f"- Flag rows: `{len(flag_rows)}`",
        "",
        "## Overall Counts",
        "",
        "| Flag type | Rows |",
        "| --- | ---: |",
    ]
    for flag_type in FLAG_TYPES:
        lines.append(f"| `{flag_type}` | {flag_counts[flag_type]:,} |")

    lines.extend(
        [
            "",
            "## Source / Corpus Summary",
            "",
            "| Source family | Corpus class | Corpus | Flag type | Rows | Distinct terms | Share |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows[: args.markdown_row_limit]:
        lines.append(
            "| "
            f"`{row['source_family']}` | `{row['corpus_class']}` | `{row['corpus']}` | "
            f"`{row['flag_type']}` | {row['flag_rows']} | {row['distinct_terms']} | {row['share_of_input_rows']} |"
        )
    if len(summary_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | {len(summary_rows) - args.markdown_row_limit:,} more rows in CSV |")

    lines.extend(
        [
            "",
            "## Flag Rows",
            "",
            "| Source family | Corpus | Term | Center ref | Center word | Skip | Flag type | Value | Evidence |",
            "| --- | --- | --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in flag_rows[: args.markdown_row_limit]:
        lines.append(
            "| "
            f"`{row['source_family']}` | `{row['corpus']}` | `{row['term_id']}` | "
            f"`{row['center_ref']}` | `{row['center_word']}` | `{row['skip']}` | "
            f"`{row['flag_type']}` | {md_cell(row['flag_value'])} | {md_cell(row['evidence'])} |"
        )
    if len(flag_rows) > args.markdown_row_limit:
        lines.append(f"| ... | ... | ... | ... | ... | ... | ... | ... | {len(flag_rows) - args.markdown_row_limit:,} more rows in CSV |")

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- These flags help prioritize review; they do not change hit counts.",
            "- Meaningful constants and gematria schemes must be locked before",
            "  claim-grade use.",
            "- Bigram and letter-frequency flags are corpus-local metadata; controls",
            "  still decide whether a flagged row is unusual.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    input_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    flag_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_review_flag_summary.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "input_rows": len(input_rows),
        "summary_rows": len(summary_rows),
        "flag_rows": len(flag_rows),
        "inputs": {"strata": str(args.strata)},
        "outputs": {
            "out": str(args.out),
            "flag_out": str(args.flag_out),
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
