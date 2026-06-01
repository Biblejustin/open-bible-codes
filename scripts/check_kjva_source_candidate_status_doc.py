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
    Path("docs/KJVA_CURRENT_SOURCE_LOCK_SIDECAR.md"),
    Path("docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md"),
    Path("docs/KJVA_GUTENBERG_CANDIDATE_SOURCE_AUDIT.md"),
    Path("docs/KJVA_GUTENBERG_BOOK_COVERAGE_PROBE.md"),
    Path("docs/KJVA_GUTENBERG_CANDIDATE_CHECKSUM_SIDECAR.md"),
    Path("docs/KJVA_GUTENBERG_SOURCE_LOCK_PREP.md"),
    Path("docs/KJVA_GUTENBERG_SOURCE_LOCK_DECISION_PACKET.md"),
    Path("docs/KJVA_GUTENBERG_SOURCE_LOCK_BLOCKER_PACKET.md"),
    Path("docs/KJVA_HAKKAAC_APOCRYPHA_BOUNDARY_CANDIDATE.md"),
    Path("docs/KJVA_HAKKAAC_APOCRYPHA_MARKER_COVERAGE.md"),
    Path("docs/KJVA_HAKKAAC_APOCRYPHA_COLLATION_AUDIT.md"),
    Path("docs/KJVA_HAKKAAC_SOURCE_LOCK_DECISION_PACKET.md"),
    Path("docs/KJVA_GUTENBERG_HAKKAAC_SPLIT_SOURCE_ROLE_SIDECAR.md"),
    Path("docs/KJVA_SOURCE_POLICY_BLOCKER_PACKET.md"),
    Path("docs/KJVA_NEXT_RESULT_GATE.md"),
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
    "Possible independent KJVA metadata candidates: 2.",
    "Public-domain split KJV+Apocrypha coverage candidates needing collation: 1.",
    "Result-ready sources: 0.",
    "source-lock ready sources: 0.",
    "No result-bearing KJVA replication is source-ready yet.",
    "The next-result gate records 11 gate rows",
    "only current-source rerun reproducibility is ready",
    "10 gates are blocked",
    "new result-bearing KJVA output is not allowed",
    "current eBible KJV + Apocrypha source family",
    "current eBible KJVA source-lock sidecar",
    "14 apocrypha/deuterocanon books, 5720 verses, and 593090 normalized letters",
    "CSV SHA-256 `f4f4549c7323de20a6cdd7aa74aeae32d184b2b6a1a51cd41390540efd710360`",
    "full 80-book order",
    "36822 verses",
    "not an independent replication source",
    "CrossWire GitLab KJV/KJVA",
    "possible independent metadata candidate",
    "`kjva.osis.xml` and `kjvdc.xml` path names",
    "DistributionLicense=GPL",
    "Crown rights language",
    "no local source import, verse mapping, collation, checksum lock, or source-use decision exists yet",
    "Project Gutenberg eBook 30",
    "eBook 124",
    "public-domain-USA split KJV+Apocrypha coverage candidate",
    "The Bible, King James Version, Complete",
    "Public domain in the USA.",
    "66 KJV book headings",
    "14 tracked KJVA Apocrypha/deuterocanon coverage rows",
    "Epistle of Jeremiah",
    "source-lock prep count comparison",
    "Gutenberg checksum sidecar",
    "RDF and plain-text SHA-256 identifiers",
    "2 checksum records ready",
    "0 source-use ready pages",
    "0 verse-import ready pages",
    "source-lock decision packet",
    "source-lock blocker packet",
    "Hakkaac boundary-candidate audit",
    "Hakkaac full-marker coverage audit",
    "Hakkaac ignored-local collation audit",
    "Hakkaac source-lock decision packet",
    "exact verse-count agreement for all 66 KJV books",
    "12 of 14 tracked Apocrypha/deuterocanon books",
    "Sirach at one fewer marker",
    "Prayer of Manasseh with no body verse markers",
    "recommends Gutenberg source order",
    "rolling the separate Epistle of Jeremiah source section into BAR",
    "blocking source lock until Sirach and Prayer of Manasseh",
    "citable non-text collation decisions",
    "Sirach marker-only gap is `SIR 44:23`",
    "detected Prayer of Manasseh source section has 0 body markers against 15 local markers",
    "visible markers for Sirach 44:23 and Prayer of Manasseh 1..15",
    "public-domain note",
    "exact marker-count agreement for all 14 tracked Apocrypha/deuterocanon books",
    "5720 source markers",
    "5720 local markers",
    "173 chapter rows",
    "0 chapter drift rows",
    "marker-coverage audit only",
    "5719 of 5720 exact normalized verse matches",
    "one `SIR 19:1` one-letter normalized length drift",
    "13 of 14 exact book-stream matches",
    "exact `SIR 44:23` and `MAN 1:1..15` blocker rows",
    "no tracked Bible text",
    "keeps Hakkaac as candidate evidence only",
    "keeps current eBible KJVA as the rerun baseline",
    "blocks Project Gutenberg plus Hakkaac split-source use",
    "The split-source role sidecar now writes that role/order boundary as planning-only evidence",
    "Hakkaac is marker/collation witness-only",
    "no result-bearing source lock is ready",
    "source-policy blocker packet",
    "5 policy option rows, 7 blocker rows, 2 policy-ready options, and 3 blocked options",
    "Only the current eBible rerun path and deferral of new KJVA result work are policy-ready",
    "Project Gutenberg-only, Project Gutenberg plus Hakkaac, and Hakkaac-primary streams remain blocked",
    "Sirach `SIR 19:1` drift decision",
    "source-role sidecar",
    "candidate audit only",
    "possible split-source replication candidate",
    "Baruch/Epistle handling decision",
    "Wikisource Ballantyne 1911 KJV + Apocrypha",
    "metadata-level future source candidate",
    "36 existing KJV book links, 30 KJV redlinks",
    "0 apocrypha/deuterocanon book links",
    "`seven1m/open-bibles`",
    "KJV-only metadata candidate",
    "not a KJVA/apocrypha source candidate",
    "does not import Bible text, normalize verses, run ELS searches",
    "does not change any KJVA result status",
    "next-result gate",
    "source policy, source text, verse map, collation, drift/boundary, fresh terms, leakage audit, fixed controls, and study lock all pass",
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
