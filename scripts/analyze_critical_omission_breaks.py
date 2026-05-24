#!/usr/bin/env python3
"""Find TR ELS hits broken by verse blocks absent from a critical text."""

from __future__ import annotations

import csv
import json
import argparse
from datetime import UTC, datetime
from pathlib import Path

from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.critical import (
    BrokenHit,
    OmittedBlock,
    TermBreakStats,
    blocks_in_offsets,
    classify_missing_verses,
    count_breaks_for_blocks,
)
from els.search import (
    iter_els_query_matches_by_lanes,
    normalize_for_corpus,
)


TR_CONFIG = Path("configs/example_ebible_grctr.toml")
CRITICAL_CONFIG = Path("configs/example_sblgnt.toml")
TERM_PATHS = [
    Path("terms/theological_terms.csv"),
    Path("terms/modern_names_dates.csv"),
    Path("terms/table_of_nations.csv"),
    Path("terms/prophetic_terms.csv"),
]
SUMMARY_OUT = Path("reports/critical_omission_breaks_summary.csv")
EXAMPLES_OUT = Path("reports/critical_omission_breaks_examples.csv")
VERSES_OUT = Path("reports/critical_omission_breaks_by_verse.csv")
MISSING_VERSES_OUT = Path("reports/critical_omission_missing_verses.csv")
MANIFEST_OUT = Path("reports/critical_omission_breaks.manifest.json")

MIN_SKIP = 2
MAX_SKIP = 50
MIN_TERM_LENGTH = 3


def main() -> int:
    args = build_parser().parse_args()
    tr = load_corpus(args.tr_config)
    critical = load_corpus(args.critical_config)
    extra_deleted_refs, passage_refs, partial_deleted_refs = read_treat_as_deleted_refs(args.treat_as_deleted)
    omitted_blocks = classify_missing_verses(
        tr,
        critical,
        extra_deleted_refs=extra_deleted_refs,
    )
    omitted_blocks.extend(build_partial_deleted_blocks(tr, partial_deleted_refs))
    deleted_blocks = [block for block in omitted_blocks if block.used_as_deletion]
    term_paths = term_paths_for_args(args)
    terms = read_greek_terms(term_paths, tr)
    if args.max_terms is not None:
        terms = terms[: args.max_terms]
    output_paths = output_paths_for_suffix(args.out_suffix)

    write_rows(output_paths["missing"], [block.__dict__ for block in omitted_blocks])

    by_verse = {
        block.ref: {
            "omitted_ref": block.ref,
            "norm_start": block.start,
            "norm_end": block.end,
            "norm_length": block.length,
            "span_intersect_hits": 0,
            "broken_removed_letter_hits": 0,
            "broken_spacing_hits": 0,
            "broken_total_hits": 0,
        }
        for block in deleted_blocks
    }

    term_stats, stats_by_query = build_stats_by_query(tr, terms)
    matches = list(
        iter_els_query_matches_by_lanes(
            tr.text,
            stats_by_query,
            min_skip=MIN_SKIP,
            max_skip=MAX_SKIP,
            direction="both",
        )
    )
    span_intersects = count_span_intersects_by_block(tr, stats_by_query, deleted_blocks, matches=matches)
    for block in deleted_blocks:
        by_verse[block.ref]["span_intersect_hits"] = span_intersects.get(block.ref, 0)
    _total_breaks, _per_block_breaks, broken_hit_records = count_breaks_for_blocks(
        tr,
        stats_by_query,
        deleted_blocks,
        min_skip=MIN_SKIP,
        max_skip=MAX_SKIP,
        direction="both",
        matches=matches,
    )
    for record in broken_hit_records:
        if record.break_type == "broken_removed_letter":
            for block in record.removed_blocks:
                by_verse[block.ref]["broken_removed_letter_hits"] += 1
                by_verse[block.ref]["broken_total_hits"] += 1
        elif record.break_type == "broken_spacing":
            for block in record.span_blocks:
                by_verse[block.ref]["broken_spacing_hits"] += 1
                by_verse[block.ref]["broken_total_hits"] += 1

    summary_rows = summary_rows_from_stats(term_stats)

    example_rows = [
        record.as_row()
        for record in sorted(broken_hit_records, key=broken_hit_sort_key)
    ]
    write_rows(output_paths["summary"], summary_rows)
    write_rows(output_paths["examples"], example_rows)
    write_rows(output_paths["by_verse"], list(by_verse.values()))
    write_manifest(
        output_paths["manifest"],
        tr,
        critical,
        omitted_blocks,
        terms,
        len(example_rows),
        term_paths,
        args,
    )
    if passage_refs:
        write_passage_outputs(
            output_paths,
            passage_refs,
            example_rows,
            by_verse,
            tr,
            deleted_blocks,
            stats_by_query,
            matches,
        )

    print(output_paths["summary"])
    print(output_paths["examples"])
    print(output_paths["by_verse"])
    print(output_paths["missing"])
    print(output_paths["manifest"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tr-config", type=Path, default=TR_CONFIG)
    parser.add_argument("--critical-config", type=Path, default=CRITICAL_CONFIG)
    parser.add_argument("--treat-as-deleted", type=Path)
    parser.add_argument("--no-default-terms", action="store_true")
    parser.add_argument("--extra-terms", type=Path, action="append", default=[])
    parser.add_argument("--out-suffix", default="")
    parser.add_argument("--max-terms", type=int, help="Test helper: limit term rows before building queries.")
    return parser


def term_paths_for_args(args: argparse.Namespace) -> list[Path]:
    paths = [] if args.no_default_terms else list(TERM_PATHS)
    return paths + list(args.extra_terms)


def output_paths_for_suffix(suffix: str) -> dict[str, Path]:
    if not suffix:
        return {
            "summary": SUMMARY_OUT,
            "examples": EXAMPLES_OUT,
            "by_verse": VERSES_OUT,
            "missing": MISSING_VERSES_OUT,
            "manifest": MANIFEST_OUT,
        }
    return {
        "summary": Path(f"reports/critical_omission_breaks{suffix}_summary.csv"),
        "examples": Path(f"reports/critical_omission_breaks{suffix}_examples.csv"),
        "by_verse": Path(f"reports/critical_omission_breaks{suffix}_by_verse.csv"),
        "missing": Path(f"reports/critical_omission_missing_verses{suffix}.csv"),
        "manifest": Path(f"reports/critical_omission_breaks{suffix}.manifest.json"),
    }


def read_treat_as_deleted_refs(
    path: Path | None,
) -> tuple[set[str] | None, dict[str, set[str]], list[dict[str, str]]]:
    if path is None:
        return None, {}, []
    refs: set[str] = set()
    passage_refs: dict[str, set[str]] = {}
    partial_refs: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            ref = row.get("ref", "").strip()
            if not ref:
                continue
            normalized_ref = normalize_ref_label(ref)
            passage = row.get("passage", "").strip() or "override"
            if row.get("normalized_subspan", "").strip():
                partial_refs.append(
                    {
                        "ref": normalized_ref,
                        "base_ref": normalize_ref_label(partial_ref_base(ref)),
                        "passage": passage,
                        "normalized_subspan": row["normalized_subspan"].strip(),
                    }
                )
            else:
                refs.add(normalized_ref)
            passage_refs.setdefault(passage, set()).add(normalized_ref)
    return refs, passage_refs, partial_refs


def build_partial_deleted_blocks(corpus: Corpus, partial_refs: list[dict[str, str]]) -> list[OmittedBlock]:
    verses_by_ref = {verse.ref: verse for verse in corpus.verses}
    blocks: list[OmittedBlock] = []
    for spec in partial_refs:
        verse = verses_by_ref.get(spec["base_ref"])
        if verse is None:
            raise RuntimeError(f"partial override base ref not found: {spec['base_ref']}")
        normalized_verse = normalize_for_corpus(corpus, verse.raw_text)
        subspan = spec["normalized_subspan"]
        start_local = normalized_verse.find(subspan)
        if start_local < 0:
            raise RuntimeError(f"partial override subspan not found: {spec['ref']}")
        start = verse.norm_start + start_local
        end = start + len(subspan) - 1
        blocks.append(
            OmittedBlock(
                ref=spec["ref"],
                start=start,
                end=end,
                length=len(subspan),
                status="explicit_deleted_partial_ref",
                used_as_deletion=True,
            )
        )
    return blocks


def partial_ref_base(ref: str) -> str:
    return ref.rstrip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def normalize_ref_label(ref: str) -> str:
    parts = ref.strip().split()
    if len(parts) == 3 and parts[0].isdigit():
        book = f"{parts[0]} {parts[1]}"
        chapter_verse = parts[2]
    elif len(parts) == 2:
        book, chapter_verse = parts
    else:
        return ref
    book_code = {
        "Matthew": "MAT",
        "Mark": "MRK",
        "Luke": "LUK",
        "John": "JHN",
        "Acts": "ACT",
        "Romans": "ROM",
        "1 Corinthians": "1CO",
        "2 Corinthians": "2CO",
        "Galatians": "GAL",
        "Ephesians": "EPH",
        "Philippians": "PHP",
        "Colossians": "COL",
        "1 Thessalonians": "1TH",
        "2 Thessalonians": "2TH",
        "1 Timothy": "1TI",
        "2 Timothy": "2TI",
        "Titus": "TIT",
        "Philemon": "PHM",
        "Hebrews": "HEB",
        "James": "JAS",
        "1 Peter": "1PE",
        "2 Peter": "2PE",
        "1 John": "1JN",
        "2 John": "2JN",
        "3 John": "3JN",
        "Jude": "JUD",
        "Revelation": "REV",
    }.get(book, book)
    return f"{book_code} {chapter_verse}"


def build_stats_by_query(
    corpus: Corpus,
    terms: list[dict[str, str]],
) -> tuple[list[TermBreakStats], dict[str, list[TermBreakStats]]]:
    term_stats: list[TermBreakStats] = []
    stats_by_query: dict[str, list[TermBreakStats]] = {}
    for term_row in terms:
        term_row["_order"] = str(len(term_stats))
        normalized = normalize_for_corpus(corpus, term_row["term"])
        if len(normalized) < MIN_TERM_LENGTH:
            term_stats.append(
                TermBreakStats(
                    order=len(term_stats),
                    term_row=term_row,
                    normalized=normalized,
                    status="skipped_short_term",
                )
            )
            continue

        stats = TermBreakStats(
            order=len(term_stats),
            term_row=term_row,
            normalized=normalized,
        )
        term_stats.append(stats)
        stats_by_query.setdefault(normalized, []).append(stats)
    return term_stats, stats_by_query


def read_greek_terms(paths: list[Path], corpus: Corpus) -> list[dict[str, str]]:
    languages = accepted_term_languages(corpus.language)
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("language") not in languages:
                    continue
                key = (str(path), row.get("term_id", ""))
                if key in seen:
                    continue
                seen.add(key)
                row = dict(row)
                row["term_source"] = str(path)
                rows.append(row)
    return rows


def count_span_intersects_by_block(
    corpus: Corpus,
    stats_by_query: dict[str, list[TermBreakStats]],
    blocks: list[OmittedBlock],
    *,
    matches: list[tuple[str, int, int, int]] | None = None,
) -> dict[str, int]:
    counts = {block.ref: 0 for block in blocks}
    match_iter = matches
    if match_iter is None:
        match_iter = list(
            iter_els_query_matches_by_lanes(
                corpus.text,
                stats_by_query,
                min_skip=MIN_SKIP,
                max_skip=MAX_SKIP,
                direction="both",
            )
        )
    for normalized, _skip, start, end in match_iter:
        multiplier = len(stats_by_query[normalized])
        for block in blocks_in_offsets(start, end, blocks):
            counts[block.ref] += multiplier
    return counts


def broken_hit_sort_key(record: BrokenHit) -> tuple[int, int, int, int, int]:
    direction_order = 0 if record.hit.skip > 0 else 1
    low, high = sorted((record.hit.start_offset, record.hit.end_offset))
    order = int(record.term_row.get("_order", "0"))
    return order, abs(record.hit.skip), direction_order, low, high


def write_passage_outputs(
    output_paths: dict[str, Path],
    passage_refs: dict[str, set[str]],
    example_rows: list[dict[str, object]],
    by_verse: dict[str, dict[str, object]],
    corpus: Corpus,
    deleted_blocks: list[OmittedBlock],
    stats_by_query: dict[str, list[TermBreakStats]],
    matches: list[tuple[str, int, int, int]],
) -> None:
    suffix_base = output_paths["summary"].name.removeprefix("critical_omission_breaks").removesuffix("_summary.csv")
    for passage, refs in passage_refs.items():
        slug = passage_slug(passage)
        prefix = Path("reports") / f"critical_omission_breaks_treat_as_deleted_{slug}{suffix_base}"
        passage_blocks = [block for block in deleted_blocks if block.ref in refs]
        passage_examples = [
            row
            for row in example_rows
            if refs & set(str(row.get("omitted_refs_in_span", "")).split(";"))
        ]
        passage_summary = passage_summary_rows_for_blocks(corpus, stats_by_query, passage_blocks, matches)
        passage_by_verse = [row for ref, row in by_verse.items() if ref in refs]
        write_rows(prefix.with_name(prefix.name + "_summary.csv"), passage_summary)
        write_rows(prefix.with_name(prefix.name + "_examples.csv"), passage_examples)
        write_rows(prefix.with_name(prefix.name + "_by_verse.csv"), passage_by_verse)


def passage_summary_rows_for_blocks(
    corpus: Corpus,
    stats_by_query: dict[str, list[TermBreakStats]],
    blocks: list[OmittedBlock],
    matches: list[tuple[str, int, int, int]],
) -> list[dict[str, object]]:
    term_stats, scoped_stats_by_query = clone_stats_by_query(stats_by_query)
    count_breaks_for_blocks(
        corpus,
        scoped_stats_by_query,
        blocks,
        min_skip=MIN_SKIP,
        max_skip=MAX_SKIP,
        direction="both",
        matches=matches,
        collect_broken_hits=False,
    )
    return summary_rows_from_stats(term_stats, broken_only=True)


def clone_stats_by_query(
    stats_by_query: dict[str, list[TermBreakStats]],
) -> tuple[list[TermBreakStats], dict[str, list[TermBreakStats]]]:
    term_stats: list[TermBreakStats] = []
    cloned_by_query: dict[str, list[TermBreakStats]] = {}
    for normalized, stats_list in stats_by_query.items():
        for stats in stats_list:
            cloned = TermBreakStats(
                order=stats.order,
                term_row=stats.term_row,
                normalized=stats.normalized,
                status=stats.status,
            )
            term_stats.append(cloned)
            cloned_by_query.setdefault(normalized, []).append(cloned)
    return sorted(term_stats, key=lambda stats: stats.order), cloned_by_query


def summary_rows_from_stats(
    term_stats: list[TermBreakStats],
    *,
    broken_only: bool = False,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for stats in term_stats:
        if broken_only and not (stats.broken_removed_letter_hits or stats.broken_spacing_hits):
            continue
        rows.append(
            summary_row(
                stats.term_row,
                stats.normalized,
                stats.total_hits,
                stats.span_intersect_hits,
                stats.broken_removed_letter_hits,
                stats.broken_spacing_hits,
                stats.preserved_across_omission_hits,
                stats.status,
            )
        )
    return rows


def passage_slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def summary_row(
    term_row: dict[str, str],
    normalized: str,
    total_hits: int,
    span_intersect_hits: int,
    broken_removed_letter_hits: int,
    broken_spacing_hits: int,
    preserved_across_omission_hits: int,
    status: str,
) -> dict[str, object]:
    return {
        "term_source": term_row.get("term_source", ""),
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "term": term_row.get("term", ""),
        "normalized_term": normalized,
        "normalized_length": len(normalized),
        "tr_hits": total_hits,
        "span_intersect_hits": span_intersect_hits,
        "broken_removed_letter_hits": broken_removed_letter_hits,
        "broken_spacing_hits": broken_spacing_hits,
        "broken_total_hits": broken_removed_letter_hits + broken_spacing_hits,
        "preserved_across_omission_hits": preserved_across_omission_hits,
        "status": status,
    }


def example_row(
    term_row: dict[str, str],
    hit: ELSHit,
    break_type: str,
    span_blocks: list[OmittedBlock],
    removed_blocks: list[OmittedBlock],
) -> dict[str, object]:
    return {
        "term_source": term_row.get("term_source", ""),
        "term_id": term_row.get("term_id", ""),
        "concept": term_row.get("concept", ""),
        "category": term_row.get("category", ""),
        "term": term_row.get("term", ""),
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "start_offset": hit.start_offset,
        "end_offset": hit.end_offset,
        "span_letters": hit.span_letters,
        "start_ref": hit.start_ref,
        "end_ref": hit.end_ref,
        "center_ref": hit.center_ref,
        "center_word_index": hit.center_word_index,
        "center_word": hit.center_word,
        "center_normalized_word": hit.center_normalized_word,
        "break_type": break_type,
        "omitted_refs_in_span": ";".join(block.ref for block in span_blocks),
        "omitted_refs_with_sequence_letters": ";".join(block.ref for block in removed_blocks),
    }


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    tr: Corpus,
    critical: Corpus,
    blocks: list[OmittedBlock],
    terms: list[dict[str, str]],
    examples: int,
    term_paths: list[Path],
    args: argparse.Namespace,
) -> None:
    used_blocks = [block for block in blocks if block.used_as_deletion]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "tool": "critical_omission_breaks",
                "created_utc": datetime.now(UTC).isoformat(),
                "tr_config": str(args.tr_config.resolve()),
                "critical_config": str(args.critical_config.resolve()),
                "tr_corpus": tr.summary(),
                "critical_corpus": critical.summary(),
                "term_paths": [str(term_path.resolve()) for term_path in term_paths],
                "default_terms_enabled": not args.no_default_terms,
                "treat_as_deleted": str(args.treat_as_deleted.resolve()) if args.treat_as_deleted else "",
                "out_suffix": args.out_suffix,
                "term_rows": len(terms),
                "min_skip": MIN_SKIP,
                "max_skip": MAX_SKIP,
                "min_term_length": MIN_TERM_LENGTH,
                "ref_missing_verses": len(blocks),
                "deleted_blocks_used": len(used_blocks),
                "deleted_letters_used": sum(block.length for block in used_blocks),
                "broken_example_rows": examples,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
