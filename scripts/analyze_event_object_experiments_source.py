#!/usr/bin/env python3
"""Audit Torah-code.org event/object experiment source files without ELS results."""

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
from html.parser import HTMLParser
from pathlib import Path

from els import __version__


DEFAULT_SOURCES = [
    Path("reports/wrr_1994/torah_code_experiment_sons_of_haman.html"),
    Path("reports/wrr_1994/torah_code_experiment_sons_of_haman_data.html"),
    Path("reports/wrr_1994/torah_code_experiment_pumbedita.html"),
    Path("reports/wrr_1994/torah_code_experiment_pumbedita_data.pdf"),
    Path("reports/wrr_1994/torah_code_experiment_auschwitz.html"),
    Path("reports/wrr_1994/torah_code_experiment_auschwitz_data.pdf"),
    Path("reports/wrr_1994/torah_code_experiment_ark.html"),
    Path("reports/wrr_1994/torah_code_experiment_ark_code.pdf"),
]
DEFAULT_OUT = Path("reports/wrr_1994/event_object_experiment_source_files.csv")
DEFAULT_STATUS_OUT = Path("reports/wrr_1994/event_object_experiment_status.csv")
DEFAULT_DATA_ROWS_OUT = Path("reports/wrr_1994/event_object_experiment_data_rows.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/event_object_experiment_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/event_object_experiment_anchors.csv")
DEFAULT_MD = Path("docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/event_object_experiment_source_audit.manifest.json")

FILE_FIELDNAMES = [
    "experiment",
    "path",
    "extension",
    "detected_kind",
    "status",
    "bytes",
    "sha256",
    "pdf_pages",
    "text_chars",
    "title",
    "link_count",
    "pdf_link_count",
]
STATUS_FIELDNAMES = [
    "experiment",
    "source_files",
    "data_rows",
    "declared_status",
    "protocol_table_present",
    "notes",
]
DATA_ROW_FIELDNAMES = [
    "experiment",
    "source_table",
    "row_index",
    "english_label",
    "hebrew_keyword",
    "raw_line",
]
SUMMARY_FIELDNAMES = [
    "source_files",
    "html_files",
    "pdf_files",
    "pdf_pages",
    "pdf_text_extractable_files",
    "protocol_table_pages",
    "reported_significant_pages",
    "reported_non_significant_pages",
    "under_construction_pages",
    "sons_of_haman_keyword_rows",
    "pumbedita_rows",
    "auschwitz_rows",
    "auschwitz_topic_keyword_rows",
    "machine_data_rows",
    "ark_pdf_pages",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class SourceText:
    path: Path
    experiment: str
    raw_text: str
    plain_text: str


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "a":
            for name, value in attrs:
                if name.lower() == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            return
        if self.in_title:
            self.title_parts.append(stripped)
        self.parts.append(stripped)

    @property
    def text(self) -> str:
        return normalize_space(" ".join(self.parts))

    @property
    def title(self) -> str:
        return normalize_space(" ".join(self.title_parts))


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_paths = args.source or DEFAULT_SOURCES
    args.source = source_paths
    file_rows, texts = analyze_sources(source_paths)
    data_rows = event_object_data_rows(texts)
    status_rows = build_status_rows(file_rows, texts, data_rows)
    summary = build_summary(file_rows, status_rows, data_rows)
    anchors = protocol_anchors(texts, status_rows, summary)
    write_csv(args.out, FILE_FIELDNAMES, file_rows)
    write_csv(args.status_out, STATUS_FIELDNAMES, status_rows)
    write_csv(args.data_rows_out, DATA_ROW_FIELDNAMES, data_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, status_rows, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(file_rows), started)
    print(args.out)
    print(args.status_out)
    print(args.data_rows_out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", type=Path, default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--status-out", type=Path, default=DEFAULT_STATUS_OUT)
    parser.add_argument("--data-rows-out", type=Path, default=DEFAULT_DATA_ROWS_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def analyze_sources(paths: list[Path]) -> tuple[list[dict[str, object]], list[SourceText]]:
    rows: list[dict[str, object]] = []
    texts: list[SourceText] = []
    for path in paths:
        row, source_text = analyze_file(path)
        rows.append(row)
        texts.append(source_text)
    return rows, texts


def analyze_file(path: Path) -> tuple[dict[str, object], SourceText]:
    raw = path.read_bytes()
    extension = path.suffix.lower().lstrip(".")
    detected_kind = detect_kind(raw)
    experiment = experiment_for_path(path)
    title = ""
    link_count = 0
    pdf_link_count = 0
    pdf_pages = ""
    text = ""
    status = detected_kind
    if detected_kind == "html":
        html = raw.decode("utf-8", errors="replace")
        extractor = TextExtractor()
        extractor.feed(html)
        title = extractor.title
        link_count = len(extractor.links)
        pdf_link_count = sum(1 for link in extractor.links if ".pdf" in link.lower())
        text = extractor.text
    elif detected_kind == "pdf":
        pdf_pages = pdfinfo_pages(path)
        text = pdftotext(path).strip()
        if not pdf_pages:
            status = "pdf_parse_error"
        elif not text:
            status = "pdf_no_extractable_text"
        else:
            status = "pdf_text_extractable"
    else:
        text = raw.decode("utf-8", errors="replace")
    return (
        {
            "experiment": experiment,
            "path": str(path),
            "extension": extension,
            "detected_kind": detected_kind,
            "status": status,
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
            "pdf_pages": pdf_pages,
            "text_chars": len(text),
            "title": title,
            "link_count": link_count,
            "pdf_link_count": pdf_link_count,
        },
        SourceText(
            path=path,
            experiment=experiment,
            raw_text=raw.decode("utf-8", errors="replace"),
            plain_text=text,
        ),
    )


def detect_kind(raw: bytes) -> str:
    stripped = raw.lstrip()
    if stripped.startswith(b"%PDF"):
        return "pdf"
    if stripped[:20].lower().startswith(b"<!doctype html") or stripped[:10].lower().startswith(
        b"<html"
    ):
        return "html"
    return "other"


def experiment_for_path(path: Path) -> str:
    name = path.name.lower()
    if "sons_of_haman" in name:
        return "sons_of_haman"
    if "pumbedita" in name:
        return "pumbedita"
    if "auschwitz" in name:
        return "auschwitz"
    if "ark" in name:
        return "ark"
    return "unknown"


def build_status_rows(
    file_rows: list[dict[str, object]],
    texts: list[SourceText],
    data_rows: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    data_rows = event_object_data_rows(texts) if data_rows is None else data_rows
    rows_by_experiment: dict[str, list[dict[str, object]]] = {}
    text_by_experiment: dict[str, str] = {}
    for row in file_rows:
        rows_by_experiment.setdefault(str(row["experiment"]), []).append(row)
    for source_text in texts:
        text_by_experiment[source_text.experiment] = (
            text_by_experiment.get(source_text.experiment, "")
            + " "
            + normalize_space(source_text.plain_text)
        )
    pumbedita_rows = count_numbered_pdf_rows(texts, "pumbedita")
    auschwitz_rows = count_numbered_pdf_rows(texts, "auschwitz")
    sons_rows = sum(1 for row in data_rows if row["experiment"] == "sons_of_haman")
    status = [
        {
            "experiment": "sons_of_haman",
            "source_files": len(rows_by_experiment.get("sons_of_haman", [])),
            "data_rows": sons_rows,
            "declared_status": "reported_significant_followup_after_non_significant_original",
            "protocol_table_present": has_protocol_table(text_by_experiment.get("sons_of_haman", "")),
            "notes": "main page says original test was not significant; data page lists Hebrew keywords and reports p-value 16.5/10000 for follow-up",
        },
        {
            "experiment": "pumbedita",
            "source_files": len(rows_by_experiment.get("pumbedita", [])),
            "data_rows": pumbedita_rows,
            "declared_status": "reported_non_significant",
            "protocol_table_present": has_protocol_table(text_by_experiment.get("pumbedita", "")),
            "notes": "source page reports failed significance test; PDF has Amoraim spelling rows",
        },
        {
            "experiment": "auschwitz",
            "source_files": len(rows_by_experiment.get("auschwitz", [])),
            "data_rows": auschwitz_rows,
            "declared_status": "reported_non_significant_replication",
            "protocol_table_present": has_protocol_table(text_by_experiment.get("auschwitz", "")),
            "notes": "source page cites Witztum probability but reports local replication not significant",
        },
        {
            "experiment": "ark",
            "source_files": len(rows_by_experiment.get("ark", [])),
            "data_rows": "",
            "declared_status": "under_construction",
            "protocol_table_present": has_protocol_table(text_by_experiment.get("ark", "")),
            "notes": "source page is under construction and links a tutorial PDF, not a completed experiment data sheet",
        },
    ]
    return status


def build_summary(
    file_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    data_rows: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    data_rows = [] if data_rows is None else data_rows
    page_total = sum(int(row["pdf_pages"] or 0) for row in file_rows)
    status_counts = Counter(str(row["declared_status"]) for row in status_rows)
    return {
        "source_files": len(file_rows),
        "html_files": sum(1 for row in file_rows if row["detected_kind"] == "html"),
        "pdf_files": sum(1 for row in file_rows if row["detected_kind"] == "pdf"),
        "pdf_pages": page_total,
        "pdf_text_extractable_files": sum(
            1 for row in file_rows if row["status"] == "pdf_text_extractable"
        ),
        "protocol_table_pages": sum(1 for row in status_rows if row["protocol_table_present"]),
        "reported_significant_pages": status_counts[
            "reported_significant_followup_after_non_significant_original"
        ],
        "reported_non_significant_pages": (
            status_counts["reported_non_significant"]
            + status_counts["reported_non_significant_replication"]
        ),
        "under_construction_pages": status_counts["under_construction"],
        "sons_of_haman_keyword_rows": sum(
            1 for row in data_rows if row["experiment"] == "sons_of_haman"
        ),
        "pumbedita_rows": data_rows_for(status_rows, "pumbedita"),
        "auschwitz_rows": data_rows_for(status_rows, "auschwitz"),
        "auschwitz_topic_keyword_rows": sum(
            1
            for row in data_rows
            if row["experiment"] == "auschwitz"
            and row["source_table"] == "auschwitz_topic_keyword"
        ),
        "machine_data_rows": len(data_rows),
        "ark_pdf_pages": ark_pdf_pages(file_rows),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def protocol_anchors(
    texts: list[SourceText],
    status_rows: list[dict[str, object]],
    summary: dict[str, object],
) -> list[dict[str, str]]:
    by_experiment: dict[str, str] = {}
    raw_by_experiment: dict[str, str] = {}
    for source_text in texts:
        by_experiment[source_text.experiment] = (
            by_experiment.get(source_text.experiment, "")
            + " "
            + normalize_space(source_text.plain_text)
        )
        raw_by_experiment[source_text.experiment] = (
            raw_by_experiment.get(source_text.experiment, "") + " " + source_text.raw_text
        )
    sons = by_experiment.get("sons_of_haman", "").lower()
    pumbedita = by_experiment.get("pumbedita", "").lower()
    auschwitz = by_experiment.get("auschwitz", "").lower()
    ark_raw = raw_by_experiment.get("ark", "").lower()
    checks = [
        (
            "sons_of_haman",
            "original_results_not_significant",
            "not statistically significant" in sons
            or "statistically insignificant results" in sons,
            "main page reports non-significant original test",
        ),
        (
            "sons_of_haman",
            "followup_p_value_16_5_of_10000",
            "16.5/10,000" in sons,
            "data page reports follow-up p-value",
        ),
        (
            "sons_of_haman",
            "followup_trials_10000",
            "number of trials 10,000" in sons,
            "data page reports 10000 trials",
        ),
        (
            "pumbedita",
            "pumbedita_non_significant",
            "failed to produce any statistically significant results" in pumbedita,
            "Pumbedita page reports no significant result",
        ),
        (
            "pumbedita",
            "pumbedita_pdf_20_rows",
            data_rows_for(status_rows, "pumbedita") == 20,
            "Pumbedita PDF has 20 numbered source rows",
        ),
        (
            "auschwitz",
            "witztum_probability_1_of_1000000",
            "1/1,000,000" in auschwitz,
            "Auschwitz page cites Witztum probability",
        ),
        (
            "auschwitz",
            "auschwitz_non_significant_replication",
            "failed to produce statistically significant results" in auschwitz,
            "Auschwitz page reports local replication not significant",
        ),
        (
            "auschwitz",
            "auschwitz_pdf_32_rows",
            data_rows_for(status_rows, "auschwitz") == 32,
            "Auschwitz PDF has 32 numbered subcamp rows",
        ),
        (
            "ark",
            "ark_under_construction",
            "underconstruction" in ark_raw,
            "Ark page contains under-construction marker",
        ),
        (
            "ark",
            "ark_tutorial_pdf_57_pages",
            int(summary["ark_pdf_pages"]) == 57,
            "Ark tutorial PDF has 57 pages",
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


def event_object_data_rows(texts: list[SourceText]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_text in texts:
        if source_text.experiment == "sons_of_haman" and source_text.path.suffix == ".html":
            rows.extend(sons_of_haman_keyword_rows(source_text))
        if source_text.experiment == "pumbedita" and source_text.path.suffix.lower() == ".pdf":
            rows.extend(numbered_pdf_data_rows(source_text, "pumbedita_amoraim"))
        if source_text.experiment == "auschwitz" and source_text.path.suffix.lower() == ".pdf":
            rows.extend(numbered_pdf_data_rows(source_text, "auschwitz"))
    return rows


def sons_of_haman_keyword_rows(source_text: SourceText) -> list[dict[str, object]]:
    extractor = TextExtractor()
    extractor.feed(source_text.raw_text)
    rows: list[dict[str, object]] = []
    in_keyword_list = False
    for part in extractor.parts:
        for line in [line.strip() for line in part.splitlines() if line.strip()]:
            if line == "Key Word List":
                in_keyword_list = True
                continue
            if in_keyword_list and line in {"Sons of Haman", "Experimental Protocol"}:
                return rows
            if not in_keyword_list or not re.search(r"[\u0590-\u05ff]", line):
                continue
            keyword = line
            rows.append(
                {
                    "experiment": "sons_of_haman",
                    "source_table": "sons_of_haman_keyword_list",
                    "row_index": len(rows) + 1,
                    "english_label": "",
                    "hebrew_keyword": keyword,
                    "raw_line": keyword,
                }
            )
    return rows


def numbered_pdf_data_rows(source_text: SourceText, source_table: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    last_by_column: dict[str, dict[str, object]] = {}
    for raw_line in source_text.plain_text.splitlines():
        line = raw_line.rstrip()
        matches = list(re.finditer(r"(?<!\S)(\d{1,2})\s+[A-Z]", line))
        if matches:
            for offset, match in enumerate(matches):
                end = matches[offset + 1].start() if offset + 1 < len(matches) else len(line)
                segment = line[match.start() : end].rstrip()
                row = parse_numbered_segment(source_text.experiment, source_table, segment)
                if not row:
                    continue
                if source_table == "auschwitz" and row["english_label"] == "Of Auschwitz":
                    row["source_table"] = "auschwitz_topic_keyword"
                elif source_table == "auschwitz":
                    row["source_table"] = "auschwitz_subcamp_keywords"
                rows.append(row)
                column = "left" if match.start() < 35 else "right"
                last_by_column[column] = row
            continue
        continuation = parse_continuation_segment(line)
        if not continuation:
            continue
        first_nonspace = len(line) - len(line.lstrip())
        column = "left" if first_nonspace < 35 else "right"
        previous = last_by_column.get(column)
        if previous is None:
            continue
        previous["english_label"] = f"{previous['english_label']} {continuation[0]}".strip()
        previous["hebrew_keyword"] = f"{previous['hebrew_keyword']} {continuation[1]}".strip()
        previous["raw_line"] = f"{previous['raw_line']} / {line.strip()}"
    table_order = {
        "auschwitz_topic_keyword": 0,
        "auschwitz_subcamp_keywords": 1,
    }
    return sorted(
        rows,
        key=lambda row: (
            table_order.get(str(row["source_table"]), 0),
            int(row["row_index"]),
        ),
    )


def parse_numbered_segment(
    experiment: str,
    source_table: str,
    segment: str,
) -> dict[str, object] | None:
    tokens = segment.strip().split()
    if len(tokens) < 3 or not tokens[0].isdigit():
        return None
    first_hebrew = first_hebrew_token(tokens[1:])
    if first_hebrew is None:
        return None
    hebrew_index = first_hebrew + 1
    english_tokens = tokens[1:hebrew_index]
    hebrew_tokens = tokens[hebrew_index:]
    return {
        "experiment": experiment,
        "source_table": source_table,
        "row_index": int(tokens[0]),
        "english_label": " ".join(english_tokens),
        "hebrew_keyword": " ".join(hebrew_tokens),
        "raw_line": segment.strip(),
    }


def first_hebrew_token(tokens: list[str]) -> int | None:
    for index, token in enumerate(tokens):
        if re.fullmatch(r"[`a-z]+", token):
            return index
    return None


def parse_continuation_segment(line: str) -> tuple[str, str] | None:
    tokens = line.strip().split()
    if len(tokens) < 2 or tokens[0].isdigit():
        return None
    first_hebrew = first_hebrew_token(tokens)
    if first_hebrew is None or first_hebrew == 0:
        return None
    english = " ".join(tokens[:first_hebrew])
    hebrew = " ".join(tokens[first_hebrew:])
    return english, hebrew


def count_numbered_pdf_rows(texts: list[SourceText], experiment: str) -> int:
    total = 0
    for source_text in texts:
        if source_text.experiment != experiment or source_text.path.suffix.lower() != ".pdf":
            continue
        line_count = sum(
            1 for line in source_text.plain_text.splitlines() if re.match(r"^\s*\d+\s+", line)
        )
        numbered_entries = {
            int(match.group(1))
            for match in re.finditer(r"(?<!\S)(\d{1,2})\s+[A-Z]", source_text.plain_text)
        }
        total += max(line_count, len(numbered_entries))
    return total


def data_rows_for(status_rows: list[dict[str, object]], experiment: str) -> int:
    for row in status_rows:
        if row["experiment"] == experiment and row["data_rows"] != "":
            return int(row["data_rows"])
    return 0


def ark_pdf_pages(file_rows: list[dict[str, object]]) -> int:
    for row in file_rows:
        if row["experiment"] == "ark" and row["extension"] == "pdf" and row["pdf_pages"]:
            return int(row["pdf_pages"])
    return 0


def has_protocol_table(text: str) -> bool:
    lowered = text.lower()
    return "expected number of els = 10" in lowered and "compactness measure" in lowered


def pdfinfo_pages(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdfinfo", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if completed.returncode != 0:
        return ""
    for line in completed.stdout.splitlines():
        if line.startswith("Pages:"):
            return line.split(":", 1)[1].strip()
    return ""


def pdftotext(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout


def write_markdown(
    path: Path,
    summary: dict[str, object],
    status_rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Event/Object Experiment Source Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| source files scanned | {summary['source_files']} |",
        f"| HTML files | {summary['html_files']} |",
        f"| PDF files | {summary['pdf_files']} |",
        f"| total PDF pages | {summary['pdf_pages']} |",
        f"| PDF files with extractable text | {summary['pdf_text_extractable_files']} |",
        f"| protocol-table pages | {summary['protocol_table_pages']} |",
        f"| reported significant follow-up pages | {summary['reported_significant_pages']} |",
        f"| reported non-significant pages | {summary['reported_non_significant_pages']} |",
        f"| under-construction pages | {summary['under_construction_pages']} |",
        f"| Sons of Haman keyword rows | {summary['sons_of_haman_keyword_rows']} |",
        f"| Pumbedita numbered source rows | {summary['pumbedita_rows']} |",
        f"| Auschwitz numbered source rows | {summary['auschwitz_rows']} |",
        f"| Auschwitz topic keyword rows | {summary['auschwitz_topic_keyword_rows']} |",
        f"| machine data rows extracted | {summary['machine_data_rows']} |",
        f"| Ark tutorial PDF pages | {summary['ark_pdf_pages']} |",
        "",
        "## Declared Status",
        "",
        "| Experiment | Source Files | Data Rows | Declared Status | Notes |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in status_rows:
        lines.append(
            f"| {row['experiment']} | {row['source_files']} | {row['data_rows']} | "
            f"{row['declared_status']} | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Protocol Anchors",
            "",
            f"Found anchors: {anchor_counts.get('found', 0)} of {len(anchors)}.",
            "",
            "| Source | Anchor | Status | Diagnostic |",
            "| --- | --- | --- | --- |",
        ]
    )
    for anchor in anchors:
        lines.append(
            f"| {anchor['source']} | `{anchor['anchor']}` | {anchor['status']} | {anchor['diagnostic']} |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This audit records source availability, source shape, row counts, and",
            "declared status for event/object experiment pages. It also exports",
            "machine-readable source rows from the available keyword lists and data",
            "PDFs. It does not normalize Hebrew spellings, choose variants, run ELS",
            "hits, evaluate controls, or verify any reported p-value.",
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
        "sources": [str(path) for path in args.source],
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "files": str(args.out),
            "status": str(args.status_out),
            "data_rows": str(args.data_rows_out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-shape audit only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
