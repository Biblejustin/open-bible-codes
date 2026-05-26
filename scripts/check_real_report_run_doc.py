#!/usr/bin/env python3
"""Validate real-report run documentation names current preflight guards."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_DOC = Path("docs/REAL_REPORT_RUN.md")

REQUIRED_PHRASES = (
    "python3 -m scripts.run_protocol protocols/real_report_run.toml --resume",
    "make real-report",
    "`reports/real_report_run/preflight.json`",
    "`reports/real_report_run/summary.md`",
    "`reports/INDEX.md`",
    "claim-catalog summary table stays aligned with `claims/claim_catalog.csv`",
    "final report highlights markdown matches the deterministic builder output",
    "centered occurrence index markdown matches the deterministic builder output",
    "strongest candidate deep-dive markdown matches the deterministic builder output",
    "hypothesis-testing source audit doc keeps the source-status/no-result boundary visible",
    "research missing model pages audit doc keeps the missing level-2/3 model page boundary visible",
    "WRR adjacent source audit and simulation docs keep source-shape and simulation-only boundaries visible",
    "critical-omission follow-up docs keep Setup, Method, Results, and Cautions sections plus current headline counts visible",
    "Cities source-row lock status",
    "Cities source-row lock decision records stay aligned to the 14-row evidence packet before any populated source-row lock can pass preflight",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_real_report_run_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"real-report run doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"real-report run doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_real_report_run_doc(doc: Path = DEFAULT_DOC) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    normalized = normalize_space(doc.read_text(encoding="utf-8"))
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
