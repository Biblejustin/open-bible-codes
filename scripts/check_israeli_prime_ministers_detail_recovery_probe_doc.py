#!/usr/bin/env python3
"""Validate Israeli prime-minister detail recovery doc keeps limits explicit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_israeli_prime_ministers_detail_recovery_probe as builder


DEFAULT_DOC = Path("docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md")
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
EXPECTED_PAGES = {"9", "10", "11", "12"}
EXPECTED_BYTES = "629155"
EXPECTED_SHA256 = "d60a59519b55bcff8b6a287eab9c7b06113e0967e95b362cfccaeb66d9cb84f4"
EXPECTED_SHA16 = EXPECTED_SHA256[:16]
EXPECTED_TITLE = (
    "Daftar Bet Kecil 100, 200, 300, 500 Perak - Agen Slot Bet Kecil "
    "Deposit Via Pulsa 5000 Terjangkau"
)
EXPECTED_CANONICAL = "https://www.torah-code.org/"
EXPECTED_ROWS = {
    "9": "Benjamin Netanyahu",
    "10": "Ehud Barak",
    "11": "Ariel Sharon",
    "12": "Ehud Olmert",
}
EXPECTED_SUMMARY = {
    "pages_probed": "4",
    "expected_title_present_rows": "0",
    "redirected_rows": "4",
    "root_final_url_rows": "4",
    "root_canonical_rows": "4",
    "spam_marker_rows": "4",
    "usable_detail_pages": "0",
    "unrecovered_detail_pages": "4",
    "recovery_status": "no_detail_pages_recovered",
}
EXPECTED_CLAIM_BOUNDARY = "live source recovery only; no ELS result"
REQUIRED_PHRASES = (
    "# Israeli Prime Ministers Detail Recovery Probe",
    "Status: live-source recovery probe only.",
    "does not infer missing",
    "| missing detail pages probed | 4 |",
    "| rows where expected title appeared | 0 |",
    "| redirected rows | 4 |",
    "| final URL is Torah-code root | 4 |",
    "| canonical URL is Torah-code root | 4 |",
    "| unrelated slot/gambling markers | 4 |",
    "| usable detail pages | 0 |",
    "Current recovery status: `no_detail_pages_recovered`.",
    "Do not run a result-bearing protocol",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_detail_recovery_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"Israeli PM detail recovery doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Israeli PM detail recovery doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_detail_recovery_doc(
    doc: Path,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    present_pages = probe_pages(text)
    missing_pages = sorted(EXPECTED_PAGES - present_pages)
    if missing_pages:
        failures.append(f"{doc} missing probe pages: " + ", ".join(missing_pages))
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(
            validate_manifest(
                manifest,
                doc=doc,
                rows=rows or DEFAULT_ROWS,
                summary=summary or DEFAULT_SUMMARY,
            )
        )
    return failures


def probe_pages(text: str) -> set[str]:
    pages: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 10 and cells[0] in EXPECTED_PAGES:
            pages.add(cells[0])
    return pages


def validate_rows_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    observed_pages = [row.get("page_index", "") for row in rows]
    if observed_pages != list(EXPECTED_ROWS):
        failures.append(f"{path} page order drifted")
    by_page = {row.get("page_index", ""): row for row in rows}
    for page, title in EXPECTED_ROWS.items():
        row = by_page.get(page)
        if row is None:
            failures.append(f"{path} missing page {page}")
            continue
        expected_path = (
            "reports/israeli_prime_ministers_detail_recovery_probe/"
            f"snapshots/israeli_prime_ministers_{page}.html"
        )
        expected_url = (
            "https://www.torah-code.org/experiments/"
            f"israeli_prime_ministers_{page}.html"
        )
        checks = {
            "expected_title": title,
            "requested_url": expected_url,
            "final_url": EXPECTED_CANONICAL,
            "redirected": "True",
            "http_status": "200",
            "path": expected_path,
            "bytes": EXPECTED_BYTES,
            "sha256": EXPECTED_SHA256,
            "title": EXPECTED_TITLE,
            "canonical": EXPECTED_CANONICAL,
            "expected_title_present": "False",
            "canonical_is_root": "True",
            "final_url_is_root": "True",
            "spam_marker_present": "True",
            "usable_status": "unrecovered_detail_page",
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{path} page {page} {key} drifted")
        failures.extend(validate_snapshot_file(Path(expected_path), page))
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} has {len(rows)} rows; expected 1")
        return failures
    row = rows[0]
    for key, value in EXPECTED_SUMMARY.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_manifest(path: Path, *, doc: Path, rows: Path, summary: Path) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    checks: dict[str, Any] = {
        "tool": "build_israeli_prime_ministers_detail_recovery_probe.py",
        "rows": len(EXPECTED_ROWS),
        "summary": _int_summary(),
        "outputs": {
            "csv": str(rows),
            "summary": str(summary),
            "markdown": str(doc),
            "manifest": str(path),
        },
        "claim_boundary": EXPECTED_CLAIM_BOUNDARY,
    }
    for key, value in checks.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_snapshot_file(path: Path, page: str) -> list[str]:
    if not path.exists():
        return [f"{path} is missing for page {page}"]
    raw = path.read_bytes()
    failures: list[str] = []
    if str(len(raw)) != EXPECTED_BYTES:
        failures.append(f"{path} page {page} snapshot bytes drifted")
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        failures.append(f"{path} page {page} snapshot sha256 drifted")
    return failures


def _int_summary() -> dict[str, object]:
    return {
        key: int(value) if value.isdigit() else value
        for key, value in EXPECTED_SUMMARY.items()
    }


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
