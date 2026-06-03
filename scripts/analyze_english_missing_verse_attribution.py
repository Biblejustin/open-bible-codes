#!/usr/bin/env python3
"""Attribute English version candidate hits to KJV-missing verse gaps."""

from __future__ import annotations

import argparse
import csv
import json
import tomllib
from array import array
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.books import canonical_book_code as _canonical_book
from els.corpus import Corpus, VerseSpan, load_corpus, splice_verses_into_corpus
from els.critical import (
    BrokenHit,
    OmittedBlock,
    TermBreakStats,
    blocks_in_offsets,
    count_insertion_breaks_for_blocks,
    keeps_same_skip,
)
from els.search import normalize_for_corpus
from scripts.run_biblegateway_english_versions import (
    build_generated_configs,
    read_versions,
    resolve_versions,
)


DEFAULT_BASELINE_CONFIG = Path("configs/example_ebible_engkjv.toml")
DEFAULT_VERSIONS = Path("configs/biblegateway_english_versions.csv")
DEFAULT_TERMS = Path("reports/english_version_control_triage/context_seed_terms.csv")
DEFAULT_CONTEXT_HITS = Path("reports/english_version_control_triage/context_hits.csv")
DEFAULT_OUT_DIR = Path("reports/english_missing_verse_attribution")

MIN_SKIP = 2
MAX_SKIP = 100
MIN_TERM_LENGTH = 3
# Labeling set for categorizing reference gaps (ref_gap_category). This is a
# broader, code-form (e.g. 'JHN 8:6') list and is intentionally NOT the same as
# protocols/treat_as_deleted/critical_consensus.csv, which is a narrower,
# name-form study override. Keep the two separate; they serve different roles.
KNOWN_NT_DISPUTED_REFS = {
    "MAT 12:47",
    "MAT 17:21",
    "MAT 18:11",
    "MAT 23:14",
    "MRK 7:16",
    "MRK 9:44",
    "MRK 9:46",
    "MRK 11:26",
    "MRK 15:28",
    "MRK 16:9",
    "MRK 16:10",
    "MRK 16:11",
    "MRK 16:12",
    "MRK 16:13",
    "MRK 16:14",
    "MRK 16:15",
    "MRK 16:16",
    "MRK 16:17",
    "MRK 16:18",
    "MRK 16:19",
    "MRK 16:20",
    "LUK 17:36",
    "LUK 22:43",
    "LUK 22:44",
    "LUK 23:17",
    "JHN 5:4",
    "JHN 7:53",
    "JHN 8:1",
    "JHN 8:2",
    "JHN 8:3",
    "JHN 8:4",
    "JHN 8:5",
    "JHN 8:6",
    "JHN 8:7",
    "JHN 8:8",
    "JHN 8:9",
    "JHN 8:10",
    "JHN 8:11",
    "ACT 8:37",
    "ACT 15:34",
    "ACT 24:7",
    "ACT 28:29",
    "ROM 16:24",
    "1JN 5:7",
}

SUMMARY_FIELDNAMES = [
    "version_label",
    "version_name",
    "coverage",
    "source_family",
    "basis_status",
    "version_letters",
    "version_verses",
    "missing_kjv_refs",
    "missing_kjv_letters",
    "known_nt_disputed_kjv_refs",
    "other_reference_gaps",
    "seed_term_rows",
    "total_seed_hits",
    "hits_spanning_inserted_kjv_refs",
    "missing_verse_attributed_hits",
    "preserved_across_insertions",
    "result",
]
MISSING_REF_FIELDNAMES = [
    "version_label",
    "version_name",
    "ref",
    "book",
    "chapter",
    "verse",
    "kjv_norm_start",
    "kjv_norm_end",
    "kjv_norm_length",
    "ref_gap_category",
]
BROKEN_FIELDNAMES = [
    "version_label",
    "version_name",
    "term_source",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "span_letters",
    "start_ref",
    "end_ref",
    "center_ref",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "break_type",
    "omitted_refs_in_span",
    "omitted_refs_with_sequence_letters",
]
CONTEXT_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "start_ref",
    "end_ref",
    "center_ref",
    "best_context",
    "missing_refs_in_augmented_span",
    "missing_verse_attribution",
]


def main() -> int:
    args = build_parser().parse_args()
    started = datetime.now(UTC)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    baseline = load_corpus(args.baseline_config)
    versions = read_versions(args.versions)
    included, missing = resolve_versions(versions, args)
    if args.max_versions is not None:
        included = included[: args.max_versions]
    generated_configs = build_generated_configs(included, args.out_dir)
    terms = read_terms(args.terms)
    if args.max_terms is not None:
        terms = terms[: args.max_terms]

    summary_rows: list[dict[str, object]] = []
    missing_ref_rows: list[dict[str, object]] = []
    broken_rows: list[dict[str, object]] = []
    context_rows = read_csv_rows(args.context_hits) if args.context_hits.exists() else []
    context_by_version: dict[str, list[dict[str, str]]] = {}
    for row in context_rows:
        context_by_version.setdefault(row.get("corpus", ""), []).append(row)
    context_attribution_rows: list[dict[str, object]] = []

    for version_row in included:
        label = version_row["label"]
        config_path = Path(generated_configs[label])
        target_keys, version_verse_count = target_verse_keys_from_config(config_path)
        missing_verses = missing_baseline_verses(baseline, target_keys)
        donor_refs = [verse.ref for verse in missing_verses]
        version_context_rows = context_by_version.get(label, [])
        needs_augmented_corpus = args.full_seed_scan or bool(version_context_rows)
        corpus: Corpus | None = None
        augmented: Corpus | None = None
        inserted_blocks: list[OmittedBlock] = []
        if needs_augmented_corpus:
            corpus = load_corpus(config_path, use_cache=False)
            augmented = splice_verses_into_corpus(corpus, baseline, donor_refs)
            inserted_blocks = inserted_blocks_from_augmented(augmented, donor_refs)

        for verse in missing_verses:
            missing_ref_rows.append(
                {
                    "version_label": label,
                    "version_name": version_row.get("name", ""),
                    "ref": verse.ref,
                    "book": verse.book,
                    "chapter": verse.chapter,
                    "verse": verse.verse,
                    "kjv_norm_start": verse.norm_start,
                    "kjv_norm_end": verse.norm_end,
                    "kjv_norm_length": verse.norm_length,
                    "ref_gap_category": ref_gap_category(verse.ref),
                }
            )

        term_stats: list[TermBreakStats] | None = None
        broken: list[BrokenHit] = []
        if args.full_seed_scan:
            if augmented is None:
                if corpus is None:
                    corpus = load_corpus(config_path, use_cache=False)
                augmented = splice_verses_into_corpus(corpus, baseline, donor_refs)
                inserted_blocks = inserted_blocks_from_augmented(augmented, donor_refs)
            term_stats, stats_by_query = build_stats_by_query(
                corpus,
                [dict(row) for row in terms],
                min_term_length=args.min_term_length,
            )
            _total, _per_block, broken = count_insertion_breaks_for_blocks(
                corpus,
                augmented,
                stats_by_query,
                inserted_blocks,
                min_skip=args.min_skip,
                max_skip=args.max_skip,
                direction=args.direction,
            )
            for row in broken_rows_for_version(version_row, broken):
                broken_rows.append(row)

        summary_rows.append(
            summary_row_for_version(
                version_row,
                corpus,
                missing_verses,
                term_stats,
                version_verse_count=version_verse_count,
                seed_term_rows=len(terms),
                seed_scan_run=args.full_seed_scan,
                missing_verse_attributed_hits=len(broken),
            )
        )

        for context_row in version_context_rows:
            if augmented is None:
                if corpus is None:
                    corpus = load_corpus(config_path, use_cache=False)
                augmented = splice_verses_into_corpus(corpus, baseline, donor_refs)
                inserted_blocks = inserted_blocks_from_augmented(augmented, donor_refs)
            context_attribution_rows.append(
                context_attribution_for_row(
                    context_row,
                    corpus,
                    augmented,
                    inserted_blocks,
                )
            )

    summary_path = args.out_dir / "summary.csv"
    missing_refs_path = args.out_dir / "missing_refs.csv"
    broken_path = args.out_dir / "missing_verse_attributed_hits.csv"
    context_path = args.out_dir / "context_hit_attribution.csv"
    manifest_path = args.out_dir / "manifest.json"
    markdown_path = args.out_dir / "summary.md"

    write_rows(summary_path, summary_rows, SUMMARY_FIELDNAMES)
    write_rows(missing_refs_path, missing_ref_rows, MISSING_REF_FIELDNAMES)
    write_rows(broken_path, broken_rows, BROKEN_FIELDNAMES)
    write_rows(context_path, context_attribution_rows, CONTEXT_FIELDNAMES)
    write_markdown(
        markdown_path,
        summary_rows,
        context_attribution_rows,
        broken_rows,
        missing,
        full_seed_scan=args.full_seed_scan,
    )
    write_manifest(
        manifest_path,
        args,
        baseline,
        included,
        missing,
        terms,
        summary_rows,
        broken_rows,
        context_attribution_rows,
        started,
    )

    print(summary_path)
    print(missing_refs_path)
    print(broken_path)
    print(context_path)
    print(markdown_path)
    print(manifest_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-config", type=Path, default=DEFAULT_BASELINE_CONFIG)
    parser.add_argument("--versions", type=Path, default=DEFAULT_VERSIONS)
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--context-hits", type=Path, default=DEFAULT_CONTEXT_HITS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--min-skip", type=int, default=MIN_SKIP)
    parser.add_argument("--max-skip", type=int, default=MAX_SKIP)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=MIN_TERM_LENGTH)
    parser.add_argument("--max-versions", type=int)
    parser.add_argument("--max-terms", type=int)
    parser.add_argument(
        "--full-seed-scan",
        action="store_true",
        help="Also rescan every seed term in every version. Slow; default only attributes existing context rows.",
    )
    return parser


def read_terms(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("language") != "english":
                continue
            copied = dict(row)
            copied["term_source"] = str(path)
            rows.append(copied)
    return rows


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def target_verse_keys_from_config(config_path: Path) -> tuple[set[tuple[str, str, str]], int]:
    with config_path.open("rb") as handle:
        config = tomllib.load(handle)
    keys: set[tuple[str, str, str]] = set()
    row_count = 0
    for source_config in config.get("sources", []):
        if source_config.get("format") != "csv":
            raise ValueError(f"unsupported source format for ref-only scan: {config_path}")
        source_path = Path(source_config["path"]).expanduser()
        if not source_path.is_absolute():
            source_path = config_path.parent / source_path
        ref_column = source_config.get("ref_column", "ref")
        book_column = source_config.get("book_column", "book")
        chapter_column = source_config.get("chapter_column", "chapter")
        verse_column = source_config.get("verse_column", "verse")
        with source_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                row_count += 1
                keys.add(
                    verse_key_from_parts(
                        row.get(book_column, ""),
                        row.get(chapter_column, ""),
                        row.get(verse_column, ""),
                        row.get(ref_column, ""),
                    )
                )
    return keys, row_count


def build_stats_by_query(
    corpus: Corpus,
    terms: list[dict[str, str]],
    *,
    min_term_length: int,
) -> tuple[list[TermBreakStats], dict[str, list[TermBreakStats]]]:
    term_stats: list[TermBreakStats] = []
    stats_by_query: dict[str, list[TermBreakStats]] = {}
    for term_row in terms:
        term_row["_order"] = str(len(term_stats))
        normalized = normalize_for_corpus(corpus, term_row["term"])
        if len(normalized) < min_term_length:
            term_stats.append(
                TermBreakStats(
                    order=len(term_stats),
                    term_row=term_row,
                    normalized=normalized,
                    status="skipped_short_term",
                )
            )
            continue
        stats = TermBreakStats(order=len(term_stats), term_row=term_row, normalized=normalized)
        term_stats.append(stats)
        stats_by_query.setdefault(normalized, []).append(stats)
    return term_stats, stats_by_query


def verse_key(verse: VerseSpan) -> tuple[str, str, str]:
    return (_canonical_book(verse.book), verse.chapter, verse.verse)


def verse_key_from_parts(book: str, chapter: str, verse: str, ref: str) -> tuple[str, str, str]:
    if book and chapter and verse:
        return (_canonical_book(book), chapter, verse)
    ref_parts = ref.split()
    if len(ref_parts) == 2 and ":" in ref_parts[1]:
        chapter_part, verse_part = ref_parts[1].split(":", 1)
        return (_canonical_book(ref_parts[0]), chapter_part, verse_part)
    return (_canonical_book(book or ref), chapter, verse)



def missing_baseline_verses(
    baseline: Corpus,
    target: Corpus | set[tuple[str, str, str]],
) -> list[VerseSpan]:
    target_keys = target if isinstance(target, set) else {verse_key(verse) for verse in target.verses}
    return [verse for verse in baseline.verses if verse_key(verse) not in target_keys]


def inserted_blocks_from_augmented(augmented: Corpus, donor_refs: list[str]) -> list[OmittedBlock]:
    donor_ref_set = set(donor_refs)
    return [
        OmittedBlock(
            ref=verse.ref,
            start=verse.norm_start,
            end=verse.norm_end,
            length=verse.norm_length,
            status="inserted_kjv_missing_ref",
            used_as_deletion=True,
        )
        for verse in augmented.verses
        if verse.ref in donor_ref_set
    ]


def ref_gap_category(ref: str) -> str:
    if ref in KNOWN_NT_DISPUTED_REFS:
        return "known_nt_disputed_kjv_ref"
    return "other_reference_gap"


def broken_rows_for_version(
    version_row: dict[str, str],
    broken: list[BrokenHit],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in broken:
        row = {
            "version_label": version_row.get("label", ""),
            "version_name": version_row.get("name", ""),
        }
        row.update(record.as_row())
        rows.append(row)
    return rows


def summary_row_for_version(
    version_row: dict[str, str],
    corpus: Corpus | None,
    missing_verses: list[VerseSpan],
    term_stats: list[TermBreakStats] | None,
    *,
    version_verse_count: int,
    seed_term_rows: int,
    seed_scan_run: bool,
    missing_verse_attributed_hits: int,
) -> dict[str, object]:
    if term_stats is None:
        total_hits: int | str = ""
        span_hits: int | str = ""
        preserved: int | str = ""
    else:
        total_hits = sum(stats.total_hits for stats in term_stats)
        span_hits = sum(stats.span_intersect_hits for stats in term_stats)
        preserved = sum(stats.preserved_across_omission_hits for stats in term_stats)
    if not seed_scan_run:
        result = "seed_scan_not_run"
    elif missing_verse_attributed_hits:
        result = "missing_verse_attributed_seed_hits"
    elif total_hits:
        result = "seed_hits_not_missing_verse_attributed"
    else:
        result = "no_seed_hits"
    return {
        "version_label": version_row.get("label", ""),
        "version_name": version_row.get("name", ""),
        "coverage": version_row.get("coverage", ""),
        "source_family": version_row.get("source_family", ""),
        "basis_status": version_row.get("basis_status", ""),
        "version_letters": len(corpus.text) if corpus is not None else "",
        "version_verses": len(corpus.verses) if corpus is not None else version_verse_count,
        "missing_kjv_refs": len(missing_verses),
        "missing_kjv_letters": sum(verse.norm_length for verse in missing_verses),
        "known_nt_disputed_kjv_refs": sum(
            ref_gap_category(verse.ref) == "known_nt_disputed_kjv_ref"
            for verse in missing_verses
        ),
        "other_reference_gaps": sum(
            ref_gap_category(verse.ref) == "other_reference_gap" for verse in missing_verses
        ),
        "seed_term_rows": seed_term_rows,
        "total_seed_hits": total_hits,
        "hits_spanning_inserted_kjv_refs": span_hits,
        "missing_verse_attributed_hits": missing_verse_attributed_hits,
        "preserved_across_insertions": preserved,
        "result": result,
    }


def context_attribution_for_row(
    context_row: dict[str, str],
    corpus: Corpus,
    augmented: Corpus,
    inserted_blocks: list[OmittedBlock],
) -> dict[str, object]:
    start = int(context_row["start_offset"])
    skip = int(context_row["skip"])
    normalized = context_row["normalized_term"]
    attribution, refs = hit_missing_verse_attribution(
        corpus,
        augmented,
        inserted_blocks,
        start=start,
        skip=skip,
        normalized_length=len(normalized),
    )
    return {
        "corpus": context_row.get("corpus", ""),
        "term_id": context_row.get("term_id", ""),
        "concept": context_row.get("concept", ""),
        "term": context_row.get("term", ""),
        "normalized_term": normalized,
        "skip": skip,
        "direction": context_row.get("direction", ""),
        "start_offset": start,
        "end_offset": context_row.get("end_offset", ""),
        "start_ref": context_row.get("start_ref", ""),
        "end_ref": context_row.get("end_ref", ""),
        "center_ref": context_row.get("center_ref", ""),
        "best_context": context_row.get("best_context", ""),
        "missing_refs_in_augmented_span": ";".join(refs),
        "missing_verse_attribution": attribution,
    }


def hit_missing_verse_attribution(
    base: Corpus,
    augmented: Corpus,
    inserted_blocks: list[OmittedBlock],
    *,
    start: int,
    skip: int,
    normalized_length: int,
) -> tuple[str, list[str]]:
    if not inserted_blocks:
        return "no_missing_kjv_refs_for_version", []
    augmented_by_ref = {verse.ref: verse for verse in augmented.verses}

    def augmented_position(position: int) -> int | None:
        verse = base.verses[base.position_to_verse[position]]
        augmented_verse = augmented_by_ref.get(verse.ref)
        if augmented_verse is None:
            return None
        return augmented_verse.norm_start + (position - verse.norm_start)

    positions = [start + index * skip for index in range(normalized_length)]
    if any(position < 0 or position >= len(base.text) for position in positions):
        return "hit_offsets_out_of_range", []
    mapped = [augmented_position(position) for position in positions]
    if any(position is None for position in mapped):
        return "base_ref_absent_from_augmented", []
    augmented_positions = [int(position) for position in mapped]
    span_blocks = blocks_in_offsets(min(augmented_positions), max(augmented_positions), inserted_blocks)
    refs = [block.ref for block in span_blocks]
    if not span_blocks:
        return "not_missing_verse_related", refs
    if keeps_same_skip(augmented_positions, skip):
        return "crosses_inserted_refs_but_spacing_preserved", refs
    return "missing_verse_attributed", refs


def write_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, object]],
    context_rows: list[dict[str, object]],
    broken_rows: list[dict[str, object]],
    missing_versions: list[dict[str, str]],
    *,
    full_seed_scan: bool,
) -> None:
    def int_or_zero(value: object) -> int:
        if value == "":
            return 0
        return int(value)

    available = len(summary_rows)
    with_missing = sum(int_or_zero(row["missing_kjv_refs"]) > 0 for row in summary_rows)
    total_ref_gaps = sum(int_or_zero(row["missing_kjv_refs"]) for row in summary_rows)
    total_known_disputed = sum(
        int_or_zero(row["known_nt_disputed_kjv_refs"]) for row in summary_rows
    )
    versions_with_known_disputed = sum(
        int_or_zero(row["known_nt_disputed_kjv_refs"]) > 0 for row in summary_rows
    )
    attributed_versions = [
        row for row in summary_rows if int_or_zero(row["missing_verse_attributed_hits"]) > 0
    ]
    total_attributed = sum(int_or_zero(row["missing_verse_attributed_hits"]) for row in summary_rows)
    context_attributed = [
        row for row in context_rows if row["missing_verse_attribution"] == "missing_verse_attributed"
    ]
    seed_scan_status = "run" if full_seed_scan else "not run; existing context-review rows only"
    seed_result = (
        f"- Missing-verse-attributed seed hits: {total_attributed}."
        if full_seed_scan
        else "- Missing-verse-attributed seed hits: not computed in fast mode."
    )
    lines = [
        "# English Missing-Verse Attribution",
        "",
        "This report tests whether English version seed hits are explained by KJV",
        "verse references that are absent from a compared English version.",
        "",
        "## Scope",
        "",
        f"- Available BibleGateway-overlap English versions checked: {available}.",
        f"- Missing BibleGateway versions skipped: {len(missing_versions)}.",
        f"- Versions with at least one KJV ref absent: {with_missing}.",
        f"- Reference-gap rows: {total_ref_gaps}.",
        f"- Known NT disputed KJV-ref rows: {total_known_disputed} across "
        f"{versions_with_known_disputed} versions.",
        "- Terms checked: English version-control seed terms.",
        "- Method: splice absent KJV verse refs back into each version, then test",
        "  whether the version's existing seed ELS hits keep the same skip.",
        f"- Full seed rescan: {seed_scan_status}.",
        "",
        "## Result",
        "",
        seed_result,
        f"- Context-review rows attributed to missing verses: {len(context_attributed)}.",
        "- Current reviewed English hits are not in spans crossing those absent",
        "  KJV refs, so the current reviewed differences point to translation",
        "  wording/spacing or ordinary background, not a missing-verse gap.",
    ]
    if attributed_versions:
        lines.extend(
            [
                "",
                "| Version | Missing KJV refs | Attributed seed hits |",
                "| --- | ---: | ---: |",
            ]
        )
        for row in attributed_versions:
            lines.append(
                f"| {row['version_label']} | {row['missing_kjv_refs']} | "
                f"{row['missing_verse_attributed_hits']} |"
            )
    else:
        seed_no_hit_text = (
            "No current English seed hit is attributed to KJV-missing verse gaps."
            if full_seed_scan
            else "Full seed-hit attribution was not run in this fast report."
        )
        lines.extend(
            [
                "",
                seed_no_hit_text,
            ]
        )
    lines.extend(
        [
            "",
            "## Context-Hit Attribution",
            "",
            "| Corpus | Term | Span | Attribution | Missing refs in augmented span |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in context_rows:
        span = f"{row['start_ref']} -> {row['end_ref']}"
        refs = row["missing_refs_in_augmented_span"] or ""
        lines.append(
            f"| {row['corpus']} | `{row['normalized_term']}` | {span} | "
            f"`{row['missing_verse_attribution']}` | {refs} |"
        )
    if not context_rows:
        lines.append("| none | none | none | none | none |")
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `reports/english_missing_verse_attribution/summary.csv`",
            "- `reports/english_missing_verse_attribution/missing_refs.csv`",
            "- `reports/english_missing_verse_attribution/missing_verse_attributed_hits.csv`",
            "- `reports/english_missing_verse_attribution/context_hit_attribution.csv`",
            "- `reports/english_missing_verse_attribution/manifest.json`",
            "",
            "## Cautions",
            "",
            "- This is an attribution test for the current English seed rows, not a new",
            "  claim search.",
            "- A row not attributed to missing verses may still differ because of",
            "  translation wording, word order, paraphrase style, canon coverage, or",
            "  ordinary ELS background.",
            "- Missing KJV refs are reference-level differences. This does not classify",
            "  every smaller wording change inside shared verses.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    baseline: Corpus,
    included: list[dict[str, str]],
    missing: list[dict[str, str]],
    terms: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    broken_rows: list[dict[str, object]],
    context_rows: list[dict[str, object]],
    started: datetime,
) -> None:
    path.write_text(
        json.dumps(
            {
                "tool": "english_missing_verse_attribution",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "started_utc": started.isoformat(),
                "baseline_config": str(args.baseline_config.resolve()),
                "versions": str(args.versions.resolve()),
                "terms": str(args.terms.resolve()),
                "context_hits": str(args.context_hits.resolve()),
                "baseline_letters": len(baseline.text),
                "baseline_verses": len(baseline.verses),
                "included_versions": len(included),
                "missing_versions": len(missing),
                "term_rows": len(terms),
                "versions_with_missing_kjv_refs": sum(
                    int(row["missing_kjv_refs"]) > 0 for row in summary_rows
                ),
                "known_nt_disputed_kjv_ref_rows": sum(
                    int(row["known_nt_disputed_kjv_refs"]) for row in summary_rows
                ),
                "versions_with_known_nt_disputed_kjv_refs": sum(
                    int(row["known_nt_disputed_kjv_refs"]) > 0 for row in summary_rows
                ),
                "other_reference_gap_rows": sum(
                    int(row["other_reference_gaps"]) for row in summary_rows
                ),
                "missing_verse_attributed_hits": len(broken_rows),
                "context_hit_rows": len(context_rows),
                "context_missing_verse_attributed_rows": sum(
                    row["missing_verse_attribution"] == "missing_verse_attributed"
                    for row in context_rows
                ),
                "full_seed_scan": args.full_seed_scan,
                "min_skip": args.min_skip,
                "max_skip": args.max_skip,
                "direction": args.direction,
                "method": "splice_missing_kjv_refs_into_version_and_check_skip_preservation",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _toy_corpus(name: str, verse_lengths: list[tuple[str, int]]) -> Corpus:
    verses: list[VerseSpan] = []
    letters: list[str] = []
    position_to_verse: list[int] = []
    for index, (ref, length) in enumerate(verse_lengths):
        start = len(letters)
        letters.extend("a" * length)
        position_to_verse.extend([index] * length)
        book, chapter_verse = ref.split()
        chapter, verse = chapter_verse.split(":")
        verses.append(
            VerseSpan(
                source=name,
                ref=ref,
                book=book,
                chapter=chapter,
                verse=verse,
                raw_text="a" * length,
                norm_start=start,
                norm_end=len(letters) - 1,
                norm_length=length,
            )
        )
    return Corpus(
        name=name,
        language="english",
        keep_hebrew_final_forms=False,
        text="".join(letters),
        verses=tuple(verses),
        position_to_verse=array("i", position_to_verse),
    )


if __name__ == "__main__":
    raise SystemExit(main())
