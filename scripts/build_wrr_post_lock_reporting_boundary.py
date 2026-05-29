#!/usr/bin/env python3
"""Build the WRR post-lock reporting-boundary artifact."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_CLAIM_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_LOCKED_METHOD_REPORT = Path("reports/wrr_1994/wrr_locked_method_report.csv")
DEFAULT_DASHBOARD = Path("reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv")
DEFAULT_PRIORITY_PACKET = Path("reports/wrr_1994/wrr_exact_gap_priority_packet.csv")
DEFAULT_MANUAL_DECISION_RECORDS = Path(
    "data/study/mappings/wrr_manual_decision_records.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_post_lock_reporting_boundary.csv")
DEFAULT_MD = Path("docs/WRR_POST_LOCK_REPORTING_BOUNDARY.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_post_lock_reporting_boundary.manifest.json"
)

FIELDNAMES = ["section", "item", "status", "value", "evidence", "source"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = {
        "claim_readiness": read_rows(args.claim_readiness),
        "locked_method_report": read_rows(args.locked_method_report),
        "dashboard": read_rows(args.dashboard),
        "priority_packet": read_rows(args.priority_packet),
        "manual_decision_records": read_rows(args.manual_decision_records),
    }
    rows = build_boundary_rows(inputs, args)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, rows, inputs, args, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-readiness", type=Path, default=DEFAULT_CLAIM_READINESS)
    parser.add_argument(
        "--locked-method-report", type=Path, default=DEFAULT_LOCKED_METHOD_REPORT
    )
    parser.add_argument("--dashboard", type=Path, default=DEFAULT_DASHBOARD)
    parser.add_argument("--priority-packet", type=Path, default=DEFAULT_PRIORITY_PACKET)
    parser.add_argument(
        "--manual-decision-records",
        type=Path,
        default=DEFAULT_MANUAL_DECISION_RECORDS,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_boundary_rows(
    inputs: dict[str, list[dict[str, str]]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    readiness_rows = inputs["claim_readiness"]
    dashboard_rows = keyed(inputs["dashboard"])
    locked_rows = keyed(inputs["locked_method_report"])
    priority_rows = keyed(inputs["priority_packet"])
    manual_records = inputs["manual_decision_records"]

    ready_count = sum(1 for row in readiness_rows if row.get("ready") == "true")
    locked_report_status = locked_rows.get(("status", "report_status"), {}).get(
        "value", ""
    )
    source_cited = dashboard_rows.get(("gap", "source_cited_defined_distances"), {}).get(
        "value", ""
    )
    current_defined = dashboard_rows.get(("gap", "current_defined_distances"), {}).get(
        "value", ""
    )
    remaining_gap = dashboard_rows.get(("gap", "remaining_gap"), {}).get("value", "")
    simple_variant_residual = dashboard_rows.get(
        ("variant_upper_bound", "residual_after_simple_variants"), {}
    ).get("value", "")
    manual_counts = manual_record_counts(manual_records)
    next_boundary = priority_rows.get(
        ("priority_lane", "post-lock reporting boundary"), {}
    ).get(
        "boundary",
        "describe the residual gap as exact-reproduction work, not pending source edits",
    )

    return [
        row(
            "allowed",
            "local_locked_method_language",
            "ready",
            f"{ready_count} readiness gates ready; {locked_report_status}",
            (
                "May report the repo-defined locked local WRR method result when "
                "the exact-published caveat remains attached."
            ),
            str(args.claim_readiness),
        ),
        row(
            "not_allowed",
            "exact_published_reproduction_language",
            "forbidden",
            f"{current_defined} of {source_cited} defined; gap {remaining_gap}",
            (
                "Do not describe the local result as exact published WRR "
                "reproduction while this gap remains."
            ),
            str(args.dashboard),
        ),
        row(
            "source_boundary",
            "manual_decision_records",
            "all_current_manual_reviews_locked"
            if manual_counts["unlocked"] == 0
            else "manual_reviews_unlocked",
            (
                f"{manual_counts['locked']} locked; {manual_counts['unlocked']} unlocked; "
                f"{format_counts(manual_counts['actions'])}"
            ),
            (
                "Current manual records keep source changes separate from "
                "reporting language."
            ),
            str(args.manual_decision_records),
        ),
        row(
            "source_boundary",
            "source_changes",
            "none_selected",
            f"{manual_counts['actions'].get('no_source_change', 0)} no_source_change rows",
            "No current decision record selects a source correction or pair exclusion.",
            str(args.manual_decision_records),
        ),
        row(
            "method_boundary",
            "method_locks",
            "locked",
            f"{manual_counts['actions'].get('method_lock', 0)} method_lock rows",
            "Method-lane rows lock the current result rather than opening source edits.",
            str(args.manual_decision_records),
        ),
        row(
            "residual_gap",
            "remaining_163_distance_gap",
            "open",
            remaining_gap,
            (
                "Exact published reproduction remains caveated by the "
                "163-distance gap, not pending source-edit choices."
            ),
            str(args.dashboard),
        ),
        row(
            "residual_gap",
            "simple_variant_upper_bound_residual",
            "open",
            simple_variant_residual,
            "Simple one-edit variant leads cannot close the current gap.",
            str(args.dashboard),
        ),
        row(
            "allowed_wording",
            "local_lock",
            "allowed_with_caveat",
            (
                "locked local selected-policy result under keep_all_working_source, "
                "printed D(w), cap1000 corrected distances, and 999999 date-label permutation"
            ),
            "Always pair this with the exact-published reproduction caveat.",
            str(args.locked_method_report),
        ),
        row(
            "forbidden_wording",
            "exact_published_reproduced",
            "forbidden",
            "exact published WRR reproduced",
            "This wording is not supported by current source-defined gap evidence.",
            str(args.dashboard),
        ),
        row(
            "next_action",
            "post_lock_reporting_boundary",
            "complete",
            next_boundary,
            (
                "All current manual review rows are locked; report the residual "
                "gap as exact-reproduction work, not pending source edits."
            ),
            str(args.priority_packet),
        ),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    by_key = keyed(rows)
    allowed = by_key[("allowed", "local_locked_method_language")]
    forbidden = by_key[("not_allowed", "exact_published_reproduction_language")]
    records = by_key[("source_boundary", "manual_decision_records")]
    source_changes = by_key[("source_boundary", "source_changes")]
    method_locks = by_key[("method_boundary", "method_locks")]
    gap = by_key[("residual_gap", "remaining_163_distance_gap")]
    variant = by_key[("residual_gap", "simple_variant_upper_bound_residual")]
    lines = [
        "# WRR Post-Lock Reporting Boundary",
        "",
        "Status: post-lock reporting boundary locked.",
        "",
        "This document separates allowed local locked-method language from forbidden exact-published reproduction language.",
        "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_post_lock_reporting_boundary "
            f"--claim-readiness {args.claim_readiness} "
            f"--locked-method-report {args.locked_method_report} "
            f"--dashboard {args.dashboard} "
            f"--priority-packet {args.priority_packet} "
            f"--manual-decision-records {args.manual_decision_records} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Boundary",
        "",
        "| Boundary | Status | Value |",
        "| --- | --- | --- |",
        f"| Local locked-method result | `{allowed['status']}` | {md_cell(allowed['value'])} |",
        f"| Exact published WRR reproduction | `{forbidden['status']}` | {md_cell(forbidden['value'])} |",
        f"| Manual decision records | `{records['status']}` | {md_cell(records['value'])} |",
        f"| Source changes | `{source_changes['status']}` | {md_cell(source_changes['value'])} |",
        f"| Method locks | `{method_locks['status']}` | {md_cell(method_locks['value'])} |",
        f"| Remaining 163-distance gap | `{gap['status']}` | {md_cell(gap['value'])} |",
        f"| Simple-variant residual gap | `{variant['status']}` | {md_cell(variant['value'])} |",
        "",
        "## Allowed Wording",
        "",
        "- Local locked-method result: allowed with caveats.",
        "- It may be described as locked local selected-policy evidence under keep_all_working_source, printed D(w), cap1000 corrected distances, and a 999999 date-label permutation.",
        "- Exact published reproduction remains caveated by the 163-distance gap, not pending source-edit choices.",
        "",
        "## Forbidden Wording",
        "",
        "- Do not say exact published WRR reproduced.",
        "- Do not say the residual gap is closed.",
        "- Do not say source corrections, pair exclusions, replacement spellings, or method changes have been selected.",
        "",
        "## Cautions",
        "",
        "- This is a reporting boundary, not a new statistical result.",
        "- Current manual decision records keep 26 no_source_change rows and 11 method_lock rows.",
        "- Future source or method changes require a separate decision record before any report language changes.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    rows: list[dict[str, str]],
    inputs: dict[str, list[dict[str, str]]],
    args: argparse.Namespace,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "claim_readiness": str(args.claim_readiness),
            "locked_method_report": str(args.locked_method_report),
            "dashboard": str(args.dashboard),
            "priority_packet": str(args.priority_packet),
            "manual_decision_records": str(args.manual_decision_records),
        },
        "outputs": {
            "out": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "input_rows": {name: len(value) for name, value in inputs.items()},
        "boundary_rows": rows,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def keyed(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row.get("section", ""), row.get("item", "")): row for row in rows}


def manual_record_counts(rows: list[dict[str, str]]) -> dict[str, object]:
    statuses = Counter(row.get("decision_status", "") for row in rows)
    actions = Counter(row.get("selected_action", "") for row in rows)
    return {
        "locked": statuses.get("locked", 0),
        "unlocked": len(rows) - statuses.get("locked", 0),
        "actions": actions,
    }


def format_counts(counts: Counter[str]) -> str:
    return "; ".join(f"{key}={counts[key]}" for key in sorted(counts) if key)


def row(
    section: str,
    item: str,
    status: str,
    value: str,
    evidence: str,
    source: str,
) -> dict[str, str]:
    return {
        "section": section,
        "item": item,
        "status": status,
        "value": value,
        "evidence": evidence,
        "source": source,
    }


def md_cell(value: str) -> str:
    return str(value).replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
