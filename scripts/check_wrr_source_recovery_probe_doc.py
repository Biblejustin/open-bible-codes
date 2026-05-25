#!/usr/bin/env python3
"""Validate WRR source-recovery probe doc keeps live-source limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_RECOVERY_PROBE.md")

EXPECTED_PROBE_LABELS = (
    "torah_code_research_program_1",
    "torah_code_research_program_1_shtml",
    "torah_code_research_program_2",
    "torah_code_research_program_2_shtml",
    "torah_code_research_model_overview",
    "torah_code_research_model_overview_shtml",
    "torah_code_research_geometric_model_level_1",
    "torah_code_research_geometric_model_level_1_shtml",
    "torah_code_research_geometric_model_level_2",
    "torah_code_research_geometric_model_level_2_shtml",
    "torah_code_research_geometric_model_level_3",
    "torah_code_research_geometric_model_level_3_shtml",
    "torah_code_research_els_model_level_1",
    "torah_code_research_els_model_level_1_shtml",
    "torah_code_research_els_model_level_2",
    "torah_code_research_els_model_level_2_shtml",
    "torah_code_research_els_model_level_3",
    "torah_code_research_els_model_level_3_shtml",
)

REQUIRED_PHRASES = (
    "# WRR Source Recovery Probe",
    "Status: live-source recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "claim-ready source decisions",
    "| downloads probed | 18 |",
    "| rows where expected label appeared | 0 |",
    "| redirected rows | 18 |",
    "| final URL is Torah-code root | 18 |",
    "| canonical URL is Torah-code root | 18 |",
    "| unrelated slot/gambling markers | 18 |",
    "| usable current source rows | 0 |",
    "Current recovery status: `no_live_sources_recovered`.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_recovery_probe_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-recovery probe doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_recovery_probe_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    present_labels = probe_labels(text)
    missing_labels = sorted(set(EXPECTED_PROBE_LABELS) - present_labels)
    if missing_labels:
        failures.append(
            f"{doc} missing probe labels: " + ", ".join(missing_labels)
        )
    return failures


def probe_labels(text: str) -> set[str]:
    labels: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 9 and cells[0].startswith("torah_code_research_"):
            labels.add(cells[0])
    return labels


if __name__ == "__main__":
    raise SystemExit(main())
