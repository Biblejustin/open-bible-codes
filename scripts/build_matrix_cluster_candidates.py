#!/usr/bin/env python3
"""Extract matrix-neighborhood candidate pairs from existing ELS hit CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import defaultdict
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.matrix import MatrixCell, cell_relation, closest_cell_pair, matrix_cell, validate_row_width


DEFAULT_OUT = Path("reports/matrix_clusters/candidates.csv")
DEFAULT_SUMMARY_OUT = Path("reports/matrix_clusters/summary.csv")
DEFAULT_MANIFEST_OUT = Path("reports/matrix_clusters/manifest.json")

FIELDNAMES = [
    "row_width",
    "max_cell_distance",
    "cell_distance",
    "cell_relation",
    "left_cell",
    "right_cell",
    "corpus_label",
    "left_hit_index",
    "right_hit_index",
    "left_term_id",
    "right_term_id",
    "left_concept",
    "right_concept",
    "left_normalized_term",
    "right_normalized_term",
    "left_skip",
    "right_skip",
    "left_direction",
    "right_direction",
    "left_center_ref",
    "right_center_ref",
    "left_center_word",
    "right_center_word",
]

SUMMARY_FIELDS = ["bucket", "value", "pairs"]


@dataclass(frozen=True)
class MatrixHit:
    hit_index: int
    corpus_label: str
    term_id: str
    concept: str
    normalized_term: str
    skip: int
    direction: str
    center_ref: str
    center_word: str
    cells: tuple[MatrixCell, ...]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    hits = read_hits(args.hits, row_width=args.row_width, max_rows=args.max_input_rows)
    rows = matrix_cluster_rows(
        hits,
        row_width=args.row_width,
        max_cell_distance=args.max_cell_distance,
        max_pairs=args.max_pairs,
        allow_same_term=args.allow_same_term,
    )
    summary_rows = summarize_rows(rows)
    write_rows(args.out, rows)
    write_rows(args.summary_out, summary_rows, fieldnames=SUMMARY_FIELDS)
    write_manifest(args.manifest_out, args, input_hits=hits, rows=rows, summary_rows=summary_rows, started=started)
    print(args.out)
    print(args.summary_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hits", action="append", type=Path, required=True)
    parser.add_argument("--row-width", type=int, required=True)
    parser.add_argument("--max-cell-distance", type=int, default=1)
    parser.add_argument("--max-pairs", type=int, default=100_000)
    parser.add_argument("--max-input-rows", type=int, default=0)
    parser.add_argument("--allow-same-term", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    return parser


def read_hits(paths: list[Path], *, row_width: int, max_rows: int = 0) -> list[MatrixHit]:
    validate_row_width(row_width)
    hits: list[MatrixHit] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                hit = matrix_hit_from_row(row, hit_index=len(hits) + 1, row_width=row_width)
                if hit is not None:
                    hits.append(hit)
                if max_rows > 0 and len(hits) >= max_rows:
                    return hits
    return hits


def matrix_hit_from_row(
    row: dict[str, str],
    *,
    hit_index: int,
    row_width: int,
) -> MatrixHit | None:
    sequence = row.get("sequence", "")
    if not sequence:
        return None
    try:
        start_offset = int(row.get("start_offset", ""))
        skip = int(row.get("skip", ""))
    except ValueError:
        return None
    offsets = tuple(start_offset + index * skip for index in range(len(sequence)))
    if any(offset < 0 for offset in offsets):
        return None
    return MatrixHit(
        hit_index=hit_index,
        corpus_label=corpus_label(row),
        term_id=row.get("term_id", "") or row.get("term", ""),
        concept=row.get("concept", ""),
        normalized_term=row.get("normalized_term", ""),
        skip=skip,
        direction=row.get("direction", "") or ("forward" if skip > 0 else "backward"),
        center_ref=row.get("center_ref", ""),
        center_word=row.get("center_word", ""),
        cells=tuple(matrix_cell(offset, row_width) for offset in offsets),
    )


def corpus_label(row: dict[str, str]) -> str:
    for key in ("corpus_label", "corpus", "base_corpus"):
        value = row.get(key, "").strip()
        if value:
            return value
    return ""


def matrix_cluster_rows(
    hits: list[MatrixHit],
    *,
    row_width: int,
    max_cell_distance: int = 1,
    max_pairs: int = 100_000,
    allow_same_term: bool = False,
) -> list[dict[str, object]]:
    if max_cell_distance < 0:
        raise ValueError("max_cell_distance must be >= 0")
    if max_pairs < 1:
        raise ValueError("max_pairs must be >= 1")

    rows: list[dict[str, object]] = []
    by_hit_index = {hit.hit_index: hit for hit in hits}
    cell_index: dict[tuple[str, MatrixCell], list[int]] = defaultdict(list)
    emitted: set[tuple[int, int]] = set()

    for hit in hits:
        candidate_ids = nearby_prior_hit_ids(hit, cell_index, max_cell_distance=max_cell_distance)
        for candidate_id in sorted(candidate_ids):
            prior = by_hit_index[candidate_id]
            if not allow_same_term and prior.term_id == hit.term_id:
                continue
            pair_key = (prior.hit_index, hit.hit_index)
            if pair_key in emitted:
                continue
            distance, left_cell, right_cell = closest_cell_pair(prior.cells, hit.cells)
            if distance <= max_cell_distance:
                rows.append(
                    matrix_cluster_row(
                        prior,
                        hit,
                        row_width=row_width,
                        max_cell_distance=max_cell_distance,
                        cell_distance=distance,
                        left_cell=left_cell,
                        right_cell=right_cell,
                    )
                )
                emitted.add(pair_key)
                if len(rows) >= max_pairs:
                    return rows
        for cell in set(hit.cells):
            cell_index[(hit.corpus_label, cell)].append(hit.hit_index)
    return rows


def nearby_prior_hit_ids(
    hit: MatrixHit,
    cell_index: dict[tuple[str, MatrixCell], list[int]],
    *,
    max_cell_distance: int,
) -> set[int]:
    candidates: set[int] = set()
    for row, col in set(hit.cells):
        for neighbor_row in range(row - max_cell_distance, row + max_cell_distance + 1):
            for neighbor_col in range(col - max_cell_distance, col + max_cell_distance + 1):
                if neighbor_row < 0 or neighbor_col < 0:
                    continue
                candidates.update(cell_index.get((hit.corpus_label, (neighbor_row, neighbor_col)), ()))
    return candidates


def matrix_cluster_row(
    left: MatrixHit,
    right: MatrixHit,
    *,
    row_width: int,
    max_cell_distance: int,
    cell_distance: int,
    left_cell: MatrixCell,
    right_cell: MatrixCell,
) -> dict[str, object]:
    return {
        "row_width": row_width,
        "max_cell_distance": max_cell_distance,
        "cell_distance": cell_distance,
        "cell_relation": cell_relation(left_cell, right_cell),
        "left_cell": format_cell(left_cell),
        "right_cell": format_cell(right_cell),
        "corpus_label": left.corpus_label,
        "left_hit_index": left.hit_index,
        "right_hit_index": right.hit_index,
        "left_term_id": left.term_id,
        "right_term_id": right.term_id,
        "left_concept": left.concept,
        "right_concept": right.concept,
        "left_normalized_term": left.normalized_term,
        "right_normalized_term": right.normalized_term,
        "left_skip": left.skip,
        "right_skip": right.skip,
        "left_direction": left.direction,
        "right_direction": right.direction,
        "left_center_ref": left.center_ref,
        "right_center_ref": right.center_ref,
        "left_center_word": left.center_word,
        "right_center_word": right.center_word,
    }


def format_cell(cell: MatrixCell) -> str:
    return f"{cell[0]}:{cell[1]}"


def summarize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    relation_counts = Counter(str(row.get("cell_relation", "")) for row in rows)
    corpus_counts = Counter(str(row.get("corpus_label", "")) for row in rows)
    distance_counts = Counter(str(row.get("cell_distance", "")) for row in rows)
    summary_rows: list[dict[str, object]] = []
    for bucket, counts in (
        ("cell_relation", relation_counts),
        ("corpus_label", corpus_counts),
        ("cell_distance", distance_counts),
    ):
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            summary_rows.append({"bucket": bucket, "value": value, "pairs": count})
    return summary_rows


def write_rows(path: Path, rows: list[dict[str, object]], *, fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    *,
    input_hits: list[MatrixHit],
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_matrix_cluster_candidates.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "row_width": args.row_width,
        "max_cell_distance": args.max_cell_distance,
        "max_pairs": args.max_pairs,
        "max_input_rows": args.max_input_rows,
        "allow_same_term": args.allow_same_term,
        "input_hit_rows": len(input_hits),
        "candidate_pairs": len(rows),
        "summary_rows": len(summary_rows),
        "inputs": {"hits": [str(path) for path in args.hits]},
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
