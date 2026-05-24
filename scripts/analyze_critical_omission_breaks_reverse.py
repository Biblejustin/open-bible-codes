#!/usr/bin/env python3
"""Reverse omission check using TR-only verses spliced into SBLGNT."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus, splice_verses_into_corpus
from els.critical import OmittedBlock, classify_missing_verses, count_breaks_for_blocks
from scripts.analyze_critical_omission_breaks import (
    CRITICAL_CONFIG,
    MAX_SKIP,
    MIN_SKIP,
    TERM_PATHS,
    TR_CONFIG,
    build_stats_by_query,
    read_greek_terms,
    summary_row,
)


SUMMARY_OUT = Path("reports/critical_omission_breaks_reverse_summary.csv")
EXAMPLES_OUT = Path("reports/critical_omission_breaks_reverse_examples.csv")
BY_VERSE_OUT = Path("reports/critical_omission_breaks_reverse_by_verse.csv")
MANIFEST_OUT = Path("reports/critical_omission_breaks_reverse.manifest.json")


def main() -> int:
    tr = load_corpus(TR_CONFIG)
    critical = load_corpus(CRITICAL_CONFIG)
    actual = [block for block in classify_missing_verses(tr, critical) if block.used_as_deletion]
    donor_refs = [block.ref for block in actual]
    augmented = splice_verses_into_corpus(critical, tr, donor_refs)
    inserted_blocks = [
        OmittedBlock(
            ref=verse.ref,
            start=verse.norm_start,
            end=verse.norm_end,
            length=verse.norm_length,
            status="spliced_tr_only_block",
            used_as_deletion=True,
        )
        for verse in augmented.verses
        if verse.ref in set(donor_refs)
    ]
    terms = read_greek_terms(TERM_PATHS, augmented)
    term_stats, stats_by_query = build_stats_by_query(augmented, [dict(row) for row in terms])
    _total, per_block, broken = count_breaks_for_blocks(
        augmented,
        stats_by_query,
        inserted_blocks,
        min_skip=MIN_SKIP,
        max_skip=MAX_SKIP,
        direction="both",
    )
    summary_rows = [
        summary_row(
            stats.term_row,
            stats.normalized,
            stats.total_hits,
            stats.span_intersect_hits,
            stats.broken_removed_letter_hits,
            stats.broken_spacing_hits,
            stats.preserved_across_omission_hits,
            stats.status,
        )
        for stats in term_stats
    ]
    example_rows = [record.as_row() for record in broken]
    by_verse_rows = [
        {
            "omitted_ref": block.ref,
            "norm_start": block.start,
            "norm_end": block.end,
            "norm_length": block.length,
            "broken_total_hits": per_block[index],
        }
        for index, block in enumerate(inserted_blocks)
    ]
    write_rows(SUMMARY_OUT, summary_rows)
    write_rows(EXAMPLES_OUT, example_rows)
    write_rows(BY_VERSE_OUT, by_verse_rows)
    MANIFEST_OUT.write_text(
        json.dumps(
            {
                "tool": "critical_omission_breaks_reverse",
                "created_utc": datetime.now(UTC).isoformat(),
                "tr_config": str(TR_CONFIG.resolve()),
                "critical_config": str(CRITICAL_CONFIG.resolve()),
                "term_paths": [str(path.resolve()) for path in TERM_PATHS],
                "spliced_refs": donor_refs,
                "spliced_blocks": len(inserted_blocks),
                "broken_example_rows": len(example_rows),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(SUMMARY_OUT)
    print(EXAMPLES_OUT)
    print(BY_VERSE_OUT)
    print(MANIFEST_OUT)
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
