#!/usr/bin/env python3
"""Download Miqra according to the Masorah HTML files into data/raw/mam/html."""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path


INDEX_URL = "https://bdenckla.github.io/MAM-with-doc/"
SOURCE_ATTRIBUTION_URL = "https://he.wikisource.org/wiki/מקרא_על_פי_המסורה"
OUT_DIR = Path("data/raw/mam/html")
MANIFEST_PATH = Path("data/raw/mam/manifest.json")
USER_AGENT = "open-bible-codes/0.1 (+https://github.com/Biblejustin/open-bible-codes)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    if not args.refresh and existing_book_count() == 39 and MANIFEST_PATH.exists():
        print("cached")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_html = download_text(INDEX_URL)
    links = MAMIndexParser()
    links.feed(index_html)
    links.close()

    expected_names = {Path(urllib.parse.unquote(href)).name for href in links.book_links}
    for existing in OUT_DIR.glob("*.html"):
        if existing.name not in expected_names:
            existing.unlink()

    extracted: list[dict[str, str | int]] = []
    for href in links.book_links:
        url = urllib.parse.urljoin(INDEX_URL, urllib.parse.quote(href))
        content = download_bytes(url)
        out_path = OUT_DIR / Path(urllib.parse.unquote(href)).name
        out_path.write_bytes(content)
        extracted.append(
            {
                "path": str(out_path),
                "source_url": url,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
        print(out_path)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(
            {
                "source": "Miqra according to the Masorah",
                "source_url": INDEX_URL,
                "source_attribution_url": SOURCE_ATTRIBUTION_URL,
                "downloaded_at": datetime.now(UTC).isoformat(),
                "license": "CC BY-SA 4.0",
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


class MAMIndexParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.book_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = {key: value or "" for key, value in attrs}
        href = values.get("href", "")
        if is_book_href(href):
            self.book_links.append(href)


def download_text(url: str) -> str:
    return download_bytes(url).decode("utf-8")


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def existing_book_count() -> int:
    if not OUT_DIR.exists():
        return 0
    return sum(
        1
        for path in OUT_DIR.glob("*.html")
        if path.is_file() and is_book_href(path.name)
    )


def is_book_href(href: str) -> bool:
    return href.endswith(".html") and "/" not in href and href[:1] in {"A", "B", "C", "D", "E", "F"}


if __name__ == "__main__":
    raise SystemExit(main())
