#!/usr/bin/env python3
"""Validate KJVA apocrypha bridge prospective result stays negative/cautioned."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


DEFAULT_TERMS = Path("terms/kjv_apocrypha_bridge_prospective_terms.csv")
DEFAULT_CANDIDATES = Path(
    "reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv"
)
DEFAULT_BRIDGE_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective/bridge_summary.csv"
)
DEFAULT_TERM_SUMMARY = Path("reports/kjv_apocrypha_bridge_prospective/term_summary.csv")
DEFAULT_NONBIBLE_CONTROL_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv"
)
DEFAULT_NONBIBLE_TERM_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/term_summary.csv"
)
DEFAULT_PROFILES = Path("configs/prospective_study_lanes.json")
DEFAULT_CANDIDATES_DOC = Path("docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md")
DEFAULT_CONTROLS_DOC = Path("docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md")
DEFAULT_NONBIBLE_DOC = Path(
    "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md"
)

PROFILE_ID = "kjva_apocrypha_bridge_prospective"
EXPECTED_TERM_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "language",
    "term",
    "notes",
]
EXPECTED_TERM_IDS = {
    "kjva_apocrypha_antiochus",
    "kjva_apocrypha_mattathias",
    "kjva_apocrypha_judas_maccabeus",
    "kjva_apocrypha_eleazar",
    "kjva_apocrypha_tobit",
    "kjva_apocrypha_judith",
    "kjva_apocrypha_holofernes",
}
EXPECTED_CANDIDATE_ROW = {
    "corpus": "KJVA Prospective",
    "term_ids": "kjva_apocrypha_tobit",
    "concepts": "Tobit",
    "normalized_term": "tobit",
    "term_length": "5",
    "skip": "-215",
    "direction": "backward",
    "bridge_type": "canonical_to_apocrypha",
    "start_ref": "MAT 1:8",
    "center_ref": "MAT 1:2",
    "end_ref": "2ES 16:75",
    "canonical_books": "MAT",
    "apocrypha_books": "2ES",
    "class_path": "CCCAA",
    "center_word": "Abraham",
    "center_normalized_word": "abraham",
}
EXPECTED_BRIDGE_METRICS = {
    "corpus": "KJVA Prospective",
    "queries_tested": "7",
    "min_skip": "2",
    "max_skip": "250",
    "direction": "both",
    "bridge_rows": "1",
    "terms_with_bridge_rows": "1",
    "apocrypha_books_touched": "1",
    "bridge_type:canonical_to_apocrypha": "1",
}
EXPECTED_TERM_SUMMARY_FIELDNAMES = [
    "rank",
    "normalized_term",
    "term_ids",
    "concepts",
    "categories",
    "observed_bridge_rows",
    "samples",
    "sample_min",
    "sample_mean",
    "sample_max",
    "samples_ge_observed",
    "p_ge",
    "q_ge",
    "observed_minus_sample_max",
    "observed_gt_sample_max",
]
EXPECTED_NONBIBLE_CONTROL_ROWS = {
    "SHAKESPEARE": "0",
    "WAR_PEACE": "0",
    "MOBY_DICK": "1",
}
CANDIDATES_DOC_PHRASES = (
    "Status: bounded bridge-candidate scan. This is not a claim report.",
    "queries_tested: 7",
    "bridge_rows: 1",
    "| 1 | `canonical_to_apocrypha` | `tobit` | -215 | MAT 1:8 | MAT 1:2 | 2ES 16:75 | 2ES | `CCCAA` |",
)
CONTROLS_DOC_PHRASES = (
    "Status: term-level shuffled-insertion controls. This is not a claim report.",
    "bridge terms reviewed: 7",
    "terms with observed count above every shuffled sample: 0",
    "terms with BH q_ge <= 0.05: 0",
    "| 1 | `tobit` | Tobit | 1 | 2 | 0.1016 | 485 | 0.097181 | 0.680267 | -1 |",
)
NONBIBLE_DOC_PHRASES = (
    "Status: non-Bible boundary controls for the initial KJVA Prospective apocrypha bridge scan.",
    "This is not a claim report.",
    "observed bridge rows: 1",
    "non-Bible controls >= observed total: 1 of 3",
    "| `MOBY_DICK` | 1 | 1 | 1 | 0 | 0 |",
    "| `MOBY_DICK` | `tobit` | 1 | 1 | 0 | 0 |",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_apocrypha_bridge_prospective_boundary(
        terms=args.terms,
        candidates=args.candidates,
        bridge_summary=args.bridge_summary,
        term_summary=args.term_summary,
        nonbible_control_summary=args.nonbible_control_summary,
        nonbible_term_summary=args.nonbible_term_summary,
        profiles=args.profiles,
        candidates_doc=args.candidates_doc,
        controls_doc=args.controls_doc,
        nonbible_doc=args.nonbible_doc,
        threshold=args.threshold,
    )
    if failures:
        for failure in failures:
            print(
                f"KJVA apocrypha bridge prospective boundary failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print("KJVA apocrypha bridge prospective boundary ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--bridge-summary", type=Path, default=DEFAULT_BRIDGE_SUMMARY)
    parser.add_argument("--term-summary", type=Path, default=DEFAULT_TERM_SUMMARY)
    parser.add_argument(
        "--nonbible-control-summary",
        type=Path,
        default=DEFAULT_NONBIBLE_CONTROL_SUMMARY,
    )
    parser.add_argument(
        "--nonbible-term-summary",
        type=Path,
        default=DEFAULT_NONBIBLE_TERM_SUMMARY,
    )
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--candidates-doc", type=Path, default=DEFAULT_CANDIDATES_DOC)
    parser.add_argument("--controls-doc", type=Path, default=DEFAULT_CONTROLS_DOC)
    parser.add_argument("--nonbible-doc", type=Path, default=DEFAULT_NONBIBLE_DOC)
    parser.add_argument("--threshold", type=float, default=0.05)
    return parser


def validate_kjva_apocrypha_bridge_prospective_boundary(
    *,
    terms: Path = DEFAULT_TERMS,
    candidates: Path = DEFAULT_CANDIDATES,
    bridge_summary: Path = DEFAULT_BRIDGE_SUMMARY,
    term_summary: Path = DEFAULT_TERM_SUMMARY,
    nonbible_control_summary: Path = DEFAULT_NONBIBLE_CONTROL_SUMMARY,
    nonbible_term_summary: Path = DEFAULT_NONBIBLE_TERM_SUMMARY,
    profiles: Path = DEFAULT_PROFILES,
    candidates_doc: Path = DEFAULT_CANDIDATES_DOC,
    controls_doc: Path = DEFAULT_CONTROLS_DOC,
    nonbible_doc: Path = DEFAULT_NONBIBLE_DOC,
    threshold: float = 0.05,
) -> list[str]:
    failures: list[str] = []
    failures.extend(validate_terms(terms))
    failures.extend(validate_candidates(candidates))
    failures.extend(validate_bridge_summary(bridge_summary))
    failures.extend(validate_term_summary(term_summary, threshold=threshold))
    failures.extend(
        validate_nonbible_controls(
            nonbible_control_summary,
            nonbible_term_summary,
            observed_total=1,
        )
    )
    failures.extend(validate_profiles(profiles))
    failures.extend(validate_doc(candidates_doc, CANDIDATES_DOC_PHRASES))
    failures.extend(validate_doc(controls_doc, CONTROLS_DOC_PHRASES))
    failures.extend(validate_doc(nonbible_doc, NONBIBLE_DOC_PHRASES))
    return failures


def validate_terms(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != EXPECTED_TERM_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != len(EXPECTED_TERM_IDS):
        failures.append(f"{path} has {len(rows)} term row(s), expected 7")
    term_ids = {row.get("term_id", "") for row in rows}
    if term_ids != EXPECTED_TERM_IDS:
        failures.append(f"{path} term ids drifted")
    for row in rows:
        if row.get("category") != "kjv_apocrypha_bridge_prospective":
            failures.append(f"{path} {row.get('term_id')} category drifted")
        if row.get("language") != "english":
            failures.append(f"{path} {row.get('term_id')} language drifted")
    return failures


def validate_candidates(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    if len(rows) != 1:
        failures.append(f"{path} has {len(rows)} candidate row(s), expected 1")
        return failures
    row = rows[0]
    for field, expected in EXPECTED_CANDIDATE_ROW.items():
        if row.get(field) != expected:
            failures.append(
                f"{path} candidate {field}={row.get(field)!r}, expected {expected!r}"
            )
    return failures


def validate_bridge_summary(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    _, rows = data
    metrics = {row.get("metric", ""): row.get("value", "") for row in rows}
    failures: list[str] = []
    for metric, expected in EXPECTED_BRIDGE_METRICS.items():
        if metrics.get(metric) != expected:
            failures.append(
                f"{path} {metric}={metrics.get(metric)!r}, expected {expected!r}"
            )
    return failures


def validate_term_summary(path: Path, *, threshold: float) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != EXPECTED_TERM_SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != len(EXPECTED_TERM_IDS):
        failures.append(f"{path} has {len(rows)} term summary row(s), expected 7")

    rows_by_term = {row.get("normalized_term", ""): row for row in rows}
    tobit = rows_by_term.get("tobit")
    if tobit is None:
        failures.append(f"{path} missing tobit row")
    else:
        expected_tobit = {
            "observed_bridge_rows": "1",
            "samples": "5000",
            "sample_max": "2",
            "samples_ge_observed": "485",
            "p_ge": "0.097181",
            "q_ge": "0.680267",
            "observed_gt_sample_max": "False",
        }
        for field, expected in expected_tobit.items():
            if tobit.get(field) != expected:
                failures.append(
                    f"{path} tobit {field}={tobit.get(field)!r}, expected {expected!r}"
                )

    observed_total = 0
    for row in rows:
        label = row.get("normalized_term", "")
        observed = parse_int(row.get("observed_bridge_rows", ""), path, label, failures)
        observed_total += observed
        if row.get("samples") != "5000":
            failures.append(f"{path} {label} samples={row.get('samples')!r}, expected '5000'")
        q_value = parse_float(row.get("q_ge", ""), path, label, "q_ge", failures)
        if q_value <= threshold:
            failures.append(f"{path} {label} crosses q_ge threshold: {q_value}")
        if truthy_csv(row.get("observed_gt_sample_max", "")):
            failures.append(f"{path} {label} observed count is above every shuffled sample")
    if observed_total != 1:
        failures.append(f"{path} observed bridge total is {observed_total}, expected 1")
    return failures


def validate_nonbible_controls(
    control_summary: Path,
    term_summary: Path,
    *,
    observed_total: int,
) -> list[str]:
    data = read_csv(control_summary)
    if isinstance(data, str):
        return [data]
    _, control_rows = data
    failures: list[str] = []
    if len(control_rows) != len(EXPECTED_NONBIBLE_CONTROL_ROWS):
        failures.append(
            f"{control_summary} has {len(control_rows)} control row(s), expected 3"
        )
    rows_by_label = {row.get("control_label", ""): row for row in control_rows}
    for label, expected_bridge_rows in EXPECTED_NONBIBLE_CONTROL_ROWS.items():
        row = rows_by_label.get(label)
        if row is None:
            failures.append(f"{control_summary} missing {label} row")
            continue
        if row.get("bridge_rows") != expected_bridge_rows:
            failures.append(
                f"{control_summary} {label} bridge_rows={row.get('bridge_rows')!r}, expected {expected_bridge_rows!r}"
            )
    controls_ge_observed = sum(
        parse_int(row.get("bridge_rows", ""), control_summary, row.get("control_label", ""), failures)
        >= observed_total
        for row in control_rows
    )
    if controls_ge_observed != 1:
        failures.append(
            f"{control_summary} controls >= observed total is {controls_ge_observed} of {len(control_rows)}, expected 1 of 3"
        )

    term_data = read_csv(term_summary)
    if isinstance(term_data, str):
        return failures + [term_data]
    _, term_rows = term_data
    if len(term_rows) != 1:
        failures.append(f"{term_summary} has {len(term_rows)} term row(s), expected 1")
        return failures
    row = term_rows[0]
    expected_term_row = {
        "control_label": "MOBY_DICK",
        "normalized_term": "tobit",
        "bridge_rows": "1",
        "canonical_to_apocrypha": "1",
        "apocrypha_to_canonical": "0",
        "multi_segment_bridge": "0",
    }
    for field, expected in expected_term_row.items():
        if row.get(field) != expected:
            failures.append(
                f"{term_summary} {field}={row.get(field)!r}, expected {expected!r}"
            )
    return failures


def validate_profiles(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]

    profiles = payload.get("profiles")
    if not isinstance(profiles, list):
        return [f"{path} missing profiles list"]

    failures: list[str] = []
    ready = [profile.get("id", "") for profile in profiles if profile.get("status") == "ready_for_preflight"]
    if ready:
        failures.append(f"{path} still has ready_for_preflight lane(s): {', '.join(ready)}")

    matches = [profile for profile in profiles if profile.get("id") == PROFILE_ID]
    if len(matches) != 1:
        failures.append(f"{path} has {len(matches)} profiles for {PROFILE_ID}, expected 1")
        return failures
    profile = matches[0]
    expected_values = {
        "status": "completed_negative_controlled_result",
        "language": "english",
        "term_file": "terms/kjv_apocrypha_bridge_prospective_terms.csv",
        "protocol": "protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml",
        "report_doc": "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
        "skip_range": "2..250",
        "direction": "both",
        "min_normalized_length": "4",
        "correction": "benjamini_hochberg_across_registered_terms",
        "primary_study_outcome": "negative: no term survives BH q <= 0.05 and one non-Bible control matches the observed total",
    }
    for field, expected in expected_values.items():
        if profile.get(field) != expected:
            failures.append(
                f"{path} {PROFILE_ID} {field}={profile.get(field)!r}, expected {expected!r}"
            )
    controls = normalize_space(str(profile.get("controls", "")))
    required_control_phrase = (
        "5000 shuffled apocrypha-block samples plus same-length non-Bible insertion controls"
    )
    if normalize_space(required_control_phrase) not in controls:
        failures.append(f"{path} {PROFILE_ID} controls phrase drifted")
    return failures


def validate_doc(path: Path, required_phrases: tuple[str, ...]) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    normalized = normalize_space(path.read_text(encoding="utf-8"))
    return [
        f"{path} missing phrase: {phrase}"
        for phrase in required_phrases
        if normalize_space(phrase) not in normalized
    ]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def parse_int(
    value: str,
    path: Path,
    label: str,
    failures: list[str],
) -> int:
    try:
        return int(value)
    except ValueError:
        failures.append(f"{path} {label} has nonnumeric integer value: {value!r}")
        return 0


def parse_float(
    value: str,
    path: Path,
    label: str,
    field: str,
    failures: list[str],
) -> float:
    try:
        return float(value)
    except ValueError:
        failures.append(f"{path} {label} has nonnumeric {field}: {value!r}")
        return float("nan")


def truthy_csv(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
