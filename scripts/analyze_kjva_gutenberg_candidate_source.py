#!/usr/bin/env python3
"""Audit Project Gutenberg KJV + Apocrypha metadata without importing Bible text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from els import __version__


KJV_RDF_URL = "https://www.gutenberg.org/ebooks/30.rdf"
APOCRYPHA_RDF_URL = "https://www.gutenberg.org/ebooks/124.rdf"
RDF_URL = KJV_RDF_URL
KJV_EBOOK_PAGE_URL = "https://www.gutenberg.org/ebooks/30"
APOCRYPHA_EBOOK_PAGE_URL = "https://www.gutenberg.org/ebooks/124"
EBOOK_PAGE_URL = KJV_EBOOK_PAGE_URL
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_candidate_source")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "source_status.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_CANDIDATE_SOURCE_AUDIT.md")
USER_AGENT = "OpenBibleCodes-EDLS source-status audit/1.0"

NS = {
    "dcterms": "http://purl.org/dc/terms/",
    "pgterms": "http://www.gutenberg.org/2009/pgterms/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
}

ROW_FIELDNAMES = [
    "source_id",
    "rdf_url",
    "final_url",
    "fetch_status",
    "error",
    "bytes",
    "sha256",
    "ebook_no",
    "ebook_page_url",
    "title",
    "rights",
    "issued",
    "downloads",
    "description_count",
    "descriptions",
    "plain_text_utf8_url_present",
    "html_url_present",
    "epub_url_present",
    "apocrypha_marker_present",
    "public_domain_usa_marker_present",
    "source_audit_status",
    "source_use_status",
    "verse_numbered_import_ready",
    "source_lock_ready_status",
    "result_ready_status",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "metadata_fetches_ok",
    "public_domain_usa_pages",
    "kjv_complete_metadata_candidates",
    "apocrypha_metadata_candidates",
    "split_kjv_apocrypha_metadata_candidates",
    "apocrypha_marker_pages",
    "plain_text_utf8_pages",
    "source_use_ready_pages",
    "source_lock_ready_pages",
    "verse_import_ready_pages",
    "result_ready_pages",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class FetchedRdf:
    raw: bytes
    final_url: str
    fetch_status: str
    error: str = ""


@dataclass(frozen=True)
class GutenbergSource:
    source_id: str
    ebook_no: str
    component: str
    default_rdf_url: str
    default_page_url: str


KJV_SOURCE = GutenbergSource(
    source_id="gutenberg_ebook_30_kjv_complete",
    ebook_no="30",
    component="kjv",
    default_rdf_url=KJV_RDF_URL,
    default_page_url=KJV_EBOOK_PAGE_URL,
)
APOCRYPHA_SOURCE = GutenbergSource(
    source_id="gutenberg_ebook_124_deuterocanonical",
    ebook_no="124",
    component="apocrypha",
    default_rdf_url=APOCRYPHA_RDF_URL,
    default_page_url=APOCRYPHA_EBOOK_PAGE_URL,
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    sources = [
        (KJV_SOURCE, args.rdf_url, args.ebook_page_url),
        (APOCRYPHA_SOURCE, args.apocrypha_rdf_url, args.apocrypha_ebook_page_url),
    ]
    rows = []
    for source, rdf_url, page_url in sources:
        fetched = fetch_rdf(rdf_url, timeout=args.timeout)
        rows.append(analyze_rdf(args, fetched, source=source, rdf_url=rdf_url, ebook_page_url=page_url))
    summary = build_summary(rows)
    anchors = build_anchors(rows, summary)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors)
    write_manifest(args.manifest_out, args, rows, summary, anchors, started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rdf-url", default=KJV_RDF_URL)
    parser.add_argument("--apocrypha-rdf-url", default=APOCRYPHA_RDF_URL)
    parser.add_argument("--ebook-page-url", default=KJV_EBOOK_PAGE_URL)
    parser.add_argument("--apocrypha-ebook-page-url", default=APOCRYPHA_EBOOK_PAGE_URL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    return parser


def fetch_rdf(url: str, *, timeout: float) -> FetchedRdf:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return FetchedRdf(
                raw=response.read(),
                final_url=response.geturl(),
                fetch_status="fetched",
            )
    except HTTPError as exc:
        return FetchedRdf(raw=b"", final_url=url, fetch_status=f"http_error_{exc.code}", error=str(exc))
    except (OSError, URLError) as exc:
        return FetchedRdf(raw=b"", final_url=url, fetch_status="fetch_error", error=str(exc))


def analyze_rdf(
    args: argparse.Namespace,
    fetched: FetchedRdf,
    *,
    source: GutenbergSource = KJV_SOURCE,
    rdf_url: str | None = None,
    ebook_page_url: str | None = None,
) -> dict[str, object]:
    parsed = parse_rdf(fetched.raw) if fetched.raw else {}
    title = str(parsed.get("title", ""))
    rights = str(parsed.get("rights", ""))
    descriptions = [str(value) for value in parsed.get("descriptions", [])]
    format_urls = [str(value) for value in parsed.get("format_urls", [])]
    public_domain = "public domain in the usa" in rights.casefold()
    kjv_complete = "king james version, complete" in title.casefold()
    plain_text = any("txt.utf-8" in url for url in format_urls)
    apocrypha_marker = any(
        marker in value.casefold()
        for value in [title, rights, *descriptions]
        for marker in ("apocrypha", "deuterocanonical")
    )
    metadata_candidate = fetched.fetch_status == "fetched" and public_domain and plain_text
    if source.component == "kjv" and metadata_candidate and kjv_complete:
        source_audit_status = "public_domain_kjv_complete_metadata_component"
    elif source.component == "apocrypha" and metadata_candidate and apocrypha_marker:
        source_audit_status = "public_domain_apocrypha_metadata_component"
    else:
        source_audit_status = "source_candidate_not_confirmed"
    return {
        "source_id": source.source_id,
        "rdf_url": rdf_url or getattr(args, "rdf_url", source.default_rdf_url),
        "final_url": fetched.final_url,
        "fetch_status": fetched.fetch_status,
        "error": fetched.error,
        "bytes": len(fetched.raw),
        "sha256": hashlib.sha256(fetched.raw).hexdigest() if fetched.raw else "",
        "ebook_no": source.ebook_no,
        "ebook_page_url": ebook_page_url or getattr(args, "ebook_page_url", source.default_page_url),
        "title": title,
        "rights": rights,
        "issued": str(parsed.get("issued", "")),
        "downloads": str(parsed.get("downloads", "")),
        "description_count": len(descriptions),
        "descriptions": " | ".join(descriptions),
        "plain_text_utf8_url_present": plain_text,
        "html_url_present": any("html" in url for url in format_urls),
        "epub_url_present": any("epub" in url for url in format_urls),
        "apocrypha_marker_present": apocrypha_marker,
        "public_domain_usa_marker_present": public_domain,
        "source_audit_status": source_audit_status,
        "source_use_status": "needs_source_use_policy_lock",
        "verse_numbered_import_ready": False,
        "source_lock_ready_status": "not_source_lock_ready",
        "result_ready_status": "not_result_ready",
    }


def parse_rdf(raw: bytes) -> dict[str, object]:
    root = ET.fromstring(raw)
    descriptions = [text for node in root.findall(".//dcterms:description", NS) if (text := node_text(node))]
    format_urls = [
        str(node.attrib.get(f"{{{NS['rdf']}}}about", ""))
        for node in root.findall(".//pgterms:file", NS)
    ]
    title_node = root.find(".//dcterms:title", NS)
    rights_node = root.find(".//dcterms:rights", NS)
    issued_node = root.find(".//dcterms:issued", NS)
    downloads_node = root.find(".//pgterms:downloads", NS)
    return {
        "title": node_text(title_node) if title_node is not None else "",
        "rights": node_text(rights_node) if rights_node is not None else "",
        "issued": node_text(issued_node) if issued_node is not None else "",
        "downloads": node_text(downloads_node) if downloads_node is not None else "",
        "descriptions": descriptions,
        "format_urls": format_urls,
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    kjv_candidate = any(
        row["source_audit_status"] == "public_domain_kjv_complete_metadata_component"
        for row in rows
    )
    apocrypha_candidate = any(
        row["source_audit_status"] == "public_domain_apocrypha_metadata_component"
        for row in rows
    )
    return {
        "source_pages": len(rows),
        "metadata_fetches_ok": sum(1 for row in rows if row["fetch_status"] == "fetched"),
        "public_domain_usa_pages": sum(1 for row in rows if bool(row["public_domain_usa_marker_present"])),
        "kjv_complete_metadata_candidates": sum(
            1
            for row in rows
            if row["source_audit_status"] == "public_domain_kjv_complete_metadata_component"
        ),
        "apocrypha_metadata_candidates": sum(
            1
            for row in rows
            if row["source_audit_status"] == "public_domain_apocrypha_metadata_component"
        ),
        "split_kjv_apocrypha_metadata_candidates": int(kjv_candidate and apocrypha_candidate),
        "apocrypha_marker_pages": sum(1 for row in rows if bool(row["apocrypha_marker_present"])),
        "plain_text_utf8_pages": sum(1 for row in rows if bool(row["plain_text_utf8_url_present"])),
        "source_use_ready_pages": sum(1 for row in rows if row["source_use_status"] == "source_use_ready"),
        "source_lock_ready_pages": sum(1 for row in rows if row["source_lock_ready_status"] != "not_source_lock_ready"),
        "verse_import_ready_pages": sum(1 for row in rows if bool(row["verse_numbered_import_ready"])),
        "result_ready_pages": sum(1 for row in rows if row["result_ready_status"] != "not_result_ready"),
        "claim_status": "source_status_only_not_result_bearing",
    }


def build_anchors(rows: list[dict[str, object]], summary: dict[str, object]) -> list[dict[str, str]]:
    checks = [
        ("gutenberg", "metadata_fetch_status_recorded", int(summary["metadata_fetches_ok"]) == 2, "Project Gutenberg RDF metadata fetched for eBook 30 and eBook 124"),
        ("gutenberg", "public_domain_usa_recorded", int(summary["public_domain_usa_pages"]) == 2, "RDF rights fields say public domain in the USA"),
        ("gutenberg", "plain_text_format_recorded", int(summary["plain_text_utf8_pages"]) == 2, "plain text UTF-8 format URLs are recorded"),
        ("gutenberg", "apocrypha_metadata_recorded", int(summary["apocrypha_metadata_candidates"]) == 1, "eBook 124 RDF metadata identifies the Apocrypha/deuterocanonical component"),
        ("gutenberg", "split_metadata_components_recorded", int(summary["split_kjv_apocrypha_metadata_candidates"]) == 1, "eBook 30 plus eBook 124 form a split metadata candidate"),
        ("gutenberg", "source_lock_not_ready", int(summary["source_lock_ready_pages"]) == 0, "no source-lock-ready corpus import is declared"),
        ("gutenberg", "result_not_ready", int(summary["result_ready_pages"]) == 0, "no result-bearing replication is declared ready"),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if ok else "missing",
            "diagnostic": diagnostic,
        }
        for source, anchor, ok, diagnostic in checks
    ]


def write_markdown(path: Path, summary: dict[str, object], rows: list[dict[str, object]], anchors: list[dict[str, str]]) -> None:
    found = sum(1 for row in anchors if row["status"] == "found")
    lines = [
        "# KJVA Gutenberg Candidate Source Audit",
        "",
        "Status: source-status audit only.",
        "",
        "This is not an ELS result, not a corpus import, and not a source lock.",
        "It records Project Gutenberg eBook 30 and eBook 124 RDF metadata only and does not download, retain, normalize, or commit Bible text.",
        "",
        "## Summary",
        "",
        f"- Source pages: {summary['source_pages']}.",
        f"- Metadata fetches ok: {summary['metadata_fetches_ok']}.",
        f"- Public-domain-USA pages: {summary['public_domain_usa_pages']}.",
        f"- KJV-complete metadata candidates: {summary['kjv_complete_metadata_candidates']}.",
        f"- Apocrypha/deuterocanon metadata candidates: {summary['apocrypha_metadata_candidates']}.",
        f"- Split KJV+Apocrypha metadata candidates: {summary['split_kjv_apocrypha_metadata_candidates']}.",
        f"- Apocrypha marker pages in RDF: {summary['apocrypha_marker_pages']}.",
        f"- Plain-text UTF-8 format pages: {summary['plain_text_utf8_pages']}.",
        f"- Source-use ready pages: {summary['source_use_ready_pages']}.",
        f"- Source-lock ready pages: {summary['source_lock_ready_pages']}.",
        f"- Verse-numbered import ready pages: {summary['verse_import_ready_pages']}.",
        f"- Result-ready pages: {summary['result_ready_pages']}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Source Rows",
        "",
        "| Source | Status | Rights | Plain text | Apocrypha marker | Source use | Source lock | Result |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["source_id"]),
                    f"`{row['source_audit_status']}`",
                    str(row["rights"]),
                    str(row["plain_text_utf8_url_present"]),
                    str(row["apocrypha_marker_present"]),
                    f"`{row['source_use_status']}`",
                    f"`{row['source_lock_ready_status']}`",
                    f"`{row['result_ready_status']}`",
                ]
            )
            + " |"
        )
    lines.extend(["", "## Anchors", "", f"Found anchors: {found}/{len(anchors)}.", "", "| Source | Anchor | Status | Diagnostic |", "| --- | --- | --- | --- |"])
    for row in anchors:
        lines.append(f"| {row['source']} | `{row['anchor']}` | `{row['status']}` | {row['diagnostic']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Project Gutenberg RDF metadata records eBook 30 as `The Bible, King James Version, Complete` and eBook 124 as `Deuterocanonical Books of the Bible Apocrypha`, both with `Public domain in the USA.` rights and plain-text UTF-8 format URLs.",
            "This metadata audit pairs with the separate heading-level coverage probe, but it does not declare source-lock readiness.",
            "A future source-lock pass must still inspect lawful source text in an ignored local cache, then lock verse mapping, book order, Baruch/Epistle handling, checksums, collation, terms, and controls before any result-bearing run.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(path: Path, args: argparse.Namespace, rows: list[dict[str, object]], summary: dict[str, object], anchors: list[dict[str, str]], started: float) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_gutenberg_candidate_source",
        "rdf_urls": [args.rdf_url, args.apocrypha_rdf_url],
        "claim_boundary": "source-status audit only; no ELS result",
        "text_retention": "metadata only; no Bible text retained",
        "row_count": len(rows),
        "summary": summary,
        "anchor_count": len(anchors),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def node_text(node: ET.Element) -> str:
    return " ".join("".join(node.itertext()).split())


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
