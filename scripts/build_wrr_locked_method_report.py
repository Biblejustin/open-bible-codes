#!/usr/bin/env python3
"""Build a reader-facing WRR locked-method report."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_METHOD_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_LOCK_OPTIONS = Path("reports/wrr_1994/wrr_lock_options.csv")
DEFAULT_MANUAL_WORKSHEET = Path(
    "reports/wrr_1994/wrr_manual_decision_record_worksheet.csv"
)
DEFAULT_CORRECTED_DISTANCE_SUMMARY = Path(
    "reports/wrr_1994/direct_all/highcap_1000/"
    "wrr2_corrected_distance_all_lanes_merged_summary.csv"
)
DEFAULT_CORRECTED_DISTANCE_AGGREGATE = Path(
    "reports/wrr_1994/direct_all/highcap_1000/"
    "wrr2_corrected_distance_all_lanes_aggregate.csv"
)
DEFAULT_PERMUTATION_SUMMARY = Path(
    "reports/wrr_1994/cross_pair_grid/highcap_1000/"
    "wrr2_cross_pair_permutations_999999_summary.csv"
)
DEFAULT_PRIMARY_RESULT_TABLE = Path("reports/wrr_1994/wrr_primary_result_table.csv")
DEFAULT_DEFINED_PAIR_SUMMARY = Path(
    "reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv"
)
DEFAULT_OUT = Path("reports/wrr_1994/wrr_locked_method_report.csv")
DEFAULT_MD = Path("docs/WRR_LOCKED_METHOD_REPORT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_locked_method_report.manifest.json")

FIELDNAMES = ["section", "item", "value", "status", "evidence", "source"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        method_status=read_rows(args.method_status),
        readiness=read_rows(args.readiness),
        lock_options=read_rows(args.lock_options),
        manual_worksheet=read_rows(args.manual_worksheet),
        corrected_distance_summary=read_rows(args.corrected_distance_summary),
        corrected_distance_aggregate=read_rows(args.corrected_distance_aggregate),
        permutation_summary=read_rows(args.permutation_summary),
        primary_result_table=read_rows(args.primary_result_table),
        defined_pair_summary=read_rows(args.defined_pair_summary),
    )
    report_rows = build_report_rows(inputs, args)
    write_csv(args.out, report_rows)
    write_markdown(args.markdown_out, report_rows, inputs, args)
    write_manifest(args.manifest_out, report_rows, inputs, args, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


class LoadedInputs:
    def __init__(
        self,
        *,
        method_status: list[dict[str, str]],
        readiness: list[dict[str, str]],
        lock_options: list[dict[str, str]],
        manual_worksheet: list[dict[str, str]],
        corrected_distance_summary: list[dict[str, str]],
        corrected_distance_aggregate: list[dict[str, str]],
        permutation_summary: list[dict[str, str]],
        primary_result_table: list[dict[str, str]],
        defined_pair_summary: list[dict[str, str]],
    ) -> None:
        self.method_status = method_status
        self.readiness = readiness
        self.lock_options = lock_options
        self.manual_worksheet = manual_worksheet
        self.corrected_distance_summary = corrected_distance_summary
        self.corrected_distance_aggregate = corrected_distance_aggregate
        self.permutation_summary = permutation_summary
        self.primary_result_table = primary_result_table
        self.defined_pair_summary = defined_pair_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method-status", type=Path, default=DEFAULT_METHOD_STATUS)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--lock-options", type=Path, default=DEFAULT_LOCK_OPTIONS)
    parser.add_argument("--manual-worksheet", type=Path, default=DEFAULT_MANUAL_WORKSHEET)
    parser.add_argument(
        "--corrected-distance-summary",
        type=Path,
        default=DEFAULT_CORRECTED_DISTANCE_SUMMARY,
    )
    parser.add_argument(
        "--corrected-distance-aggregate",
        type=Path,
        default=DEFAULT_CORRECTED_DISTANCE_AGGREGATE,
    )
    parser.add_argument(
        "--permutation-summary",
        type=Path,
        default=DEFAULT_PERMUTATION_SUMMARY,
    )
    parser.add_argument(
        "--primary-result-table",
        type=Path,
        default=DEFAULT_PRIMARY_RESULT_TABLE,
    )
    parser.add_argument(
        "--defined-pair-summary",
        type=Path,
        default=DEFAULT_DEFINED_PAIR_SUMMARY,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_report_rows(inputs: LoadedInputs, args: argparse.Namespace) -> list[dict[str, str]]:
    method_by_area = {row.get("decision_area", ""): row for row in inputs.method_status}
    readiness_by_area = {row.get("decision_area", ""): row for row in inputs.readiness}
    lock_by_area = selected_lock_options(inputs.lock_options)
    manual_counts = manual_decision_counts(inputs.manual_worksheet)
    corrected = first(inputs.corrected_distance_summary)
    aggregate = first(inputs.corrected_distance_aggregate)
    permutation = first(inputs.permutation_summary)
    published_g = first(
        [row for row in inputs.primary_result_table if row.get("label") == "G"]
        or inputs.primary_result_table
    )
    defined_all_lanes = first(
        [
            row
            for row in inputs.defined_pair_summary
            if row.get("run_label") == "all_lanes_cap1000"
        ]
        or inputs.defined_pair_summary
    )

    rows = [
        summary_row(
            "status",
            "report_status",
            "locked local WRR method report; not an exact published WRR reproduction",
            "locked_local_not_exact_reproduction",
            "Selected local policy is locked while exact published reproduction remains caveated.",
            str(args.method_status),
        ),
        summary_row(
            "lock",
            "Pair universe",
            "keep_all_working_source",
            method_by_area.get("Pair universe", {}).get("status", ""),
            lock_by_area.get("Pair universe", {}).get("evidence", ""),
            str(args.lock_options),
        ),
        summary_row(
            "lock",
            "D(w)",
            "printed WRR formula main; reported-program formula sensitivity",
            method_by_area.get("D(w) skip-cap formula", {}).get("status", ""),
            lock_by_area.get("D(w) skip-cap formula", {}).get("evidence", ""),
            str(args.lock_options),
        ),
        summary_row(
            "lock",
            "corrected_distance",
            "full selected universe cap1000; undefined ordinary-not-valid",
            method_by_area.get("Corrected distance c(w,w')", {}).get("status", ""),
            method_by_area.get("Corrected distance c(w,w')", {}).get("evidence", ""),
            str(args.corrected_distance_summary),
        ),
        summary_row(
            "lock",
            "Permutation",
            "999,999 date-label shuffles",
            method_by_area.get("Aggregate statistic and permutation", {}).get("status", ""),
            lock_by_area.get("Permutation", {}).get("evidence", ""),
            str(args.permutation_summary),
        ),
        summary_row(
            "lock",
            "Manual decisions",
            manual_decision_summary(manual_counts),
            "locked",
            "Manual worksheet rows counted by selected action.",
            str(args.manual_worksheet),
        ),
        summary_row(
            "local_result",
            "observed_rows",
            corrected.get("pairs", permutation.get("observed_rows", aggregate.get("rows", ""))),
            corrected.get("status", aggregate.get("status", "")),
            "Selected keep_all_working_source corrected-distance rows.",
            str(args.corrected_distance_summary),
        ),
        summary_row(
            "local_result",
            "defined_c_values",
            corrected.get(
                "defined_corrected_distances",
                permutation.get("observed_defined_corrected_distances", ""),
            ),
            corrected.get("status", aggregate.get("status", "")),
            "Defined corrected-distance values available to the aggregate statistic.",
            str(args.corrected_distance_summary),
        ),
        summary_row(
            "local_result",
            "ordinary_not_valid",
            corrected.get("ordinary_not_valid_pairs", aggregate.get("undefined_rows", "")),
            corrected.get("status", aggregate.get("status", "")),
            "Undefined rows are ordinary-not-valid, not missing work.",
            str(args.corrected_distance_summary),
        ),
        summary_row(
            "local_result",
            "P-values",
            (
                f"P1={aggregate.get('p1', '')}; P2={aggregate.get('p2', '')}; "
                f"P3={aggregate.get('p3', '')}; P4={aggregate.get('p4', '')}"
            ),
            aggregate.get("status", ""),
            "Aggregate statistic over local defined c-values.",
            str(args.corrected_distance_aggregate),
        ),
        summary_row(
            "local_result",
            "rho_values",
            (
                f"rho P1={permutation.get('rho_p1', '')}; "
                f"rho P2={permutation.get('rho_p2', '')}; "
                f"rho P3={permutation.get('rho_p3', '')}; "
                f"rho P4={permutation.get('rho_p4', '')}; "
                f"rho0={permutation.get('rho0_bonferroni', '')}"
            ),
            permutation.get("status", ""),
            "999,999 date-label permutation summary.",
            str(args.permutation_summary),
        ),
        summary_row(
            "published_anchor",
            "Table 3 Genesis",
            (
                f"min statistic {published_g.get('min_statistic', '')}; "
                f"rank {published_g.get('min_rank', '')}; "
                f"p0={published_g.get('bonferroni_p0', '')}"
            ),
            published_g.get("status", ""),
            "Published result anchor from primary PDF table extraction.",
            str(args.primary_result_table),
        ),
        summary_row(
            "boundary",
            "source_defined_gap",
            (
                f"defined {defined_all_lanes.get('defined', '')} of "
                f"{defined_all_lanes.get('source_cited_defined_distances', '')}; "
                f"gap {defined_all_lanes.get('defined_gap_to_source_cited', '')}"
            ),
            defined_all_lanes.get("status", ""),
            "Exact published WRR reproduction remains caveated by this gap.",
            str(args.defined_pair_summary),
        ),
    ]

    for area in [
        "Pair universe",
        "D(w) skip-cap formula",
        "Corrected distance c(w,w')",
        "Aggregate statistic and permutation",
    ]:
        readiness_row = readiness_by_area.get(area, {})
        rows.append(
            summary_row(
                "readiness_gate",
                area,
                readiness_row.get("ready", ""),
                readiness_row.get("status", ""),
                readiness_row.get("current_read", ""),
                str(args.readiness),
            )
        )
    return rows


def selected_lock_options(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    selected: dict[str, dict[str, str]] = {}
    for row in rows:
        area = row.get("area", "")
        status = row.get("status", "")
        if status.startswith("selected") or status.startswith("source_locked"):
            selected[area] = row
        if status.startswith("locked"):
            selected[area] = row
    return selected


def manual_decision_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row.get("record_selected_action", "") for row in rows)


def manual_decision_summary(counts: Counter[str]) -> str:
    total = sum(counts.values())
    no_source = counts.get("no_source_change", 0)
    method_lock = counts.get("method_lock", 0)
    return f"{total} locked rows: {no_source} no_source_change; {method_lock} method_lock"


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    inputs: LoadedInputs,
    args: argparse.Namespace,
) -> None:
    values = {(row["section"], row["item"]): row for row in rows}
    corrected = first(inputs.corrected_distance_summary)
    aggregate = first(inputs.corrected_distance_aggregate)
    permutation = first(inputs.permutation_summary)
    boundary = values[("boundary", "source_defined_gap")]
    manual = values[("lock", "Manual decisions")]
    published = values[("published_anchor", "Table 3 Genesis")]
    lines = [
        "# WRR Locked Method Report",
        "",
        "Status: locked local WRR method report; not an exact published WRR reproduction.",
        "",
        "This report is the compact handoff for the selected local WRR policy. It",
        "records what is locked, what the selected-policy run reports, and where",
        "exact published WRR reproduction remains outside the current evidence.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_locked_method_report "
            f"--method-status {args.method_status} "
            f"--readiness {args.readiness} "
            f"--lock-options {args.lock_options} "
            f"--manual-worksheet {args.manual_worksheet} "
            f"--corrected-distance-summary {args.corrected_distance_summary} "
            f"--corrected-distance-aggregate {args.corrected_distance_aggregate} "
            f"--permutation-summary {args.permutation_summary} "
            f"--primary-result-table {args.primary_result_table} "
            f"--defined-pair-summary {args.defined_pair_summary} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Selected Locks",
        "",
        "| Lock | Status | Evidence |",
        "| --- | --- | --- |",
        lock_line(values, "Pair universe", "Pair universe: keep_all_working_source"),
        lock_line(values, "D(w)", "D(w): printed WRR formula main; reported-program formula sensitivity"),
        lock_line(
            values,
            "corrected_distance",
            "Corrected distance: full selected universe cap1000; undefined ordinary-not-valid",
        ),
        lock_line(values, "Permutation", "Permutation: 999,999 date-label shuffles"),
        (
            f"| Manual decisions: {manual['value']} | `{manual['status']}` | "
            f"{markdown_cell(manual['evidence'])} |"
        ),
        "",
        "## Main Local Result",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Observed rows | {markdown_cell(corrected.get('pairs', ''))} |",
        f"| Defined c-values | {markdown_cell(corrected.get('defined_corrected_distances', ''))} |",
        f"| Ordinary-not-valid rows | {markdown_cell(corrected.get('ordinary_not_valid_pairs', ''))} |",
        f"| P1 | {markdown_cell(aggregate.get('p1', ''))} |",
        f"| P2 | {markdown_cell(aggregate.get('p2', ''))} |",
        f"| P3 | {markdown_cell(aggregate.get('p3', ''))} |",
        f"| P4 | {markdown_cell(aggregate.get('p4', ''))} |",
        f"| rho P1 | {markdown_cell(permutation.get('rho_p1', ''))} |",
        f"| rho P2 | {markdown_cell(permutation.get('rho_p2', ''))} |",
        f"| rho P3 | {markdown_cell(permutation.get('rho_p3', ''))} |",
        f"| rho P4 | {markdown_cell(permutation.get('rho_p4', ''))} |",
        f"| rho0 | {markdown_cell(permutation.get('rho0_bonferroni', ''))} |",
        "",
        "## Published Anchor",
        "",
        f"- Primary Table 3 Genesis anchor: {published['value']}.",
        "- This anchor is shown for comparison only. The local selected-policy run is not an exact published WRR reproduction.",
        "",
        "## Exact Published WRR Boundary",
        "",
        "- Exact published WRR reproduction remains caveated by the source-defined 163-distance gap and primary-source transcription limits.",
        f"- Current source-defined gap: {boundary['value']}.",
        "- Source-review and visual-review flags remain diagnostic unless a separate manual source-policy record changes them.",
        "- Do not describe this as an exact published WRR reproduction.",
        "",
        "## Allowed Language",
        "",
        "- Locked local WRR method report under keep_all_working_source.",
        "- Repo-defined selected-policy result with printed D(w) as main and reported-program D(w) as sensitivity.",
        "- Exact published WRR reproduction remains caveated.",
        "",
        "## Forbidden Language",
        "",
        "- exact published WRR reproduced",
        "- proves WRR",
        "- source correction selected",
        "",
        "## Readiness Gate",
        "",
        "| Area | Ready | Status | Read |",
        "| --- | --- | --- | --- |",
    ]
    for row in [r for r in rows if r["section"] == "readiness_gate"]:
        lines.append(
            "| {item} | `{value}` | `{status}` | {evidence} |".format(
                item=markdown_cell(row["item"]),
                value=markdown_cell(row["value"]),
                status=markdown_cell(row["status"]),
                evidence=markdown_cell(row["evidence"]),
            )
        )
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def lock_line(
    values: dict[tuple[str, str], dict[str, str]], item: str, label: str
) -> str:
    row = values[("lock", item)]
    return "| {label} | `{status}` | {evidence} |".format(
        label=markdown_cell(label),
        status=markdown_cell(row["status"]),
        evidence=markdown_cell(row["evidence"]),
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    rows: list[dict[str, str]],
    inputs: LoadedInputs,
    args: argparse.Namespace,
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_locked_method_report",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "report_rows": len(rows),
        "method_status_rows": len(inputs.method_status),
        "readiness_rows": len(inputs.readiness),
        "lock_option_rows": len(inputs.lock_options),
        "manual_decision_rows": len(inputs.manual_worksheet),
        "inputs": {
            "method_status": str(args.method_status),
            "readiness": str(args.readiness),
            "lock_options": str(args.lock_options),
            "manual_worksheet": str(args.manual_worksheet),
            "corrected_distance_summary": str(args.corrected_distance_summary),
            "corrected_distance_aggregate": str(args.corrected_distance_aggregate),
            "permutation_summary": str(args.permutation_summary),
            "primary_result_table": str(args.primary_result_table),
            "defined_pair_summary": str(args.defined_pair_summary),
        },
        "outputs": {
            "out": str(args.out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def summary_row(
    section: str,
    item: str,
    value: str,
    status: str,
    evidence: str,
    source: str,
) -> dict[str, str]:
    return {
        "section": section,
        "item": item,
        "value": value,
        "status": status,
        "evidence": evidence,
        "source": source,
    }


def first(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
