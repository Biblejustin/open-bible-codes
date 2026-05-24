#!/usr/bin/env python3
"""Analyze Gog/Magog ELS proximity with paired controls."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from bisect import bisect_left
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from els import __version__
from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.search import build_hit, iter_els_query_matches_by_lanes, normalize_for_corpus
from els.search import process_context
from els.statistics import (
    benjamini_hochberg_q_values,
    numeric_value,
    round_float,
    tail_p_value_ge,
    tail_p_value_le,
)


TERMS = Path("terms/prophetic_terms.csv")
SUMMARY_OUT = Path("reports/gog_magog_pairs_summary.csv")
EXAMPLES_OUT = Path("reports/gog_magog_pairs_examples.csv")
MD_OUT = Path("reports/gog_magog_pairs.md")
MANIFEST_OUT = Path("reports/gog_magog_pairs.manifest.json")

CORPORA = [
    ("MT_WLC", Path("configs/example_oshb_wlc.toml")),
    ("LXX", Path("configs/example_ebible_grclxx.toml")),
    ("TR_NT", Path("configs/example_ebible_grctr.toml")),
    ("SBLGNT", Path("configs/example_sblgnt.toml")),
]
CORPUS_ORDER = {label: index for index, (label, _path) in enumerate(CORPORA)}

SUMMARY_FIELDNAMES = [
    "pair_label",
    "corpus",
    "left_term_id",
    "left_term",
    "left_normalized",
    "left_hits",
    "right_term_id",
    "right_term",
    "right_normalized",
    "right_hits",
    "max_gap",
    "observed_pairs_within_gap",
    "observed_overlap_pairs",
    "observed_best_span_gap",
    "observed_best_center_distance",
    "term_control_samples",
    "term_pairs_mean",
    "term_pairs_p_ge",
    "term_overlap_mean",
    "term_overlap_p_ge",
    "term_best_gap_mean",
    "term_best_gap_p_le",
    "random_control_samples",
    "random_pairs_mean",
    "random_pairs_p_ge",
    "random_overlap_mean",
    "random_overlap_p_ge",
    "random_best_gap_mean",
    "random_best_gap_p_le",
    "combined_min_p",
    "combined_min_q",
    "pair_band",
    "warning_count",
    "flags",
    "read",
]

EXAMPLE_FIELDNAMES = [
    "pair_label",
    "corpus",
    "left_term_id",
    "left_term",
    "left_skip",
    "left_start_ref",
    "left_end_ref",
    "left_center_ref",
    "left_center_word",
    "right_term_id",
    "right_term",
    "right_skip",
    "right_start_ref",
    "right_end_ref",
    "right_center_ref",
    "right_center_word",
    "span_gap",
    "center_distance",
    "shared_chapters",
]


@dataclass(frozen=True)
class HitLite:
    query: str
    skip: int
    start: int
    end: int

    @property
    def low(self) -> int:
        return min(self.start, self.end)

    @property
    def high(self) -> int:
        return max(self.start, self.end)

    @property
    def center(self) -> float:
        return (self.start + self.end) / 2


@dataclass(frozen=True)
class PairMetrics:
    left_hits: int
    right_hits: int
    pairs_within_gap: int
    overlap_pairs: int
    best_span_gap: int | None
    best_center_distance: float | None


@dataclass(frozen=True)
class PairExample:
    corpus: str
    left_query: str
    left_hit: HitLite
    right_query: str
    right_hit: HitLite
    span_gap: int
    center_distance: float


@dataclass(frozen=True)
class ControlSample:
    left_query: str
    right_query: str


@dataclass(frozen=True)
class CorpusResult:
    row: dict[str, object]
    examples: list[PairExample]
    term_metrics: tuple[PairMetrics, ...]
    random_metrics: tuple[PairMetrics, ...]


@dataclass(frozen=True)
class CorpusAnalysis:
    label: str
    config: str
    summary: dict[str, object]
    seconds: float
    result: CorpusResult | None
    examples: list[dict[str, object]]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_rows = {row["term_id"]: row for row in read_rows(args.terms)}
    corpora = selected_corpora(args)
    tasks = [
        (corpus_label, config, term_rows, args)
        for corpus_label, config in corpora
    ]
    analyses = run_corpus_analyses(tasks, resolve_corpus_jobs(args.jobs, len(tasks)))
    results = [analysis.result for analysis in analyses if analysis.result is not None]
    corpus_manifests = [
        {
            "label": analysis.label,
            "config": analysis.config,
            "summary": analysis.summary,
            "seconds": analysis.seconds,
        }
        for analysis in analyses
    ]

    annotate_results(results)
    rows = [result.row for result in sorted(results, key=result_sort_key)]
    examples = []
    for analysis in sorted(analyses, key=analysis_sort_key):
        examples.extend(analysis.examples)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, rows)
    write_rows(args.examples_out, EXAMPLE_FIELDNAMES, examples)
    write_markdown(args.markdown_out, rows, args.pair_label)
    write_manifest(args, corpus_manifests, len(rows), len(examples), started)

    print(args.summary_out)
    print(args.examples_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument(
        "--corpus",
        type=parse_corpus_arg,
        action="append",
        metavar="LABEL=CONFIG",
        help="Analyze an explicit corpus config. May be repeated. Defaults to public baseline corpora.",
    )
    parser.add_argument(
        "--corpus-label",
        action="append",
        choices=[label for label, _config in CORPORA],
        help="Filter the default public baseline corpus set by label.",
    )
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=50)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--max-gap", type=int, default=500)
    parser.add_argument("--term-control-samples", type=int, default=100)
    parser.add_argument("--random-control-samples", type=int, default=5)
    parser.add_argument("--pair-label", default="Gog/Magog")
    parser.add_argument("--left-hebrew-term-id", default="gog_h")
    parser.add_argument("--right-hebrew-term-id", default="magog_h")
    parser.add_argument("--left-greek-term-id", default="gog_g")
    parser.add_argument("--right-greek-term-id", default="magog_g")
    parser.add_argument("--require-same-chapter", action="store_true")
    parser.add_argument("--require-same-skip", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--hit-jobs", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1776)
    parser.add_argument("--max-examples-per-corpus", type=int, default=10)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def parse_corpus_arg(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("corpus must be LABEL=CONFIG")
    label, config = raw.split("=", 1)
    label = label.strip()
    config = config.strip()
    if not label:
        raise argparse.ArgumentTypeError("corpus label cannot be empty")
    if not config:
        raise argparse.ArgumentTypeError("corpus config cannot be empty")
    return label, Path(config)


def selected_corpora(args: argparse.Namespace) -> list[tuple[str, Path]]:
    corpora = list(args.corpus or CORPORA)
    if args.corpus_label:
        labels = set(args.corpus_label)
        corpora = [(label, config) for label, config in corpora if label in labels]
    return corpora


def run_corpus_analyses(
    tasks: list[tuple[str, Path, dict[str, dict[str, str]], argparse.Namespace]],
    jobs: int,
) -> list[CorpusAnalysis]:
    if jobs <= 1:
        return [analyze_corpus_task(task) for task in tasks]
    try:
        executor = ProcessPoolExecutor(max_workers=jobs, mp_context=process_context())
    except PermissionError:
        return [analyze_corpus_task(task) for task in tasks]
    with executor:
        return list(executor.map(analyze_corpus_task, tasks))


def analyze_corpus_task(
    task: tuple[str, Path, dict[str, dict[str, str]], argparse.Namespace],
) -> CorpusAnalysis:
    corpus_label, config, term_rows, args = task
    corpus_started = time.perf_counter()
    corpus = load_corpus(config)
    result = analyze_corpus(corpus_label, corpus, term_rows, args)
    examples = (
        [
            example_row(corpus, example, result.row)
            for example in result.examples[: args.max_examples_per_corpus]
        ]
        if result is not None
        else []
    )
    return CorpusAnalysis(
        label=corpus_label,
        config=str(config),
        summary=corpus.summary(),
        seconds=round(time.perf_counter() - corpus_started, 3),
        result=result,
        examples=examples,
    )


def analyze_corpus(
    corpus_label: str,
    corpus: Corpus,
    term_rows: dict[str, dict[str, str]],
    args: argparse.Namespace,
) -> CorpusResult | None:
    left_id, right_id = term_ids_for_corpus(corpus, args)
    left_row = term_rows[left_id]
    right_row = term_rows[right_id]
    if left_row["language"] not in accepted_term_languages(corpus.language):
        return None
    left_query = normalize_for_corpus(corpus, left_row["term"])
    right_query = normalize_for_corpus(corpus, right_row["term"])

    term_samples = paired_term_samples(
        left_query,
        right_query,
        samples=args.term_control_samples,
        rng=random.Random(stable_seed(args.seed, corpus_label, "term")),
    )
    random_samples = paired_random_samples(
        left_length=len(left_query),
        right_length=len(right_query),
        corpus_text=corpus.text,
        samples=args.random_control_samples,
        rng=random.Random(stable_seed(args.seed, corpus_label, "random")),
    )
    queries = sorted(
        {
            left_query,
            right_query,
            *(sample.left_query for sample in term_samples),
            *(sample.right_query for sample in term_samples),
            *(sample.left_query for sample in random_samples),
            *(sample.right_query for sample in random_samples),
        }
    )
    hits_by_query = collect_hits_by_query(
        corpus,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.hit_jobs,
    )
    chapter_cache: dict[HitLite, set[str]] = {}
    observed_metrics, observed_examples = score_pair(
        corpus_label,
        corpus,
        left_query,
        right_query,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=args.require_same_chapter,
        require_same_skip=args.require_same_skip,
        keep_examples=True,
        chapter_cache=chapter_cache,
    )
    term_metrics = score_control_samples(
        corpus_label,
        corpus,
        term_samples,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=args.require_same_chapter,
        require_same_skip=args.require_same_skip,
        chapter_cache=chapter_cache,
    )
    random_metrics = score_control_samples(
        corpus_label,
        corpus,
        random_samples,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=args.require_same_chapter,
        require_same_skip=args.require_same_skip,
        chapter_cache=chapter_cache,
    )
    row = summary_row(
        corpus_label,
        left_id,
        left_row,
        left_query,
        right_id,
        right_row,
        right_query,
        observed_metrics,
        term_metrics,
        random_metrics,
        args,
    )
    return CorpusResult(
        row=row,
        examples=observed_examples,
        term_metrics=term_metrics,
        random_metrics=random_metrics,
    )


def term_ids_for_corpus(corpus: Corpus, args: argparse.Namespace) -> tuple[str, str]:
    if corpus.language == "hebrew":
        return args.left_hebrew_term_id, args.right_hebrew_term_id
    return args.left_greek_term_id, args.right_greek_term_id


def collect_hits_by_query(
    corpus: Corpus,
    queries: Iterable[str],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    jobs: int = 1,
) -> dict[str, list[HitLite]]:
    hits_by_query = {query: [] for query in queries}
    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        queries,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
    ):
        hits_by_query[query].append(HitLite(query=query, skip=skip, start=start, end=end))
    for hits in hits_by_query.values():
        hits.sort(key=hit_center)
    return hits_by_query


def score_pair(
    corpus_label: str,
    corpus: Corpus | None,
    left_query: str,
    right_query: str,
    hits_by_query: dict[str, list[HitLite]],
    *,
    max_gap: int,
    require_same_chapter: bool = False,
    require_same_skip: bool = False,
    keep_examples: bool,
    chapter_cache: dict[HitLite, set[str]] | None = None,
) -> tuple[PairMetrics, list[PairExample]]:
    if require_same_chapter and corpus is None:
        raise ValueError("corpus is required for same-chapter pair scoring")
    left_hits = hits_by_query.get(left_query, [])
    right_hits = hits_by_query.get(right_query, [])
    if not left_hits or not right_hits:
        return (
            PairMetrics(
                left_hits=len(left_hits),
                right_hits=len(right_hits),
                pairs_within_gap=0,
                overlap_pairs=0,
                best_span_gap=None,
                best_center_distance=None,
            ),
            [],
        )
    right_centers = [hit.center for hit in right_hits]
    pairs_within_gap = 0
    overlap_pairs = 0
    best_span_gap: int | None = None
    best_center_distance: float | None = None
    examples = []
    if chapter_cache is None:
        chapter_cache = {}
    for left_hit in left_hits:
        for right_hit in nearest_hits(left_hit, right_hits, right_centers, radius=8):
            if require_same_skip and left_hit.skip != right_hit.skip:
                continue
            if require_same_chapter and not shared_hit_chapters(
                corpus,
                left_hit,
                right_hit,
                chapter_cache,
            ):
                continue
            gap = span_gap(left_hit, right_hit)
            if best_span_gap is None or (gap, abs(left_hit.center - right_hit.center)) < (
                best_span_gap,
                best_center_distance or 0.0,
            ):
                best_span_gap = gap
                best_center_distance = abs(left_hit.center - right_hit.center)
            if gap > max_gap:
                continue
            pairs_within_gap += 1
            if gap == 0:
                overlap_pairs += 1
            if keep_examples:
                examples.append(
                    PairExample(
                        corpus=corpus_label,
                        left_query=left_query,
                        left_hit=left_hit,
                        right_query=right_query,
                        right_hit=right_hit,
                        span_gap=gap,
                        center_distance=abs(left_hit.center - right_hit.center),
                    )
                )
    examples.sort(key=lambda example: (example.span_gap, example.center_distance))
    return (
        PairMetrics(
            left_hits=len(left_hits),
            right_hits=len(right_hits),
            pairs_within_gap=pairs_within_gap,
            overlap_pairs=overlap_pairs,
            best_span_gap=best_span_gap,
            best_center_distance=best_center_distance,
        ),
        dedupe_examples(examples),
    )


def score_control_samples(
    corpus_label: str,
    corpus: Corpus | None,
    samples: tuple[ControlSample, ...],
    hits_by_query: dict[str, list[HitLite]],
    *,
    max_gap: int,
    require_same_chapter: bool = False,
    require_same_skip: bool = False,
    chapter_cache: dict[HitLite, set[str]] | None = None,
) -> tuple[PairMetrics, ...]:
    metrics_by_pair: dict[ControlSample, PairMetrics] = {}
    output = []
    for sample in samples:
        metrics = metrics_by_pair.get(sample)
        if metrics is None:
            metrics = score_pair(
                corpus_label,
                corpus,
                sample.left_query,
                sample.right_query,
                hits_by_query,
                max_gap=max_gap,
                require_same_chapter=require_same_chapter,
                require_same_skip=require_same_skip,
                keep_examples=False,
                chapter_cache=chapter_cache,
            )[0]
            metrics_by_pair[sample] = metrics
        output.append(metrics)
    return tuple(output)


def nearest_hits(
    hit: HitLite,
    sorted_hits: list[HitLite],
    centers: list[float],
    *,
    radius: int,
) -> list[HitLite]:
    center = hit.center
    insertion_index = bisect_left(centers, center)
    if insertion_index == 0:
        best_index = 0
    elif insertion_index == len(centers):
        best_index = len(centers) - 1
    else:
        before = insertion_index - 1
        after = insertion_index
        best_index = before if center - centers[before] <= centers[after] - center else after
    best_index = bisect_left(centers, centers[best_index])
    start = max(0, best_index - radius)
    end = min(len(sorted_hits), best_index + radius + 1)
    return sorted_hits[start:end]


def summary_row(
    corpus_label: str,
    left_id: str,
    left_row: dict[str, str],
    left_query: str,
    right_id: str,
    right_row: dict[str, str],
    right_query: str,
    observed: PairMetrics,
    term_metrics: tuple[PairMetrics, ...],
    random_metrics: tuple[PairMetrics, ...],
    args: argparse.Namespace,
) -> dict[str, object]:
    term_pairs = tuple(metric.pairs_within_gap for metric in term_metrics)
    random_pairs = tuple(metric.pairs_within_gap for metric in random_metrics)
    term_overlaps = tuple(metric.overlap_pairs for metric in term_metrics)
    random_overlaps = tuple(metric.overlap_pairs for metric in random_metrics)
    term_gaps = tuple(metric.best_span_gap for metric in term_metrics if metric.best_span_gap is not None)
    random_gaps = tuple(
        metric.best_span_gap for metric in random_metrics if metric.best_span_gap is not None
    )
    p_values = [
        p_value_ge(observed.pairs_within_gap, term_pairs),
        p_value_ge(observed.pairs_within_gap, random_pairs),
        p_value_ge(observed.overlap_pairs, term_overlaps),
        p_value_ge(observed.overlap_pairs, random_overlaps),
        p_value_le(observed.best_span_gap, term_gaps),
        p_value_le(observed.best_span_gap, random_gaps),
    ]
    p_values = [value for value in p_values if value is not None]
    flags = flags_for_row(observed, term_metrics, random_metrics)
    return {
        "pair_label": args.pair_label,
        "corpus": corpus_label,
        "left_term_id": left_id,
        "left_term": left_row["term"],
        "left_normalized": left_query,
        "left_hits": observed.left_hits,
        "right_term_id": right_id,
        "right_term": right_row["term"],
        "right_normalized": right_query,
        "right_hits": observed.right_hits,
        "max_gap": args.max_gap,
        "observed_pairs_within_gap": observed.pairs_within_gap,
        "observed_overlap_pairs": observed.overlap_pairs,
        "observed_best_span_gap": empty_if_none(observed.best_span_gap),
        "observed_best_center_distance": round_float(observed.best_center_distance),
        "term_control_samples": len(term_metrics),
        "term_pairs_mean": round_float(mean_or_none(term_pairs)),
        "term_pairs_p_ge": round_float(p_value_ge(observed.pairs_within_gap, term_pairs)),
        "term_overlap_mean": round_float(mean_or_none(term_overlaps)),
        "term_overlap_p_ge": round_float(p_value_ge(observed.overlap_pairs, term_overlaps)),
        "term_best_gap_mean": round_float(mean_or_none(term_gaps)),
        "term_best_gap_p_le": round_float(p_value_le(observed.best_span_gap, term_gaps)),
        "random_control_samples": len(random_metrics),
        "random_pairs_mean": round_float(mean_or_none(random_pairs)),
        "random_pairs_p_ge": round_float(p_value_ge(observed.pairs_within_gap, random_pairs)),
        "random_overlap_mean": round_float(mean_or_none(random_overlaps)),
        "random_overlap_p_ge": round_float(p_value_ge(observed.overlap_pairs, random_overlaps)),
        "random_best_gap_mean": round_float(mean_or_none(random_gaps)),
        "random_best_gap_p_le": round_float(p_value_le(observed.best_span_gap, random_gaps)),
        "combined_min_p": round_float(min(p_values)) if p_values else "",
        "combined_min_q": "",
        "pair_band": "",
        "warning_count": "",
        "flags": ";".join(flags),
        "read": "",
    }


def annotate_results(results: list[CorpusResult]) -> None:
    rows = [result.row for result in results]
    q_values = benjamini_hochberg_q_values(
        [numeric_value(row.get("combined_min_p")) for row in rows]
    )
    for row, q_value in zip(rows, q_values, strict=True):
        row["combined_min_q"] = round_float(q_value)
        flags = split_flags(str(row["flags"]))
        combined_p = numeric_value(row.get("combined_min_p"))
        combined_q = numeric_value(row.get("combined_min_q"))
        if combined_p is not None and combined_p <= 0.05 and (
            combined_q is None or combined_q > 0.10
        ):
            flags.append("uncorrected_only")
        if combined_q is not None:
            flags.append("pair_min_p_adjusted")
        row["pair_band"] = pair_band(row)
        row["flags"] = ";".join(sorted(set(flags)))
        row["warning_count"] = len(split_flags(str(row["flags"])))
        row["read"] = read_label(row)


def pair_band(row: dict[str, object]) -> str:
    combined_q = numeric_value(row.get("combined_min_q"))
    combined_p = numeric_value(row.get("combined_min_p"))
    if combined_q is not None:
        if combined_q <= 0.01:
            return "pair_q_le_0.01"
        if combined_q <= 0.05:
            return "pair_q_le_0.05"
        if combined_q <= 0.10:
            return "pair_q_le_0.10"
    if combined_p is not None and combined_p <= 0.05:
        return "pair_uncorrected_p_le_0.05"
    return "not_unusual"


def read_label(row: dict[str, object]) -> str:
    if int_or_zero(row.get("observed_pairs_within_gap")) == 0:
        return "no close pairs"
    if str(row.get("pair_band", "")).startswith("pair_q_"):
        return "pair-control screen; inspect examples"
    if row.get("pair_band") == "pair_uncorrected_p_le_0.05":
        return "uncorrected pair screen only"
    return "not unusual under pair controls"


def flags_for_row(
    observed: PairMetrics,
    term_metrics: tuple[PairMetrics, ...],
    random_metrics: tuple[PairMetrics, ...],
) -> list[str]:
    flags = []
    if observed.left_hits < 5:
        flags.append("low_left_hits")
    if observed.right_hits < 5:
        flags.append("low_right_hits")
    if observed.pairs_within_gap == 0:
        flags.append("no_close_pairs")
    if len(term_metrics) < 100:
        flags.append("few_term_pair_controls")
    if len(random_metrics) < 100:
        flags.append("few_random_pair_controls")
    if len({metric.pairs_within_gap for metric in term_metrics}) < 2:
        flags.append("low_term_pair_variance")
    if len({metric.pairs_within_gap for metric in random_metrics}) < 2:
        flags.append("low_random_pair_variance")
    return sorted(set(flags))


def paired_term_samples(
    left_query: str,
    right_query: str,
    *,
    samples: int,
    rng: random.Random,
) -> tuple[ControlSample, ...]:
    return tuple(
        ControlSample(
            left_query=shuffle_query(left_query, rng),
            right_query=shuffle_query(right_query, rng),
        )
        for _index in range(samples)
    )


def paired_random_samples(
    *,
    left_length: int,
    right_length: int,
    corpus_text: str,
    samples: int,
    rng: random.Random,
) -> tuple[ControlSample, ...]:
    counts = Counter(corpus_text)
    alphabet = sorted(counts)
    weights = [counts[char] for char in alphabet]
    return tuple(
        ControlSample(
            left_query=random_query(alphabet, weights, left_length, rng),
            right_query=random_query(alphabet, weights, right_length, rng),
        )
        for _index in range(samples)
    )


def shuffle_query(query: str, rng: random.Random) -> str:
    letters = list(query)
    rng.shuffle(letters)
    return "".join(letters)


def random_query(
    alphabet: list[str],
    weights: list[int],
    length: int,
    rng: random.Random,
) -> str:
    return "".join(rng.choices(alphabet, weights=weights, k=length))


def example_row(
    corpus: Corpus,
    example: PairExample,
    result_row: dict[str, object],
) -> dict[str, object]:
    left = build_hit(
        corpus,
        example.left_query,
        example.left_query,
        example.left_hit.skip,
        example.left_hit.start,
        example.left_hit.end,
    )
    right = build_hit(
        corpus,
        example.right_query,
        example.right_query,
        example.right_hit.skip,
        example.right_hit.start,
        example.right_hit.end,
    )
    shared = sorted(hit_chapters(corpus, example.left_hit) & hit_chapters(corpus, example.right_hit))
    return {
        "pair_label": result_row["pair_label"],
        "corpus": example.corpus,
        "left_term_id": result_row["left_term_id"],
        "left_term": left.term,
        "left_skip": left.skip,
        "left_start_ref": left.start_ref,
        "left_end_ref": left.end_ref,
        "left_center_ref": left.center_ref,
        "left_center_word": left.center_word,
        "right_term_id": result_row["right_term_id"],
        "right_term": right.term,
        "right_skip": right.skip,
        "right_start_ref": right.start_ref,
        "right_end_ref": right.end_ref,
        "right_center_ref": right.center_ref,
        "right_center_word": right.center_word,
        "span_gap": example.span_gap,
        "center_distance": round(example.center_distance, 1),
        "shared_chapters": ";".join(shared),
    }


def hit_chapters(corpus: Corpus, hit: HitLite) -> set[str]:
    chapter_refs = set()
    previous_verse_index = None
    for position in range(hit.low, hit.high + 1):
        verse_index = corpus.position_to_verse[position]
        if verse_index == previous_verse_index:
            continue
        previous_verse_index = verse_index
        verse = corpus.verses[verse_index]
        if verse.book and verse.chapter:
            chapter_refs.add(f"{verse.book} {verse.chapter}")
    return chapter_refs


def shared_hit_chapters(
    corpus: Corpus | None,
    left_hit: HitLite,
    right_hit: HitLite,
    cache: dict[HitLite, set[str]],
) -> set[str]:
    if corpus is None:
        return set()
    if left_hit not in cache:
        cache[left_hit] = hit_chapters(corpus, left_hit)
    if right_hit not in cache:
        cache[right_hit] = hit_chapters(corpus, right_hit)
    return cache[left_hit] & cache[right_hit]


def write_markdown(path: Path, rows: list[dict[str, object]], pair_label: str) -> None:
    lines = [
        f"# {pair_label} Pair Controls",
        "",
        "This report checks whether declared ELS term-pair hits cluster closer than paired controls.",
        "",
        "## Summary",
        "",
        "| Corpus | Left hits | Right hits | Close pairs | Overlaps | Best gap | Combined p | Combined q | Band | Read |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["corpus"]),
                    str(row["left_hits"]),
                    str(row["right_hits"]),
                    str(row["observed_pairs_within_gap"]),
                    str(row["observed_overlap_pairs"]),
                    str(row["observed_best_span_gap"]),
                    str(row["combined_min_p"]),
                    str(row["combined_min_q"]),
                    f"`{row['pair_band']}`",
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Control Means",
            "",
            "| Corpus | Term close mean | Random close mean | Term overlap mean | Random overlap mean |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["corpus"]),
                    str(row["term_pairs_mean"]),
                    str(row["random_pairs_mean"]),
                    str(row["term_overlap_mean"]),
                    str(row["random_overlap_mean"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "Pair metrics are still screens. Dense short forms can create many close pairs by chance. Treat only adjusted pair-control results as worth close review.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpora: list[dict[str, object]],
    rows: int,
    examples: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_gog_magog_pairs",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "terms": str(args.terms),
        "corpus_labels": list(args.corpus_label or []),
        "corpus_args": [f"{label}={config}" for label, config in (args.corpus or [])],
        "pair_label": args.pair_label,
        "left_hebrew_term_id": args.left_hebrew_term_id,
        "right_hebrew_term_id": args.right_hebrew_term_id,
        "left_greek_term_id": args.left_greek_term_id,
        "right_greek_term_id": args.right_greek_term_id,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "max_gap": args.max_gap,
        "require_same_chapter": args.require_same_chapter,
        "require_same_skip": args.require_same_skip,
        "term_control_samples": args.term_control_samples,
        "random_control_samples": args.random_control_samples,
        "seed": args.seed,
        "jobs": args.jobs,
        "hit_jobs": args.hit_jobs,
        "rows": rows,
        "examples": examples,
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


def dedupe_examples(examples: list[PairExample]) -> list[PairExample]:
    seen = set()
    unique = []
    for example in examples:
        key = (
            example.left_hit.skip,
            example.left_hit.start,
            example.left_hit.end,
            example.right_hit.skip,
            example.right_hit.start,
            example.right_hit.end,
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(example)
    return unique


def hit_center(hit: HitLite) -> float:
    return hit.center


def span_gap(left: HitLite, right: HitLite) -> int:
    if left.low <= right.high and right.low <= left.high:
        return 0
    if left.high < right.low:
        return right.low - left.high
    return left.low - right.high


def p_value_ge(observed: int, samples: tuple[int, ...]) -> float | None:
    return tail_p_value_ge(observed, samples)


def p_value_le(observed: int | None, samples: tuple[int, ...]) -> float | None:
    return tail_p_value_le(observed, samples)


def mean_or_none(values: tuple[int, ...]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def result_sort_key(result: CorpusResult) -> int:
    return CORPUS_ORDER.get(str(result.row["corpus"]), 99)


def analysis_sort_key(analysis: CorpusAnalysis) -> int:
    return CORPUS_ORDER.get(analysis.label, 99)


def resolve_corpus_jobs(jobs: int, task_count: int) -> int:
    if jobs < 0:
        raise ValueError("jobs must be >= 0")
    if task_count < 1:
        return 1
    if jobs == 0:
        import os

        jobs = os.cpu_count() or 1
    return max(1, min(jobs, task_count))


def stable_seed(*parts: object) -> int:
    value = 0
    for part in parts:
        for char in str(part):
            value = (value * 131 + ord(char)) % 2_147_483_647
    return value


def empty_if_none(value: int | None) -> int | str:
    return "" if value is None else value


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def split_flags(raw_flags: str) -> list[str]:
    return [flag for flag in raw_flags.split(";") if flag]


if __name__ == "__main__":
    raise SystemExit(main())
