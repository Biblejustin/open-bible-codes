#!/usr/bin/env python3
"""Download unfoldingWord Hebrew Bible USFM and convert it to CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from els.ebible_usfm import UsfmVerse, parse_usfm_zip


SOURCE_ID = "hbo_uhb"
SOURCE_NAME = "unfoldingWord Hebrew Bible"
SOURCE_VERSION = "v2.1.30"
SOURCE_URL = (
    f"https://git.door43.org/unfoldingWord/hbo_uhb/archive/{SOURCE_VERSION}.zip"
)
DETAILS_URL = f"https://git.door43.org/unfoldingWord/hbo_uhb/src/tag/{SOURCE_VERSION}"
LICENSE_URL = f"{DETAILS_URL}/LICENSE.md"
LICENSE_LABEL = "CC BY-SA 4.0; preserve upstream attribution and trademark notice"
RAW_ZIP = Path(f"data/raw/unfoldingword/hbo_uhb_{SOURCE_VERSION}.zip")
OUT_CSV = Path("data/processed/unfoldingword/hbo_uhb.csv")
OUT_MANIFEST = Path("data/processed/unfoldingword/hbo_uhb.manifest.json")
USER_AGENT = "Open Bible Codes source importer"


def main() -> int:
    args = _parse_args()
    zip_path = Path(args.zip_out or RAW_ZIP)
    csv_path = Path(args.csv_out or OUT_CSV)
    manifest_path = Path(args.manifest_out or OUT_MANIFEST)
    source_url = args.url or SOURCE_URL

    if not args.skip_download or not zip_path.exists():
        _download(source_url, zip_path)

    verses = parse_usfm_zip(zip_path)
    _write_csv(csv_path, verses)
    _write_manifest(
        manifest_path,
        source_url=source_url,
        zip_path=zip_path,
        csv_path=csv_path,
        verses=verses,
    )
    print(csv_path)
    print(manifest_path)
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--zip-out")
    parser.add_argument("--csv-out")
    parser.add_argument("--manifest-out")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reuse existing zip-out file.",
    )
    return parser.parse_args()


def _download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        out_path.write_bytes(response.read())


def _write_csv(path: Path, verses: list[UsfmVerse]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["ref", "book", "chapter", "verse", "text"],
        )
        writer.writeheader()
        for verse in verses:
            writer.writerow(
                {
                    "ref": verse.ref,
                    "book": verse.book,
                    "chapter": verse.chapter,
                    "verse": verse.verse,
                    "text": verse.text,
                }
            )


def _write_manifest(
    path: Path,
    *,
    source_url: str,
    zip_path: Path,
    csv_path: Path,
    verses: list[UsfmVerse],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_id": SOURCE_ID,
        "source_name": SOURCE_NAME,
        "source_version": SOURCE_VERSION,
        "source_url": source_url,
        "details_url": DETAILS_URL,
        "license_url": LICENSE_URL,
        "license": LICENSE_LABEL,
        "downloaded_at": datetime.now(UTC).isoformat(),
        "zip_path": str(zip_path),
        "zip_sha256": _sha256(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "csv_path": str(csv_path),
        "book_count": len({verse.book for verse in verses}),
        "verse_count": len(verses),
        "normalization": "USFM markers, word attributes, notes, and crossrefs removed; verse text preserved.",
    }
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
