#!/usr/bin/env python3
"""Build Greek prospective terms from Strong's Greek Dictionary XML."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.normalization import normalize_text


SOURCE_URL = (
    "https://raw.githubusercontent.com/morphgnt/strongs-dictionary-xml/"
    "master/strongsgreek.xml"
)
README_URL = (
    "https://raw.githubusercontent.com/morphgnt/strongs-dictionary-xml/"
    "master/README.md"
)
SOURCE_XML = Path("data/raw/morphgnt/strongs-dictionary-xml/strongsgreek.xml")
OUT = Path("terms/greek_lexicon_prospective_terms.csv")
SUMMARY_OUT = Path("reports/study_locks/greek_lexicon_prospective_terms.summary.json")
MIN_NORMALIZED_LENGTH = 5
SOURCE_NOTE = (
    "source=morphgnt/strongs-dictionary-xml; license=CC0-1.0; "
    "source_url=https://github.com/morphgnt/strongs-dictionary-xml; "
    "registered_before_result_producing_run=true"
)


@dataclass(frozen=True)
class StrongGreekEntry:
    strong_id: str
    term: str
    normalized: str
    transliteration: str
    beta: str
    concept: str
    derivation: str


@dataclass(frozen=True)
class Term:
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    notes: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_xml = Path(args.source_xml)
    if args.download or not source_xml.exists():
        download_file(SOURCE_URL, source_xml)

    entries = parse_strongs_greek(source_xml)
    terms = build_terms(entries, min_normalized_length=args.min_normalized_length)
    write_terms(Path(args.out), terms)
    write_summary(
        Path(args.summary_out),
        {
            "tool": "build_greek_lexicon_prospective_terms",
            "edls_version": __version__,
            "generated_at": datetime.now(UTC).isoformat(),
            "duration_seconds": round(time.perf_counter() - started, 6),
            "source_url": SOURCE_URL,
            "license_readme_url": README_URL,
            "license": "CC0-1.0",
            "source_xml": str(source_xml),
            "source_sha256": sha256_file(source_xml),
            "out": str(args.out),
            "min_normalized_length": args.min_normalized_length,
            "raw_entry_count": len(entries),
            "output_rows": len(terms),
            "category_counts": dict(Counter(term.category for term in terms)),
        },
    )
    print(f"{args.out}: {len(terms)}")
    print(args.summary_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-xml", type=Path, default=SOURCE_XML)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--min-normalized-length", type=int, default=MIN_NORMALIZED_LENGTH)
    return parser


def download_file(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Open Bible Codes source importer"})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def parse_strongs_greek(path: Path) -> list[StrongGreekEntry]:
    root = ET.parse(path).getroot()
    entries: list[StrongGreekEntry] = []
    for entry in root.findall(".//entry"):
        strong_id = normalize_strong_id(entry.attrib.get("strongs", ""))
        if not strong_id:
            continue
        greek = entry.find("greek")
        if greek is None:
            continue
        term = greek.attrib.get("unicode", "").strip()
        normalized = normalize_text(term, "greek")
        if not normalized:
            continue
        entries.append(
            StrongGreekEntry(
                strong_id=strong_id,
                term=term,
                normalized=normalized,
                transliteration=greek.attrib.get("translit", "").strip(),
                beta=greek.attrib.get("BETA", "").strip(),
                concept=entry_concept(entry),
                derivation=element_text(entry.find("strongs_derivation")),
            )
        )
    return entries


def normalize_strong_id(value: str) -> str:
    digits = "".join(char for char in value if char.isdigit())
    if not digits:
        return ""
    return f"G{int(digits):05d}"


def entry_concept(entry: ET.Element) -> str:
    for tag in ("strongs_def", "kjv_def", "strongs_derivation"):
        text = compact_concept(element_text(entry.find(tag)))
        if text:
            return text
    strong = entry.findtext("strongs", default="").strip()
    return f"Strong G{int(strong):05d}" if strong.isdigit() else "Strong Greek entry"


def element_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join(" ".join(element.itertext()).replace("\n", " ").split())


def compact_concept(value: str, limit: int = 90) -> str:
    text = " ".join(value.replace(":--", " ").replace("--", " ").split()).strip(" ;,:")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip(" ,;:") + "."


def build_terms(entries: list[StrongGreekEntry], *, min_normalized_length: int) -> list[Term]:
    by_normalized: dict[str, list[StrongGreekEntry]] = {}
    for entry in entries:
        if len(entry.normalized) < min_normalized_length:
            continue
        by_normalized.setdefault(entry.normalized, []).append(entry)

    rows: list[Term] = []
    for normalized in sorted(by_normalized, key=lambda key: min(strong_number(e.strong_id) for e in by_normalized[key])):
        group = sorted(by_normalized[normalized], key=lambda entry: strong_number(entry.strong_id))
        first = group[0]
        rows.append(
            Term(
                term_id=f"glex_g{strong_number(first.strong_id):05d}",
                concept=first.concept,
                category=category_for(group),
                language="greek",
                term=first.term,
                notes=notes_for(group),
            )
        )
    return rows


def strong_number(strong_id: str) -> int:
    return int(strong_id[1:])


def category_for(group: list[StrongGreekEntry]) -> str:
    derivations = " ".join(entry.derivation.lower() for entry in group)
    if "hebrew origin" in derivations or "chaldee origin" in derivations:
        return "strongs_greek_semitic_origin"
    return "strongs_greek_lexicon"


def notes_for(group: list[StrongGreekEntry]) -> str:
    strong_ids = ",".join(entry.strong_id for entry in group)
    transliterations = ",".join(sorted({entry.transliteration for entry in group if entry.transliteration}))
    beta = ",".join(sorted({entry.beta for entry in group if entry.beta}))
    return f"{SOURCE_NOTE}; strong_ids={strong_ids}; translit={transliterations}; beta={beta}"


def write_terms(path: Path, terms: list[Term]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["term_id", "concept", "category", "language", "term", "notes"],
            lineterminator="\n",
        )
        writer.writeheader()
        for term in terms:
            writer.writerow(asdict(term))


def write_summary(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
