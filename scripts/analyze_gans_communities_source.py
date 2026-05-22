#!/usr/bin/env python3
"""Audit the Gans/Inbal/Bombach communities data PDF source shape."""

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


DEFAULT_SOURCE = Path("reports/wrr_1994/gans_communities_data.pdf")
DEFAULT_OUT = Path("reports/wrr_1994/gans_communities_source_records.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/gans_communities_source_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/gans_communities_protocol_anchors.csv")
DEFAULT_MD = Path("docs/GANS_COMMUNITIES_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/gans_communities_source_audit.manifest.json")

TRACE_RE = re.compile(r"^[?a-z][0-9?]{4}[?a-z0-9][0-9?]{4}[a-z0-9]{0,2}$")
RECORD_START_RE = re.compile(r"^\s*(\d+)\.\s+(\S+)(?:\s+(.*))?$")
COMMUNITY_TRACE_RE = re.compile(r"\(([bcd][A-Za-z0-9?]{12,15})\)")
COMMUNITY_REUSE_RE = re.compile(r"\b([bcd])\((\d+)\)")

RECORD_FIELDNAMES = [
    "record_index",
    "trace1",
    "trace2",
    "line_count",
    "explicit_community_rows",
    "reused_community_rows",
    "total_community_rows",
    "has_no_personality_marker",
    "has_malformed_trace_line",
]

SUMMARY_FIELDNAMES = [
    "source_pdf",
    "source_sha256",
    "source_bytes",
    "pages_from_text",
    "data_records",
    "record_index_min",
    "record_index_max",
    "missing_record_indexes",
    "records_with_trace1",
    "records_with_trace2",
    "explicit_community_rows",
    "reused_community_rows",
    "total_community_rows",
    "records_with_no_personality_marker",
    "records_with_malformed_trace_line",
    "claim_status",
]

ANCHOR_FIELDNAMES = ["anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class SourceRecord:
    record_index: int
    trace1: str
    trace2: str
    lines: tuple[str, ...]

    @property
    def explicit_community_rows(self) -> int:
        return sum(len(COMMUNITY_TRACE_RE.findall(line)) for line in self.lines)

    @property
    def reused_community_rows(self) -> int:
        return sum(len(COMMUNITY_REUSE_RE.findall(line)) for line in self.lines)

    @property
    def has_no_personality_marker(self) -> bool:
        return any(re.search(r"\s-\s*(?:\(|$)", line) for line in self.lines)

    @property
    def has_malformed_trace_line(self) -> bool:
        return not TRACE_RE.match(self.trace1) or not TRACE_RE.match(self.trace2)

    def as_row(self) -> dict[str, object]:
        explicit = self.explicit_community_rows
        reused = self.reused_community_rows
        return {
            "record_index": self.record_index,
            "trace1": self.trace1,
            "trace2": self.trace2,
            "line_count": len(self.lines),
            "explicit_community_rows": explicit,
            "reused_community_rows": reused,
            "total_community_rows": explicit + reused,
            "has_no_personality_marker": int(self.has_no_personality_marker),
            "has_malformed_trace_line": int(self.has_malformed_trace_line),
        }


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    text = extract_pdf_text(args.source)
    records = parse_records(text)
    record_rows = [record.as_row() for record in records]
    summary = build_summary(args.source, text, records)
    anchors = protocol_anchors(text)
    write_csv(args.out, RECORD_FIELDNAMES, record_rows)
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
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
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


def parse_records(text: str) -> list[SourceRecord]:
    data_text = data_section(text)
    grouped: list[tuple[int, list[str]]] = []
    current_index: int | None = None
    current_lines: list[str] = []
    for raw_line in data_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        match = RECORD_START_RE.match(line)
        if match:
            if current_index is not None:
                grouped.append((current_index, current_lines))
            current_index = int(match.group(1))
            rest = " ".join(part for part in (match.group(2), match.group(3) or "") if part)
            current_lines = [rest]
            continue
        if current_index is not None:
            current_lines.append(line)
    if current_index is not None:
        grouped.append((current_index, current_lines))
    return [build_record(index, lines) for index, lines in grouped]


def data_section(text: str) -> str:
    start_marker = "3. The Data"
    end_marker = "4. References"
    try:
        start = text.index(start_marker) + len(start_marker)
    except ValueError as error:
        raise ValueError("could not find Gans communities data section") from error
    try:
        end = text.index(end_marker, start)
    except ValueError:
        end = len(text)
    return text[start:end]


def build_record(index: int, lines: list[str]) -> SourceRecord:
    trace_tokens = trace_like_tokens(lines)
    trace1 = trace_tokens[0] if trace_tokens else ""
    trace2 = trace_tokens[1] if len(trace_tokens) > 1 else ""
    return SourceRecord(index, trace1, trace2, tuple(lines))


def trace_like_tokens(lines: list[str]) -> list[str]:
    tokens: list[str] = []
    for line in lines[:4]:
        for token in line.strip().split():
            cleaned = token.strip(",;:")
            if TRACE_RE.match(cleaned):
                tokens.append(cleaned)
                break
    return tokens


def build_summary(source: Path, text: str, records: list[SourceRecord]) -> dict[str, object]:
    indexes = [record.record_index for record in records]
    missing = []
    if indexes:
        expected = set(range(min(indexes), max(indexes) + 1))
        missing = sorted(expected.difference(indexes))
    explicit = sum(record.explicit_community_rows for record in records)
    reused = sum(record.reused_community_rows for record in records)
    return {
        "source_pdf": str(source),
        "source_sha256": sha256(source),
        "source_bytes": source.stat().st_size,
        "pages_from_text": pages_from_text(text),
        "data_records": len(records),
        "record_index_min": min(indexes, default=""),
        "record_index_max": max(indexes, default=""),
        "missing_record_indexes": " ".join(str(index) for index in missing),
        "records_with_trace1": sum(1 for record in records if record.trace1),
        "records_with_trace2": sum(1 for record in records if record.trace2),
        "explicit_community_rows": explicit,
        "reused_community_rows": reused,
        "total_community_rows": explicit + reused,
        "records_with_no_personality_marker": sum(
            1 for record in records if record.has_no_personality_marker
        ),
        "records_with_malformed_trace_line": sum(
            1 for record in records if record.has_malformed_trace_line
        ),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def pages_from_text(text: str) -> int:
    stripped = text.rstrip("\f\n\r ")
    if not stripped:
        return 0
    return stripped.count("\f") + 1


def protocol_anchors(text: str) -> list[dict[str, str]]:
    normalized = re.sub(r"\s+", " ", text)
    checks = {
        "wrr_lists_1_and_2_names": "without modification from WRR lists 1 and 2" in normalized,
        "community_prefixes_lhq_tlhq": "lhq" in normalized and "tlhq" in normalized,
        "length_window_5_8": "5≤d≤8" in normalized or "5 ≤ k ≤ 8" in normalized,
        "rabbi_appellation_ybr_exclusion": "begin with “ybr”" in normalized
        or 'begin with "ybr"' in normalized,
        "additional_qq_nonconforming_experiment": "not in conformity with WRR" in normalized,
        "trace_words_defined": all(
            marker in normalized for marker in ("Trace word 1", "Trace word 2", "Trace word 3")
        ),
    }
    diagnostics = {
        "wrr_lists_1_and_2_names": "personality names/appellations source rule found",
        "community_prefixes_lhq_tlhq": "community prefix rule found",
        "length_window_5_8": "length filter rule found",
        "rabbi_appellation_ybr_exclusion": "Rabbi-prefix exclusion rule found",
        "additional_qq_nonconforming_experiment": "separate qq experiment caveat found",
        "trace_words_defined": "trace-word definitions found",
    }
    return [
        {
            "anchor": anchor,
            "status": "found" if found else "missing",
            "diagnostic": diagnostics[anchor] if found else "anchor text not found",
        }
        for anchor, found in checks.items()
    ]


def write_markdown(
    path: Path,
    summary: dict[str, object],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Gans Communities Source Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "compactness calculation, and not a claim-ready replication.",
        "",
        "## Source",
        "",
        "- Data PDF: `https://www.torah-code.org/papers/communities_data.pdf`",
        f"- Local ignored file: `{summary['source_pdf']}`",
        f"- SHA-256: `{summary['source_sha256']}`",
        f"- Bytes: {summary['source_bytes']}",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| pages from extracted text | {summary['pages_from_text']} |",
        f"| data records | {summary['data_records']} |",
        f"| record index minimum | {summary['record_index_min']} |",
        f"| record index maximum | {summary['record_index_max']} |",
        f"| records with trace word 1 | {summary['records_with_trace1']} |",
        f"| records with trace word 2 | {summary['records_with_trace2']} |",
        f"| explicit community rows | {summary['explicit_community_rows']} |",
        f"| reused community rows | {summary['reused_community_rows']} |",
        f"| total community rows | {summary['total_community_rows']} |",
        f"| records with no personality marker | {summary['records_with_no_personality_marker']} |",
        f"| records with malformed trace line | {summary['records_with_malformed_trace_line']} |",
        "",
        "## Protocol Anchors",
        "",
        f"Found anchors: {anchor_counts.get('found', 0)} of {len(anchors)}.",
        "",
        "| Anchor | Status | Diagnostic |",
        "| --- | --- | --- |",
    ]
    for anchor in anchors:
        lines.append(
            f"| `{anchor['anchor']}` | {anchor['status']} | {anchor['diagnostic']} |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This audit makes the source usable as a future locked-data intake target.",
            "It does not yet normalize Hebrew spellings, add community prefixes, apply",
            "the length/Rabbi-prefix filters, compute ELS hits, or test compactness.",
            "",
            "Next result-bearing step, if chosen later: write a separate preregistered",
            "communities protocol that freezes source rows, normalization, filters,",
            "Genesis text, skip caps, compactness metric, and controls before running",
            "any ELS search.",
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
        "source": str(args.source),
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
