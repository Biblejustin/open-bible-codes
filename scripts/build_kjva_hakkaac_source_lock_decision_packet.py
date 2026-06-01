#!/usr/bin/env python3
"""Build a Hakkaac KJVA Apocrypha source-lock decision packet from non-text evidence."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_COLLATION_SUMMARY = Path("reports/kjva_hakkaac_apocrypha_collation/summary.csv")
DEFAULT_BOOK_COLLATION = Path("reports/kjva_hakkaac_apocrypha_collation/book_collation.csv")
DEFAULT_BLOCKER_COLLATION = Path(
    "reports/kjva_hakkaac_apocrypha_collation/blocker_collation.csv"
)
DEFAULT_VERSE_COLLATION = Path("reports/kjva_hakkaac_apocrypha_collation/verse_collation.csv")
DEFAULT_MARKER_SUMMARY = Path("reports/kjva_hakkaac_apocrypha_marker_coverage/summary.csv")
DEFAULT_OUT_DIR = Path("reports/kjva_hakkaac_source_lock_decision_packet")
DEFAULT_DECISIONS = DEFAULT_OUT_DIR / "decisions.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_DRIFT_ROWS = DEFAULT_OUT_DIR / "drift_rows.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_HAKKAAC_SOURCE_LOCK_DECISION_PACKET.md")

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
DRIFT_FIELDNAMES = [
    "ref",
    "book",
    "status",
    "local_norm_len",
    "hakkaac_norm_len",
    "norm_len_delta",
    "first_diff_offset",
    "recommendation",
]
SUMMARY_FIELDNAMES = [
    "decision_rows",
    "policy_ready_rows",
    "recommended_policy_rows",
    "blocked_rows",
    "candidate_not_locked_rows",
    "total_verses",
    "exact_normalized_verse_matches",
    "length_drift_verses",
    "exact_book_stream_matches",
    "book_stream_drift_books",
    "blocker_rows_exact",
    "marker_books_exact",
    "source_policy_recommendation",
    "drift_recommendation",
    "split_source_recommendation",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    collation_summary = read_single_csv_row(args.collation_summary)
    book_rows = read_csv_dicts(args.book_collation)
    blocker_rows = read_csv_dicts(args.blocker_collation)
    verse_rows = read_csv_dicts(args.verse_collation)
    marker_summary = read_single_csv_row(args.marker_summary)
    drift_rows = build_drift_rows(verse_rows)
    decisions = build_decisions(
        collation_summary,
        marker_summary,
        blocker_rows,
        drift_rows,
    )
    summary = build_summary(decisions, collation_summary, marker_summary, blocker_rows)
    write_csv(args.out, DECISION_FIELDNAMES, decisions)
    write_csv(args.drift_out, DRIFT_FIELDNAMES, drift_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, decisions, drift_rows, book_rows)
    write_manifest(args.manifest_out, args, decisions, summary, started)
    print(args.out)
    print(args.drift_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collation-summary", type=Path, default=DEFAULT_COLLATION_SUMMARY)
    parser.add_argument("--book-collation", type=Path, default=DEFAULT_BOOK_COLLATION)
    parser.add_argument("--blocker-collation", type=Path, default=DEFAULT_BLOCKER_COLLATION)
    parser.add_argument("--verse-collation", type=Path, default=DEFAULT_VERSE_COLLATION)
    parser.add_argument("--marker-summary", type=Path, default=DEFAULT_MARKER_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--drift-out", type=Path, default=DEFAULT_DRIFT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_decisions(
    collation: dict[str, str],
    marker_summary: dict[str, str],
    blocker_rows: list[dict[str, str]],
    drift_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    exact_blockers = sum(1 for row in blocker_rows if row.get("status") == "exact_normalized_match")
    return [
        decision(
            "source_use_boundary",
            "source use",
            "Hakkaac was approved only for ignored local import and non-text collation evidence.",
            "Keep Hakkaac as candidate evidence unless a separate source-use lock is written.",
            "candidate_not_locked",
            "Current approval does not authorize tracked source text or result-bearing corpus use.",
            "Write a source-use lock before any source replacement or new replication stream.",
        ),
        decision(
            "raw_text_retention",
            "text retention",
            f"Collation summary private_text_path={collation.get('private_text_path', '')}.",
            "Keep raw Hakkaac verse text under ignored data/private output; commit only hashes, counts, lengths, refs, and decisions.",
            "policy_ready",
            "",
            "Continue using non-text tracked outputs.",
        ),
        decision(
            "marker_coverage",
            "marker coverage",
            f"{marker_summary.get('exact_book_marker_matches', '')} of {marker_summary.get('local_books_compared', '')} books have exact marker-count agreement.",
            "Use Hakkaac marker coverage as non-text evidence that all 14 tracked Apocrypha/deuterocanon books are represented.",
            "policy_ready",
            "",
            "Keep marker coverage in the source-candidate evidence chain.",
        ),
        decision(
            "gutenberg_blocker_rows",
            "Gutenberg blockers",
            f"{exact_blockers} of {len(blocker_rows)} blocker rows are exact normalized matches.",
            "Use Hakkaac as non-text corroboration for the Gutenberg Sirach 44:23 and Prayer of Manasseh marker blockers.",
            "recommended_policy_not_locked",
            "This corroborates blockers but does not make either source stream ready.",
            "Keep Project Gutenberg and Hakkaac roles separate in a future study-lock sidecar.",
        ),
        decision(
            "collation_strength",
            "collation strength",
            f"{collation.get('exact_normalized_verse_matches', '')} of {collation.get('comparable_refs', '')} comparable refs are exact normalized verse matches.",
            "Treat Hakkaac as a strong external witness for the current eBible KJVA Apocrypha stream, subject to the one drift row.",
            "recommended_policy_not_locked",
            "One verse has normalized length drift.",
            "Keep the exact-match evidence, but do not claim source-lock readiness.",
        ),
        decision(
            "sirach_19_1_drift",
            "Sirach drift",
            describe_drift_rows(drift_rows),
            "Do not patch either source automatically; keep SIR 19:1 as a named drift until a source policy chooses which normalized stream to lock.",
            "blocked",
            "One normalized-letter length drift changes the ELS letter stream.",
            "Choose a cited drift policy or keep Hakkaac as corroborating evidence only.",
        ),
        decision(
            "split_source_policy",
            "split-source policy",
            "Project Gutenberg has public-domain-USA metadata and broad coverage; Hakkaac resolves marker/blocker evidence but is approved here only as ignored-local collation evidence.",
            "Do not combine Project Gutenberg plus Hakkaac into a result-bearing split-source stream without a written source-order and source-role policy.",
            "blocked",
            "Split-source roles affect reproducibility, source order, and source provenance.",
            "Write a split-source policy sidecar before any result-bearing run.",
        ),
        decision(
            "current_ebible_reference",
            "current eBible KJVA",
            "The existing eBible KJV + Apocrypha corpus remains the current rerun corpus and is public-domain-marked by eBible in the control registry.",
            "Keep current eBible KJVA as the rerun baseline until a fresh independent source lock is complete.",
            "policy_ready",
            "",
            "Use Hakkaac and Gutenberg as source-candidate evidence, not as silent replacements.",
        ),
        decision(
            "result_boundary",
            "result boundary",
            "No term lock, control lock, source-lock sidecar, split-source sidecar, or SIR 19:1 drift decision exists for a new KJVA replication stream.",
            "Do not run a result-bearing KJVA bridge replication from Hakkaac or split-source evidence yet.",
            "blocked",
            "Source-lock prerequisites remain open.",
            "Finish source decisions, then build a fresh study-lock package before results.",
        ),
    ]


def build_drift_rows(verse_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in verse_rows:
        if row.get("status") == "exact_normalized_match":
            continue
        rows.append(
            {
                "ref": row.get("ref", ""),
                "book": row.get("book", ""),
                "status": row.get("status", ""),
                "local_norm_len": row.get("local_norm_len", ""),
                "hakkaac_norm_len": row.get("hakkaac_norm_len", ""),
                "norm_len_delta": row.get("norm_len_delta", ""),
                "first_diff_offset": row.get("first_diff_offset", ""),
                "recommendation": "keep_named_drift_until_source_policy_lock",
            }
        )
    return rows


def build_summary(
    decisions: list[dict[str, str]],
    collation: dict[str, str],
    marker_summary: dict[str, str],
    blocker_rows: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "decision_rows": len(decisions),
        "policy_ready_rows": count_status(decisions, "policy_ready"),
        "recommended_policy_rows": count_status(decisions, "recommended_policy_not_locked"),
        "blocked_rows": count_status(decisions, "blocked"),
        "candidate_not_locked_rows": count_status(decisions, "candidate_not_locked"),
        "total_verses": collation.get("local_verses", ""),
        "exact_normalized_verse_matches": collation.get("exact_normalized_verse_matches", ""),
        "length_drift_verses": collation.get("length_drift_verses", ""),
        "exact_book_stream_matches": collation.get("exact_book_stream_matches", ""),
        "book_stream_drift_books": collation.get("book_stream_drift_books", ""),
        "blocker_rows_exact": sum(
            1 for row in blocker_rows if row.get("status") == "exact_normalized_match"
        ),
        "marker_books_exact": marker_summary.get("exact_book_marker_matches", ""),
        "source_policy_recommendation": "candidate_evidence_only_until_source_use_lock",
        "drift_recommendation": "keep_sir_19_1_named_drift_do_not_patch_automatically",
        "split_source_recommendation": "do_not_combine_gutenberg_and_hakkaac_without_sidecar",
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "decision_packet_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    decisions: list[dict[str, str]],
    drift_rows: list[dict[str, Any]],
    book_rows: list[dict[str, str]],
) -> None:
    lines = [
        "# KJVA Hakkaac Source-Lock Decision Packet",
        "",
        "Status: decision packet only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "It converts Hakkaac marker coverage and ignored-local collation evidence into explicit source-lock decisions and blockers.",
        "It does not commit Bible text, normalize Bible text into a tracked corpus, replace the current eBible KJVA source, or authorize a split-source run.",
        "",
        "## Summary",
        "",
        f"- Decision rows: {summary['decision_rows']}.",
        f"- Policy-ready rows: {summary['policy_ready_rows']}.",
        f"- Recommended-but-not-locked rows: {summary['recommended_policy_rows']}.",
        f"- Blocked rows: {summary['blocked_rows']}.",
        f"- Candidate-not-locked rows: {summary['candidate_not_locked_rows']}.",
        f"- Exact normalized verse matches: {summary['exact_normalized_verse_matches']}/{summary['total_verses']}.",
        f"- Length-drift verses: {summary['length_drift_verses']}.",
        f"- Exact book stream matches: {summary['exact_book_stream_matches']}/14.",
        f"- Book stream drift books: {summary['book_stream_drift_books']}.",
        f"- Exact blocker rows: {summary['blocker_rows_exact']}/16.",
        f"- Exact marker books: {summary['marker_books_exact']}/14.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Recommendation",
        "",
        "Keep Hakkaac as candidate evidence only until a separate source-use lock is written.",
        "Keep current eBible KJVA as the rerun baseline until a fresh independent source lock is complete.",
        "Do not patch either source automatically for `SIR 19:1`.",
        "Do not combine Project Gutenberg plus Hakkaac into a result-bearing split-source stream without a written source-order and source-role sidecar.",
        "",
        "## Drift Rows",
        "",
        "| Ref | Status | Local letters | Hakkaac letters | Delta | First diff offset | Recommendation |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in drift_rows:
        lines.append(
            f"| `{row['ref']}` | `{row['status']}` | {row['local_norm_len']} | {row['hakkaac_norm_len']} | {row['norm_len_delta']} | {row['first_diff_offset']} | `{row['recommendation']}` |"
        )
    lines.extend(
        [
            "",
            "## Book Read",
            "",
            "| Book | Exact verses | Length-drift verses | Stream status |",
            "| --- | ---: | ---: | --- |",
        ]
    )
    for row in book_rows:
        lines.append(
            f"| `{row['book']}` | {row['exact_normalized_verse_matches']} | {row['length_drift_verses']} | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Decision Rows",
            "",
            "| Decision | Area | Status | Recommendation | Blocker |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in decisions:
        lines.append(
            f"| `{row['decision_id']}` | {row['area']} | `{row['lock_status']}` | {row['recommendation']} | {row['blocker']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is a planning and audit artifact.",
            "It does not choose final source text, create verse mappings, perform result-bearing ELS searches, lock terms, lock controls, or authorize a new KJVA bridge run.",
            "No Bible text is written to tracked outputs.",
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
        "tool": "scripts.build_kjva_hakkaac_source_lock_decision_packet",
        "claim_boundary": "decision packet only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "row_count": len(decisions),
        "summary": summary,
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "collation_summary": str(args.collation_summary),
            "book_collation": str(args.book_collation),
            "blocker_collation": str(args.blocker_collation),
            "verse_collation": str(args.verse_collation),
            "marker_summary": str(args.marker_summary),
        },
        "outputs": {
            "decisions": str(args.out),
            "drift_rows": str(args.drift_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def describe_drift_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No non-exact Hakkaac/local KJVA collation rows."
    return "; ".join(
        f"{row['ref']} {row['status']} local={row['local_norm_len']} hakkaac={row['hakkaac_norm_len']} delta={row['norm_len_delta']}"
        for row in rows
    )


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
