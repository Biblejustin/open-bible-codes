#!/usr/bin/env python3
"""Build context review rows for synthetic extension match controls."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus
from els.normalization import normalize_text
from scripts import analyze_extension_paired_controls as paired


MATCHES_IN = Path("reports/synthetic_extension_baselines_matches.csv")
SUMMARY_OUT = Path("reports/synthetic_extension_match_review_summary.csv")
MD_OUT = Path("reports/synthetic_extension_match_review.md")
MANIFEST_OUT = Path("reports/synthetic_extension_match_review.manifest.json")

FIELDNAMES = [
    "target_id",
    "corpus",
    "target_term",
    "target_extension_type",
    "target_extended_sequence",
    "observed_score",
    "synthetic_query",
    "synthetic_score",
    "synthetic_extension_type",
    "synthetic_extended_sequence",
    "synthetic_matched_examples",
    "synthetic_matched_refs",
    "synthetic_hit_refs",
    "synthetic_extension_refs",
    "synthetic_center_ref",
    "synthetic_center_word",
    "center_has_synthetic_query_surface",
    "hit_span_has_synthetic_query_surface",
    "extension_span_has_synthetic_phrase_surface",
    "center_verse_text",
    "hit_verse_text",
    "extension_verse_text",
    "context_read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    matches = read_rows(args.matches)
    corpora = {
        corpus_label: load_corpus(paired.CORPUS_CONFIGS[corpus_label])
        for corpus_label in sorted({row["corpus"] for row in matches})
    }
    rows = [review_row(row, corpora[row["corpus"]]) for row in matches]
    rows.sort(key=lambda row: (row["corpus"], row["target_id"], row["synthetic_query"]))
    write_rows(args.summary_out, rows)
    write_markdown(args.markdown_out, rows)
    write_manifest(args, len(matches), len(rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", type=Path, default=MATCHES_IN)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def review_row(row: dict[str, str], corpus: Corpus) -> dict[str, str]:
    hit_verses = verses_between_refs(
        corpus,
        row["synthetic_hit_start_ref"],
        row["synthetic_hit_end_ref"],
    )
    extension_verses = verses_between_refs(
        corpus,
        row["synthetic_extension_start_ref"],
        row["synthetic_extension_end_ref"],
    )
    center_verse = verse_by_ref(corpus, row["synthetic_hit_center_ref"])
    center_norm = normalize_text(center_verse.raw_text, corpus.language)
    hit_norm = normalize_text(" ".join(verse.raw_text for verse in hit_verses), corpus.language)
    extension_norm = normalize_text(
        " ".join(verse.raw_text for verse in extension_verses),
        corpus.language,
    )
    query = row["synthetic_query"]
    phrase = row["synthetic_extended_sequence"]
    center_has_query = query in center_norm
    hit_has_query = query in hit_norm
    extension_has_phrase = phrase in extension_norm
    return {
        "target_id": row["target_id"],
        "corpus": row["corpus"],
        "target_term": row["term"],
        "target_extension_type": row["target_extension_type"],
        "target_extended_sequence": row["target_extended_sequence"],
        "observed_score": row["observed_score"],
        "synthetic_query": query,
        "synthetic_score": row["synthetic_score"],
        "synthetic_extension_type": row["synthetic_extension_type"],
        "synthetic_extended_sequence": phrase,
        "synthetic_matched_examples": row["synthetic_matched_examples"],
        "synthetic_matched_refs": row["synthetic_matched_refs"],
        "synthetic_hit_refs": refs_cell(hit_verses),
        "synthetic_extension_refs": refs_cell(extension_verses),
        "synthetic_center_ref": center_verse.ref,
        "synthetic_center_word": row["synthetic_hit_center_word"],
        "center_has_synthetic_query_surface": yes_no(center_has_query),
        "hit_span_has_synthetic_query_surface": yes_no(hit_has_query),
        "extension_span_has_synthetic_phrase_surface": yes_no(extension_has_phrase),
        "center_verse_text": center_verse.raw_text,
        "hit_verse_text": verses_cell(hit_verses),
        "extension_verse_text": verses_cell(extension_verses),
        "context_read": context_read(center_has_query, hit_has_query, extension_has_phrase),
    }


def verse_by_ref(corpus: Corpus, ref: str) -> VerseSpan:
    for verse in corpus.verses:
        if verse.ref == ref:
            return verse
    raise ValueError(f"unknown ref {ref}")


def verses_between_refs(corpus: Corpus, first_ref: str, second_ref: str) -> tuple[VerseSpan, ...]:
    first = verse_by_ref(corpus, first_ref)
    second = verse_by_ref(corpus, second_ref)
    low, high = sorted((verse_index(corpus, first), verse_index(corpus, second)))
    return tuple(corpus.verses[low : high + 1])


def verse_index(corpus: Corpus, verse: VerseSpan) -> int:
    return corpus.position_to_verse[verse.norm_start]


def context_read(
    center_has_query: bool,
    hit_has_query: bool,
    extension_has_phrase: bool,
) -> str:
    if extension_has_phrase:
        return "synthetic phrase appears as surface text in extension span"
    if center_has_query:
        return "synthetic query appears in center verse surface text"
    if hit_has_query:
        return "synthetic query appears in hit-span surface text"
    return "synthetic ELS-only at hit span; matched phrase appears elsewhere"


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Synthetic Extension Match Review",
        "",
        "Context review for synthetic extension control rows that equal or exceed target any-type scores.",
        "",
        "## Summary",
        "",
        "| Read | Rows |",
        "| --- | ---: |",
    ]
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["context_read"]] = counts.get(row["context_read"], 0) + 1
    for read, count in sorted(counts.items()):
        lines.append(f"| {read} | {count} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Corpus | Target | Synthetic | Center | Surface checks | Matched phrase |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        checks = (
            f"center query={row['center_has_synthetic_query_surface']}; "
            f"hit query={row['hit_span_has_synthetic_query_surface']}; "
            f"extension phrase={row['extension_span_has_synthetic_phrase_surface']}"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    f"`{row['target_term']}` `{row['target_extended_sequence']}`",
                    f"`{row['synthetic_query']}` `{row['synthetic_extended_sequence']}` score {row['synthetic_score']}",
                    f"{row['synthetic_center_ref']} `{row['synthetic_center_word']}`",
                    checks,
                    f"{row['synthetic_matched_examples']} @ {row['synthetic_matched_refs']}",
                ]
            )
            + " |"
        )
    lines.extend(["", "## Context Excerpts"])
    for row in rows:
        lines.append("")
        lines.append(
            f"- {row['corpus']} `{row['synthetic_query']}` / `{row['synthetic_extended_sequence']}` at {row['synthetic_center_ref']}: {row['center_verse_text']}"
        )
        if row["hit_verse_text"] != row["center_verse_text"]:
            lines.append(f"  Hit span: {row['hit_verse_text']}")
        if row["extension_verse_text"] != row["hit_verse_text"]:
            lines.append(f"  Extension span: {row['extension_verse_text']}")
        lines.append(f"  Read: {row['context_read']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(args: argparse.Namespace, matches: int, rows: int, started: float) -> None:
    payload = {
        "tool": "analyze_synthetic_extension_match_review",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "matches": str(args.matches),
        "match_rows": matches,
        "rows": rows,
        "outputs": [
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


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def refs_cell(verses: tuple[VerseSpan, ...]) -> str:
    return "; ".join(verse.ref for verse in verses)


def verses_cell(verses: tuple[VerseSpan, ...]) -> str:
    return " ".join(f"{verse.ref}: {verse.raw_text}" for verse in verses)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


if __name__ == "__main__":
    raise SystemExit(main())
