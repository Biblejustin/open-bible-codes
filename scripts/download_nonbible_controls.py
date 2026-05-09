#!/usr/bin/env python3
"""Download non-Bible control corpora for Hebrew, Greek, and English."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


USER_AGENT = "open-bible-codes/0.1 (+https://github.com/Biblejustin/open-bible-codes)"
RAW_DIR = Path("data/raw/nonbible_controls")
PROCESSED_DIR = Path("data/processed/nonbible_controls")


@dataclass(frozen=True)
class NonBibleSource:
    source_id: str
    language: str
    name: str
    kind: str
    source_url: str
    details_url: str
    license: str
    raw_path: Path
    out_text: Path
    manifest_path: Path


def source(
    source_id: str,
    language: str,
    name: str,
    kind: str,
    source_url: str,
    details_url: str,
    license: str,
    raw_suffix: str,
) -> NonBibleSource:
    return NonBibleSource(
        source_id=source_id,
        language=language,
        name=name,
        kind=kind,
        source_url=source_url,
        details_url=details_url,
        license=license,
        raw_path=RAW_DIR / raw_suffix,
        out_text=PROCESSED_DIR / f"{source_id}.txt",
        manifest_path=PROCESSED_DIR / f"{source_id}.manifest.json",
    )


SOURCES = {
    "hebrew_pby_bialik": source(
        "hebrew_pby_bialik",
        "hebrew",
        "Project Ben-Yehuda Haim Nahman Bialik",
        "github_dir_text",
        "https://api.github.com/repos/projectbenyehuda/public_domain_dump/contents/txt_stripped/p89?ref=master",
        "https://github.com/projectbenyehuda/public_domain_dump",
        "public domain; Project Ben-Yehuda public domain dump",
        "hebrew_pby_bialik",
    ),
    "hebrew_pby_brenner": source(
        "hebrew_pby_brenner",
        "hebrew",
        "Project Ben-Yehuda Yosef Haim Brenner",
        "github_dir_text",
        "https://api.github.com/repos/projectbenyehuda/public_domain_dump/contents/txt_stripped/p66?ref=master",
        "https://github.com/projectbenyehuda/public_domain_dump",
        "public domain; Project Ben-Yehuda public domain dump",
        "hebrew_pby_brenner",
    ),
    "hebrew_pby_ahad_haam": source(
        "hebrew_pby_ahad_haam",
        "hebrew",
        "Project Ben-Yehuda Ahad Ha'am",
        "github_dir_text",
        "https://api.github.com/repos/projectbenyehuda/public_domain_dump/contents/txt_stripped/p23?ref=master",
        "https://github.com/projectbenyehuda/public_domain_dump",
        "public domain; Project Ben-Yehuda public domain dump",
        "hebrew_pby_ahad_haam",
    ),
    "greek_perseus_iliad": source(
        "greek_perseus_iliad",
        "greek",
        "Perseus Homer Iliad",
        "tei_xml",
        "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml",
        "https://github.com/PerseusDL/canonical-greekLit",
        "CC BY-SA 4.0 unless otherwise indicated by PerseusDL/canonical-greekLit",
        "greek_perseus_iliad.xml",
    ),
    "greek_perseus_odyssey": source(
        "greek_perseus_odyssey",
        "greek",
        "Perseus Homer Odyssey",
        "tei_xml",
        "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml",
        "https://github.com/PerseusDL/canonical-greekLit",
        "CC BY-SA 4.0 unless otherwise indicated by PerseusDL/canonical-greekLit",
        "greek_perseus_odyssey.xml",
    ),
    "greek_perseus_herodotus": source(
        "greek_perseus_herodotus",
        "greek",
        "Perseus Herodotus Histories",
        "tei_xml",
        "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0016/tlg001/tlg0016.tlg001.perseus-grc2.xml",
        "https://github.com/PerseusDL/canonical-greekLit",
        "CC BY-SA 4.0 unless otherwise indicated by PerseusDL/canonical-greekLit",
        "greek_perseus_herodotus.xml",
    ),
    "english_pg_shakespeare": source(
        "english_pg_shakespeare",
        "english",
        "Project Gutenberg Complete Works of William Shakespeare",
        "gutenberg_text",
        "https://www.gutenberg.org/cache/epub/100/pg100.txt",
        "https://www.gutenberg.org/ebooks/100",
        "public domain in the USA; Project Gutenberg",
        "english_pg_shakespeare.txt",
    ),
    "english_pg_war_and_peace": source(
        "english_pg_war_and_peace",
        "english",
        "Project Gutenberg War and Peace",
        "gutenberg_text",
        "https://www.gutenberg.org/cache/epub/2600/pg2600.txt",
        "https://www.gutenberg.org/ebooks/2600",
        "public domain in the USA; Project Gutenberg",
        "english_pg_war_and_peace.txt",
    ),
    "english_pg_moby_dick": source(
        "english_pg_moby_dick",
        "english",
        "Project Gutenberg Moby Dick",
        "gutenberg_text",
        "https://www.gutenberg.org/cache/epub/2701/pg2701.txt",
        "https://www.gutenberg.org/ebooks/2701",
        "public domain in the USA; Project Gutenberg",
        "english_pg_moby_dick.txt",
    ),
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    selected = selected_sources(args)
    for item in selected:
        if not args.refresh and item.out_text.exists() and item.manifest_path.exists():
            print(f"cached {item.source_id}")
            continue
        download_source(item)
        print(item.out_text)
        print(item.manifest_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=sorted(SOURCES), action="append", default=[])
    parser.add_argument("--language", choices=["hebrew", "greek", "english"], action="append", default=[])
    parser.add_argument("--refresh", action="store_true")
    return parser


def selected_sources(args: argparse.Namespace) -> list[NonBibleSource]:
    items = list(SOURCES.values())
    if args.source:
        allowed_sources = set(args.source)
        items = [item for item in items if item.source_id in allowed_sources]
    if args.language:
        allowed_languages = set(args.language)
        items = [item for item in items if item.language in allowed_languages]
    return sorted(items, key=lambda item: (item.language, item.source_id))


def download_source(item: NonBibleSource) -> None:
    if item.kind == "github_dir_text":
        raw_files = download_github_dir_text(item)
        text = "\n\n".join(path.read_text(encoding="utf-8") for path in raw_files)
        write_processed(item, text, raw_files)
        return
    payload = download_bytes(item.source_url)
    item.raw_path.parent.mkdir(parents=True, exist_ok=True)
    item.raw_path.write_bytes(payload)
    if item.kind == "tei_xml":
        text = tei_xml_to_text(payload)
    elif item.kind == "gutenberg_text":
        text = strip_gutenberg_boilerplate(payload.decode("utf-8-sig"))
    else:
        text = payload.decode("utf-8-sig")
    write_processed(item, text, [item.raw_path])


def download_github_dir_text(item: NonBibleSource) -> list[Path]:
    entries = json.loads(download_bytes(item.source_url).decode("utf-8"))
    if not isinstance(entries, list):
        raise ValueError(f"GitHub directory listing did not return a list: {item.source_url}")
    raw_dir = item.raw_path
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_files: list[Path] = []
    for entry in sorted(entries, key=lambda row: str(row.get("name", ""))):
        if entry.get("type") != "file" or not str(entry.get("name", "")).endswith(".txt"):
            continue
        download_url = entry.get("download_url")
        if not download_url:
            continue
        path = raw_dir / str(entry["name"])
        path.write_bytes(download_bytes(str(download_url)))
        raw_files.append(path)
    if not raw_files:
        raise ValueError(f"no text files found for {item.source_id}")
    return raw_files


def write_processed(item: NonBibleSource, text: str, raw_files: list[Path]) -> None:
    item.out_text.parent.mkdir(parents=True, exist_ok=True)
    item.out_text.write_text(text.rstrip() + "\n", encoding="utf-8")
    item.manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_id": item.source_id,
        "language": item.language,
        "name": item.name,
        "kind": item.kind,
        "source_url": item.source_url,
        "details_url": item.details_url,
        "license": item.license,
        "downloaded_at": datetime.now(UTC).isoformat(),
        "processed_path": str(item.out_text),
        "processed_bytes": item.out_text.stat().st_size,
        "processed_sha256": sha256_file(item.out_text),
        "raw_files": [
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in raw_files
        ],
    }
    item.manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def tei_xml_to_text(payload: bytes) -> str:
    root = ET.fromstring(payload)
    found_text_node = first_by_local_name(root, "text")
    text_node = found_text_node if found_text_node is not None else root
    parts: list[str] = []
    for element in text_node.iter():
        if element.text:
            parts.append(element.text)
        if element.tail:
            parts.append(element.tail)
    return "\n".join(part.strip() for part in parts if part.strip())


def first_by_local_name(root: ET.Element, local_name: str) -> ET.Element | None:
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == local_name:
            return element
    return None


def strip_gutenberg_boilerplate(text: str) -> str:
    lines = text.splitlines()
    start = 0
    end = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("*** START OF "):
            start = index + 1
            break
    for index, line in enumerate(lines[start:], start=start):
        if line.startswith("*** END OF "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
