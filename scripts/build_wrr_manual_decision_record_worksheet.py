#!/usr/bin/env python3
"""Build a WRR manual-decision worksheet with current record status."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_REGISTER = Path("reports/wrr_1994/wrr_manual_decision_register.csv")
DEFAULT_RECORDS_TEMPLATE = Path("data/study/mappings/wrr_manual_decision_records.csv")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_manual_decision_record_worksheet.csv")
DEFAULT_MD = Path("docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_manual_decision_record_worksheet.manifest.json")

FIELDNAMES = [
    "decision_id",
    "register_decision_rank",
    "decision_lane",
    "review_state",
    "decision_target",
    "source_checklist",
    "required_decision_record",
    "evidence_prompt",
    "suggested_decision_status_values",
    "suggested_selected_action_values",
    "allowed_without_input",
    "record_decision_status",
    "record_selected_action",
    "record_locked_by",
    "record_locked_at",
    "record_evidence_citation",
    "record_evidence_summary",
]

RECORD_FIELDS = [
    "decision_id",
    "register_decision_rank",
    "decision_lane",
    "review_state",
    "decision_target",
    "source_checklist",
    "decision_status",
    "selected_action",
    "evidence_citation",
    "evidence_summary",
    "locked_by",
    "locked_at",
    "notes",
]

NO_MUTATION_BOUNDARY = (
    "Record rows document manual locks; this worksheet does not mutate source rows, "
    "method rules, replacement choices, or pair membership."
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    record_by_id = records_by_decision_id(read_rows_if_exists(args.records_template))
    rows = build_worksheet_rows(read_rows(args.register), record_by_id)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--records-template", type=Path, default=DEFAULT_RECORDS_TEMPLATE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_rows_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_rows(path)


def records_by_decision_id(record_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["decision_id"]: row for row in record_rows if row.get("decision_id")}


def build_worksheet_rows(
    register_rows: list[dict[str, str]],
    record_by_id: dict[str, dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    records = record_by_id or {}
    return [worksheet_row(row, records) for row in register_rows]


def worksheet_row(
    row: dict[str, str],
    record_by_id: dict[str, dict[str, str]],
) -> dict[str, str]:
    lane = row.get("decision_lane", "")
    rank = int(row.get("decision_rank", "0"))
    decision_id = f"wrr_decision_{rank:03d}"
    record = record_by_id.get(decision_id, {})
    return {
        "decision_id": decision_id,
        "register_decision_rank": str(rank),
        "decision_lane": lane,
        "review_state": row.get("review_state", ""),
        "decision_target": row.get("decision_target", ""),
        "source_checklist": row.get("source_checklist", ""),
        "required_decision_record": row.get("required_decision_record", ""),
        "evidence_prompt": evidence_prompt(lane),
        "suggested_decision_status_values": suggested_status_values(),
        "suggested_selected_action_values": suggested_action_values(lane),
        "allowed_without_input": row.get("allowed_without_input", ""),
        "record_decision_status": record.get("decision_status", "").strip() or "unrecorded",
        "record_selected_action": record.get("selected_action", ""),
        "record_locked_by": record.get("locked_by", ""),
        "record_locked_at": record.get("locked_at", ""),
        "record_evidence_citation": record.get("evidence_citation", ""),
        "record_evidence_summary": record.get("evidence_summary", ""),
    }


def evidence_prompt(lane: str) -> str:
    return {
        "source_policy_pair_rule": (
            "cite primary source and pair-rule evidence before changing the working source"
        ),
        "source_transcription_row_cluster": (
            "cite row image or source-list transcription plus row/column alignment evidence"
        ),
        "page_image_near_match": "cite page-image transcription evidence",
        "method_pair_universe": "explain zero ordinary hits with explicit method or pair-universe evidence",
    }.get(lane, "cite source evidence before locking a decision")


def suggested_status_values() -> str:
    return ";".join(
        [
            "accepted_keep",
            "accepted_correction",
            "accepted_exclusion",
            "accepted_method_lock",
            "deferred_no_lock",
        ]
    )


def suggested_action_values(lane: str) -> str:
    values = {
        "source_policy_pair_rule": [
            "no_source_change",
            "source_policy_correction",
            "pair_rule_change",
            "deferred_no_lock",
        ],
        "source_transcription_row_cluster": [
            "no_source_change",
            "row_transcription_update",
            "pair_exclusion",
            "deferred_no_lock",
        ],
        "page_image_near_match": [
            "no_source_change",
            "source_correction",
            "pair_exclusion",
            "deferred_no_lock",
        ],
        "method_pair_universe": [
            "method_lock",
            "pair_universe_lock",
            "pair_exclusion",
            "deferred_no_lock",
        ],
    }
    return ";".join(values.get(lane, ["deferred_no_lock"]))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    lane_counts = Counter(row["decision_lane"] for row in rows)
    record_status_counts = Counter(row["record_decision_status"] for row in rows)
    action_counts = Counter(row["record_selected_action"] for row in rows if row["record_selected_action"])
    recorded_count = sum(1 for row in rows if row["record_decision_status"] != "unrecorded")
    locked_count = record_status_counts["locked"]
    lines = [
        "# WRR Manual Decision Record Worksheet",
        "",
        "Status: worksheet plus current WRR manual decision-record status.",
        "It reads `data/study/mappings/wrr_manual_decision_records.csv` but does not update it.",
        NO_MUTATION_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_manual_decision_record_worksheet "
            f"--register {args.register} "
            f"--records-template {args.records_template} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Worksheet rows: {len(rows)}.",
        f"- Source-policy/pair-rule rows: {lane_counts['source_policy_pair_rule']}.",
        f"- Source-transcription row-cluster rows: {lane_counts['source_transcription_row_cluster']}.",
        f"- Page-image rows: {lane_counts['page_image_near_match']}.",
        f"- Method/pair-universe rows: {lane_counts['method_pair_universe']}.",
        f"- Target records file: `{args.records_template}`.",
        f"- Recorded decision rows: {recorded_count}.",
        f"- Locked decision rows: {locked_count}.",
        f"- Unrecorded decision rows: {len(rows) - recorded_count}.",
        f"- Recorded selected actions: {format_counts(action_counts)}.",
        "",
        "## Lock Row Fields",
        "",
        "`" + ",".join(RECORD_FIELDS) + "`",
        "",
        "The worksheet gives exact `decision_id`, register fields, and current record fields when a lock row exists.",
        "Locked rows are evidence records. Working-source changes, replacement locks, and pair exclusions remain absent unless `selected_action` names them.",
        "",
        "## Worksheet",
        "",
        "| Decision id | Rank | Lane | State | Target | Checklist | Record status | Recorded action | Locked by | Locked at | Evidence prompt | Suggested actions |",
        "| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| `{decision_id}` | {register_decision_rank} | `{decision_lane}` | "
            "`{review_state}` | `{decision_target}` | `{source_checklist}` | "
            "`{record_decision_status}` | `{record_selected_action}` | "
            "{record_locked_by} | {record_locked_at} | {evidence_prompt} | "
            "`{suggested_selected_action_values}` |".format(
                **markdown_row(row)
            )
        )
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    lane_counts = Counter(row["decision_lane"] for row in rows)
    record_status_counts = Counter(row["record_decision_status"] for row in rows)
    action_counts = Counter(row["record_selected_action"] for row in rows if row["record_selected_action"])
    recorded_count = sum(1 for row in rows if row["record_decision_status"] != "unrecorded")
    payload = {
        "tool": "build_wrr_manual_decision_record_worksheet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "lane_counts": dict(sorted(lane_counts.items())),
        "recorded_rows": recorded_count,
        "locked_rows": record_status_counts["locked"],
        "unrecorded_rows": len(rows) - recorded_count,
        "record_status_counts": dict(sorted(record_status_counts.items())),
        "recorded_action_counts": dict(sorted(action_counts.items())),
        "inputs": {
            "register": str(args.register),
            "records_template": str(args.records_template),
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


def markdown_row(row: dict[str, str]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def format_counts(counts: Counter[str]) -> str:
    if not counts:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in sorted(counts.items()))


if __name__ == "__main__":
    raise SystemExit(main())
