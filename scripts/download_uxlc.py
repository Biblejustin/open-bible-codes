#!/usr/bin/env python3
"""Download Unicode/XML Leningrad Codex XML files into data/raw/uxlc/books."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path


SOURCE_URL = "https://www.tanach.us/Books/Tanach.xml.zip"
DETAILS_URL = "https://www.tanach.us/Pages/About.html"
OUT_DIR = Path("data/raw/uxlc/books")
MANIFEST_PATH = Path("data/raw/uxlc/manifest.json")
USER_AGENT = "open-bible-codes/0.1 (+https://github.com/Biblejustin/open-bible-codes)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    if not args.refresh and (OUT_DIR / "Genesis.xml").exists():
        print("cached")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = download_bytes(SOURCE_URL)
    archive_hash = hashlib.sha256(data).hexdigest()

    extracted: list[dict[str, str | int]] = []
    with zipfile.ZipFile(BytesIO(data)) as archive:
        for member in sorted(archive.namelist()):
            if not is_book_xml(member):
                continue
            out_path = OUT_DIR / Path(member).name
            content = archive.read(member)
            out_path.write_bytes(content)
            extracted.append(
                {
                    "path": str(out_path),
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            )
            print(out_path)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(
            {
                "source": "Unicode/XML Leningrad Codex",
                "source_url": SOURCE_URL,
                "details_url": DETAILS_URL,
                "downloaded_at": datetime.now(UTC).isoformat(),
                "archive_bytes": len(data),
                "archive_sha256": archive_hash,
                "license": "Biblical Hebrew text may be copied without restriction; cite Tanach.us.",
                "files": extracted,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(MANIFEST_PATH)
    return 0


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def is_book_xml(member: str) -> bool:
    path = Path(member)
    return (
        path.parent.name == "Books"
        and path.suffix == ".xml"
        and not path.name.endswith(".DH.xml")
        and path.name not in {"TanachHeader.xml", "TanachIndex.xml"}
    )


if __name__ == "__main__":
    raise SystemExit(main())
