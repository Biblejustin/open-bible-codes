#!/usr/bin/env python3
"""Run paired controls for filtered same-skip extension top rows."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.extensions import (
    ExtensionLexicon,
    ExtensionMatch,
    build_extension_lexicon,
    extension_score as score_extension,
)
from els.search import iter_els_query_matches_by_lanes, process_context, resolve_count_jobs
from els.statistics import (
    benjamini_hochberg_q_values,
    numeric_value,
    round_float,
    tail_p_value_ge,
)
from els.term_display import display_term


BASE = Path("reports/protocols/public_baseline")
TOP_FILES = [
    BASE / "surface_context_extensions_tr_nt_top.csv",
    BASE / "surface_context_extensions_sblgnt_top.csv",
]
SURFACE_CONTEXT_HITS = BASE / "surface_context_hits.csv"
CORPUS_CONFIGS = {
    "MT_WLC": Path("configs/example_oshb_wlc.toml"),
    "UXLC": Path("configs/example_uxlc.toml"),
    "EBIBLE_WLC": Path("configs/example_ebible_hebwlc.toml"),
    "MAM": Path("configs/example_mam.toml"),
    "UHB": Path("configs/example_uhb.toml"),
    "TR_NT": Path("configs/example_ebible_grctr.toml"),
    "BYZ_NT": Path("configs/example_ebible_grcmt.toml"),
    "TCG_NT": Path("configs/example_ebible_grctcgnt.toml"),
    "SBLGNT": Path("configs/example_sblgnt.toml"),
    "KJV": Path("configs/example_ebible_engkjv.toml"),
}

SUMMARY_OUT = Path("reports/extension_paired_controls_summary.csv")
EXAMPLES_OUT = Path("reports/extension_paired_controls_examples.csv")
MD_OUT = Path("reports/extension_paired_controls.md")
MANIFEST_OUT = Path("reports/extension_paired_controls.manifest.json")

STRONG_EXTENSION_TYPES = {
    "before_plus_term",
    "term_plus_after",
    "before_plus_term_plus_after",
}
SUMMARY_FIELDNAMES = [
    "target_id",
    "corpus",
    "overlap_key",
    "overlap_corpora",
    "overlap_group_size",
    "term",
    "normalized_term",
    "concept",
    "category",
    "skip",
    "direction",
    "extension_type",
    "extension_side",
    "extension_length",
    "extended_sequence",
    "matched_examples",
    "matched_refs",
    "observed_score",
    "observed_match_count",
    "term_control_samples",
    "term_same_type_score_mean",
    "term_same_type_score_max",
    "term_same_type_ge_observed",
    "term_same_type_p_ge",
    "term_any_score_mean",
    "term_any_score_max",
    "term_any_ge_observed",
    "term_any_p_ge",
    "random_control_samples",
    "random_same_type_score_mean",
    "random_same_type_score_max",
    "random_same_type_ge_observed",
    "random_same_type_p_ge",
    "random_any_score_mean",
    "random_any_score_max",
    "random_any_ge_observed",
    "random_any_p_ge",
    "combined_min_p",
    "combined_min_q",
    "all_controls_max_p",
    "all_controls_max_q",
    "extension_band",
    "all_controls_band",
    "warning_count",
    "flags",
    "read",
    "all_controls_read",
]

EXAMPLE_FIELDNAMES = [
    *SUMMARY_FIELDNAMES,
    "term_same_type_scores_sample",
    "term_any_scores_sample",
    "term_queries_sample",
    "random_same_type_scores_sample",
    "random_any_scores_sample",
    "random_queries_sample",
]


@dataclass(frozen=True)
class ExtensionTarget:
    target_id: str
    source_file: str
    row: dict[str, str]

    @property
    def corpus(self) -> str:
        return self.row["corpus"]

    @property
    def normalized_term(self) -> str:
        return self.row["normalized_term"]

    @property
    def skip(self) -> int:
        return int(self.row["skip"])

    @property
    def direction(self) -> str:
        return self.row["direction"]

    @property
    def extension_type(self) -> str:
        return self.row["extension_type"]

    @property
    def observed_score(self) -> int:
        return int_or_zero(self.row.get("extension_score"))

    @property
    def overlap_key(self) -> str:
        return "|".join(
            [
                self.row.get("normalized_term", ""),
                self.row.get("skip", ""),
                self.row.get("direction", ""),
                self.row.get("extension_type", ""),
                self.row.get("extended_sequence", ""),
                self.row.get("matched_normalized", ""),
            ]
        )


@dataclass(frozen=True)
class ControlScores:
    same_type_scores: tuple[int, ...]
    any_scores: tuple[int, ...]
    queries: tuple[str, ...]


@dataclass(frozen=True)
class ExtensionControlRow:
    row: dict[str, object]
    term_controls: ControlScores
    random_controls: ControlScores


@dataclass(frozen=True)
class TargetControlQueries:
    target: ExtensionTarget
    term_queries: tuple[str, ...]
    random_queries: tuple[str, ...]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.require_center_exact and args.surface_context_hits is None:
        args.surface_context_hits = SURFACE_CONTEXT_HITS
    targets = read_targets(args.top_file or TOP_FILES)
    surface_context = (
        read_surface_context(args.surface_context_hits)
        if args.require_center_exact and args.surface_context_hits is not None
        else {}
    )
    targets = prepare_targets(targets, args, surface_context=surface_context)
    rows, corpus_manifests = analyze_target_corpora(targets, args)

    annotate_rows(rows)
    sorted_rows = sorted(rows, key=control_row_sort_key)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [row.row for row in sorted_rows])
    write_rows(
        args.examples_out,
        EXAMPLE_FIELDNAMES,
        example_rows(sorted_rows, args.max_examples),
    )
    write_markdown(
        args.markdown_out,
        [row.row for row in sorted_rows],
        title=args.title,
        lead=args.lead,
        caution=args.caution,
    )
    write_manifest(args, targets, corpus_manifests, len(rows), started)

    print(args.summary_out)
    print(args.examples_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-file", action="append", type=Path)
    parser.add_argument("--term-control-samples", type=int, default=25)
    parser.add_argument("--random-control-samples", type=int, default=25)
    parser.add_argument("--seed", type=int, default=2718)
    parser.add_argument("--max-before", type=int, default=12)
    parser.add_argument("--max-after", type=int, default=12)
    parser.add_argument("--phrase-words", type=int, default=4)
    parser.add_argument("--include-both-sided", action="store_true", default=True)
    parser.add_argument("--no-include-both-sided", dest="include_both_sided", action="store_false")
    parser.add_argument("--max-extensions-per-hit", type=int, default=20)
    parser.add_argument("--min-extension-length", type=int, default=3)
    parser.add_argument("--match-kind-prefix", default="phrase_")
    parser.add_argument("--require-cross-corpus-overlap", action="store_true")
    parser.add_argument(
        "--require-overlap-corpus",
        action="append",
        default=[],
        help="Require each overlap key group to include this corpus label. Repeatable.",
    )
    parser.add_argument("--dedupe-targets", action="store_true")
    parser.add_argument("--include-overlap-key", action="append", default=[])
    parser.add_argument("--surface-context-hits", type=Path)
    parser.add_argument("--require-center-exact", action="store_true")
    parser.add_argument("--max-examples", type=int, default=80)
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Corpus workers for paired controls. Use 0 for all available CPUs.",
    )
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--title", default="Extension Paired Controls")
    parser.add_argument(
        "--lead",
        default=(
            "This report compares extension-top rows against shuffled-term and "
            "same-corpus random controls at the same skip and direction."
        ),
    )
    parser.add_argument(
        "--caution",
        default=(
            "Controls are row-local and exploratory. Low scores mainly identify "
            "rows worth manual review, not statistical claims."
        ),
    )
    return parser


def read_targets(paths: list[Path]) -> list[ExtensionTarget]:
    targets = []
    for path in paths:
        for index, row in enumerate(read_rows(path), start=1):
            row = normalize_target_row(row)
            targets.append(
                ExtensionTarget(
                    target_id=f"{row['corpus']}_{index:03d}",
                    source_file=str(path),
                    row=row,
                )
            )
    return targets


def normalize_target_row(row: dict[str, str]) -> dict[str, str]:
    normalized = dict(row)
    if not normalized.get("corpus") and normalized.get("audit_corpus"):
        normalized["corpus"] = normalized["audit_corpus"]
    return normalized


def prepare_targets(
    targets: list[ExtensionTarget],
    args: argparse.Namespace,
    *,
    surface_context: dict[tuple[str, ...], dict[str, str]] | None = None,
) -> list[ExtensionTarget]:
    if args.require_cross_corpus_overlap:
        targets = cross_corpus_overlap_targets(targets)
    targets = require_overlap_corpora_targets(
        targets,
        set(getattr(args, "require_overlap_corpus", [])),
    )
    if args.include_overlap_key:
        targets = include_overlap_key_targets(targets, set(args.include_overlap_key))
    if args.require_center_exact:
        targets = center_exact_targets(targets, surface_context or {})
    if args.dedupe_targets:
        targets = dedupe_targets(targets)
    annotate_overlap_fields(targets)
    return targets


def read_surface_context(path: Path) -> dict[tuple[str, ...], dict[str, str]]:
    return {surface_context_key(row): row for row in read_rows(path)}


def center_exact_targets(
    targets: list[ExtensionTarget],
    surface_context: dict[tuple[str, ...], dict[str, str]],
) -> list[ExtensionTarget]:
    return [
        target
        for target in targets
        if surface_context.get(surface_context_key(target.row), {}).get("center_exact") == "True"
    ]


def surface_context_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("corpus", ""),
        row.get("term", ""),
        row.get("normalized_term", ""),
        row.get("skip", ""),
        row.get("start_offset", ""),
        row.get("end_offset", ""),
        row.get("center_offset", ""),
    )


def cross_corpus_overlap_targets(targets: list[ExtensionTarget]) -> list[ExtensionTarget]:
    groups = targets_by_overlap_key(targets)
    overlap_keys = {
        key
        for key, group in groups.items()
        if len({target.corpus for target in group}) > 1
    }
    return [target for target in targets if target.overlap_key in overlap_keys]


def require_overlap_corpora_targets(
    targets: list[ExtensionTarget],
    required_corpora: set[str],
) -> list[ExtensionTarget]:
    if not required_corpora:
        return targets
    groups = targets_by_overlap_key(targets)
    overlap_keys = {
        key
        for key, group in groups.items()
        if required_corpora <= {target.corpus for target in group}
    }
    return [target for target in targets if target.overlap_key in overlap_keys]


def include_overlap_key_targets(
    targets: list[ExtensionTarget],
    overlap_keys: set[str],
) -> list[ExtensionTarget]:
    return [target for target in targets if target.overlap_key in overlap_keys]


def dedupe_targets(targets: list[ExtensionTarget]) -> list[ExtensionTarget]:
    seen: set[tuple[str, str]] = set()
    output = []
    for target in targets:
        key = (target.corpus, target.overlap_key)
        if key in seen:
            continue
        seen.add(key)
        output.append(target)
    return output


def annotate_overlap_fields(targets: list[ExtensionTarget]) -> None:
    groups = targets_by_overlap_key(targets)
    for target in targets:
        group = groups[target.overlap_key]
        target.row["overlap_key"] = target.overlap_key
        target.row["overlap_corpora"] = ",".join(sorted({item.corpus for item in group}))
        target.row["overlap_group_size"] = str(len(group))


def targets_by_overlap_key(
    targets: list[ExtensionTarget],
) -> dict[str, list[ExtensionTarget]]:
    groups: dict[str, list[ExtensionTarget]] = {}
    for target in targets:
        groups.setdefault(target.overlap_key, []).append(target)
    return groups


def analyze_target_corpora(
    targets: list[ExtensionTarget],
    args: argparse.Namespace,
) -> tuple[list[ExtensionControlRow], list[dict[str, object]]]:
    tasks = []
    for corpus_label in sorted({target.corpus for target in targets}):
        config = CORPUS_CONFIGS.get(corpus_label)
        if config is None:
            raise SystemExit(f"no config for corpus {corpus_label}")
        tasks.append(
            (
                corpus_label,
                config,
                [target for target in targets if target.corpus == corpus_label],
                args,
            )
        )

    effective_jobs = resolve_count_jobs(args.jobs, len(tasks))
    if effective_jobs <= 1:
        results = [analyze_corpus_task(task) for task in tasks]
    else:
        try:
            executor = ProcessPoolExecutor(
                max_workers=effective_jobs,
                mp_context=process_context(),
            )
        except PermissionError:
            results = [analyze_corpus_task(task) for task in tasks]
        else:
            with executor:
                results = list(executor.map(analyze_corpus_task, tasks))

    rows: list[ExtensionControlRow] = []
    corpus_manifests = []
    for corpus_rows, corpus_manifest in results:
        rows.extend(corpus_rows)
        corpus_manifests.append(corpus_manifest)
    return rows, corpus_manifests


def analyze_corpus_task(
    task: tuple[str, Path, list[ExtensionTarget], argparse.Namespace],
) -> tuple[list[ExtensionControlRow], dict[str, object]]:
    corpus_label, config, corpus_targets, args = task
    corpus_started = time.perf_counter()
    corpus = load_corpus(config)
    lexicon = build_extension_lexicon(corpus, max_phrase_words=args.phrase_words)
    return (
        analyze_corpus(corpus, lexicon, corpus_targets, args),
        {
            "label": corpus_label,
            "config": str(config),
            "summary": corpus.summary(),
            "targets": len(corpus_targets),
            "seconds": round(time.perf_counter() - corpus_started, 3),
        },
    )


def analyze_corpus(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    targets: list[ExtensionTarget],
    args: argparse.Namespace,
) -> list[ExtensionControlRow]:
    alphabet, weights = weighted_alphabet(corpus.text)
    target_queries = [
        TargetControlQueries(
            target=target,
            term_queries=sample_term_controls(
                target.normalized_term,
                samples=args.term_control_samples,
                rng=random.Random(stable_seed(args.seed, target.target_id, "term")),
            ),
            random_queries=sample_random_controls(
                length=len(target.normalized_term),
                samples=args.random_control_samples,
                rng=random.Random(stable_seed(args.seed, target.target_id, "random")),
                alphabet=alphabet,
                weights=weights,
            ),
        )
        for target in targets
    ]
    grouped_scores = score_control_query_groups(corpus, lexicon, target_queries, args)
    rows = []
    for item in target_queries:
        target_scores = grouped_scores.get(score_group_key(item.target), {})
        term_controls = control_scores_for_target_queries(
            target_scores,
            item.target,
            item.term_queries,
        )
        random_controls = control_scores_for_target_queries(
            target_scores,
            item.target,
            item.random_queries,
        )
        rows.append(
            ExtensionControlRow(
                row=summary_row(item.target, term_controls, random_controls),
                term_controls=term_controls,
                random_controls=random_controls,
            )
        )
    return rows


def analyze_target(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target: ExtensionTarget,
    args: argparse.Namespace,
) -> ExtensionControlRow:
    term_queries = sample_term_controls(
        target.normalized_term,
        samples=args.term_control_samples,
        rng=random.Random(stable_seed(args.seed, target.target_id, "term")),
    )
    random_queries = sample_random_controls(
        length=len(target.normalized_term),
        corpus_text=corpus.text,
        samples=args.random_control_samples,
        rng=random.Random(stable_seed(args.seed, target.target_id, "random")),
    )
    term_controls, random_controls = score_control_sets(
        corpus,
        lexicon,
        target,
        term_queries,
        random_queries,
        args,
    )
    row = summary_row(target, term_controls, random_controls)
    return ExtensionControlRow(row=row, term_controls=term_controls, random_controls=random_controls)


def score_control_sets(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target: ExtensionTarget,
    term_queries: tuple[str, ...],
    random_queries: tuple[str, ...],
    args: argparse.Namespace,
) -> tuple[ControlScores, ControlScores]:
    unique_queries = sorted({query for query in (*term_queries, *random_queries) if query})
    scores_by_query = score_queries(corpus, lexicon, target, tuple(unique_queries), args)
    return (
        control_scores_for_queries(scores_by_query, term_queries),
        control_scores_for_queries(scores_by_query, random_queries),
    )


def score_controls(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target: ExtensionTarget,
    queries: tuple[str, ...],
    args: argparse.Namespace,
) -> ControlScores:
    return score_control_sets(corpus, lexicon, target, queries, (), args)[0]


def score_control_query_groups(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target_queries: list[TargetControlQueries],
    args: argparse.Namespace,
) -> dict[tuple[int, str, bool], dict[str, tuple[int, dict[str, int]]]]:
    queries_by_group: dict[tuple[int, str, bool], set[str]] = {}
    extension_types_by_group: dict[tuple[int, str, bool], set[str]] = {}
    for item in target_queries:
        group_key = score_group_key(item.target)
        queries_by_group.setdefault(group_key, set()).update(
            query for query in (*item.term_queries, *item.random_queries) if query
        )
        extension_types_by_group.setdefault(group_key, set()).add(item.target.extension_type)

    return {
        group_key: score_queries_for_extension_types(
            corpus,
            lexicon,
            tuple(sorted(queries)),
            skip=group_key[0],
            direction=group_key[1],
            high_priority_scale=group_key[2],
            extension_types=tuple(sorted(extension_types_by_group[group_key])),
            args=args,
        )
        for group_key, queries in queries_by_group.items()
    }


def score_group_key(target: ExtensionTarget) -> tuple[int, str, bool]:
    return (
        abs(target.skip),
        "forward" if target.skip > 0 else "backward",
        target.observed_score >= 100000,
    )


def control_scores_for_target_queries(
    scores_by_query: dict[str, tuple[int, dict[str, int]]],
    target: ExtensionTarget,
    queries: tuple[str, ...],
) -> ControlScores:
    return ControlScores(
        same_type_scores=tuple(
            scores_by_query.get(query, (0, {}))[1].get(target.extension_type, 0)
            for query in queries
        ),
        any_scores=tuple(scores_by_query.get(query, (0, {}))[0] for query in queries),
        queries=queries,
    )


def score_queries(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target: ExtensionTarget,
    queries: tuple[str, ...],
    args: argparse.Namespace,
) -> dict[str, tuple[int, int]]:
    grouped_scores = score_queries_for_extension_types(
        corpus,
        lexicon,
        queries,
        skip=abs(target.skip),
        direction="forward" if target.skip > 0 else "backward",
        high_priority_scale=target.observed_score >= 100000,
        extension_types=(target.extension_type,),
        args=args,
    )
    return {
        query: (
            query_scores[1].get(target.extension_type, 0),
            query_scores[0],
        )
        for query, query_scores in grouped_scores.items()
    }


def score_queries_for_extension_types(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    queries: tuple[str, ...],
    *,
    skip: int,
    direction: str,
    high_priority_scale: bool,
    extension_types: tuple[str, ...],
    args: argparse.Namespace,
) -> dict[str, tuple[int, dict[str, int]]]:
    extension_type_set = set(extension_types)
    scores_by_query = {
        query: (0, {extension_type: 0 for extension_type in extension_type_set})
        for query in queries
        if query
    }
    for query, signed_skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        scores_by_query,
        min_skip=skip,
        max_skip=skip,
        direction=direction,
    ):
        any_score, same_type_scores = scores_by_query[query]
        hit_any_score, hit_same_type_scores = score_hit_extensions(
            corpus,
            lexicon,
            query=query,
            signed_skip=signed_skip,
            start=start,
            end=end,
            extension_types=extension_type_set,
            high_priority_scale=high_priority_scale,
            args=args,
        )
        any_score = max(any_score, hit_any_score)
        for extension_type, score in hit_same_type_scores.items():
            same_type_scores[extension_type] = max(
                same_type_scores[extension_type],
                score,
            )
        scores_by_query[query] = (any_score, same_type_scores)
    return scores_by_query


def score_hit_extensions(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    *,
    query: str,
    signed_skip: int,
    start: int,
    end: int,
    extension_types: set[str],
    high_priority_scale: bool,
    args: argparse.Namespace,
) -> tuple[int, dict[str, int]]:
    any_score = 0
    same_type_scores = {extension_type: 0 for extension_type in extension_types}
    appended_matches = 0
    entries_get = lexicon.entries.get
    before_sequences = extension_sequences_before_text(
        corpus.text,
        start,
        signed_skip,
        args.max_before,
    )
    after_sequences = extension_sequences_after_text(
        corpus.text,
        end,
        signed_skip,
        args.max_after,
    )

    def visit(
        extension_type: str,
        extension_length: int,
        extended_sequence: str,
    ) -> bool:
        nonlocal any_score, appended_matches
        entry = entries_get(extended_sequence)
        if entry is None:
            return False
        appended_matches += 1
        if extension_fields_pass_filter(
            extension_type,
            extension_length,
            entry.match_kind,
            args,
        ):
            score = extension_score(
                extension_type,
                extension_length,
                entry.match_kind,
                entry.count,
                high_priority_scale=high_priority_scale,
            )
            any_score = max(any_score, score)
            if extension_type in extension_types:
                same_type_scores[extension_type] = max(
                    same_type_scores[extension_type],
                    score,
                )
        return (
            args.max_extensions_per_hit is not None
            and appended_matches >= args.max_extensions_per_hit
        )

    for letters in before_sequences:
        if visit("before_match", len(letters), letters):
            return any_score, same_type_scores
        if visit("before_plus_term", len(letters), letters + query):
            return any_score, same_type_scores

    for letters in after_sequences:
        if visit("after_match", len(letters), letters):
            return any_score, same_type_scores
        if visit("term_plus_after", len(letters), query + letters):
            return any_score, same_type_scores

    if args.include_both_sided:
        for before_letters in before_sequences:
            for after_letters in after_sequences:
                if visit(
                    "before_plus_term_plus_after",
                    len(before_letters) + len(after_letters),
                    before_letters + query + after_letters,
                ):
                    return any_score, same_type_scores

    return any_score, same_type_scores


def extension_sequences_before_text(
    text: str,
    start: int,
    signed_skip: int,
    max_before: int,
) -> list[str]:
    sequences: list[str] = []
    text_length = len(text)
    sequence = ""
    for length in range(1, max_before + 1):
        offset = start - signed_skip * length
        if offset < 0 or offset >= text_length:
            break
        sequence = text[offset] + sequence
        sequences.append(sequence)
    return sequences


def extension_sequences_after_text(
    text: str,
    end: int,
    signed_skip: int,
    max_after: int,
) -> list[str]:
    sequences: list[str] = []
    text_length = len(text)
    sequence = ""
    for length in range(1, max_after + 1):
        offset = end + signed_skip * length
        if offset < 0 or offset >= text_length:
            break
        sequence += text[offset]
        sequences.append(sequence)
    return sequences


def control_scores_for_queries(
    scores_by_query: dict[str, tuple[int, int]],
    queries: tuple[str, ...],
) -> ControlScores:
    return ControlScores(
        same_type_scores=tuple(scores_by_query.get(query, (0, 0))[0] for query in queries),
        any_scores=tuple(scores_by_query.get(query, (0, 0))[1] for query in queries),
        queries=queries,
    )


def extension_passes_filter(extension: ExtensionMatch, args: argparse.Namespace) -> bool:
    return extension_fields_pass_filter(
        extension.extension_type,
        extension.extension_length,
        extension.match_kind,
        args,
    )


def extension_fields_pass_filter(
    extension_type: str,
    extension_length: int,
    match_kind: str,
    args: argparse.Namespace,
) -> bool:
    if extension_type not in STRONG_EXTENSION_TYPES:
        return False
    if extension_length < args.min_extension_length:
        return False
    return not args.match_kind_prefix or match_kind.startswith(args.match_kind_prefix)


def summary_row(
    target: ExtensionTarget,
    term_controls: ControlScores,
    random_controls: ControlScores,
) -> dict[str, object]:
    observed_score = target.observed_score
    p_values = [
        p_value_ge(observed_score, term_controls.same_type_scores),
        p_value_ge(observed_score, term_controls.any_scores),
        p_value_ge(observed_score, random_controls.same_type_scores),
        p_value_ge(observed_score, random_controls.any_scores),
    ]
    p_values = [value for value in p_values if value is not None]
    flags = flags_for_row(target, term_controls, random_controls)
    return {
        "target_id": target.target_id,
        "corpus": target.row["corpus"],
        "overlap_key": target.row.get("overlap_key", target.overlap_key),
        "overlap_corpora": target.row.get("overlap_corpora", target.corpus),
        "overlap_group_size": target.row.get("overlap_group_size", "1"),
        "term": target.row["term"],
        "normalized_term": target.row["normalized_term"],
        "concept": target.row.get("concept", ""),
        "category": target.row.get("category", ""),
        "skip": target.row["skip"],
        "direction": target.row["direction"],
        "extension_type": target.row["extension_type"],
        "extension_side": target.row["extension_side"],
        "extension_length": target.row["extension_length"],
        "extended_sequence": target.row["extended_sequence"],
        "matched_examples": target.row["matched_examples"],
        "matched_refs": target.row["matched_refs"],
        "observed_score": observed_score,
        "observed_match_count": target.row["match_count"],
        "term_control_samples": len(term_controls.queries),
        "term_same_type_score_mean": round_float(mean_or_none(term_controls.same_type_scores)),
        "term_same_type_score_max": max_or_blank(term_controls.same_type_scores),
        "term_same_type_ge_observed": count_ge(observed_score, term_controls.same_type_scores),
        "term_same_type_p_ge": round_float(p_value_ge(observed_score, term_controls.same_type_scores)),
        "term_any_score_mean": round_float(mean_or_none(term_controls.any_scores)),
        "term_any_score_max": max_or_blank(term_controls.any_scores),
        "term_any_ge_observed": count_ge(observed_score, term_controls.any_scores),
        "term_any_p_ge": round_float(p_value_ge(observed_score, term_controls.any_scores)),
        "random_control_samples": len(random_controls.queries),
        "random_same_type_score_mean": round_float(
            mean_or_none(random_controls.same_type_scores)
        ),
        "random_same_type_score_max": max_or_blank(random_controls.same_type_scores),
        "random_same_type_ge_observed": count_ge(
            observed_score, random_controls.same_type_scores
        ),
        "random_same_type_p_ge": round_float(
            p_value_ge(observed_score, random_controls.same_type_scores)
        ),
        "random_any_score_mean": round_float(mean_or_none(random_controls.any_scores)),
        "random_any_score_max": max_or_blank(random_controls.any_scores),
        "random_any_ge_observed": count_ge(observed_score, random_controls.any_scores),
        "random_any_p_ge": round_float(p_value_ge(observed_score, random_controls.any_scores)),
        "combined_min_p": round_float(min(p_values)) if p_values else "",
        "combined_min_q": "",
        "all_controls_max_p": round_float(max(p_values)) if p_values else "",
        "all_controls_max_q": "",
        "extension_band": "",
        "all_controls_band": "",
        "warning_count": "",
        "flags": ";".join(flags),
        "read": "",
        "all_controls_read": "",
    }


def annotate_rows(rows: list[ExtensionControlRow]) -> None:
    row_dicts = [row.row for row in rows]
    min_q_values = benjamini_hochberg_q_values(
        [numeric_value(row.get("combined_min_p")) for row in row_dicts]
    )
    all_q_values = benjamini_hochberg_q_values(
        [numeric_value(row.get("all_controls_max_p")) for row in row_dicts]
    )
    for row, min_q_value, all_q_value in zip(
        row_dicts,
        min_q_values,
        all_q_values,
        strict=True,
    ):
        row["combined_min_q"] = round_float(min_q_value)
        row["all_controls_max_q"] = round_float(all_q_value)
        flags = split_flags(str(row["flags"]))
        combined_p = numeric_value(row.get("combined_min_p"))
        combined_q = numeric_value(row.get("combined_min_q"))
        if combined_p is not None and combined_p <= 0.05 and (
            combined_q is None or combined_q > 0.10
        ):
            flags.append("uncorrected_only")
        if combined_q is not None:
            flags.append("extension_min_p_adjusted")
        row["extension_band"] = extension_band(row)
        row["all_controls_band"] = all_controls_band(row)
        row["flags"] = ";".join(sorted(set(flags)))
        row["warning_count"] = len(split_flags(str(row["flags"])))
        row["read"] = read_label(row)
        row["all_controls_read"] = all_controls_read_label(row)


def extension_band(row: dict[str, object]) -> str:
    combined_q = numeric_value(row.get("combined_min_q"))
    combined_p = numeric_value(row.get("combined_min_p"))
    if combined_q is not None:
        if combined_q <= 0.01:
            return "extension_q_le_0.01"
        if combined_q <= 0.05:
            return "extension_q_le_0.05"
        if combined_q <= 0.10:
            return "extension_q_le_0.10"
    if combined_p is not None and combined_p <= 0.05:
        return "extension_uncorrected_p_le_0.05"
    return "not_unusual"


def read_label(row: dict[str, object]) -> str:
    band = str(row.get("extension_band", ""))
    if band.startswith("extension_q_"):
        return "extension-control screen; inspect manually"
    if band == "extension_uncorrected_p_le_0.05":
        return "uncorrected extension screen only"
    return "not unusual under extension controls"


def all_controls_band(row: dict[str, object]) -> str:
    all_q = numeric_value(row.get("all_controls_max_q"))
    all_p = numeric_value(row.get("all_controls_max_p"))
    if all_q is not None:
        if all_q <= 0.01:
            return "all_controls_q_le_0.01"
        if all_q <= 0.05:
            return "all_controls_q_le_0.05"
        if all_q <= 0.10:
            return "all_controls_q_le_0.10"
    if all_p is not None and all_p <= 0.05:
        return "all_controls_uncorrected_p_le_0.05"
    return "not_unusual"


def all_controls_read_label(row: dict[str, object]) -> str:
    band = str(row.get("all_controls_band", ""))
    if band.startswith("all_controls_q_"):
        return "all-control screen; inspect manually"
    if band == "all_controls_uncorrected_p_le_0.05":
        return "uncorrected all-control screen only"
    return "not unusual under all-control check"


def flags_for_row(
    target: ExtensionTarget,
    term_controls: ControlScores,
    random_controls: ControlScores,
) -> list[str]:
    flags = []
    if len(target.normalized_term) <= 4:
        flags.append("short_base_term")
    if len(term_controls.queries) < 100:
        flags.append("few_term_extension_controls")
    if len(random_controls.queries) < 100:
        flags.append("few_random_extension_controls")
    if len(set(term_controls.same_type_scores)) < 2:
        flags.append("low_term_same_type_variance")
    if len(set(random_controls.same_type_scores)) < 2:
        flags.append("low_random_same_type_variance")
    return sorted(set(flags))


def sample_term_controls(query: str, *, samples: int, rng: random.Random) -> tuple[str, ...]:
    output = []
    letters = list(query)
    for _index in range(samples):
        shuffled = letters[:]
        rng.shuffle(shuffled)
        output.append("".join(shuffled))
    return tuple(output)


def sample_random_controls(
    *,
    length: int,
    corpus_text: str | None = None,
    samples: int,
    rng: random.Random,
    alphabet: tuple[str, ...] | None = None,
    weights: tuple[int, ...] | None = None,
) -> tuple[str, ...]:
    if alphabet is None or weights is None:
        if corpus_text is None:
            raise ValueError("corpus_text is required when alphabet and weights are absent")
        alphabet, weights = weighted_alphabet(corpus_text)
    return tuple(
        "".join(rng.choices(alphabet, weights=weights, k=length))
        for _index in range(samples)
    )


def weighted_alphabet(corpus_text: str) -> tuple[tuple[str, ...], tuple[int, ...]]:
    counts = Counter(corpus_text)
    alphabet = tuple(sorted(counts))
    return alphabet, tuple(counts[char] for char in alphabet)


def example_rows(
    rows: list[ExtensionControlRow],
    limit: int,
) -> list[dict[str, object]]:
    output = []
    for control_row in rows[:limit]:
        row = dict(control_row.row)
        row["term_same_type_scores_sample"] = sample_cell(control_row.term_controls.same_type_scores)
        row["term_any_scores_sample"] = sample_cell(control_row.term_controls.any_scores)
        row["term_queries_sample"] = sample_cell(control_row.term_controls.queries)
        row["random_same_type_scores_sample"] = sample_cell(
            control_row.random_controls.same_type_scores
        )
        row["random_any_scores_sample"] = sample_cell(control_row.random_controls.any_scores)
        row["random_queries_sample"] = sample_cell(control_row.random_controls.queries)
        output.append(row)
    return output


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    *,
    title: str = "Extension Paired Controls",
    lead: str = (
        "This report compares extension-top rows against shuffled-term and "
        "same-corpus random controls at the same skip and direction."
    ),
    caution: str = (
        "Controls are row-local and exploratory. Low scores mainly identify "
        "rows worth manual review, not statistical claims."
    ),
) -> None:
    band_counts = Counter(str(row["extension_band"]) for row in rows)
    all_control_band_counts = Counter(str(row.get("all_controls_band", "")) for row in rows)
    lines = [
        f"# {title}",
        "",
        lead,
        "",
        "## Band Counts",
        "",
        "| Band | Rows |",
        "| --- | ---: |",
    ]
    for band, count in sorted(band_counts.items()):
        lines.append(f"| `{band}` | {count} |")
    lines.extend(
        [
            "",
            "## All-Control Band Counts",
            "",
            "| Band | Rows |",
            "| --- | ---: |",
        ]
    )
    for band, count in sorted(all_control_band_counts.items()):
        lines.append(f"| `{band}` | {count} |")
    lines.extend(
        [
            "",
            "## Top Screens",
            "",
            "| Corpus | Target | Score | Best control | Control ge | Min q | All-control q | Screen band | All-control band | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in sorted(rows, key=markdown_row_sort_key)[:40]:
        best_control = max(
            int_or_zero(row.get("term_any_score_max")),
            int_or_zero(row.get("random_any_score_max")),
        )
        controls_ge = max(
            int_or_zero(row.get("term_any_ge_observed")),
            int_or_zero(row.get("random_any_ge_observed")),
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["corpus"]),
                    markdown_target_cell(row),
                    str(row["observed_score"]),
                    str(best_control),
                    str(controls_ge),
                    str(row["combined_min_q"]),
                    str(row["all_controls_max_q"]),
                    f"`{row['extension_band']}`",
                    f"`{row['all_controls_band']}`",
                    str(row["all_controls_read"]),
                ]
            )
            + " |"
        )
    conservative_rows = [
        row for row in rows if str(row.get("all_controls_band", "")) != "not_unusual"
    ]
    lines.extend(
        [
            "",
            "## Conservative All-Control Screens",
            "",
            "| Corpus | Target | Min q | All-control q | All-control band | Read |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in sorted(conservative_rows, key=all_control_row_sort_key):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["corpus"]),
                    markdown_target_cell(row),
                    str(row["combined_min_q"]),
                    str(row["all_controls_max_q"]),
                    f"`{row['all_controls_band']}`",
                    str(row["all_controls_read"]),
                ]
            )
            + " |"
        )
    if not conservative_rows:
        lines.append("| none | none |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Caution",
            "",
            caution,
            "",
            "`Min q` is the adjusted minimum across term-shuffle, random-letter, same-extension-type, and any-extension controls. `All-control q` is the adjusted maximum across those same checks, so it is the conservative companion read.",
            "",
            "With small control sample counts, empirical p-values are floor-limited at `1 / (samples + 1)`. Treat low q-values here as post-screen flags, not claim evidence.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_target_cell(row: dict[str, object]) -> str:
    term = display_term(str(row["term"]), english=str(row.get("concept", "")))
    extended_sequence = str(row["extended_sequence"])
    extended = display_term(extended_sequence)
    if "English:" not in extended:
        extended = display_term(
            extended_sequence,
            english=extension_english_gloss(row),
        )
    return (
        f"{term} {row['skip']} "
        f"{row['extension_type']} {extended}"
    )


def extension_english_gloss(row: dict[str, object]) -> str:
    concept = str(row.get("concept", "")).strip()
    if concept:
        return f"hidden extension form involving {concept}"
    return "hidden extension sequence"


def write_manifest(
    args: argparse.Namespace,
    targets: list[ExtensionTarget],
    corpora: list[dict[str, object]],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_extension_paired_controls",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "top_files": [str(path) for path in (args.top_file or TOP_FILES)],
        "targets": len(targets),
        "term_control_samples": args.term_control_samples,
        "random_control_samples": args.random_control_samples,
        "max_before": args.max_before,
        "max_after": args.max_after,
        "phrase_words": args.phrase_words,
        "max_extensions_per_hit": args.max_extensions_per_hit,
        "min_extension_length": args.min_extension_length,
        "match_kind_prefix": args.match_kind_prefix,
        "require_cross_corpus_overlap": args.require_cross_corpus_overlap,
        "require_overlap_corpus": list(args.require_overlap_corpus),
        "dedupe_targets": args.dedupe_targets,
        "include_overlap_keys": list(args.include_overlap_key),
        "surface_context_hits": str(args.surface_context_hits)
        if args.surface_context_hits is not None
        else "",
        "require_center_exact": args.require_center_exact,
        "rows": rows,
        "corpora": corpora,
        "outputs": [
            str(args.summary_out),
            str(args.examples_out),
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


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def extension_score(
    extension_type: str,
    extension_length: int,
    match_kind: str,
    match_count: int,
    *,
    high_priority_scale: bool = False,
) -> int:
    return score_extension(
        extension_type,
        extension_length,
        match_kind,
        match_count,
        high_priority_scale=high_priority_scale,
    )


def p_value_ge(observed: int, samples: tuple[int, ...]) -> float | None:
    return tail_p_value_ge(observed, samples)


def mean_or_none(values: tuple[int, ...]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def max_or_blank(values: tuple[int, ...]) -> int | str:
    return max(values) if values else ""


def count_ge(observed: int, values: tuple[int, ...]) -> int:
    return sum(1 for value in values if value >= observed)


def sample_cell(values: tuple[object, ...], limit: int = 20) -> str:
    return ";".join(str(value) for value in values[:limit])


def control_row_sort_key(row: ExtensionControlRow) -> tuple[float, float, str]:
    return markdown_row_sort_key(row.row)


def markdown_row_sort_key(row: dict[str, object]) -> tuple[float, float, str]:
    combined_q = numeric_value(row.get("combined_min_q"))
    combined_p = numeric_value(row.get("combined_min_p"))
    return (
        1.0 if combined_q is None else combined_q,
        1.0 if combined_p is None else combined_p,
        str(row.get("target_id", "")),
    )


def all_control_row_sort_key(row: dict[str, object]) -> tuple[float, float, str]:
    all_q = numeric_value(row.get("all_controls_max_q"))
    all_p = numeric_value(row.get("all_controls_max_p"))
    return (
        1.0 if all_q is None else all_q,
        1.0 if all_p is None else all_p,
        str(row.get("target_id", "")),
    )


def stable_seed(*parts: object) -> int:
    value = 0
    for part in parts:
        for char in str(part):
            value = (value * 131 + ord(char)) % 2_147_483_647
    return value


def split_flags(raw_flags: str) -> list[str]:
    return [flag for flag in raw_flags.split(";") if flag]


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


if __name__ == "__main__":
    raise SystemExit(main())
