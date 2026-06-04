"""`batch` and `batch-many` subcommands: count ELS hits per term across corpora.

Carries the batch term-set dataclasses and all per-corpus preparation, counting,
row-building, and manifest helpers. Cross-corpus parallelism uses a thread pool
(process_batch_many_corpus runs in worker threads that share memory); there are no
module-level worker globals here. Imports only els leaf modules, never els.cli.
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.io import write_run_manifest
from els.maxskip import effective_max_skip_for_query
from els.rows import write_batch_rows
from els.search import count_els_terms_by_lanes, normalize_for_corpus
from els.term_io import accepted_term_languages, is_safe_report_label, parse_corpus_args, read_term_rows


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
