#!/usr/bin/env python3
"""Build a non-text Gutenberg + Hakkaac KJVA split-source role sidecar."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_CURRENT_SUMMARY = Path("reports/kjva_current_source_lock_sidecar/summary.csv")
DEFAULT_GUTENBERG_DECISION_SUMMARY = Path(
    "reports/kjva_gutenberg_source_lock_decision_packet/summary.csv"
)
DEFAULT_GUTENBERG_DECISIONS = Path(
    "reports/kjva_gutenberg_source_lock_decision_packet/decisions.csv"
)
DEFAULT_GUTENBERG_BLOCKER_SUMMARY = Path(
    "reports/kjva_gutenberg_source_lock_blocker_packet/summary.csv"
)
DEFAULT_GUTENBERG_BOUNDARY_OPTIONS = Path(
    "reports/kjva_gutenberg_source_lock_blocker_packet/boundary_options.csv"
)
DEFAULT_GUTENBERG_MARKER_DIFF = Path(
    "reports/kjva_gutenberg_source_lock_blocker_packet/marker_diff.csv"
)
DEFAULT_HAKKAAC_SUMMARY = Path("reports/kjva_hakkaac_source_lock_decision_packet/summary.csv")
DEFAULT_HAKKAAC_DECISIONS = Path(
    "reports/kjva_hakkaac_source_lock_decision_packet/decisions.csv"
)
DEFAULT_HAKKAAC_DRIFT_ROWS = Path(
    "reports/kjva_hakkaac_source_lock_decision_packet/drift_rows.csv"
)
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_hakkaac_split_source_role_sidecar")
DEFAULT_ROLES = DEFAULT_OUT_DIR / "source_roles.csv"
DEFAULT_BLOCKERS = DEFAULT_OUT_DIR / "unresolved_blockers.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_HAKKAAC_SPLIT_SOURCE_ROLE_SIDECAR.md")

ROLE_FIELDNAMES = [
    "role_id",
    "source_family",
    "component",
    "source_role",
    "order_role",
    "lock_status",
    "allowed_use",
    "blocked_use",
    "evidence_summary",
    "next_action",
    "result_boundary",
]
BLOCKER_FIELDNAMES = [
    "blocker_id",
    "area",
    "current_status",
    "evidence_summary",
    "blocked_until",
    "affects_letter_stream",
    "result_boundary",
]
SUMMARY_FIELDNAMES = [
    "role_rows",
    "blocker_rows",
    "policy_ready_rows",
    "recommended_policy_rows",
    "blocked_rows",
    "candidate_not_locked_rows",
    "current_rerun_locked",
    "split_source_role_sidecar_written",
    "local_apocrypha_order",
    "gutenberg_apocrypha_order",
    "future_independent_order_recommendation",
    "hakkaac_exact_marker_books",
    "hakkaac_exact_normalized_verse_matches",
    "hakkaac_length_drift_verses",
    "gutenberg_sirach_gap_refs",
    "gutenberg_manasseh_source_markers",
    "gutenberg_manasseh_local_markers",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    current = read_single_csv_row(args.current_summary)
    gutenberg = read_single_csv_row(args.gutenberg_decision_summary)
    gutenberg_decisions = read_csv_dicts(args.gutenberg_decisions)
    blocker_summary = read_single_csv_row(args.gutenberg_blocker_summary)
    boundary_options = read_csv_dicts(args.gutenberg_boundary_options)
    marker_diff = read_csv_dicts(args.gutenberg_marker_diff)
    hakkaac = read_single_csv_row(args.hakkaac_summary)
    hakkaac_decisions = read_csv_dicts(args.hakkaac_decisions)
    hakkaac_drift_rows = read_csv_dicts(args.hakkaac_drift_rows)

    roles = build_roles(current, gutenberg, blocker_summary, hakkaac)
    blockers = build_blockers(
        blocker_summary,
        boundary_options,
        marker_diff,
        hakkaac,
        hakkaac_drift_rows,
        hakkaac_decisions,
        gutenberg_decisions,
    )
    summary = build_summary(roles, blockers, current, gutenberg, blocker_summary, hakkaac)
    write_csv(args.roles_out, ROLE_FIELDNAMES, roles)
    write_csv(args.blockers_out, BLOCKER_FIELDNAMES, blockers)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, roles, blockers)
    write_manifest(args.manifest_out, args, summary, roles, blockers, started)
    print(args.roles_out)
    print(args.blockers_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current-summary", type=Path, default=DEFAULT_CURRENT_SUMMARY)
    parser.add_argument(
        "--gutenberg-decision-summary",
        type=Path,
        default=DEFAULT_GUTENBERG_DECISION_SUMMARY,
    )
    parser.add_argument("--gutenberg-decisions", type=Path, default=DEFAULT_GUTENBERG_DECISIONS)
    parser.add_argument(
        "--gutenberg-blocker-summary",
        type=Path,
        default=DEFAULT_GUTENBERG_BLOCKER_SUMMARY,
    )
    parser.add_argument(
        "--gutenberg-boundary-options",
        type=Path,
        default=DEFAULT_GUTENBERG_BOUNDARY_OPTIONS,
    )
    parser.add_argument(
        "--gutenberg-marker-diff",
        type=Path,
        default=DEFAULT_GUTENBERG_MARKER_DIFF,
    )
    parser.add_argument("--hakkaac-summary", type=Path, default=DEFAULT_HAKKAAC_SUMMARY)
    parser.add_argument("--hakkaac-decisions", type=Path, default=DEFAULT_HAKKAAC_DECISIONS)
    parser.add_argument("--hakkaac-drift-rows", type=Path, default=DEFAULT_HAKKAAC_DRIFT_ROWS)
    parser.add_argument("--roles-out", type=Path, default=DEFAULT_ROLES)
    parser.add_argument("--blockers-out", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_roles(
    current: dict[str, str],
    gutenberg: dict[str, str],
    blocker_summary: dict[str, str],
    hakkaac: dict[str, str],
) -> list[dict[str, Any]]:
    return [
        role(
            "current_ebible_rerun_baseline",
            "current eBible KJV + Apocrypha",
            "full KJVA stream",
            "rerun_baseline_only",
            "current_local_order",
            "policy_ready",
            "rerun and reproduce current KJVA work by checksum/order/count sidecar",
            "independent replication source or silent replacement stream",
            f"{current.get('apocrypha_book_count', '')} apocrypha/deuterocanon books; {current.get('apocrypha_verse_count', '')} verses; CSV SHA-256 {current.get('csv_sha256', '')}",
            "Keep as current-source rerun lane only.",
        ),
        role(
            "gutenberg_kjv_component",
            "Project Gutenberg eBook 30",
            "66-book KJV component",
            "primary_kjv_candidate",
            "gutenberg_canonical_component",
            "recommended_policy_not_locked",
            "candidate component for a future independent stream",
            "result-bearing import before source-use, verse-map, checksum, and collation locks",
            "Gutenberg decision packet records 66/66 KJV count agreement.",
            "Build source-use, checksum, and collation locks before result use.",
        ),
        role(
            "gutenberg_apocrypha_component",
            "Project Gutenberg eBook 124",
            "Apocrypha/deuterocanon component",
            "primary_apocrypha_candidate",
            "gutenberg_source_order",
            "blocked",
            "candidate component after blocker policy is resolved",
            "source-locked stream while Sirach and Prayer of Manasseh blockers remain",
            f"{gutenberg.get('order_recommendation', '')}; Sirach gap {blocker_summary.get('sirach_gap_refs', '')}; MAN markers {blocker_summary.get('manasseh_source_markers', '')}/{blocker_summary.get('manasseh_local_markers', '')}",
            "Resolve marker/boundary blockers or keep out of result-bearing work.",
        ),
        role(
            "gutenberg_lje_baruch_rollup",
            "Project Gutenberg eBook 124",
            "Epistle of Jeremiah source section",
            "component_metadata_rollup_candidate",
            "roll_lje_source_into_bar_for_kjva_book_code",
            "recommended_policy_not_locked",
            "document source-component metadata in a future independent stream",
            "unlabeled merger without preregistered source-role metadata",
            gutenberg.get("baruch_epistle_recommendation", ""),
            "Name the BAR/LJE rollup in any future study-lock sidecar.",
        ),
        role(
            "hakkaac_marker_collation_witness",
            "Hakkaac KJV Apocrypha",
            "14-book Apocrypha/deuterocanon witness",
            "marker_and_collation_witness_only",
            "not_primary_order_source",
            "candidate_not_locked",
            "non-text marker/collation corroboration and drift evidence",
            "primary source text authority or tracked corpus import",
            f"{hakkaac.get('marker_books_exact', '')}/14 marker books exact; {hakkaac.get('exact_normalized_verse_matches', '')}/{hakkaac.get('total_verses', '')} normalized verse matches; {hakkaac.get('length_drift_verses', '')} drift row",
            "Keep Hakkaac as evidence unless source-use and drift policies are locked.",
        ),
        role(
            "split_stream_boundary",
            "Project Gutenberg plus Hakkaac",
            "future split-source candidate",
            "split_source_policy_boundary",
            "gutenberg_order_if_future_independent_stream",
            "blocked",
            "planning-only role map",
            "result-bearing split-source run",
            "This sidecar writes roles/order, but source-use, drift, term/control, and study locks remain open.",
            "Finish blockers before any ELS result run.",
        ),
        role(
            "tracked_text_retention_boundary",
            "all KJVA source candidates",
            "tracked outputs",
            "no_tracked_bible_text",
            "not_applicable",
            "policy_ready",
            "commit checksums, counts, refs, lengths, roles, and decisions",
            "tracked raw Bible text",
            "All inputs used here are existing derived reports and ignored/private source evidence.",
            "Keep report outputs non-text.",
        ),
    ]


def build_blockers(
    blocker_summary: dict[str, str],
    boundary_options: list[dict[str, str]],
    marker_diff: list[dict[str, str]],
    hakkaac: dict[str, str],
    hakkaac_drift_rows: list[dict[str, str]],
    hakkaac_decisions: list[dict[str, str]],
    gutenberg_decisions: list[dict[str, str]],
) -> list[dict[str, Any]]:
    sirach_gap = ";".join(row.get("local_ref", "") for row in marker_diff) or "SIR 44:23"
    boundary_option_ids = ";".join(row.get("option_id", "") for row in boundary_options)
    source_use_boundary = find_decision(hakkaac_decisions, "source_use_boundary")
    split_source_policy = find_decision(hakkaac_decisions, "split_source_policy")
    gutenberg_source_stream = find_decision(gutenberg_decisions, "source_stream")
    drift_refs = ";".join(row.get("ref", "") for row in hakkaac_drift_rows) or "SIR 19:1"
    return [
        blocker(
            "sirach_44_23_gutenberg_marker_gap",
            "Sirach marker gap",
            "non_text_corroborated_not_source_locked",
            f"Gutenberg marker list misses {sirach_gap}; Hakkaac blocker rows exact {hakkaac.get('blocker_rows_exact', '')}/16.",
            "a source policy decides whether Hakkaac can supply marker/text authority or Gutenberg remains blocked",
            True,
        ),
        blocker(
            "manasseh_unmarked_gutenberg_section",
            "Prayer of Manasseh boundary",
            "non_text_corroborated_not_source_locked",
            f"Gutenberg MAN source markers {blocker_summary.get('manasseh_source_markers', '')}; local markers {blocker_summary.get('manasseh_local_markers', '')}; options {boundary_option_ids}.",
            "a cited marked source, exclusion policy, or boundary rule is locked before results",
            True,
        ),
        blocker(
            "sirach_19_1_hakkaac_length_drift",
            "Hakkaac/local drift",
            "blocked",
            f"Hakkaac decision packet names {drift_refs}; {hakkaac.get('length_drift_verses', '')} length-drift verse.",
            "a cited source policy chooses which normalized stream to lock",
            True,
        ),
        blocker(
            "hakkaac_source_use_boundary",
            "source use",
            "candidate_not_locked",
            source_use_boundary.get(
                "blocker",
                "Hakkaac has candidate evidence only, not source-use approval.",
            ),
            "source-use lock permits exactly stated role, or Hakkaac remains witness-only",
            True,
        ),
        blocker(
            "split_source_result_boundary",
            "split-source result boundary",
            "blocked",
            split_source_policy.get(
                "blocker",
                "Split-source roles affect reproducibility, source order, and source provenance.",
            ),
            "source roles, source use, drift policy, term lock, control lock, and study lock all exist",
            True,
        ),
        blocker(
            "gutenberg_source_stream_boundary",
            "Gutenberg source stream",
            "candidate_not_locked",
            gutenberg_source_stream.get(
                "blocker",
                "No study-lock sidecar, verse map, collation, or source-use lock exists yet.",
            ),
            "source-use, verse-map, collation, checksum, term, control, and study locks exist",
            True,
        ),
    ]


def build_summary(
    roles: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    current: dict[str, str],
    gutenberg: dict[str, str],
    blocker_summary: dict[str, str],
    hakkaac: dict[str, str],
) -> dict[str, Any]:
    return {
        "role_rows": len(roles),
        "blocker_rows": len(blockers),
        "policy_ready_rows": count_status(roles, "policy_ready"),
        "recommended_policy_rows": count_status(roles, "recommended_policy_not_locked"),
        "blocked_rows": count_status(roles, "blocked"),
        "candidate_not_locked_rows": count_status(roles, "candidate_not_locked"),
        "current_rerun_locked": current.get("rerun_baseline_locked", "") == "True",
        "split_source_role_sidecar_written": True,
        "local_apocrypha_order": gutenberg.get("local_apocrypha_order", ""),
        "gutenberg_apocrypha_order": gutenberg.get("gutenberg_apocrypha_order", ""),
        "future_independent_order_recommendation": (
            "use_gutenberg_source_order_for_independent_replication"
        ),
        "hakkaac_exact_marker_books": hakkaac.get("marker_books_exact", ""),
        "hakkaac_exact_normalized_verse_matches": hakkaac.get(
            "exact_normalized_verse_matches", ""
        ),
        "hakkaac_length_drift_verses": hakkaac.get("length_drift_verses", ""),
        "gutenberg_sirach_gap_refs": blocker_summary.get("sirach_gap_refs", ""),
        "gutenberg_manasseh_source_markers": blocker_summary.get(
            "manasseh_source_markers", ""
        ),
        "gutenberg_manasseh_local_markers": blocker_summary.get(
            "manasseh_local_markers", ""
        ),
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "split_source_role_sidecar_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    roles: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> None:
    lines = [
        "# KJVA Gutenberg Hakkaac Split-Source Role Sidecar",
        "",
        "Status: split-source role sidecar only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, not a source-use approval, and not a result-bearing replication.",
        "It writes the source roles and order boundary for the Project Gutenberg plus Hakkaac candidate path.",
        "It does not commit Bible text, choose a final source text, replace current eBible KJVA, or authorize a split-source run.",
        "",
        "## Summary",
        "",
        f"- Role rows: {summary['role_rows']}.",
        f"- Unresolved blocker rows: {summary['blocker_rows']}.",
        f"- Policy-ready role rows: {summary['policy_ready_rows']}.",
        f"- Recommended-but-not-locked role rows: {summary['recommended_policy_rows']}.",
        f"- Blocked role rows: {summary['blocked_rows']}.",
        f"- Candidate-not-locked role rows: {summary['candidate_not_locked_rows']}.",
        f"- Current eBible rerun baseline locked: {int(bool(summary['current_rerun_locked']))}.",
        f"- Split-source role sidecar written: {int(bool(summary['split_source_role_sidecar_written']))}.",
        f"- Hakkaac exact marker books: {summary['hakkaac_exact_marker_books']}/14.",
        f"- Hakkaac exact normalized verse matches: {summary['hakkaac_exact_normalized_verse_matches']}/5720.",
        f"- Hakkaac length-drift verses: {summary['hakkaac_length_drift_verses']}.",
        f"- Gutenberg Sirach gap refs: `{summary['gutenberg_sirach_gap_refs']}`.",
        f"- Gutenberg Prayer of Manasseh markers: {summary['gutenberg_manasseh_source_markers']}/{summary['gutenberg_manasseh_local_markers']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Source Order",
        "",
        f"- Current local KJVA Apocrypha/deuterocanon order: `{summary['local_apocrypha_order']}`.",
        f"- Project Gutenberg Apocrypha source order: `{summary['gutenberg_apocrypha_order']}`.",
        "- Future independent candidate order recommendation: `use_gutenberg_source_order_for_independent_replication`.",
        "- Current eBible KJVA order remains the rerun baseline order only.",
        "",
        "## Source Roles",
        "",
        "| Role | Source family | Component | Source role | Order role | Status | Allowed use | Blocked use |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in roles:
        lines.append(
            f"| `{row['role_id']}` | {row['source_family']} | {row['component']} | `{row['source_role']}` | `{row['order_role']}` | `{row['lock_status']}` | {row['allowed_use']} | {row['blocked_use']} |"
        )
    lines.extend(
        [
            "",
            "## Unresolved Blockers",
            "",
            "| Blocker | Area | Status | Evidence | Blocked until | Affects letter stream |",
            "| --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for row in blockers:
        lines.append(
            f"| `{row['blocker_id']}` | {row['area']} | `{row['current_status']}` | {row['evidence_summary']} | {row['blocked_until']} | {int(bool(row['affects_letter_stream']))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This sidecar closes only the missing written source-role/order boundary.",
            "It does not close the source-use boundary, the `SIR 19:1` drift boundary, the Prayer of Manasseh boundary, or the future term/control/study-lock boundary.",
            "No Bible text is written to tracked outputs.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    roles: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_gutenberg_hakkaac_split_source_role_sidecar",
        "claim_boundary": "split-source role sidecar only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "role_rows": len(roles),
        "blocker_rows": len(blockers),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "current_summary": str(args.current_summary),
            "gutenberg_decision_summary": str(args.gutenberg_decision_summary),
            "gutenberg_decisions": str(args.gutenberg_decisions),
            "gutenberg_blocker_summary": str(args.gutenberg_blocker_summary),
            "gutenberg_boundary_options": str(args.gutenberg_boundary_options),
            "gutenberg_marker_diff": str(args.gutenberg_marker_diff),
            "hakkaac_summary": str(args.hakkaac_summary),
            "hakkaac_decisions": str(args.hakkaac_decisions),
            "hakkaac_drift_rows": str(args.hakkaac_drift_rows),
        },
        "outputs": {
            "roles": str(args.roles_out),
            "blockers": str(args.blockers_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def role(
    role_id: str,
    source_family: str,
    component: str,
    source_role: str,
    order_role: str,
    lock_status: str,
    allowed_use: str,
    blocked_use: str,
    evidence_summary: str,
    next_action: str,
) -> dict[str, Any]:
    return {
        "role_id": role_id,
        "source_family": source_family,
        "component": component,
        "source_role": source_role,
        "order_role": order_role,
        "lock_status": lock_status,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use,
        "evidence_summary": evidence_summary,
        "next_action": next_action,
        "result_boundary": "not_result_bearing",
    }


def blocker(
    blocker_id: str,
    area: str,
    current_status: str,
    evidence_summary: str,
    blocked_until: str,
    affects_letter_stream: bool,
) -> dict[str, Any]:
    return {
        "blocker_id": blocker_id,
        "area": area,
        "current_status": current_status,
        "evidence_summary": evidence_summary,
        "blocked_until": blocked_until,
        "affects_letter_stream": affects_letter_stream,
        "result_boundary": "not_result_bearing",
    }


def find_decision(rows: list[dict[str, str]], decision_id: str) -> dict[str, str]:
    for row in rows:
        if row.get("decision_id") == decision_id:
            return row
    return {}


def count_status(rows: list[dict[str, Any]], status: str) -> int:
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
