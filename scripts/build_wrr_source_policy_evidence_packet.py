#!/usr/bin/env python3
"""Build source-policy evidence packet for WRR residual action targets."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_ACTION_PLAN = Path("reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_ROW_OCR = Path("reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv")
DEFAULT_SCENARIO_PAIRS = Path("reports/wrr_1994/wrr_source_policy_scenario_pairs.csv")
DEFAULT_TABLE2_BRIDGE = Path("reports/wrr_1994/wrr_table2_source_bridge.csv")
DEFAULT_WNP_HTML = Path("reports/wrr_1994/wnp_en.html")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_policy_evidence_packet.csv")
DEFAULT_SOURCE_CONTEXT_OUT = Path(
    "reports/wrr_1994/wrr_source_policy_evidence_context.csv"
)
DEFAULT_SUMMARY_OUT = Path(
    "reports/wrr_1994/wrr_source_policy_evidence_summary.csv"
)
DEFAULT_MD = Path("docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md")
DEFAULT_MANIFEST = Path(
    "reports/wrr_1994/wrr_source_policy_evidence_packet.manifest.json"
)

EVIDENCE_FIELDNAMES = [
    "run_label",
    "evidence_rank",
    "term_id",
    "term",
    "concept",
    "source_flags",
    "residual_pairs",
    "frontier_pairs",
    "related_source_term_ids",
    "related_source_terms",
    "row_ocr_matched_terms",
    "row_ocr_not_matched_related_terms",
    "scenario_pair_statuses",
    "wnp_evidence_refs",
    "table2_bridge_read",
    "decision_boundary",
    "evidence_read",
]

SOURCE_CONTEXT_FIELDNAMES = [
    "context_id",
    "source_flag",
    "source_ref",
    "source_terms",
    "read",
    "decision_boundary",
]

SUMMARY_FIELDNAMES = [
    "run_label",
    "priority_source_policy_terms",
    "related_source_review_rows",
    "related_scenario_pair_rows",
    "wnp_context_blocks",
    "decision_boundary",
    "read",
]

SOURCE_POLICY_LANE = "source_policy_or_pair_rule_review"
CHELM_FLAG = "wnp_chelm_spelling_context"
DIAGNOSTIC_BOUNDARY = (
    "No automatic correction or exclusion; source-policy targets need citable "
    "pair-rule evidence before changing the working source."
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    action_rows = read_rows(args.action_plan)
    source_rows = read_rows(args.source_queue)
    row_ocr_rows = read_rows(args.row_ocr)
    scenario_pair_rows = read_rows(args.scenario_pairs)
    table2_bridge_rows = read_rows(args.table2_bridge)
    source_context_rows = build_source_context_rows(args.wnp_html)
    evidence_rows = build_evidence_rows(
        action_rows,
        source_rows,
        row_ocr_rows,
        scenario_pair_rows,
        table2_bridge_rows,
        source_context_rows,
    )
    summary_rows = build_summary_rows(evidence_rows, source_rows, scenario_pair_rows, source_context_rows)
    write_csv(args.out, EVIDENCE_FIELDNAMES, evidence_rows)
    write_csv(args.source_context_out, SOURCE_CONTEXT_FIELDNAMES, source_context_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, evidence_rows, source_rows, row_ocr_rows, scenario_pair_rows, source_context_rows, summary_rows, args)
    write_manifest(
        args.manifest_out,
        args,
        evidence_rows,
        source_context_rows,
        summary_rows,
        started,
    )
    print(args.out)
    print(args.source_context_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--action-plan", type=Path, default=DEFAULT_ACTION_PLAN)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument("--row-ocr", type=Path, default=DEFAULT_ROW_OCR)
    parser.add_argument("--scenario-pairs", type=Path, default=DEFAULT_SCENARIO_PAIRS)
    parser.add_argument("--table2-bridge", type=Path, default=DEFAULT_TABLE2_BRIDGE)
    parser.add_argument("--wnp-html", type=Path, default=DEFAULT_WNP_HTML)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--source-context-out", type=Path, default=DEFAULT_SOURCE_CONTEXT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_evidence_rows(
    action_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    row_ocr_rows: list[dict[str, str]],
    scenario_pair_rows: list[dict[str, str]],
    table2_bridge_rows: list[dict[str, str]],
    source_context_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    source_by_term = {row.get("term_id", ""): row for row in source_rows}
    rows = []
    for action_row in action_rows:
        if action_row.get("action_lane") != SOURCE_POLICY_LANE:
            continue
        term_id = action_row.get("term_id", "")
        source_row = source_by_term.get(term_id, {})
        concept = source_row.get("concepts", "") or concept_from_pair_ids(
            action_row.get("pair_ids", "")
        )
        source_flags = action_row.get("source_flags", "") or source_row.get(
            "source_review_flags", ""
        )
        related_source_rows = related_source_queue_rows(source_rows, concept, source_flags)
        related_ids = {row.get("term_id", "") for row in related_source_rows}
        concept_ocr_rows = [row for row in row_ocr_rows if row.get("concept") == concept]
        scenario_rows = related_scenario_rows(scenario_pair_rows, related_ids, concept, source_flags)
        rows.append(
            {
                "run_label": action_row.get("run_label", ""),
                "evidence_rank": 0,
                "term_id": term_id,
                "term": action_row.get("term", ""),
                "concept": concept,
                "source_flags": source_flags,
                "residual_pairs": int_or_zero(action_row.get("residual_pairs", "")),
                "frontier_pairs": int_or_zero(action_row.get("frontier_pairs", "")),
                "related_source_term_ids": join_nonempty(
                    row.get("term_id", "") for row in related_source_rows
                ),
                "related_source_terms": join_nonempty(
                    f"{row.get('term_id', '')} {row.get('term', '')}"
                    for row in related_source_rows
                ),
                "row_ocr_matched_terms": row_ocr_terms(concept_ocr_rows, "matched"),
                "row_ocr_not_matched_related_terms": row_ocr_terms(
                    [
                        row
                        for row in concept_ocr_rows
                        if row.get("term_id") in related_ids
                    ],
                    "not_matched",
                ),
                "scenario_pair_statuses": scenario_statuses(scenario_rows),
                "wnp_evidence_refs": join_nonempty(
                    row.get("source_ref", "")
                    for row in source_context_rows
                    if row.get("source_flag") in split_flags(source_flags)
                ),
                "table2_bridge_read": table2_bridge_read(table2_bridge_rows, concept),
                "decision_boundary": DIAGNOSTIC_BOUNDARY,
                "evidence_read": evidence_read(source_flags, term_id),
            }
        )
    rows.sort(key=lambda row: (str(row["source_flags"]), str(row["term_id"])))
    for index, row in enumerate(rows, start=1):
        row["evidence_rank"] = index
    return rows


def build_source_context_rows(wnp_html: Path) -> list[dict[str, str]]:
    if not wnp_html.exists():
        return []
    lines = wnp_html.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = [
        (
            "wnp_chelm_spelling_argument",
            608,
            619,
            "clma; cilma; wlmh clma; wlmh cilma",
            (
                "WNP discusses Chelma spellings and says the practical additions are "
                "cilma and wlmh clma under the 5-8 letter filter."
            ),
        ),
        (
            "wnp_chelm_appellation_table",
            931,
            935,
            "rby wlmh; cilma; wlmh clma",
            "WNP table context lists row 32 with rby wlmh plus cilma and wlmh clma.",
        ),
        (
            "wnp_chelm_bibliography_context",
            1052,
            1054,
            "r' wlmh cilma; mrkbt hmwnh",
            "WNP bibliography context cites a Brik biography title using wlmh cilma.",
        ),
    ]
    rows = []
    for context_id, start, end, source_terms, read in blocks:
        if line_range_present(lines, start, end):
            rows.append(
                {
                    "context_id": context_id,
                    "source_flag": CHELM_FLAG,
                    "source_ref": f"{wnp_html}:{start}-{end}",
                    "source_terms": source_terms,
                    "read": read,
                    "decision_boundary": DIAGNOSTIC_BOUNDARY,
                }
            )
    return rows


def build_summary_rows(
    evidence_rows: list[dict[str, object]],
    source_rows: list[dict[str, str]],
    scenario_pair_rows: list[dict[str, str]],
    source_context_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    if not evidence_rows:
        return []
    related_ids: set[str] = set()
    concepts: set[str] = set()
    flags: set[str] = set()
    for row in evidence_rows:
        related_ids.update(split_semicolon(str(row.get("related_source_term_ids", ""))))
        concepts.add(str(row.get("concept", "")))
        flags.update(split_flags(str(row.get("source_flags", ""))))
    related_source_count = sum(
        1 for row in source_rows if row.get("term_id", "") in related_ids
    )
    related_scenario_count = sum(
        1
        for row in scenario_pair_rows
        if row.get("concept", "") in concepts
        and split_flags(row.get("source_review_flags", "")) & flags
    )
    return [
        {
            "run_label": str(evidence_rows[0].get("run_label", "")),
            "priority_source_policy_terms": len(evidence_rows),
            "related_source_review_rows": related_source_count,
            "related_scenario_pair_rows": related_scenario_count,
            "wnp_context_blocks": len(source_context_rows),
            "decision_boundary": DIAGNOSTIC_BOUNDARY,
            "read": (
                "source-policy residual is now tied to local WNP context, row OCR, "
                "and diagnostic scenario status without changing the working source"
            ),
        }
    ]


def write_markdown(
    path: Path,
    evidence_rows: list[dict[str, object]],
    source_rows: list[dict[str, str]],
    row_ocr_rows: list[dict[str, str]],
    scenario_pair_rows: list[dict[str, str]],
    source_context_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary = summary_rows[0] if summary_rows else {}
    related_ids = split_semicolon(
        ";".join(str(row.get("related_source_term_ids", "")) for row in evidence_rows)
    )
    concepts = {str(row.get("concept", "")) for row in evidence_rows}
    flags = set().union(
        *(split_flags(str(row.get("source_flags", ""))) for row in evidence_rows)
    ) if evidence_rows else set()
    related_source_rows = [
        row for row in source_rows if row.get("term_id", "") in set(related_ids)
    ]
    concept_ocr_rows = [row for row in row_ocr_rows if row.get("concept", "") in concepts]
    related_scenario_rows_for_doc = [
        row
        for row in scenario_pair_rows
        if row.get("concept", "") in concepts
        and split_flags(row.get("source_review_flags", "")) & flags
    ]
    lines = [
        "# WRR Source-Policy Evidence Packet",
        "",
        "Status: diagnostic evidence packet for source-policy residual terms.",
        "It does not choose a source correction, exclude a pair, or lock a replacement.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_policy_evidence_packet "
            f"--action-plan {args.action_plan} "
            f"--source-queue {args.source_queue} "
            f"--row-ocr {args.row_ocr} "
            f"--scenario-pairs {args.scenario_pairs} "
            f"--table2-bridge {args.table2_bridge} "
            f"--wnp-html {args.wnp_html} "
            f"--out {args.out} "
            f"--source-context-out {args.source_context_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Priority source-policy terms: {summary.get('priority_source_policy_terms', 0)}.",
        f"- Related source-review rows: {summary.get('related_source_review_rows', 0)}.",
        f"- Related scenario-pair rows: {summary.get('related_scenario_pair_rows', 0)}.",
        f"- WNP context blocks: {summary.get('wnp_context_blocks', 0)}.",
        f"- Boundary: {DIAGNOSTIC_BOUNDARY}",
        "",
        "## Priority Source-Policy Targets",
        "",
        "| Rank | Term id | Term | Concept | Source flags | Residual pairs | Frontier pairs | Evidence read |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for row in evidence_rows:
        lines.append(
            "| {evidence_rank} | `{term_id}` | `{term}` | `{concept}` | `{source_flags}` | "
            "{residual_pairs} | {frontier_pairs} | {evidence_read} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Related Source-Queue Context",
            "",
            "| Term id | Term | OCR status | Variant hits | Source action | Visual action |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in sorted(related_source_rows, key=lambda row: row.get("term_id", "")):
        lines.append(
            "| `{term_id}` | `{term}` | {row_ocr_status} | {best_variant_hit_count} | {source_review_action} | {visual_review_action} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Row OCR Context",
            "",
            "| Term id | Term | Category | OCR status | Column OCR read |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(concept_ocr_rows, key=lambda row: row.get("term_id", "")):
        lines.append(
            "| `{term_id}` | `{michigan_term}` | {category} | {row_ocr_status} | `{row_ocr_text_normalized}` |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Local WNP Context",
            "",
            "| Context | Source ref | Source terms | Read |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in source_context_rows:
        lines.append(
            "| `{context_id}` | `{source_ref}` | `{source_terms}` | {read} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Scenario Status",
            "",
            "| Scenario | Pair id | Action | Review status | Candidate lane |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in related_scenario_rows_for_doc:
        lines.append(
            "| `{scenario}` | `{pair_id}` | {scenario_action} | {pair_review_status} | {candidate_lane} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## No-Input Boundary",
            "",
            "- No automatic correction or exclusion comes from this packet.",
            "- Row OCR supports the visible Rabbi Shelomo baseline and date in this pass; it does not lock the Chełm forms.",
            "- WNP context supports why the Chełm forms are in review scope, not a final pair-rule decision.",
            "- Keep the working source unchanged until source/pair-rule review is citable enough to lock.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    evidence_rows: list[dict[str, object]],
    source_context_rows: list[dict[str, str]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_source_policy_evidence_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "evidence_rows": len(evidence_rows),
        "source_context_rows": len(source_context_rows),
        "summary_rows": len(summary_rows),
        "inputs": {
            "action_plan": str(args.action_plan),
            "source_queue": str(args.source_queue),
            "row_ocr": str(args.row_ocr),
            "scenario_pairs": str(args.scenario_pairs),
            "table2_bridge": str(args.table2_bridge),
            "wnp_html": str(args.wnp_html),
        },
        "outputs": {
            "out": str(args.out),
            "source_context_out": str(args.source_context_out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def related_source_queue_rows(
    source_rows: list[dict[str, str]], concept: str, source_flags: str
) -> list[dict[str, str]]:
    flags = split_flags(source_flags)
    return [
        row
        for row in source_rows
        if row.get("concepts", "") == concept
        and split_flags(row.get("source_review_flags", "")) & flags
    ]


def related_scenario_rows(
    scenario_pair_rows: list[dict[str, str]],
    related_ids: set[str],
    concept: str,
    source_flags: str,
) -> list[dict[str, str]]:
    flags = split_flags(source_flags)
    return [
        row
        for row in scenario_pair_rows
        if row.get("concept", "") == concept
        and (
            row.get("appellation_term_id", "") in related_ids
            or split_flags(row.get("source_review_flags", "")) & flags
        )
    ]


def row_ocr_terms(rows: list[dict[str, str]], status: str) -> str:
    return join_nonempty(
        f"{row.get('term_id', '')} {row.get('michigan_term', '')}"
        for row in rows
        if row.get("row_ocr_status", "") == status
    )


def scenario_statuses(rows: list[dict[str, str]]) -> str:
    values = []
    for row in rows:
        values.append(
            "{scenario}:{action}:{pair}:{status}".format(
                scenario=row.get("scenario", ""),
                action=row.get("scenario_action", ""),
                pair=row.get("pair_id", ""),
                status=row.get("pair_review_status", ""),
            )
        )
    return join_nonempty(values)


def table2_bridge_read(rows: list[dict[str, str]], concept: str) -> str:
    row_number = concept.split()[-1].lstrip("0")
    for row in rows:
        if row.get("row_number", "").lstrip("0") == row_number:
            return row.get("current_read", "")
    return ""


def evidence_read(source_flags: str, term_id: str) -> str:
    if CHELM_FLAG in split_flags(source_flags):
        return (
            f"{term_id} is a Chełm spelling-context target; local evidence supports "
            "review scope, while row OCR still leaves the pair-rule/source-cell decision open"
        )
    return f"{term_id} needs source-policy evidence before a source-lock change"


def concept_from_pair_ids(pair_ids: str) -> str:
    first = next(iter(split_semicolon(pair_ids)), "")
    match = re.match(r"wrr2_(\d+)_", first)
    return f"WRR2 {match.group(1)}" if match else ""


def line_range_present(lines: list[str], start: int, end: int) -> bool:
    return 1 <= start <= end <= len(lines)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def split_flags(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def join_nonempty(values) -> str:
    return ";".join(value for value in values if value)


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
