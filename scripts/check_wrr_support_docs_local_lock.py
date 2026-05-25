#!/usr/bin/env python3
"""Validate WRR support docs keep the locked-local boundary current."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PHRASES_BY_DOC = {
    Path("docs/WRR_REPLICATION_PLAN.md"): (
        "Status: local locked-method run complete; exact published WRR reproduction",
        "full cap-1000 corrected distances over 182 observed rows",
        "999,999 date-label permutation",
        "72 defined observed c-values over 182 observed rows",
        "rho0 `0.000404`",
        "not an exact published WRR reproduction",
        "source-cited 163-distance count",
    ),
    Path("docs/WRR_METHODOLOGY_GAPS.md"): (
        "72 defined, 110 ordinary-not-valid, 0 under-minimum",
        "keep-all cap-1000 999,999-permutation run",
        "182 observed rows with 72 defined c-values",
        "Bonferroni rho0 `0.000404`",
        "current manual source records locked unchanged",
        "not exact published reproduction",
    ),
    Path("docs/WRR_CORRECTED_DISTANCE_NOTES.md"): (
        "printed `D(w)` as main",
        "reported-program `D(w)` as required sensitivity",
        "keep_all_working_source cap-1000 local lock",
        "999,999 date-label permutation",
        "72 defined observed c-values over 182 observed rows",
        "Bonferroni rho0 `0.000404`",
        "locked local evidence, not exact published reproduction",
    ),
}

FORBIDDEN_PHRASES = (
    "final `D(w)` formula decision",
    "optimized full corrected-distance run over the final locked pair universe",
    "choose one before final `D(w)` runs",
    "because the pair universe and `D(w)` formula are not locked",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_support_docs(args.root)
    if failures:
        for failure in failures:
            print(f"WRR support-doc local-lock failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR support docs local-lock boundary ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_support_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    combined = ""
    for relative_path, required_phrases in REQUIRED_PHRASES_BY_DOC.items():
        doc = root / relative_path
        if not doc.exists():
            failures.append(f"{relative_path} is missing")
            continue
        text = doc.read_text(encoding="utf-8")
        normalized_text = normalize_space(text)
        combined += "\n" + normalized_text
        for phrase in required_phrases:
            if normalize_space(phrase) not in normalized_text:
                failures.append(f"{relative_path} missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if normalize_space(phrase) in combined:
            failures.append(f"support docs contain stale phrase: {phrase}")
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
