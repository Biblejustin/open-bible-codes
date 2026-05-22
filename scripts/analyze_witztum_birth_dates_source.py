#!/usr/bin/env python3
"""Audit Witztum Genesis birth-date source PDFs without running ELS results."""

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


DEFAULT_PAPER_SOURCE = Path("reports/wrr_1994/witztum_birth_dates.pdf")
DEFAULT_DATA_SOURCE = Path("reports/wrr_1994/witztum_birth_dates_data.pdf")
DEFAULT_OUT = Path("reports/wrr_1994/witztum_birth_dates_source_rows.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/witztum_birth_dates_source_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/witztum_birth_dates_protocol_anchors.csv")
DEFAULT_MD = Path("docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/witztum_birth_dates_source_audit.manifest.json")

TABLE_START_RE = re.compile(r"^\s*Table\s+([12])\s*$", re.MULTILINE)
ROW_START_RE = re.compile(r"^([A-Za-z][A-Za-z’']*)\s{2,}")
HEADING_WORDS = {"Personality", "Name", "Date", "References", "Sample", "List"}

ROW_FIELDNAMES = [
    "sample",
    "personality",
    "line_count",
    "name_variants",
    "date_forms",
    "starred_date_forms",
    "pair_forms_before_length_filter",
    "pair_forms_after_star_filter",
]
SUMMARY_FIELDNAMES = [
    "paper_pdf",
    "paper_sha256",
    "paper_bytes",
    "paper_pages_from_text",
    "data_pdf",
    "data_sha256",
    "data_bytes",
    "data_pages_from_text",
    "sample_tables",
    "total_table_rows",
    "s1_rows",
    "s2_rows",
    "s1_name_variants",
    "s2_name_variants",
    "s1_date_forms",
    "s2_date_forms",
    "s1_starred_date_forms",
    "s2_starred_date_forms",
    "s1_pair_forms_after_star_filter",
    "s2_pair_forms_after_star_filter",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class BirthDateRow:
    sample: str
    personality: str
    lines: tuple[str, ...]

    @property
    def name_variants(self) -> int:
        return len(split_forms(name_text(self.lines)))

    @property
    def date_forms(self) -> int:
        return len(split_forms(date_text(self.lines)))

    @property
    def starred_date_forms(self) -> int:
        return sum(1 for form in split_forms(date_text(self.lines)) if form.startswith("*"))

    @property
    def pair_forms_before_length_filter(self) -> int:
        return self.name_variants * self.date_forms

    @property
    def pair_forms_after_star_filter(self) -> int:
        return self.name_variants * (self.date_forms - self.starred_date_forms)

    def as_row(self) -> dict[str, object]:
        return {
            "sample": self.sample,
            "personality": self.personality,
            "line_count": len(self.lines),
            "name_variants": self.name_variants,
            "date_forms": self.date_forms,
            "starred_date_forms": self.starred_date_forms,
            "pair_forms_before_length_filter": self.pair_forms_before_length_filter,
            "pair_forms_after_star_filter": self.pair_forms_after_star_filter,
        }


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    paper_text = extract_pdf_text(args.paper_source)
    data_text = extract_pdf_text(args.data_source)
    rows = parse_birth_date_rows(data_text)
    row_dicts = [row.as_row() for row in rows]
    summary = build_summary(args, paper_text, data_text, rows)
    anchors = protocol_anchors(paper_text, data_text)
    write_csv(args.out, ROW_FIELDNAMES, row_dicts)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(row_dicts), started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-source", type=Path, default=DEFAULT_PAPER_SOURCE)
    parser.add_argument("--data-source", type=Path, default=DEFAULT_DATA_SOURCE)
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


def parse_birth_date_rows(text: str) -> list[BirthDateRow]:
    rows: list[BirthDateRow] = []
    for table_number, table_text in table_sections(text).items():
        sample = f"S{table_number}"
        current_personality: str | None = None
        current_lines: list[str] = []
        for raw_line in table_text.splitlines():
            line = raw_line.rstrip()
            if not line.strip() or is_table_header(line):
                continue
            match = ROW_START_RE.match(line)
            if match and match.group(1) not in HEADING_WORDS:
                if current_personality is not None:
                    rows.append(BirthDateRow(sample, current_personality, tuple(current_lines)))
                current_personality = match.group(1)
                current_lines = [line]
                continue
            if current_personality is not None:
                current_lines.append(line)
        if current_personality is not None:
            rows.append(BirthDateRow(sample, current_personality, tuple(current_lines)))
    return rows


def table_sections(text: str) -> dict[str, str]:
    starts: list[tuple[str, int]] = []
    for match in TABLE_START_RE.finditer(text):
        starts.append((match.group(1), match.end()))
    sections: dict[str, str] = {}
    for position, (number, start) in enumerate(starts):
        end = starts[position + 1][1] if position + 1 < len(starts) else len(text)
        section = text[start:end]
        stop_markers = [
            "This table presents sample S1",
            "(Note that S2 differs",
            "References and notes",
        ]
        stop_indexes = [section.find(marker) for marker in stop_markers if marker in section]
        if stop_indexes:
            section = section[: min(stop_indexes)]
        sections[number] = section
    return sections


def is_table_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("Personality") or stripped.startswith("Name") or stripped.startswith("Date")


def name_text(lines: tuple[str, ...]) -> str:
    names, _dates = line_fields(lines)
    return " ".join(names)


def date_text(lines: tuple[str, ...]) -> str:
    _names, dates = line_fields(lines)
    return " ".join(dates)


def line_fields(lines: tuple[str, ...]) -> tuple[list[str], list[str]]:
    names: list[str] = []
    dates: list[str] = []
    for line in lines:
        start_match = ROW_START_RE.match(line)
        if start_match:
            parts = re.split(r"\s{2,}", line.strip(), maxsplit=2)
            if len(parts) >= 2:
                names.append(parts[1].strip())
            if len(parts) >= 3:
                dates.append(parts[2].strip())
            continue
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        if indent >= 29:
            dates.append(stripped)
        else:
            names.append(stripped)
    return names, dates


def split_forms(text: str) -> list[str]:
    cleaned = text.replace(".", " ")
    return [part.strip() for part in cleaned.split(",") if part.strip()]


def build_summary(
    args: argparse.Namespace,
    paper_text: str,
    data_text: str,
    rows: list[BirthDateRow],
) -> dict[str, object]:
    row_dicts = [row.as_row() for row in rows]
    by_sample = {
        sample: [row for row in row_dicts if row["sample"] == sample]
        for sample in ("S1", "S2")
    }
    return {
        "paper_pdf": str(args.paper_source),
        "paper_sha256": sha256(args.paper_source),
        "paper_bytes": args.paper_source.stat().st_size,
        "paper_pages_from_text": pages_from_text(paper_text),
        "data_pdf": str(args.data_source),
        "data_sha256": sha256(args.data_source),
        "data_bytes": args.data_source.stat().st_size,
        "data_pages_from_text": pages_from_text(data_text),
        "sample_tables": len(table_sections(data_text)),
        "total_table_rows": len(rows),
        "s1_rows": len(by_sample["S1"]),
        "s2_rows": len(by_sample["S2"]),
        "s1_name_variants": sum(int(row["name_variants"]) for row in by_sample["S1"]),
        "s2_name_variants": sum(int(row["name_variants"]) for row in by_sample["S2"]),
        "s1_date_forms": sum(int(row["date_forms"]) for row in by_sample["S1"]),
        "s2_date_forms": sum(int(row["date_forms"]) for row in by_sample["S2"]),
        "s1_starred_date_forms": sum(int(row["starred_date_forms"]) for row in by_sample["S1"]),
        "s2_starred_date_forms": sum(int(row["starred_date_forms"]) for row in by_sample["S2"]),
        "s1_pair_forms_after_star_filter": sum(
            int(row["pair_forms_after_star_filter"]) for row in by_sample["S1"]
        ),
        "s2_pair_forms_after_star_filter": sum(
            int(row["pair_forms_after_star_filter"]) for row in by_sample["S2"]
        ),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def pages_from_text(text: str) -> int:
    stripped = text.rstrip("\f\n\r ")
    if not stripped:
        return 0
    return stripped.count("\f") + 1


def protocol_anchors(paper_text: str, data_text: str) -> list[dict[str, str]]:
    paper = re.sub(r"\s+", " ", paper_text)
    data = re.sub(r"\s+", " ", data_text)
    checks = [
        (
            "paper",
            "pattern_type_b_definition",
            "Pattern of type B" in paper or "PTB" in paper,
            "type-B pattern framing found",
        ),
        (
            "paper",
            "one_million_permutation_rank",
            "999, 999 random permu" in paper and "1, 000, 000 numbers" in paper,
            "one-million rank procedure found",
        ),
        (
            "paper",
            "sample_s1_s2_results",
            "0.00051" in paper and "0.000046" in paper,
            "published S1/S2 result numbers found",
        ),
        (
            "data",
            "list_l_definition",
            "List L consists of these 14 personalities" in data,
            "List L size rule found",
        ),
        (
            "data",
            "sample_s1_definition",
            "Sample S1 is a set of word pairs" in data,
            "Sample S1 definition found",
        ),
        (
            "data",
            "sample_s2_definition",
            "This yields the Sample S2" in data,
            "Sample S2 definition found",
        ),
        (
            "data",
            "date_three_fixed_forms",
            "three fixed forms" in data,
            "date-form rule found",
        ),
        (
            "data",
            "length_range_5_8",
            "range 5-8" in data,
            "length range rule found",
        ),
        (
            "data",
            "asterisk_short_date_exclusion",
            "asterisk" in data and "not included in the sample" in data,
            "asterisk exclusion rule found",
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
        "# Witztum Birth Dates Source Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Sources",
        "",
        "- Paper PDF: `https://www.torah-code.org/papers/witztum.pdf`",
        "- Data PDF: `https://www.torah-code.org/papers/personaldata.pdf`",
        f"- Paper SHA-256: `{summary['paper_sha256']}`",
        f"- Data SHA-256: `{summary['data_sha256']}`",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| paper PDF pages from extracted text | {summary['paper_pages_from_text']} |",
        f"| data PDF pages from extracted text | {summary['data_pages_from_text']} |",
        f"| sample tables | {summary['sample_tables']} |",
        f"| total table rows | {summary['total_table_rows']} |",
        f"| S1 rows | {summary['s1_rows']} |",
        f"| S2 rows | {summary['s2_rows']} |",
        f"| S1 name variants | {summary['s1_name_variants']} |",
        f"| S2 name variants | {summary['s2_name_variants']} |",
        f"| S1 date forms | {summary['s1_date_forms']} |",
        f"| S2 date forms | {summary['s2_date_forms']} |",
        f"| S1 starred date forms | {summary['s1_starred_date_forms']} |",
        f"| S2 starred date forms | {summary['s2_starred_date_forms']} |",
        f"| S1 pair forms after star filter | {summary['s1_pair_forms_after_star_filter']} |",
        f"| S2 pair forms after star filter | {summary['s2_pair_forms_after_star_filter']} |",
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
            "This audit only verifies that the paper and data PDFs expose stable source",
            "shape for the S1/S2 birth-date samples. It does not normalize terms into",
            "repo search rows, compute ELS/SL proximity, rank permutations, or evaluate",
            "the published p-levels.",
            "",
            "Next result-bearing step, if chosen later: write a separate preregistered",
            "birth-date protocol that freezes source rows, name/date normalization, text",
            "source, skip caps, proximity metric, permutation schedule, and controls",
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
            "paper": str(args.paper_source),
            "data": str(args.data_source),
        },
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "rows": str(args.out),
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
