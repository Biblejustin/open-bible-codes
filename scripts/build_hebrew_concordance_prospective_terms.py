#!/usr/bin/env python3
"""Build Hebrew prospective terms from open concordance/lexicon sources."""

from __future__ import annotations

import argparse
import csv
import re
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from els.normalization import normalize_text


STRONGS_URL = (
    "https://raw.githubusercontent.com/openscriptures/strongs/master/"
    "hebrew/StrongHebrewG.xml"
)
STRONGS_XML = Path("data/raw/openscriptures/strongs/StrongHebrewG.xml")
STEP_TAHOT_DIR = Path("data/raw/step/tahot")
OUT = Path("terms/hebrew_concordance_prospective_terms.csv")
MIN_NORMALIZED_LENGTH = 4
SOURCE_NOTE = (
    "source=OpenScriptures StrongHebrewG public domain; "
    "cross_check=STEP Bible TAHOT CC BY 4.0; "
    "registered=2026-05-21 before result-producing prospective run"
)

OSIS_NS = {"osis": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
STEP_STRONG_RE = re.compile(r"^H(?P<number>\d{4})")


@dataclass(frozen=True)
class StrongEntry:
    strong_id: str
    term: str
    normalized: str
    concept: str
    morph: str
    transliteration: str
    xml_lang: str


@dataclass(frozen=True)
class Term:
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    notes: str


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    strongs_xml = Path(args.strongs_xml)
    if args.download_strongs or not strongs_xml.exists():
        download_file(STRONGS_URL, strongs_xml)

    step_counts = load_step_tahot_counts(Path(args.step_tahot_dir))
    rows = build_terms(
        parse_strongs(strongs_xml),
        step_counts=step_counts,
        min_normalized_length=args.min_normalized_length,
        require_step_count=not args.include_zero_step_counts,
    )
    write_terms(Path(args.out), rows)
    print(f"{args.out}: {len(rows)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strongs-xml", type=Path, default=STRONGS_XML)
    parser.add_argument("--step-tahot-dir", type=Path, default=STEP_TAHOT_DIR)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--download-strongs", action="store_true")
    parser.add_argument("--include-zero-step-counts", action="store_true")
    parser.add_argument("--min-normalized-length", type=int, default=MIN_NORMALIZED_LENGTH)
    return parser


def download_file(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Open Bible Codes source importer"})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def parse_strongs(path: Path) -> list[StrongEntry]:
    root = ET.parse(path).getroot()
    entries: list[StrongEntry] = []
    for div in root.findall(".//osis:div[@type='entry']", OSIS_NS):
        word = div.find("osis:w", OSIS_NS)
        if word is None:
            continue
        strong_id = word.attrib.get("ID", "")
        xml_lang = word.attrib.get(XML_LANG, "")
        if not strong_id.startswith("H") or xml_lang not in {"heb", "arc", "x-pn"}:
            continue
        term = (word.text or "").strip() or word.attrib.get("lemma", "").strip()
        normalized = normalize_text(term, "hebrew")
        if not normalized:
            continue
        entries.append(
            StrongEntry(
                strong_id=strong_id,
                term=term,
                normalized=normalized,
                concept=entry_concept(div, word),
                morph=word.attrib.get("morph", "").strip(),
                transliteration=word.attrib.get("xlit", "").strip(),
                xml_lang=xml_lang,
            )
        )
    return entries


def entry_concept(div: ET.Element, word: ET.Element) -> str:
    for item in div.findall("osis:list/osis:item", OSIS_NS):
        text = clean_text(" ".join(item.itertext()))
        if text:
            return compact_concept(text)
    for note_type in ["translation", "explanation"]:
        note = div.find(f"osis:note[@type='{note_type}']", OSIS_NS)
        if note is not None:
            text = clean_text(" ".join(note.itertext()))
            if text:
                return compact_concept(text)
    return word.attrib.get("xlit", "").strip() or word.attrib.get("ID", "").strip()


def clean_text(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())


def compact_concept(value: str, limit: int = 90) -> str:
    text = clean_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip(" ,;:") + "."


def load_step_tahot_counts(raw_dir: Path) -> Counter[str]:
    files = sorted(raw_dir.glob("TAHOT *.txt"))
    if not files:
        raise FileNotFoundError(
            f"missing STEP TAHOT raw files under {raw_dir}; run scripts.download_step_tahot"
        )
    counts: Counter[str] = Counter()
    for path in files:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for row in reader:
                if len(row) <= 8:
                    continue
                strong_id = normalized_step_strong(row[8].strip())
                if strong_id:
                    counts[strong_id] += 1
    return counts


def normalized_step_strong(value: str) -> str:
    match = STEP_STRONG_RE.match(value)
    if not match:
        return ""
    number = int(match.group("number"))
    if number >= 9000:
        return ""
    return f"H{number}"


def build_terms(
    entries: list[StrongEntry],
    *,
    step_counts: Counter[str],
    min_normalized_length: int,
    require_step_count: bool,
) -> list[Term]:
    by_normalized: dict[str, list[StrongEntry]] = {}
    for entry in entries:
        if len(entry.normalized) < min_normalized_length:
            continue
        if require_step_count and step_counts[entry.strong_id] <= 0:
            continue
        by_normalized.setdefault(entry.normalized, []).append(entry)

    rows: list[Term] = []
    for normalized in sorted(by_normalized, key=lambda key: min(strong_number(e.strong_id) for e in by_normalized[key])):
        group = sorted(by_normalized[normalized], key=lambda entry: strong_number(entry.strong_id))
        first = group[0]
        strong_ids = [entry.strong_id for entry in group]
        step_count = sum(step_counts[strong_id] for strong_id in strong_ids)
        rows.append(
            Term(
                term_id=f"hcon_h{strong_number(first.strong_id):04d}",
                concept=first.concept,
                category=category_for(group),
                language="hebrew",
                term=first.term,
                notes=notes_for(group, step_count),
            )
        )
    return rows


def strong_number(strong_id: str) -> int:
    return int(strong_id[1:])


def category_for(group: list[StrongEntry]) -> str:
    morphs = {entry.morph for entry in group}
    if any("n-pr" in morph for morph in morphs):
        return "strong_proper_names"
    if any(morph.startswith("v") for morph in morphs):
        return "strong_verbs"
    if any(morph.startswith("n") for morph in morphs):
        return "strong_nouns"
    if any(morph.startswith("a") for morph in morphs):
        return "strong_adjectives"
    return "strong_particles_other"


def notes_for(group: list[StrongEntry], step_count: int) -> str:
    strong_ids = ",".join(entry.strong_id for entry in group)
    morphs = ",".join(sorted({entry.morph for entry in group if entry.morph}))
    langs = ",".join(sorted({entry.xml_lang for entry in group if entry.xml_lang}))
    xlit = group[0].transliteration
    return (
        f"{SOURCE_NOTE}; strong_ids={strong_ids}; step_tahot_count={step_count}; "
        f"morph={morphs}; xml_lang={langs}; xlit={xlit}"
    )


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
            writer.writerow(term.__dict__)


if __name__ == "__main__":
    raise SystemExit(main())
