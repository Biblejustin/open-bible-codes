#!/usr/bin/env python3
"""Run ELS null-model controls for public term sets."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.search import count_els_terms_by_lanes, normalize_for_corpus
from els.statistics import (
    benjamini_hochberg_q_values,
    direction_count,
    estimated_search_space,
    hits_per_million,
    numeric_value,
    round_float,
)
from els.stats import NullSummary, shuffled_term_samples, summarize_null_counts


DEFAULT_TERM_SETS = [
    "theological_terms=terms/theological_terms.csv",
    "modern_names_dates=terms/modern_names_dates.csv",
    "table_of_nations=terms/table_of_nations.csv",
    "prophetic_terms=terms/prophetic_terms.csv",
]
DEFAULT_CORPORA = [
    "MT_WLC=configs/example_oshb_wlc.toml",
    "LXX=configs/example_ebible_grclxx.toml",
    "TR_NT=configs/example_ebible_grctr.toml",
    "SBLGNT=configs/example_sblgnt.toml",
]

SUMMARY_OUT = Path("reports/els_controls_summary.csv")
EXAMPLES_OUT = Path("reports/els_controls_examples.csv")
MANIFEST_OUT = Path("reports/els_controls.manifest.json")

SUMMARY_FIELDNAMES = [
    "corpus",
    "corpus_language",
    "term_set",
    "term_source",
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
    "skip_count",
    "direction_count",
    "search_space_positions",
    "hits_per_million_positions",
    "observed_hits",
    "letter_shuffles",
    "letter_null_mean",
    "letter_null_stdev",
    "letter_z_score",
    "letter_p_ge",
    "letter_q_value",
    "letter_percentile",
    "letter_null_min",
    "letter_null_max",
    "term_shuffles",
    "term_null_mean",
    "term_null_stdev",
    "term_z_score",
    "term_p_ge",
    "term_q_value",
    "term_percentile",
    "term_null_min",
    "term_null_max",
    "term_unique_samples",
    "term_same_as_observed_samples",
    "combined_min_p_ge",
    "combined_min_q_value",
    "significance_band",
    "status",
    "warning_count",
    "flags",
]
EXAMPLE_FIELDNAMES = [
    *SUMMARY_FIELDNAMES,
    "letter_null_counts_sample",
    "term_null_counts_sample",
    "term_samples_sample",
]


@dataclass(frozen=True)
class TermSet:
    label: str
    path: Path
    rows: list[dict[str, str]]


@dataclass(frozen=True)
class ControlTerm:
    term_set: str
    term_source: str
    row: dict[str, str]
    term_language: str
    term: str
    normalized: str
    status: str


@dataclass(frozen=True)
class ControlRow:
    row: dict[str, object]
    letter_counts: tuple[int, ...]
    term_counts: tuple[int, ...]
    term_samples: tuple[str, ...]


@dataclass
class ProgressTicker:
    enabled: bool
    interval: float
    started: float
    last_emit: float

    def emit(self, message: str, *, force: bool = False) -> None:
        if not self.enabled:
            return
        now = time.perf_counter()
        if force or now - self.last_emit >= self.interval:
            print(
                f"[progress {now - self.started:.1f}s] {message}",
                file=sys.stderr,
                flush=True,
            )
            self.last_emit = now


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.progress_interval < 0:
        raise SystemExit("--progress-interval must be >= 0")
    started = time.perf_counter()
    progress = ProgressTicker(
        enabled=bool(args.progress),
        interval=float(args.progress_interval),
        started=started,
        last_emit=started,
    )
    term_sets = parse_term_sets(args.term_set or DEFAULT_TERM_SETS)
    corpus_configs = parse_label_paths(args.corpus or DEFAULT_CORPORA, "--corpus")
    progress.emit(
        f"loaded {len(term_sets)} term sets; {len(corpus_configs)} corpora queued",
        force=True,
    )

    summary_rows: list[dict[str, object]] = []
    control_rows: list[ControlRow] = []
    corpus_manifests: list[dict[str, object]] = []
    for corpus_index, (corpus_label, config_path) in enumerate(corpus_configs, start=1):
        corpus_started = time.perf_counter()
        progress.emit(
            f"corpus {corpus_index}/{len(corpus_configs)} {corpus_label}: load",
            force=True,
        )
        corpus = load_corpus(config_path)
        terms = prepare_terms(corpus, term_sets, args.min_term_length)
        progress.emit(
            (
                f"corpus {corpus_index}/{len(corpus_configs)} {corpus_label}: "
                f"{sum(1 for term in terms if term.status == 'counted')}/{len(terms)} terms countable"
            ),
            force=True,
        )
        rows = analyze_corpus(corpus_label, corpus, terms, args, progress)
        control_rows.extend(rows)
        corpus_manifests.append(
            {
                "label": corpus_label,
                "config": str(Path(config_path).expanduser().resolve()),
                "summary": corpus.summary(),
                "terms": len(terms),
                "counted_terms": sum(1 for term in terms if term.status == "counted"),
                "seconds": round(time.perf_counter() - corpus_started, 3),
            }
        )
        progress.emit(
            f"corpus {corpus_index}/{len(corpus_configs)} {corpus_label}: done",
            force=True,
        )

    annotate_control_rows(control_rows)
    progress.emit("writing outputs", force=True)
    summary_rows.extend(control_row.row for control_row in control_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(
        args.examples_out,
        EXAMPLE_FIELDNAMES,
        example_rows(control_rows, args.max_examples),
    )
    write_manifest(args, term_sets, corpus_manifests, len(summary_rows), started)

    print(args.summary_out)
    print(args.examples_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--term-set", action="append")
    parser.add_argument("--corpus", action="append")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=50)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--min-term-length", type=int, default=3)
    parser.add_argument("--letter-shuffles", type=int, default=3)
    parser.add_argument("--term-shuffles", type=int, default=25)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=0)
    parser.add_argument("--max-examples", type=int, default=200)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-interval", type=float, default=10.0)
    return parser


def parse_term_sets(raw_items: list[str]) -> list[TermSet]:
    term_sets = []
    for label, path in parse_label_paths(raw_items, "--term-set"):
        term_sets.append(TermSet(label=label, path=Path(path), rows=read_rows(Path(path))))
    return term_sets


def parse_label_paths(raw_items: list[str], flag: str) -> list[tuple[str, str]]:
    parsed = []
    seen: set[str] = set()
    for raw in raw_items:
        if "=" not in raw:
            raise SystemExit(f"{flag} must be label=path: {raw}")
        label, path = raw.split("=", 1)
        label = label.strip()
        path = path.strip()
        if not label or not path:
            raise SystemExit(f"{flag} must be label=path: {raw}")
        if label in seen:
            raise SystemExit(f"duplicate label for {flag}: {label}")
        seen.add(label)
        parsed.append((label, path))
    return parsed


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def prepare_terms(
    corpus: Corpus,
    term_sets: list[TermSet],
    min_term_length: int,
) -> list[ControlTerm]:
    accepted_languages = accepted_term_languages(corpus.language)
    terms: list[ControlTerm] = []
    for term_set in term_sets:
        for raw_row in term_set.rows:
            term_language = raw_row.get("language", "").strip()
            if term_language not in accepted_languages:
                continue
            term = raw_row.get("term", "").strip()
            normalized = normalize_for_corpus(corpus, term)
            status = "counted" if len(normalized) >= min_term_length else "skipped_short_term"
            terms.append(
                ControlTerm(
                    term_set=term_set.label,
                    term_source=str(term_set.path),
                    row=raw_row,
                    term_language=term_language,
                    term=term,
                    normalized=normalized,
                    status=status,
                )
            )
    return terms


def analyze_corpus(
    corpus_label: str,
    corpus: Corpus,
    terms: list[ControlTerm],
    args: argparse.Namespace,
    progress: ProgressTicker,
) -> list[ControlRow]:
    counted_queries = sorted({term.normalized for term in terms if term.status == "counted"})
    letter_counts = shuffled_letter_counts(
        corpus,
        corpus_label,
        counted_queries,
        args,
        progress,
        seed=args.seed + stable_offset(corpus_label, "letters"),
    )
    observed_counts, term_counts, term_samples = observed_and_shuffled_term_counts(
        corpus,
        corpus_label,
        counted_queries,
        args,
        progress,
        seed=args.seed + stable_offset(corpus_label, "terms"),
    )

    rows = []
    for term_index, term in enumerate(terms, start=1):
        progress.emit(f"{corpus_label}: summarize term {term_index}/{len(terms)}")
        observed = 0 if term.status != "counted" else observed_counts.get(term.normalized, 0)
        row_letter_counts = letter_counts.get(term.normalized, ())
        row_term_counts = term_counts.get(term.normalized, ())
        row_term_samples = term_samples.get(term.normalized, ())
        letter_summary = summarize_null_counts(observed, row_letter_counts)
        term_summary = summarize_null_counts(observed, row_term_counts)
        rows.append(
            ControlRow(
                row=summary_row(
                    corpus_label,
                    corpus,
                    term,
                    observed,
                    letter_summary,
                    term_summary,
                    row_term_samples,
                    args,
                ),
                letter_counts=row_letter_counts,
                term_counts=row_term_counts,
                term_samples=row_term_samples,
            )
        )
    return rows


def shuffled_letter_counts(
    corpus: Corpus,
    corpus_label: str,
    queries: list[str],
    args: argparse.Namespace,
    progress: ProgressTicker,
    *,
    seed: int,
) -> dict[str, tuple[int, ...]]:
    if args.letter_shuffles < 1 or not queries:
        return {query: () for query in queries}
    rng = random.Random(seed)
    letters = list(corpus.text)
    counts_by_query: dict[str, list[int]] = {query: [] for query in queries}
    for index in range(args.letter_shuffles):
        progress.emit(f"{corpus_label}: letter shuffle {index + 1}/{args.letter_shuffles}")
        rng.shuffle(letters)
        counts = count_els_terms_by_lanes(
            "".join(letters),
            queries,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            jobs=args.jobs,
        )
        for query in queries:
            counts_by_query[query].append(counts.get(query, 0))
    return {query: tuple(counts) for query, counts in counts_by_query.items()}


def observed_and_shuffled_term_counts(
    corpus: Corpus,
    corpus_label: str,
    queries: list[str],
    args: argparse.Namespace,
    progress: ProgressTicker,
    *,
    seed: int,
) -> tuple[dict[str, int], dict[str, tuple[int, ...]], dict[str, tuple[str, ...]]]:
    if not queries:
        return {}, {}, {}
    if args.term_shuffles < 1:
        progress.emit(f"{corpus_label}: observed counts")
        observed_counts = count_els_terms_by_lanes(
            corpus.text,
            queries,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            jobs=args.jobs,
        )
        return (
            observed_counts,
            {query: () for query in queries},
            {query: () for query in queries},
        )
    rng = random.Random(seed)
    samples_by_query = {
        query: shuffled_term_samples(query, shuffles=args.term_shuffles, rng=rng)
        for query in queries
    }
    unique_samples = sorted({sample for samples in samples_by_query.values() for sample in samples})
    count_queries = sorted(set(queries).union(unique_samples))
    progress.emit(
        (
            f"{corpus_label}: term-shuffle count {len(unique_samples)} unique samples "
            f"plus {len(queries)} observed terms"
        ),
    )
    counts = count_els_terms_by_lanes(
        corpus.text,
        count_queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    observed_counts = {query: counts.get(query, 0) for query in queries}
    counts_by_query = {
        query: tuple(counts.get(sample, 0) for sample in samples)
        for query, samples in samples_by_query.items()
    }
    return observed_counts, counts_by_query, samples_by_query


def summary_row(
    corpus_label: str,
    corpus: Corpus,
    term: ControlTerm,
    observed: int,
    letter_summary: NullSummary,
    term_summary: NullSummary,
    term_samples: tuple[str, ...],
    args: argparse.Namespace,
) -> dict[str, object]:
    letter_row = summary_fields("letter", letter_summary)
    term_row = summary_fields("term", term_summary)
    p_values = [
        value
        for value in [letter_summary.p_greater_equal, term_summary.p_greater_equal]
        if value is not None
    ]
    unique_term_samples = len(set(term_samples))
    same_as_observed = sum(1 for sample in term_samples if sample == term.normalized)
    search_space = estimated_search_space(
        len(corpus.text),
        len(term.normalized),
        args.min_skip,
        args.max_skip,
        args.direction,
    ) if term.status == "counted" else 0
    return {
        "corpus": corpus_label,
        "corpus_language": corpus.language,
        "term_set": term.term_set,
        "term_source": term.term_source,
        "term_id": term.row.get("term_id", ""),
        "concept": term.row.get("concept", ""),
        "category": term.row.get("category", ""),
        "term_language": term.term_language,
        "term": term.term,
        "normalized_term": term.normalized,
        "normalized_length": len(term.normalized),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "skip_count": max(0, args.max_skip - args.min_skip + 1),
        "direction_count": direction_count(args.direction),
        "search_space_positions": search_space,
        "hits_per_million_positions": hits_per_million(observed, search_space),
        "observed_hits": observed,
        **letter_row,
        **term_row,
        "term_unique_samples": unique_term_samples,
        "term_same_as_observed_samples": same_as_observed,
        "combined_min_p_ge": round_float(min(p_values)) if p_values else "",
        "letter_q_value": "",
        "term_q_value": "",
        "combined_min_q_value": "",
        "significance_band": "",
        "status": term.status,
        "warning_count": "",
        "flags": ";".join(
            flags_for_row(
                term,
                observed,
                letter_summary,
                term_summary,
                term_samples,
                search_space,
            )
        ),
    }


def summary_fields(prefix: str, summary: NullSummary) -> dict[str, object]:
    return {
        f"{prefix}_shuffles": summary.samples,
        f"{prefix}_null_mean": round_float(summary.mean),
        f"{prefix}_null_stdev": round_float(summary.stdev),
        f"{prefix}_z_score": round_float(summary.z_score),
        f"{prefix}_p_ge": round_float(summary.p_greater_equal),
        f"{prefix}_percentile": round_float(summary.percentile),
        f"{prefix}_null_min": empty_if_none(summary.min_count),
        f"{prefix}_null_max": empty_if_none(summary.max_count),
    }


def flags_for_row(
    term: ControlTerm,
    observed: int,
    letter_summary: NullSummary,
    term_summary: NullSummary,
    term_samples: tuple[str, ...],
    search_space: int,
) -> list[str]:
    flags = []
    if term.status != "counted":
        flags.append(term.status)
        return flags
    if len(term.normalized) <= 3:
        flags.append("short_counted_term")
    if letter_summary.samples < 1:
        flags.append("no_letter_controls")
    elif letter_summary.samples < 100:
        flags.append("few_letter_controls")
    if term_summary.samples < 1:
        flags.append("no_term_controls")
    elif term_summary.samples < 100:
        flags.append("few_term_controls")
    if letter_summary.stdev == 0:
        flags.append("zero_letter_variance")
    if term_summary.stdev == 0:
        flags.append("zero_term_variance")
    if observed < 5:
        flags.append("low_observed_hits")
    if search_space >= 10_000_000:
        flags.append("huge_search_space")
    elif search_space >= 1_000_000:
        flags.append("large_search_space")
    if search_space >= 1_000_000 and observed < 5:
        flags.append("large_search_space_low_hits")
    if term_samples and len(set(term_samples)) < max(2, len(term_samples) // 4):
        flags.append("low_term_null_diversity")
    return flags


def annotate_control_rows(rows: list[ControlRow]) -> None:
    row_dicts = [control_row.row for control_row in rows]
    apply_q_values(row_dicts, "letter_p_ge", "letter_q_value")
    apply_q_values(row_dicts, "term_p_ge", "term_q_value")
    apply_q_values(row_dicts, "combined_min_p_ge", "combined_min_q_value")
    for row in row_dicts:
        row["significance_band"] = significance_band(row)
        flags = split_flags(str(row.get("flags", "")))
        if row.get("status") == "counted":
            combined_p = numeric_value(row.get("combined_min_p_ge"))
            combined_q = numeric_value(row.get("combined_min_q_value"))
            if combined_p is not None and combined_p <= 0.05 and (
                combined_q is None or combined_q > 0.10
            ):
                flags.append("uncorrected_only")
            if combined_q is None:
                flags.append("no_q_value")
            else:
                flags.append("screening_min_p_adjusted")
        flags = sorted(set(flags))
        row["warning_count"] = len(flags)
        row["flags"] = ";".join(flags)


def apply_q_values(rows: list[dict[str, object]], p_field: str, q_field: str) -> None:
    q_values = benjamini_hochberg_q_values(
        [numeric_value(row.get(p_field)) for row in rows]
    )
    for row, q_value in zip(rows, q_values, strict=True):
        row[q_field] = round_float(q_value)


def significance_band(row: dict[str, object]) -> str:
    if row.get("status") != "counted":
        return "not_tested"
    combined_q = numeric_value(row.get("combined_min_q_value"))
    combined_p = numeric_value(row.get("combined_min_p_ge"))
    if combined_q is not None:
        if combined_q <= 0.01:
            return "screen_q_le_0.01"
        if combined_q <= 0.05:
            return "screen_q_le_0.05"
        if combined_q <= 0.10:
            return "screen_q_le_0.10"
    if combined_p is not None and combined_p <= 0.05:
        return "uncorrected_p_le_0.05"
    return "not_unusual"


def example_rows(rows: list[ControlRow], limit: int) -> list[dict[str, object]]:
    candidates = [row for row in rows if row.row.get("status") == "counted"]
    candidates.sort(key=example_sort_key)
    output = []
    for control_row in candidates[:limit]:
        row = dict(control_row.row)
        row["letter_null_counts_sample"] = sample_csv_cell(control_row.letter_counts)
        row["term_null_counts_sample"] = sample_csv_cell(control_row.term_counts)
        row["term_samples_sample"] = sample_csv_cell(control_row.term_samples)
        output.append(row)
    return output


def example_sort_key(row: ControlRow) -> tuple[float, float, int, float, str, str, str]:
    combined = row.row.get("combined_min_q_value")
    combined_q = float(combined) if combined != "" else 1.0
    combined_p = numeric_value(row.row.get("combined_min_p_ge")) or 1.0
    observed = int(row.row.get("observed_hits", 0))
    z_values = [
        float(value)
        for value in [row.row.get("letter_z_score"), row.row.get("term_z_score")]
        if value != ""
    ]
    best_z = max(z_values) if z_values else 0.0
    return (
        combined_q,
        combined_p,
        -observed,
        -best_z,
        str(row.row.get("corpus", "")),
        str(row.row.get("term_set", "")),
        str(row.row.get("term_id", "")),
    )


def sample_csv_cell(values: tuple[Any, ...], limit: int = 20) -> str:
    return ";".join(str(value) for value in values[:limit])


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    term_sets: list[TermSet],
    corpora: list[dict[str, object]],
    row_count: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_els_controls",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "term_sets": [
            {"label": term_set.label, "path": str(term_set.path), "rows": len(term_set.rows)}
            for term_set in term_sets
        ],
        "corpora": corpora,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "min_term_length": args.min_term_length,
        "letter_shuffles": args.letter_shuffles,
        "term_shuffles": args.term_shuffles,
        "seed": args.seed,
        "jobs": args.jobs,
        "progress": bool(args.progress),
        "progress_interval": args.progress_interval,
        "rows": row_count,
        "summary_out": str(args.summary_out),
        "examples_out": str(args.examples_out),
        "seconds": round(time.perf_counter() - started, 3),
        "notes": [
            "Letter controls shuffle corpus letters while preserving corpus letter frequencies.",
            "Term controls shuffle letters within each normalized term while preserving term length and letter multiset.",
            "p_ge values are empirical greater-or-equal tail estimates with add-one smoothing.",
            "q_value fields use Benjamini-Hochberg correction across emitted summary rows.",
            "combined_min_q_value corrects the screening minimum of letter_p_ge and term_p_ge; treat it as ranking evidence, not a proof statistic.",
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def stable_offset(*parts: str) -> int:
    value = 0
    for part in parts:
        for char in part:
            value = (value * 131 + ord(char)) % 1_000_000
    return value


def split_flags(raw_flags: str) -> list[str]:
    return [flag for flag in raw_flags.split(";") if flag]


def empty_if_none(value: int | None) -> int | str:
    return "" if value is None else value


if __name__ == "__main__":
    raise SystemExit(main())
