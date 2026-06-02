#!/usr/bin/env python3
"""Validate Gutenberg + Hakkaac KJVA split-source role sidecar boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_gutenberg_hakkaac_split_source_role_sidecar as sidecar


DEFAULT_DOC = sidecar.DEFAULT_MD
DEFAULT_ROLES = sidecar.DEFAULT_ROLES
DEFAULT_BLOCKERS = sidecar.DEFAULT_BLOCKERS
DEFAULT_SUMMARY = sidecar.DEFAULT_SUMMARY
DEFAULT_MANIFEST = sidecar.DEFAULT_MANIFEST

EXPECTED_LOCAL_ORDER = "TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES"
EXPECTED_GUTENBERG_ORDER = "1ES;2ES;TOB;JDT;ESG;WIS;SIR;BAR;LJE_SOURCE;S3Y;SUS;BEL;MAN;1MA;2MA"

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Hakkaac Split-Source Role Sidecar",
    "Status: split-source role sidecar only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a source-use approval",
    "not a result-bearing replication",
    "does not commit Bible text",
    "does not commit Bible text, choose a final source text",
    "Role rows: 7.",
    "Unresolved blocker rows: 6.",
    "Policy-ready role rows: 2.",
    "Recommended-but-not-locked role rows: 2.",
    "Blocked role rows: 2.",
    "Candidate-not-locked role rows: 1.",
    "Current eBible rerun baseline locked: 1.",
    "Split-source role sidecar written: 1.",
    "Hakkaac exact marker books: 14/14.",
    "Hakkaac exact normalized verse matches: 5719/5720.",
    "Hakkaac length-drift verses: 1.",
    "Gutenberg Sirach gap refs: `SIR 44:23`.",
    "Gutenberg Prayer of Manasseh markers: 0/15.",
    "Source-lock ready: 0.",
    "Result-ready: 0.",
    f"Current local KJVA Apocrypha/deuterocanon order: `{EXPECTED_LOCAL_ORDER}`.",
    f"Project Gutenberg Apocrypha source order: `{EXPECTED_GUTENBERG_ORDER}`.",
    "Future independent candidate order recommendation: `use_gutenberg_source_order_for_independent_replication`.",
    "`current_ebible_rerun_baseline`",
    "`gutenberg_apocrypha_component`",
    "`hakkaac_marker_collation_witness`",
    "`split_stream_boundary`",
    "`sirach_19_1_hakkaac_length_drift`",
    "closes only the missing written source-role/order boundary",
    "does not close the source-use boundary",
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
    failures = validate_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc(
        args.doc,
        roles=args.roles,
        blockers=args.blockers,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA split-source role sidecar failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA split-source role sidecar ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--roles", type=Path, default=DEFAULT_ROLES)
    parser.add_argument("--blockers", type=Path, default=DEFAULT_BLOCKERS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc(
    doc: Path = DEFAULT_DOC,
    *,
    roles: Path | None = DEFAULT_ROLES,
    blockers: Path | None = DEFAULT_BLOCKERS,
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
    if roles is not None:
        failures.extend(validate_roles_csv(roles))
    if blockers is not None:
        failures.extend(validate_blockers_csv(blockers))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_roles_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != sidecar.ROLE_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 7:
        failures.append(f"{path} expected 7 role rows, found {len(rows)}")
    ids = {row.get("role_id") for row in rows}
    for required in {
        "current_ebible_rerun_baseline",
        "gutenberg_kjv_component",
        "gutenberg_apocrypha_component",
        "gutenberg_lje_baruch_rollup",
        "hakkaac_marker_collation_witness",
        "split_stream_boundary",
        "tracked_text_retention_boundary",
    }:
        if required not in ids:
            failures.append(f"{path} missing role row {required}")
    statuses = [row.get("lock_status") for row in rows]
    if statuses.count("policy_ready") != 2:
        failures.append(f"{path} expected 2 policy_ready rows")
    if statuses.count("recommended_policy_not_locked") != 2:
        failures.append(f"{path} expected 2 recommended rows")
    if statuses.count("blocked") != 2:
        failures.append(f"{path} expected 2 blocked rows")
    if statuses.count("candidate_not_locked") != 1:
        failures.append(f"{path} expected 1 candidate-not-locked row")
    return failures


def validate_blockers_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != sidecar.BLOCKER_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 6:
        failures.append(f"{path} expected 6 blocker rows, found {len(rows)}")
    ids = {row.get("blocker_id") for row in rows}
    for required in {
        "sirach_44_23_gutenberg_marker_gap",
        "manasseh_unmarked_gutenberg_section",
        "sirach_19_1_hakkaac_length_drift",
        "hakkaac_source_use_boundary",
        "split_source_result_boundary",
        "gutenberg_source_stream_boundary",
    }:
        if required not in ids:
            failures.append(f"{path} missing blocker row {required}")
    if {row.get("affects_letter_stream") for row in rows} != {"True"}:
        failures.append(f"{path} expected all blockers to affect letter stream")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != sidecar.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "role_rows": "7",
        "blocker_rows": "6",
        "policy_ready_rows": "2",
        "recommended_policy_rows": "2",
        "blocked_rows": "2",
        "candidate_not_locked_rows": "1",
        "current_rerun_locked": "True",
        "split_source_role_sidecar_written": "True",
        "local_apocrypha_order": EXPECTED_LOCAL_ORDER,
        "gutenberg_apocrypha_order": EXPECTED_GUTENBERG_ORDER,
        "future_independent_order_recommendation": (
            "use_gutenberg_source_order_for_independent_replication"
        ),
        "hakkaac_exact_marker_books": "14",
        "hakkaac_exact_normalized_verse_matches": "5719",
        "hakkaac_length_drift_verses": "1",
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": "0",
        "gutenberg_manasseh_local_markers": "15",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "split_source_role_sidecar_only_not_result_bearing",
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
    if payload.get("claim_boundary") != "split-source role sidecar only; no ELS result":
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
