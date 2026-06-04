#!/usr/bin/env python3
"""Check TR omission-broken hits against BYZ/Majority and TCG NT corpora."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import Corpus, load_corpus
from els.critical import verse_span_preserved
from scripts.analyze_critical_omission_breaks import TR_CONFIG


DEFAULT_EXAMPLES = Path("reports/critical_omission_breaks_examples.csv")
BYZ_CONFIG = Path("configs/example_ebible_grcmt.toml")
TCG_CONFIG = Path("configs/example_ebible_grctcgnt.toml")
DEFAULT_OUT = Path("reports/critical_omission_breaks_cross_tradition.csv")
DEFAULT_MANIFEST = Path("reports/critical_omission_breaks_cross_tradition.manifest.json")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--examples", type=Path, default=DEFAULT_EXAMPLES)
    parser.add_argument("--tr-config", type=Path, default=TR_CONFIG)
    parser.add_argument("--byz-config", type=Path, default=BYZ_CONFIG)
    parser.add_argument("--tcg-config", type=Path, default=TCG_CONFIG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--window-verses",
        type=int,
        default=2,
        help="Verse window for the proximity preservation test (Stage 1).",
    )
    args = parser.parse_args()

    tr = load_corpus(args.tr_config)
    byz = load_corpus(args.byz_config)
    tcg = load_corpus(args.tcg_config)
    tr_by_ref = {verse.ref: verse for verse in tr.verses}
    byz_by_ref = {verse.ref: verse for verse in byz.verses}
    tcg_by_ref = {verse.ref: verse for verse in tcg.verses}
    byz_ref_to_index = {verse.ref: index for index, verse in enumerate(byz.verses)}
    tcg_ref_to_index = {verse.ref: index for index, verse in enumerate(tcg.verses)}

    rows = []
    with args.examples.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            byz_status = equivalent_status(row, tr, tr_by_ref, byz, byz_by_ref)
            tcg_status = equivalent_status(row, tr, tr_by_ref, tcg, tcg_by_ref)
            byz_prox = proximity_status(row, tr_by_ref, byz, byz_ref_to_index, args.window_verses)
            tcg_prox = proximity_status(row, tr_by_ref, tcg, tcg_ref_to_index, args.window_verses)
            out = dict(row)
            out["tr_hits"] = 1
            out["sbl_status"] = row.get("break_type", "")
            out["byz_status"] = byz_status
            out["tcg_status"] = tcg_status
            out["cross_tradition_class"] = classify_cross(byz_status, tcg_status)
            out["window_verses"] = args.window_verses
            out["byz_proximity_status"] = byz_prox
            out["tcg_proximity_status"] = tcg_prox
            out["cross_tradition_class_proximity"] = classify_cross_proximity(byz_prox, tcg_prox)
            rows.append(out)

    write_rows(args.out, rows)
    args.manifest_out.write_text(
        json.dumps(
            {
                "tool": "critical_omission_breaks_cross_tradition",
                "created_utc": datetime.now(UTC).isoformat(),
                "examples": str(args.examples.resolve()),
                "tr_config": str(args.tr_config.resolve()),
                "byz_config": str(args.byz_config.resolve()),
                "tcg_config": str(args.tcg_config.resolve()),
                "window_verses": args.window_verses,
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


def equivalent_status(row, tr: Corpus, tr_by_ref, other: Corpus, other_by_ref) -> str:
    start_ref = row["start_ref"]
    end_ref = row["end_ref"]
    if start_ref not in tr_by_ref or end_ref not in tr_by_ref:
        return "tr_ref_missing"
    if start_ref not in other_by_ref or end_ref not in other_by_ref:
        return "ref_missing"
    start_local = int(row["start_offset"]) - tr_by_ref[start_ref].norm_start
    end_local = int(row["end_offset"]) - tr_by_ref[end_ref].norm_start
    start = other_by_ref[start_ref].norm_start + start_local
    end = other_by_ref[end_ref].norm_start + end_local
    skip = int(row["skip"])
    query = row["normalized_term"]
    positions = [start + index * skip for index in range(len(query))]
    if positions[-1] != end:
        return "coordinate_mismatch"
    if any(position < 0 or position >= len(other.text) for position in positions):
        return "offset_out_of_range"
    observed = "".join(other.text[position] for position in positions)
    return "preserved_equivalent_offsets" if observed == query else "not_preserved_equivalent_offsets"


def classify_cross(byz_status: str, tcg_status: str) -> str:
    byz = byz_status == "preserved_equivalent_offsets"
    tcg = tcg_status == "preserved_equivalent_offsets"
    if byz and tcg:
        return "preserved_by_byz_and_tcg"
    if byz:
        return "preserved_by_byz"
    if tcg:
        return "preserved_by_tcg"
    return "tr_specific_under_equivalent_offsets"


def proximity_status(row, tr_by_ref, other: Corpus, other_ref_to_index, window: int) -> str:
    """Stage-1 preservation: same query+skip within +/-window verses of the
    hit's span, tolerating upstream word-length deltas the strict test rejects."""
    start_ref = row["start_ref"]
    end_ref = row["end_ref"]
    if start_ref not in tr_by_ref or end_ref not in tr_by_ref:
        return "tr_ref_missing"
    if start_ref not in other_ref_to_index or end_ref not in other_ref_to_index:
        return "ref_missing"
    preserved = verse_span_preserved(
        other,
        other_ref_to_index,
        start_ref,
        end_ref,
        row["normalized_term"],
        int(row["skip"]),
        window_verses=window,
    )
    return "preserved_within_verse_span" if preserved else "not_preserved_within_window"


def classify_cross_proximity(byz_status: str, tcg_status: str) -> str:
    byz = byz_status == "preserved_within_verse_span"
    tcg = tcg_status == "preserved_within_verse_span"
    if byz and tcg:
        return "preserved_by_byz_and_tcg"
    if byz:
        return "preserved_by_byz"
    if tcg:
        return "preserved_by_tcg"
    return "tr_specific_within_window"


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
