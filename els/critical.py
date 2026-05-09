"""Critical-text omission helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .corpus import Corpus, VerseSpan
from .normalization import normalize_text
from .search import normalize_for_corpus


BOOK_TO_SBL = {
    "MAT": "Matt",
    "MRK": "Mark",
    "LUK": "Luke",
    "JHN": "John",
    "ACT": "Acts",
    "ROM": "Rom",
    "1CO": "1Cor",
    "2CO": "2Cor",
    "GAL": "Gal",
    "EPH": "Eph",
    "PHP": "Phil",
    "COL": "Col",
    "1TH": "1Thess",
    "2TH": "2Thess",
    "1TI": "1Tim",
    "2TI": "2Tim",
    "TIT": "Titus",
    "PHM": "Phlm",
    "HEB": "Heb",
    "JAS": "Jas",
    "1PE": "1Pet",
    "2PE": "2Pet",
    "1JN": "1John",
    "2JN": "2John",
    "3JN": "3John",
    "JUD": "Jude",
    "REV": "Rev",
    "Matthew": "Matt",
    "Mark": "Mark",
    "Luke": "Luke",
    "John": "John",
    "Acts": "Acts",
    "Romans": "Rom",
    "1 Corinthians": "1Cor",
    "2 Corinthians": "2Cor",
    "Galatians": "Gal",
    "Ephesians": "Eph",
    "Philippians": "Phil",
    "Colossians": "Col",
    "1 Thessalonians": "1Thess",
    "2 Thessalonians": "2Thess",
    "1 Timothy": "1Tim",
    "2 Timothy": "2Tim",
    "Titus": "Titus",
    "Philemon": "Phlm",
    "Hebrews": "Heb",
    "James": "Jas",
    "1 Peter": "1Pet",
    "2 Peter": "2Pet",
    "1 John": "1John",
    "2 John": "2John",
    "3 John": "3John",
    "Jude": "Jude",
    "Revelation": "Rev",
}


@dataclass(frozen=True)
class OmittedBlock:
    ref: str
    start: int
    end: int
    length: int
    status: str
    used_as_deletion: bool


def classify_missing_verses(tr: Corpus, critical: Corpus) -> list[OmittedBlock]:
    critical_refs = {(verse.book, verse.chapter, verse.verse) for verse in critical.verses}
    critical_verses = list(critical.verses)
    blocks: list[OmittedBlock] = []
    for verse in tr.verses:
        critical_book = BOOK_TO_SBL.get(verse.book, verse.book)
        if (critical_book, verse.chapter, verse.verse) in critical_refs:
            continue
        normalized = normalize_for_corpus(tr, verse.raw_text)
        status = "deleted_block"
        used_as_deletion = True
        if is_adjacent_merge(normalized, verse, critical_book, critical_verses):
            status = "adjacent_merge"
            used_as_deletion = False
        elif normalized.endswith("αμην") and is_adjacent_merge(
            normalized[:-4],
            verse,
            critical_book,
            critical_verses,
        ):
            status = "renumbered_minus_amen"
            used_as_deletion = False
        blocks.append(
            OmittedBlock(
                ref=verse.ref,
                start=verse.norm_start,
                end=verse.norm_end,
                length=verse.norm_length,
                status=status,
                used_as_deletion=used_as_deletion,
            )
        )
    return blocks


def is_adjacent_merge(
    normalized: str,
    verse: VerseSpan,
    critical_book: str,
    critical_verses: list[VerseSpan],
) -> bool:
    if not normalized:
        return False
    try:
        tr_verse_num = int(verse.verse)
    except ValueError:
        return False
    for critical_verse in critical_verses:
        if critical_verse.book != critical_book or critical_verse.chapter != verse.chapter:
            continue
        try:
            critical_verse_num = int(critical_verse.verse)
        except ValueError:
            continue
        if abs(critical_verse_num - tr_verse_num) > 1:
            continue
        critical_normalized = normalize_text(critical_verse.raw_text, "greek")
        if normalized in critical_normalized:
            return True
    return False
