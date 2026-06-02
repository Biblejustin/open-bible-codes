#!/usr/bin/env python3
"""Probe live and archived Cities PDF links without running ELS results."""

from __future__ import annotations

import argparse
import csv
import glob
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
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from els import __version__
from scripts.build_wrr_wayback_source_recovery_probe import (
    cdx_rows_from_payload,
    closest_snapshot,
    markdown_cell,
    markdown_link,
    select_cdx_snapshot,
    wayback_availability_url,
    wayback_cdx_url,
    wayback_raw_snapshot_url,
)
from scripts.download_wrr_sources import FetchResult


DEFAULT_HTML_GLOB = "reports/wrr_1994/torah_code_experiment_cities*.html"
DEFAULT_OUT_DIR = Path("reports/cities_pdf_recovery_probe")
DEFAULT_OUT = DEFAULT_OUT_DIR / "cities_pdf_recovery_probe.csv"
DEFAULT_SUMMARY_OUT = DEFAULT_OUT_DIR / "cities_pdf_recovery_probe_summary.csv"
DEFAULT_MD = Path("docs/CITIES_PDF_RECOVERY_PROBE.md")
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "cities_pdf_recovery_probe.manifest.json"
NETWORK_TIMEOUT_SECONDS = 8

DEFAULT_SOURCE_PAGE_URLS = {
    "torah_code_experiment_cities.html": (
        "https://www.torah-code.org/experiments/cities_experiment.shtml"
    ),
    "torah_code_experiment_cities_gans.html": (
        "https://www.torah-code.org/experiments/gans_cities.html"
    ),
    "torah_code_experiment_cities_aumann.html": (
        "https://www.torah-code.org/experiments/aumann_experiment.html"
    ),
    "torah_code_experiment_cities_simon_mckay.html": (
        "https://www.torah-code.org/experiments/simon_mckay_experiment.html"
    ),
    "torah_code_experiment_cities_haralick.html": (
        "https://www.torah-code.org/experiments/haralick_cities_experiment.html"
    ),
}

ROW_FIELDNAMES = [
    "label",
    "source_pages",
    "url",
    "live_final_url",
    "live_http_status",
    "live_status",
    "live_kind",
    "live_bytes",
    "live_sha256",
    "archive_probe_url",
    "archive_status",
    "archive_snapshot_source",
    "archive_timestamp",
    "archive_cdx_checked",
    "archive_cdx_candidate_count",
    "archive_raw_url",
    "archive_kind",
    "archive_bytes",
    "archive_sha256",
    "selected_source",
    "selected_path",
    "pdf_pages",
    "pdf_text_chars",
    "usable_status",
]

SUMMARY_FIELDNAMES = [
    "pdf_urls_probed",
    "live_pdf_rows",
    "live_html_or_other_rows",
    "archive_available_rows",
    "archive_cdx_checked_rows",
    "archive_cdx_candidate_rows",
    "archive_pdf_rows",
    "usable_pdf_rows",
    "unrecovered_pdf_rows",
    "current_pdf_recovery_status",
]


@dataclass(frozen=True)
class PdfSource:
    label: str
    source_pages: tuple[str, ...]
    url: str


@dataclass(frozen=True)
class ArchiveProbe:
    probe_url: str = ""
    status: str = "not_checked"
    snapshot_source: str = ""
    timestamp: str = ""
    cdx_checked: bool = False
    cdx_candidate_count: int = 0
    raw_url: str = ""
    kind: str = ""
    raw: bytes = b""


class PdfLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value and ".pdf" in value.lower():
                self.links.append(value)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_globs = args.source_glob or [DEFAULT_HTML_GLOB]
    args.source_glob = source_globs
    paths = sorted({Path(path) for pattern in source_globs for path in glob.glob(pattern)})
    sources = discover_pdf_sources(paths)
    rows = []
    for index, source in enumerate(sources, start=1):
        row = probe_pdf_source(source, args.snapshot_dir, refresh=args.refresh)
        rows.append(row)
        print(
            f"probed {index}/{len(sources)} {source.label}: {row['usable_status']}",
            flush=True,
        )
    summary = build_summary(rows)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, rows)
    write_manifest(args.manifest_out, args, summary, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-glob",
        action="append",
        default=[],
        help="Glob for cached Cities HTML pages. Repeatable.",
    )
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_OUT_DIR / "snapshots")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--refresh", action="store_true")
    return parser


def discover_pdf_sources(paths: list[Path]) -> list[PdfSource]:
    by_url: dict[str, set[str]] = {}
    for path in paths:
        if not path.exists():
            continue
        page_url = DEFAULT_SOURCE_PAGE_URLS.get(path.name, path.resolve().as_uri())
        parser = PdfLinkParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        for link in parser.links:
            url = urljoin(page_url, link)
            by_url.setdefault(url, set()).add(path.stem)
    return [
        PdfSource(label=url_label(url), source_pages=tuple(sorted(pages)), url=url)
        for url, pages in sorted(by_url.items())
    ]


def url_label(url: str) -> str:
    name = Path(url.split("?", 1)[0]).stem or "pdf"
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return f"cities_pdf_{slug}"


def probe_pdf_source(source: PdfSource, snapshot_dir: Path, *, refresh: bool) -> dict[str, object]:
    live_dir = snapshot_dir / "live"
    archive_dir = snapshot_dir / "archive"
    live_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)
    live_path = live_dir / f"{source.label}.pdf"
    live_result, live_error = fetch_live(source.url, live_path, refresh=refresh)
    live_raw = live_path.read_bytes() if live_path.exists() else b""
    live_kind = detect_kind(live_raw)
    live_status = live_kind if live_result else f"live_fetch_error:{live_error}"
    archive = ArchiveProbe()
    archive_path = archive_dir / f"{source.label}.pdf"
    if live_kind != "pdf":
        archive = probe_archive(source, archive_path, refresh=refresh)
    selected_source = ""
    selected_path = ""
    pdf_pages = ""
    pdf_text_chars = ""
    if live_kind == "pdf":
        selected_source = "live"
        selected_path = str(live_path)
        pdf_pages = pdfinfo_pages(live_path)
        pdf_text_chars = str(len(pdftotext(live_path).strip()))
    elif archive.kind == "pdf" and archive_path.exists():
        selected_source = "archive"
        selected_path = str(archive_path)
        pdf_pages = pdfinfo_pages(archive_path)
        pdf_text_chars = str(len(pdftotext(archive_path).strip()))
    usable_status = (
        "usable_live_pdf"
        if selected_source == "live"
        else "usable_archived_pdf"
        if selected_source == "archive"
        else "no_pdf_recovered"
    )
    return {
        "label": source.label,
        "source_pages": ";".join(source.source_pages),
        "url": source.url,
        "live_final_url": live_result.final_url if live_result else "",
        "live_http_status": live_result.http_status if live_result else "",
        "live_status": live_status,
        "live_kind": live_kind,
        "live_bytes": len(live_raw),
        "live_sha256": sha256_bytes(live_raw) if live_raw else "",
        "archive_probe_url": archive.probe_url,
        "archive_status": archive.status,
        "archive_snapshot_source": archive.snapshot_source,
        "archive_timestamp": archive.timestamp,
        "archive_cdx_checked": archive.cdx_checked,
        "archive_cdx_candidate_count": archive.cdx_candidate_count,
        "archive_raw_url": archive.raw_url,
        "archive_kind": archive.kind,
        "archive_bytes": len(archive.raw),
        "archive_sha256": sha256_bytes(archive.raw) if archive.raw else "",
        "selected_source": selected_source,
        "selected_path": selected_path,
        "pdf_pages": pdf_pages,
        "pdf_text_chars": pdf_text_chars,
        "usable_status": usable_status,
    }


def fetch_live(url: str, path: Path, *, refresh: bool) -> tuple[FetchResult | None, str]:
    if path.exists() and not refresh:
        return FetchResult(data=path.read_bytes(), final_url="", http_status=None), ""
    try:
        result = fetch_url_with_timeout(url)
    except Exception as exc:  # pragma: no cover - live network failures vary.
        return None, type(exc).__name__
    path.write_bytes(result.data)
    return result, ""


def probe_archive(source: PdfSource, path: Path, *, refresh: bool) -> ArchiveProbe:
    if path.exists() and not refresh:
        raw = path.read_bytes()
        return ArchiveProbe(
            probe_url=source.url,
            status="cached",
            kind=detect_kind(raw),
            raw=raw,
        )
    best = ArchiveProbe(status="no_archived_snapshot")
    for probe_url in archive_candidate_urls(source.url):
        try:
            archive = probe_archive_url(probe_url)
        except Exception as exc:  # pragma: no cover - live archive failures vary.
            archive = ArchiveProbe(probe_url=probe_url, status=f"archive_error:{type(exc).__name__}")
        if archive.kind == "pdf":
            path.write_bytes(archive.raw)
            return archive
        if archive.status != "no_archived_snapshot" and best.status == "no_archived_snapshot":
            best = archive
    return best


def archive_candidate_urls(url: str) -> list[str]:
    candidates = [url]
    if url.startswith("https://"):
        candidates.append("http://" + url.removeprefix("https://"))
    return candidates


def probe_archive_url(url: str) -> ArchiveProbe:
    closest = closest_snapshot(fetch_json_with_timeout(wayback_availability_url(url)))
    snapshot_source = "availability_closest" if closest.get("available") else ""
    cdx_count = 0
    if not closest.get("available"):
        cdx_rows = cdx_snapshots_with_timeout(url)
        cdx_checked = True
        cdx_count = len(cdx_rows)
        closest = select_cdx_snapshot(cdx_rows)
        snapshot_source = "cdx_fallback" if closest.get("available") else ""
    else:
        cdx_checked = False
    if not closest.get("available"):
        return ArchiveProbe(
            probe_url=url,
            status="no_archived_snapshot",
            cdx_checked=cdx_checked,
            cdx_candidate_count=cdx_count,
        )
    raw_url = wayback_raw_snapshot_url(str(closest.get("url") or ""))
    raw = fetch_bytes_with_timeout(raw_url)
    return ArchiveProbe(
        probe_url=url,
        status="archive_downloaded",
        snapshot_source=snapshot_source,
        timestamp=str(closest.get("timestamp") or ""),
        cdx_checked=cdx_checked,
        cdx_candidate_count=cdx_count,
        raw_url=raw_url,
        kind=detect_kind(raw),
        raw=raw,
    )


def detect_kind(raw: bytes) -> str:
    stripped = raw.lstrip()
    if stripped.startswith(b"%PDF"):
        return "pdf"
    if stripped[:20].lower().startswith(b"<!doctype html") or stripped[:10].lower().startswith(
        b"<html"
    ):
        return "html"
    if not raw:
        return ""
    return "other"


def fetch_url_with_timeout(url: str) -> FetchResult:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 EDLS source audit"})
    with urlopen(request, timeout=NETWORK_TIMEOUT_SECONDS) as response:
        return FetchResult(
            data=response.read(),
            final_url=response.geturl(),
            http_status=getattr(response, "status", None),
        )


def cdx_snapshots_with_timeout(url: str) -> list[dict[str, str]]:
    payload = fetch_json_with_timeout(wayback_cdx_url(url))
    return cdx_rows_from_payload(payload, source="Cities Wayback CDX API")


def fetch_json_with_timeout(url: str):
    raw = fetch_bytes_with_timeout(url)
    return json.loads(raw.decode("utf-8", errors="replace"))


def fetch_bytes_with_timeout(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 EDLS source audit"})
    with urlopen(request, timeout=NETWORK_TIMEOUT_SECONDS) as response:
        return response.read()


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


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    status_counts = Counter(str(row["usable_status"]) for row in rows)
    usable = status_counts.get("usable_live_pdf", 0) + status_counts.get(
        "usable_archived_pdf", 0
    )
    return {
        "pdf_urls_probed": len(rows),
        "live_pdf_rows": sum(1 for row in rows if row["live_kind"] == "pdf"),
        "live_html_or_other_rows": sum(1 for row in rows if row["live_kind"] != "pdf"),
        "archive_available_rows": sum(
            1 for row in rows if row["archive_status"] in {"archive_downloaded", "cached"}
        ),
        "archive_cdx_checked_rows": sum(
            1 for row in rows if row.get("archive_cdx_checked")
        ),
        "archive_cdx_candidate_rows": sum(
            1 for row in rows if int(row["archive_cdx_candidate_count"] or 0) > 0
        ),
        "archive_pdf_rows": sum(1 for row in rows if row["archive_kind"] == "pdf"),
        "usable_pdf_rows": usable,
        "unrecovered_pdf_rows": status_counts.get("no_pdf_recovered", 0),
        "current_pdf_recovery_status": (
            "all_pdf_sources_recovered"
            if usable == len(rows)
            else "partial_pdf_sources_recovered"
            if usable
            else "no_pdf_sources_recovered"
        ),
    }


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
) -> None:
    usable_rows = [row for row in rows if row["usable_status"] != "no_pdf_recovered"]
    missing_rows = [row for row in rows if row["usable_status"] == "no_pdf_recovered"]
    lines = [
        "# Cities PDF Recovery Probe",
        "",
        "Status: live/archive PDF recovery probe only. This does not run ELS",
        "searches, does not update the cached `reports/wrr_1994/` bundle, and",
        "does not make claim-ready source decisions.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| PDF URLs probed | {summary['pdf_urls_probed']} |",
        f"| live PDF rows | {summary['live_pdf_rows']} |",
        f"| live HTML/other rows | {summary['live_html_or_other_rows']} |",
        f"| archived rows downloaded or cached | {summary['archive_available_rows']} |",
        f"| rows checked with CDX fallback | {summary['archive_cdx_checked_rows']} |",
        f"| rows with CDX exact-URL candidates | {summary['archive_cdx_candidate_rows']} |",
        f"| archived PDF rows | {summary['archive_pdf_rows']} |",
        f"| usable PDF rows | {summary['usable_pdf_rows']} |",
        f"| unrecovered PDF rows | {summary['unrecovered_pdf_rows']} |",
        "",
        f"Current PDF recovery status: `{summary['current_pdf_recovery_status']}`.",
        "",
        "## Usable PDF Rows",
        "",
        "| Label | Source pages | Selected | Pages | Text chars | SHA-256 | Source URL |",
        "| --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in usable_rows:
        sha = row["live_sha256"] if row["selected_source"] == "live" else row["archive_sha256"]
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["source_pages"]),
                    markdown_cell(row["selected_source"]),
                    markdown_cell(row["pdf_pages"]),
                    markdown_cell(row["pdf_text_chars"]),
                    f"`{str(sha)[:16]}`" if sha else "",
                    markdown_link("url", str(row["url"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Unrecovered PDF Rows",
            "",
            "| Label | Source pages | Live kind | Archive status | CDX candidates | URL |",
            "| --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in missing_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["label"]),
                    markdown_cell(row["source_pages"]),
                    markdown_cell(row["live_kind"]),
                    markdown_cell(row["archive_status"]),
                    markdown_cell(row["archive_cdx_candidate_count"]),
                    markdown_link("url", str(row["url"])),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Source Boundary",
            "",
            "Recovered PDF bytes are source-shape inputs only. This probe verifies",
            "whether linked Cities/Aumann/Simon-McKay PDFs can be fetched live or",
            "through exact-URL Wayback snapshots. It does not perform OCR, city-name",
            "normalization, ELS searches, compactness calculations, or p-level",
            "verification.",
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
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source_globs": args.source_glob,
        "rows": rows,
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "live/archive PDF recovery probe only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
