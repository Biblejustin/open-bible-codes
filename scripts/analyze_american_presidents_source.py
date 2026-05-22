#!/usr/bin/env python3
"""Audit Torah-code.org American presidents source PDFs without running ELS results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_DATA_SOURCE = Path("reports/wrr_1994/torah_code_experiment_american_presidents_data.pdf")
DEFAULT_RULES_SOURCE = Path(
    "reports/wrr_1994/torah_code_experiment_english_hebrew_transliteration_rules.pdf"
)
DEFAULT_OUT = Path("reports/wrr_1994/american_presidents_source_records.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/american_presidents_source_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/american_presidents_protocol_anchors.csv")
DEFAULT_MD = Path("docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/american_presidents_source_audit.manifest.json")

RECORD_START_RE = re.compile(r"^\s*(\d+)\s+")
FIELDNAMES = [
    "record_index",
    "line_count",
    "last_name_spellings",
    "last_name_with_initial_spellings",
    "total_spellings",
    "has_continuation_only_initial_spellings",
]
SUMMARY_FIELDNAMES = [
    "data_pdf",
    "data_sha256",
    "data_bytes",
    "data_pages_from_text",
    "rules_pdf",
    "rules_sha256",
    "rules_bytes",
    "rules_pages_from_text",
    "data_records",
    "record_index_min",
    "record_index_max",
    "missing_record_indexes",
    "last_name_spellings",
    "last_name_with_initial_spellings",
    "total_spellings",
    "max_spellings_per_record",
    "records_with_initial_only_lines",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class PresidentRecord:
    record_index: int
    lines: tuple[str, ...]

    @property
    def last_name_spellings(self) -> int:
        return sum(1 for line in self.lines if last_name_field(line))

    @property
    def with_initial_spellings(self) -> int:
        return sum(1 for line in self.lines if initial_field(line))

    @property
    def has_continuation_only_initial_spellings(self) -> bool:
        return any(initial_field(line) and not last_name_field(line) for line in self.lines)

    def as_row(self) -> dict[str, object]:
        last = self.last_name_spellings
        initial = self.with_initial_spellings
        return {
            "record_index": self.record_index,
            "line_count": len(self.lines),
            "last_name_spellings": last,
            "last_name_with_initial_spellings": initial,
            "total_spellings": last + initial,
            "has_continuation_only_initial_spellings": int(
                self.has_continuation_only_initial_spellings
            ),
        }


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    data_text = extract_pdf_text(args.data_source)
    rules_text = extract_pdf_text(args.rules_source)
    records = parse_records(data_text)
    record_rows = [record.as_row() for record in records]
    summary = build_summary(args, data_text, rules_text, records)
    anchors = protocol_anchors(data_text, rules_text)
    write_csv(args.out, FIELDNAMES, record_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(record_rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-source", type=Path, default=DEFAULT_DATA_SOURCE)
    parser.add_argument("--rules-source", type=Path, default=DEFAULT_RULES_SOURCE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def extract_pdf_text(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise SystemExit("pdftotext is required; install poppler") from error
    return completed.stdout


def parse_records(text: str) -> list[PresidentRecord]:
    grouped: list[tuple[int, list[str]]] = []
    current_index: int | None = None
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.lstrip("\f").rstrip()
        if not is_data_line(line):
            continue
        match = RECORD_START_RE.match(line)
        if match:
            if current_index is not None:
                grouped.append((current_index, current_lines))
            current_index = int(match.group(1))
            current_lines = [line]
            continue
        if current_index is not None:
            current_lines.append(line)
    if current_index is not None:
        grouped.append((current_index, current_lines))
    return [PresidentRecord(index, tuple(lines)) for index, lines in grouped]


def is_data_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("No "):
        return False
    if stripped.startswith("Spellings"):
        return False
    if stripped.startswith("Last Name"):
        return False
    return bool(RECORD_START_RE.match(line) or last_name_field(line) or initial_field(line))


def last_name_field(line: str) -> str:
    return line[27:49].strip() if len(line) > 27 else ""


def initial_field(line: str) -> str:
    return line[49:].strip() if len(line) > 49 else ""


def build_summary(
    args: argparse.Namespace,
    data_text: str,
    rules_text: str,
    records: list[PresidentRecord],
) -> dict[str, object]:
    rows = [record.as_row() for record in records]
    indexes = [record.record_index for record in records]
    missing = []
    if indexes:
        expected = set(range(min(indexes), max(indexes) + 1))
        missing = sorted(expected.difference(indexes))
    last_total = sum(int(row["last_name_spellings"]) for row in rows)
    initial_total = sum(int(row["last_name_with_initial_spellings"]) for row in rows)
    return {
        "data_pdf": str(args.data_source),
        "data_sha256": sha256(args.data_source),
        "data_bytes": args.data_source.stat().st_size,
        "data_pages_from_text": pages_from_text(data_text),
        "rules_pdf": str(args.rules_source),
        "rules_sha256": sha256(args.rules_source),
        "rules_bytes": args.rules_source.stat().st_size,
        "rules_pages_from_text": pages_from_text(rules_text),
        "data_records": len(records),
        "record_index_min": min(indexes, default=""),
        "record_index_max": max(indexes, default=""),
        "missing_record_indexes": " ".join(str(index) for index in missing),
        "last_name_spellings": last_total,
        "last_name_with_initial_spellings": initial_total,
        "total_spellings": last_total + initial_total,
        "max_spellings_per_record": max((int(row["total_spellings"]) for row in rows), default=0),
        "records_with_initial_only_lines": sum(
            int(row["has_continuation_only_initial_spellings"]) for row in rows
        ),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def pages_from_text(text: str) -> int:
    stripped = text.rstrip("\f\n\r ")
    if not stripped:
        return 0
    return stripped.count("\f") + 1


def protocol_anchors(data_text: str, rules_text: str) -> list[dict[str, str]]:
    data_normalized = re.sub(r"\s+", " ", data_text)
    rules_normalized = re.sub(r"\s+", " ", rules_text)
    checks = [
        (
            "data",
            "president_number_column",
            "No President" in data_normalized,
            "numbered president data table found",
        ),
        (
            "data",
            "last_name_spellings_column",
            "Last Name Hebrew" in data_normalized and "Spellings" in data_normalized,
            "last-name spelling column found",
        ),
        (
            "data",
            "initial_spellings_column",
            "Last Name and First" in data_normalized
            and "Initial Hebrew Spellings" in data_normalized,
            "initial-spelling column found",
        ),
        (
            "rules",
            "english_to_hebrew_title",
            "Transliteration of English Names Into Hebrew" in rules_normalized,
            "transliteration rule title found",
        ),
        (
            "rules",
            "consonant_mapping_table",
            "letter to letter correspondence" in rules_normalized,
            "consonant mapping table found",
        ),
        (
            "rules",
            "vowel_variability_rule",
            "vowels are the place where there is some variability" in rules_normalized,
            "vowel variability rule found",
        ),
        (
            "rules",
            "final_vowel_explicit_rule",
            "last sound of a name is a vowel" in rules_normalized,
            "final-vowel rule found",
        ),
        (
            "rules",
            "basic_name_and_initial_variations",
            "first initial" in rules_normalized,
            "initial-variant rule found",
        ),
        (
            "rules",
            "double_consonant_variations",
            "double consonant" in rules_normalized,
            "double-consonant rule found",
        ),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if found else "missing",
            "diagnostic": diagnostic if found else "anchor text not found",
        }
        for source, anchor, found, diagnostic in checks
    ]


def write_markdown(
    path: Path,
    summary: dict[str, object],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# American Presidents Source Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Sources",
        "",
        "- Data PDF: `https://www.torah-code.org/experiments/americanpresidents_nasi_data.pdf`",
        "- Transliteration rules PDF: `https://www.torah-code.org/experiments/english_hebrew_transliteration_rule.pdf`",
        f"- Data SHA-256: `{summary['data_sha256']}`",
        f"- Rules SHA-256: `{summary['rules_sha256']}`",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| data PDF pages from extracted text | {summary['data_pages_from_text']} |",
        f"| rules PDF pages from extracted text | {summary['rules_pages_from_text']} |",
        f"| data records | {summary['data_records']} |",
        f"| record index minimum | {summary['record_index_min']} |",
        f"| record index maximum | {summary['record_index_max']} |",
        f"| last-name spelling rows | {summary['last_name_spellings']} |",
        f"| last-name plus initial spelling rows | {summary['last_name_with_initial_spellings']} |",
        f"| total spelling rows | {summary['total_spellings']} |",
        f"| maximum spelling rows per record | {summary['max_spellings_per_record']} |",
        f"| records with initial-only continuation lines | {summary['records_with_initial_only_lines']} |",
        "",
        "## Protocol Anchors",
        "",
        f"Found anchors: {anchor_counts.get('found', 0)} of {len(anchors)}.",
        "",
        "| Source | Anchor | Status | Diagnostic |",
        "| --- | --- | --- | --- |",
    ]
    for anchor in anchors:
        lines.append(
            f"| {anchor['source']} | `{anchor['anchor']}` | {anchor['status']} | {anchor['diagnostic']} |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This audit only verifies that the data and transliteration-rule sources can",
            "be parsed into a stable source-shape summary. It does not normalize Hebrew",
            "spellings, choose among variants, define controls, compute ELS hits, or",
            "compare against random baselines.",
            "",
            "Next result-bearing step, if chosen later: write a separate preregistered",
            "American-presidents protocol that freezes the source rows, transliteration",
            "policy, Genesis/Torah text, skip caps, compactness metric, and controls",
            "before any ELS search.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, object],
    anchors: list[dict[str, str]],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "sources": {
            "data": str(args.data_source),
            "rules": str(args.rules_source),
        },
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "records": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-shape audit only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
