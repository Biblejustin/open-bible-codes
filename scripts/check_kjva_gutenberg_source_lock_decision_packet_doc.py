#!/usr/bin/env python3
"""Validate Project Gutenberg KJVA source-lock decision packet boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_gutenberg_source_lock_decision_packet as packet


DEFAULT_DOC = packet.DEFAULT_MD
DEFAULT_DECISIONS = packet.DEFAULT_DECISIONS
DEFAULT_SUMMARY = packet.DEFAULT_SUMMARY
DEFAULT_MANIFEST = packet.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Source-Lock Decision Packet",
    "Status: decision packet only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text, normalize Bible text, create a local corpus",
    "Decision rows: 10.",
    "Policy-ready rows: 2.",
    "Recommended-but-not-locked rows: 3.",
    "Blocked rows: 4.",
    "Candidate-not-locked rows: 1.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Use Project Gutenberg eBook 30 plus eBook 124 as the next independent KJVA candidate stream",
    "Use Gutenberg source order for an independent Project Gutenberg replication stream",
    "Roll the separate Epistle of Jeremiah source section into BAR",
    "Do not source-lock Sirach or Prayer of Manasseh",
    "Local KJVA Apocrypha order: `TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES`.",
    "Gutenberg Apocrypha source order: `1ES;2ES;TOB;JDT;ESG;WIS;SIR;BAR;LJE_SOURCE;S3Y;SUS;BEL;MAN;1MA;2MA`.",
    "KJV exact count matches: 66/66.",
    "Apocrypha/deuterocanon exact count matches: 12/14.",
    "Apocrypha/deuterocanon count drifts: 2.",
    "Extra source sections: 1.",
    "`sirach_count_drift`",
    "`prayer_count_drift`",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|result-bearing replication is ready|claim report|"
    r"claim-level|proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_gutenberg_source_lock_decision_packet_doc(
        args.doc,
        decisions=args.decisions,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(
                f"KJVA Gutenberg source-lock decision packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"KJVA Gutenberg source-lock decision packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_source_lock_decision_packet_doc(
    doc: Path = DEFAULT_DOC,
    *,
    decisions: Path | None = DEFAULT_DECISIONS,
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
    if decisions is not None:
        failures.extend(validate_decisions_csv(decisions))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_decisions_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.DECISION_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 10:
        failures.append(f"{path} expected 10 decision rows, found {len(rows)}")
    ids = {row["decision_id"] for row in rows}
    for required in {
        "source_stream",
        "book_order",
        "baruch_epistle",
        "sirach_count_drift",
        "prayer_count_drift",
        "result_boundary",
    }:
        if required not in ids:
            failures.append(f"{path} missing decision row {required}")
    blocked = [row for row in rows if row.get("lock_status") == "blocked"]
    if len(blocked) != 4:
        failures.append(f"{path} expected 4 blocked rows, found {len(blocked)}")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "decision_rows": "10",
        "policy_ready_rows": "2",
        "recommended_policy_rows": "3",
        "blocked_rows": "4",
        "candidate_not_locked_rows": "1",
        "local_apocrypha_order": "TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES",
        "gutenberg_apocrypha_order": "1ES;2ES;TOB;JDT;ESG;WIS;SIR;BAR;LJE_SOURCE;S3Y;SUS;BEL;MAN;1MA;2MA",
        "order_recommendation": "use_gutenberg_source_order_for_independent_replication",
        "baruch_epistle_recommendation": "roll_lje_source_into_bar_with_component_metadata",
        "sirach_blocker": "one_source_marker_short_needs_collation",
        "prayer_blocker": "unmarked_prose_needs_verse_boundary_policy",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "decision_packet_only_not_result_bearing",
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
    if not isinstance(payload, dict):
        return [f"{path} JSON root must be an object"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "decision packet only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
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
