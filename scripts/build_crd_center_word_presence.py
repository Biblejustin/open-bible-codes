#!/usr/bin/env python3
"""Summarize CRD exact center-word hits by term and Bible edition."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from els.term_display import KNOWN_TERMS, display_term, normalized_script_key


FIELDNAMES = [
    "term_id",
    "term",
    "concept",
    "category",
    "language",
    "center_word_rows",
    "corpus_count",
    "corpora",
    "center_refs_sample",
    "bible_max_corpus",
    "bible_max_density",
    "secular_max_corpus",
    "secular_max_density",
    "ratio",
    "exceeds_secular_max",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_presence_rows(args.center_word_hits, args.summary, sample_refs=args.sample_refs)
    write_csv(args.output, rows)
    if args.markdown_out:
        write_markdown(args.markdown_out, rows, args)
    print(args.output)
    if args.markdown_out:
        print(args.markdown_out)
    print(f"terms={len(rows)}")
    print(f"hit_rows={sum(int(row['center_word_rows']) for row in rows)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--center-word-hits", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--sample-refs", type=int, default=6)
    return parser


def build_presence_rows(center_word_hits: Path, summary: Path, *, sample_refs: int) -> list[dict[str, str]]:
    summary_by_term = {row["term_id"]: row for row in read_dicts(summary)}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_dicts(center_word_hits):
        grouped[row["term_id"]].append(row)

    rows: list[dict[str, str]] = []
    for term_id, term_rows in grouped.items():
        first = term_rows[0]
        summary_row = summary_by_term.get(term_id, {})
        corpora = sorted({row.get("corpus", "") for row in term_rows if row.get("corpus")})
        refs = sorted(
            {
                f"{row.get('corpus', '')}:{row.get('center_ref', '')}"
                for row in term_rows
                if row.get("corpus") and row.get("center_ref")
            }
        )
        rows.append(
            {
                "term_id": term_id,
                "term": first.get("term", ""),
                "concept": first.get("concept", ""),
                "category": first.get("category", ""),
                "language": first.get("language", ""),
                "center_word_rows": str(len(term_rows)),
                "corpus_count": str(len(corpora)),
                "corpora": ";".join(corpora),
                "center_refs_sample": ";".join(refs[:sample_refs]),
                "bible_max_corpus": summary_row.get("bible_max_corpus", ""),
                "bible_max_density": summary_row.get("bible_max_density", ""),
                "secular_max_corpus": summary_row.get("secular_max_corpus", ""),
                "secular_max_density": summary_row.get("secular_max_density", ""),
                "ratio": summary_row.get("ratio", ""),
                "exceeds_secular_max": summary_row.get("exceeds_secular_max", ""),
            }
        )
    rows.sort(key=presence_sort_key)
    return rows


def presence_sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
    return (
        0 if row.get("exceeds_secular_max") == "true" else 1,
        -int(row.get("corpus_count") or 0),
        -int(row.get("center_word_rows") or 0),
        row.get("term_id", ""),
    )


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    corpus_counts = Counter(row["corpus_count"] for row in rows)
    language_counts = Counter(row["language"] for row in rows)
    exceeding = [row for row in rows if row.get("exceeds_secular_max") == "true"]
    lines = [
        "# CRD Exact Center-Word Version Presence",
        "",
        "Status: local summary generated from ignored CRD exact center-word artifacts.",
        "",
        "## Inputs",
        "",
        f"- center-word hits: `{args.center_word_hits}`",
        f"- center-word summary: `{args.summary}`",
        "",
        "## Summary",
        "",
        f"- term rows: {len(rows):,}",
        f"- exact center-word hit rows: {sum(int(row['center_word_rows']) for row in rows):,}",
        f"- terms exceeding secular max: {len(exceeding):,}",
        f"- language distribution: {format_counter(language_counts)}",
        f"- corpus-count distribution: {format_counter(corpus_counts)}",
        "",
        "## Strongest Multi-Version Rows",
        "",
        "| Term | Language | Rows | Corpus count | Corpora | Exceeds secular max | Bible max | Secular max |",
        "| --- | --- | ---: | ---: | --- | --- | ---: | ---: |",
    ]
    for row in rows[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    term_cell(row),
                    escape_md(row["language"]),
                    row["center_word_rows"],
                    row["corpus_count"],
                    escape_md(row["corpora"]),
                    row["exceeds_secular_max"],
                    row["bible_max_density"],
                    row["secular_max_density"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- A term can be meaningful in one source without appearing in every source.",
            "- Multi-version rows are useful for stability review, not automatic claim promotion.",
            "- Single-version rows remain visible because source-specific patterns are part of the study question.",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def term_cell(row: dict[str, str]) -> str:
    term = row.get("term", "")
    concept = row.get("concept", "")
    term_id = row.get("term_id", "")
    if term:
        english = None if normalized_script_key(term) in KNOWN_TERMS else concept or None
        return md_cell(f"{display_term(term, english=english)}<br>`{term_id}`")
    return f"`{escape_md(term_id)}`"


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def format_counter(counter: Counter[str]) -> str:
    return ", ".join(f"{key}={value:,}" for key, value in counter.most_common())


def escape_md(value: str) -> str:
    return value.replace("|", "\\|")


def md_cell(value: str) -> str:
    return escape_md(value).replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
