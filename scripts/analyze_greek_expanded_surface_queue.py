#!/usr/bin/env python3
"""Summarize exact-center surface-verse patterns from the expanded Greek screen."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_hebrew_hit_version_presence import canonical_ref


INPUT = Path("reports/greek_expanded_prospective_exact_center/surface_context_hits.csv")
OUT_DIR = Path("reports/greek_expanded_surface_queue")
PATTERNS_OUT = OUT_DIR / "surface_patterns.csv"
SUMMARY_OUT = OUT_DIR / "term_summary.csv"
MD_OUT = Path("docs/GREEK_EXPANDED_SURFACE_QUEUE.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"
DEFAULT_CORPORA = ("TR_NT", "BYZ_NT", "TCG_NT", "SBLGNT")

PATTERN_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "present_corpora",
    "absent_corpora",
    "presence_scope",
    "hit_count",
    "center_words_by_corpus",
    "offsets_by_corpus",
    "read",
]
SUMMARY_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "total_exact_center_hits",
    "unique_patterns",
    "all_source_patterns",
    "multi_source_patterns",
    "source_specific_patterns",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = [row for row in read_rows(args.surface_hits) if row.get("center_exact") == "True"]
    pattern_rows = surface_pattern_rows(rows, tuple(args.corpus))
    summary_rows = term_summary_rows(pattern_rows, rows)
    write_rows(args.patterns_out, PATTERN_FIELDNAMES, pattern_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, pattern_rows, summary_rows, args)
    write_manifest(args, len(rows), len(pattern_rows), len(summary_rows), started)
    print(args.patterns_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface-hits", type=Path, default=INPUT)
    parser.add_argument("--corpus", action="append", default=list(DEFAULT_CORPORA))
    parser.add_argument("--title", default="Greek Expanded Surface Queue")
    parser.add_argument(
        "--status",
        default="post-screen exact-center surface queue; no claim.",
    )
    parser.add_argument(
        "--term-scope",
        default="terms/greek_expanded_prospective_terms.csv",
    )
    parser.add_argument(
        "--description",
        default=(
            "This report summarizes exact-center surface hits from the expanded Greek "
            "prospective term screen. It does not require same-skip phrase extension and "
            "does not run controls."
        ),
    )
    parser.add_argument("--patterns-out", type=Path, default=PATTERNS_OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def surface_pattern_rows(
    rows: list[dict[str, str]],
    corpus_order: tuple[str, ...],
) -> list[dict[str, str]]:
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[pattern_key(row)].append(row)
    return sorted(
        [surface_pattern_row(group, corpus_order) for group in groups.values()],
        key=lambda row: (
            -len(split_corpora(row["present_corpora"])),
            row["term_id"],
            int(row["skip"]),
            row["direction"],
            row["center_ref"],
        ),
    )


def pattern_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row["term_id"],
        row["normalized_term"],
        row["skip"],
        row["direction"],
        canonical_ref(row["start_ref"]),
        canonical_ref(row["center_ref"]),
        canonical_ref(row["end_ref"]),
    )


def surface_pattern_row(
    group: list[dict[str, str]],
    corpus_order: tuple[str, ...],
) -> dict[str, str]:
    first = group[0]
    present = ordered_corpora({row["corpus"] for row in group}, corpus_order)
    absent = [corpus for corpus in corpus_order if corpus not in present]
    return {
        "term_id": first["term_id"],
        "concept": first["concept"],
        "category": first["category"],
        "term": first["term"],
        "normalized_term": first["normalized_term"],
        "skip": first["skip"],
        "direction": first["direction"],
        "start_ref": canonical_ref(first["start_ref"]),
        "center_ref": canonical_ref(first["center_ref"]),
        "end_ref": canonical_ref(first["end_ref"]),
        "present_corpora": ",".join(present),
        "absent_corpora": ",".join(absent),
        "presence_scope": scope_label(present, corpus_order),
        "hit_count": str(len(group)),
        "center_words_by_corpus": joined_by_corpus(group, "center_word", corpus_order),
        "offsets_by_corpus": joined_offsets(group, corpus_order),
        "read": read_label(present, corpus_order),
    }


def term_summary_rows(
    pattern_rows: list[dict[str, str]],
    exact_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    exact_counts = Counter(row["term_id"] for row in exact_rows)
    by_term: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in pattern_rows:
        by_term[row["term_id"]].append(row)
    output = []
    for term_id, rows in by_term.items():
        first = rows[0]
        all_source = sum(row["presence_scope"] == "all_sources" for row in rows)
        multi = sum(row["presence_scope"] == "multi_source" for row in rows)
        source_only = sum(row["presence_scope"] == "source_only" for row in rows)
        output.append(
            {
                "term_id": term_id,
                "concept": first["concept"],
                "category": first["category"],
                "term": first["term"],
                "normalized_term": first["normalized_term"],
                "total_exact_center_hits": str(exact_counts[term_id]),
                "unique_patterns": str(len(rows)),
                "all_source_patterns": str(all_source),
                "multi_source_patterns": str(multi),
                "source_specific_patterns": str(source_only),
                "read": term_read(all_source, multi, source_only),
            }
        )
    return sorted(
        output,
        key=lambda row: (
            -int(row["all_source_patterns"]),
            -int(row["multi_source_patterns"]),
            -int(row["total_exact_center_hits"]),
            row["term_id"],
        ),
    )


def ordered_corpora(corpora: set[str], corpus_order: tuple[str, ...]) -> list[str]:
    ordered = [corpus for corpus in corpus_order if corpus in corpora]
    ordered.extend(sorted(corpora - set(ordered)))
    return ordered


def split_corpora(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def scope_label(present: list[str], corpus_order: tuple[str, ...]) -> str:
    if len(present) == len(corpus_order):
        return "all_sources"
    if len(present) > 1:
        return "multi_source"
    return "source_only"


def read_label(present: list[str], corpus_order: tuple[str, ...]) -> str:
    present_set = set(present)
    if len(present) == len(corpus_order):
        return "surface exact-center pattern in every compared source"
    if present_set == {"BYZ_NT", "TCG_NT"}:
        return "surface exact-center pattern in related Byzantine-source pair"
    if len(present) > 1:
        return "surface exact-center pattern in multiple sources"
    return "source-specific surface exact-center pattern"


def term_read(all_source: int, multi: int, source_only: int) -> str:
    if all_source:
        return "all-source surface queue; needs controls before interpretation"
    if multi:
        return "multi-source surface queue; inspect source distribution"
    if source_only:
        return "source-specific surface queue"
    return "no exact-center surface rows"


def joined_by_corpus(
    rows: list[dict[str, str]],
    field: str,
    corpus_order: tuple[str, ...],
) -> str:
    by_corpus: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        value = row.get(field, "")
        if value:
            by_corpus[row["corpus"]].append(value)
    return "; ".join(
        f"{corpus}:{'/'.join(values)}"
        for corpus in corpus_order
        if (values := by_corpus.get(corpus))
    )


def joined_offsets(rows: list[dict[str, str]], corpus_order: tuple[str, ...]) -> str:
    by_corpus = {row["corpus"]: row for row in rows}
    cells = []
    for corpus in corpus_order:
        row = by_corpus.get(corpus)
        if row is None:
            continue
        cells.append(
            f"{corpus}:{row['start_offset']}/{row['center_offset']}/{row['end_offset']}"
        )
    return "; ".join(cells)


def write_markdown(
    path: Path,
    pattern_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    scope_counts = Counter(row["presence_scope"] for row in pattern_rows)
    lines = [
        f"# {args.title}",
        "",
        f"Status: {args.status}",
        "",
        *wrap_sentences(args.description),
        "",
        "## Inputs",
        "",
        f"- Surface hits: `{args.surface_hits}`",
        f"- Term scope: `{args.term_scope}`",
        "- Compared sources: TR_NT, BYZ_NT, TCG_NT, SBLGNT",
        "",
        "## Definition",
        "",
        "`exact-center surface` means the ELS hit center falls in a verse where the",
        "normalized term also appears as ordinary surface text. The `Center words`",
        "column reports the actual word at the ELS center offset, so it may differ",
        "from the searched term.",
        "",
        "## Scope Counts",
        "",
        "| Scope | Patterns |",
        "| --- | ---: |",
    ]
    for scope, count in sorted(scope_counts.items()):
        lines.append(f"| `{scope}` | {count:,} |")
    lines.extend(
        [
            "",
            f"Total exact-center surface patterns: {len(pattern_rows):,}.",
            "",
            "## Top Term Queue",
            "",
            "| Term | Concept | Exact-center hits | Unique patterns | All-source | Multi-source | Source-specific | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in summary_rows[:30]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['normalized_term']}`",
                    row["concept"],
                    row["total_exact_center_hits"],
                    row["unique_patterns"],
                    row["all_source_patterns"],
                    row["multi_source_patterns"],
                    row["source_specific_patterns"],
                    row["read"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## All-Source Pattern Examples",
            "",
            "| Term | Center | Skip | Direction | Present | Center words |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in [item for item in pattern_rows if item["presence_scope"] == "all_sources"][:30]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['normalized_term']}`",
                    row["center_ref"],
                    row["skip"],
                    row["direction"],
                    row["present_corpora"],
                    row["center_words_by_corpus"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This queue is broader and weaker than the phrase-extension gate. It is useful",
            "for deciding which exact-center surface rows deserve matched controls.",
            "It does not promote any row to claim status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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


def write_manifest(
    args: argparse.Namespace,
    exact_rows: int,
    pattern_rows: int,
    summary_rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_expanded_surface_queue",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "surface_hits": str(args.surface_hits),
        "exact_center_rows": exact_rows,
        "pattern_rows": pattern_rows,
        "summary_rows": summary_rows,
        "outputs": [
            str(args.patterns_out),
            str(args.summary_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
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


if __name__ == "__main__":
    raise SystemExit(main())
