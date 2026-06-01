#!/usr/bin/env python3
"""Validate real-report run documentation names current preflight guards."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import Any

from scripts import build_real_report_run_summary as summary_builder

DEFAULT_DOC = Path("docs/REAL_REPORT_RUN.md")
DEFAULT_PROTOCOL = Path("protocols/real_report_run.toml")
DEFAULT_MAKEFILE = Path("Makefile")
RUN_COMMAND = "python3 -m scripts.run_protocol protocols/real_report_run.toml --resume"
EXPECTED_GENERATED_OUTPUTS = (
    "reports/real_report_run/preflight.json",
    str(summary_builder.SUMMARY_OUT),
    str(summary_builder.MANIFEST_OUT),
    "reports/real_report_run/protocol_run.manifest.json",
    "reports/INDEX.md",
    "reports/index.json",
)
EXPECTED_PREFLIGHT_INPUTS = (
    "scripts/preflight_real_report_run.py",
    "scripts/check_real_report_run_doc.py",
    "docs/REAL_REPORT_RUN.md",
    "protocols/real_report_run.toml",
    "Makefile",
)
EXPECTED_SUMMARY_INPUTS = (
    "scripts/build_real_report_run_summary.py",
    "reports/step_tahot_final_gate/manifest.json",
    "reports/greek_exact_center_final_gate/summary.csv",
    "reports/wrr_1994/audit_counts_protocol.manifest.json",
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_queue_summary.csv",
    "reports/kjva_no_input_handoff_status/summary.csv",
    "reports/kjva_no_input_handoff_status/manifest.json",
    "reports/final_report_highlights/highlights.csv",
)
EXPECTED_SUMMARY_OUTPUTS = (
    str(summary_builder.SUMMARY_OUT),
    str(summary_builder.MANIFEST_OUT),
)
EXPECTED_MAKE_TARGET = f"real-report:\n\t{RUN_COMMAND}"

REQUIRED_PHRASES = (
    RUN_COMMAND,
    "make real-report",
    "`reports/real_report_run/preflight.json`",
    "`reports/real_report_run/summary.md`",
    "`reports/INDEX.md`",
    "protocol TOML files pass runner schema and duplicate-name checks",
    "corpus config TOML files pass required name/language/source schema checks",
    "term CSV files pass schema, language, normalization, constants, and gematria checks",
    "every `scripts/check_*.py` guard has a matching `tests/test_check_*.py` test module",
    "every `scripts/check_*.py` guard is wired through Make, preflight, or a protocol input",
    "claim-catalog summary table stays aligned with `claims/claim_catalog.csv`",
    "Cities claim-catalog row stays `under_specified`, source-review only, and aligned with the current Cities source-row lock decision records",
    "final report highlights markdown matches the deterministic builder output",
    "centered occurrence index markdown matches the deterministic builder output",
    "strongest candidate deep-dive markdown matches the deterministic builder output",
    "hypothesis-testing source audit doc keeps the source-status/no-result boundary visible",
    "research missing model pages audit doc keeps the missing level-2/3 model page boundary visible",
    "WRR adjacent source audit and simulation docs keep source-shape and simulation-only boundaries visible",
    "critical-omission follow-up docs keep Setup, Method, Results, and Cautions sections plus current headline counts visible",
    "Cities source-row lock evidence packet checks local recovered PDF and page-image artifact paths before any lock row can pass preflight",
    "populated Cities source-row lock decision records must name the exact decision id in their evidence citation or summary",
    "Cities source-row lock status",
    "Cities source-row lock decision records stay aligned to the 14-row evidence packet before any populated source-row lock can pass preflight",
    "study-mapping CSV schemas retain exact columns, required locked values, ISO `locked_at` dates, supported language markers, tracked term IDs",
    "KJVA Gutenberg plus Hakkaac split-source role sidecar writes the missing role/order boundary as planning-only evidence",
    "Hakkaac as marker/collation witness-only",
    "KJVA Gutenberg candidate checksum sidecar records eBook 30 and eBook 124 RDF and plain-text SHA-256 identifiers",
    "KJVA source-policy blocker packet",
    "docs/KJVA_SOURCE_POLICY_BLOCKER_PACKET.md",
    "KJVA next-result gate",
    "docs/KJVA_NEXT_RESULT_GATE.md",
    "KJVA no-input handoff status",
    "docs/KJVA_NO_INPUT_HANDOFF_STATUS.md",
    "no-new-KJVA-result boundary",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_real_report_run_doc(args.doc, args.protocol, args.makefile)
    if failures:
        for failure in failures:
            print(f"real-report run doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"real-report run doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--makefile", type=Path, default=DEFAULT_MAKEFILE)
    return parser


def validate_real_report_run_doc(
    doc: Path = DEFAULT_DOC,
    protocol: Path = DEFAULT_PROTOCOL,
    makefile: Path = DEFAULT_MAKEFILE,
) -> list[str]:
    missing = [str(path) for path in (doc, protocol, makefile) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    normalized = normalize_space(doc.read_text(encoding="utf-8"))
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_generated_outputs(doc, normalized))
    failures.extend(validate_protocol(protocol))
    failures.extend(validate_makefile(makefile))
    return failures


def validate_generated_outputs(doc: Path, normalized_doc: str) -> list[str]:
    failures: list[str] = []
    for output in EXPECTED_GENERATED_OUTPUTS:
        if normalize_space(f"`{output}`") not in normalized_doc:
            failures.append(f"{doc} missing generated output: {output}")
    return failures


def validate_protocol(path: Path) -> list[str]:
    data = read_toml(path)
    if isinstance(data, str):
        return [data]
    steps = {
        step.get("id"): step
        for step in data.get("steps", [])
        if isinstance(step, dict)
    }
    failures: list[str] = []
    if data.get("name") != "real_report_run":
        failures.append(f"{path} name drifted")
    if data.get("manifest_out") != "reports/real_report_run/protocol_run.manifest.json":
        failures.append(f"{path} manifest_out drifted")
    if data.get("max_parallel") != 1:
        failures.append(f"{path} max_parallel drifted")
    if data.get("progress_interval_seconds") != 15:
        failures.append(f"{path} progress_interval_seconds drifted")
    failures.extend(validate_preflight_step(path, steps.get("preflight")))
    failures.extend(validate_summary_step(path, steps.get("real_report_summary")))
    return failures


def validate_preflight_step(path: Path, step: Any) -> list[str]:
    if not isinstance(step, dict):
        return [f"{path} missing preflight step"]
    failures: list[str] = []
    if step.get("argv") != ["-m", "scripts.preflight_real_report_run"]:
        failures.append(f"{path} preflight argv drifted")
    if step.get("always_run") is not True:
        failures.append(f"{path} preflight always_run drifted")
    if step.get("outputs") != ["reports/real_report_run/preflight.json"]:
        failures.append(f"{path} preflight outputs drifted")
    inputs = set(step.get("inputs", []))
    missing_inputs = sorted(set(EXPECTED_PREFLIGHT_INPUTS) - inputs)
    if missing_inputs:
        failures.append(
            f"{path} preflight inputs missing: " + ", ".join(missing_inputs)
        )
    return failures


def validate_summary_step(path: Path, step: Any) -> list[str]:
    if not isinstance(step, dict):
        return [f"{path} missing real_report_summary step"]
    failures: list[str] = []
    if step.get("argv") != ["-m", "scripts.build_real_report_run_summary"]:
        failures.append(f"{path} real_report_summary argv drifted")
    if step.get("always_run") is not True:
        failures.append(f"{path} real_report_summary always_run drifted")
    if step.get("outputs") != list(EXPECTED_SUMMARY_OUTPUTS):
        failures.append(f"{path} real_report_summary outputs drifted")
    inputs = set(step.get("inputs", []))
    missing_inputs = sorted(set(EXPECTED_SUMMARY_INPUTS) - inputs)
    if missing_inputs:
        failures.append(
            f"{path} real_report_summary inputs missing: "
            + ", ".join(missing_inputs)
        )
    return failures


def validate_makefile(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if EXPECTED_MAKE_TARGET not in text:
        return [f"{path} real-report target drifted"]
    return []


def read_toml(path: Path) -> dict[str, Any] | str:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        return f"{path} is invalid TOML: {error}"


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
