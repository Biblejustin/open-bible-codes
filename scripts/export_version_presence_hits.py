#!/usr/bin/env python3
"""Export exact version-presence pattern rows as ordinary ELS hit rows."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.cli import FIELDNAMES
from els.corpus import load_corpus
from els.search import build_hit
from scripts.analyze_hebrew_hit_version_presence import split_labeled_path


DEFAULT_SCOPES = ["present_all_observed_sources"]
EXTRA_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "category",
    "presence_scope",
    "present_corpora",
    "absent_corpora",
    "pattern_hit_count",
]
OUTPUT_FIELDNAMES = [*EXTRA_FIELDNAMES, *FIELDNAMES]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    scopes = set(args.presence_scope or DEFAULT_SCOPES)
    corpora = {label: load_corpus(path) for label, path in labeled_paths(args.corpus)}
    rows = export_rows(
        args.patterns,
        corpora,
        scopes,
        set(args.term_id or []),
        set(args.concept or []),
        set(args.category or []),
        args.max_patterns_per_term,
        args.max_patterns,
    )
    write_rows(args.out, rows)
    if args.manifest_out:
        write_manifest(args, rows, corpora, started)
    print(args.out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", type=Path, required=True)
    parser.add_argument("--corpus", action="append", required=True)
    parser.add_argument("--presence-scope", action="append", default=None)
    parser.add_argument("--term-id", action="append", default=None)
    parser.add_argument("--concept", action="append", default=None)
    parser.add_argument("--category", action="append", default=None)
    parser.add_argument("--max-patterns-per-term", type=int)
    parser.add_argument("--max-patterns", type=int)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path)
    return parser


def labeled_paths(values: list[str]) -> list[tuple[str, Path]]:
    return [split_labeled_path(value) for value in values]


def export_rows(
    path: Path,
    corpora,
    scopes: set[str],
    term_ids: set[str],
    concepts: set[str],
    categories: set[str],
    max_patterns_per_term: int | None,
    max_patterns: int | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    selected_patterns = 0
    patterns_by_term: dict[str, int] = defaultdict(int)
    with path.open("r", encoding="utf-8", newline="") as handle:
        for pattern in csv.DictReader(handle):
            if not pattern_selected(pattern, scopes, term_ids, concepts, categories):
                continue
            term_id = pattern["term_id"]
            if max_patterns_per_term is not None and patterns_by_term[term_id] >= max_patterns_per_term:
                continue
            if max_patterns is not None and selected_patterns >= max_patterns:
                break
            emitted = rows_for_pattern(pattern, corpora)
            if not emitted:
                continue
            rows.extend(emitted)
            patterns_by_term[term_id] += 1
            selected_patterns += 1
    return rows


def pattern_selected(
    pattern: dict[str, str],
    scopes: set[str],
    term_ids: set[str],
    concepts: set[str],
    categories: set[str],
) -> bool:
    return (
        pattern["presence_scope"] in scopes
        and (not term_ids or pattern["term_id"] in term_ids)
        and (not concepts or pattern["concept"] in concepts)
        and (not categories or pattern["category"] in categories)
    )


def rows_for_pattern(pattern: dict[str, str], corpora) -> list[dict[str, object]]:
    offsets = parse_offsets_by_corpus(pattern.get("offsets_by_corpus", ""))
    rows: list[dict[str, object]] = []
    for label in pattern.get("present_corpora", "").split(","):
        label = label.strip()
        if not label or label not in corpora or label not in offsets:
            continue
        start, end = offsets[label]
        hit = build_hit(
            corpora[label],
            pattern["term"],
            pattern["normalized_term"],
            int(pattern["skip"]),
            start,
            end,
        )
        row = {
            "corpus": label,
            "term_id": pattern["term_id"],
            "concept": pattern["concept"],
            "category": pattern["category"],
            "presence_scope": pattern["presence_scope"],
            "present_corpora": pattern["present_corpora"],
            "absent_corpora": pattern["absent_corpora"],
            "pattern_hit_count": pattern["hit_count"],
        }
        row.update(hit.as_row())
        rows.append(row)
    return rows


def parse_offsets_by_corpus(value: str) -> dict[str, tuple[int, int]]:
    offsets: dict[str, tuple[int, int]] = {}
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        label, span = part.split(":", 1)
        start, end = span.split("-", 1)
        offsets[label.strip()] = (int(start), int(end))
    return offsets


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(args, rows: list[dict[str, object]], corpora, started: float) -> None:
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "patterns": str(args.patterns),
        "presence_scope": args.presence_scope or DEFAULT_SCOPES,
        "term_ids": args.term_id,
        "concepts": args.concept,
        "categories": args.category,
        "max_patterns_per_term": args.max_patterns_per_term,
        "max_patterns": args.max_patterns,
        "row_count": len(rows),
        "corpora": {
            label: {"name": corpus.name, "verses": len(corpus.verses), "letters": len(corpus.text)}
            for label, corpus in corpora.items()
        },
        "outputs": {"hits": str(args.out)},
    }
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
