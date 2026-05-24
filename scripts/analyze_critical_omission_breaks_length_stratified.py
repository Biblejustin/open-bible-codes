#!/usr/bin/env python3
"""Normalize critical-omission breaks by total TR hits per term."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus
from els.critical import classify_missing_verses, count_breaks_for_blocks
from scripts.analyze_critical_omission_breaks import (
    CRITICAL_CONFIG,
    MAX_SKIP,
    MIN_SKIP,
    TERM_PATHS,
    TR_CONFIG,
    build_stats_by_query,
    read_greek_terms,
)


DEFAULT_SUMMARY = Path("reports/critical_omission_breaks_summary.csv")
DEFAULT_OUT = Path("reports/critical_omission_breaks_length_stratified.csv")
DEFAULT_MANIFEST = Path("reports/critical_omission_breaks_length_stratified.manifest.json")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    tr = load_corpus(TR_CONFIG)
    critical = load_corpus(CRITICAL_CONFIG)
    deleted_blocks = [block for block in classify_missing_verses(tr, critical) if block.used_as_deletion]
    terms = read_greek_terms(TERM_PATHS, tr)
    term_stats, stats_by_query = build_stats_by_query(tr, [dict(row) for row in terms])
    count_breaks_for_blocks(
        tr,
        stats_by_query,
        [],
        min_skip=MIN_SKIP,
        max_skip=MAX_SKIP,
        direction="both",
    )
    hits_by_key = {
        (stats.term_row.get("term_source", ""), stats.term_row.get("term_id", "")): stats.total_hits
        for stats in term_stats
    }
    deleted_letters = sum(block.length for block in deleted_blocks)
    rows = []
    with args.summary.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row.get("term_source", ""), row.get("term_id", ""))
            total_hits = hits_by_key.get(key, int(row.get("tr_hits", "0") or 0))
            broken_hits = int(row.get("broken_total_hits", "0") or 0)
            normalized_length = int(row.get("normalized_length", "0") or 0)
            break_rate = broken_hits / total_hits if total_hits else 0
            naive_expected = normalized_length * deleted_letters / len(tr.text) if tr.text else 0
            ratio = break_rate / naive_expected if naive_expected else ""
            rows.append(
                {
                    "term_id": row.get("term_id", ""),
                    "term": row.get("term", ""),
                    "normalized_term": row.get("normalized_term", ""),
                    "normalized_length": normalized_length,
                    "total_tr_hits": total_hits,
                    "broken_hits": broken_hits,
                    "break_rate": break_rate,
                    "naive_expected_break_rate": naive_expected,
                    "ratio": ratio,
                }
            )
    write_rows(args.out, rows)
    args.manifest_out.write_text(
        json.dumps(
            {
                "tool": "critical_omission_breaks_length_stratified",
                "created_utc": datetime.now(UTC).isoformat(),
                "summary": str(args.summary.resolve()),
                "out": str(args.out.resolve()),
                "deleted_letters": deleted_letters,
                "tr_letters": len(tr.text),
                "rows": len(rows),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(args.out)
    print(args.manifest_out)
    return 0


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
