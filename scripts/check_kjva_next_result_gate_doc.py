#!/usr/bin/env python3
"""Validate KJVA next-result gate boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_next_result_gate as gate_builder


DEFAULT_DOC = gate_builder.DEFAULT_MD
DEFAULT_GATES = gate_builder.DEFAULT_GATES
DEFAULT_SUMMARY = gate_builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = gate_builder.DEFAULT_MANIFEST

REQUIRED_GATE_IDS = {
    "current_rerun_reproducibility",
    "completed_lane_claim_gate",
    "source_policy_lock",
    "source_text_lock",
    "verse_map_collation_lock",
    "drift_boundary_lock",
    "fresh_term_lock",
    "leakage_audit_lock",
    "fixed_controls_lock",
    "study_lock_manifest",
    "result_allowed",
}
REQUIRED_PHRASES = (
    "# KJVA Next Result Gate",
    "Status: next-result gate only.",
    "not an ELS result",
    "not a corpus import",
    "not a source-use approval",
    "not a source lock",
    "not a term lock",
    "not a study lock",
    "allows only current-source rerun reproducibility",
    "Gate rows: 11.",
    "Rerun-only ready rows: 1.",
    "Blocked rows: 10.",
    "Source-policy blocker rows: 7.",
    "Completed lane terms: 7.",
    "Completed lane observed bridge rows: 1.",
    "Completed lane significant terms: 0.",
    "Non-Bible controls at or above observed: 1.",
    "Source-lock ready: 0.",
    "Fresh terms ready: 0.",
    "Leakage audit ready: 0.",
    "Fixed controls ready: 0.",
    "Study-lock ready: 0.",
    "Result allowed: 0.",
    "`kjva_next_result_gate_blocks_new_output`",
    "`current_rerun_reproducibility`",
    "`completed_lane_claim_gate`",
    "`source_policy_lock`",
    "`source_text_lock`",
    "`verse_map_collation_lock`",
    "`drift_boundary_lock`",
    "`fresh_term_lock`",
    "`leakage_audit_lock`",
    "`fixed_controls_lock`",
    "`study_lock_manifest`",
    "`result_allowed`",
    "No new independent KJVA result-bearing run is allowed by this gate.",
    "No Bible text is written to tracked outputs.",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|source-use approved|term lock ready|study lock ready|"
    r"result allowed|result-bearing run is allowed|claim report|claim-level|"
    r"proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
    "Term lock, and not a study lock.",
    "Study-lock ready: 0.",
    "Result allowed: 0.",
    "No new independent KJVA result-bearing run is allowed by this gate.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_next_result_gate_doc(
        args.doc,
        gates=args.gates,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA next-result gate failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA next-result gate ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--gates", type=Path, default=DEFAULT_GATES)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_next_result_gate_doc(
    doc: Path = DEFAULT_DOC,
    *,
    gates: Path | None = DEFAULT_GATES,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    failures.extend(validate_no_overclaim(doc, text))
    if gates is not None:
        failures.extend(validate_gates_csv(gates))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_gates_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != gate_builder.GATE_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 11:
        failures.append(f"{path} expected 11 gate rows, found {len(rows)}")
    ids = {row.get("gate_id") for row in rows}
    for gate_id in REQUIRED_GATE_IDS:
        if gate_id not in ids:
            failures.append(f"{path} missing gate row {gate_id}")
    statuses = [row.get("status") for row in rows]
    if statuses.count("rerun_only_ready") != 1:
        failures.append(f"{path} expected 1 rerun_only_ready row")
    if statuses.count("blocked") != 10:
        failures.append(f"{path} expected 10 blocked rows")
    if {row.get("result_boundary") for row in rows} != {"not_result_bearing"}:
        failures.append(f"{path} result_boundary drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != gate_builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "gate_rows": "11",
        "rerun_only_ready_rows": "1",
        "blocked_rows": "10",
        "source_policy_blocker_rows": "7",
        "completed_lane_terms": "7",
        "completed_lane_observed_bridge_rows": "1",
        "completed_lane_significant_terms": "0",
        "nonbible_controls_at_or_above_observed": "1",
        "source_lock_ready": "False",
        "fresh_terms_ready": "False",
        "leakage_audit_ready": "False",
        "fixed_controls_ready": "False",
        "study_lock_ready": "False",
        "result_allowed": "False",
        "claim_status": "kjva_next_result_gate_blocks_new_output",
    }
    row = rows[0]
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "KJVA next-result gate only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    if payload.get("summary", {}).get("result_allowed") is not False:
        failures.append(f"{path} summary.result_allowed drifted")
    outputs = payload.get("outputs", {})
    markdown = outputs.get("markdown") if isinstance(outputs, dict) else None
    allowed_markdown_paths = {str(doc)}
    try:
        allowed_markdown_paths.add(str(doc.relative_to(Path.cwd())))
    except ValueError:
        pass
    if markdown not in allowed_markdown_paths:
        failures.append(f"{path} markdown output drifted")
    return failures


def validate_no_overclaim(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        line_text = text.splitlines()[line - 1].strip()
        if any(context in line_text for context in ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        failures.append(f"{path}:{line} overclaim phrase: {match.group(0)!r}")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
