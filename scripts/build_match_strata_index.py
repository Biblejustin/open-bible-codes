#!/usr/bin/env python3
"""Annotate centered occurrences with post-search match strata."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import load_corpus
from els.gematria import standard_gematria_value
from els.letter_stats import BigramProfile, BigramSurprise, LetterFrequencyAnomaly, LetterFrequencyProfile
from els.match_strata import (
    BoundaryIndex,
    BOOK_ORDER,
    boundary_strata_for_offsets,
    build_boundary_index,
    canonical_ref_sort_key,
    canonical_first_keys,
    center_position_strata_for_ref,
    direction_counts_by_key,
    direction_strata_by_key,
    normalize_book,
    parse_ref,
    parse_skip_values,
    row_identity,
)
from els.term_display import display_term


DEFAULT_OCCURRENCES = Path("reports/centered_occurrence_index/centered_occurrences.csv")
DEFAULT_OUT = Path("reports/match_strata_index/occurrence_strata.csv")
DEFAULT_SUMMARY_OUT = Path("reports/match_strata_index/strata_summary.csv")
DEFAULT_MARKDOWN = Path("docs/MATCH_STRATA_INDEX.md")
DEFAULT_MANIFEST = Path("reports/match_strata_index/manifest.json")
DEFAULT_MEANINGFUL_CONSTANTS = Path("terms/meaningful_constants.csv")
DEFAULT_THEMATIC_CHAPTERS = Path("data/study/mappings/thematic_chapters.csv")
DEFAULT_AUTHOR_BOOK_MAPPING = Path("data/study/mappings/author_book_mapping.csv")
DEFAULT_PROTAGONIST_NARRATIVE_MAPPING = Path("data/study/mappings/protagonist_narrative_mapping.csv")

GROUP_FIELDS = ("source_family", "source_queue", "corpus", "present_corpora", "term_id", "normalized_term")
DEFAULT_CORPUS_CONFIGS = (
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "MAM=configs/example_mam.toml",
    "UHB=configs/example_uhb.toml",
    "LXX=configs/example_ebible_grclxx.toml",
    "KJV=configs/example_ebible_engkjv.toml",
    "KJVA=configs/example_ebible_engkjv_apocrypha.toml",
    "TR_NT=configs/example_ebible_grctr.toml",
    "SBLGNT=configs/example_sblgnt.toml",
    "BYZ_NT=configs/example_ebible_grcmt.toml",
    "TCG_NT=configs/example_ebible_grctcgnt.toml",
)
LETTER_PATH_RE = re.compile(r"^\d+:.+@.+:(?:canonical|apocrypha):(?P<position>-?\d+)$")

FIELDNAMES = [
    "occurrence_rank",
    "source_family",
    "source_queue",
    "corpus_class",
    "corpus",
    "present_corpora",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "occurrence_type",
    "skip",
    "direction",
    "skip_equals_meaningful_constant",
    "meaningful_constant_skips",
    "meaningful_constant_labels",
    "gematria_scheme",
    "term_gematria_value",
    "skip_equals_term_gematria",
    "term_gematria_matching_skips",
    "center_word_gematria_scheme",
    "center_word_gematria_value",
    "skip_equals_center_word_gematria",
    "center_word_gematria_matching_skips",
    "bigram_surprise_stratum",
    "bigram_surprise_evidence",
    "bigram_min_count",
    "bigram_max_count",
    "letter_frequency_stratum",
    "letter_frequency_evidence",
    "letter_frequency_min_count",
    "letter_frequency_max_count",
    "forward_direction_count",
    "backward_direction_count",
    "direction_stratum",
    "direction_imbalance_score",
    "canonical_first_centered_occurrence",
    "canonical_first_group",
    "canonical_first_in_thematic_chapter",
    "thematic_chapter_mappings",
    "thematic_chapter_evidence",
    "author_in_own_book",
    "author_in_own_book_mappings",
    "author_in_own_book_evidence",
    "protagonist_in_own_narrative",
    "protagonist_in_own_narrative_mappings",
    "protagonist_in_own_narrative_evidence",
    "boundary_strata",
    "boundary_corpora",
    "boundary_evidence",
    "center_position_strata",
    "center_position_corpora",
    "center_position_evidence",
    "cross_skip_pair_at_word",
    "cross_skip_pair_count",
    "cross_skip_pair_terms",
    "cross_skip_pair_skips",
    "cross_skip_pair_at_letter",
    "cross_skip_pair_at_letter_count",
    "cross_skip_pair_at_letter_terms",
    "cross_skip_pair_within_N_letters",
    "cross_skip_pair_within_letter_distance",
    "cross_skip_pair_within_letter_min_distance",
    "cross_skip_pair_within_letter_count",
    "cross_skip_pair_within_letter_terms",
    "extended_strata",
    "review_note",
    "source_record",
]

SUMMARY_FIELDNAMES = ["stratum", "rows"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.occurrences)
    meaningful_constants = read_meaningful_constants(args.meaningful_constants)
    thematic_mappings = read_mapping_rows(args.thematic_chapters)
    author_mappings = read_mapping_rows(args.author_book_mapping)
    protagonist_mappings = read_mapping_rows(args.protagonist_narrative_mapping)
    corpus_configs = corpus_config_map(args.corpus_config)
    boundary_indexes, bigram_profiles, letter_frequency_profiles = load_corpus_metadata(corpus_configs)
    rows = build_strata_rows(
        input_rows,
        boundary_indexes=boundary_indexes,
        meaningful_constants=meaningful_constants,
        thematic_mappings=thematic_mappings,
        author_mappings=author_mappings,
        protagonist_mappings=protagonist_mappings,
        bigram_profiles=bigram_profiles,
        letter_frequency_profiles=letter_frequency_profiles,
    )
    summary_rows = build_summary_rows(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started, corpus_configs=corpus_configs)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--occurrences", type=Path, default=DEFAULT_OCCURRENCES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--meaningful-constants", type=Path, default=DEFAULT_MEANINGFUL_CONSTANTS)
    parser.add_argument("--thematic-chapters", type=Path, default=DEFAULT_THEMATIC_CHAPTERS)
    parser.add_argument("--author-book-mapping", type=Path, default=DEFAULT_AUTHOR_BOOK_MAPPING)
    parser.add_argument("--protagonist-narrative-mapping", type=Path, default=DEFAULT_PROTAGONIST_NARRATIVE_MAPPING)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    parser.add_argument("--cross-skip-letter-distance", type=int, default=10)
    parser.add_argument(
        "--corpus-config",
        action="append",
        default=[],
        help="Corpus label to config mapping, e.g. MT_WLC=configs/example_oshb_wlc.toml.",
    )
    return parser


def build_strata_rows(
    input_rows: list[dict[str, str]],
    *,
    boundary_indexes: dict[str, BoundaryIndex] | None = None,
    meaningful_constants: dict[int, str] | None = None,
    thematic_mappings: list[dict[str, str]] | None = None,
    author_mappings: list[dict[str, str]] | None = None,
    protagonist_mappings: list[dict[str, str]] | None = None,
    bigram_profiles: dict[str, BigramProfile] | None = None,
    letter_frequency_profiles: dict[str, LetterFrequencyProfile] | None = None,
    cross_skip_letter_distance: int = 10,
) -> list[dict[str, object]]:
    direction_counts = direction_counts_by_key(input_rows, key_fields=GROUP_FIELDS)
    direction_by_key = direction_strata_by_key(input_rows, key_fields=GROUP_FIELDS)
    canonical_first = canonical_first_keys(input_rows, group_fields=GROUP_FIELDS)
    boundary_indexes = boundary_indexes or {}
    meaningful_constants = meaningful_constants or {}
    thematic_mappings = thematic_mappings or []
    author_mappings = author_mappings or []
    protagonist_mappings = protagonist_mappings or []
    bigram_profiles = bigram_profiles or {}
    letter_frequency_profiles = letter_frequency_profiles or {}
    cross_skip = cross_skip_annotations(input_rows, within_letter_distance=cross_skip_letter_distance)
    output = []
    for row in input_rows:
        key = tuple(row.get(field, "") for field in GROUP_FIELDS)
        is_first = row_identity(row) in canonical_first
        counts = direction_counts[key]
        boundary_strata, boundary_corpora, boundary_evidence = boundary_annotations(row, boundary_indexes)
        center_position_strata, center_position_corpora, center_position_evidence = center_position_annotations(
            row,
            boundary_indexes,
        )
        thematic_matches = thematic_chapter_matches(row, thematic_mappings) if is_first else []
        author_matches = scoped_mapping_matches(
            row,
            author_mappings,
            term_field="author_term_id",
            name_field="author_name",
        )
        protagonist_matches = scoped_mapping_matches(
            row,
            protagonist_mappings,
            term_field="protagonist_term_id",
            name_field="protagonist_name",
        )
        cross = cross_skip.get(row_identity(row), {})
        skip_values = sorted({abs(value) for value in parse_skip_values(row.get("skip", ""))})
        constant_skips = [value for value in skip_values if value in meaningful_constants]
        gematria_scheme, term_gematria_value = standard_gematria_value(
            row.get("normalized_term", ""),
            row.get("language", ""),
        )
        gematria_skips = [value for value in skip_values if term_gematria_value > 0 and value == term_gematria_value]
        center_gematria_scheme, center_word_gematria_value = standard_gematria_value(
            row.get("center_normalized_word", ""),
            row.get("language", ""),
        )
        center_word_gematria_skips = [
            value for value in skip_values if center_word_gematria_value > 0 and value == center_word_gematria_value
        ]
        bigram_surprise = bigram_surprise_for_row(row, bigram_profiles)
        letter_frequency = letter_frequency_for_row(row, letter_frequency_profiles)
        strata = [
            row.get("occurrence_type", ""),
            direction_by_key.get(key, ""),
            *boundary_strata,
            *center_position_strata,
        ]
        if is_first:
            strata.append("canonical_first_occurrence")
        if thematic_matches:
            strata.append("canonical_first_in_thematic_chapter")
        if author_matches:
            strata.append("author_in_own_book")
        if protagonist_matches:
            strata.append("protagonist_in_own_narrative")
        if cross.get("word_pair_count"):
            strata.append("cross_skip_pair_at_word")
        if cross.get("letter_pair_count"):
            strata.append("cross_skip_pair_at_letter")
        if cross.get("within_pair_count"):
            strata.append("cross_skip_pair_within_N_letters")
        if constant_skips:
            strata.append("skip_equals_meaningful_constant")
        if gematria_skips:
            strata.append("skip_equals_term_gematria")
        if center_word_gematria_skips:
            strata.append("skip_equals_center_word_gematria")
        if bigram_surprise.stratum:
            strata.append(bigram_surprise.stratum)
        if letter_frequency.stratum:
            strata.append(letter_frequency.stratum)
        output.append(
            {
                "occurrence_rank": row.get("occurrence_rank", ""),
                "source_family": row.get("source_family", ""),
                "source_queue": row.get("source_queue", ""),
                "corpus_class": row.get("corpus_class", ""),
                "corpus": row.get("corpus", ""),
                "present_corpora": row.get("present_corpora", ""),
                "term_id": row.get("term_id", ""),
                "concept": row.get("concept", ""),
                "category": row.get("category", ""),
                "normalized_term": row.get("normalized_term", ""),
                "center_ref": row.get("center_ref", ""),
                "center_word": row.get("center_word", ""),
                "center_normalized_word": row.get("center_normalized_word", ""),
                "occurrence_type": row.get("occurrence_type", ""),
                "skip": row.get("skip", ""),
                "direction": row.get("direction", ""),
                "skip_equals_meaningful_constant": "yes" if constant_skips else "no",
                "meaningful_constant_skips": ";".join(str(value) for value in constant_skips),
                "meaningful_constant_labels": ";".join(meaningful_constants[value] for value in constant_skips),
                "gematria_scheme": gematria_scheme,
                "term_gematria_value": str(term_gematria_value) if term_gematria_value else "",
                "skip_equals_term_gematria": "yes" if gematria_skips else "no",
                "term_gematria_matching_skips": ";".join(str(value) for value in gematria_skips),
                "center_word_gematria_scheme": center_gematria_scheme,
                "center_word_gematria_value": (
                    str(center_word_gematria_value) if center_word_gematria_value else ""
                ),
                "skip_equals_center_word_gematria": "yes" if center_word_gematria_skips else "no",
                "center_word_gematria_matching_skips": ";".join(
                    str(value) for value in center_word_gematria_skips
                ),
                "bigram_surprise_stratum": bigram_surprise.stratum,
                "bigram_surprise_evidence": bigram_surprise.evidence,
                "bigram_min_count": "" if bigram_surprise.min_count is None else str(bigram_surprise.min_count),
                "bigram_max_count": "" if bigram_surprise.max_count is None else str(bigram_surprise.max_count),
                "letter_frequency_stratum": letter_frequency.stratum,
                "letter_frequency_evidence": letter_frequency.evidence,
                "letter_frequency_min_count": (
                    "" if letter_frequency.min_count is None else str(letter_frequency.min_count)
                ),
                "letter_frequency_max_count": (
                    "" if letter_frequency.max_count is None else str(letter_frequency.max_count)
                ),
                "forward_direction_count": counts.forward,
                "backward_direction_count": counts.backward,
                "direction_stratum": direction_by_key.get(key, ""),
                "direction_imbalance_score": direction_imbalance_score(counts.forward, counts.backward),
                "canonical_first_centered_occurrence": "yes" if is_first else "no",
                "canonical_first_group": "|".join(key),
                "canonical_first_in_thematic_chapter": "yes" if thematic_matches else "no",
                "thematic_chapter_mappings": ";".join(match["mapping_id"] for match in thematic_matches),
                "thematic_chapter_evidence": ";".join(match["evidence"] for match in thematic_matches),
                "author_in_own_book": "yes" if author_matches else "no",
                "author_in_own_book_mappings": ";".join(match["mapping_id"] for match in author_matches),
                "author_in_own_book_evidence": ";".join(match["evidence"] for match in author_matches),
                "protagonist_in_own_narrative": "yes" if protagonist_matches else "no",
                "protagonist_in_own_narrative_mappings": ";".join(
                    match["mapping_id"] for match in protagonist_matches
                ),
                "protagonist_in_own_narrative_evidence": ";".join(
                    match["evidence"] for match in protagonist_matches
                ),
                "boundary_strata": ";".join(boundary_strata),
                "boundary_corpora": ";".join(boundary_corpora),
                "boundary_evidence": ";".join(boundary_evidence),
                "center_position_strata": ";".join(center_position_strata),
                "center_position_corpora": ";".join(center_position_corpora),
                "center_position_evidence": ";".join(center_position_evidence),
                "cross_skip_pair_at_word": "yes" if cross.get("word_pair_count") else "no",
                "cross_skip_pair_count": cross.get("word_pair_count", ""),
                "cross_skip_pair_terms": cross.get("word_terms", ""),
                "cross_skip_pair_skips": cross.get("word_skips", ""),
                "cross_skip_pair_at_letter": "yes" if cross.get("letter_pair_count") else "no",
                "cross_skip_pair_at_letter_count": cross.get("letter_pair_count", ""),
                "cross_skip_pair_at_letter_terms": cross.get("letter_terms", ""),
                "cross_skip_pair_within_N_letters": "yes" if cross.get("within_pair_count") else "no",
                "cross_skip_pair_within_letter_distance": (
                    str(cross_skip_letter_distance) if cross.get("within_pair_count") else ""
                ),
                "cross_skip_pair_within_letter_min_distance": cross.get("within_min_distance", ""),
                "cross_skip_pair_within_letter_count": cross.get("within_pair_count", ""),
                "cross_skip_pair_within_letter_terms": cross.get("within_terms", ""),
                "extended_strata": ";".join(value for value in strata if value),
                "review_note": row.get("review_note", ""),
                "source_record": row.get("source_record", ""),
            }
        )
    return output


def build_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts: Counter[str] = Counter()
    for row in rows:
        for stratum in str(row.get("extended_strata", "")).split(";"):
            if stratum:
                counts[stratum] += 1
    return [{"stratum": key, "rows": value} for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


def direction_imbalance_score(forward: int, backward: int) -> str:
    total = forward + backward
    if total == 0:
        return ""
    return f"{(forward - backward) / total:.6f}"


def cross_skip_annotations(
    rows: list[dict[str, str]],
    *,
    within_letter_distance: int = 10,
) -> dict[tuple[str, ...], dict[str, str]]:
    if within_letter_distance < 0:
        raise ValueError("within_letter_distance must be >= 0")
    annotations: dict[tuple[str, ...], dict[str, Any]] = {}
    word_groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        word_groups.setdefault(cross_skip_group_key(row), []).append(row)

    for group_rows in word_groups.values():
        if len({row.get("normalized_term", "") for row in group_rows}) < 2:
            continue
        skip_sets = {row_identity(row): set(parse_skip_values(row.get("skip", ""))) for row in group_rows}
        for row in group_rows:
            row_key = row_identity(row)
            row_skips = skip_sets[row_key]
            peer_rows = [
                peer
                for peer in group_rows
                if peer is not row
                and peer.get("normalized_term", "") != row.get("normalized_term", "")
                and has_different_skip(row_skips, skip_sets[row_identity(peer)])
            ]
            if not peer_rows:
                continue
            for peer in peer_rows:
                note_cross_skip_pair(
                    annotations,
                    row,
                    peer,
                    kind="word",
                    peer_skips=skip_sets[row_identity(peer)],
                )

    broad_groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        broad_groups.setdefault(cross_skip_broad_group_key(row), []).append(row)
    for group_rows in broad_groups.values():
        if len({row.get("normalized_term", "") for row in group_rows}) < 2:
            continue
        skip_sets = {row_identity(row): set(parse_skip_values(row.get("skip", ""))) for row in group_rows}
        path_positions = {row_identity(row): path_positions_by_corpus(row) for row in group_rows}
        endpoints = {row_identity(row): endpoint_positions_by_corpus(row) for row in group_rows}
        for left_index, left in enumerate(group_rows):
            left_key = row_identity(left)
            for right in group_rows[left_index + 1 :]:
                right_key = row_identity(right)
                if left.get("normalized_term", "") == right.get("normalized_term", ""):
                    continue
                if not has_different_skip(skip_sets[left_key], skip_sets[right_key]):
                    continue
                if shares_letter_position(path_positions[left_key], path_positions[right_key]):
                    note_cross_skip_pair(
                        annotations,
                        left,
                        right,
                        kind="letter",
                        peer_skips=skip_sets[right_key],
                    )
                    note_cross_skip_pair(
                        annotations,
                        right,
                        left,
                        kind="letter",
                        peer_skips=skip_sets[left_key],
                    )
                distance = minimum_endpoint_distance(endpoints[left_key], endpoints[right_key])
                if distance is not None and distance <= within_letter_distance:
                    note_cross_skip_pair(
                        annotations,
                        left,
                        right,
                        kind="within",
                        peer_skips=skip_sets[right_key],
                        distance=distance,
                    )
                    note_cross_skip_pair(
                        annotations,
                        right,
                        left,
                        kind="within",
                        peer_skips=skip_sets[left_key],
                        distance=distance,
                    )
    return finalize_cross_skip_annotations(annotations)


def note_cross_skip_pair(
    annotations: dict[tuple[str, ...], dict[str, Any]],
    row: dict[str, str],
    peer: dict[str, str],
    *,
    kind: str,
    peer_skips: set[int],
    distance: int | None = None,
) -> None:
    annotation = annotations.setdefault(row_identity(row), {})
    annotation.setdefault(f"{kind}_terms", set()).add(peer.get("normalized_term", ""))
    annotation.setdefault(f"{kind}_skips", set()).update(peer_skips)
    annotation[f"{kind}_pair_count"] = int(annotation.get(f"{kind}_pair_count", 0)) + 1
    if distance is not None:
        current = annotation.get(f"{kind}_min_distance")
        annotation[f"{kind}_min_distance"] = distance if current is None else min(int(current), distance)


def finalize_cross_skip_annotations(
    annotations: dict[tuple[str, ...], dict[str, Any]],
) -> dict[tuple[str, ...], dict[str, str]]:
    output: dict[tuple[str, ...], dict[str, str]] = {}
    for key, annotation in annotations.items():
        row: dict[str, str] = {}
        for kind in ("word", "letter", "within"):
            pair_count = int(annotation.get(f"{kind}_pair_count", 0))
            if not pair_count:
                continue
            terms = sorted(value for value in annotation.get(f"{kind}_terms", set()) if value)
            skips = sorted(annotation.get(f"{kind}_skips", set()))
            row[f"{kind}_pair_count"] = str(pair_count)
            row[f"{kind}_terms"] = ";".join(terms)
            row[f"{kind}_skips"] = ";".join(str(value) for value in skips)
            if f"{kind}_min_distance" in annotation:
                row[f"{kind}_min_distance"] = str(annotation[f"{kind}_min_distance"])
        output[key] = row
    return output


def cross_skip_group_key(row: dict[str, str]) -> tuple[str, str, str, str, str, str, str]:
    return (
        row.get("source_family", ""),
        row.get("source_queue", ""),
        row.get("corpus", ""),
        row.get("present_corpora", ""),
        row.get("center_ref", ""),
        row.get("center_normalized_word", ""),
        row.get("center_word", ""),
    )


def cross_skip_broad_group_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("source_family", ""),
        row.get("source_queue", ""),
        row.get("corpus", ""),
        row.get("present_corpora", ""),
    )


def has_different_skip(left: set[int], right: set[int]) -> bool:
    if not left or not right:
        return False
    return any(left_skip != right_skip for left_skip in left for right_skip in right)


def path_positions_by_corpus(row: dict[str, str]) -> dict[str, set[int]]:
    corpus = row.get("corpus", "")
    positions: dict[str, set[int]] = {}
    letter_positions = letter_path_positions(row)
    if corpus and letter_positions:
        positions[corpus] = set(letter_positions)
    for record_corpus, start, end in offset_records(row):
        positions.setdefault(record_corpus, set()).update(reconstructed_path_positions(row, start, end))
    return positions


def endpoint_positions_by_corpus(row: dict[str, str]) -> dict[str, set[int]]:
    endpoints: dict[str, set[int]] = {}
    for corpus, start, end in offset_records(row):
        endpoints.setdefault(corpus, set()).update((start, end))
    if endpoints:
        return endpoints
    corpus = row.get("corpus", "")
    positions = letter_path_positions(row)
    if corpus and positions:
        endpoints[corpus] = {min(positions), max(positions)}
    return endpoints


def letter_path_positions(row: dict[str, str]) -> list[int]:
    positions = []
    for part in row.get("letter_path", "").split(";"):
        match = LETTER_PATH_RE.match(part.strip())
        if match:
            positions.append(int(match.group("position")))
    return positions


def reconstructed_path_positions(row: dict[str, str], start: int, end: int) -> set[int]:
    term_length = len(row.get("normalized_term", ""))
    if term_length <= 1:
        return {start}
    gap_count = term_length - 1
    delta = end - start
    if delta % gap_count != 0:
        return {start, end}
    step = delta // gap_count
    return {start + index * step for index in range(term_length)}


def shares_letter_position(left: dict[str, set[int]], right: dict[str, set[int]]) -> bool:
    for corpus in set(left) & set(right):
        if left[corpus] & right[corpus]:
            return True
    return False


def minimum_endpoint_distance(left: dict[str, set[int]], right: dict[str, set[int]]) -> int | None:
    distances = [
        abs(left_position - right_position)
        for corpus in set(left) & set(right)
        for left_position in left[corpus]
        for right_position in right[corpus]
    ]
    if not distances:
        return None
    return min(distances)


def bigram_surprise_for_row(row: dict[str, str], profiles: dict[str, BigramProfile]) -> BigramSurprise:
    profile = profiles.get(row.get("corpus", ""))
    if profile is None:
        return BigramProfile.from_text("").classify_term("")
    return profile.classify_term(row.get("normalized_term", ""))


def letter_frequency_for_row(
    row: dict[str, str],
    profiles: dict[str, LetterFrequencyProfile],
) -> LetterFrequencyAnomaly:
    profile = profiles.get(row.get("corpus", ""))
    if profile is None:
        return LetterFrequencyProfile.from_text("").classify_term("")
    return profile.classify_term(row.get("normalized_term", ""))


def thematic_chapter_matches(row: dict[str, str], mappings: list[dict[str, str]]) -> list[dict[str, str]]:
    center = parse_ref(row.get("center_ref", ""))
    if center is None:
        return []
    matches: list[dict[str, str]] = []
    for mapping in mappings:
        if mapping.get("term_id", "").strip() != row.get("term_id", "").strip():
            continue
        book = normalize_book(mapping.get("book", ""))
        if book != center.book:
            continue
        try:
            chapter_start = int(mapping.get("chapter_start", ""))
            chapter_end = int(mapping.get("chapter_end", ""))
        except ValueError:
            continue
        if chapter_start <= center.chapter <= chapter_end:
            matches.append(
                {
                    "mapping_id": mapping.get("mapping_id", ""),
                    "evidence": (
                        f"{mapping.get('mapping_id', '')}:"
                        f"{book} {chapter_start}-{chapter_end}"
                    ),
                }
            )
    return matches


def scoped_mapping_matches(
    row: dict[str, str],
    mappings: list[dict[str, str]],
    *,
    term_field: str,
    name_field: str,
) -> list[dict[str, str]]:
    center = parse_ref(row.get("center_ref", ""))
    if center is None:
        return []
    matches: list[dict[str, str]] = []
    for mapping in mappings:
        if mapping.get(term_field, "").strip() != row.get("term_id", "").strip():
            continue
        if not ref_inside_mapping_scope(center, mapping):
            continue
        matches.append(
            {
                "mapping_id": mapping.get("mapping_id", ""),
                "evidence": (
                    f"{mapping.get('mapping_id', '')}:"
                    f"{mapping.get(name_field, '')} "
                    f"{mapping.get('scope_start_ref', '')}-{mapping.get('scope_end_ref', '')}"
                ),
            }
        )
    return matches


def ref_inside_mapping_scope(center: Any, mapping: dict[str, str]) -> bool:
    book = normalize_book(mapping.get("book", ""))
    if book and book != center.book:
        return False
    start = parse_ref(mapping.get("scope_start_ref", ""))
    end = parse_ref(mapping.get("scope_end_ref", ""))
    if start is None or end is None:
        return bool(book and book == center.book)
    center_key = (BOOK_ORDER.get(center.book, 999999), center.chapter, center.verse)
    start_key = canonical_ref_sort_key(mapping.get("scope_start_ref", ""))[:3]
    end_key = canonical_ref_sort_key(mapping.get("scope_end_ref", ""))[:3]
    return start_key <= center_key <= end_key


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Extended Match Strata Index",
        "",
        "This index annotates the current centered occurrence index with cheap",
        "post-search strata. It does not promote any row to claim status. The",
        "extra flags are review-prioritization metadata that still require the",
        "same preregistered controls described in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Bottom Line",
        "",
        f"- annotated occurrence rows: {len(rows):,}",
        "- materialized now: `forward_only`, `backward_only`, `bidirectional_present`, `canonical_first_occurrence`, available `boundary_*` endpoint strata, and cross-skip pair strata.",
        "- mapping-dependent strata use locked CSVs under `data/study/mappings/` and stay blank until those maps are populated.",
        "- meaningful skip strata use the locked constants file and standard Hebrew/Greek gematria only as review flags.",
        "- bigram-surprise strata compare the hidden term's adjacent letter pairs to the matched corpus text.",
        "- letter-frequency anomaly strata compare the hidden term's individual letters to the matched corpus text.",
        "- center-position strata flag when the center verse is first/last in its chapter or book.",
        "- boundary strata are exact only when the source occurrence row retains endpoint offsets for a mapped corpus.",
        "",
        "## Strata Counts",
        "",
        "| Stratum | Rows |",
        "| --- | ---: |",
    ]
    for row in summary_rows:
        lines.append(f"| `{row['stratum']}` | {int(row['rows']):,} |")
    lines.extend(
        [
            "",
            "## Top Annotated Rows",
            "",
            "| Rank | Term | Center | Existing type | Direction stratum | Boundary strata | Canonical first | Source |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows[: args.markdown_row_limit]:
        lines.append(markdown_row(row))
    if len(rows) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | {len(rows) - args.markdown_row_limit:,} more rows in CSV |"
        )
    boundary_rows = [row for row in rows if row.get("boundary_strata")]
    if boundary_rows:
        lines.extend(
            [
                "",
                "## Boundary Rows",
                "",
                "| Rank | Term | Center | Boundary strata | Evidence | Source |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in boundary_rows[: args.markdown_row_limit]:
            lines.append(boundary_markdown_row(row))
        if len(boundary_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | {len(boundary_rows) - args.markdown_row_limit:,} more boundary rows in CSV |"
            )
    center_position_rows = [row for row in rows if row.get("center_position_strata")]
    if center_position_rows:
        lines.extend(
            [
                "",
                "## Center Position Rows",
                "",
                "| Rank | Term | Center | Center position strata | Evidence | Source |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in center_position_rows[: args.markdown_row_limit]:
            lines.append(center_position_markdown_row(row))
        if len(center_position_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | {len(center_position_rows) - args.markdown_row_limit:,} more center-position rows in CSV |"
            )
    cross_skip_rows = [
        row
        for row in rows
        if row.get("cross_skip_pair_at_word") == "yes"
        or row.get("cross_skip_pair_at_letter") == "yes"
        or row.get("cross_skip_pair_within_N_letters") == "yes"
    ]
    if cross_skip_rows:
        lines.extend(
            [
                "",
                "## Cross-Skip Pair Rows",
                "",
                "| Rank | Term | Center | At word | At letter | Within N letters | Source |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in cross_skip_rows[: args.markdown_row_limit]:
            lines.append(cross_skip_markdown_row(row))
        if len(cross_skip_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(cross_skip_rows) - args.markdown_row_limit:,} more cross-skip rows in CSV |"
            )
    mapping_rows = [
        row
        for row in rows
        if row.get("canonical_first_in_thematic_chapter") == "yes"
        or row.get("author_in_own_book") == "yes"
        or row.get("protagonist_in_own_narrative") == "yes"
    ]
    if mapping_rows:
        lines.extend(
            [
                "",
                "## Mapping-Dependent Rows",
                "",
                "| Rank | Term | Center | Thematic first | Author scope | Protagonist scope | Source |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in mapping_rows[: args.markdown_row_limit]:
            lines.append(mapping_markdown_row(row))
        if len(mapping_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(mapping_rows) - args.markdown_row_limit:,} more mapping rows in CSV |"
            )
    meaningful_rows = [
        row
        for row in rows
        if row.get("skip_equals_meaningful_constant") == "yes"
        or row.get("skip_equals_term_gematria") == "yes"
        or row.get("skip_equals_center_word_gematria") == "yes"
    ]
    if meaningful_rows:
        lines.extend(
            [
                "",
                "## Meaningful Skip Rows",
                "",
                "| Rank | Term | Center | Skip | Constant match | Term gematria match | Center-word gematria match | Source |",
                "| ---: | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in meaningful_rows[: args.markdown_row_limit]:
            lines.append(meaningful_skip_markdown_row(row))
        if len(meaningful_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(meaningful_rows) - args.markdown_row_limit:,} more meaningful-skip rows in CSV |"
            )
    bigram_rows = [row for row in rows if row.get("bigram_surprise_stratum")]
    if bigram_rows:
        lines.extend(
            [
                "",
                "## Bigram Surprise Rows",
                "",
                "| Rank | Term | Center | Stratum | Evidence | Min/max counts | Source |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in bigram_rows[: args.markdown_row_limit]:
            lines.append(bigram_markdown_row(row))
        if len(bigram_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(bigram_rows) - args.markdown_row_limit:,} more bigram rows in CSV |"
            )
    letter_rows = [row for row in rows if row.get("letter_frequency_stratum")]
    if letter_rows:
        lines.extend(
            [
                "",
                "## Letter Frequency Rows",
                "",
                "| Rank | Term | Center | Stratum | Evidence | Min/max counts | Source |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in letter_rows[: args.markdown_row_limit]:
            lines.append(letter_frequency_markdown_row(row))
        if len(letter_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(letter_rows) - args.markdown_row_limit:,} more letter-frequency rows in CSV |"
            )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `canonical_first_occurrence` means first centered occurrence within the current indexed family, not first hidden occurrence in every raw hit export.",
            "- Direction strata are computed per source family / queue / corpus set / term group.",
            "- Boundary strata are computed only from retained endpoint offsets, so blank boundary fields mean unavailable evidence, not proven absence.",
            "- Center-position strata use the center verse reference, not ELS path endpoints.",
            "- `cross_skip_pair_at_word` means at least one other normalized term shares the same center word/reference in the indexed family at a different skip.",
            "- `cross_skip_pair_at_letter` means two different terms at different skips share at least one retained letter-path position.",
            "- `cross_skip_pair_within_N_letters` means two different terms at different skips have endpoints within the configured letter distance.",
            "- `canonical_first_in_thematic_chapter`, `author_in_own_book`, and `protagonist_in_own_narrative` are locked-mapping annotations only; empty mapping files mean no rows are flagged.",
            "- Meaningful-skip and gematria-skip strata are metadata flags; they do not change the search space or promote claim status.",
            "- Bigram-surprise strata are corpus-local review aids, not claim promotion rules; missing adjacent surface bigrams count as rare.",
            "- Letter-frequency anomaly strata are corpus-local review aids; missing letters count as rare.",
            "- Matrix, cipher, broader cross-skip, and cohort-density strata widen the review surface and need separate locked controls before claim language.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def boundary_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(row.get('boundary_strata', ''))} | "
        f"{md_cell(row.get('boundary_evidence', ''))} | `{row.get('source_family', '')}` |"
    )


def center_position_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(row.get('center_position_strata', ''))} | "
        f"{md_cell(row.get('center_position_evidence', ''))} | `{row.get('source_family', '')}` |"
    )


def cross_skip_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    at_word = ""
    if row.get("cross_skip_pair_at_word") == "yes":
        at_word = f"{row.get('cross_skip_pair_count', '')}: {row.get('cross_skip_pair_terms', '')}"
    at_letter = ""
    if row.get("cross_skip_pair_at_letter") == "yes":
        at_letter = (
            f"{row.get('cross_skip_pair_at_letter_count', '')}: "
            f"{row.get('cross_skip_pair_at_letter_terms', '')}"
        )
    within = ""
    if row.get("cross_skip_pair_within_N_letters") == "yes":
        within = (
            f"{row.get('cross_skip_pair_within_letter_count', '')}: "
            f"{row.get('cross_skip_pair_within_letter_terms', '')}; "
            f"min={row.get('cross_skip_pair_within_letter_min_distance', '')}"
        )
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(at_word)} | {md_cell(at_letter)} | {md_cell(within)} | "
        f"`{row.get('source_family', '')}` |"
    )


def meaningful_skip_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    constant_match = ""
    if row.get("skip_equals_meaningful_constant") == "yes":
        constant_match = (
            f"{row.get('meaningful_constant_skips', '')}: "
            f"{row.get('meaningful_constant_labels', '')}"
        )
    gematria_match = ""
    if row.get("skip_equals_term_gematria") == "yes":
        gematria_match = (
            f"{row.get('term_gematria_matching_skips', '')} "
            f"({row.get('gematria_scheme', '')})"
        )
    center_gematria_match = ""
    if row.get("skip_equals_center_word_gematria") == "yes":
        center_gematria_match = (
            f"{row.get('center_word_gematria_matching_skips', '')} "
            f"({row.get('center_word_gematria_scheme', '')})"
        )
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(row.get('skip', ''))} | {md_cell(constant_match)} | "
        f"{md_cell(gematria_match)} | {md_cell(center_gematria_match)} | `{row.get('source_family', '')}` |"
    )


def mapping_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(row.get('thematic_chapter_evidence', ''))} | "
        f"{md_cell(row.get('author_in_own_book_evidence', ''))} | "
        f"{md_cell(row.get('protagonist_in_own_narrative_evidence', ''))} | "
        f"`{row.get('source_family', '')}` |"
    )


def bigram_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    counts = f"{row.get('bigram_min_count', '')}/{row.get('bigram_max_count', '')}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"`{row.get('bigram_surprise_stratum', '')}` | "
        f"{md_cell(row.get('bigram_surprise_evidence', ''))} | "
        f"{md_cell(counts)} | `{row.get('source_family', '')}` |"
    )


def letter_frequency_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    counts = f"{row.get('letter_frequency_min_count', '')}/{row.get('letter_frequency_max_count', '')}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"`{row.get('letter_frequency_stratum', '')}` | "
        f"{md_cell(row.get('letter_frequency_evidence', ''))} | "
        f"{md_cell(counts)} | `{row.get('source_family', '')}` |"
    )


def markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"`{row.get('occurrence_type', '')}` | `{row.get('direction_stratum', '')}` | "
        f"{md_cell(row.get('boundary_strata', ''))} | "
        f"{row.get('canonical_first_centered_occurrence', '')} | `{row.get('source_family', '')}` |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
    *,
    corpus_configs: dict[str, str],
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_match_strata_index.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "materialized_strata": [row["stratum"] for row in summary_rows],
        "cross_skip_letter_distance": args.cross_skip_letter_distance,
        "corpus_configs": corpus_configs,
        "inputs": {
            "occurrences": str(args.occurrences),
            "meaningful_constants": str(args.meaningful_constants),
            "thematic_chapters": str(args.thematic_chapters),
            "author_book_mapping": str(args.author_book_mapping),
            "protagonist_narrative_mapping": str(args.protagonist_narrative_mapping),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_meaningful_constants(path: Path) -> dict[int, str]:
    constants: dict[int, str] = {}
    if not path.exists():
        return constants
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                value = int(row["value"])
            except (KeyError, ValueError):
                continue
            constants[value] = row.get("label", str(value)).strip() or str(value)
    return constants


def read_mapping_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
            if any((value or "").strip() for value in row.values())
        ]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def corpus_config_map(overrides: list[str]) -> dict[str, str]:
    values = list(DEFAULT_CORPUS_CONFIGS)
    values.extend(overrides)
    output = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"invalid --corpus-config value: {value}")
        label, path = value.split("=", 1)
        output[label.strip()] = path.strip()
    return output


def load_corpus_metadata(
    configs: dict[str, str],
) -> tuple[dict[str, BoundaryIndex], dict[str, BigramProfile], dict[str, LetterFrequencyProfile]]:
    boundary_indexes = {}
    bigram_profiles = {}
    letter_frequency_profiles = {}
    for label, path in configs.items():
        try:
            corpus = load_corpus(path)
        except FileNotFoundError:
            continue
        boundary_indexes[label] = build_boundary_index(corpus)
        bigram_profiles[label] = BigramProfile.from_text(corpus.text)
        letter_frequency_profiles[label] = LetterFrequencyProfile.from_text(corpus.text)
    return boundary_indexes, bigram_profiles, letter_frequency_profiles


def boundary_annotations(
    row: dict[str, str],
    boundary_indexes: dict[str, BoundaryIndex],
) -> tuple[list[str], list[str], list[str]]:
    strata_by_corpus: dict[str, tuple[str, ...]] = {}
    for corpus, start, end in offset_records(row):
        index = boundary_indexes.get(corpus)
        if index is None:
            continue
        strata = boundary_strata_for_offsets(start_offset=start, end_offset=end, boundary_index=index)
        if strata:
            strata_by_corpus[corpus] = strata
    strata = sorted({value for values in strata_by_corpus.values() for value in values})
    corpora = sorted(strata_by_corpus)
    evidence = [f"{corpus}:{','.join(strata_by_corpus[corpus])}" for corpus in corpora]
    return strata, corpora, evidence


def center_position_annotations(
    row: dict[str, str],
    boundary_indexes: dict[str, BoundaryIndex],
) -> tuple[list[str], list[str], list[str]]:
    strata_by_corpus: dict[str, tuple[str, ...]] = {}
    for corpus in candidate_corpora(row):
        index = boundary_indexes.get(corpus)
        if index is None:
            continue
        strata = center_position_strata_for_ref(row.get("center_ref", ""), boundary_index=index)
        if strata:
            strata_by_corpus[corpus] = strata
    strata = sorted({value for values in strata_by_corpus.values() for value in values})
    corpora = sorted(strata_by_corpus)
    evidence = [f"{corpus}:{','.join(strata_by_corpus[corpus])}" for corpus in corpora]
    return strata, corpora, evidence


def candidate_corpora(row: dict[str, str]) -> list[str]:
    values = [row.get("corpus", "")]
    values.extend(re.split(r"[;,| ]+", row.get("present_corpora", "")))
    return sorted({value for value in values if value})


def offset_records(row: dict[str, str]) -> list[tuple[str, int, int]]:
    records = parse_offset_triplets(row.get("offset_triplets", ""))
    if records:
        return records
    letter_path = row.get("letter_path", "")
    if not letter_path:
        return []
    positions = []
    for part in letter_path.split(";"):
        match = LETTER_PATH_RE.match(part.strip())
        if match:
            positions.append(int(match.group("position")))
    corpus = row.get("corpus", "")
    if not corpus or not positions:
        return []
    return [(corpus, positions[0], positions[-1])]


def parse_offset_triplets(value: str) -> list[tuple[str, int, int]]:
    records = []
    for part in str(value or "").split(";"):
        if ":" not in part or "/" not in part:
            continue
        corpus, offsets = part.split(":", 1)
        pieces = offsets.split("/")
        if len(pieces) != 3:
            continue
        try:
            records.append((corpus.strip(), int(pieces[0]), int(pieces[2])))
        except ValueError:
            continue
    return records


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_match_strata_index "
        f"--occurrences {args.occurrences} "
        f"--meaningful-constants {args.meaningful_constants} "
        f"--thematic-chapters {args.thematic_chapters} "
        f"--author-book-mapping {args.author_book_mapping} "
        f"--protagonist-narrative-mapping {args.protagonist_narrative_mapping} "
        f"--out {args.out} "
        f"--summary-out {args.summary_out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out} "
        f"--cross-skip-letter-distance {args.cross_skip_letter_distance}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
