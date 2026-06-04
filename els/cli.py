"""Command-line interface for Open Bible Codes."""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from . import __version__
from .corpus import load_corpus
from .search import (
    ELSHit,
    build_hit,
    find_els,
    iter_els_query_matches_by_lanes,
    iter_forward_matches_in_lanes,
    make_lanes,
    process_context,
)
from .surface import (
    SurfaceTerm,
    build_surface_context_index,
    normalize_verses,
    surface_context_for_hit_indexed,
)
from .io import (
    open_dict_writer,
    write_dict_rows,
    write_run_manifest,
)
from .term_io import (
    accepted_term_languages,
    build_surface_terms,
    parse_corpus_args,
    read_term_rows_many,
)
from .rows import (
    FIELDNAMES,
    SURFACE_CONTEXT_FIELDNAMES,
    hit_from_row,
    hit_with_corpus_center,
    surface_context_row,
)
from .commands.batch import cmd_batch, cmd_batch_many
from .commands.extension_summary import cmd_extension_summary
from .commands.extensions import cmd_extensions
from .commands.gematria import cmd_gematria_year
from .commands.matrix import cmd_matrix
from .commands.pairs import cmd_pairs
from .commands.search import cmd_search
from .commands.skip_plan import cmd_skip_plan
from .commands.stats import cmd_stats
from .maxskip import effective_max_skip_for_normalized


MAX_SKIP_MODES = ("fixed", "full-span", "letters-per-term")

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


if __name__ == "__main__":
    raise SystemExit(main())
