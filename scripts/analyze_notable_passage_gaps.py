#!/usr/bin/env python3
"""Record ELS absences and low-density terms in declared notable passages."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from els import __version__
from els.corpus import Corpus, VerseSpan, load_corpus
from els.search import build_hit, iter_els_query_matches_by_lanes, normalize_for_corpus
from els.statistics import benjamini_hochberg_q_values
from els.term_display import display_term
from scripts.analyze_mt_version_differences import normalize_book


DEFAULT_CORPORA = [
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "MAM=configs/example_mam.toml",
    "UHB=configs/example_uhb.toml",
]
DEFAULT_PASSAGES = Path("configs/notable_passage_gap_passages.csv")
DEFAULT_TERMS = Path("terms/notable_passage_gap_terms.csv")
DEFAULT_THEMATIC_CHAPTERS = Path("data/study/mappings/thematic_chapters.csv")
DEFAULT_TERMS_DIR = Path("terms")
OUT_DIR = Path("reports/notable_passage_gaps")
DETAIL_OUT = OUT_DIR / "term_gap_detail.csv"
SUMMARY_OUT = OUT_DIR / "passage_summary.csv"
MD_OUT = Path("docs/NOTABLE_PASSAGE_GAPS.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

DETAIL_FIELDS = [
    "passage_id",
    "passage_concept",
    "passage_category",
    "corpus_label",
    "corpus_name",
    "term_id",
    "concept",
    "category",
    "language",
    "term",
    "normalized_term",
    "normalized_length",
    "status",
    "gap_class",
    "common_elsewhere",
    "total_hits",
    "centered_in_passage",
    "centered_elsewhere",
    "expected_in_passage_uniform",
    "uniform_zero_probability",
    "uniform_zero_bh_q",
    "passage_letters",
    "corpus_letters",
    "passage_hit_rate_per_million",
    "corpus_hit_rate_per_million",
    "sample_center_refs",
    "sample_center_words",
]

SUMMARY_FIELDS = [
    "passage_id",
    "passage_concept",
    "passage_category",
    "corpus_label",
    "corpus_name",
    "language",
    "start_ref",
    "end_ref",
    "passage_letters",
    "corpus_letters",
    "eligible_terms",
    "skipped_terms",
    "terms_present_in_passage",
    "terms_absent_in_passage_present_elsewhere",
    "terms_absent_in_passage_common_elsewhere",
    "terms_no_hits_anywhere",
    "terms_low_vs_uniform",
    "observed_centered_hits_in_passage",
    "expected_centered_hits_in_passage_uniform",
]


@dataclass(frozen=True)
class RefKey:
    book: str
    chapter: int
    verse: int


@dataclass(frozen=True)
class Passage:
    passage_id: str
    concept: str
    category: str
    language: str
    corpus_group: str
    start_ref: str
    end_ref: str
    notes: str
    term_ids: str = ""


@dataclass(frozen=True)
class TermRow:
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    notes: str


@dataclass(frozen=True)
class PassageSpan:
    verses: tuple[VerseSpan, ...]
    norm_start: int
    norm_end: int
    norm_length: int


def ref_number(value: str) -> int:
    match = re.match(r"\d+", value.strip())
    if match is None:
        raise ValueError(f"unsupported ref number: {value}")
    return int(match.group(0))


def parse_ref(value: str) -> RefKey:
    book_and_rest = value.strip().rsplit(" ", 1)
    if len(book_and_rest) != 2 or ":" not in book_and_rest[1]:
        raise ValueError(f"unsupported ref: {value}")
    book, chapter_verse = book_and_rest
    chapter, verse = chapter_verse.split(":", 1)
    return RefKey(normalize_book(book), ref_number(chapter), ref_number(verse))


def verse_key(verse: VerseSpan) -> RefKey:
    return RefKey(normalize_book(verse.book), ref_number(verse.chapter), ref_number(verse.verse))


def verse_key_or_none(verse: VerseSpan) -> RefKey | None:
    try:
        return verse_key(verse)
    except ValueError:
        return None


def passage_span(corpus: Corpus, passage: Passage) -> PassageSpan:
    start = parse_ref(passage.start_ref)
    end = parse_ref(passage.end_ref)
    if (start.book, start.chapter, start.verse) > (end.book, end.chapter, end.verse):
        raise ValueError(f"passage start is after end: {passage.passage_id}")

    verses = tuple(verse for verse in corpus.verses if verse_in_range(verse, start, end))
    if not verses:
        raise ValueError(f"passage {passage.passage_id} not found in {corpus.name}")
    return PassageSpan(
        verses=verses,
        norm_start=min(verse.norm_start for verse in verses),
        norm_end=max(verse.norm_end for verse in verses),
        norm_length=sum(verse.norm_length for verse in verses),
    )


def verse_in_range(verse: VerseSpan, start: RefKey, end: RefKey) -> bool:
    key = verse_key_or_none(verse)
    if key is None:
        return False
    return (
        (start.book, start.chapter, start.verse)
        <= (key.book, key.chapter, key.verse)
        <= (end.book, end.chapter, end.verse)
    )


def offset_in_span(offset: int, span: PassageSpan) -> bool:
    return span.norm_start <= offset < span.norm_end


def classify_gap(
    *,
    total_hits: int,
    centered_in_passage: int,
    expected_in_passage: float,
    common_elsewhere: bool,
) -> str:
    if total_hits == 0:
        return "no_hits_anywhere"
    if centered_in_passage == 0:
        if common_elsewhere:
            return "absent_in_passage_common_elsewhere"
        return "absent_in_passage_present_elsewhere"
    if expected_in_passage >= 1.0 and centered_in_passage < expected_in_passage * 0.25:
        return "low_in_passage_vs_uniform"
    return "present_in_passage"


def term_allowed_for_passage(term: TermRow, passage: Passage) -> bool:
    allowed = passage_term_ids(passage)
    return not allowed or term.term_id in allowed


def passage_term_ids(passage: Passage) -> set[str]:
    return {
        value.strip()
        for value in re.split(r"[;,| ]+", passage.term_ids)
        if value.strip()
    }


def restricted_term_ids_for_passages(passages: list[Passage]) -> set[str] | None:
    if not passages:
        return set()
    restricted: set[str] = set()
    for passage in passages:
        term_ids = passage_term_ids(passage)
        if not term_ids:
            return None
        restricted.update(term_ids)
    return restricted


def read_passages(path: Path) -> list[Passage]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [passage_from_row(row) for row in csv.DictReader(handle)]


def read_terms(path: Path) -> list[TermRow]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [term_from_row(row) for row in csv.DictReader(handle)]


def passage_from_row(row: dict[str, str]) -> Passage:
    return Passage(
        passage_id=row.get("passage_id", ""),
        concept=row.get("concept", ""),
        category=row.get("category", ""),
        language=row.get("language", ""),
        corpus_group=row.get("corpus_group", ""),
        start_ref=row.get("start_ref", ""),
        end_ref=row.get("end_ref", ""),
        notes=row.get("notes", ""),
        term_ids=row.get("term_ids", ""),
    )


def term_from_row(row: dict[str, str]) -> TermRow:
    return TermRow(
        term_id=row.get("term_id", ""),
        concept=row.get("concept", ""),
        category=row.get("category", ""),
        language=row.get("language", ""),
        term=row.get("term", ""),
        notes=row.get("notes", ""),
    )


def read_term_lookup(terms_dir: Path) -> dict[str, TermRow]:
    lookup: dict[str, TermRow] = {}
    for path in sorted(terms_dir.glob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not {"term_id", "concept", "category", "language", "term"}.issubset(reader.fieldnames or ()):
                continue
            for row in reader:
                term = term_from_row(row)
                if term.term_id:
                    lookup.setdefault(term.term_id, term)
    return lookup


def read_thematic_chapter_targets(
    path: Path,
    *,
    terms_dir: Path,
) -> tuple[list[Passage], list[TermRow]]:
    if not path.exists():
        return [], []
    term_lookup = read_term_lookup(terms_dir)
    passages: list[Passage] = []
    terms: dict[str, TermRow] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            term_id = row.get("term_id", "").strip()
            term = term_lookup.get(term_id)
            if term is None:
                continue
            mapping_id = row.get("mapping_id", "").strip()
            book = row.get("book", "").strip()
            chapter_start = row.get("chapter_start", "").strip()
            chapter_end = row.get("chapter_end", "").strip()
            if not mapping_id or not book or not chapter_start or not chapter_end:
                continue
            passages.append(
                Passage(
                    passage_id=f"thematic_absence_{mapping_id}",
                    concept=f"{row.get('concept', term.concept)} Thematic Chapter",
                    category="thematic_chapter_absence",
                    language=row.get("language", term.language),
                    corpus_group="thematic_mapping",
                    start_ref=f"{book} {chapter_start}:1",
                    end_ref=f"{book} {chapter_end}:999",
                    notes=f"Generated from {path}:{mapping_id}",
                    term_ids=term_id,
                )
            )
            terms[term_id] = term
    return passages, list(terms.values())


def merge_terms(primary: list[TermRow], extra: list[TermRow]) -> list[TermRow]:
    merged: dict[str, TermRow] = {term.term_id: term for term in primary if term.term_id}
    for term in extra:
        if term.term_id:
            merged.setdefault(term.term_id, term)
    return list(merged.values())


def parse_corpus_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("corpus must be LABEL=path")
    label, path = value.split("=", 1)
    return label, Path(path)


def samples_join(values: Iterable[str], limit: int = 5) -> str:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
        if len(seen) >= limit:
            break
    return "; ".join(seen)


def analyze_corpus(
    *,
    corpus_label: str,
    corpus: Corpus,
    passages: list[Passage],
    terms: list[TermRow],
    min_skip: int,
    max_skip: int,
    direction: str,
    min_term_length: int,
    common_elsewhere_threshold: int,
    jobs: int,
    skip_missing_passages: bool = False,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    usable_passages = [passage for passage in passages if passage.language == corpus.language]
    spans: dict[str, PassageSpan] = {}
    found_passages: list[Passage] = []
    for passage in usable_passages:
        try:
            spans[passage.passage_id] = passage_span(corpus, passage)
        except ValueError:
            if skip_missing_passages:
                continue
            raise
        found_passages.append(passage)
    usable_passages = found_passages
    allowed_term_ids = restricted_term_ids_for_passages(usable_passages)

    eligible_by_query: dict[str, list[TermRow]] = defaultdict(list)
    skipped_terms: list[tuple[TermRow, str]] = []
    for term in terms:
        if term.language != corpus.language:
            continue
        if allowed_term_ids is not None and term.term_id not in allowed_term_ids:
            continue
        query = normalize_for_corpus(corpus, term.term)
        if len(query) < min_term_length:
            skipped_terms.append((term, query))
            continue
        eligible_by_query[query].append(term)

    counts: dict[str, int] = {query: 0 for query in eligible_by_query}
    passage_counts: dict[tuple[str, str], int] = defaultdict(int)
    passage_refs: dict[tuple[str, str], list[str]] = defaultdict(list)
    passage_words: dict[tuple[str, str], list[str]] = defaultdict(list)

    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        eligible_by_query.keys(),
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
    ):
        counts[query] += 1
        low = min(start, end)
        high = max(start, end)
        center_offset = (low + high) // 2
        matching_passages = [
            passage
            for passage in usable_passages
            if offset_in_span(center_offset, spans[passage.passage_id])
        ]
        if not matching_passages:
            continue
        hit = build_hit(corpus, query, query, skip, start, end)
        for passage in matching_passages:
            key = (passage.passage_id, query)
            passage_counts[key] += 1
            if len(passage_refs[key]) < 5:
                passage_refs[key].append(hit.center_ref)
                passage_words[key].append(hit.center_word)

    detail_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    corpus_letters = len(corpus.text)
    for passage in usable_passages:
        span = spans[passage.passage_id]
        observed_total = 0
        expected_total = 0.0
        eligible_terms = 0
        present_terms = 0
        absent_present_elsewhere = 0
        absent_common_elsewhere = 0
        no_hits_anywhere = 0
        low_vs_uniform = 0
        skipped_for_passage = 0

        for term, query in skipped_terms:
            if not term_allowed_for_passage(term, passage):
                continue
            skipped_for_passage += 1
            detail_rows.append(
                detail_row(
                    passage=passage,
                    corpus_label=corpus_label,
                    corpus=corpus,
                    term=term,
                    normalized_term=query,
                    status="skipped_short_term",
                    gap_class="skipped_short_term",
                    common_elsewhere=False,
                    total_hits=0,
                    centered_in_passage=0,
                    passage_span=span,
                    expected_in_passage=0.0,
                    sample_refs="",
                    sample_words="",
                )
            )

        for query, query_terms in eligible_by_query.items():
            allowed_query_terms = [term for term in query_terms if term_allowed_for_passage(term, passage)]
            if not allowed_query_terms:
                continue
            total_hits = counts[query]
            centered = passage_counts[(passage.passage_id, query)]
            expected = total_hits * span.norm_length / corpus_letters if corpus_letters else 0.0
            expected_total += expected
            observed_total += centered
            for term in allowed_query_terms:
                eligible_terms += 1
                common_elsewhere = (total_hits - centered) >= common_elsewhere_threshold
                gap_class = classify_gap(
                    total_hits=total_hits,
                    centered_in_passage=centered,
                    expected_in_passage=expected,
                    common_elsewhere=common_elsewhere,
                )
                if centered > 0:
                    present_terms += 1
                if gap_class == "absent_in_passage_present_elsewhere":
                    absent_present_elsewhere += 1
                elif gap_class == "absent_in_passage_common_elsewhere":
                    absent_present_elsewhere += 1
                    absent_common_elsewhere += 1
                elif gap_class == "no_hits_anywhere":
                    no_hits_anywhere += 1
                elif gap_class == "low_in_passage_vs_uniform":
                    low_vs_uniform += 1
                detail_rows.append(
                    detail_row(
                        passage=passage,
                        corpus_label=corpus_label,
                        corpus=corpus,
                        term=term,
                        normalized_term=query,
                        status="eligible",
                        gap_class=gap_class,
                        common_elsewhere=common_elsewhere,
                        total_hits=total_hits,
                        centered_in_passage=centered,
                        passage_span=span,
                        expected_in_passage=expected,
                        sample_refs=samples_join(passage_refs[(passage.passage_id, query)]),
                        sample_words=samples_join(passage_words[(passage.passage_id, query)]),
                    )
                )

        summary_rows.append(
            {
                "passage_id": passage.passage_id,
                "passage_concept": passage.concept,
                "passage_category": passage.category,
                "corpus_label": corpus_label,
                "corpus_name": corpus.name,
                "language": corpus.language,
                "start_ref": passage.start_ref,
                "end_ref": passage.end_ref,
                "passage_letters": span.norm_length,
                "corpus_letters": corpus_letters,
                "eligible_terms": eligible_terms,
                "skipped_terms": skipped_for_passage,
                "terms_present_in_passage": present_terms,
                "terms_absent_in_passage_present_elsewhere": absent_present_elsewhere,
                "terms_absent_in_passage_common_elsewhere": absent_common_elsewhere,
                "terms_no_hits_anywhere": no_hits_anywhere,
                "terms_low_vs_uniform": low_vs_uniform,
                "observed_centered_hits_in_passage": observed_total,
                "expected_centered_hits_in_passage_uniform": f"{expected_total:.3f}",
            }
        )
    return detail_rows, summary_rows


def detail_row(
    *,
    passage: Passage,
    corpus_label: str,
    corpus: Corpus,
    term: TermRow,
    normalized_term: str,
    status: str,
    gap_class: str,
    common_elsewhere: bool,
    total_hits: int,
    centered_in_passage: int,
    passage_span: PassageSpan,
    expected_in_passage: float,
    sample_refs: str,
    sample_words: str,
) -> dict[str, object]:
    passage_rate = (
        centered_in_passage / passage_span.norm_length * 1_000_000
        if passage_span.norm_length
        else 0.0
    )
    corpus_rate = total_hits / len(corpus.text) * 1_000_000 if corpus.text else 0.0
    return {
        "passage_id": passage.passage_id,
        "passage_concept": passage.concept,
        "passage_category": passage.category,
        "corpus_label": corpus_label,
        "corpus_name": corpus.name,
        "term_id": term.term_id,
        "concept": term.concept,
        "category": term.category,
        "language": term.language,
        "term": term.term,
        "normalized_term": normalized_term,
        "normalized_length": len(normalized_term),
        "status": status,
        "gap_class": gap_class,
        "common_elsewhere": str(common_elsewhere).lower(),
        "total_hits": total_hits,
        "centered_in_passage": centered_in_passage,
        "centered_elsewhere": max(total_hits - centered_in_passage, 0),
        "expected_in_passage_uniform": f"{expected_in_passage:.3f}",
        "uniform_zero_probability": f"{math.exp(-expected_in_passage):.6f}",
        "uniform_zero_bh_q": "",
        "passage_letters": passage_span.norm_length,
        "corpus_letters": len(corpus.text),
        "passage_hit_rate_per_million": f"{passage_rate:.3f}",
        "corpus_hit_rate_per_million": f"{corpus_rate:.3f}",
        "sample_center_refs": sample_refs,
        "sample_center_words": sample_words,
    }


def add_uniform_zero_q_values(rows: list[dict[str, object]]) -> None:
    p_values = [
        float(row["uniform_zero_probability"])
        if row.get("gap_class") in {"absent_in_passage_common_elsewhere", "low_in_passage_vs_uniform"}
        else None
        for row in rows
    ]
    q_values = benjamini_hochberg_q_values(p_values)
    for row, q_value in zip(rows, q_values, strict=True):
        row["uniform_zero_bh_q"] = "" if q_value is None else f"{q_value:.6f}"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    *,
    detail_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notable_absences = [
        row
        for row in detail_rows
        if row["gap_class"] in {"absent_in_passage_common_elsewhere", "low_in_passage_vs_uniform"}
    ]
    notable_absences.sort(
        key=lambda row: (
            0 if row["gap_class"] == "absent_in_passage_common_elsewhere" else 1,
            -int(row["centered_elsewhere"]),
            -float(row["expected_in_passage_uniform"]),
            str(row["passage_id"]),
            str(row["corpus_label"]),
            str(row["term_id"]),
        )
    )
    highest_gap_passages = sorted(
        summary_rows,
        key=lambda row: (
            -int(row["terms_absent_in_passage_common_elsewhere"]),
            -int(row["terms_low_vs_uniform"]),
            int(row["passage_letters"]),
            str(row["passage_id"]),
            str(row["corpus_label"]),
        ),
    )
    declared_gap_targets = [
        row for row in summary_rows if row.get("passage_category") == "notable_passage_gap"
    ]
    declared_gap_target_details = [
        row
        for row in notable_absences
        if row.get("passage_category") == "notable_passage_gap"
    ]
    lines = [
        f"# {getattr(args, 'title', 'Notable Passage Gaps')}",
        "",
        "This report records declared passages where selected ELS terms are absent, sparse, or present when centered inside the passage.",
        "It is intentionally a screening ledger: absence inside a short passage is often expected, so the useful rows are the terms that are absent in the passage while recurring elsewhere in the same corpus, or present at notably lower density than a uniform placement expectation.",
        "",
        "## Run Settings",
        "",
        f"- Passages: `{args.passages}`",
        f"- Config passages disabled: `{str(getattr(args, 'no_config_passages', False)).lower()}`",
        f"- Terms: `{args.terms}`",
        f"- Thematic chapters: `{getattr(args, 'thematic_chapters', None) or ''}`",
        f"- Skip range: `{args.min_skip}..{args.max_skip}`",
        f"- Direction: `{args.direction}`",
        f"- Jobs: `{args.jobs}`",
        f"- Minimum normalized term length: `{args.min_term_length}`",
        f"- Common-elsewhere threshold: `{args.common_elsewhere_threshold}` centered hits outside the passage",
        f"- Missing declared passages skipped: `{str(getattr(args, 'skip_missing_passages', False)).lower()}`",
        "",
        "## Highest Gap Passage Rows",
        "",
        "These rows rank declared passages by how many eligible terms are absent inside the passage while recurring at least the threshold count elsewhere in the same corpus. Short passages naturally rank high, so use this as a triage list rather than a formal significance test.",
        "",
        "| Passage | Corpus | Letters | Present | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in highest_gap_passages[:30]:
        lines.append(
            "| {passage_concept} | {corpus_label} | {passage_letters} | "
            "{terms_present_in_passage} | {terms_absent_in_passage_common_elsewhere} | "
            "{terms_low_vs_uniform} | {observed_centered_hits_in_passage} | "
            "{expected_centered_hits_in_passage_uniform} |".format(**row)
        )
    if declared_gap_targets:
        lines.extend(
            [
                "",
                "## Declared Gap-Target Passages",
                "",
                "These rows isolate passages explicitly registered as gap targets, instead of letting short high-profile passages dominate the global ranking.",
                "",
                "| Passage | Corpus | Letters | Present | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |",
                "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in declared_gap_targets:
            lines.append(
                "| {passage_concept} | {corpus_label} | {passage_letters} | "
                "{terms_present_in_passage} | {terms_absent_in_passage_common_elsewhere} | "
                "{terms_low_vs_uniform} | {observed_centered_hits_in_passage} | "
                "{expected_centered_hits_in_passage_uniform} |".format(**row)
            )
    if declared_gap_target_details:
        lines.extend(
            [
                "",
                "## Declared Gap-Target Detail",
                "",
                "| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Uniform Zero P | Uniform Zero Q | Sample Center Refs |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for row in declared_gap_target_details[:40]:
            term_display = display_term(str(row["normalized_term"]), english=str(row["concept"]))
            lines.append(
                "| {passage_concept} | {corpus_label} | {term} | {gap_class} | {centered_elsewhere} | "
                "{centered_in_passage} | {expected_in_passage_uniform} | {uniform_zero_probability} | "
                "{uniform_zero_bh_q} | {sample_center_refs} |".format(
                    passage_concept=row["passage_concept"],
                    corpus_label=row["corpus_label"],
                    term=term_display,
                    gap_class=row["gap_class"],
                    centered_elsewhere=row["centered_elsewhere"],
                    centered_in_passage=row["centered_in_passage"],
                    expected_in_passage_uniform=row["expected_in_passage_uniform"],
                    uniform_zero_probability=row["uniform_zero_probability"],
                    uniform_zero_bh_q=row.get("uniform_zero_bh_q", ""),
                    sample_center_refs=row["sample_center_refs"],
                )
            )
    lines.extend(
        [
            "",
        "## Passage Summary",
        "",
        "| Passage | Corpus | Letters | Eligible Terms | Present | Absent Elsewhere | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary_rows:
        lines.append(
            "| {passage_concept} | {corpus_label} | {passage_letters} | {eligible_terms} | "
            "{terms_present_in_passage} | {terms_absent_in_passage_present_elsewhere} | "
            "{terms_absent_in_passage_common_elsewhere} | {terms_low_vs_uniform} | "
            "{observed_centered_hits_in_passage} | {expected_centered_hits_in_passage_uniform} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Notable Absence / Low-Density Rows",
            "",
            "Rows are sorted by gap class first, then by how frequently the term appears centered elsewhere in the same corpus.",
            "",
            "| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Uniform Zero P | Uniform Zero Q | Sample Center Refs |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in notable_absences[:80]:
        term_display = display_term(str(row["normalized_term"]), english=str(row["concept"]))
        lines.append(
            "| {passage_concept} | {corpus_label} | {term} | {gap_class} | {centered_elsewhere} | "
            "{centered_in_passage} | {expected_in_passage_uniform} | {uniform_zero_probability} | "
            "{uniform_zero_bh_q} | {sample_center_refs} |".format(
                passage_concept=row["passage_concept"],
                corpus_label=row["corpus_label"],
                term=term_display,
                gap_class=row["gap_class"],
                centered_elsewhere=row["centered_elsewhere"],
                centered_in_passage=row["centered_in_passage"],
                expected_in_passage_uniform=row["expected_in_passage_uniform"],
                uniform_zero_probability=row["uniform_zero_probability"],
                uniform_zero_bh_q=row.get("uniform_zero_bh_q", ""),
                sample_center_refs=row["sample_center_refs"],
            )
        )
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- Detail CSV: `{args.detail_out}`",
            f"- Passage summary CSV: `{args.summary_out}`",
            f"- Manifest: `{args.manifest_out}`",
            "",
            "## Cautions",
            "",
            "- This report does not treat absence as a negative proof. It records silence and lower-density rows so they can be reviewed alongside positive centered hits.",
            "- `expected_in_passage_uniform` is a descriptive baseline only; it is not a formal p-value.",
            "- `uniform_zero_probability` is the simple Poisson `exp(-expected)` probability of zero hits under that uniform baseline; it is a triage aid, not a formal independence test.",
            "- `uniform_zero_bh_q` applies Benjamini-Hochberg correction to that simple zero-hit triage probability over absent/low-density detail rows.",
            "- Short surface terms can be skipped by the minimum term length rule; skipped rows remain in the detail CSV for auditability.",
            "- Passage ranges are resolved independently per source; versification and source differences can change passage letter counts even when the declared start/end refs are the same.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    *,
    args: argparse.Namespace,
    started: float,
    detail_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "script": "scripts/analyze_notable_passage_gaps.py",
        "version": __version__,
        "title": args.title,
        "started_at": datetime.fromtimestamp(started, UTC).isoformat(),
        "finished_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.time() - started, 3),
        "passages": str(args.passages),
        "terms": str(args.terms),
        "thematic_chapters": "" if args.thematic_chapters is None else str(args.thematic_chapters),
        "terms_dir": str(args.terms_dir),
        "no_config_passages": args.no_config_passages,
        "corpora": args.corpus,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "jobs": args.jobs,
        "min_term_length": args.min_term_length,
        "common_elsewhere_threshold": args.common_elsewhere_threshold,
        "skip_missing_passages": args.skip_missing_passages,
        "detail_rows": len(detail_rows),
        "summary_rows": len(summary_rows),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--passages", type=Path, default=DEFAULT_PASSAGES)
    parser.add_argument("--no-config-passages", action="store_true")
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--thematic-chapters", type=Path)
    parser.add_argument("--terms-dir", type=Path, default=DEFAULT_TERMS_DIR)
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=100)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--min-term-length", type=int, default=3)
    parser.add_argument("--common-elsewhere-threshold", type=int, default=10)
    parser.add_argument("--skip-missing-passages", action="store_true")
    parser.add_argument("--title", default="Notable Passage Gaps")
    parser.add_argument("--detail-out", type=Path, default=DETAIL_OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    args = parser.parse_args()

    started = time.time()
    passages = [] if args.no_config_passages else read_passages(args.passages)
    terms = read_terms(args.terms)
    if args.thematic_chapters is not None:
        thematic_passages, thematic_terms = read_thematic_chapter_targets(
            args.thematic_chapters,
            terms_dir=args.terms_dir,
        )
        passages.extend(thematic_passages)
        terms = merge_terms(terms, thematic_terms)
    corpus_specs = [parse_corpus_arg(value) for value in (args.corpus or DEFAULT_CORPORA)]

    detail_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    for label, path in corpus_specs:
        corpus = load_corpus(path)
        corpus_detail, corpus_summary = analyze_corpus(
            corpus_label=label,
            corpus=corpus,
            passages=passages,
            terms=terms,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            min_term_length=args.min_term_length,
            common_elsewhere_threshold=args.common_elsewhere_threshold,
            jobs=args.jobs,
            skip_missing_passages=args.skip_missing_passages,
        )
        detail_rows.extend(corpus_detail)
        summary_rows.extend(corpus_summary)

    add_uniform_zero_q_values(detail_rows)
    write_csv(args.detail_out, DETAIL_FIELDS, detail_rows)
    write_csv(args.summary_out, SUMMARY_FIELDS, summary_rows)
    write_markdown(args.markdown_out, detail_rows=detail_rows, summary_rows=summary_rows, args=args)
    write_manifest(
        args.manifest_out,
        args=args,
        started=started,
        detail_rows=detail_rows,
        summary_rows=summary_rows,
    )
    print(args.detail_out)
    print(args.summary_out)
    print(args.markdown_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
