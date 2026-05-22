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
DEFAULT_SPELLINGS_OUT = Path("reports/wrr_1994/american_presidents_source_spellings.csv")
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
SPELLING_FIELDNAMES = [
    "record_index",
    "spelling_row_index",
    "spelling_type",
    "hebrew_spelling",
    "raw_line",
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
    "machine_spelling_rows",
    "max_spellings_per_record",
    "records_with_initial_only_lines",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class PresidentLine:
    raw_line: str
    last_name: str
    initial: str


@dataclass(frozen=True)
class PresidentRecord:
    record_index: int
    lines: tuple[PresidentLine, ...]

    @property
    def last_name_spellings(self) -> int:
        return sum(1 for line in self.lines if line.last_name)

    @property
    def with_initial_spellings(self) -> int:
        return sum(1 for line in self.lines if line.initial)

    @property
    def has_continuation_only_initial_spellings(self) -> bool:
        return any(line.initial and not line.last_name for line in self.lines)

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
    spelling_rows = spelling_rows_from_records(records)
    summary = build_summary(args, data_text, rules_text, records)
    anchors = protocol_anchors(data_text, rules_text)
    write_csv(args.out, FIELDNAMES, record_rows)
    write_csv(args.spellings_out, SPELLING_FIELDNAMES, spelling_rows)
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
    parser.add_argument("--spellings-out", type=Path, default=DEFAULT_SPELLINGS_OUT)
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
    grouped: list[tuple[int, list[PresidentLine]]] = []
    current_index: int | None = None
    current_lines: list[PresidentLine] = []
    last_col = 27
    initial_col = 49
    for raw_line in text.splitlines():
        line = raw_line.lstrip("\f").rstrip()
        header_columns = spelling_columns(line)
        if header_columns is not None:
            last_col, initial_col = header_columns
            continue
        if not is_data_line(line, last_col, initial_col):
            continue
        parsed_line = parse_president_line(line, last_col, initial_col)
        match = RECORD_START_RE.match(line)
        if match:
            if current_index is not None:
                grouped.append((current_index, current_lines))
            current_index = int(match.group(1))
            current_lines = [parsed_line]
            continue
        if current_index is not None:
            current_lines.append(parsed_line)
    if current_index is not None:
        grouped.append((current_index, current_lines))
    return [PresidentRecord(index, tuple(lines)) for index, lines in grouped]


def spelling_rows_from_records(records: list[PresidentRecord]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in records:
        row_index = 0
        for line in record.lines:
            stripped = line.raw_line.strip()
            last_name = line.last_name
            if last_name:
                row_index += 1
                rows.append(
                    {
                        "record_index": record.record_index,
                        "spelling_row_index": row_index,
                        "spelling_type": "last_name",
                        "hebrew_spelling": last_name,
                        "raw_line": stripped,
                    }
                )
            initial = line.initial
            if initial:
                row_index += 1
                rows.append(
                    {
                        "record_index": record.record_index,
                        "spelling_row_index": row_index,
                        "spelling_type": "last_name_with_initial",
                        "hebrew_spelling": initial,
                        "raw_line": stripped,
                    }
                )
    return rows


def spelling_columns(line: str) -> tuple[int, int] | None:
    last_col = line.find("Last Name Hebrew")
    initial_col = line.find("Last Name and First")
    if last_col < 0 or initial_col < 0:
        return None
    return last_col, initial_col


def parse_president_line(line: str, last_col: int, initial_col: int) -> PresidentLine:
    last_name, initial = split_spelling_fields(line, initial_col)
    return PresidentLine(
        raw_line=line,
        last_name=last_name,
        initial=initial,
    )


def is_data_line(line: str, last_col: int = 27, initial_col: int = 49) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("No "):
        return False
    if stripped.startswith("Spellings"):
        return False
    if stripped.startswith("Last Name"):
        return False
    return bool(
        RECORD_START_RE.match(line)
        or last_name_field(line, last_col, initial_col)
        or initial_field(line, initial_col)
    )


def split_spelling_fields(line: str, initial_col: int = 49) -> tuple[str, str]:
    stripped = line.strip()
    if not stripped:
        return "", ""
    parts = re.split(r"\s{2,}", stripped)
    is_record_start = bool(RECORD_START_RE.match(line))
    if is_record_start and len(parts) >= 3:
        return clean_last_name_candidate(parts[-2]), parts[-1].strip()
    if not is_record_start and len(parts) >= 2:
        return clean_last_name_candidate(parts[-2]), parts[-1].strip()
    if not is_record_start and len(parts) == 1:
        first_nonspace = len(line) - len(line.lstrip())
        if first_nonspace >= initial_col - 3:
            return "", parts[0].strip()
        return clean_last_name_candidate(parts[0]), ""
    return "", ""


def clean_last_name_candidate(value: str) -> str:
    candidate = value.strip()
    if re.search(r"[A-Z]\.|[A-Z][a-z]", candidate):
        return candidate.split()[-1]
    return candidate


def last_name_field(line: str, last_col: int = 27, initial_col: int = 49) -> str:
    del last_col
    return split_spelling_fields(line, initial_col)[0]


def initial_field(line: str, initial_col: int = 49) -> str:
    return split_spelling_fields(line, initial_col)[1]


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
        "machine_spelling_rows": len(spelling_rows_from_records(records)),
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
        f"| machine spelling rows extracted | {summary['machine_spelling_rows']} |",
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
            "spellings": str(args.spellings_out),
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
