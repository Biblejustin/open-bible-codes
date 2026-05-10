#!/usr/bin/env python3
"""Add surface-context review fields to apocrypha bridge candidates."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus
from els.normalization import normalize_text
from els.search import build_hit, normalize_for_corpus
from els.surface import (
    SurfaceContext,
    SurfaceTerm,
    build_surface_context_index,
    normalize_verses,
    surface_context_for_hit_indexed,
)
from els.term_display import display_term


DEFAULT_CANDIDATES = Path("reports/apocrypha_bridge_candidates/bridge_candidates.csv")
DEFAULT_TERMS = [
    Path("terms/theological_terms.csv"),
    Path("terms/prophetic_terms.csv"),
    Path("terms/greek_nt_claim_terms.csv"),
]
DEFAULT_OUT = Path("reports/apocrypha_bridge_context/context.csv")
DEFAULT_SUMMARY = Path("reports/apocrypha_bridge_context/summary.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_BRIDGE_CONTEXT.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_bridge_context/manifest.json")

BUCKET_ORDER = {
    "center_word_exact": 0,
    "center_word_same_concept": 1,
    "center_word_same_category": 2,
    "center_verse_exact": 3,
    "center_verse_same_concept": 4,
    "center_verse_same_category": 5,
    "span_exact": 6,
    "span_same_concept": 7,
    "span_same_category": 8,
    "hidden_path_only": 9,
}

FIELDNAMES = [
    "context_rank",
    "source_rank",
    "corpus",
    "term_ids",
    "concepts",
    "categories",
    "normalized_term",
    "term_length",
    "skip",
    "direction",
    "bridge_type",
    "context_bucket",
    "best_context",
    "start_ref",
    "center_ref",
    "end_ref",
    "start_book",
    "center_book",
    "end_book",
    "canonical_books",
    "apocrypha_books",
    "class_path",
    "center_word",
    "center_normalized_word",
    "center_word_exact",
    "center_word_same_concept",
    "center_word_same_category",
    "center_exact",
    "center_same_concept",
    "center_same_category",
    "span_exact",
    "span_same_concept",
    "span_same_category",
    "center_word_same_concept_terms",
    "center_word_same_category_terms",
    "center_same_concept_terms",
    "center_same_category_terms",
    "span_exact_refs",
    "span_same_concept_refs",
    "span_same_category_refs",
    "span_refs",
    "center_verse_text",
    "span_verse_text",
    "letter_path",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


@dataclass
class TermLookup:
    terms: tuple[SurfaceTerm, ...]
    by_id: dict[str, SurfaceTerm]
    by_normalized: dict[str, tuple[SurfaceTerm, ...]]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.terms is None:
        args.terms = list(DEFAULT_TERMS)
    corpus = load_corpus(args.config)
    candidates = read_rows(args.candidates)
    lookup = build_term_lookup(corpus, args.terms, min_length=args.min_term_length)
    rows = build_context_rows(candidates, corpus, lookup, args)
    summary = summarize(rows, candidates, corpus, args)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary)
    write_markdown(args.markdown_out, rows, summary, args)
    write_manifest(args.manifest_out, args, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-label", default="LXX")
    parser.add_argument("--config", type=Path, default=Path("configs/example_ebible_grclxx.toml"))
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--terms", type=Path, action="append")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_term_lookup(
    corpus: Corpus,
    paths: list[Path],
    *,
    min_length: int,
) -> TermLookup:
    terms: list[SurfaceTerm] = []
    seen_ids: set[str] = set()
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("language") != corpus.language:
                    continue
                term_id = row.get("term_id", "")
                if not term_id or term_id in seen_ids:
                    continue
                seen_ids.add(term_id)
                term = row.get("term", "").strip()
                normalized = normalize_for_corpus(corpus, term)
                if len(normalized) < min_length:
                    continue
                terms.append(
                    SurfaceTerm(
                        term_source=str(path),
                        term_id=term_id,
                        concept=row.get("concept", ""),
                        category=row.get("category", ""),
                        term=term,
                        normalized_term=normalized,
                    )
                )
    by_id = {term.term_id: term for term in terms}
    by_normalized: dict[str, list[SurfaceTerm]] = {}
    for term in terms:
        by_normalized.setdefault(term.normalized_term, []).append(term)
    return TermLookup(
        terms=tuple(terms),
        by_id=by_id,
        by_normalized={
            normalized: tuple(items)
            for normalized, items in by_normalized.items()
        },
    )


def build_context_rows(
    candidates: list[dict[str, str]],
    corpus: Corpus,
    lookup: TermLookup,
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    normalized_verses = normalize_verses(corpus)
    context_index = build_surface_context_index(corpus, list(lookup.terms), normalized_verses)
    rows: list[dict[str, str]] = []
    for candidate in candidates:
        term = choose_surface_term(candidate, lookup)
        if term is None:
            continue
        positions = letter_positions(candidate.get("letter_path", ""))
        if not positions:
            continue
        skip = int(candidate["skip"])
        hit = build_hit(
            corpus,
            term.term,
            candidate["normalized_term"],
            skip,
            positions[0],
            positions[-1],
        )
        context = surface_context_for_hit_indexed(
            corpus,
            hit,
            term,
            list(lookup.terms),
            context_index,
        )
        span_indexes = list(range(
            corpus.position_to_verse[min(positions)],
            corpus.position_to_verse[max(positions)] + 1,
        ))
        rows.append(context_row(candidate, corpus, positions, span_indexes, context))
    rows.sort(key=context_sort_key)
    for rank, row in enumerate(rows, 1):
        row["context_rank"] = str(rank)
    return rows


def choose_surface_term(row: dict[str, str], lookup: TermLookup) -> SurfaceTerm | None:
    for term_id in split_semicolon(row.get("term_ids", "")):
        term = lookup.by_id.get(term_id)
        if term is not None:
            return term
    normalized = row.get("normalized_term", "")
    matches = lookup.by_normalized.get(normalized, ())
    return matches[0] if matches else None


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def letter_positions(letter_path: str) -> list[int]:
    positions: list[int] = []
    for part in split_semicolon(letter_path):
        try:
            positions.append(int(part.rsplit(":", 1)[1]))
        except (IndexError, ValueError):
            continue
    return positions


def context_row(
    candidate: dict[str, str],
    corpus: Corpus,
    positions: list[int],
    span_indexes: list[int],
    context: SurfaceContext,
) -> dict[str, str]:
    center_index = corpus.position_to_verse[(min(positions) + max(positions)) // 2]
    center_verse = corpus.verses[center_index]
    span_verses = [corpus.verses[index] for index in span_indexes]
    row = {
        "context_rank": "0",
        "source_rank": candidate.get("rank", ""),
        "corpus": candidate.get("corpus", ""),
        "term_ids": candidate.get("term_ids", ""),
        "concepts": candidate.get("concepts", ""),
        "categories": candidate.get("categories", ""),
        "normalized_term": candidate.get("normalized_term", ""),
        "term_length": candidate.get("term_length", ""),
        "skip": candidate.get("skip", ""),
        "direction": candidate.get("direction", ""),
        "bridge_type": candidate.get("bridge_type", ""),
        "context_bucket": bucket_for_context(context),
        "best_context": context.best_context,
        "start_ref": candidate.get("start_ref", ""),
        "center_ref": candidate.get("center_ref", ""),
        "end_ref": candidate.get("end_ref", ""),
        "start_book": candidate.get("start_book", ""),
        "center_book": candidate.get("center_book", ""),
        "end_book": candidate.get("end_book", ""),
        "canonical_books": candidate.get("canonical_books", ""),
        "apocrypha_books": candidate.get("apocrypha_books", ""),
        "class_path": candidate.get("class_path", ""),
        "center_word": candidate.get("center_word", ""),
        "center_normalized_word": candidate.get("center_normalized_word", ""),
        "center_word_exact": str(context.center_word_exact),
        "center_word_same_concept": str(context.center_word_same_concept),
        "center_word_same_category": str(context.center_word_same_category),
        "center_exact": str(context.center_exact),
        "center_same_concept": str(context.center_same_concept),
        "center_same_category": str(context.center_same_category),
        "span_exact": str(context.span_exact),
        "span_same_concept": str(context.span_same_concept),
        "span_same_category": str(context.span_same_category),
        "center_word_same_concept_terms": context.center_word_same_concept_terms,
        "center_word_same_category_terms": context.center_word_same_category_terms,
        "center_same_concept_terms": context.center_same_concept_terms,
        "center_same_category_terms": context.center_same_category_terms,
        "span_exact_refs": context.span_exact_refs,
        "span_same_concept_refs": context.span_same_concept_refs,
        "span_same_category_refs": context.span_same_category_refs,
        "span_refs": ";".join(verse.ref for verse in span_verses),
        "center_verse_text": center_verse.raw_text,
        "span_verse_text": " || ".join(format_verse(verse) for verse in span_verses),
        "letter_path": candidate.get("letter_path", ""),
    }
    return row


def format_verse(verse: VerseSpan) -> str:
    return f"{verse.ref}: {verse.raw_text}"


def bucket_for_context(context: SurfaceContext) -> str:
    if context.center_word_exact:
        return "center_word_exact"
    if context.center_word_same_concept:
        return "center_word_same_concept"
    if context.center_word_same_category:
        return "center_word_same_category"
    if context.center_exact:
        return "center_verse_exact"
    if context.center_same_concept:
        return "center_verse_same_concept"
    if context.center_same_category:
        return "center_verse_same_category"
    if context.span_exact:
        return "span_exact"
    if context.span_same_concept:
        return "span_same_concept"
    if context.span_same_category:
        return "span_same_category"
    return "hidden_path_only"


def context_sort_key(row: dict[str, str]) -> tuple[Any, ...]:
    return (
        BUCKET_ORDER[row["context_bucket"]],
        abs(int(row["skip"])),
        int_or_large(row.get("source_rank", "")),
        row.get("normalized_term", ""),
    )


def int_or_large(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 10**12


def summarize(
    rows: list[dict[str, str]],
    candidates: list[dict[str, str]],
    corpus: Corpus,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    buckets = Counter(row["context_bucket"] for row in rows)
    terms_by_bucket: dict[str, set[str]] = {bucket: set() for bucket in BUCKET_ORDER}
    for row in rows:
        terms_by_bucket[row["context_bucket"]].add(row["normalized_term"])
    summary: list[dict[str, object]] = [
        {"metric": "corpus", "value": args.corpus_label},
        {"metric": "corpus_letters", "value": len(corpus.text)},
        {"metric": "candidate_rows", "value": len(candidates)},
        {"metric": "context_rows", "value": len(rows)},
        {"metric": "terms_with_context_rows", "value": len({row["normalized_term"] for row in rows})},
    ]
    for bucket in BUCKET_ORDER:
        summary.append({"metric": f"bucket:{bucket}", "value": buckets[bucket]})
        summary.append(
            {
                "metric": f"terms:{bucket}",
                "value": len(terms_by_bucket[bucket]),
            }
        )
    return summary


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary_map = {str(row["metric"]): row["value"] for row in summary}
    lines = [
        f"# {args.corpus_label} Apocrypha Bridge Context",
        "",
        "Status: surface-context review aid for bridge candidates. This is not a claim report.",
        "",
        "This report keeps all bridge rows and tags whether the hidden term is",
        "centered on the same surface word, a same-concept word, a same-category",
        "word, the center verse, or the start-to-end span.",
        "",
        "## Reproduce",
        "",
        "```bash",
        format_command(args),
        "```",
        "",
        "## Summary",
        "",
        f"- candidate rows: {summary_map.get('candidate_rows', 0)}",
        f"- context rows: {summary_map.get('context_rows', 0)}",
        f"- terms with context rows: {summary_map.get('terms_with_context_rows', 0)}",
    ]
    for bucket in BUCKET_ORDER:
        lines.append(
            f"- {bucket}: {summary_map.get(f'bucket:{bucket}', 0)} "
            f"rows / {summary_map.get(f'terms:{bucket}', 0)} terms"
        )
    lines.extend(
        [
            "",
            "## Highest-Priority Rows",
            "",
            "| Rank | Bucket | Term | Skip | Bridge | Center | Center word | Span refs |",
            "| ---: | --- | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in rows[: args.markdown_row_limit]:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["context_rank"],
                    f"`{row['context_bucket']}`",
                    display_term(row["normalized_term"]),
                    row["skip"],
                    f"`{row['bridge_type']}`",
                    row["center_ref"],
                    display_term(row["center_normalized_word"]),
                    md_cell(truncate(row["span_refs"], 80)),
                ]
            )
            + " |"
        )
    if len(rows) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | {len(rows) - args.markdown_row_limit} more rows in CSV |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `center_word_exact` is the rare direct case: hidden term text is also",
            "  present in the surface word containing the ELS center.",
            "- same-concept and same-category rows are broader review queues, not",
            "  interpretation claims.",
            "- `hidden_path_only` means the bridge exists, but this pass did not find",
            "  declared surface-term support at the center or span level.",
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
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary: list[dict[str, object]],
    started: float,
) -> None:
    manifest = {
        "tool": "analyze_apocrypha_bridge_context",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "args": manifest_args(args),
        "rows": len(rows),
        "summary": summary,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def manifest_args(args: argparse.Namespace) -> dict[str, object]:
    data: dict[str, object] = {}
    for key, value in vars(args).items():
        if key == "terms":
            data[key] = [str(path) for path in value]
        elif isinstance(value, Path):
            data[key] = str(value)
        else:
            data[key] = value
    return data


def format_command(args: argparse.Namespace) -> str:
    parts = [
        "python3 -m scripts.analyze_apocrypha_bridge_context",
        "--corpus-label",
        args.corpus_label,
        "--config",
        str(args.config),
        "--candidates",
        str(args.candidates),
    ]
    for path in args.terms:
        parts.extend(["--terms", str(path)])
    parts.extend(
        [
            "--min-term-length",
            str(args.min_term_length),
            "--out",
            str(args.out),
            "--summary-out",
            str(args.summary_out),
            "--markdown-out",
            str(args.markdown_out),
            "--manifest-out",
            str(args.manifest_out),
        ]
    )
    return " ".join(parts)


if __name__ == "__main__":
    raise SystemExit(main())
