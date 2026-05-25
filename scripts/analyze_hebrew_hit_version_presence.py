#!/usr/bin/env python3
"""Compare exact ELS hit patterns across labeled corpora."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.search import (
    ELSHit,
    build_hit,
    iter_els_query_matches_by_lanes,
    normalize_for_corpus,
    process_context,
)
from els.term_display import display_term
from scripts.analyze_mt_version_differences import normalize_book


DEFAULT_CORPORA = [
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "MAM=configs/example_mam.toml",
    "UHB=configs/example_uhb.toml",
]
DEFAULT_TERMS = Path("terms/modern_names_dates.csv")
OUT_DIR = Path("reports/hebrew_hit_version_presence")
PATTERNS_OUT = OUT_DIR / "hit_patterns.csv"
SUMMARY_OUT = OUT_DIR / "term_summary.csv"
MD_OUT = OUT_DIR / "hebrew_hit_version_presence.md"
MANIFEST_OUT = OUT_DIR / "manifest.json"

FOCUS_CONCEPTS = {
    "Trump",
    "Donald Trump",
    "Vance",
    "Netanyahu",
    "Iran",
    "Russia",
    "Europe",
    "Germany",
    "Turkey",
    "United States",
    "United States Of America",
    "USA",
    "United Nations",
    "European Union",
    "France",
    "Cowboy",
    "Catering",
    "Cowboy Catering",
    "Simsberry",
    "Simscorner",
}
LENINGRAD_LABELS = {"MT_WLC", "UXLC", "EBIBLE_WLC"}
NT_BOOK_ALIASES = {
    "mat": "Matt",
    "matt": "Matt",
    "matthew": "Matt",
    "mrk": "Mark",
    "mk": "Mark",
    "mark": "Mark",
    "luk": "Luke",
    "lk": "Luke",
    "luke": "Luke",
    "jhn": "John",
    "jn": "John",
    "john": "John",
    "act": "Acts",
    "acts": "Acts",
    "rom": "Rom",
    "romans": "Rom",
    "1co": "1Cor",
    "1cor": "1Cor",
    "1corinthians": "1Cor",
    "1 cor": "1Cor",
    "1 corinthians": "1Cor",
    "2co": "2Cor",
    "2cor": "2Cor",
    "2corinthians": "2Cor",
    "2 cor": "2Cor",
    "2 corinthians": "2Cor",
    "gal": "Gal",
    "galatians": "Gal",
    "eph": "Eph",
    "ephesians": "Eph",
    "php": "Phil",
    "phil": "Phil",
    "philippians": "Phil",
    "col": "Col",
    "colossians": "Col",
    "1th": "1Thess",
    "1thess": "1Thess",
    "1thessalonians": "1Thess",
    "1 thess": "1Thess",
    "1 thessalonians": "1Thess",
    "2th": "2Thess",
    "2thess": "2Thess",
    "2thessalonians": "2Thess",
    "2 thess": "2Thess",
    "2 thessalonians": "2Thess",
    "1ti": "1Tim",
    "1tim": "1Tim",
    "1timothy": "1Tim",
    "1 tim": "1Tim",
    "1 timothy": "1Tim",
    "2ti": "2Tim",
    "2tim": "2Tim",
    "2timothy": "2Tim",
    "2 tim": "2Tim",
    "2 timothy": "2Tim",
    "tit": "Titus",
    "titus": "Titus",
    "phm": "Phlm",
    "phlm": "Phlm",
    "philemon": "Phlm",
    "heb": "Heb",
    "hebrews": "Heb",
    "jas": "Jas",
    "jam": "Jas",
    "james": "Jas",
    "1pe": "1Pet",
    "1pet": "1Pet",
    "1peter": "1Pet",
    "1 pet": "1Pet",
    "1 peter": "1Pet",
    "2pe": "2Pet",
    "2pet": "2Pet",
    "2peter": "2Pet",
    "2 pet": "2Pet",
    "2 peter": "2Pet",
    "1jn": "1John",
    "1jhn": "1John",
    "1john": "1John",
    "1 john": "1John",
    "2jn": "2John",
    "2jhn": "2John",
    "2john": "2John",
    "2 john": "2John",
    "3jn": "3John",
    "3jhn": "3John",
    "3john": "3John",
    "3 john": "3John",
    "jud": "Jude",
    "jude": "Jude",
    "rev": "Rev",
    "revelation": "Rev",
}

PATTERN_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "present_corpora",
    "absent_corpora",
    "presence_scope",
    "hit_count",
    "center_words_by_corpus",
    "offsets_by_corpus",
    "read",
]
SUMMARY_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "observed_corpora",
    "hit_counts_by_corpus",
    "total_hits",
    "unique_patterns",
    "all_observed_patterns",
    "all_leningrad_patterns",
    "multi_source_patterns",
    "source_specific_patterns",
    "read",
]


@dataclass(frozen=True)
class TermRow:
    term_id: str
    concept: str
    category: str
    term: str


@dataclass(frozen=True)
class CorpusSource:
    label: str
    path: Path


@dataclass(frozen=True)
class CorpusMetadata:
    name: str
    verses: int
    letters: int


@dataclass(frozen=True)
class HitRecord:
    corpus: str
    term: TermRow
    normalized_term: str
    hit: ELSHit


@dataclass(frozen=True)
class CorpusHitResult:
    label: str
    metadata: CorpusMetadata
    records: list[HitRecord]
    observed: dict[str, set[str]]
    normalized_by_term: dict[str, str]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus_sources = parse_labeled_corpus_sources(args.corpus or DEFAULT_CORPORA)
    term_paths = args.terms or [DEFAULT_TERMS]
    concepts = selected_concepts(args, term_paths)
    terms = read_terms(
        term_paths,
        language=args.language,
        concepts=concepts,
        categories=args.category,
        term_ids=args.term_id,
        duplicate_policy=args.duplicate_term_id,
    )
    stable_labels = selected_stable_family_labels(args)
    records, observed, term_lookup, normalized_by_term, corpus_metadata = collect_hits_from_sources(
        corpus_sources,
        terms,
        args,
    )
    pattern_rows = pattern_presence_rows(records, observed, stable_labels)
    summary_rows = term_summary_rows(
        pattern_rows,
        records,
        observed,
        term_lookup,
        normalized_by_term,
        stable_family_name=args.stable_family_name,
    )
    write_rows(args.patterns_out, PATTERN_FIELDNAMES, pattern_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, pattern_rows, summary_rows, args)
    write_manifest(args, corpus_metadata, terms, records, pattern_rows, summary_rows, started)
    print(args.patterns_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, action="append", default=None)
    parser.add_argument("--language", choices=["hebrew", "greek"], default="hebrew")
    parser.add_argument("--concept", action="append", default=None)
    parser.add_argument("--category", action="append", default=None)
    parser.add_argument("--term-id", action="append", default=None)
    parser.add_argument("--all-concepts", action="store_true")
    parser.add_argument("--duplicate-term-id", choices=["error", "first"], default="error")
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=100)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--min-term-length", type=int, default=4)
    parser.add_argument("--max-hits-per-term", type=int, default=200)
    parser.add_argument(
        "--corpus-jobs",
        type=int,
        default=1,
        help="Parallel corpus workers. Use 0 for one worker per corpus.",
    )
    parser.add_argument("--stable-family-label", action="append", default=None)
    parser.add_argument("--stable-family-name", default="Leningrad-family")
    parser.add_argument("--no-stable-family", action="store_true")
    parser.add_argument("--report-title", default="Hebrew Hit Version Presence")
    parser.add_argument("--patterns-out", type=Path, default=PATTERNS_OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def selected_concepts(args: argparse.Namespace, term_paths: list[Path]) -> list[str] | None:
    if args.concept is not None:
        return args.concept
    if args.all_concepts or args.category or args.term_id:
        return None
    if term_paths == [DEFAULT_TERMS]:
        return sorted(FOCUS_CONCEPTS)
    return None


def selected_stable_family_labels(args: argparse.Namespace) -> set[str]:
    if args.no_stable_family:
        return set()
    if args.stable_family_label is not None:
        return set(args.stable_family_label)
    return set(LENINGRAD_LABELS)


def load_labeled_corpora(values: list[str]) -> dict[str, Corpus]:
    return load_labeled_corpus_sources(parse_labeled_corpus_sources(values))


def parse_labeled_corpus_sources(values: list[str]) -> list[CorpusSource]:
    return [CorpusSource(*split_labeled_path(value)) for value in values]


def load_labeled_corpus_sources(sources: list[CorpusSource]) -> dict[str, Corpus]:
    corpora: dict[str, Corpus] = {}
    for source in sources:
        corpora[source.label] = load_corpus(source.path)
    return corpora


def split_labeled_path(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, path = value.split("=", 1)
    if not label:
        raise ValueError(f"empty corpus label: {value}")
    return label, Path(path)


def read_terms(
    paths: list[Path],
    *,
    language: str = "hebrew",
    concepts: list[str] | None = None,
    categories: list[str] | None = None,
    term_ids: list[str] | None = None,
    duplicate_policy: str = "error",
) -> list[TermRow]:
    allowed_concepts = set(concepts or [])
    allowed_categories = set(categories or [])
    allowed_term_ids = set(term_ids or [])
    terms: list[TermRow] = []
    seen_term_ids: dict[str, Path] = {}
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("language", "") != language:
                    continue
                if allowed_concepts and row.get("concept", "") not in allowed_concepts:
                    continue
                if allowed_categories and row.get("category", "") not in allowed_categories:
                    continue
                if allowed_term_ids and row.get("term_id", "") not in allowed_term_ids:
                    continue
                term_id = row.get("term_id", "")
                if term_id in seen_term_ids:
                    if duplicate_policy == "first":
                        continue
                    previous = seen_term_ids[term_id]
                    raise ValueError(
                        f"duplicate selected term_id {term_id!r} in {previous} and {path}"
                    )
                seen_term_ids[term_id] = path
                terms.append(
                    TermRow(
                        term_id=term_id,
                        concept=row.get("concept", ""),
                        category=row.get("category", ""),
                        term=row.get("term", ""),
                    )
                )
    return terms


def collect_hits(
    corpora: dict[str, Corpus],
    terms: list[TermRow],
    args: argparse.Namespace,
) -> tuple[list[HitRecord], dict[str, set[str]], dict[str, TermRow], dict[str, str]]:
    records: list[HitRecord] = []
    observed: dict[str, set[str]] = defaultdict(set)
    term_lookup = {term.term_id: term for term in terms}
    normalized_by_term: dict[str, str] = {}
    for corpus_label, corpus in corpora.items():
        terms_by_query: dict[str, list[TermRow]] = defaultdict(list)
        for term in terms:
            normalized = normalize_for_corpus(corpus, term.term)
            if len(normalized) < args.min_term_length:
                continue
            observed[term.term_id].add(corpus_label)
            normalized_by_term.setdefault(term.term_id, normalized)
            terms_by_query[normalized].append(term)

        query_hit_counts: dict[str, int] = defaultdict(int)
        capped_queries: set[str] = set()
        cap = args.max_hits_per_term if args.max_hits_per_term > 0 else None
        for query, skip, start, end in iter_els_query_matches_by_lanes(
            corpus.text,
            terms_by_query.keys(),
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            max_hits_per_query=cap,
        ):
            if cap is not None and query_hit_counts[query] >= cap:
                continue
            for term in terms_by_query[query]:
                hit = build_hit(corpus, term.term, query, skip, start, end)
                records.append(
                    HitRecord(
                        corpus=corpus_label,
                        term=term,
                        normalized_term=hit.normalized_term,
                        hit=hit,
                    )
                )
            query_hit_counts[query] += 1
            if cap is not None and query_hit_counts[query] >= cap:
                capped_queries.add(query)
                if len(capped_queries) == len(terms_by_query):
                    break
    return records, observed, term_lookup, normalized_by_term


def collect_hits_from_sources(
    sources: list[CorpusSource],
    terms: list[TermRow],
    args: argparse.Namespace,
) -> tuple[
    list[HitRecord],
    dict[str, set[str]],
    dict[str, TermRow],
    dict[str, str],
    dict[str, CorpusMetadata],
]:
    jobs = resolve_corpus_jobs(args.corpus_jobs, len(sources))
    if jobs == 1:
        return collect_hits_from_sources_sequential(sources, terms, args)

    results: list[CorpusHitResult] = []
    try:
        executor = ProcessPoolExecutor(max_workers=jobs, mp_context=process_context())
    except PermissionError:
        return collect_hits_from_sources_sequential(sources, terms, args)

    with executor:
        payloads = [(source, terms, args) for source in sources]
        for result in executor.map(collect_hits_for_source_worker, payloads):
            results.append(result)
    records, observed, normalized_by_term, corpus_metadata = merge_corpus_hit_results(results)
    return records, observed, {term.term_id: term for term in terms}, normalized_by_term, corpus_metadata


def collect_hits_from_sources_sequential(
    sources: list[CorpusSource],
    terms: list[TermRow],
    args: argparse.Namespace,
) -> tuple[
    list[HitRecord],
    dict[str, set[str]],
    dict[str, TermRow],
    dict[str, str],
    dict[str, CorpusMetadata],
]:
    corpora = load_labeled_corpus_sources(sources)
    records, observed, term_lookup, normalized_by_term = collect_hits(
        corpora,
        terms,
        args,
    )
    return (
        records,
        observed,
        term_lookup,
        normalized_by_term,
        corpus_metadata_from_corpora(corpora),
    )


def collect_hits_for_source_worker(
    payload: tuple[CorpusSource, list[TermRow], argparse.Namespace],
) -> CorpusHitResult:
    source, terms, args = payload
    corpus = load_corpus(source.path)
    records, observed, _term_lookup, normalized_by_term = collect_hits(
        {source.label: corpus},
        terms,
        args,
    )
    return CorpusHitResult(
        label=source.label,
        metadata=corpus_metadata(corpus),
        records=records,
        observed={term_id: set(labels) for term_id, labels in observed.items()},
        normalized_by_term=normalized_by_term,
    )


def merge_corpus_hit_results(
    results: list[CorpusHitResult],
) -> tuple[list[HitRecord], dict[str, set[str]], dict[str, str], dict[str, CorpusMetadata]]:
    records: list[HitRecord] = []
    observed: dict[str, set[str]] = defaultdict(set)
    normalized_by_term: dict[str, str] = {}
    corpus_metadata_by_label: dict[str, CorpusMetadata] = {}
    for result in results:
        corpus_metadata_by_label[result.label] = result.metadata
        records.extend(result.records)
        for term_id, labels in result.observed.items():
            observed[term_id].update(labels)
        for term_id, normalized in result.normalized_by_term.items():
            normalized_by_term.setdefault(term_id, normalized)
    return records, observed, normalized_by_term, corpus_metadata_by_label


def corpus_metadata_from_corpora(corpora: dict[str, Corpus]) -> dict[str, CorpusMetadata]:
    return {label: corpus_metadata(corpus) for label, corpus in corpora.items()}


def corpus_metadata(corpus: Corpus) -> CorpusMetadata:
    return CorpusMetadata(
        name=corpus.name,
        verses=len(corpus.verses),
        letters=len(corpus.text),
    )


def resolve_corpus_jobs(corpus_jobs: int, corpus_count: int) -> int:
    if corpus_jobs < 0:
        raise SystemExit("--corpus-jobs must be >= 0")
    if corpus_jobs == 0:
        corpus_jobs = corpus_count
    return max(1, min(corpus_jobs, max(1, corpus_count)))


def pattern_presence_rows(
    records: list[HitRecord],
    observed: dict[str, set[str]],
    stable_labels: set[str] | None = None,
) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, int, str, str, str, str], list[HitRecord]] = defaultdict(list)
    for record in records:
        groups[pattern_key(record)].append(record)
    rows = [
        pattern_row(group, observed[group[0].term.term_id], stable_labels)
        for group in groups.values()
    ]
    return sorted(rows, key=pattern_sort_key)


def pattern_key(record: HitRecord) -> tuple[str, str, int, str, str, str, str]:
    hit = record.hit
    return (
        record.term.term_id,
        record.normalized_term,
        hit.skip,
        hit.direction,
        canonical_ref(hit.start_ref),
        canonical_ref(hit.center_ref),
        canonical_ref(hit.end_ref),
    )


def canonical_ref(ref: str) -> str:
    if not ref or " " not in ref or ":" not in ref:
        return ref
    book, rest = ref.rsplit(" ", 1)
    chapter, verse = rest.split(":", 1)
    try:
        book = canonical_book(book)
        return f"{book} {int(chapter)}:{int(verse)}"
    except (ValueError, TypeError):
        return ref


def canonical_book(book: str) -> str:
    cleaned = " ".join(book.strip().replace("_", " ").split()).lower()
    collapsed = cleaned.replace(" ", "")
    for key in (cleaned, collapsed):
        if key in NT_BOOK_ALIASES:
            return NT_BOOK_ALIASES[key]
    return normalize_book(book)


def pattern_row(
    group: list[HitRecord],
    observed_corpora: set[str],
    stable_labels: set[str] | None = None,
) -> dict[str, object]:
    first = group[0]
    hit = first.hit
    present = sorted({record.corpus for record in group})
    absent = sorted(observed_corpora - set(present))
    scope = presence_scope(present, absent, stable_labels)
    return {
        "term_id": first.term.term_id,
        "concept": first.term.concept,
        "category": first.term.category,
        "term": first.term.term,
        "normalized_term": first.normalized_term,
        "skip": hit.skip,
        "direction": hit.direction,
        "start_ref": canonical_ref(hit.start_ref),
        "center_ref": canonical_ref(hit.center_ref),
        "end_ref": canonical_ref(hit.end_ref),
        "present_corpora": ",".join(present),
        "absent_corpora": ",".join(absent),
        "presence_scope": scope,
        "hit_count": len(group),
        "center_words_by_corpus": "; ".join(
            f"{record.corpus}:{record.hit.center_normalized_word}" for record in group
        ),
        "offsets_by_corpus": "; ".join(
            f"{record.corpus}:{record.hit.start_offset}-{record.hit.end_offset}"
            for record in group
        ),
        "read": read_label(scope),
    }


def presence_scope(
    present: list[str],
    absent: list[str],
    stable_labels: set[str] | None = None,
) -> str:
    if stable_labels is None:
        stable_labels = LENINGRAD_LABELS
    present_set = set(present)
    if not absent:
        return "present_all_observed_sources"
    if stable_labels and stable_labels.issubset(present_set):
        return "present_all_leningrad_streams"
    if len(present_set) > 1:
        return "present_multiple_sources"
    return "source_specific"


def read_label(scope: str) -> str:
    if scope == "present_all_observed_sources":
        return "same ref-key pattern present in every compatible corpus"
    if scope == "present_all_leningrad_streams":
        return "stable across Leningrad-family streams; not all MT-family streams"
    if scope == "present_multiple_sources":
        return "multi-source pattern; inspect version distribution"
    return "source-specific exact ref-key pattern"


def term_summary_rows(
    pattern_rows: list[dict[str, object]],
    records: list[HitRecord],
    observed: dict[str, set[str]],
    term_lookup: dict[str, TermRow] | None = None,
    normalized_terms: dict[str, str] | None = None,
    stable_family_name: str = "Leningrad-family",
) -> list[dict[str, object]]:
    term_lookup = term_lookup or {}
    normalized_terms = normalized_terms or {}
    patterns_by_term: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in pattern_rows:
        patterns_by_term[str(row["term_id"])].append(row)
    hit_counts: dict[tuple[str, str], int] = defaultdict(int)
    term_meta: dict[str, TermRow] = {}
    normalized_by_term: dict[str, str] = {}
    for record in records:
        hit_counts[(record.term.term_id, record.corpus)] += 1
        term_meta[record.term.term_id] = record.term
        normalized_by_term[record.term.term_id] = record.normalized_term
    rows: list[dict[str, object]] = []
    for term_id, corpora in sorted(observed.items()):
        meta = (
            term_meta.get(term_id)
            or term_lookup.get(term_id)
            or term_from_pattern(patterns_by_term.get(term_id, []))
        )
        patterns = patterns_by_term.get(term_id, [])
        scope_counts = defaultdict(int)
        for row in patterns:
            scope_counts[str(row["presence_scope"])] += 1
        counts_by_corpus = {
            corpus: hit_counts.get((term_id, corpus), 0)
            for corpus in sorted(corpora)
        }
        rows.append(
            {
                "term_id": term_id,
                "concept": meta.concept,
                "category": meta.category,
                "term": meta.term,
                "normalized_term": normalized_by_term.get(term_id, normalized_terms.get(term_id, "")),
                "observed_corpora": ",".join(sorted(corpora)),
                "hit_counts_by_corpus": "; ".join(
                    f"{corpus}:{count}" for corpus, count in counts_by_corpus.items()
                ),
                "total_hits": sum(counts_by_corpus.values()),
                "unique_patterns": len(patterns),
                "all_observed_patterns": scope_counts["present_all_observed_sources"],
                "all_leningrad_patterns": scope_counts["present_all_leningrad_streams"],
                "multi_source_patterns": scope_counts["present_multiple_sources"],
                "source_specific_patterns": scope_counts["source_specific"],
                "read": term_read(scope_counts, len(patterns), stable_family_name),
            }
        )
    return sorted(rows, key=summary_sort_key)


def term_from_pattern(patterns: list[dict[str, object]]) -> TermRow:
    if not patterns:
        return TermRow("", "", "", "")
    first = patterns[0]
    return TermRow(
        term_id=str(first["term_id"]),
        concept=str(first["concept"]),
        category=str(first["category"]),
        term=str(first["term"]),
    )


def term_read(
    scope_counts: dict[str, int],
    pattern_count: int,
    stable_family_name: str = "Leningrad-family",
) -> str:
    if pattern_count == 0:
        return "no exact patterns in capped scan"
    if scope_counts.get("present_all_observed_sources", 0):
        return "has exact patterns stable across all observed streams"
    if scope_counts.get("present_all_leningrad_streams", 0):
        return f"has exact patterns stable across {stable_family_name} streams"
    if scope_counts.get("present_multiple_sources", 0):
        return "has some multi-source exact patterns"
    return "only source-specific exact patterns in capped scan"


def pattern_sort_key(row: dict[str, object]) -> tuple[int, str, str, int, str]:
    scope_order = {
        "present_all_observed_sources": 0,
        "present_all_leningrad_streams": 1,
        "present_multiple_sources": 2,
        "source_specific": 3,
    }
    return (
        scope_order.get(str(row["presence_scope"]), 9),
        str(row["concept"]),
        str(row["normalized_term"]),
        -int(row["hit_count"]),
        str(row["center_ref"]),
    )


def summary_sort_key(row: dict[str, object]) -> tuple[int, str]:
    return (-int(row["all_observed_patterns"]) - int(row["all_leningrad_patterns"]), str(row["term_id"]))


def write_rows(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    pattern_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    scope_counts = defaultdict(int)
    for row in pattern_rows:
        scope_counts[str(row["presence_scope"])] += 1
    lines = [
        f"# {args.report_title}",
        "",
        "This report compares exact ELS hit ref-key patterns across configured",
        "corpora. A pattern key is term + normalized term + signed skip + direction",
        "+ canonical start/center/end refs. Offsets are reported separately because",
        "source streams can differ in length.",
        "",
        "## Scope",
        "",
        f"- Skip range: `{args.min_skip}..{args.max_skip}`",
        f"- Direction: `{args.direction}`",
        f"- Minimum normalized term length: `{args.min_term_length}`",
        f"- Max hits per term per corpus: `{args.max_hits_per_term}`",
        f"- Language: `{args.language}`",
        f"- Term files: `{', '.join(str(path) for path in (args.terms or [DEFAULT_TERMS]))}`",
        "",
        "## Current Read",
        "",
        *current_read_lines(pattern_rows, summary_rows),
        "",
        "## Pattern Scope Counts",
        "",
        "| Scope | Patterns |",
        "| --- | ---: |",
    ]
    for scope in [
        "present_all_observed_sources",
        "present_all_leningrad_streams",
        "present_multiple_sources",
        "source_specific",
    ]:
        lines.append(f"| `{scope}` | {scope_counts[scope]} |")
    lines.extend(
        [
            "",
            "## Term Summary",
            "",
            f"| Term | Hits by corpus | Unique patterns | All observed | All {args.stable_family_name} | Multi-source | Source-specific | Read |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in summary_rows[:80]:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_summary_term(row),
                    str(row["hit_counts_by_corpus"]),
                    str(row["unique_patterns"]),
                    str(row["all_observed_patterns"]),
                    str(row["all_leningrad_patterns"]),
                    str(row["multi_source_patterns"]),
                    str(row["source_specific_patterns"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Strongest Shared Pattern Rows",
            "",
            "| Term | Skip | Refs | Present | Absent | Read |",
            "| --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in pattern_rows[:80]:
        if row["presence_scope"] == "source_specific":
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    display_summary_term(row),
                    str(row["skip"]),
                    f"{row['start_ref']} / {row['center_ref']} / {row['end_ref']}",
                    str(row["present_corpora"]),
                    str(row["absent_corpora"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This is exact ref-key presence in a capped hit scan. It does not establish",
            "textual identity, and it can miss later hits once the per-term cap is",
            "reached. Use it to find stable review rows, not to score significance.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def display_summary_term(row: dict[str, object]) -> str:
    return " ".join(
        part
        for part in [
            f"`{row['term_id']}`",
            display_term(
                str(row.get("normalized_term", "")),
                english=str(row.get("concept", "")),
            ),
        ]
        if part
    )


def current_read_lines(
    pattern_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[str]:
    scope_counts = defaultdict(int)
    for row in pattern_rows:
        scope_counts[str(row["presence_scope"])] += 1
    no_exact = [
        str(row["term_id"])
        for row in summary_rows
        if int(row.get("unique_patterns", "0") or 0) == 0
    ]
    dense = [
        str(row["term_id"])
        for row in sorted(
            summary_rows,
            key=lambda row: (
                -int(row.get("all_observed_patterns", "0") or 0),
                -int(row.get("total_hits", "0") or 0),
                str(row["term_id"]),
            ),
        )[:8]
    ]
    lines = [
        (
            f"This run found {len(pattern_rows):,} exact ref-key pattern rows "
            f"across {len(summary_rows):,} normalized terms that met the length gate."
        ),
        (
            f"All-observed-source rows: {scope_counts['present_all_observed_sources']:,}; "
            f"Leningrad-family-only rows: {scope_counts['present_all_leningrad_streams']:,}; "
            f"source-specific rows: {scope_counts['source_specific']:,}."
        ),
    ]
    if dense:
        lines.append(
            "Highest all-source buckets are: "
            + ", ".join(f"`{term_id}`" for term_id in dense)
            + "."
        )
    if no_exact:
        lines.append(
            "No exact patterns in the capped scan for: "
            + ", ".join(f"`{term_id}`" for term_id in no_exact[:18])
            + ("." if len(no_exact) <= 18 else f", plus {len(no_exact) - 18} more.")
        )
    lines.extend(
        [
            "",
            "Interpretation: this is a source-version distribution report, not a",
            "significance report. Version stability is common for short strings across",
            "related MT-family streams, so stable rows should be treated as review",
            "queue material until separate controls and context review are applied.",
        ]
    )
    return lines


def write_manifest(
    args: argparse.Namespace,
    corpus_metadata: dict[str, CorpusMetadata],
    terms: list[TermRow],
    records: list[HitRecord],
    pattern_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "terms": [str(path) for path in (args.terms or [DEFAULT_TERMS])],
        "language": args.language,
        "concepts": args.concept,
        "categories": args.category,
        "term_ids": args.term_id,
        "stable_family_labels": sorted(selected_stable_family_labels(args)),
        "stable_family_name": args.stable_family_name,
        "term_count": len(terms),
        "corpora": {
            label: {
                "name": metadata.name,
                "verses": metadata.verses,
                "letters": metadata.letters,
            }
            for label, metadata in corpus_metadata.items()
        },
        "corpus_jobs": args.corpus_jobs,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "min_term_length": args.min_term_length,
        "max_hits_per_term": args.max_hits_per_term,
        "hit_records": len(records),
        "pattern_rows": len(pattern_rows),
        "summary_rows": len(summary_rows),
        "outputs": {
            "patterns": str(args.patterns_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
