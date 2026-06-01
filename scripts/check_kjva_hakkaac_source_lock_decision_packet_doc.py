#!/usr/bin/env python3
"""Validate Hakkaac KJVA source-lock decision packet boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_hakkaac_source_lock_decision_packet as packet


DEFAULT_DOC = packet.DEFAULT_MD
DEFAULT_DECISIONS = packet.DEFAULT_DECISIONS
DEFAULT_DRIFT_ROWS = packet.DEFAULT_DRIFT_ROWS
DEFAULT_SUMMARY = packet.DEFAULT_SUMMARY
DEFAULT_MANIFEST = packet.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Hakkaac Source-Lock Decision Packet",
    "Status: decision packet only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text, normalize Bible text into a tracked corpus",
    "Decision rows: 9.",
    "Policy-ready rows: 3.",
    "Recommended-but-not-locked rows: 2.",
    "Blocked rows: 3.",
    "Candidate-not-locked rows: 1.",
    "Exact normalized verse matches: 5719/5720.",
    "Length-drift verses: 1.",
    "Exact book stream matches: 13/14.",
    "Book stream drift books: 1.",
    "Exact blocker rows: 16/16.",
    "Exact marker books: 14/14.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Keep Hakkaac as candidate evidence only until a separate source-use lock is written.",
    "Keep current eBible KJVA as the rerun baseline",
    "Do not patch either source automatically for `SIR 19:1`.",
    "Do not combine Project Gutenberg plus Hakkaac into a result-bearing split-source stream",
    "`SIR 19:1`",
    "`source_use_boundary`",
    "`sirach_19_1_drift`",
    "`split_source_policy`",
    "No Bible text is written to tracked outputs.",
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
    failures = validate_kjva_hakkaac_source_lock_decision_packet_doc(
        args.doc,
        decisions=args.decisions,
        drift_rows=args.drift_rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(
                f"KJVA Hakkaac source-lock decision packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"KJVA Hakkaac source-lock decision packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    parser.add_argument("--drift-rows", type=Path, default=DEFAULT_DRIFT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_hakkaac_source_lock_decision_packet_doc(
    doc: Path = DEFAULT_DOC,
    *,
    decisions: Path | None = DEFAULT_DECISIONS,
    drift_rows: Path | None = DEFAULT_DRIFT_ROWS,
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
    if drift_rows is not None:
        failures.extend(validate_drift_rows_csv(drift_rows))
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
    if len(rows) != 9:
        failures.append(f"{path} expected 9 decision rows, found {len(rows)}")
    ids = {row["decision_id"] for row in rows}
    for required in {
        "source_use_boundary",
        "gutenberg_blocker_rows",
        "sirach_19_1_drift",
        "split_source_policy",
        "result_boundary",
    }:
        if required not in ids:
            failures.append(f"{path} missing decision row {required}")
    blocked = [row for row in rows if row.get("lock_status") == "blocked"]
    if len(blocked) != 3:
        failures.append(f"{path} expected 3 blocked rows, found {len(blocked)}")
    return failures


def validate_drift_rows_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != packet.DRIFT_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 drift row, found {len(rows)}")
        return failures
    row = rows[0]
    expected = {
        "ref": "SIR 19:1",
        "book": "SIR",
        "status": "length_drift",
        "local_norm_len": "107",
        "hakkaac_norm_len": "108",
        "norm_len_delta": "1",
        "first_diff_offset": "17",
        "recommendation": "keep_named_drift_until_source_policy_lock",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
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
        "decision_rows": "9",
        "policy_ready_rows": "3",
        "recommended_policy_rows": "2",
        "blocked_rows": "3",
        "candidate_not_locked_rows": "1",
        "total_verses": "5720",
        "exact_normalized_verse_matches": "5719",
        "length_drift_verses": "1",
        "exact_book_stream_matches": "13",
        "book_stream_drift_books": "1",
        "blocker_rows_exact": "16",
        "marker_books_exact": "14",
        "source_policy_recommendation": "candidate_evidence_only_until_source_use_lock",
        "drift_recommendation": "keep_sir_19_1_named_drift_do_not_patch_automatically",
        "split_source_recommendation": "do_not_combine_gutenberg_and_hakkaac_without_sidecar",
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
