#!/usr/bin/env python3
"""Validate KJVA source-candidate status rollup boundaries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/KJVA_SOURCE_CANDIDATE_STATUS.md")
DEFAULT_LINKED_DOCS = (
    Path("docs/KJVA_APOCRYPHA_BRIDGE_NEXT_REPLICATION_DESIGN.md"),
    Path("docs/APOCRYPHA_SOURCE_COVERAGE.md"),
    Path("docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md"),
    Path("docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md"),
    Path("docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md"),
    Path("docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md"),
)

REQUIRED_PHRASES = (
    "# KJVA Source Candidate Status",
    "Status: source-status rollup only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "Ready independent KJVA replication sources: 0.",
    "Possible independent KJVA metadata candidates: 1.",
    "Result-ready sources: 0.",
    "source-lock ready sources: 0.",
    "No result-bearing KJVA replication is source-ready yet.",
    "current eBible KJV + Apocrypha source family",
    "14 apocrypha/deuterocanon books, 5720 verses, and 593090 normalized letters",
    "not an independent replication source",
    "CrossWire GitLab KJV/KJVA",
    "possible independent metadata candidate",
    "`kjva.osis.xml` and `kjvdc.xml` path names",
    "no local source import, verse mapping, collation, checksum lock, or source-use decision exists yet",
    "Wikisource Ballantyne 1911 KJV + Apocrypha",
    "metadata-level future source candidate",
    "36 existing KJV book links, 30 KJV redlinks",
    "0 apocrypha/deuterocanon book links",
    "`seven1m/open-bibles`",
    "KJV-only metadata candidate",
    "not a KJVA/apocrypha source candidate",
    "does not import Bible text, normalize verses, run ELS searches",
    "does not change any KJVA result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:result-bearing replication is ready|source-ready replication|"
    r"corpus import ready|claim report|claim-level|proved|proves|"
    r"conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "not a claim-ready replication",
    "No result-bearing KJVA replication is source-ready yet.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_source_candidate_status_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"KJVA source candidate status doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA source candidate status doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_kjva_source_candidate_status_doc(
    doc: Path = DEFAULT_DOC,
    *,
    linked_docs: tuple[Path, ...] = DEFAULT_LINKED_DOCS,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    root = doc.parent.parent if doc.parent.name == "docs" else Path(".")
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    for linked_doc in linked_docs:
        linked_path = linked_doc if linked_doc.is_absolute() else root / linked_doc
        if not linked_path.exists():
            failures.append(f"{linked_path} is missing")
            continue
        reference = f"`{linked_doc.as_posix()}`"
        if reference not in text:
            failures.append(f"{doc} missing linked doc reference: {reference}")
    failures.extend(validate_no_overclaim(doc, text))
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


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
