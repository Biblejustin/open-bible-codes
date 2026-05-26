#!/usr/bin/env python3
"""Validate WRR-adjacent source audit docs keep non-result boundaries explicit."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocRule:
    path: Path
    required_phrases: tuple[str, ...]


DOC_RULES = (
    DocRule(
        Path("docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md"),
        (
            "# Torah-Code Research Model Simulation",
            "Status: simulation harness; not a Torah-code result.",
            "transparent power/sanity check",
            "replication claim.",
            "This is model-design scaffolding only.",
            "ELS cylinder geometry remains separate work.",
        ),
    ),
    DocRule(
        Path("docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md"),
        (
            "# Torah-Code ELS Model Simulation",
            "Status: simulation harness; not a Torah-code result.",
            "does not test real Torah text.",
            "source-published set of weights.",
            "complete source-method reconstruction.",
        ),
    ),
    DocRule(
        Path("docs/GANS_COMMUNITIES_SOURCE_AUDIT.md"),
        (
            "# Gans Communities Source Audit",
            "Status: source-shape audit only.",
            "compactness calculation",
            "| data records | 66 |",
            "This audit makes the source usable as a future locked-data intake target.",
            "It does not yet normalize Hebrew spellings",
            "CITIES_EXTRACTABLE_TEXT_REVIEW.md",
            "Next result-bearing step, if chosen later",
        ),
    ),
    DocRule(
        Path("docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md"),
        (
            "# American Presidents Source Audit",
            "Status: source-shape audit only.",
            "not a claim-ready replication.",
            "| data records | 42 |",
            "| total spelling rows | 279 |",
            "be parsed into a stable source-shape summary",
            "Next result-bearing step, if chosen later",
        ),
    ),
    DocRule(
        Path("docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md"),
        (
            "# Witztum Birth Dates Source Audit",
            "Status: source-shape audit only.",
            "not a claim-ready replication.",
            "| total table rows | 28 |",
            "| S1 rows | 14 |",
            "| S2 rows | 14 |",
            "It does not normalize terms into",
            "Next result-bearing step, if chosen later",
        ),
    ),
    DocRule(
        Path("docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md"),
        (
            "# Israeli Prime Ministers Source Audit",
            "Status: source-shape audit only.",
            "not a claim-ready replication.",
            "| PDF prime-minister rows | 12 |",
            "| HTML detail pages found | 8 |",
            "missing detail-source coverage",
            "No term normalization, ELS search",
        ),
    ),
    DocRule(
        Path("docs/COLINEAR_ELS_SOURCE_AUDIT.md"),
        (
            "# Co-linear ELS Source Audit",
            "Status: source-shape audit only.",
            "not a claim-ready co-linear ELS reproduction.",
            "| PLS pair rows extracted | 6060 |",
            "| reviewed subset rows extracted | 502 |",
            "future co-linear ELS/verse protocol",
            "not normalize Hebrew terms",
        ),
    ),
    DocRule(
        Path("docs/CITIES_SOURCE_CHAIN_AUDIT.md"),
        (
            "# Cities Source Chain Audit",
            "Status: source-shape audit only.",
            "not a claim-ready replication.",
            "| source files scanned | 13 |",
            "| `.pdf` files that are HTML wrappers | 6 |",
            "must not be treated as source data",
            "No city-name rows are normalized",
        ),
    ),
    DocRule(
        Path("docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md"),
        (
            "# Event/Object Experiment Source Audit",
            "Status: source-shape audit only.",
            "not a claim-ready replication.",
            "| source files scanned | 8 |",
            "| machine data rows extracted | 65 |",
            "declared status for event/object experiment pages",
            "does not normalize Hebrew spellings",
        ),
    ),
    DocRule(
        Path("docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md"),
        (
            "# Under-Construction Experiment Source Audit",
            "Status: source-status audit only.",
            "not a claim-ready replication.",
            "| source files scanned | 6 |",
            "| under-construction pages | 6 |",
            "should not supply",
            "data-bearing pages and records fresh checksums.",
        ),
    ),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_adjacent_source_audit_docs(args.root)
    if failures:
        for failure in failures:
            print(f"WRR adjacent source audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR adjacent source audit docs ok: {args.root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    return parser


def validate_adjacent_source_audit_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for rule in DOC_RULES:
        doc = root / rule.path
        if not doc.exists():
            failures.append(f"{rule.path} is missing")
            continue
        text = doc.read_text(encoding="utf-8")
        for phrase in rule.required_phrases:
            if phrase not in text:
                failures.append(f"{rule.path} missing phrase: {phrase}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
