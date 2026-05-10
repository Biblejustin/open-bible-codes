#!/usr/bin/env python3
"""Triage the expanded Greek exact-center surface queue with explicit filters."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.normalization import normalize_greek
from els.term_display import display_term


TERMS_IN = Path("terms/greek_expanded_prospective_terms.csv")
PATTERNS_IN = Path("reports/greek_expanded_surface_queue/surface_patterns.csv")
SUMMARY_IN = Path("reports/greek_expanded_surface_queue/term_summary.csv")
OUT_DIR = Path("reports/greek_expanded_surface_triage")
SELECTED_OUT = OUT_DIR / "selected_patterns.csv"
COHORT_OUT = OUT_DIR / "term_cohort.csv"
MD_OUT = Path("docs/GREEK_EXPANDED_SURFACE_TRIAGE.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

COHORT_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "total_exact_center_hits",
    "unique_patterns",
    "all_source_patterns",
    "multi_source_patterns",
    "source_specific_patterns",
    "length_cohort_terms",
    "length_cohort_all_source_rank",
    "selected",
    "read",
]

SELECTED_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "present_corpora",
    "center_words_by_corpus",
    "offsets_by_corpus",
    "length_cohort_all_source_rank",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_rows = read_rows(args.terms)
    summary_rows = read_rows(args.term_summary)
    pattern_rows = read_rows(args.patterns)
    cohort_rows = build_cohort_rows(
        term_rows,
        summary_rows,
        min_length=args.min_length,
    )
    selected_rows = selected_pattern_rows(
        pattern_rows,
        cohort_rows,
        min_length=args.min_length,
    )
    write_rows(args.cohort_out, COHORT_FIELDNAMES, cohort_rows)
    write_rows(args.selected_out, SELECTED_FIELDNAMES, selected_rows)
    write_markdown(args.markdown_out, cohort_rows, selected_rows, args)
    write_manifest(args, cohort_rows, selected_rows, started)
    print(args.selected_out)
    print(args.cohort_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS_IN)
    parser.add_argument("--patterns", type=Path, default=PATTERNS_IN)
    parser.add_argument("--term-summary", type=Path, default=SUMMARY_IN)
    parser.add_argument("--min-length", type=int, default=5)
    parser.add_argument("--title", default="Greek Expanded Surface Triage")
    parser.add_argument("--status", default="post-screen triage; no claim and no p-value.")
    parser.add_argument(
        "--description",
        default=(
            "This report narrows the expanded Greek exact-center surface queue with a "
            "mechanical filter before any future controls are designed."
        ),
    )
    parser.add_argument("--selected-out", type=Path, default=SELECTED_OUT)
    parser.add_argument("--cohort-out", type=Path, default=COHORT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def build_cohort_rows(
    term_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    *,
    min_length: int,
) -> list[dict[str, str]]:
    summary_by_term = {row["term_id"]: row for row in summary_rows}
    rows = []
    for term in term_rows:
        normalized = normalize_greek(term["term"])
        summary = summary_by_term.get(term["term_id"], {})
        all_source = int_or_zero(summary.get("all_source_patterns", "0"))
        multi = int_or_zero(summary.get("multi_source_patterns", "0"))
        source_specific = int_or_zero(summary.get("source_specific_patterns", "0"))
        unique = int_or_zero(summary.get("unique_patterns", "0"))
        hits = int_or_zero(summary.get("total_exact_center_hits", "0"))
        selected = all_source > 0 and len(normalized) >= min_length
        rows.append(
            {
                "term_id": term["term_id"],
                "concept": term["concept"],
                "category": term["category"],
                "term": term["term"],
                "normalized_term": normalized,
                "normalized_length": str(len(normalized)),
                "total_exact_center_hits": str(hits),
                "unique_patterns": str(unique),
                "all_source_patterns": str(all_source),
                "multi_source_patterns": str(multi),
                "source_specific_patterns": str(source_specific),
                "length_cohort_terms": "0",
                "length_cohort_all_source_rank": "0",
                "selected": str(selected),
                "read": term_read(selected, all_source, multi, source_specific, len(normalized), min_length),
            }
        )
    return ranked_cohort_rows(rows)


def ranked_cohort_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_length: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_length[int(row["normalized_length"])].append(row)
    for length_rows in by_length.values():
        sorted_rows = sorted(
            length_rows,
            key=lambda row: (
                -int(row["all_source_patterns"]),
                -int(row["multi_source_patterns"]),
                -int(row["total_exact_center_hits"]),
                row["term_id"],
            ),
        )
        for index, row in enumerate(sorted_rows, start=1):
            row["length_cohort_terms"] = str(len(length_rows))
            row["length_cohort_all_source_rank"] = str(index)
    return sorted(
        rows,
        key=lambda row: (
            row["selected"] != "True",
            int(row["normalized_length"]),
            int(row["length_cohort_all_source_rank"]),
            row["term_id"],
        ),
    )


def selected_pattern_rows(
    pattern_rows: list[dict[str, str]],
    cohort_rows: list[dict[str, str]],
    *,
    min_length: int,
) -> list[dict[str, str]]:
    cohort_by_term = {row["term_id"]: row for row in cohort_rows}
    rows = []
    for pattern in pattern_rows:
        cohort = cohort_by_term.get(pattern["term_id"])
        if cohort is None:
            continue
        if pattern["presence_scope"] != "all_sources":
            continue
        if int(cohort["normalized_length"]) < min_length:
            continue
        rows.append(
            {
                "term_id": pattern["term_id"],
                "concept": pattern["concept"],
                "category": pattern["category"],
                "term": pattern["term"],
                "normalized_term": pattern["normalized_term"],
                "normalized_length": cohort["normalized_length"],
                "skip": pattern["skip"],
                "direction": pattern["direction"],
                "start_ref": pattern["start_ref"],
                "center_ref": pattern["center_ref"],
                "end_ref": pattern["end_ref"],
                "present_corpora": pattern["present_corpora"],
                "center_words_by_corpus": pattern["center_words_by_corpus"],
                "offsets_by_corpus": pattern["offsets_by_corpus"],
                "length_cohort_all_source_rank": cohort["length_cohort_all_source_rank"],
                "read": "tight review row; needs matched surface-frequency controls",
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            int(row["normalized_length"]),
            int(row["length_cohort_all_source_rank"]),
            row["term_id"],
            int(row["skip"]),
        ),
    )


def term_read(
    selected: bool,
    all_source: int,
    multi: int,
    source_specific: int,
    length: int,
    min_length: int,
) -> str:
    if selected:
        return "tight all-source surface review queue"
    if all_source and length < min_length:
        return "all-source but below length threshold"
    if multi:
        return "multi-source broader surface queue"
    if source_specific:
        return "source-specific broader surface queue"
    return "no exact-center surface pattern"


def write_markdown(
    path: Path,
    cohort_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    selected_terms = {row["term_id"] for row in selected_rows}
    scope_counts = Counter(
        "selected" if row["selected"] == "True" else row["read"] for row in cohort_rows
    )
    all_source_short = sum(
        int(row["all_source_patterns"]) for row in cohort_rows if row["read"] == "all-source but below length threshold"
    )
    lines = [
        f"# {args.title}",
        "",
        f"Status: {args.status}",
        "",
        *wrap_sentences(args.description),
        "",
        "## Inputs",
        "",
        f"- Term list: `{args.terms}`",
        f"- Surface patterns: `{args.patterns}`",
        f"- Term summary: `{args.term_summary}`",
        "",
        "## Filter",
        "",
        f"- keep only patterns present in every compared Greek NT source;",
        f"- require normalized term length >= {args.min_length};",
        "- keep hidden-path-only rows as review candidates rather than failures;",
        "- do not use random nonsense terms as surface controls, because surface",
        "  context requires real words that can appear openly in a verse.",
        "",
        *length_filter_note(args.min_length),
        "",
        "## Result",
        "",
        f"- selected patterns: {len(selected_rows):,}",
        f"- selected terms: {len(selected_terms):,}",
        f"- all-source patterns below length threshold: {all_source_short:,}",
        f"- total cohort terms: {len(cohort_rows):,}",
        "",
        "| Term | Concept | Length | Center | Skip | Direction | Length-cohort rank | Center words |",
        "| --- | --- | ---: | --- | ---: | --- | ---: | --- |",
    ]
    for row in selected_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(display_triage_term(row)),
                    md_cell(row["concept"]),
                    row["normalized_length"],
                    row["center_ref"],
                    row["skip"],
                    row["direction"],
                    row["length_cohort_all_source_rank"],
                    display_center_words_by_corpus(row["center_words_by_corpus"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Cohort Counts",
            "",
            "| Bucket | Terms |",
            "| --- | ---: |",
        ]
    )
    for bucket, count in sorted(scope_counts.items()):
        lines.append(f"| {bucket} | {count:,} |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            *triage_read_lines(selected_rows, all_source_short),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def triage_read_lines(
    selected_rows: list[dict[str, str]],
    all_source_short: int,
) -> list[str]:
    if not selected_rows:
        return [
            "No row met the registered all-source plus length threshold.",
            f"The all-source surface patterns found here were below the length threshold: {all_source_short}.",
            "This is a negative result for the primary prospective filter, not a claim.",
        ]
    selected_terms = ", ".join(unique_display_terms(selected_rows))
    return [
        f"This creates a smaller review queue: {selected_terms}.",
        "It is not a claim-grade result. The next statistically honest control",
        "compares these rows against real Greek terms matched by length and",
        "surface frequency, not against random strings that cannot satisfy the",
        "surface-context condition.",
    ]


def length_filter_note(min_length: int) -> list[str]:
    if min_length > 4:
        amen_display = display_term("αμην", english="Amen")
        return [
            "The length filter is deliberately mechanical. It excludes the dense length-4",
            f"bucket, including {amen_display}, without making a term-specific judgment about",
            "which short terms are meaningful.",
        ]
    return [
        "This follow-up deliberately includes the dense length-4 bucket. Treat",
        "short-form all-source rows as post-discovery review material unless a",
        "separate prospective study registers them in advance.",
    ]


def wrap_sentences(text: str) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        if sum(len(item) + 1 for item in current) + len(word) > 78:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def display_triage_term(row: dict[str, str]) -> str:
    return display_term(row["normalized_term"], english=row.get("concept", ""))


def display_center_words_by_corpus(value: str) -> str:
    cells = []
    for part in value.split("; "):
        if ":" not in part:
            cells.append(display_term(part))
            continue
        corpus, words = part.split(":", 1)
        displayed_words = "/".join(display_term(word) for word in words.split("/") if word)
        cells.append(f"{corpus}:{displayed_words}")
    return md_cell("; ".join(cells))


def unique_display_terms(rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    terms = []
    for row in sorted(rows, key=lambda item: (item["normalized_term"], item["concept"])):
        key = row["normalized_term"]
        if key in seen:
            continue
        seen.add(key)
        terms.append(display_triage_term(row))
    return terms


def md_cell(value: str) -> str:
    return value.replace("|", "\\|")


def write_manifest(
    args: argparse.Namespace,
    cohort_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_expanded_surface_triage",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "min_length": args.min_length,
        "terms": str(args.terms),
        "patterns": str(args.patterns),
        "term_summary": str(args.term_summary),
        "cohort_terms": len(cohort_rows),
        "selected_patterns": len(selected_rows),
        "selected_terms": len({row["term_id"] for row in selected_rows}),
        "outputs": [
            str(args.selected_out),
            str(args.cohort_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def int_or_zero(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
