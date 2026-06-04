"""Command-line interface for Open Bible Codes."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from bisect import bisect_left
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from heapq import nlargest, nsmallest
from pathlib import Path

from . import __version__
from .corpus import load_corpus
from .extensions import (
    EXTENSION_TYPE_PRIORITY,
    build_extension_lexicon,
    extension_score as score_extension,
    extensions_for_hit,
)
from .gematria import hebrew_year_additive, hebrew_year_compact, hebrew_year_remainder
from .matrix import matrix_letters, matrix_summary
from .pairing import cylindrical_hit_distance, hit_center, pair_metrics, span_gap
from .search import (
    ELSHit,
    build_hit,
    count_els_terms_by_lanes,
    find_els,
    iter_els_query_matches_by_lanes,
    iter_forward_matches_in_lanes,
    make_lanes,
    normalize_for_corpus,
    process_context,
)
from .skip_plan import max_skip_for_mode, plan_skip_cap
from .stats import shuffled_letter_controls
from .surface import (
    SurfaceTerm,
    build_surface_context_index,
    normalize_verses,
    surface_context_for_hit_indexed,
)
from .io import (
    open_dict_reader,
    open_dict_writer,
    write_control_stats,
    write_dict_rows,
    write_run_manifest,
)
from .term_io import (
    accepted_term_languages,
    build_surface_terms,
    collect_terms,
    is_safe_report_label,
    parse_corpus_args,
    read_term_rows,
    read_term_rows_many,
)


FIELDNAMES = [
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "span_letters",
    "sequence",
    "start_ref",
    "end_ref",
    "start_source",
    "end_source",
    "center_offset",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
]

SURFACE_CONTEXT_FIELDNAMES = [
    "corpus",
    "term_source",
    "term_id",
    "concept",
    "category",
    *FIELDNAMES,
    "best_context",
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
]

PAIR_FIELDNAMES = [
    "corpus",
    "left_term_id",
    "left_concept",
    "left_term",
    "left_normalized",
    "left_skip",
    "left_start_ref",
    "left_end_ref",
    "left_center_ref",
    "left_center_word_index",
    "left_center_word",
    "left_center_normalized_word",
    "left_start_offset",
    "left_end_offset",
    "right_term_id",
    "right_concept",
    "right_term",
    "right_normalized",
    "right_skip",
    "right_start_ref",
    "right_end_ref",
    "right_center_ref",
    "right_center_word_index",
    "right_center_word",
    "right_center_normalized_word",
    "right_start_offset",
    "right_end_offset",
    "center_distance",
    "span_gap",
    "overlap",
    "same_center_ref",
    "same_center_chapter",
    "same_signed_skip",
    "same_abs_skip",
    "skip_abs_delta",
    "span_union_letters",
    "compactness_score",
    "cylindrical_row_width",
    "cylindrical_distance",
]

BATCH_FIELDNAMES = [
    "corpus",
    "corpus_language",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "min_skip",
    "max_skip",
    "direction",
    "hit_count",
    "status",
]

EXTENSION_FIELDNAMES = [
    "corpus",
    *FIELDNAMES,
    "extension_type",
    "extension_side",
    "extension_length",
    "before_letters",
    "after_letters",
    "extended_sequence",
    "matched_normalized",
    "match_kind",
    "match_count",
    "matched_examples",
    "matched_refs",
    "extension_start_offset",
    "extension_end_offset",
    "extension_start_ref",
    "extension_end_ref",
]

EXTENSION_SUMMARY_FIELDNAMES = [
    "corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extension_side",
    "match_kind",
    "rows",
    "unique_extended_sequences",
    "max_extension_length",
    "max_match_count",
]

EXTENSION_TOP_FIELDNAMES = [
    *EXTENSION_FIELDNAMES,
    "extension_score",
]

MATRIX_LETTER_FIELDNAMES = [
    "corpus",
    "hit_index",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "letter_index",
    "letter",
    "offset",
    "row_width",
    "row",
    "col",
    "ref",
    "word_index",
    "word",
    "normalized_word",
    "start_ref",
    "end_ref",
    "center_ref",
]

MATRIX_SUMMARY_FIELDNAMES = [
    "corpus",
    "hit_index",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "row_width",
    "min_row",
    "max_row",
    "min_col",
    "max_col",
    "rows_spanned",
    "cols_spanned",
    "letter_count",
    "first_offset",
    "last_offset",
    "start_ref",
    "end_ref",
    "center_ref",
]

SKIP_PLAN_FIELDNAMES = [
    "term",
    "normalized_term",
    "normalized_length",
    "min_skip",
    "max_skip_limit",
    "selected_max_skip",
    "direction",
    "target_expected_hits",
    "expected_hits",
    "expected_at_min_skip",
    "status",
]

STRONG_EXTENSION_TYPES = {
    "before_plus_term",
    "term_plus_after",
    "before_plus_term_plus_after",
}
MAX_SKIP_MODES = ("fixed", "full-span", "letters-per-term")

@dataclass
class BatchTermSet:
    label: str
    path: str
    rows: list[dict[str, str]]


@dataclass
class BatchManyCorpusResult:
    label: str
    summary: dict[str, object]
    rows_by_label: dict[str, list[dict[str, object]]]
    timing: dict[str, object]


@dataclass
class SurfaceTermResult:
    summary_row: dict[str, object]
    surface_rows: list[dict[str, object]]


@dataclass
class SurfaceTermAccumulator:
    term: SurfaceTerm
    status: str = "counted"
    max_skip: int | None = None
    hit_count: int = 0
    context_count: int = 0
    exact_center_word_hits: int = 0
    concept_center_word_hits: int = 0
    category_center_word_hits: int = 0
    exact_center_hits: int = 0
    concept_center_hits: int = 0
    category_center_hits: int = 0
    exact_span_hits: int = 0
    concept_span_hits: int = 0
    category_span_hits: int = 0
    surface_rows: list[dict[str, object]] = field(default_factory=list)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    prog = Path(sys.argv[0]).name if sys.argv else "open-bible-codes"
    parser = argparse.ArgumentParser(prog=prog)
    subparsers = parser.add_subparsers(required=True)

    stats_parser = subparsers.add_parser("stats", help="show corpus statistics")
    stats_parser.add_argument("--config", required=True)
    stats_parser.set_defaults(func=cmd_stats)

    search_parser = subparsers.add_parser("search", help="search ELS terms")
    search_parser.add_argument("--config", required=True)
    search_parser.add_argument("--term", action="append", default=[])
    search_parser.add_argument("--terms-file")
    search_parser.add_argument("--min-skip", type=int, default=2)
    search_parser.add_argument("--max-skip", type=int, default=100)
    add_dynamic_max_skip_args(search_parser)
    search_parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    search_parser.add_argument("--max-hits", type=int)
    search_parser.add_argument("--out")
    search_parser.add_argument("--manifest-out")
    search_parser.add_argument("--shuffles", type=int, default=0)
    search_parser.add_argument("--seed", type=int, default=1)
    search_parser.add_argument("--stats-out")
    search_parser.set_defaults(func=cmd_search)

    extensions_parser = subparsers.add_parser(
        "extensions",
        help="check same-skip words or phrases before and after ELS hits",
    )
    extensions_parser.add_argument("--config", required=True)
    extensions_parser.add_argument(
        "--hits",
        required=True,
        help="CSV from search or surface-context",
    )
    extensions_parser.add_argument("--corpus-label")
    extensions_parser.add_argument("--max-before", type=int, default=12)
    extensions_parser.add_argument("--max-after", type=int, default=12)
    extensions_parser.add_argument("--phrase-words", type=int, default=4)
    extensions_parser.add_argument(
        "--include-both-sided",
        action="store_true",
        help="also test before+term+after candidates",
    )
    extensions_parser.add_argument("--max-extensions-per-hit", type=int)
    extensions_parser.add_argument("--out", required=True)
    extensions_parser.add_argument("--manifest-out")
    extensions_parser.set_defaults(func=cmd_extensions)

    matrix_parser = subparsers.add_parser(
        "matrix",
        help="export row/column coordinates and letter paths for ELS hits",
    )
    matrix_parser.add_argument("--config", required=True)
    matrix_parser.add_argument(
        "--hits",
        required=True,
        help="CSV from search, surface-context, or a filtered hit export",
    )
    matrix_parser.add_argument("--corpus-label")
    matrix_parser.add_argument(
        "--row-width",
        type=int,
        help="table row width; defaults to abs(skip) for each hit",
    )
    matrix_parser.add_argument("--out", required=True)
    matrix_parser.add_argument("--summary-out")
    matrix_parser.add_argument("--manifest-out")
    matrix_parser.set_defaults(func=cmd_matrix)

    skip_plan_parser = subparsers.add_parser(
        "skip-plan",
        help="estimate a max skip from target expected hit count",
    )
    skip_plan_parser.add_argument("--config", required=True)
    skip_plan_parser.add_argument("--term", action="append", default=[])
    skip_plan_parser.add_argument("--terms-file")
    skip_plan_parser.add_argument("--min-skip", type=int, default=2)
    skip_plan_parser.add_argument("--max-skip-limit", type=int, default=1000)
    skip_plan_parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    skip_plan_parser.add_argument("--target-expected-hits", type=float, default=100.0)
    skip_plan_parser.add_argument("--out", required=True)
    skip_plan_parser.add_argument("--manifest-out")
    skip_plan_parser.set_defaults(func=cmd_skip_plan)

    extension_summary_parser = subparsers.add_parser(
        "extension-summary",
        help="summarize and rank ELS extension rows",
    )
    extension_summary_parser.add_argument("--extensions", required=True)
    extension_summary_parser.add_argument(
        "--min-extension-length",
        type=int,
        default=2,
        help="filter short extension rows; default removes 1-letter noise",
    )
    extension_summary_parser.add_argument(
        "--min-term-length",
        type=int,
        default=0,
        help="filter rows whose normalized term is shorter than this length",
    )
    extension_summary_parser.add_argument(
        "--match-kind-prefix",
        help="filter rows to match kinds with this prefix, for example phrase_",
    )
    extension_summary_parser.add_argument(
        "--exclude-term",
        action="append",
        default=[],
        help="exclude raw or normalized terms; may be repeated",
    )
    extension_summary_parser.add_argument(
        "--top",
        type=int,
        default=200,
        help="number of strongest rows to write",
    )
    extension_summary_parser.add_argument("--out", required=True)
    extension_summary_parser.add_argument("--top-out")
    extension_summary_parser.add_argument("--manifest-out")
    extension_summary_parser.set_defaults(func=cmd_extension_summary)

    batch_parser = subparsers.add_parser("batch", help="count term ELS hits in corpora")
    batch_parser.add_argument("--terms", required=True)
    batch_parser.add_argument(
        "--corpus",
        action="append",
        required=True,
        help="label=config_path; may be repeated",
    )
    batch_parser.add_argument("--min-skip", type=int, default=2)
    batch_parser.add_argument("--max-skip", type=int, default=50)
    add_dynamic_max_skip_args(batch_parser)
    batch_parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    batch_parser.add_argument("--min-term-length", type=int, default=3)
    batch_parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="parallel count workers; 0 uses CPU count",
    )
    batch_parser.add_argument("--out", required=True)
    batch_parser.add_argument("--manifest-out")
    batch_parser.set_defaults(func=cmd_batch)

    batch_many_parser = subparsers.add_parser(
        "batch-many",
        help="count multiple term CSVs with one corpus scan per corpus",
    )
    batch_many_parser.add_argument(
        "--term-set",
        action="append",
        required=True,
        help="label=terms_csv; may be repeated",
    )
    batch_many_parser.add_argument(
        "--corpus",
        action="append",
        required=True,
        help="label=config_path; may be repeated",
    )
    batch_many_parser.add_argument("--min-skip", type=int, default=2)
    batch_many_parser.add_argument("--max-skip", type=int, default=50)
    add_dynamic_max_skip_args(batch_many_parser)
    batch_many_parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    batch_many_parser.add_argument("--min-term-length", type=int, default=3)
    batch_many_parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="parallel count workers; 0 uses CPU count",
    )
    batch_many_parser.add_argument(
        "--corpus-jobs",
        type=int,
        default=1,
        help="parallel corpus workers; 0 uses corpus count",
    )
    batch_many_parser.add_argument("--out-dir", required=True)
    batch_many_parser.add_argument("--manifest-out")
    batch_many_parser.set_defaults(func=cmd_batch_many)

    pairs_parser = subparsers.add_parser("pairs", help="find nearest ELS term pairs")
    pairs_parser.add_argument("--terms", required=True)
    pairs_parser.add_argument(
        "--corpus",
        action="append",
        required=True,
        help="label=config_path; may be repeated",
    )
    pairs_parser.add_argument("--left-category", required=True)
    pairs_parser.add_argument("--right-category", required=True)
    pairs_parser.add_argument("--min-skip", type=int, default=2)
    pairs_parser.add_argument("--max-skip", type=int, default=50)
    add_dynamic_max_skip_args(pairs_parser)
    pairs_parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    pairs_parser.add_argument("--min-term-length", type=int, default=3)
    pairs_parser.add_argument("--max-gap", type=int, default=500)
    pairs_parser.add_argument(
        "--row-width",
        type=int,
        help="optional common table width for cylindrical pair distance",
    )
    pairs_parser.add_argument("--top", type=int, default=200)
    pairs_parser.add_argument("--out", required=True)
    pairs_parser.add_argument("--summary-out")
    pairs_parser.add_argument("--manifest-out")
    pairs_parser.set_defaults(func=cmd_pairs)

    surface_parser = subparsers.add_parser(
        "surface-context",
        help="find ELS hits whose surface text discusses the term",
    )
    surface_parser.add_argument(
        "--terms",
        action="append",
        required=True,
        help="term CSV; may be repeated",
    )
    surface_parser.add_argument(
        "--corpus",
        action="append",
        required=True,
        help="label=config_path; may be repeated",
    )
    surface_parser.add_argument("--min-skip", type=int, default=2)
    surface_parser.add_argument("--max-skip", type=int, default=50)
    add_dynamic_max_skip_args(surface_parser)
    surface_parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    surface_parser.add_argument("--min-term-length", type=int, default=3)
    surface_parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="parallel term workers; 0 uses CPU count",
    )
    surface_parser.add_argument("--max-hits-per-term", type=int)
    surface_parser.add_argument(
        "--include-all",
        action="store_true",
        help="write all hits, not only contextual hits",
    )
    surface_parser.add_argument("--out", required=True)
    surface_parser.add_argument("--summary-out")
    surface_parser.add_argument("--manifest-out")
    surface_parser.set_defaults(func=cmd_surface_context)

    gematria_parser = subparsers.add_parser("gematria-year", help="print Hebrew year encodings")
    gematria_parser.add_argument("year", type=int)
    gematria_parser.set_defaults(func=cmd_gematria_year)

    return parser


def add_dynamic_max_skip_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--max-skip-mode",
        choices=MAX_SKIP_MODES,
        default="fixed",
        help=(
            "fixed uses --max-skip; full-span uses floor((letters-1)/(term_letters-1)); "
            "letters-per-term uses floor(letters/term_letters)"
        ),
    )
    parser.add_argument(
        "--max-skip-limit",
        type=int,
        help="optional safety cap applied after a dynamic max-skip calculation",
    )


def cmd_stats(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.config)
    print(corpus.summary_json())
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    terms = collect_terms(args.term, args.terms_file)
    if not terms:
        raise SystemExit("provide --term or --terms-file")

    corpus = load_corpus(args.config)
    hit_count = 0
    control_rows: list[dict[str, object]] = []
    effective_max_skips: dict[str, int | str] = {}
    if args.shuffles and args.max_skip_mode != "fixed":
        raise SystemExit("--shuffles currently requires --max-skip-mode fixed")

    with open_hits_writer(args.out) as writer:
        for term in terms:
            normalized = normalize_for_corpus(corpus, term)
            effective_max_skip = effective_max_skip_for_query(corpus, normalized, args)
            effective_max_skips[term] = effective_max_skip or ""
            if effective_max_skip is None:
                continue
            for hit in find_els(
                corpus,
                term,
                min_skip=args.min_skip,
                max_skip=effective_max_skip,
                direction=args.direction,
                max_hits=args.max_hits,
            ):
                writer.writerow(hit.as_row())
                hit_count += 1

    if args.shuffles:
        controls = shuffled_letter_controls(
            corpus,
            terms,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            shuffles=args.shuffles,
            seed=args.seed,
        )
        for term, control in controls:
            control_rows.append(
                {
                    "term": term,
                    "observed": control.observed,
                    "shuffled_counts": list(control.shuffled_counts),
                    "p_greater_equal": control.p_greater_equal,
                }
            )

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "corpus": corpus.summary(),
                "terms": terms,
                "min_skip": args.min_skip,
                "max_skip": args.max_skip,
                "max_skip_mode": args.max_skip_mode,
                "max_skip_limit": args.max_skip_limit,
                "effective_max_skips": effective_max_skips,
                "direction": args.direction,
                "max_hits": args.max_hits,
                "hit_count": hit_count,
                "shuffles": args.shuffles,
                "seed": args.seed,
            },
            args.manifest_out,
        )
    if args.shuffles:
        write_control_stats(control_rows, args.stats_out)
    return 0


def cmd_extensions(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.config)
    lexicon = build_extension_lexicon(corpus, max_phrase_words=args.phrase_words)
    corpus_label = args.corpus_label or corpus.name
    input_hit_count = 0
    hit_count = 0
    skipped_hit_count = 0
    extension_count = 0

    with open_dict_reader(args.hits) as rows, open_dict_writer(
        args.out,
        EXTENSION_FIELDNAMES,
    ) as writer:
        for row in rows:
            input_hit_count += 1
            row_corpus = row.get("corpus", "")
            if row_corpus:
                if not args.corpus_label:
                    raise SystemExit(
                        "hits file has corpus labels; pass --corpus-label to select one"
                    )
                if row_corpus != args.corpus_label:
                    skipped_hit_count += 1
                    continue
            hit = hit_from_row(row)
            hit = hit_with_corpus_center(corpus, hit)
            hit_count += 1
            for extension in extensions_for_hit(
                corpus,
                hit,
                lexicon,
                max_before=args.max_before,
                max_after=args.max_after,
                include_both_sided=args.include_both_sided,
                max_extensions=args.max_extensions_per_hit,
            ):
                writer.writerow(extension_row(corpus_label, hit, extension))
                extension_count += 1

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "hits": str(Path(args.hits).expanduser().resolve()),
                "corpus": corpus.summary(),
                "max_before": args.max_before,
                "max_after": args.max_after,
                "phrase_words": args.phrase_words,
                "include_both_sided": args.include_both_sided,
                "max_extensions_per_hit": args.max_extensions_per_hit,
                "lexicon_entries": len(lexicon.entries),
                "input_hit_count": input_hit_count,
                "skipped_hit_count": skipped_hit_count,
                "hit_count": hit_count,
                "extension_count": extension_count,
            },
            args.manifest_out,
        )
    return 0


def cmd_matrix(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.config)
    corpus_label = args.corpus_label or corpus.name
    input_hit_count = 0
    skipped_hit_count = 0
    hit_count = 0
    letter_count = 0
    summary_rows: list[dict[str, object]] = []

    with open_dict_reader(args.hits) as rows, open_dict_writer(
        args.out,
        MATRIX_LETTER_FIELDNAMES,
    ) as writer:
        for row in rows:
            input_hit_count += 1
            row_corpus = row.get("corpus", "")
            if row_corpus:
                if not args.corpus_label:
                    raise SystemExit(
                        "hits file has corpus labels; pass --corpus-label to select one"
                    )
                if row_corpus != args.corpus_label:
                    skipped_hit_count += 1
                    continue
            hit = hit_with_corpus_center(corpus, hit_from_row(row))
            hit_count += 1
            hit_index = hit_count
            letters = matrix_letters(
                corpus,
                hit,
                hit_index=hit_index,
                row_width=args.row_width,
            )
            width = args.row_width or abs(hit.skip)
            for letter in letters:
                writer.writerow(matrix_letter_row(corpus_label, hit, letter, width))
            letter_count += len(letters)
            summary_rows.append(
                matrix_summary_row(
                    corpus_label,
                    hit,
                    matrix_summary(hit, letters, row_width=args.row_width),
                )
            )

    if args.summary_out:
        write_dict_rows(summary_rows, args.summary_out, MATRIX_SUMMARY_FIELDNAMES)
    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "hits": str(Path(args.hits).expanduser().resolve()),
                "corpus": corpus.summary(),
                "corpus_label": corpus_label,
                "row_width": args.row_width,
                "input_hit_count": input_hit_count,
                "skipped_hit_count": skipped_hit_count,
                "hit_count": hit_count,
                "letter_count": letter_count,
            },
            args.manifest_out,
        )
    return 0


def cmd_skip_plan(args: argparse.Namespace) -> int:
    terms = collect_terms(args.term, args.terms_file)
    if not terms:
        raise SystemExit("provide --term or --terms-file")

    corpus = load_corpus(args.config)
    rows: list[dict[str, object]] = []
    for term in terms:
        normalized = normalize_for_corpus(corpus, term)
        plan = plan_skip_cap(
            corpus.text,
            term,
            normalized,
            min_skip=args.min_skip,
            max_skip_limit=args.max_skip_limit,
            direction=args.direction,
            target_expected_hits=args.target_expected_hits,
        )
        rows.append(skip_plan_row(plan))

    write_dict_rows(rows, args.out, SKIP_PLAN_FIELDNAMES)
    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "mode": "skip-plan",
                "created_utc": datetime.now(UTC).isoformat(),
                "config": str(Path(args.config).expanduser().resolve()),
                "corpus": corpus.summary(),
                "terms": terms,
                "min_skip": args.min_skip,
                "max_skip_limit": args.max_skip_limit,
                "direction": args.direction,
                "target_expected_hits": args.target_expected_hits,
                "rows": len(rows),
                "model": "independent letters from corpus frequency",
            },
            args.manifest_out,
        )
    return 0


def cmd_extension_summary(args: argparse.Namespace) -> int:
    input_rows = 0
    kept_rows = 0
    filtered_short_rows = 0
    filtered_term_length_rows = 0
    filtered_match_kind_rows = 0
    filtered_excluded_term_rows = 0
    excluded_terms = set(args.exclude_term)
    groups: dict[tuple[str, ...], dict[str, object]] = {}
    top_candidates: list[dict[str, object]] = []

    with open_dict_reader(args.extensions) as rows:
        for row in rows:
            input_rows += 1
            extension_length = int(row["extension_length"])
            if extension_length < args.min_extension_length:
                filtered_short_rows += 1
                continue
            if len(row.get("normalized_term", "")) < args.min_term_length:
                filtered_term_length_rows += 1
                continue
            if args.match_kind_prefix and not row.get("match_kind", "").startswith(
                args.match_kind_prefix
            ):
                filtered_match_kind_rows += 1
                continue
            if (
                row.get("term", "") in excluded_terms
                or row.get("normalized_term", "") in excluded_terms
            ):
                filtered_excluded_term_rows += 1
                continue
            kept_rows += 1
            add_extension_summary_group(groups, row, extension_length)
            if row.get("extension_type") in STRONG_EXTENSION_TYPES:
                ranked_row = dict(row)
                ranked_row["extension_score"] = extension_score(row, extension_length)
                top_candidates.append(ranked_row)

    summary_rows = extension_summary_rows(groups)
    write_dict_rows(summary_rows, args.out, fieldnames=EXTENSION_SUMMARY_FIELDNAMES)

    top_rows = nlargest(
        args.top,
        top_candidates,
        key=extension_rank_key,
    )
    if args.top_out:
        write_dict_rows(top_rows, args.top_out, fieldnames=EXTENSION_TOP_FIELDNAMES)

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "extensions": str(Path(args.extensions).expanduser().resolve()),
                "min_extension_length": args.min_extension_length,
                "min_term_length": args.min_term_length,
                "match_kind_prefix": args.match_kind_prefix,
                "exclude_terms": sorted(excluded_terms),
                "top": args.top,
                "input_rows": input_rows,
                "kept_rows": kept_rows,
                "filtered_short_rows": filtered_short_rows,
                "filtered_term_length_rows": filtered_term_length_rows,
                "filtered_match_kind_rows": filtered_match_kind_rows,
                "filtered_excluded_term_rows": filtered_excluded_term_rows,
                "summary_rows": len(summary_rows),
                "top_rows": len(top_rows),
            },
            args.manifest_out,
        )
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    term_rows = read_term_rows(args.terms)
    corpora = [(label, load_corpus(config)) for label, config in parse_corpus_args(args.corpus)]
    rows: list[dict[str, object]] = []

    for corpus_label, corpus in corpora:
        prepared_rows = prepare_batch_rows(corpus, term_rows, args)
        max_skip_by_query = max_skip_by_query_from_prepared(prepared_rows)
        count_max_skip = max(max_skip_by_query.values(), default=args.min_skip)
        counts = count_els_terms_by_lanes(
            corpus.text,
            counted_normalized_terms(prepared_rows),
            min_skip=args.min_skip,
            max_skip=count_max_skip,
            direction=args.direction,
            jobs=args.jobs,
            max_skip_by_query=max_skip_by_query,
        )
        rows.extend(batch_rows_from_counts(corpus_label, corpus, prepared_rows, counts, args))

    write_batch_rows(rows, args.out)
    if args.manifest_out:
        write_run_manifest(
            batch_manifest_payload(args, args.terms, corpora, len(rows)),
            args.manifest_out,
        )
    return 0


def cmd_batch_many(args: argparse.Namespace) -> int:
    term_sets = parse_term_set_args(args.term_set)
    corpus_configs = parse_corpus_args(args.corpus)
    rows_by_label: dict[str, list[dict[str, object]]] = {
        term_set.label: [] for term_set in term_sets
    }
    corpus_jobs = resolve_corpus_jobs(args.corpus_jobs, len(corpus_configs))
    validate_batch_many_parallelism(args.jobs, corpus_jobs)
    results = run_batch_many_corpora(corpus_configs, term_sets, args, corpus_jobs)
    corpus_summaries = [
        {"label": result.label, "summary": result.summary}
        for result in results
    ]
    corpus_timings = [result.timing for result in results]
    for result in results:
        for label, rows in result.rows_by_label.items():
            rows_by_label[label].extend(rows)

    out_dir = Path(args.out_dir).expanduser()
    written_reports = []
    for term_set in term_sets:
        output_path = out_dir / f"{term_set.label}_counts.csv"
        manifest_path = out_dir / f"{term_set.label}_counts.manifest.json"
        rows = rows_by_label[term_set.label]
        write_batch_rows(rows, output_path)
        write_run_manifest(
            batch_manifest_payload(
                args,
                term_set.path,
                (),
                len(rows),
                term_set_label=term_set.label,
                mode="batch-many",
                corpus_summaries=corpus_summaries,
                corpus_timings=corpus_timings,
            ),
            str(manifest_path),
        )
        written_reports.append(
            {
                "term_set": term_set.label,
                "terms": str(Path(term_set.path).expanduser().resolve()),
                "out": str(output_path),
                "manifest_out": str(manifest_path),
                "rows": len(rows),
            }
        )

    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "mode": "batch-many",
                "created_utc": datetime.now(UTC).isoformat(),
                "term_sets": written_reports,
                "corpora": corpus_summaries,
                "min_skip": args.min_skip,
                "max_skip": args.max_skip,
                "max_skip_mode": args.max_skip_mode,
                "max_skip_limit": args.max_skip_limit,
                "direction": args.direction,
                "min_term_length": args.min_term_length,
                "jobs": args.jobs,
                "corpus_jobs": args.corpus_jobs,
                "effective_corpus_jobs": corpus_jobs,
                "corpus_timings": corpus_timings,
            },
            args.manifest_out,
        )
    return 0


def run_batch_many_corpora(
    corpus_configs: list[tuple[str, str]],
    term_sets: list[BatchTermSet],
    args: argparse.Namespace,
    corpus_jobs: int,
) -> list[BatchManyCorpusResult]:
    if corpus_jobs == 1:
        return [
            process_batch_many_corpus(corpus_label, config, term_sets, args)
            for corpus_label, config in corpus_configs
        ]
    with ThreadPoolExecutor(max_workers=corpus_jobs) as executor:
        return list(
            executor.map(
                lambda item: process_batch_many_corpus(
                    item[0],
                    item[1],
                    term_sets,
                    args,
                ),
                corpus_configs,
            )
        )


def process_batch_many_corpus(
    corpus_label: str,
    config: str,
    term_sets: list[BatchTermSet],
    args: argparse.Namespace,
) -> BatchManyCorpusResult:
    corpus_started = time.perf_counter()
    load_started = time.perf_counter()
    corpus = load_corpus(config)
    load_seconds = elapsed_seconds(load_started)

    prepare_started = time.perf_counter()
    prepared_by_label = {
        term_set.label: prepare_batch_rows(
            corpus,
            term_set.rows,
            args,
        )
        for term_set in term_sets
    }
    all_normalized_terms = [
        normalized
        for prepared_rows in prepared_by_label.values()
        for normalized in counted_normalized_terms(prepared_rows)
    ]
    prepare_seconds = elapsed_seconds(prepare_started)

    count_started = time.perf_counter()
    max_skip_by_query = max_skip_by_query_from_prepared(
        [
            row
            for prepared_rows in prepared_by_label.values()
            for row in prepared_rows
        ]
    )
    count_max_skip = max(max_skip_by_query.values(), default=args.min_skip)
    counts = count_els_terms_by_lanes(
        corpus.text,
        all_normalized_terms,
        min_skip=args.min_skip,
        max_skip=count_max_skip,
        direction=args.direction,
        jobs=args.jobs,
        max_skip_by_query=max_skip_by_query,
    )
    count_seconds = elapsed_seconds(count_started)

    row_started = time.perf_counter()
    output_rows = 0
    rows_by_label: dict[str, list[dict[str, object]]] = {}
    for term_set in term_sets:
        rows = batch_rows_from_counts(
            corpus_label,
            corpus,
            prepared_by_label[term_set.label],
            counts,
            args,
        )
        rows_by_label[term_set.label] = rows
        output_rows += len(rows)
    row_seconds = elapsed_seconds(row_started)
    return BatchManyCorpusResult(
        label=corpus_label,
        summary=corpus.summary(),
        rows_by_label=rows_by_label,
        timing={
            "label": corpus_label,
            "config": str(Path(config).expanduser().resolve()),
            "language": corpus.language,
            "letters": len(corpus.text),
            "verses": len(corpus.verses),
            "term_sets": len(term_sets),
            "counted_terms": len(all_normalized_terms),
            "unique_counted_terms": len(set(all_normalized_terms)),
            "max_counted_skip": count_max_skip,
            "rows": output_rows,
            "load_seconds": load_seconds,
            "prepare_seconds": prepare_seconds,
            "count_seconds": count_seconds,
            "row_seconds": row_seconds,
            "total_seconds": elapsed_seconds(corpus_started),
        },
    )


def resolve_corpus_jobs(corpus_jobs: int, corpus_count: int) -> int:
    if corpus_jobs < 0:
        raise SystemExit("--corpus-jobs must be >= 0")
    if corpus_jobs == 0:
        corpus_jobs = corpus_count
    return max(1, min(corpus_jobs, max(1, corpus_count)))


def validate_batch_many_parallelism(count_jobs: int, corpus_jobs: int) -> None:
    if corpus_jobs > 1 and count_jobs != 1:
        raise SystemExit(
            "--corpus-jobs > 1 cannot be combined with --jobs other than 1"
        )


def prepare_batch_rows(corpus, term_rows: list[dict[str, str]], args: argparse.Namespace):
    languages = accepted_term_languages(corpus.language)
    prepared_rows = []
    for term_row in term_rows:
        term_language = term_row.get("language", "").strip()
        if term_language not in languages:
            continue
        term = term_row.get("term", "").strip()
        normalized = normalize_for_corpus(corpus, term)
        status = "counted"
        effective_max_skip = effective_max_skip_for_query(corpus, normalized, args)
        if len(normalized) < args.min_term_length:
            status = "skipped_short_term"
            effective_max_skip = None
        elif effective_max_skip is None:
            status = "skipped_no_valid_skip"
        prepared_rows.append(
            (term_row, term_language, term, normalized, status, effective_max_skip)
        )
    return prepared_rows


def counted_normalized_terms(prepared_rows) -> list[str]:
    return [
        normalized
        for (
            _term_row,
            _term_language,
            _term,
            normalized,
            status,
            _effective_max_skip,
        ) in prepared_rows
        if status == "counted"
    ]


def max_skip_by_query_from_prepared(prepared_rows) -> dict[str, int]:
    caps: dict[str, int] = {}
    for _term_row, _term_language, _term, normalized, status, effective_max_skip in prepared_rows:
        if status != "counted" or effective_max_skip is None:
            continue
        caps[normalized] = max(caps.get(normalized, 0), int(effective_max_skip))
    return caps


def batch_rows_from_counts(
    corpus_label: str,
    corpus,
    prepared_rows,
    counts: dict[str, int],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for term_row, term_language, term, normalized, status, effective_max_skip in prepared_rows:
        hit_count = counts.get(normalized, 0)
        if status != "counted":
            hit_count = 0
        rows.append(
            {
                "corpus": corpus_label,
                "corpus_language": corpus.language,
                "term_id": term_row.get("term_id", ""),
                "concept": term_row.get("concept", ""),
                "category": term_row.get("category", ""),
                "term_language": term_language,
                "term": term,
                "normalized_term": normalized,
                "normalized_length": len(normalized),
                "min_skip": args.min_skip,
                "max_skip": effective_max_skip or "",
                "direction": args.direction,
                "hit_count": hit_count,
                "status": status,
            }
        )
    return rows


def batch_manifest_payload(
    args: argparse.Namespace,
    terms_path: str,
    corpora,
    row_count: int,
    *,
    term_set_label: str = "",
    mode: str = "batch",
    corpus_summaries: list[dict[str, object]] | None = None,
    corpus_timings: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    if corpus_summaries is None:
        corpus_summaries = [
            {"label": label, "summary": corpus.summary()}
            for label, corpus in corpora
        ]
    payload = {
        "tool": "edls",
        "version": __version__,
        "mode": mode,
        "created_utc": datetime.now(UTC).isoformat(),
        "terms": str(Path(terms_path).expanduser().resolve()),
        "corpora": corpus_summaries,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "max_skip_mode": args.max_skip_mode,
        "max_skip_limit": args.max_skip_limit,
        "direction": args.direction,
        "min_term_length": args.min_term_length,
        "jobs": args.jobs,
        "rows": row_count,
    }
    if term_set_label:
        payload["term_set"] = term_set_label
    if hasattr(args, "corpus_jobs"):
        payload["corpus_jobs"] = args.corpus_jobs
    if corpus_timings is not None:
        payload["corpus_timings"] = corpus_timings
    return payload


def elapsed_seconds(started: float) -> float:
    return round(time.perf_counter() - started, 3)


def effective_max_skip_for_query(corpus, normalized: str, args: argparse.Namespace) -> int | None:
    return effective_max_skip_for_normalized(
        len(corpus.text),
        len(normalized),
        args.min_skip,
        args.max_skip,
        args.max_skip_mode,
        args.max_skip_limit,
    )


def effective_max_skip_for_normalized(
    text_length: int,
    normalized_length: int,
    min_skip: int,
    fixed_max_skip: int,
    mode: str,
    max_skip_limit,
) -> int | None:
    if min_skip < 1:
        raise SystemExit("--min-skip must be >= 1")
    if max_skip_limit is not None and int(max_skip_limit) < min_skip:
        raise SystemExit("--max-skip-limit must be >= --min-skip")
    if normalized_length <= 0:
        return None
    if mode == "fixed":
        if fixed_max_skip < min_skip:
            raise SystemExit("--max-skip must be >= --min-skip")
        return fixed_max_skip
    dynamic_max_skip = max_skip_for_mode(text_length, normalized_length, mode)
    if max_skip_limit is not None:
        dynamic_max_skip = min(dynamic_max_skip, int(max_skip_limit))
    if dynamic_max_skip < min_skip:
        return None
    return dynamic_max_skip


def cmd_pairs(args: argparse.Namespace) -> int:
    if args.row_width is not None and args.row_width <= 0:
        raise SystemExit("--row-width must be > 0")
    term_rows = read_term_rows(args.terms)
    corpora = [(label, load_corpus(config)) for label, config in parse_corpus_args(args.corpus)]
    pair_row_count = 0
    summary_rows: list[dict[str, object]] = []

    with open_dict_writer(args.out, PAIR_FIELDNAMES) as pair_writer:
        for corpus_label, corpus in corpora:
            languages = accepted_term_languages(corpus.language)
            left_terms = [
                row
                for row in term_rows
                if row.get("category") == args.left_category
                and row.get("language", "").strip() in languages
            ]
            right_terms = [
                row
                for row in term_rows
                if row.get("category") == args.right_category
                and row.get("language", "").strip() in languages
            ]
            left_by_id = {row["term_id"]: row for row in left_terms}
            right_by_id = {row["term_id"]: row for row in right_terms}
            left_hits = collect_hits_by_term(corpus, left_terms, args)
            right_hits = collect_hits_by_term(corpus, right_terms, args)
            right_index = build_hit_center_index(right_hits)

            for left_term_id, hits in left_hits.items():
                left_row = left_by_id[left_term_id]
                for right_term_id, right_data in right_index.items():
                    right_row = right_by_id[right_term_id]
                    candidates = []
                    for hit in hits:
                        nearest = nearest_hit_by_center(hit, right_data)
                        if nearest is None:
                            continue
                        right_hit, _center_distance = nearest
                        metrics = pair_metrics(hit, right_hit)
                        gap = metrics.span_gap
                        if gap <= args.max_gap:
                            cylindrical_distance = ""
                            if args.row_width is not None:
                                cylindrical_distance = round(
                                    cylindrical_hit_distance(
                                        hit,
                                        right_hit,
                                        args.row_width,
                                    ),
                                    3,
                                )
                            candidates.append(
                                {
                                    "corpus": corpus_label,
                                    "left_term_id": left_term_id,
                                    "left_concept": left_row.get("concept", ""),
                                    "left_term": left_row.get("term", ""),
                                    "left_normalized": hit.normalized_term,
                                    "left_skip": hit.skip,
                                    "left_start_ref": hit.start_ref,
                                    "left_end_ref": hit.end_ref,
                                    "left_center_ref": hit.center_ref,
                                    "left_center_word_index": hit.center_word_index,
                                    "left_center_word": hit.center_word,
                                    "left_center_normalized_word": hit.center_normalized_word,
                                    "left_start_offset": hit.start_offset,
                                    "left_end_offset": hit.end_offset,
                                    "right_term_id": right_term_id,
                                    "right_concept": right_row.get("concept", ""),
                                    "right_term": right_row.get("term", ""),
                                    "right_normalized": right_hit.normalized_term,
                                    "right_skip": right_hit.skip,
                                    "right_start_ref": right_hit.start_ref,
                                    "right_end_ref": right_hit.end_ref,
                                    "right_center_ref": right_hit.center_ref,
                                    "right_center_word_index": right_hit.center_word_index,
                                    "right_center_word": right_hit.center_word,
                                    "right_center_normalized_word": (
                                        right_hit.center_normalized_word
                                    ),
                                    "right_start_offset": right_hit.start_offset,
                                    "right_end_offset": right_hit.end_offset,
                                    "center_distance": round(metrics.center_distance, 1),
                                    "span_gap": gap,
                                    "overlap": metrics.overlap,
                                    "same_center_ref": metrics.same_center_ref,
                                    "same_center_chapter": metrics.same_center_chapter,
                                    "same_signed_skip": metrics.same_signed_skip,
                                    "same_abs_skip": metrics.same_abs_skip,
                                    "skip_abs_delta": metrics.skip_abs_delta,
                                    "span_union_letters": metrics.span_union_letters,
                                    "compactness_score": round(metrics.compactness_score, 1),
                                    "cylindrical_row_width": args.row_width or "",
                                    "cylindrical_distance": cylindrical_distance,
                                }
                            )
                    best_candidates = nsmallest(
                        args.top,
                        candidates,
                        key=lambda row: (row["span_gap"], row["center_distance"]),
                    )
                    pair_writer.writerows(best_candidates)
                    pair_row_count += len(best_candidates)
                    summary_rows.append(
                        {
                            "corpus": corpus_label,
                            "left_term_id": left_term_id,
                            "left_concept": left_row.get("concept", ""),
                            "left_hits": len(hits),
                            "right_term_id": right_term_id,
                            "right_concept": right_row.get("concept", ""),
                            "right_hits": len(right_data["hits"]),
                            "pairs_within_gap": len(candidates),
                            "best_span_gap": (
                                best_candidates[0]["span_gap"] if best_candidates else ""
                            ),
                            "best_center_distance": (
                                best_candidates[0]["center_distance"]
                                if best_candidates
                                else ""
                            ),
                        }
                    )

    if args.summary_out:
        write_dict_rows(summary_rows, args.summary_out)
    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "terms": str(Path(args.terms).expanduser().resolve()),
                "corpora": [
                    {"label": label, "summary": corpus.summary()}
                    for label, corpus in corpora
                ],
                "left_category": args.left_category,
                "right_category": args.right_category,
                "min_skip": args.min_skip,
                "max_skip": args.max_skip,
                "max_skip_mode": args.max_skip_mode,
                "max_skip_limit": args.max_skip_limit,
                "direction": args.direction,
                "min_term_length": args.min_term_length,
                "max_gap": args.max_gap,
                "row_width": args.row_width,
                "top": args.top,
                "rows": pair_row_count,
            },
            args.manifest_out,
        )
    return 0


def cmd_surface_context(args: argparse.Namespace) -> int:
    term_rows = read_term_rows_many(args.terms)
    corpora = [(label, load_corpus(config)) for label, config in parse_corpus_args(args.corpus)]
    row_count = 0
    summary_rows: list[dict[str, object]] = []

    with open_dict_writer(args.out, SURFACE_CONTEXT_FIELDNAMES) as row_writer:
        for corpus_label, corpus in corpora:
            languages = accepted_term_languages(corpus.language)
            corpus_terms = build_surface_terms(
                corpus,
                [
                    row
                    for row in term_rows
                    if row.get("language", "").strip() in languages
                ],
            )
            normalized_verses = normalize_verses(corpus)
            context_index = build_surface_context_index(
                corpus,
                corpus_terms,
                normalized_verses,
            )
            for result in process_surface_terms(
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                args,
            ):
                summary_rows.append(result.summary_row)
                row_writer.writerows(result.surface_rows)
                row_count += len(result.surface_rows)

    if args.summary_out:
        write_dict_rows(summary_rows, args.summary_out)
    if args.manifest_out:
        write_run_manifest(
            {
                "tool": "edls",
                "version": __version__,
                "created_utc": datetime.now(UTC).isoformat(),
                "terms": [str(Path(path).expanduser().resolve()) for path in args.terms],
                "corpora": [
                    {"label": label, "summary": corpus.summary()}
                    for label, corpus in corpora
                ],
                "min_skip": args.min_skip,
                "max_skip": args.max_skip,
                "direction": args.direction,
                "min_term_length": args.min_term_length,
                "jobs": args.jobs,
                "max_hits_per_term": args.max_hits_per_term,
                "include_all": args.include_all,
                "rows": row_count,
                "summary_rows": len(summary_rows),
            },
            args.manifest_out,
        )
    return 0


def process_surface_terms(
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    args: argparse.Namespace,
) -> list[SurfaceTermResult]:
    jobs = resolve_surface_jobs(args.jobs, len(corpus_terms))
    if jobs == 1:
        # Bulk AC scans the corpus once for all terms. In process chunks that would
        # rescan the same text per worker, so parallel mode keeps per-term lanes.
        options = surface_options(args)
        options["bulk_terms"] = True
        return process_surface_term_group(
            corpus_label,
            corpus,
            corpus_terms,
            corpus_terms,
            context_index,
            options,
        )

    chunks = chunk_indexes(len(corpus_terms), jobs)
    options = surface_options(args)
    options["bulk_terms"] = False
    initargs = (
        corpus_label,
        corpus,
        corpus_terms,
        context_index,
        options,
    )
    try:
        with ProcessPoolExecutor(
            max_workers=jobs,
            mp_context=process_context(),
            initializer=initialize_surface_worker,
            initargs=initargs,
        ) as executor:
            return [
                result
                for chunk_results in executor.map(process_surface_term_indexes, chunks)
                for result in chunk_results
            ]
    except PermissionError:
        initialize_surface_worker(*initargs)
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            return [
                result
                for chunk_results in executor.map(process_surface_term_indexes, chunks)
                for result in chunk_results
            ]


def chunk_indexes(item_count: int, jobs: int) -> list[tuple[int, ...]]:
    chunk_size = max(1, (item_count + jobs - 1) // jobs)
    return [
        tuple(range(index, min(item_count, index + chunk_size)))
        for index in range(0, item_count, chunk_size)
    ]


def process_surface_term(
    corpus_label: str,
    corpus,
    term: SurfaceTerm,
    corpus_terms: list[SurfaceTerm],
    context_index,
    options: dict[str, object],
) -> SurfaceTermResult:
    accumulator = SurfaceTermAccumulator(term=term)

    if len(term.normalized_term) < int(options["min_term_length"]):
        accumulator.status = "skipped_short_term"
    else:
        effective_max_skip = effective_max_skip_for_normalized(
            len(corpus.text),
            len(term.normalized_term),
            int(options["min_skip"]),
            int(options["max_skip"]),
            str(options.get("max_skip_mode", "fixed")),
            options.get("max_skip_limit"),
        )
        accumulator.max_skip = effective_max_skip
        if effective_max_skip is None:
            accumulator.status = "skipped_no_valid_skip"
            return surface_result_from_accumulator(corpus_label, accumulator)
        hits = find_els(
            corpus,
            term.term,
            min_skip=int(options["min_skip"]),
            max_skip=effective_max_skip,
            direction=str(options["direction"]),
            max_hits=options["max_hits_per_term"],
        )
        for hit in hits:
            record_surface_hit(
                accumulator,
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                hit,
                bool(options["include_all"]),
            )
    return surface_result_from_accumulator(corpus_label, accumulator)


def process_surface_term_group(
    corpus_label: str,
    corpus,
    terms: list[SurfaceTerm],
    corpus_terms: list[SurfaceTerm],
    context_index,
    options: dict[str, object],
) -> list[SurfaceTermResult]:
    accumulators = [SurfaceTermAccumulator(term=term) for term in terms]
    active_accumulators: list[SurfaceTermAccumulator] = []
    accumulators_by_query: dict[str, list[SurfaceTermAccumulator]] = {}
    min_term_length = int(options["min_term_length"])
    for accumulator in accumulators:
        if len(accumulator.term.normalized_term) < min_term_length:
            accumulator.status = "skipped_short_term"
        else:
            effective_max_skip = effective_max_skip_for_normalized(
                len(corpus.text),
                len(accumulator.term.normalized_term),
                int(options["min_skip"]),
                int(options["max_skip"]),
                str(options.get("max_skip_mode", "fixed")),
                options.get("max_skip_limit"),
            )
            accumulator.max_skip = effective_max_skip
            if effective_max_skip is None:
                accumulator.status = "skipped_no_valid_skip"
                continue
            active_accumulators.append(accumulator)
            accumulators_by_query.setdefault(
                accumulator.term.normalized_term,
                [],
            ).append(accumulator)

    if active_accumulators:
        if bool(options.get("bulk_terms", True)):
            process_surface_group_matches(
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                accumulators_by_query,
                options,
            )
        else:
            process_surface_group_by_lane_finds(
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                active_accumulators,
                options,
            )

    return [
        surface_result_from_accumulator(corpus_label, accumulator)
        for accumulator in accumulators
    ]


def process_surface_group_by_lane_finds(
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    accumulators: list[SurfaceTermAccumulator],
    options: dict[str, object],
) -> None:
    min_skip = int(options["min_skip"])
    max_skip = max(
        (int(accumulator.max_skip) for accumulator in accumulators if accumulator.max_skip),
        default=min_skip,
    )
    direction = str(options["direction"])
    max_hits_per_term = options["max_hits_per_term"]
    text_length = len(corpus.text)
    for skip in range(min_skip, max_skip + 1):
        lanes = make_lanes(corpus.text, skip)
        if direction in {"forward", "both"}:
            process_surface_group_direction(
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                accumulators,
                lanes,
                skip,
                text_length,
                max_hits_per_term,
                bool(options["include_all"]),
            )
        if direction in {"backward", "both"}:
            process_surface_group_direction(
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                accumulators,
                lanes,
                -skip,
                text_length,
                max_hits_per_term,
                bool(options["include_all"]),
            )


def process_surface_group_direction(
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    accumulators: list[SurfaceTermAccumulator],
    lanes: list[str],
    skip: int,
    text_length: int,
    max_hits_per_term,
    include_all: bool,
) -> None:
    forward_skip = abs(skip)
    for accumulator in accumulators:
        if max_hits_per_term is not None and accumulator.hit_count >= max_hits_per_term:
            continue
        if accumulator.max_skip is not None and forward_skip > accumulator.max_skip:
            continue
        query = accumulator.term.normalized_term
        if skip < 0:
            query = query[::-1]
        for low, high in iter_forward_matches_in_lanes(
            lanes,
            query,
            forward_skip,
            text_length=text_length,
        ):
            if skip > 0:
                hit = build_hit(
                    corpus,
                    accumulator.term.term,
                    accumulator.term.normalized_term,
                    skip,
                    low,
                    high,
                )
            else:
                hit = build_hit(
                    corpus,
                    accumulator.term.term,
                    accumulator.term.normalized_term,
                    skip,
                    high,
                    low,
                )
            record_surface_hit(
                accumulator,
                corpus_label,
                corpus,
                corpus_terms,
                context_index,
                hit,
                include_all,
            )
            if max_hits_per_term is not None and accumulator.hit_count >= max_hits_per_term:
                break


def process_surface_group_matches(
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    accumulators_by_query: dict[str, list[SurfaceTermAccumulator]],
    options: dict[str, object],
) -> None:
    max_hits_per_term = options["max_hits_per_term"]
    include_all = bool(options["include_all"])
    matches = iter_els_query_matches_by_lanes(
        corpus.text,
        accumulators_by_query,
        min_skip=int(options["min_skip"]),
        max_skip=max(
            (
                accumulator.max_skip
                for accumulators in accumulators_by_query.values()
                for accumulator in accumulators
                if accumulator.max_skip
            ),
            default=int(options["min_skip"]),
        ),
        direction=str(options["direction"]),
        max_skip_by_query={
            query: max(
                accumulator.max_skip or int(options["min_skip"])
                for accumulator in accumulators
            )
            for query, accumulators in accumulators_by_query.items()
        },
    )
    if max_hits_per_term is not None:
        matches = iter_ordered_surface_matches(matches)
    for query, skip, start, end in matches:
        record_surface_query_match(
            corpus_label,
            corpus,
            corpus_terms,
            context_index,
            accumulators_by_query,
            query,
            skip,
            start,
            end,
            max_hits_per_term,
            include_all,
        )


def iter_ordered_surface_matches(
    matches,
):
    return iter(sorted(matches, key=surface_match_sort_key))


def surface_match_sort_key(match) -> tuple[str, int, int, int, int]:
    query, skip, start, end = match
    return (
        query,
        abs(skip),
        0 if skip > 0 else 1,
        min(start, end),
        max(start, end),
    )


def record_surface_query_match(
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    accumulators_by_query: dict[str, list[SurfaceTermAccumulator]],
    query: str,
    skip: int,
    start: int,
    end: int,
    max_hits_per_term,
    include_all: bool,
) -> None:
    for accumulator in accumulators_by_query[query]:
        if max_hits_per_term is not None and accumulator.hit_count >= max_hits_per_term:
            continue
        hit = build_hit(
            corpus,
            accumulator.term.term,
            accumulator.term.normalized_term,
            skip,
            start,
            end,
        )
        record_surface_hit(
            accumulator,
            corpus_label,
            corpus,
            corpus_terms,
            context_index,
            hit,
            include_all,
        )


def record_surface_hit(
    accumulator: SurfaceTermAccumulator,
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    hit: ELSHit,
    include_all: bool,
) -> None:
    accumulator.hit_count += 1
    context = surface_context_for_hit_indexed(
        corpus,
        hit,
        accumulator.term,
        corpus_terms,
        context_index,
    )
    if context.center_exact:
        accumulator.exact_center_hits += 1
    if context.center_word_exact:
        accumulator.exact_center_word_hits += 1
    if context.center_same_concept:
        accumulator.concept_center_hits += 1
    if context.center_word_same_concept:
        accumulator.concept_center_word_hits += 1
    if context.center_same_category:
        accumulator.category_center_hits += 1
    if context.center_word_same_category:
        accumulator.category_center_word_hits += 1
    if context.span_exact:
        accumulator.exact_span_hits += 1
    if context.span_same_concept:
        accumulator.concept_span_hits += 1
    if context.span_same_category:
        accumulator.category_span_hits += 1
    if context.has_context:
        accumulator.context_count += 1
    if include_all or context.has_context:
        accumulator.surface_rows.append(
            surface_context_row(corpus_label, accumulator.term, hit, context)
        )


def surface_result_from_accumulator(
    corpus_label: str,
    accumulator: SurfaceTermAccumulator,
) -> SurfaceTermResult:
    term = accumulator.term
    return SurfaceTermResult(
        summary_row={
            "corpus": corpus_label,
            "term_source": term.term_source,
            "term_id": term.term_id,
            "concept": term.concept,
            "category": term.category,
            "term": term.term,
            "normalized_term": term.normalized_term,
            "normalized_length": len(term.normalized_term),
            "max_skip": accumulator.max_skip or "",
            "hit_count": accumulator.hit_count,
            "context_hit_count": accumulator.context_count,
            "exact_center_word_hits": accumulator.exact_center_word_hits,
            "same_concept_center_word_hits": accumulator.concept_center_word_hits,
            "same_category_center_word_hits": accumulator.category_center_word_hits,
            "exact_center_hits": accumulator.exact_center_hits,
            "same_concept_center_hits": accumulator.concept_center_hits,
            "same_category_center_hits": accumulator.category_center_hits,
            "exact_span_hits": accumulator.exact_span_hits,
            "same_concept_span_hits": accumulator.concept_span_hits,
            "same_category_span_hits": accumulator.category_span_hits,
            "status": accumulator.status,
        },
        surface_rows=accumulator.surface_rows,
    )


def surface_options(args: argparse.Namespace) -> dict[str, object]:
    return {
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "max_skip_mode": args.max_skip_mode,
        "max_skip_limit": args.max_skip_limit,
        "direction": args.direction,
        "min_term_length": args.min_term_length,
        "max_hits_per_term": args.max_hits_per_term,
        "include_all": args.include_all,
    }


def resolve_surface_jobs(jobs: int, term_count: int) -> int:
    if jobs < 0:
        raise SystemExit("--jobs must be >= 0")
    if jobs == 0:
        jobs = os.cpu_count() or 1
    return max(1, min(jobs, max(1, term_count)))


_SURFACE_WORKER_CORPUS_LABEL = ""
_SURFACE_WORKER_CORPUS = None
_SURFACE_WORKER_TERMS: list[SurfaceTerm] = []
_SURFACE_WORKER_CONTEXT_INDEX = None
_SURFACE_WORKER_OPTIONS: dict[str, object] = {}


def initialize_surface_worker(
    corpus_label: str,
    corpus,
    corpus_terms: list[SurfaceTerm],
    context_index,
    options: dict[str, object],
) -> None:
    global _SURFACE_WORKER_CORPUS_LABEL
    global _SURFACE_WORKER_CORPUS
    global _SURFACE_WORKER_TERMS
    global _SURFACE_WORKER_CONTEXT_INDEX
    global _SURFACE_WORKER_OPTIONS

    _SURFACE_WORKER_CORPUS_LABEL = corpus_label
    _SURFACE_WORKER_CORPUS = corpus
    _SURFACE_WORKER_TERMS = corpus_terms
    _SURFACE_WORKER_CONTEXT_INDEX = context_index
    _SURFACE_WORKER_OPTIONS = options


def clear_surface_worker() -> None:
    initialize_surface_worker("", None, [], None, {})


def process_surface_term_index(index: int) -> SurfaceTermResult:
    if _SURFACE_WORKER_CORPUS is None or _SURFACE_WORKER_CONTEXT_INDEX is None:
        raise RuntimeError("surface worker is not initialized")
    return process_surface_term(
        _SURFACE_WORKER_CORPUS_LABEL,
        _SURFACE_WORKER_CORPUS,
        _SURFACE_WORKER_TERMS[index],
        _SURFACE_WORKER_TERMS,
        _SURFACE_WORKER_CONTEXT_INDEX,
        _SURFACE_WORKER_OPTIONS,
    )


def process_surface_term_indexes(indexes: tuple[int, ...]) -> list[SurfaceTermResult]:
    if _SURFACE_WORKER_CORPUS is None or _SURFACE_WORKER_CONTEXT_INDEX is None:
        raise RuntimeError("surface worker is not initialized")
    return process_surface_term_group(
        _SURFACE_WORKER_CORPUS_LABEL,
        _SURFACE_WORKER_CORPUS,
        [_SURFACE_WORKER_TERMS[index] for index in indexes],
        _SURFACE_WORKER_TERMS,
        _SURFACE_WORKER_CONTEXT_INDEX,
        _SURFACE_WORKER_OPTIONS,
    )


def cmd_gematria_year(args: argparse.Namespace) -> int:
    print(
        json.dumps(
            {
                "year": args.year,
                "compact_thousands": hebrew_year_compact(args.year),
                "additive_full_value": hebrew_year_additive(args.year),
                "year_remainder": hebrew_year_remainder(args.year),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def parse_term_set_args(raw_term_sets: list[str]) -> list[BatchTermSet]:
    term_sets: list[BatchTermSet] = []
    labels: set[str] = set()
    for raw in raw_term_sets:
        if "=" not in raw:
            raise SystemExit(f"--term-set must be label=terms_csv: {raw}")
        label, path = raw.split("=", 1)
        label = label.strip()
        path = path.strip()
        if not label or not path:
            raise SystemExit(f"--term-set must be label=terms_csv: {raw}")
        if not is_safe_report_label(label):
            raise SystemExit(
                "--term-set label may contain only letters, digits, underscore, or hyphen: "
                f"{label}"
            )
        if label in labels:
            raise SystemExit(f"duplicate --term-set label: {label}")
        labels.add(label)
        term_sets.append(BatchTermSet(label=label, path=path, rows=read_term_rows(path)))
    return term_sets


def collect_hits_by_term(
    corpus,
    term_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, list[ELSHit]]:
    hits_by_term: dict[str, list[ELSHit]] = {}
    for term_row in term_rows:
        term = term_row.get("term", "")
        normalized = normalize_for_corpus(corpus, term)
        if len(normalized) < args.min_term_length:
            hits_by_term[term_row["term_id"]] = []
            continue
        effective_max_skip = effective_max_skip_for_query(corpus, normalized, args)
        if effective_max_skip is None:
            hits_by_term[term_row["term_id"]] = []
            continue
        hits_by_term[term_row["term_id"]] = list(
            find_els(
                corpus,
                term,
                min_skip=args.min_skip,
                max_skip=effective_max_skip,
                direction=args.direction,
            )
        )
    return hits_by_term


def build_hit_center_index(hits_by_term: dict[str, list[ELSHit]]) -> dict[str, dict[str, object]]:
    indexed = {}
    for term_id, hits in hits_by_term.items():
        sorted_hits = sorted(hits, key=hit_center)
        indexed[term_id] = {
            "hits": sorted_hits,
            "centers": [hit_center(hit) for hit in sorted_hits],
        }
    return indexed


def nearest_hit_by_center(
    hit: ELSHit,
    indexed_hits: dict[str, object],
) -> tuple[ELSHit, float] | None:
    hits = indexed_hits["hits"]
    centers = indexed_hits["centers"]
    if not hits:
        return None
    center = hit_center(hit)
    insert_at = bisect_left(centers, center)
    candidate_indexes = [insert_at - 1, insert_at, insert_at + 1]
    best: tuple[ELSHit, float] | None = None
    for index in candidate_indexes:
        if index < 0 or index >= len(hits):
            continue
        distance = abs(center - centers[index])
        if best is None or distance < best[1]:
            best = (hits[index], distance)
    return best


def surface_context_row(corpus_label: str, term: SurfaceTerm, hit: ELSHit, context) -> dict[str, object]:
    row = {
        "corpus": corpus_label,
        "term_source": term.term_source,
        "term_id": term.term_id,
        "concept": term.concept,
        "category": term.category,
    }
    row.update(hit.as_row())
    row.update(
        {
            "best_context": context.best_context,
            "center_word_exact": context.center_word_exact,
            "center_word_same_concept": context.center_word_same_concept,
            "center_word_same_category": context.center_word_same_category,
            "center_exact": context.center_exact,
            "center_same_concept": context.center_same_concept,
            "center_same_category": context.center_same_category,
            "span_exact": context.span_exact,
            "span_same_concept": context.span_same_concept,
            "span_same_category": context.span_same_category,
            "center_word_same_concept_terms": context.center_word_same_concept_terms,
            "center_word_same_category_terms": context.center_word_same_category_terms,
            "center_same_concept_terms": context.center_same_concept_terms,
            "center_same_category_terms": context.center_same_category_terms,
            "span_exact_refs": context.span_exact_refs,
            "span_same_concept_refs": context.span_same_concept_refs,
            "span_same_category_refs": context.span_same_category_refs,
        }
    )
    return row


def extension_row(corpus_label: str, hit: ELSHit, extension) -> dict[str, object]:
    row = {"corpus": corpus_label}
    row.update(hit.as_row())
    row.update(
        {
            "extension_type": extension.extension_type,
            "extension_side": extension.extension_side,
            "extension_length": extension.extension_length,
            "before_letters": extension.before_letters,
            "after_letters": extension.after_letters,
            "extended_sequence": extension.extended_sequence,
            "matched_normalized": extension.matched_normalized,
            "match_kind": extension.match_kind,
            "match_count": extension.match_count,
            "matched_examples": extension.matched_examples,
            "matched_refs": extension.matched_refs,
            "extension_start_offset": extension.extension_start_offset,
            "extension_end_offset": extension.extension_end_offset,
            "extension_start_ref": extension.extension_start_ref,
            "extension_end_ref": extension.extension_end_ref,
        }
    )
    return row


def matrix_letter_row(corpus_label: str, hit: ELSHit, letter, row_width: int) -> dict[str, object]:
    return {
        "corpus": corpus_label,
        "hit_index": letter.hit_index,
        "term": hit.term,
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "letter_index": letter.letter_index,
        "letter": letter.letter,
        "offset": letter.offset,
        "row_width": row_width,
        "row": letter.row,
        "col": letter.col,
        "ref": letter.ref,
        "word_index": letter.word_index,
        "word": letter.word,
        "normalized_word": letter.normalized_word,
        "start_ref": hit.start_ref,
        "end_ref": hit.end_ref,
        "center_ref": hit.center_ref,
    }


def matrix_summary_row(corpus_label: str, hit: ELSHit, summary) -> dict[str, object]:
    return {
        "corpus": corpus_label,
        "hit_index": summary.hit_index,
        "term": hit.term,
        "normalized_term": hit.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "row_width": summary.row_width,
        "min_row": summary.min_row,
        "max_row": summary.max_row,
        "min_col": summary.min_col,
        "max_col": summary.max_col,
        "rows_spanned": summary.rows_spanned,
        "cols_spanned": summary.cols_spanned,
        "letter_count": summary.letter_count,
        "first_offset": summary.first_offset,
        "last_offset": summary.last_offset,
        "start_ref": hit.start_ref,
        "end_ref": hit.end_ref,
        "center_ref": hit.center_ref,
    }


def skip_plan_row(plan) -> dict[str, object]:
    return {
        "term": plan.term,
        "normalized_term": plan.normalized_term,
        "normalized_length": plan.normalized_length,
        "min_skip": plan.min_skip,
        "max_skip_limit": plan.max_skip_limit,
        "selected_max_skip": plan.selected_max_skip,
        "direction": plan.direction,
        "target_expected_hits": round(plan.target_expected_hits, 6),
        "expected_hits": round(plan.expected_hits, 6),
        "expected_at_min_skip": round(plan.expected_at_min_skip, 6),
        "status": plan.status,
    }


def add_extension_summary_group(
    groups: dict[tuple[str, ...], dict[str, object]],
    row: dict[str, str],
    extension_length: int,
) -> None:
    key = (
        row.get("corpus", ""),
        row.get("term", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("direction", ""),
        row.get("extension_type", ""),
        row.get("extension_side", ""),
        row.get("match_kind", ""),
    )
    group = groups.setdefault(
        key,
        {
            "corpus": key[0],
            "term": key[1],
            "normalized_term": key[2],
            "skip": key[3],
            "direction": key[4],
            "extension_type": key[5],
            "extension_side": key[6],
            "match_kind": key[7],
            "rows": 0,
            "unique_extended_sequences": set(),
            "max_extension_length": 0,
            "max_match_count": 0,
        },
    )
    group["rows"] = int(group["rows"]) + 1
    unique_sequences = group["unique_extended_sequences"]
    assert isinstance(unique_sequences, set)
    unique_sequences.add(row.get("extended_sequence", ""))
    group["max_extension_length"] = max(
        int(group["max_extension_length"]),
        extension_length,
    )
    group["max_match_count"] = max(
        int(group["max_match_count"]),
        int_or_zero(row.get("match_count", "")),
    )


def extension_summary_rows(
    groups: dict[tuple[str, ...], dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for group in groups.values():
        unique_sequences = group["unique_extended_sequences"]
        assert isinstance(unique_sequences, set)
        rows.append(
            {
                "corpus": group["corpus"],
                "term": group["term"],
                "normalized_term": group["normalized_term"],
                "skip": group["skip"],
                "direction": group["direction"],
                "extension_type": group["extension_type"],
                "extension_side": group["extension_side"],
                "match_kind": group["match_kind"],
                "rows": group["rows"],
                "unique_extended_sequences": len(unique_sequences),
                "max_extension_length": group["max_extension_length"],
                "max_match_count": group["max_match_count"],
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            str(row["corpus"]),
            str(row["term"]),
            int_or_zero(row["skip"]),
            str(row["direction"]),
            str(row["extension_type"]),
            str(row["match_kind"]),
        ),
    )


def extension_score(row: dict[str, str], extension_length: int) -> int:
    return score_extension(
        row.get("extension_type", ""),
        extension_length,
        row.get("match_kind", ""),
        int_or_zero(row.get("match_count", "")),
    )


def extension_rank_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        int_or_zero(row.get("extension_score", "")),
        int_or_zero(row.get("extension_length", "")),
        EXTENSION_TYPE_PRIORITY.get(str(row.get("extension_type", "")), 0),
        int_or_zero(row.get("match_count", "")),
        str(row.get("corpus", "")),
        str(row.get("term", "")),
        str(row.get("extended_sequence", "")),
    )


def hit_from_row(row: dict[str, str]) -> ELSHit:
    start_offset = int(row["start_offset"])
    end_offset = int(row["end_offset"])
    center_offset = row.get("center_offset")
    if center_offset in (None, ""):
        center_offset = str((min(start_offset, end_offset) + max(start_offset, end_offset)) // 2)
    return ELSHit(
        term=row["term"],
        normalized_term=row["normalized_term"],
        skip=int(row["skip"]),
        start_offset=start_offset,
        end_offset=end_offset,
        span_letters=int(row["span_letters"]),
        sequence=row["sequence"],
        start_ref=row["start_ref"],
        end_ref=row["end_ref"],
        start_source=row["start_source"],
        end_source=row["end_source"],
        center_offset=int(center_offset),
        center_ref=row.get("center_ref", ""),
        center_source=row.get("center_source", ""),
        center_word_index=int_or_empty(row.get("center_word_index", "")),
        center_word=row.get("center_word", ""),
        center_normalized_word=row.get("center_normalized_word", ""),
    )


def hit_with_corpus_center(corpus, hit: ELSHit) -> ELSHit:
    if hit.center_ref and hit.center_word:
        return hit
    word = corpus.word_at(hit.center_offset)
    return replace(
        hit,
        center_ref=hit.center_ref or corpus.ref_at(hit.center_offset),
        center_source=hit.center_source or corpus.source_at(hit.center_offset),
        center_word_index=(
            hit.center_word_index
            if hit.center_word_index != ""
            else (word.word_index if word is not None else "")
        ),
        center_word=hit.center_word or (word.raw_word if word is not None else ""),
        center_normalized_word=(
            hit.center_normalized_word
            or (word.normalized_word if word is not None else "")
        ),
    )


def int_or_empty(value: str) -> int | str:
    value = str(value)
    if value == "":
        return ""
    return int(value)


def int_or_zero(value: object) -> int:
    if value in (None, ""):
        return 0
    return int(value)


@contextmanager
def open_hits_writer(output_path: str | None):
    if output_path:
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            writer.writeheader()
            yield writer
        return

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
    writer.writeheader()
    yield writer


def write_hits(hits, output_path: str | None) -> None:
    with open_hits_writer(output_path) as writer:
        writer.writerows(hit.as_row() for hit in hits)


def write_batch_rows(rows: list[dict[str, object]], output_path: str | Path) -> None:
    with open_dict_writer(output_path, BATCH_FIELDNAMES) as writer:
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
