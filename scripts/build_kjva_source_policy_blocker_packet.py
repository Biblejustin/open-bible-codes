#!/usr/bin/env python3
"""Build a non-text KJVA source-policy blocker packet."""

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
DEFAULT_GUTENBERG_CHECKSUM_SUMMARY = Path(
    "reports/kjva_gutenberg_candidate_checksum_sidecar/summary.csv"
)
DEFAULT_GUTENBERG_BLOCKER_SUMMARY = Path(
    "reports/kjva_gutenberg_source_lock_blocker_packet/summary.csv"
)
DEFAULT_HAKKAAC_DECISION_SUMMARY = Path(
    "reports/kjva_hakkaac_source_lock_decision_packet/summary.csv"
)
DEFAULT_SPLIT_ROLE_SUMMARY = Path(
    "reports/kjva_gutenberg_hakkaac_split_source_role_sidecar/summary.csv"
)
DEFAULT_OUT_DIR = Path("reports/kjva_source_policy_blocker_packet")
DEFAULT_OPTIONS = DEFAULT_OUT_DIR / "policy_options.csv"
DEFAULT_BLOCKERS = DEFAULT_OUT_DIR / "blockers.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_SOURCE_POLICY_BLOCKER_PACKET.md")

OPTION_FIELDNAMES = [
    "option_id",
    "source_stream",
    "status",
    "allowed_use",
    "blocked_use",
    "evidence_summary",
    "blocker_summary",
    "next_action",
    "result_boundary",
]
BLOCKER_FIELDNAMES = [
    "blocker_id",
    "area",
    "status",
    "evidence_summary",
    "required_before_result",
    "needs_user_or_source_policy_choice",
    "affects_letter_stream",
    "result_boundary",
]
SUMMARY_FIELDNAMES = [
    "policy_option_rows",
    "blocker_rows",
    "policy_ready_options",
    "blocked_options",
    "checksum_records_ready",
    "split_source_role_sidecar_written",
    "current_rerun_locked",
    "source_use_ready_pages",
    "gutenberg_sirach_gap_refs",
    "gutenberg_manasseh_source_markers",
    "gutenberg_manasseh_local_markers",
    "hakkaac_length_drift_verses",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    current = read_single_csv_row(args.current_summary)
    checksums = read_single_csv_row(args.gutenberg_checksum_summary)
    gutenberg_blockers = read_single_csv_row(args.gutenberg_blocker_summary)
    hakkaac = read_single_csv_row(args.hakkaac_decision_summary)
    split_roles = read_single_csv_row(args.split_role_summary)
    options = build_policy_options(current, checksums, gutenberg_blockers, hakkaac, split_roles)
    blockers = build_blockers(checksums, gutenberg_blockers, hakkaac, split_roles)
    summary = build_summary(options, blockers, current, checksums, gutenberg_blockers, hakkaac, split_roles)
    write_csv(args.options_out, OPTION_FIELDNAMES, options)
    write_csv(args.blockers_out, BLOCKER_FIELDNAMES, blockers)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, options, blockers)
    write_manifest(args.manifest_out, args, summary, options, blockers, started)
    print(args.options_out)
    print(args.blockers_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current-summary", type=Path, default=DEFAULT_CURRENT_SUMMARY)
    parser.add_argument(
        "--gutenberg-checksum-summary",
        type=Path,
        default=DEFAULT_GUTENBERG_CHECKSUM_SUMMARY,
    )
    parser.add_argument(
        "--gutenberg-blocker-summary",
        type=Path,
        default=DEFAULT_GUTENBERG_BLOCKER_SUMMARY,
    )
    parser.add_argument(
        "--hakkaac-decision-summary",
        type=Path,
        default=DEFAULT_HAKKAAC_DECISION_SUMMARY,
    )
    parser.add_argument("--split-role-summary", type=Path, default=DEFAULT_SPLIT_ROLE_SUMMARY)
    parser.add_argument("--options-out", type=Path, default=DEFAULT_OPTIONS)
    parser.add_argument("--blockers-out", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_policy_options(
    current: dict[str, str],
    checksums: dict[str, str],
    gutenberg_blockers: dict[str, str],
    hakkaac: dict[str, str],
    split_roles: dict[str, str],
) -> list[dict[str, Any]]:
    return [
        option(
            "current_ebible_rerun_only",
            "current eBible KJV + Apocrypha",
            "policy_ready",
            "rerun and reproduce current KJVA work by checksum/order/count sidecar",
            "independent replication claim or silent source replacement",
            f"current rerun locked={current.get('rerun_baseline_locked', '')}; books={current.get('book_count', '')}; verses={current.get('verse_count', '')}",
            "not independent-source-ready",
            "Keep as rerun baseline only.",
        ),
        option(
            "project_gutenberg_only_candidate",
            "Project Gutenberg eBook 30 plus eBook 124",
            "blocked",
            "candidate stream with checksum identifiers and count evidence",
            "source-locked or result-bearing stream",
            f"checksum records ready={checksums.get('checksum_records_ready', '')}; source-use ready pages={checksums.get('source_use_ready_pages', '')}",
            f"Sirach gap {gutenberg_blockers.get('sirach_gap_refs', '')}; MAN markers {gutenberg_blockers.get('manasseh_source_markers', '')}/{gutenberg_blockers.get('manasseh_local_markers', '')}",
            "Resolve source-use, verse-map, collation, Sirach, and MAN blockers.",
        ),
        option(
            "project_gutenberg_hakkaac_split_candidate",
            "Project Gutenberg plus Hakkaac",
            "blocked",
            "planning-only split-source candidate with written roles/order",
            "result-bearing split-source stream",
            f"split-role sidecar written={split_roles.get('split_source_role_sidecar_written', '')}; Hakkaac matches={hakkaac.get('exact_normalized_verse_matches', '')}/{hakkaac.get('total_verses', '')}",
            "source-use, SIR 19:1 drift, Prayer of Manasseh, term/control, and study-lock blockers remain",
            "Choose source-use/drift/boundary policy before any study lock.",
        ),
        option(
            "hakkaac_primary_stream",
            "Hakkaac KJV Apocrypha",
            "blocked",
            "marker and collation witness only",
            "primary tracked corpus or source-text authority",
            f"marker books exact={hakkaac.get('marker_books_exact', '')}/14; length drifts={hakkaac.get('length_drift_verses', '')}",
            "current approval does not authorize tracked source text or result-bearing corpus use",
            "Keep witness-only unless source-use approval and drift policy are locked.",
        ),
        option(
            "defer_new_kjva_replication",
            "no new independent KJVA stream",
            "policy_ready",
            "continue audit/planning while current prospective KJVA lane remains negative",
            "new result-bearing replication",
            "all current source candidates remain not source-lock ready",
            "fresh term/control/study-lock sidecar still absent",
            "Do not run new KJVA results until blockers close.",
        ),
    ]


def build_blockers(
    checksums: dict[str, str],
    gutenberg_blockers: dict[str, str],
    hakkaac: dict[str, str],
    split_roles: dict[str, str],
) -> list[dict[str, Any]]:
    return [
        blocker(
            "source_use_policy_lock",
            "source use",
            "blocked",
            f"Gutenberg source-use ready pages={checksums.get('source_use_ready_pages', '')}; Hakkaac remains witness-only.",
            "explicit source-use policy names which external source may supply result-bearing text, if any",
            True,
            True,
        ),
        blocker(
            "gutenberg_sirach_44_23_marker_gap",
            "Sirach marker gap",
            "blocked",
            f"Gutenberg marker gap refs={gutenberg_blockers.get('sirach_gap_refs', '')}; missing count={gutenberg_blockers.get('sirach_missing_source_marker_count', '')}.",
            "citable policy explains whether to keep Gutenberg blocked, exclude/patch nothing, or use witness evidence",
            True,
            True,
        ),
        blocker(
            "gutenberg_prayer_of_manasseh_boundary",
            "Prayer of Manasseh boundary",
            "blocked",
            f"Gutenberg source markers={gutenberg_blockers.get('manasseh_source_markers', '')}; local markers={gutenberg_blockers.get('manasseh_local_markers', '')}.",
            "cited marked source, exclusion policy, or boundary rule exists before results",
            True,
            True,
        ),
        blocker(
            "hakkaac_sirach_19_1_length_drift",
            "Hakkaac/local drift",
            "blocked",
            f"Hakkaac length-drift verses={hakkaac.get('length_drift_verses', '')}; exact book streams={hakkaac.get('exact_book_stream_matches', '')}/14.",
            "source policy chooses the locked normalized stream or keeps Hakkaac witness-only",
            True,
            True,
        ),
        blocker(
            "verse_map_and_collation_lock",
            "verse map and collation",
            "blocked",
            "No result-bearing verse map or full independent-source collation lock exists.",
            "verse mapping and collation sidecar exists for the selected source stream",
            False,
            True,
        ),
        blocker(
            "term_control_study_lock",
            "study lock",
            "blocked",
            "No fresh term lock, control lock, leakage audit, or study-lock sidecar exists for a new KJVA run.",
            "fresh preregistered term/control/study-lock package exists before output",
            True,
            True,
        ),
        blocker(
            "role_sidecar_complete_but_not_sufficient",
            "source roles",
            "closed_as_planning_only",
            f"role rows={split_roles.get('role_rows', '')}; blocker rows={split_roles.get('blocker_rows', '')}; role sidecar written={split_roles.get('split_source_role_sidecar_written', '')}.",
            "remaining blockers close; role sidecar alone never authorizes results",
            False,
            True,
        ),
    ]


def build_summary(
    options: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    current: dict[str, str],
    checksums: dict[str, str],
    gutenberg_blockers: dict[str, str],
    hakkaac: dict[str, str],
    split_roles: dict[str, str],
) -> dict[str, Any]:
    return {
        "policy_option_rows": len(options),
        "blocker_rows": len(blockers),
        "policy_ready_options": count_status(options, "policy_ready"),
        "blocked_options": count_status(options, "blocked"),
        "checksum_records_ready": checksums.get("checksum_records_ready", ""),
        "split_source_role_sidecar_written": (
            split_roles.get("split_source_role_sidecar_written", "") == "True"
        ),
        "current_rerun_locked": current.get("rerun_baseline_locked", "") == "True",
        "source_use_ready_pages": checksums.get("source_use_ready_pages", ""),
        "gutenberg_sirach_gap_refs": gutenberg_blockers.get("sirach_gap_refs", ""),
        "gutenberg_manasseh_source_markers": gutenberg_blockers.get(
            "manasseh_source_markers", ""
        ),
        "gutenberg_manasseh_local_markers": gutenberg_blockers.get(
            "manasseh_local_markers", ""
        ),
        "hakkaac_length_drift_verses": hakkaac.get("length_drift_verses", ""),
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "source_policy_blocker_packet_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    options: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> None:
    lines = [
        "# KJVA Source Policy Blocker Packet",
        "",
        "Status: source-policy blocker packet only.",
        "",
        "This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, and not a result-bearing replication.",
        "It narrows current KJVA source-policy options and names the blockers that remain before any new result-bearing run.",
        "It does not commit Bible text, choose a final source text, replace current eBible KJVA, or authorize a split-source run.",
        "",
        "## Summary",
        "",
        f"- Policy option rows: {summary['policy_option_rows']}.",
        f"- Blocker rows: {summary['blocker_rows']}.",
        f"- Policy-ready options: {summary['policy_ready_options']}.",
        f"- Blocked options: {summary['blocked_options']}.",
        f"- Checksum records ready: {summary['checksum_records_ready']}.",
        f"- Split-source role sidecar written: {int(bool(summary['split_source_role_sidecar_written']))}.",
        f"- Current rerun locked: {int(bool(summary['current_rerun_locked']))}.",
        f"- Source-use ready pages: {summary['source_use_ready_pages']}.",
        f"- Gutenberg Sirach gap refs: `{summary['gutenberg_sirach_gap_refs']}`.",
        f"- Gutenberg Prayer of Manasseh markers: {summary['gutenberg_manasseh_source_markers']}/{summary['gutenberg_manasseh_local_markers']}.",
        f"- Hakkaac length-drift verses: {summary['hakkaac_length_drift_verses']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Policy Options",
        "",
        "| Option | Source stream | Status | Allowed use | Blocked use | Blocker summary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in options:
        lines.append(
            f"| `{row['option_id']}` | {row['source_stream']} | `{row['status']}` | {row['allowed_use']} | {row['blocked_use']} | {row['blocker_summary']} |"
        )
    lines.extend(
        [
            "",
            "## Blockers",
            "",
            "| Blocker | Area | Status | Evidence | Required before result | Needs choice | Affects letter stream |",
            "| --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in blockers:
        lines.append(
            f"| `{row['blocker_id']}` | {row['area']} | `{row['status']}` | {row['evidence_summary']} | {row['required_before_result']} | {int(bool(row['needs_user_or_source_policy_choice']))} | {int(bool(row['affects_letter_stream']))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This packet is a blocker summary, not a decision to run KJVA results.",
            "The only policy-ready path here is current-source rerun and continued deferral of new result-bearing KJVA work.",
            "Any new independent KJVA result run still needs source-use, source-text, drift/boundary, verse-map/collation, term/control, and study-lock decisions before output.",
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
    options: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_source_policy_blocker_packet",
        "claim_boundary": "source-policy blocker packet only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "policy_option_rows": len(options),
        "blocker_rows": len(blockers),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "current_summary": str(args.current_summary),
            "gutenberg_checksum_summary": str(args.gutenberg_checksum_summary),
            "gutenberg_blocker_summary": str(args.gutenberg_blocker_summary),
            "hakkaac_decision_summary": str(args.hakkaac_decision_summary),
            "split_role_summary": str(args.split_role_summary),
        },
        "outputs": {
            "options": str(args.options_out),
            "blockers": str(args.blockers_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def option(
    option_id: str,
    source_stream: str,
    status: str,
    allowed_use: str,
    blocked_use: str,
    evidence_summary: str,
    blocker_summary: str,
    next_action: str,
) -> dict[str, Any]:
    return {
        "option_id": option_id,
        "source_stream": source_stream,
        "status": status,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use,
        "evidence_summary": evidence_summary,
        "blocker_summary": blocker_summary,
        "next_action": next_action,
        "result_boundary": "not_result_bearing",
    }


def blocker(
    blocker_id: str,
    area: str,
    status: str,
    evidence_summary: str,
    required_before_result: str,
    needs_user_or_source_policy_choice: bool,
    affects_letter_stream: bool,
) -> dict[str, Any]:
    return {
        "blocker_id": blocker_id,
        "area": area,
        "status": status,
        "evidence_summary": evidence_summary,
        "required_before_result": required_before_result,
        "needs_user_or_source_policy_choice": needs_user_or_source_policy_choice,
        "affects_letter_stream": affects_letter_stream,
        "result_boundary": "not_result_bearing",
    }


def count_status(rows: list[dict[str, Any]], status: str) -> int:
    return sum(1 for row in rows if row["status"] == status)


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
