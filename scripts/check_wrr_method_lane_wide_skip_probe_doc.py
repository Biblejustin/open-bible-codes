#!/usr/bin/env python3
"""Validate WRR method-lane wide-skip probe remains diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import analyze_wrr_method_lane_wide_skip as probe


DEFAULT_DOC = probe.DEFAULT_MD
DEFAULT_OUT = probe.DEFAULT_OUT
DEFAULT_SUMMARY = probe.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = probe.DEFAULT_MANIFEST

EXPECTED_TERM_IDS = {
    "wrr2_02_app_03",
    "wrr2_02_app_05",
    "wrr2_07_app_05",
    "wrr2_11_app_05",
    "wrr2_12_app_05",
    "wrr2_19_app_03",
    "wrr2_19_app_10",
    "wrr2_20_app_03",
    "wrr2_20_app_05",
    "wrr2_28_app_05",
    "wrr2_31_app_09",
}
EXPECTED_SUMMARY = {
    "terms": "11",
    "max_skip": "5000",
    "direction": "both",
    "profile_skips": "250;1000;2500;5000",
    "terms_with_any_hit": "0",
    "terms_zero_through_max": "11",
    "terms_with_first_hit_after_1000": "0",
    "total_hits_through_max": "0",
}
REQUIRED_PHRASES = (
    "# WRR Method-Lane Wide-Skip Probe",
    "Status: diagnostic probe for OCR-matched WRR method-lane terms.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- method-lane terms: 11.",
    "- max skip probed: 5000.",
    "- terms with any wider-skip hit: 0.",
    "- terms still zero through max skip: 11.",
    "- total hits through max skip: 0.",
    "Wide-skip hits are diagnostic only",
    "No row here changes the locked local WRR method report.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_wide_skip_probe_doc(
        args.doc,
        args.out,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR method-lane wide-skip probe failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR method-lane wide-skip probe ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_wide_skip_probe_doc(
    doc: Path,
    out: Path | None = DEFAULT_OUT,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    if out is not None:
        failures.extend(validate_out_csv(out))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_out_csv(out: Path) -> list[str]:
    data = read_csv(out)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    expected_fieldnames = probe.probe_fieldnames(list(probe.DEFAULT_PROFILE_SKIPS))
    if fieldnames != expected_fieldnames:
        failures.append(f"{out} fieldnames drifted")
    if len(rows) != int(EXPECTED_SUMMARY["terms"]):
        failures.append(f"{out} has {len(rows)} rows; expected 11")
    actual = {row.get("term_id", "") for row in rows}
    missing = sorted(EXPECTED_TERM_IDS - actual)
    unexpected = sorted(actual - EXPECTED_TERM_IDS)
    if missing:
        failures.append(f"{out} missing terms: {', '.join(missing)}")
    if unexpected:
        failures.append(f"{out} unexpected terms: {', '.join(unexpected)}")
    for row in rows:
        term_id = row.get("term_id", "")
        for profile in probe.DEFAULT_PROFILE_SKIPS:
            field = probe.profile_field(profile)
            if row.get(field) != "0":
                failures.append(f"{out} {term_id} {field}={row.get(field)!r}")
        if row.get("found_within_max_skip") != "false":
            failures.append(f"{out} {term_id} unexpectedly found a hit")
        if row.get("total_hits_through_max") != "0":
            failures.append(f"{out} {term_id} total hits not zero")
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    data = read_csv(summary)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != probe.SUMMARY_FIELDNAMES:
        failures.append(f"{summary} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{summary} has {len(rows)} rows; expected 1")
        return failures
    row = rows[0]
    for key, expected in EXPECTED_SUMMARY.items():
        if row.get(key) != expected:
            failures.append(f"{summary} {key}={row.get(key)!r}; expected {expected!r}")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "analyze_wrr_method_lane_wide_skip",
        "parameters": {
            "max_skip": probe.DEFAULT_MAX_SKIP,
            "direction": "both",
            "jobs": 1,
            "profile_skips": list(probe.DEFAULT_PROFILE_SKIPS),
        },
        "inputs": {
            "method_packet": str(probe.DEFAULT_METHOD_PACKET),
            "config": str(probe.DEFAULT_CONFIG),
        },
        "outputs": {
            "out": str(DEFAULT_OUT),
            "summary_out": str(DEFAULT_SUMMARY),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
        "probe_rows": int(EXPECTED_SUMMARY["terms"]),
        "summary_rows": 1,
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
