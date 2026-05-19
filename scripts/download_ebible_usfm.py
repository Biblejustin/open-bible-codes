#!/usr/bin/env python3
"""Download eBible USFM sources and convert them to Open Bible Codes CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els.ebible_usfm import UsfmVerse, parse_usfm_zip


LICENSE_LABEL = "public-domain-marked by eBible; preserve upstream notice"
USER_AGENT = "Open Bible Codes source importer"


@dataclass(frozen=True)
class EbibleSource:
    source_id: str
    source_name: str
    source_url: str
    details_url: str
    raw_zip: Path
    out_csv: Path
    out_manifest: Path
    license_label: str = LICENSE_LABEL


SOURCES = {
    "grclxx": EbibleSource(
        source_id="grclxx",
        source_name="eBible GRCLXX Septuagint",
        source_url="https://ebible.org/Scriptures/grclxx_usfm.zip",
        details_url="https://ebible.org/details.php?id=grclxx",
        raw_zip=Path("data/raw/ebible/grclxx_usfm.zip"),
        out_csv=Path("data/processed/ebible/grclxx.csv"),
        out_manifest=Path("data/processed/ebible/grclxx.manifest.json"),
    ),
    "grctr": EbibleSource(
        source_id="grctr",
        source_name="eBible Greek Textus Receptus NT",
        source_url="https://ebible.org/Scriptures/grctr_usfm.zip",
        details_url="https://ebible.org/details.php?id=grctr",
        raw_zip=Path("data/raw/ebible/grctr_usfm.zip"),
        out_csv=Path("data/processed/ebible/grctr.csv"),
        out_manifest=Path("data/processed/ebible/grctr.manifest.json"),
    ),
    "grcmt": EbibleSource(
        source_id="grcmt",
        source_name="eBible Greek Majority Text NT",
        source_url="https://ebible.org/Scriptures/grcmt_usfm.zip",
        details_url="https://ebible.org/bible/details.php?id=grcmt",
        raw_zip=Path("data/raw/ebible/grcmt_usfm.zip"),
        out_csv=Path("data/processed/ebible/grcmt.csv"),
        out_manifest=Path("data/processed/ebible/grcmt.manifest.json"),
    ),
    "grctcgnt": EbibleSource(
        source_id="grctcgnt",
        source_name="eBible Text-Critical Greek NT",
        source_url="https://ebible.org/Scriptures/grctcgnt_usfm.zip",
        details_url="https://ebible.org/details.php?id=grctcgnt",
        raw_zip=Path("data/raw/ebible/grctcgnt_usfm.zip"),
        out_csv=Path("data/processed/ebible/grctcgnt.csv"),
        out_manifest=Path("data/processed/ebible/grctcgnt.manifest.json"),
    ),
    "eng-kjv2006": EbibleSource(
        source_id="eng-kjv2006",
        source_name="eBible English KJV",
        source_url="https://ebible.org/Scriptures/eng-kjv2006_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=eng-kjv2006",
        raw_zip=Path("data/raw/ebible/eng-kjv2006_usfm.zip"),
        out_csv=Path("data/processed/ebible/eng-kjv2006.csv"),
        out_manifest=Path("data/processed/ebible/eng-kjv2006.manifest.json"),
    ),
    "eng-kjv": EbibleSource(
        source_id="eng-kjv",
        source_name="eBible English KJV + Apocrypha",
        source_url="https://ebible.org/Scriptures/eng-kjv_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=eng-kjv",
        raw_zip=Path("data/raw/ebible/eng-kjv_usfm.zip"),
        out_csv=Path("data/processed/ebible/eng-kjv.csv"),
        out_manifest=Path("data/processed/ebible/eng-kjv.manifest.json"),
    ),
    "eng-asv": EbibleSource(
        source_id="eng-asv",
        source_name="eBible American Standard Version",
        source_url="https://ebible.org/Scriptures/eng-asv_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=eng-asv",
        raw_zip=Path("data/raw/ebible/eng-asv_usfm.zip"),
        out_csv=Path("data/processed/ebible/eng-asv.csv"),
        out_manifest=Path("data/processed/ebible/eng-asv.manifest.json"),
    ),
    "engDBY": EbibleSource(
        source_id="engDBY",
        source_name="eBible Darby Translation",
        source_url="https://ebible.org/Scriptures/engDBY_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engDBY",
        raw_zip=Path("data/raw/ebible/engDBY_usfm.zip"),
        out_csv=Path("data/processed/ebible/engDBY.csv"),
        out_manifest=Path("data/processed/ebible/engDBY.manifest.json"),
    ),
    "engDRA": EbibleSource(
        source_id="engDRA",
        source_name="eBible Douay-Rheims 1899",
        source_url="https://ebible.org/Scriptures/engDRA_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engDRA",
        raw_zip=Path("data/raw/ebible/engDRA_usfm.zip"),
        out_csv=Path("data/processed/ebible/engDRA.csv"),
        out_manifest=Path("data/processed/ebible/engDRA.manifest.json"),
    ),
    "engerv": EbibleSource(
        source_id="engerv",
        source_name="eBible Easy-to-Read Version",
        source_url="https://ebible.org/Scriptures/engerv_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engerv",
        raw_zip=Path("data/raw/ebible/engerv_usfm.zip"),
        out_csv=Path("data/processed/ebible/engerv.csv"),
        out_manifest=Path("data/processed/ebible/engerv.manifest.json"),
        license_label="copyrighted eBible source; local analysis only; preserve upstream notice",
    ),
    "enggnv": EbibleSource(
        source_id="enggnv",
        source_name="eBible Geneva Bible 1599",
        source_url="https://ebible.org/Scriptures/enggnv_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=enggnv",
        raw_zip=Path("data/raw/ebible/enggnv_usfm.zip"),
        out_csv=Path("data/processed/ebible/enggnv.csv"),
        out_manifest=Path("data/processed/ebible/enggnv.manifest.json"),
    ),
    "enggw": EbibleSource(
        source_id="enggw",
        source_name="eBible GOD'S WORD",
        source_url="https://ebible.org/Scriptures/enggw_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=enggw",
        raw_zip=Path("data/raw/ebible/enggw_usfm.zip"),
        out_csv=Path("data/processed/ebible/enggw.csv"),
        out_manifest=Path("data/processed/ebible/enggw.manifest.json"),
        license_label="copyrighted eBible source; local analysis only; preserve upstream notice",
    ),
    "engnet": EbibleSource(
        source_id="engnet",
        source_name="eBible NET Bible",
        source_url="https://ebible.org/Scriptures/engnet_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engnet",
        raw_zip=Path("data/raw/ebible/engnet_usfm.zip"),
        out_csv=Path("data/processed/ebible/engnet.csv"),
        out_manifest=Path("data/processed/ebible/engnet.manifest.json"),
        license_label="copyrighted eBible source; local analysis only; preserve upstream notice",
    ),
    "engojb": EbibleSource(
        source_id="engojb",
        source_name="eBible Orthodox Jewish Bible",
        source_url="https://ebible.org/Scriptures/engojb_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engojb",
        raw_zip=Path("data/raw/ebible/engojb_usfm.zip"),
        out_csv=Path("data/processed/ebible/engojb.csv"),
        out_manifest=Path("data/processed/ebible/engojb.manifest.json"),
        license_label="CC BY 4.0 per eBible details; preserve attribution and upstream notice",
    ),
    "engwebp": EbibleSource(
        source_id="engwebp",
        source_name="eBible World English Bible",
        source_url="https://ebible.org/Scriptures/engwebp_usfm.zip",
        details_url="https://ebible.org/details.php?id=engwebp",
        raw_zip=Path("data/raw/ebible/engwebp_usfm.zip"),
        out_csv=Path("data/processed/ebible/engwebp.csv"),
        out_manifest=Path("data/processed/ebible/engwebp.manifest.json"),
    ),
    "engWycliffe": EbibleSource(
        source_id="engWycliffe",
        source_name="eBible Wycliffe Bible",
        source_url="https://ebible.org/Scriptures/engWycliffe_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engWycliffe",
        raw_zip=Path("data/raw/ebible/engWycliffe_usfm.zip"),
        out_csv=Path("data/processed/ebible/engWycliffe.csv"),
        out_manifest=Path("data/processed/ebible/engWycliffe.manifest.json"),
    ),
    "engylt": EbibleSource(
        source_id="engylt",
        source_name="eBible Young's Literal Translation",
        source_url="https://ebible.org/Scriptures/engylt_usfm.zip",
        details_url="https://ebible.org/find/show.php?id=engylt",
        raw_zip=Path("data/raw/ebible/engylt_usfm.zip"),
        out_csv=Path("data/processed/ebible/engylt.csv"),
        out_manifest=Path("data/processed/ebible/engylt.manifest.json"),
    ),
    "hebwlc": EbibleSource(
        source_id="hebwlc",
        source_name="eBible Hebrew WLC",
        source_url="https://ebible.org/Scriptures/hebwlc_usfm.zip",
        details_url="https://ebible.org/details.php?id=hebwlc",
        raw_zip=Path("data/raw/ebible/hebwlc_usfm.zip"),
        out_csv=Path("data/processed/ebible/hebwlc.csv"),
        out_manifest=Path("data/processed/ebible/hebwlc.manifest.json"),
    ),
}


def main() -> int:
    args = _parse_args()
    source = SOURCES[args.source]
    zip_path = Path(args.zip_out or source.raw_zip)
    csv_path = Path(args.csv_out or source.out_csv)
    manifest_path = Path(args.manifest_out or source.out_manifest)

    if not args.skip_download or not zip_path.exists():
        _download(args.url or source.source_url, zip_path)

    verses = parse_usfm_zip(zip_path)
    _write_csv(csv_path, verses)
    _write_manifest(
        manifest_path,
        source=source,
        source_url=args.url or source.source_url,
        details_url=args.details_url or source.details_url,
        zip_path=zip_path,
        csv_path=csv_path,
        verses=verses,
    )
    print(csv_path)
    print(manifest_path)
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=sorted(SOURCES), default="grclxx")
    parser.add_argument("--url")
    parser.add_argument("--details-url")
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
    source: EbibleSource,
    source_url: str,
    details_url: str,
    zip_path: Path,
    csv_path: Path,
    verses: list[UsfmVerse],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    book_count = len({verse.book for verse in verses})
    manifest = {
        "source_id": source.source_id,
        "source_name": source.source_name,
        "source_url": source_url,
        "details_url": details_url,
        "license": source.license_label,
        "downloaded_at": datetime.now(UTC).isoformat(),
        "zip_path": str(zip_path),
        "zip_sha256": _sha256(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "csv_path": str(csv_path),
        "book_count": book_count,
        "verse_count": len(verses),
        "normalization": "USFM markers, notes, crossrefs, and standalone Hebrew paragraph markers removed; verse text preserved.",
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
