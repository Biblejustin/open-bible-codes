"""`pairs` subcommand: nearest ELS term pairs within a gap, plus its hit helpers."""

from __future__ import annotations

import argparse
from bisect import bisect_left
from datetime import UTC, datetime
from heapq import nsmallest
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.io import open_dict_writer, write_dict_rows, write_run_manifest
from els.maxskip import effective_max_skip_for_query
from els.pairing import cylindrical_hit_distance, hit_center, pair_metrics
from els.rows import PAIR_FIELDNAMES
from els.search import ELSHit, find_els, normalize_for_corpus
from els.term_io import accepted_term_languages, parse_corpus_args, read_term_rows


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
