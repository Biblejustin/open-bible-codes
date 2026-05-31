#!/usr/bin/env python3
"""Build a Project Gutenberg KJVA source-lock decision packet from count-only evidence."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import OrderedDict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from scripts.analyze_kjva_gutenberg_source_lock_prep import APOCRYPHA_CODES


DEFAULT_PREP_ROWS = Path("reports/kjva_gutenberg_source_lock_prep/book_shape.csv")
DEFAULT_PREP_SUMMARY = Path("reports/kjva_gutenberg_source_lock_prep/summary.csv")
DEFAULT_KJVA_CSV = Path("data/processed/ebible/eng-kjv.csv")
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_source_lock_decision_packet")
DEFAULT_DECISIONS = DEFAULT_OUT_DIR / "decisions.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_SOURCE_LOCK_DECISION_PACKET.md")

SOURCE_APOCRYPHA_ORDER = (
    "1ES",
    "2ES",
    "TOB",
    "JDT",
    "ESG",
    "WIS",
    "SIR",
    "BAR",
    "LJE_SOURCE",
    "S3Y",
    "SUS",
    "BEL",
    "MAN",
    "1MA",
    "2MA",
)

DECISION_FIELDNAMES = [
    "decision_id",
    "area",
    "current_evidence",
    "recommendation",
    "lock_status",
    "blocker",
    "next_action",
    "result_boundary",
]
SUMMARY_FIELDNAMES = [
    "decision_rows",
    "policy_ready_rows",
    "recommended_policy_rows",
    "blocked_rows",
    "candidate_not_locked_rows",
    "local_apocrypha_order",
    "gutenberg_apocrypha_order",
    "order_recommendation",
    "baruch_epistle_recommendation",
    "sirach_blocker",
    "prayer_blocker",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    prep_rows = read_csv_dicts(args.prep_rows)
    prep_summary = read_single_csv_row(args.prep_summary)
    local_order = local_apocrypha_order(args.kjva_csv)
    decisions = build_decisions(prep_rows, prep_summary, local_order)
    summary = build_summary(decisions, local_order)
    write_csv(args.out, DECISION_FIELDNAMES, decisions)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, decisions, prep_summary)
    write_manifest(args.manifest_out, args, decisions, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prep-rows", type=Path, default=DEFAULT_PREP_ROWS)
    parser.add_argument("--prep-summary", type=Path, default=DEFAULT_PREP_SUMMARY)
    parser.add_argument("--kjva-csv", type=Path, default=DEFAULT_KJVA_CSV)
    parser.add_argument("--out", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_decisions(
    prep_rows: list[dict[str, str]],
    prep_summary: dict[str, str],
    local_order: list[str],
) -> list[dict[str, str]]:
    rows_by_book = {row["book"]: row for row in prep_rows}
    sirach = rows_by_book.get("SIR", {})
    manasseh = rows_by_book.get("MAN", {})
    baruch = rows_by_book.get("BAR", {})
    lje = rows_by_book.get("LJE_SOURCE", {})
    return [
        decision(
            "source_stream",
            "source stream",
            "Project Gutenberg eBook 30 plus eBook 124 has public-domain-USA metadata and count-only source-shape evidence.",
            "Use Project Gutenberg eBook 30 plus eBook 124 as the next independent KJVA candidate stream, after the remaining verse-map blockers are closed.",
            "candidate_not_locked",
            "No study-lock sidecar, verse map, collation, or source-use lock exists yet.",
            "Keep this as candidate evidence until the Sirach and Prayer of Manasseh blockers are resolved.",
        ),
        decision(
            "raw_text_retention",
            "text retention",
            f"Prep summary records raw_text_retained={prep_summary.get('raw_text_retained', '')}.",
            "Keep raw Gutenberg text in ignored local cache or scan in memory only; commit checksums and counts, not Bible text.",
            "policy_ready",
            "",
            "Continue committing only derived non-text evidence.",
        ),
        decision(
            "kjv_component",
            "KJV component",
            f"{prep_summary.get('kjv_books_exact_count_matches', '')} of {prep_summary.get('kjv_books_compared', '')} KJV books match local KJVA verse counts exactly.",
            "Treat the KJV component as count-ready for later collation, but not imported.",
            "recommended_policy_not_locked",
            "Count agreement is not text collation.",
            "Build verse-map/collation proof before any source lock.",
        ),
        decision(
            "apocrypha_component",
            "Apocrypha/deuterocanon component",
            f"{prep_summary.get('apocrypha_books_exact_count_matches', '')} of {prep_summary.get('apocrypha_books_compared', '')} tracked books match after Baruch/Epistle rollup.",
            "Keep eBook 124 as the likely Apocrypha/deuterocanon source component, but block source lock until the two count drifts are resolved.",
            "blocked",
            "Sirach and Prayer of Manasseh do not have exact verse-marker agreement.",
            "Resolve Sirach and Prayer of Manasseh before source-lock sidecar.",
        ),
        decision(
            "book_order",
            "book order",
            f"Local KJVA Apocrypha order is {', '.join(local_order)}; Gutenberg source order is {', '.join(SOURCE_APOCRYPHA_ORDER)}.",
            "Use Gutenberg source order for an independent Project Gutenberg replication stream, and document that this differs from current local KJVA order.",
            "recommended_policy_not_locked",
            "Book order affects ELS paths and must be preregistered before results.",
            "Put source-order choice into a future study-lock sidecar.",
        ),
        decision(
            "baruch_epistle",
            "Baruch/Epistle of Jeremiah",
            f"Baruch source markers {baruch.get('gutenberg_marker_count', '')}; Epistle source markers {lje.get('gutenberg_marker_count', '')}; combined local BAR count {baruch.get('local_kjva_verse_count', '')}.",
            "Roll the separate Epistle of Jeremiah source section into BAR for KJVA book-code compatibility while preserving source-component metadata.",
            "recommended_policy_not_locked",
            "Rollup policy must be named before a result-bearing run.",
            "Add BAR/LJE rollup rule to source-lock sidecar.",
        ),
        decision(
            "sirach_count_drift",
            "Sirach count drift",
            f"Sirach source markers {sirach.get('gutenberg_marker_count', '')}; local KJVA count {sirach.get('local_kjva_verse_count', '')}; delta {sirach.get('delta', '')}.",
            "Do not patch or infer the missing Sirach marker automatically.",
            "blocked",
            "One-verse marker drift needs citable collation.",
            "Locate the exact Sirach marker gap and record a non-text collation row.",
        ),
        decision(
            "prayer_count_drift",
            "Prayer of Manasseh count drift",
            f"Prayer of Manasseh source markers {manasseh.get('gutenberg_marker_count', '')}; local KJVA count {manasseh.get('local_kjva_verse_count', '')}; delta {manasseh.get('delta', '')}.",
            "Do not split the unmarked prose automatically.",
            "blocked",
            "eBook 124 body text has no verse markers for Prayer of Manasseh.",
            "Choose a citable verse-boundary policy or leave Prayer of Manasseh out of any source-locked stream.",
        ),
        decision(
            "checksum_record",
            "checksums",
            "Prep manifest and summary record raw-byte SHA-256 checksums for both source files.",
            "Use those checksums as candidate source identifiers once the source stream is formally selected.",
            "policy_ready",
            "",
            "Copy checksum fields into a future source-lock sidecar after blockers close.",
        ),
        decision(
            "result_boundary",
            "result boundary",
            "No term lock, control lock, source-lock sidecar, or collation sidecar exists for a Gutenberg KJVA replication run.",
            "Do not run result-bearing KJVA bridge replication from Gutenberg yet.",
            "blocked",
            "Source-lock prerequisites remain open.",
            "Finish source decisions, then build a fresh study-lock package before results.",
        ),
    ]


def build_summary(
    decisions: list[dict[str, str]],
    local_order: list[str],
) -> dict[str, Any]:
    return {
        "decision_rows": len(decisions),
        "policy_ready_rows": count_status(decisions, "policy_ready"),
        "recommended_policy_rows": count_status(decisions, "recommended_policy_not_locked"),
        "blocked_rows": count_status(decisions, "blocked"),
        "candidate_not_locked_rows": count_status(decisions, "candidate_not_locked"),
        "local_apocrypha_order": ";".join(local_order),
        "gutenberg_apocrypha_order": ";".join(SOURCE_APOCRYPHA_ORDER),
        "order_recommendation": "use_gutenberg_source_order_for_independent_replication",
        "baruch_epistle_recommendation": "roll_lje_source_into_bar_with_component_metadata",
        "sirach_blocker": "one_source_marker_short_needs_collation",
        "prayer_blocker": "unmarked_prose_needs_verse_boundary_policy",
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "decision_packet_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    decisions: list[dict[str, str]],
    prep_summary: dict[str, str],
) -> None:
    lines = [
        "# KJVA Gutenberg Source-Lock Decision Packet",
        "",
        "Status: decision packet only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "It converts the count-only Gutenberg source-lock prep into explicit source-lock decisions and blockers.",
        "It does not commit Bible text, normalize Bible text, create a local corpus, or declare a source-lock-ready stream.",
        "",
        "## Summary",
        "",
        f"- Decision rows: {summary['decision_rows']}.",
        f"- Policy-ready rows: {summary['policy_ready_rows']}.",
        f"- Recommended-but-not-locked rows: {summary['recommended_policy_rows']}.",
        f"- Blocked rows: {summary['blocked_rows']}.",
        f"- Candidate-not-locked rows: {summary['candidate_not_locked_rows']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Recommendation",
        "",
        "Use Project Gutenberg eBook 30 plus eBook 124 as the next independent KJVA candidate stream only after the remaining source-lock blockers close.",
        "Use Gutenberg source order for an independent Project Gutenberg replication stream, and document that this differs from the current local KJVA order.",
        "Roll the separate Epistle of Jeremiah source section into BAR for KJVA book-code compatibility while preserving source-component metadata.",
        "Do not source-lock Sirach or Prayer of Manasseh until their count drifts have citable, non-text collation decisions.",
        "",
        "## Source Order",
        "",
        f"- Local KJVA Apocrypha order: `{summary['local_apocrypha_order']}`.",
        f"- Gutenberg Apocrypha source order: `{summary['gutenberg_apocrypha_order']}`.",
        f"- Order recommendation: `{summary['order_recommendation']}`.",
        "",
        "## Count Evidence",
        "",
        f"- KJV exact count matches: {prep_summary.get('kjv_books_exact_count_matches', '')}/{prep_summary.get('kjv_books_compared', '')}.",
        f"- Apocrypha/deuterocanon exact count matches: {prep_summary.get('apocrypha_books_exact_count_matches', '')}/{prep_summary.get('apocrypha_books_compared', '')}.",
        f"- Apocrypha/deuterocanon count drifts: {prep_summary.get('apocrypha_books_count_drift', '')}.",
        f"- Extra source sections: {prep_summary.get('extra_source_sections', '')}.",
        "",
        "## Decision Rows",
        "",
        "| Decision | Area | Status | Recommendation | Blocker |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in decisions:
        lines.append(
            f"| `{row['decision_id']}` | {row['area']} | `{row['lock_status']}` | {row['recommendation']} | {row['blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is a planning and audit artifact. It does not choose final source text, create verse mappings, perform text collation, lock terms, lock controls, or authorize a result-bearing run.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    decisions: list[dict[str, str]],
    summary: dict[str, Any],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_gutenberg_source_lock_decision_packet",
        "claim_boundary": "decision packet only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "row_count": len(decisions),
        "summary": summary,
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "prep_rows": str(args.prep_rows),
            "prep_summary": str(args.prep_summary),
            "kjva_csv": str(args.kjva_csv),
        },
        "outputs": {
            "decisions": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def local_apocrypha_order(path: Path) -> list[str]:
    order: OrderedDict[str, None] = OrderedDict()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            book = row["book"]
            if book in APOCRYPHA_CODES:
                order.setdefault(book, None)
    return list(order)


def decision(
    decision_id: str,
    area: str,
    current_evidence: str,
    recommendation: str,
    lock_status: str,
    blocker: str,
    next_action: str,
) -> dict[str, str]:
    return {
        "decision_id": decision_id,
        "area": area,
        "current_evidence": current_evidence,
        "recommendation": recommendation,
        "lock_status": lock_status,
        "blocker": blocker,
        "next_action": next_action,
        "result_boundary": "not_result_bearing",
    }


def count_status(rows: list[dict[str, str]], status: str) -> int:
    return sum(1 for row in rows if row["lock_status"] == status)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_single_csv_row(path: Path) -> dict[str, str]:
    rows = read_csv_dicts(path)
    if len(rows) != 1:
        raise ValueError(f"{path} expected one row, found {len(rows)}")
    return rows[0]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
