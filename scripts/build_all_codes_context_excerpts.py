#!/usr/bin/env python3
"""Export center/span text excerpts for selected all-codes rows."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus
from els.normalization import normalize_text
from els.term_display import display_term
from scripts.analyze_all_codes_letter_paths import parse_offsets_by_corpus, split_corpora


SELECTED_IN = Path("reports/all_codes_followup_selection/selected_rows.csv")
OUT_DIR = Path("reports/all_codes_followup_context")
EXCERPTS_OUT = OUT_DIR / "context_excerpts.csv"
MD_OUT = Path("docs/ALL_CODES_FOLLOWUP_CONTEXT.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"
DEFAULT_CORPORA = (
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "MAM=configs/example_mam.toml",
    "UHB=configs/example_uhb.toml",
    "TR_NT=configs/example_ebible_grctr.toml",
    "BYZ_NT=configs/example_ebible_grcmt.toml",
    "TCG_NT=configs/example_ebible_grctcgnt.toml",
    "SBLGNT=configs/example_sblgnt.toml",
)

FIELDNAMES = [
    "selection_rank",
    "source_queue",
    "bucket",
    "presence_scope",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "audit_corpus",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
    "center_verse_contains_normalized_term",
    "span_contains_normalized_term",
    "span_refs",
    "center_verse_text",
    "span_verse_text",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    selected_rows = read_rows(args.selected)
    configs = parse_corpus_args(args.corpus)
    corpora = {label: load_corpus(config) for label, config in configs.items()}
    excerpt_rows = build_excerpt_rows(selected_rows, corpora)
    write_rows(args.excerpts_out, excerpt_rows)
    write_markdown(args.markdown_out, excerpt_rows, args)
    write_manifest(args, selected_rows, excerpt_rows, started)
    print(args.excerpts_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected", type=Path, default=SELECTED_IN)
    parser.add_argument("--corpus", action="append", default=list(DEFAULT_CORPORA))
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    parser.add_argument("--excerpts-out", type=Path, default=EXCERPTS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=CONFIG for --corpus, got {value!r}")
        label, config = value.split("=", 1)
        parsed[label] = Path(config)
    return parsed


def build_excerpt_rows(
    selected_rows: list[dict[str, str]],
    corpora: dict[str, Corpus],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in selected_rows:
        offsets_by_corpus = parse_offsets_by_corpus(row["offsets_by_corpus"])
        for corpus_label in split_corpora(row["present_corpora"]):
            corpus = corpora[corpus_label]
            start, center, end = offsets_by_corpus[corpus_label]
            output.append(excerpt_row(row, corpus_label, corpus, start, center, end))
    return output


def excerpt_row(
    row: dict[str, str],
    corpus_label: str,
    corpus: Corpus,
    start: int,
    center: int,
    end: int,
) -> dict[str, str]:
    start_index = corpus.position_to_verse[start]
    center_index = corpus.position_to_verse[center]
    end_index = corpus.position_to_verse[end]
    low = min(start_index, end_index)
    high = max(start_index, end_index)
    span_verses = corpus.verses[low : high + 1]
    center_verse = corpus.verses[center_index]
    normalized_term = row["normalized_term"]
    center_normalized = normalize_verse(corpus, center_verse)
    span_normalized = "".join(normalize_verse(corpus, verse) for verse in span_verses)
    return {
        "selection_rank": row.get("selection_rank", ""),
        "source_queue": row.get("source_queue", ""),
        "bucket": row.get("bucket", ""),
        "presence_scope": row.get("presence_scope", ""),
        "term_id": row.get("term_id", ""),
        "concept": row.get("concept", ""),
        "category": row.get("category", ""),
        "normalized_term": normalized_term,
        "audit_corpus": corpus_label,
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "start_ref": corpus.ref_at(start),
        "center_ref": corpus.ref_at(center),
        "end_ref": corpus.ref_at(end),
        "center_word": row.get("center_word", ""),
        "center_normalized_word": row.get("center_normalized_word", ""),
        "center_verse_contains_normalized_term": str(normalized_term in center_normalized),
        "span_contains_normalized_term": str(normalized_term in span_normalized),
        "span_refs": "; ".join(verse.ref for verse in span_verses),
        "center_verse_text": center_verse.raw_text,
        "span_verse_text": " || ".join(f"{verse.ref}: {verse.raw_text}" for verse in span_verses),
    }


def normalize_verse(corpus: Corpus, verse: VerseSpan) -> str:
    return normalize_text(
        verse.raw_text,
        corpus.language,
        keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
    )


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    rows_to_show = rows[: args.markdown_row_limit]
    by_corpus = Counter(row["audit_corpus"] for row in rows)
    center_contains = sum(row["center_verse_contains_normalized_term"] == "True" for row in rows)
    span_contains = sum(row["span_contains_normalized_term"] == "True" for row in rows)
    lines = [
        "# All-Codes Follow-Up Context",
        "",
        "Status: context excerpt aid, not a claim.",
        "",
        "This report gives center-verse and start-to-end span text for the selected",
        "all-codes follow-up rows. It helps manual review decide whether surface",
        "content is actually meaningful, merely lexical, or unrelated.",
        "",
        "## Counts",
        "",
        f"- excerpt rows: {len(rows):,}",
        f"- center verses containing normalized hidden term: {center_contains:,}",
        f"- spans containing normalized hidden term: {span_contains:,}",
        f"- rows by corpus: `{dict(sorted(by_corpus.items()))}`",
        "",
        "## Excerpts",
        "",
        "| Rank | Corpus | Term | Center | Center has term | Span has term | Center excerpt |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows_to_show:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["selection_rank"],
                    row["audit_corpus"],
                    display_term(row["normalized_term"], english=row.get("concept", "")),
                    row["center_ref"],
                    row["center_verse_contains_normalized_term"],
                    row["span_contains_normalized_term"],
                    md_cell(truncate(row["center_verse_text"], 140)),
                ]
            )
            + " |"
        )
    if len(rows) > len(rows_to_show):
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | {len(rows) - len(rows_to_show):,} more rows in CSV |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "The boolean columns are simple normalized substring checks. They do not",
            "judge theological relation; they only show whether the hidden term text",
            "itself appears in the center verse or across the ELS span verses.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def truncate(value: str, limit: int) -> str:
    value = " ".join(value.split())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def write_manifest(
    args: argparse.Namespace,
    selected_rows: list[dict[str, str]],
    excerpt_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_all_codes_context_excerpts",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "selected_rows": len(selected_rows),
        "excerpt_rows": len(excerpt_rows),
        "center_contains_normalized_term_rows": sum(
            row["center_verse_contains_normalized_term"] == "True" for row in excerpt_rows
        ),
        "span_contains_normalized_term_rows": sum(
            row["span_contains_normalized_term"] == "True" for row in excerpt_rows
        ),
        "outputs": [str(args.excerpts_out), str(args.markdown_out), str(args.manifest_out)],
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


if __name__ == "__main__":
    raise SystemExit(main())
