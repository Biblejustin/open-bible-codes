#!/usr/bin/env python3
"""Build a WRR claim-blocker packet from current readiness artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_LOCK_OPTIONS = Path("reports/wrr_1994/wrr_lock_options.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_METHOD_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_SOURCE_POLICY_SCENARIOS = Path("reports/wrr_1994/wrr_source_policy_scenarios.csv")
DEFAULT_SOURCE_POLICY_TERM_IMPACTS = Path(
    "reports/wrr_1994/wrr_source_policy_term_impacts.csv"
)
DEFAULT_DW_FORMULA_SENSITIVITY = Path("reports/wrr_1994/wrr_dw_formula_sensitivity.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_claim_blocker_packet.csv")
DEFAULT_MD = Path("docs/WRR_CLAIM_BLOCKER_PACKET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_claim_blocker_packet.manifest.json")

FIELDNAMES = [
    "decision_area",
    "current_status",
    "ready",
    "blocker",
    "current_read",
    "available_options",
    "source_review_flags",
    "no_input_next",
    "input_needed",
]


INPUT_NEEDED = {
    "Pair universe": "source policy selected: keep_all_working_source",
    "D(w) skip-cap formula": "formula selected: printed WRR formula main; program sensitivity",
    "Corrected distance c(w,w')": "run full corrected-distance over keep_all_working_source with printed D(w)",
    "Aggregate statistic and permutation": "lock aggregate/permutation procedure over full corrected-distance output",
}

NO_INPUT_NEXT = {
    "Pair universe": (
        "continue with all imported same-record pairs; source-review and visual "
        "flags remain review notes only"
    ),
    "D(w) skip-cap formula": (
        "use printed D(w) as the main formula and keep reported-program D(w) "
        "visible as sensitivity"
    ),
    "Corrected distance c(w,w')": (
        "run full-lane corrected-distance work under the selected source and D(w) locks"
    ),
    "Aggregate statistic and permutation": (
        "keep date-label permutation diagnostics separate from WRR reproduction "
        "language"
    ),
}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    readiness_rows = read_rows(args.readiness)
    lock_rows = read_rows(args.lock_options)
    source_rows = read_rows(args.source_queue)
    method_rows = read_rows(args.method_status)
    source_policy_rows = read_optional_rows(args.source_policy_scenarios)
    source_policy_term_rows = read_optional_rows(args.source_policy_term_impacts)
    dw_formula_rows = read_optional_rows(args.dw_formula_sensitivity)
    packet_rows = build_packet_rows(readiness_rows, lock_rows, source_rows, method_rows)
    write_csv(args.out, packet_rows)
    write_markdown(
        args.markdown_out,
        packet_rows,
        source_rows,
        source_policy_rows,
        source_policy_term_rows,
        dw_formula_rows,
        args,
    )
    write_manifest(
        args.manifest_out,
        args,
        packet_rows,
        source_policy_rows,
        source_policy_term_rows,
        dw_formula_rows,
        started,
    )
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--lock-options", type=Path, default=DEFAULT_LOCK_OPTIONS)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--method-status", type=Path, default=DEFAULT_METHOD_STATUS)
    parser.add_argument(
        "--source-policy-scenarios",
        type=Path,
        default=DEFAULT_SOURCE_POLICY_SCENARIOS,
    )
    parser.add_argument(
        "--source-policy-term-impacts",
        type=Path,
        default=DEFAULT_SOURCE_POLICY_TERM_IMPACTS,
    )
    parser.add_argument(
        "--dw-formula-sensitivity",
        type=Path,
        default=DEFAULT_DW_FORMULA_SENSITIVITY,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    readiness_rows: list[dict[str, str]],
    lock_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    method_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    options_by_area = group_lock_options(lock_rows)
    method_by_area = {row.get("decision_area", ""): row for row in method_rows}
    source_flags = source_flag_summary(source_rows)
    out = []
    for row in readiness_rows:
        area = row.get("decision_area", "")
        if row.get("ready", "") == "true":
            continue
        out.append(
            {
                "decision_area": area,
                "current_status": row.get("status", ""),
                "ready": row.get("ready", ""),
                "blocker": row.get("blocker", ""),
                "current_read": method_by_area.get(area, {}).get("current_read", ""),
                "available_options": options_by_area.get(area, ""),
                "source_review_flags": source_flags if area == "Pair universe" else "",
                "no_input_next": NO_INPUT_NEXT.get(area, ""),
                "input_needed": INPUT_NEEDED.get(area, ""),
            }
        )
    return out


def group_lock_options(rows: list[dict[str, str]]) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for row in rows:
        area = row.get("area", "")
        if not area:
            continue
        grouped.setdefault(area, []).append(
            f"{row.get('option', '')} [{row.get('status', '')}]"
        )
    return {area: "; ".join(options) for area, options in grouped.items()}


def source_flag_summary(rows: list[dict[str, str]]) -> str:
    counter = Counter(
        flag
        for row in rows
        for flag in row.get("source_review_flags", "").split(";")
        if flag
    )
    if not counter:
        return ""
    total = sum(counter.values())
    parts = ", ".join(f"{counter[flag]} {flag}" for flag in sorted(counter))
    return f"{total} flagged queued terms: {parts}"


def flagged_source_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flagged = [row for row in rows if row.get("source_review_flags")]
    return sorted(flagged, key=lambda row: int_or_zero(row.get("priority_rank", "")))


def visual_source_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    visual = [row for row in rows if row.get("visual_review_note")]
    return sorted(visual, key=lambda row: int_or_zero(row.get("priority_rank", "")))


def write_markdown(
    path: Path,
    packet_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    source_policy_rows: list[dict[str, str]],
    source_policy_term_rows: list[dict[str, str]],
    dw_formula_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR Claim Blocker Packet",
        "",
        "Status: full corrected-distance run selected; aggregate/permutation still not claim-grade.",
        "",
        "This packet records the selected WRR working policy and gathers the",
        "remaining claim-readiness blockers, current lock options, WNP/context source",
        "queue flags, and visual triage notes into one handoff artifact.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_claim_blocker_packet "
            f"--readiness {args.readiness} "
            f"--lock-options {args.lock_options} "
            f"--source-queue {args.source_queue} "
            f"--method-status {args.method_status} "
            f"--source-policy-scenarios {args.source_policy_scenarios} "
            f"--source-policy-term-impacts {args.source_policy_term_impacts} "
            f"--dw-formula-sensitivity {args.dw_formula_sensitivity} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Blockers",
        "",
        "| Area | Status | Blocker | Input needed |",
        "| --- | --- | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            "| {area} | `{status}` | {blocker} | {input_needed} |".format(
                area=markdown_cell(row["decision_area"]),
                status=markdown_cell(row["current_status"]),
                blocker=markdown_cell(row["blocker"]),
                input_needed=markdown_cell(row["input_needed"]),
            )
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "| Area | Current read | Available options | No-input next |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in packet_rows:
        lines.append(
            "| {area} | {current_read} | {options} | {no_input_next} |".format(
                area=markdown_cell(row["decision_area"]),
                current_read=markdown_cell(row["current_read"]),
                options=markdown_cell(row["available_options"]),
                no_input_next=markdown_cell(row["no_input_next"]),
            )
        )
    if source_policy_rows:
        lines.extend(
            [
                "",
                "## Source Policy Scenario Impact",
                "",
                "| Scenario | Type | Excluded pairs | Remaining >=5 | Gap >=5 vs 163 | Remaining 5..8 |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in source_policy_rows:
            lines.append(
                (
                    "| {scenario} | `{policy_type}` | {excluded} | "
                    "{remaining_app} | {gap_app} | {remaining_len} |"
                ).format(
                    scenario=markdown_cell(row.get("scenario", "")),
                    policy_type=markdown_cell(row.get("policy_type", "")),
                    excluded=markdown_cell(row.get("excluded_pairs", "")),
                    remaining_app=markdown_cell(
                        row.get("remaining_appellation_min_length_pairs", "")
                    ),
                    gap_app=markdown_cell(
                        row.get("gap_to_source_cited_163_after_appellation_min_length", "")
                    ),
                    remaining_len=markdown_cell(row.get("remaining_length_filtered_pairs", "")),
                )
            )
    closing_term_rows = [
        row
        for row in source_policy_term_rows
        if row.get("closes_appellation_min_length_gap_to_163", "").lower() == "true"
    ]
    if closing_term_rows:
        lines.extend(
            [
                "",
                "## Single-Term Source Policy Impact",
                "",
                "| Term id | Term | Flags | Affected >=5 pairs | Remaining >=5 | Gap >=5 vs 163 | Read |",
                "| --- | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for row in closing_term_rows:
            lines.append(
                (
                    "| {term_id} | {term} | {flags} | {affected_app} | "
                    "{remaining_app} | {gap_app} | {read} |"
                ).format(
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    flags=markdown_cell(row.get("flags", "")),
                    affected_app=markdown_cell(
                        row.get("affected_appellation_min_length_pairs", "")
                    ),
                    remaining_app=markdown_cell(
                        row.get(
                            "remaining_appellation_min_length_pairs_if_excluded",
                            "",
                        )
                    ),
                    gap_app=markdown_cell(
                        row.get(
                            "gap_to_source_cited_163_after_appellation_min_length_if_excluded",
                            "",
                        )
                    ),
                    read=markdown_cell(row.get("diagnostic_read", "")),
                )
            )
    if dw_formula_rows:
        lines.extend(
            [
                "",
                "## D(w) Formula Sensitivity",
                "",
                "| Scope | Rows | Printed defined | Program defined | Changed pairs | Read |",
                "| --- | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for row in dw_formula_rows:
            lines.append(
                (
                    "| {scope} | {rows} | {printed} | "
                    "{program} | {changed} | {read} |"
                ).format(
                    scope=markdown_cell(row.get("scope", "")),
                    rows=markdown_cell(row.get("row_count", "")),
                    printed=markdown_cell(row.get("printed_defined_corrected_distances", "")),
                    program=markdown_cell(row.get("program_defined_corrected_distances", "")),
                    changed=markdown_cell(row.get("changed_pairs", "")),
                    read=markdown_cell(row.get("diagnostic_read", "")),
                )
            )
    flagged_rows = flagged_source_rows(source_rows)
    visual_rows = visual_source_rows(source_rows)
    if visual_rows:
        lines.extend(
            [
                "",
                "## Visual Triage Highlights",
                "",
                "| Rank | Term id | Note | Action |",
                "| ---: | --- | --- | --- |",
            ]
        )
        for row in visual_rows:
            lines.append(
                "| {rank} | `{term_id}` | {note} | {action} |".format(
                    rank=markdown_cell(row.get("priority_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    note=markdown_cell(row.get("visual_review_note", "")),
                    action=markdown_cell(row.get("visual_review_action", "")),
                )
            )
    if flagged_rows:
        lines.extend(
            [
                "",
                "## Flagged Source-Review Rows",
                "",
                "| Rank | Term id | Term | Bucket | Flags | Action |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in flagged_rows:
            lines.append(
                "| {rank} | `{term_id}` | `{term}` | `{bucket}` | `{flags}` | {action} |".format(
                    rank=markdown_cell(row.get("priority_rank", "")),
                    term_id=markdown_cell(row.get("term_id", "")),
                    term=markdown_cell(row.get("term", "")),
                    bucket=markdown_cell(row.get("review_bucket", "")),
                    flags=markdown_cell(row.get("source_review_flags", "")),
                    action=markdown_cell(row.get("source_review_action", "")),
                )
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a decision packet, not a reproduction result.",
            "- Pair universe lock: keep_all_working_source; WNP/context and visual-review flags do not exclude pairs automatically.",
            "- D(w) lock: printed WRR formula main; reported-program formula remains sensitivity output.",
            "- No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_optional_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    source_policy_rows: list[dict[str, str]],
    source_policy_term_rows: list[dict[str, str]],
    dw_formula_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_claim_blocker_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "blocker_rows": len(rows),
        "source_policy_scenario_rows": len(source_policy_rows),
        "source_policy_term_impact_rows": len(source_policy_term_rows),
        "dw_formula_sensitivity_rows": len(dw_formula_rows),
        "inputs": {
            "readiness": str(args.readiness),
            "lock_options": str(args.lock_options),
            "source_queue": str(args.source_queue),
            "method_status": str(args.method_status),
            "source_policy_scenarios": str(args.source_policy_scenarios),
            "source_policy_term_impacts": str(args.source_policy_term_impacts),
            "dw_formula_sensitivity": str(args.dw_formula_sensitivity),
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


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
