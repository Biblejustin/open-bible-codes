#!/usr/bin/env python3
"""Find declared-cohort centered hits that cluster inside a word window."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import Corpus, load_corpus
from els.match_strata import normalize_book, parse_ref


DEFAULT_OCCURRENCES = Path("reports/centered_occurrence_index/centered_occurrences.csv")
DEFAULT_OUT = Path("reports/cohort_cluster_density/windows.csv")
DEFAULT_SUMMARY_OUT = Path("reports/cohort_cluster_density/summary.csv")
DEFAULT_MANIFEST_OUT = Path("reports/cohort_cluster_density/manifest.json")

FIELDNAMES = [
    "cohort_id",
    "cohort_source",
    "corpus",
    "corpus_class",
    "window_words",
    "start_word_ordinal",
    "end_word_ordinal",
    "hit_count",
    "distinct_term_count",
    "cohort_term_count",
    "cohort_full_house",
    "term_ids",
    "concepts",
    "center_refs",
    "first_center_ref",
    "last_center_ref",
    "strata",
]

SUMMARY_FIELDNAMES = ["bucket", "value", "windows", "max_distinct_term_count"]


@dataclass(frozen=True)
class Cohort:
    cohort_id: str
    source: Path
    terms: dict[str, str]


@dataclass(frozen=True)
class PositionedHit:
    row: dict[str, str]
    cohort_id: str
    cohort_source: str
    cohort_term_count: int
    word_ordinal: int


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    cohorts = read_cohorts(args.cohort)
    corpus_configs = corpus_config_map(args.corpus_config)
    corpora = {label: load_corpus(path) for label, path in corpus_configs.items()}
    occurrence_rows = read_rows(args.occurrences)
    positioned_hits = positioned_cohort_hits(occurrence_rows, cohorts=cohorts, corpora=corpora)
    window_rows = cohort_window_rows(
        positioned_hits,
        window_words=args.window_words,
        min_distinct_terms=args.min_distinct_terms,
        max_windows=args.max_windows,
    )
    summary_rows = summarize_rows(window_rows)
    write_rows(args.out, FIELDNAMES, window_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_manifest(
        args.manifest_out,
        args,
        cohorts=cohorts,
        occurrence_rows=occurrence_rows,
        positioned_hits=positioned_hits,
        window_rows=window_rows,
        summary_rows=summary_rows,
        started=started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--occurrences", type=Path, default=DEFAULT_OCCURRENCES)
    parser.add_argument("--cohort", action="append", type=Path, required=True)
    parser.add_argument("--window-words", type=int, default=50)
    parser.add_argument("--min-distinct-terms", type=int, default=2)
    parser.add_argument("--max-windows", type=int, default=100_000)
    parser.add_argument(
        "--corpus-config",
        action="append",
        default=[],
        help="Corpus label to config mapping, e.g. MT_WLC=configs/example_oshb_wlc.toml.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_cohorts(paths: list[Path]) -> list[Cohort]:
    cohorts: list[Cohort] = []
    for path in paths:
        terms: dict[str, str] = {}
        for row in read_rows(path):
            term_id = row.get("term_id", "").strip()
            if term_id:
                terms[term_id] = row.get("concept", "").strip()
        cohorts.append(Cohort(cohort_id=path.stem, source=path, terms=terms))
    return cohorts


def corpus_config_map(values: list[str]) -> dict[str, Path]:
    output = {}
    for value in values:
        label, sep, path = value.partition("=")
        if not sep:
            raise ValueError(f"corpus config must be LABEL=PATH: {value}")
        output[label] = Path(path)
    return output


def positioned_cohort_hits(
    rows: list[dict[str, str]],
    *,
    cohorts: list[Cohort],
    corpora: dict[str, Corpus],
) -> list[PositionedHit]:
    cohorts_by_term: dict[str, list[Cohort]] = {}
    for cohort in cohorts:
        for term_id in cohort.terms:
            cohorts_by_term.setdefault(term_id, []).append(cohort)

    word_indexes = {label: corpus_word_ordinal_index(corpus) for label, corpus in corpora.items()}
    hits: list[PositionedHit] = []
    for row in rows:
        term_cohorts = cohorts_by_term.get(row.get("term_id", ""))
        if not term_cohorts:
            continue
        ordinal = word_ordinal_for_row(row, word_indexes=word_indexes)
        if ordinal is None:
            continue
        for cohort in term_cohorts:
            hits.append(
                PositionedHit(
                    row=row,
                    cohort_id=cohort.cohort_id,
                    cohort_source=str(cohort.source),
                    cohort_term_count=len(cohort.terms),
                    word_ordinal=ordinal,
                )
            )
    return hits


def corpus_word_ordinal_index(corpus: Corpus) -> dict[tuple[str, int, int, int], int]:
    index = {}
    for ordinal, word in enumerate(corpus.words):
        try:
            key = (normalize_book(word.book), int(word.chapter), int(word.verse), int(word.word_index))
        except ValueError:
            parsed = parse_ref(word.ref)
            if parsed is None:
                continue
            key = (parsed.book, parsed.chapter, parsed.verse, int(word.word_index))
        index[key] = ordinal
    return index


def word_ordinal_for_row(
    row: dict[str, str],
    *,
    word_indexes: dict[str, dict[tuple[str, int, int, int], int]],
) -> int | None:
    for field in ("center_word_ordinal", "word_ordinal"):
        explicit = parse_int(row.get(field, ""))
        if explicit is not None:
            return explicit
    corpus = row.get("corpus", "") or row.get("corpus_label", "")
    word_index = center_word_index(row)
    parsed = parse_ref(row.get("center_ref", ""))
    if not corpus or word_index is None or parsed is None:
        return None
    return word_indexes.get(corpus, {}).get((parsed.book, parsed.chapter, parsed.verse, word_index))


def center_word_index(row: dict[str, str]) -> int | None:
    for field in ("center_word_index", "word_index"):
        value = parse_int(row.get(field, ""))
        if value is not None:
            return value
    ref = row.get("center_ref", "")
    if "=" not in ref:
        return None
    return parse_int(ref.rsplit("=", 1)[1])


def parse_int(value: Any) -> int | None:
    try:
        text = str(value).strip()
        if not text:
            return None
        return int(text)
    except ValueError:
        return None


def cohort_window_rows(
    hits: list[PositionedHit],
    *,
    window_words: int,
    min_distinct_terms: int,
    max_windows: int,
) -> list[dict[str, object]]:
    if window_words < 1:
        raise ValueError("window_words must be >= 1")
    if min_distinct_terms < 1:
        raise ValueError("min_distinct_terms must be >= 1")
    if max_windows < 1:
        raise ValueError("max_windows must be >= 1")

    output: list[dict[str, object]] = []
    grouped: dict[tuple[str, str], list[PositionedHit]] = {}
    for hit in hits:
        grouped.setdefault((hit.cohort_id, corpus_label(hit.row)), []).append(hit)

    for (_cohort_id, _corpus), group_hits in sorted(grouped.items()):
        ordered = sorted(group_hits, key=lambda hit: (hit.word_ordinal, hit.row.get("term_id", "")))
        right = 0
        for left, start_hit in enumerate(ordered):
            while right < len(ordered) and ordered[right].word_ordinal - start_hit.word_ordinal <= window_words:
                right += 1
            window = ordered[left:right]
            distinct_terms = {hit.row.get("term_id", "") for hit in window}
            if len(distinct_terms) >= min_distinct_terms:
                output.append(window_row(window, window_words=window_words))
                if len(output) >= max_windows:
                    return output
    return output


def window_row(window: list[PositionedHit], *, window_words: int) -> dict[str, object]:
    first = min(window, key=lambda hit: hit.word_ordinal)
    last = max(window, key=lambda hit: hit.word_ordinal)
    term_ids = sorted({hit.row.get("term_id", "") for hit in window})
    concepts = sorted({hit.row.get("concept", "") for hit in window if hit.row.get("concept", "")})
    center_refs = sorted({hit.row.get("center_ref", "") for hit in window if hit.row.get("center_ref", "")})
    cohort_term_count = first.cohort_term_count
    return {
        "cohort_id": first.cohort_id,
        "cohort_source": first.cohort_source,
        "corpus": corpus_label(first.row),
        "corpus_class": first.row.get("corpus_class", ""),
        "window_words": window_words,
        "start_word_ordinal": first.word_ordinal,
        "end_word_ordinal": last.word_ordinal,
        "hit_count": len(window),
        "distinct_term_count": len(term_ids),
        "cohort_term_count": cohort_term_count,
        "cohort_full_house": "yes" if len(term_ids) >= cohort_term_count else "no",
        "term_ids": ";".join(term_ids),
        "concepts": ";".join(concepts),
        "center_refs": ";".join(center_refs),
        "first_center_ref": first.row.get("center_ref", ""),
        "last_center_ref": last.row.get("center_ref", ""),
        "strata": "cohort_cluster_density_window_N",
    }


def corpus_label(row: dict[str, str]) -> str:
    return row.get("corpus", "") or row.get("corpus_label", "")


def summarize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for bucket in ("cohort_id", "corpus"):
        values = sorted({str(row.get(bucket, "")) for row in rows})
        for value in values:
            bucket_rows = [row for row in rows if str(row.get(bucket, "")) == value]
            max_distinct = max((int(row.get("distinct_term_count", 0)) for row in bucket_rows), default=0)
            summary.append(
                {
                    "bucket": bucket,
                    "value": value,
                    "windows": len(bucket_rows),
                    "max_distinct_term_count": max_distinct,
                }
            )
    return summary


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    *,
    cohorts: list[Cohort],
    occurrence_rows: list[dict[str, str]],
    positioned_hits: list[PositionedHit],
    window_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "script": "scripts/build_cohort_cluster_density.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "settings": {
            "window_words": args.window_words,
            "min_distinct_terms": args.min_distinct_terms,
            "max_windows": args.max_windows,
        },
        "inputs": {
            "occurrences": str(args.occurrences),
            "cohorts": [str(cohort.source) for cohort in cohorts],
            "corpus_config": list(args.corpus_config),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "manifest_out": str(args.manifest_out),
        },
        "occurrence_rows": len(occurrence_rows),
        "positioned_cohort_hits": len(positioned_hits),
        "window_rows": len(window_rows),
        "summary_rows": len(summary_rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
