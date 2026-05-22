#!/usr/bin/env python3
"""Audit co-linear ELS paper attachments without running ELS results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import subprocess
import time
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from els import __version__


DEFAULT_PAPER = Path("reports/wrr_1994/torah_code_colinear_paper.pdf")
DEFAULT_ATTACHMENTS_PAGE = Path("reports/wrr_1994/torah_code_colinear_attachments.html")
DEFAULT_ATTACHMENT_PDFS = [
    Path("reports/wrr_1994/torah_code_colinear_attachment_pls.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_roots.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_all_1698.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_res_113.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_consul_138.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_intersec_108.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_comb_143.pdf"),
    Path("reports/wrr_1994/torah_code_colinear_attachment_att_heb.pdf"),
]
DEFAULT_OUT = Path("reports/wrr_1994/colinear_els_attachment_sources.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/colinear_els_source_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/colinear_els_protocol_anchors.csv")
DEFAULT_MD = Path("docs/COLINEAR_ELS_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/colinear_els_source_audit.manifest.json")

EXPECTED_ROW_COUNTS = {
    "pls": 6060,
    "all_1698": 1698,
    "res_113": 113,
    "consul_138": 138,
    "intersec_108": 108,
    "comb_143": 143,
}

BIDI_CONTROL_CHARS = dict.fromkeys(
    map(ord, "\u200e\u200f\u202a\u202b\u202c\u202d\u202e\ufeff"),
    None,
)

ATTACHMENT_FIELDNAMES = [
    "label",
    "path",
    "bytes",
    "sha256",
    "pdf_pages",
    "text_chars",
    "nonblank_lines",
    "hebrew_lines",
    "hebrew_chars",
    "expected_rows",
    "numeric_row_prefix",
    "hash_marker_rows",
    "observed_source_rows",
    "claim_status",
]
SUMMARY_FIELDNAMES = [
    "paper_pdf",
    "paper_sha256",
    "paper_bytes",
    "paper_pages",
    "attachments_page",
    "attachments_page_sha256",
    "attachments_page_bytes",
    "attachments_page_pdf_links",
    "attachment_pdfs",
    "attachment_pdf_pages",
    "attachments_with_expected_rows",
    "expected_rows_total",
    "observed_rows_total",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class AttachmentLink:
    href: str
    label: str

    def absolute_url(self, base_url: str) -> str:
        if self.label.startswith("http://") or self.label.startswith("https://"):
            return self.label
        return urljoin(base_url, self.href)


class AttachmentLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[AttachmentLink] = []
        self.canonical = ""
        self._attrs: dict[str, str] | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lower_attrs = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "a":
            self._attrs = lower_attrs
            self._text = []
        if tag.lower() == "link" and lower_attrs.get("rel", "").lower() == "canonical":
            self.canonical = lower_attrs.get("href", "")

    def handle_data(self, data: str) -> None:
        if self._attrs is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._attrs is not None:
            href = self._attrs.get("href", "")
            label = normalize_space(" ".join(self._text))
            self.links.append(AttachmentLink(href=href, label=html.unescape(label)))
            self._attrs = None
            self._text = []


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    attachments = args.attachment_pdf or DEFAULT_ATTACHMENT_PDFS
    args.attachment_pdf = attachments
    paper_text = extract_pdf_text(args.paper)
    page_info = parse_attachments_page(args.attachments_page)
    rows = [analyze_attachment_pdf(path) for path in attachments]
    summary = build_summary(args, paper_text, page_info, rows)
    anchors = protocol_anchors(paper_text, page_info, rows)
    write_csv(args.out, ATTACHMENT_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", type=Path, default=DEFAULT_PAPER)
    parser.add_argument("--attachments-page", type=Path, default=DEFAULT_ATTACHMENTS_PAGE)
    parser.add_argument("--attachment-pdf", action="append", type=Path, default=[])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_attachments_page(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("windows-1255", errors="replace")
    parser = AttachmentLinkParser()
    parser.feed(text)
    pdf_links = [link for link in parser.links if link.href.lower().endswith(".pdf")]
    return {
        "path": str(path),
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "canonical": parser.canonical,
        "pdf_links": len(pdf_links),
        "pdf_link_targets": [link.absolute_url("https://www.torah-code.org/papers/attachments.html") for link in pdf_links],
    }


def analyze_attachment_pdf(path: Path) -> dict[str, object]:
    text = extract_pdf_text(path)
    cleaned = clean_text(text)
    label = attachment_label(path)
    expected_rows = EXPECTED_ROW_COUNTS.get(label, "")
    numeric_prefix = numeric_row_prefix(cleaned, expected_rows if isinstance(expected_rows, int) else 0)
    hash_rows = cleaned.count("###")
    observed_rows: int | str = ""
    if isinstance(expected_rows, int):
        observed_rows = numeric_prefix
        if hash_rows and numeric_prefix + hash_rows == expected_rows:
            observed_rows = expected_rows
    return {
        "label": label,
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "pdf_pages": pages_from_text(text),
        "text_chars": len(text),
        "nonblank_lines": sum(1 for line in cleaned.splitlines() if line.strip()),
        "hebrew_lines": sum(1 for line in cleaned.splitlines() if has_hebrew(line)),
        "hebrew_chars": sum(1 for ch in cleaned if "\u0590" <= ch <= "\u05ff"),
        "expected_rows": expected_rows,
        "numeric_row_prefix": numeric_prefix,
        "hash_marker_rows": hash_rows,
        "observed_source_rows": observed_rows,
        "claim_status": "source_shape_only_not_result_bearing",
    }


def attachment_label(path: Path) -> str:
    name = path.name
    prefix = "torah_code_colinear_attachment_"
    if name.startswith(prefix):
        name = name[len(prefix) :]
    return name.removesuffix(".pdf")


def numeric_row_prefix(text: str, expected_rows: int) -> int:
    if expected_rows <= 0:
        return 0
    values = {
        int(match)
        for match in re.findall(r"(?<!\d)(\d{1,4})(?!\d)", text)
        if 1 <= int(match) <= expected_rows
    }
    prefix = 0
    while prefix + 1 in values:
        prefix += 1
    return prefix


def build_summary(
    args: argparse.Namespace,
    paper_text: str,
    page_info: dict[str, object],
    rows: list[dict[str, object]],
) -> dict[str, object]:
    expected_rows = [row for row in rows if row["expected_rows"] != ""]
    return {
        "paper_pdf": str(args.paper),
        "paper_sha256": sha256(args.paper),
        "paper_bytes": args.paper.stat().st_size,
        "paper_pages": pages_from_text(paper_text),
        "attachments_page": str(args.attachments_page),
        "attachments_page_sha256": page_info["sha256"],
        "attachments_page_bytes": page_info["bytes"],
        "attachments_page_pdf_links": page_info["pdf_links"],
        "attachment_pdfs": len(rows),
        "attachment_pdf_pages": sum(int(row["pdf_pages"]) for row in rows),
        "attachments_with_expected_rows": len(expected_rows),
        "expected_rows_total": sum(int(row["expected_rows"]) for row in expected_rows),
        "observed_rows_total": sum(
            int(row["observed_source_rows"])
            for row in expected_rows
            if row["observed_source_rows"] != ""
        ),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def protocol_anchors(
    paper_text: str,
    page_info: dict[str, object],
    rows: list[dict[str, object]],
) -> list[dict[str, str]]:
    paper = normalize_space(clean_text(paper_text))
    by_label = {str(row["label"]): row for row in rows}
    checks = [
        (
            "paper",
            "paper_co_linear_definition",
            "co-linear if d = d0" in paper,
            "paper defines co-linear ELS relation",
        ),
        (
            "paper",
            "paper_pentateuch_min5_lexicon",
            "all words in P" in paper and "at least 5 letters long" in paper,
            "paper identifies Pentateuch words of length at least 5",
        ),
        (
            "paper",
            "paper_skip_distance_2_to_1000",
            "2 <= d <= 1000" in ascii_math(paper) or "2 ≤ d ≤ 1000" in paper,
            "paper states skip-distance range 2..1000",
        ),
        (
            "paper",
            "paper_6060_pls_found",
            "6, 060 PLSs were found" in paper,
            "paper reports 6,060 PLS rows",
        ),
        (
            "paper",
            "paper_p_level_6e_minus8",
            "p-level obtained for this experiment is 6 x 10-8" in ascii_math(paper)
            or "p-level obtained for this experiment is 6 × 10−8" in paper,
            "paper reports p-level 6 x 10^-8",
        ),
        (
            "attachments_page",
            "attachments_page_eight_pdf_links",
            int(page_info["pdf_links"]) == 8,
            "attachments page exposes 8 PDF links",
        ),
        (
            "attachments",
            "all_eight_attachment_pdfs_present",
            len(rows) == 8 and all(int(row["bytes"]) > 0 for row in rows),
            "all linked attachment PDFs are present locally",
        ),
        (
            "attachments",
            "pls_6060_rows_observed",
            int(by_label.get("pls", {}).get("observed_source_rows", 0)) == 6060,
            "PLS attachment exposes 6,060 source rows",
        ),
        (
            "attachments",
            "all_1698_rows_observed",
            int(by_label.get("all_1698", {}).get("observed_source_rows", 0)) == 1698,
            "all_1698 attachment exposes 1,698 source rows",
        ),
        (
            "attachments",
            "review_sets_502_rows_observed",
            sum(
                int(by_label.get(label, {}).get("observed_source_rows", 0))
                for label in ("res_113", "consul_138", "intersec_108", "comb_143")
            )
            == 502,
            "four reviewed subset attachments expose 502 rows",
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
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Co-linear ELS Source Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready co-linear ELS reproduction.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| paper PDF pages | {summary['paper_pages']} |",
        f"| attachments page PDF links | {summary['attachments_page_pdf_links']} |",
        f"| downloaded attachment PDFs | {summary['attachment_pdfs']} |",
        f"| attachment PDF pages | {summary['attachment_pdf_pages']} |",
        f"| attachments with expected row counts | {summary['attachments_with_expected_rows']} |",
        f"| expected rows in counted attachments | {summary['expected_rows_total']} |",
        f"| observed rows in counted attachments | {summary['observed_rows_total']} |",
        "",
        "## Attachment PDFs",
        "",
        "| Attachment | Pages | Expected Rows | Observed Rows | Numeric Prefix | Hash Rows | Hebrew Lines |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['label']} | {row['pdf_pages']} | {row['expected_rows']} | "
            f"{row['observed_source_rows']} | {row['numeric_row_prefix']} | "
            f"{row['hash_marker_rows']} | {row['hebrew_lines']} |"
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
            "The paper and attachment files are usable as source-shape material for a",
            "future co-linear ELS/verse protocol. This audit only records file coverage,",
            "protocol anchors, and table row counts. It does not normalize Hebrew terms,",
            "select roots, compute ELSs, score verse links, or evaluate controls.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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


def pages_from_text(text: str) -> int:
    stripped = text.rstrip("\f\n\r ")
    if not stripped:
        return 0
    return stripped.count("\f") + 1


def clean_text(text: str) -> str:
    return unicodedata.normalize("NFKC", text.translate(BIDI_CONTROL_CHARS))


def ascii_math(text: str) -> str:
    return (
        text.replace("≤", "<=")
        .replace("×", "x")
        .replace("−", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )


def has_hebrew(text: str) -> bool:
    return any("\u0590" <= ch <= "\u05ff" for ch in text)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


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
        "paper": str(args.paper),
        "attachments_page": str(args.attachments_page),
        "attachment_pdfs": [str(path) for path in args.attachment_pdf],
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "attachments": str(args.out),
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
    return sha256_bytes(path.read_bytes())


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
