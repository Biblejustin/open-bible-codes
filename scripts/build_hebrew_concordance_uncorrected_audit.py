#!/usr/bin/env python3
"""Build an audit sheet for Hebrew concordance rows with uncorrected-only controls."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_SUMMARY = Path("reports/hebrew_concordance_words_prospective/controlled_summary.csv")
DEFAULT_EXAMPLES = Path("reports/hebrew_concordance_words_prospective/controlled_examples.csv")
DEFAULT_OUT = Path("reports/hebrew_concordance_words_prospective/uncorrected_screening_audit.csv")
DEFAULT_MD = Path("docs/HEBREW_CONCORDANCE_UNCORRECTED_SCREENING_AUDIT.md")
DEFAULT_MANIFEST = Path(
    "reports/hebrew_concordance_words_prospective/uncorrected_screening_audit.manifest.json"
)

OUT_FIELDNAMES = [
    "rank",
    "term_id",
    "category",
    "term",
    "normalized_term",
    "concept",
    "normalized_length",
    "exact_total_hits",
    "exact_all_source_patterns",
    "representative_best_p",
    "representative_best_q",
    "flags",
    "sample_center_words",
    "primary_read",
]

SCOPE_PRIORITY = {
    "present_all_observed_sources": 0,
    "present_all_leningrad_streams": 1,
    "present_multiple_sources": 2,
    "source_specific": 3,
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    summary_rows = read_rows(args.summary)
    example_rows = read_rows(args.examples)
    audit_rows = build_audit(summary_rows, example_rows)
    write_rows(args.output, OUT_FIELDNAMES, audit_rows)
    write_markdown(args.markdown, audit_rows, args)
    write_manifest(args, audit_rows, started)
    print(args.output)
    print(args.markdown)
    print(args.manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--examples", type=Path, default=DEFAULT_EXAMPLES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--title",
        default="Hebrew Concordance Uncorrected Screening Audit",
    )
    return parser


def build_audit(
    summary_rows: list[dict[str, str]],
    example_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    examples_by_term = group_examples(example_rows)
    selected = [
        row
        for row in summary_rows
        if row.get("representative_best_band") == "paired_uncorrected_p_le_0.05"
    ]
    selected.sort(
        key=lambda row: (
            parse_float(row.get("representative_best_p")) or float("inf"),
            row.get("category", ""),
            row.get("term_id", ""),
        )
    )
    return [
        audit_row(rank, row, examples_by_term.get(row.get("term_id", ""), []))
        for rank, row in enumerate(selected, start=1)
    ]


def audit_row(rank: int, row: dict[str, str], examples: list[dict[str, str]]) -> dict[str, str]:
    flags = classify_row(row)
    return {
        "rank": str(rank),
        "term_id": row.get("term_id", ""),
        "category": row.get("category", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "concept": row.get("concept", ""),
        "normalized_length": row.get("normalized_length", ""),
        "exact_total_hits": row.get("exact_total_hits", ""),
        "exact_all_source_patterns": row.get("exact_all_source_patterns", ""),
        "representative_best_p": row.get("representative_best_p", ""),
        "representative_best_q": row.get("representative_best_q", ""),
        "flags": "; ".join(flags),
        "sample_center_words": "; ".join(sample_center_words(examples)),
        "primary_read": primary_read(row, flags),
    }


def classify_row(row: dict[str, str]) -> list[str]:
    flags = ["no_adjusted_support"]
    length = parse_int(row.get("normalized_length"))
    all_source_patterns = parse_int(row.get("exact_all_source_patterns")) or 0
    total_hits = parse_int(row.get("exact_total_hits")) or 0
    category = row.get("category", "")

    if all_source_patterns == 0:
        flags.append("no_all_source_exact_patterns")
    elif all_source_patterns <= 3:
        flags.append("sparse_all_source_patterns")
    if length is not None and length <= 4:
        flags.append("short_string")
    if all_source_patterns >= 1000 or total_hits >= 10000:
        flags.append("high_pattern_volume")
    if category == "strong_proper_names":
        flags.append("proper_name_gloss")
    return flags


def primary_read(row: dict[str, str], flags: list[str]) -> str:
    if "no_all_source_exact_patterns" in flags:
        return "control artifact only; no all-source exact row to review"
    if "sparse_all_source_patterns" in flags:
        return "sparse all-source pattern count; too thin for a context claim"
    if "high_pattern_volume" in flags:
        return "high-volume short-string/common-letter risk; triage only"
    if "proper_name_gloss" in flags:
        return "proper-name/gloss prompt; needs manual context review before any follow-up"
    return "ordinary lexical prompt; no adjusted representative-control support"


def group_examples(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("term_id", "")].append(row)
    for term_rows in grouped.values():
        term_rows.sort(key=example_sort_key)
    return grouped


def example_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    return (
        SCOPE_PRIORITY.get(row.get("presence_scope", ""), 9),
        abs(parse_int(row.get("skip")) or 0),
        row.get("center_ref", ""),
    )


def sample_center_words(rows: list[dict[str, str]], limit: int = 5) -> list[str]:
    words: list[str] = []
    seen = set()
    for row in rows:
        for word in parse_center_words(row.get("center_words_by_corpus", "")):
            if word in seen:
                continue
            seen.add(word)
            words.append(word)
            if len(words) == limit:
                return words
    return words


def parse_center_words(value: str) -> list[str]:
    words = []
    for item in value.split(";"):
        item = item.strip()
        if not item or ":" not in item:
            continue
        _corpus, word = item.split(":", 1)
        word = word.strip()
        if word:
            words.append(word)
    return words


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    category_counts = Counter(row["category"] for row in rows)
    flag_counts = Counter(flag for row in rows for flag in split_flags(row["flags"]))
    read_counts = Counter(row["primary_read"] for row in rows)
    q_values = sorted({row["representative_best_q"] for row in rows if row["representative_best_q"]})
    lines = [
        f"# {args.title}",
        "",
        "Status: generated audit for the Hebrew concordance uncorrected queue; no claim.",
        "",
        "This audit classifies the 87 Hebrew concordance rows that cleared only",
        "the uncorrected representative-control screen. It does not upgrade them:",
        "the corrected family-level result is still negative.",
        "",
        "## Inputs",
        "",
        f"- Summary: `{args.summary}`",
        f"- Examples: `{args.examples}`",
        f"- CSV audit: `{args.output}`",
        "",
        "## Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Audit rows | {len(rows)} |",
        f"| Adjusted-support rows | {sum(1 for row in rows if q_le_005(row['representative_best_q']))} |",
        f"| Distinct representative q values | {len(q_values)} |",
    ]
    for category, count in category_counts.most_common():
        lines.append(f"| `{category}` rows | {count} |")
    for flag, count in flag_counts.most_common():
        lines.append(f"| `{flag}` flags | {count} |")
    lines.extend(
        [
            "",
            "## Read Buckets",
            "",
            "| Read | Rows |",
            "| --- | ---: |",
        ]
    )
    for read, count in read_counts.most_common():
        lines.append(f"| {md_cell(read)} | {count} |")
    lines.extend(
        [
            "",
            "## Audit Rows",
            "",
            "| Rank | Term | Category | All-source patterns | p | q | Flags | Sample centers | Read |",
            "| ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["rank"],
                    md_cell(f"`{row['term_id']}` `{row['normalized_term']}` ({row['concept']})"),
                    md_cell(f"`{row['category']}`"),
                    format_int(row["exact_all_source_patterns"]),
                    format_float(row["representative_best_p"]),
                    format_float(row["representative_best_q"]),
                    md_cell(row["flags"]),
                    md_cell(row["sample_center_words"]),
                    md_cell(row["primary_read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Follow-Up Gate",
            "",
            "Do not use this audit as a claim list. A stricter follow-up should be",
            "preregistered before new searching. Minimum gates should include: adjusted",
            "support, non-sparse all-source pattern counts, exclusion or separate handling",
            "of high-volume short strings, and a context-distance rule that prevents",
            "surface-word and gloss artifacts from driving interpretation.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(args: argparse.Namespace, rows: list[dict[str, str]], started: float) -> None:
    manifest = {
        "tool": "build_hebrew_concordance_uncorrected_audit",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "inputs": [str(args.summary), str(args.examples)],
        "outputs": [str(args.output), str(args.markdown), str(args.manifest)],
        "rows": len(rows),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def split_flags(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def q_le_005(value: str) -> bool:
    parsed = parse_float(value)
    return parsed is not None and parsed <= 0.05


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value.replace(",", "")))


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def format_int(value: str) -> str:
    parsed = parse_int(value)
    return f"{parsed:,}" if parsed is not None else ""


def format_float(value: str) -> str:
    parsed = parse_float(value)
    return f"{parsed:.6f}" if parsed is not None else ""


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
