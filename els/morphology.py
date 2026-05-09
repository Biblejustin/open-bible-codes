"""Morphological token readers for OSHB and MorphGNT."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from .corpus import OT_BOOK_ORDER
from .normalization import normalize_greek, normalize_hebrew
from .word_counts import DEFAULT_MULTIPLES, multiples_for_count


OSIS_NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
CONTENT_POS = {"noun", "verb", "adjective"}

MORPHGNT_BOOKS = {
    "01": "Matt",
    "02": "Mark",
    "03": "Luke",
    "04": "John",
    "05": "Acts",
    "06": "Rom",
    "07": "1Cor",
    "08": "2Cor",
    "09": "Gal",
    "10": "Eph",
    "11": "Phil",
    "12": "Col",
    "13": "1Thess",
    "14": "2Thess",
    "15": "1Tim",
    "16": "2Tim",
    "17": "Titus",
    "18": "Phlm",
    "19": "Heb",
    "20": "Jas",
    "21": "1Pet",
    "22": "2Pet",
    "23": "1John",
    "24": "2John",
    "25": "3John",
    "26": "Jude",
    "27": "Rev",
}

GREEK_POS = {
    "N-": "noun",
    "V-": "verb",
    "A-": "adjective",
    "D-": "adverb",
    "RA": "article",
    "RD": "demonstrative",
    "RI": "interrogative",
    "RP": "personal_pronoun",
    "RR": "relative_pronoun",
    "C-": "conjunction",
    "P-": "preposition",
    "I-": "interjection",
    "X-": "particle",
}

HEBREW_POS = {
    "N": "noun",
    "V": "verb",
    "A": "adjective",
    "R": "preposition",
    "T": "particle",
    "C": "conjunction",
    "P": "pronoun",
    "D": "adverb",
    "S": "suffix",
}


@dataclass(frozen=True)
class MorphToken:
    corpus: str
    language: str
    ref: str
    book: str
    chapter: str
    verse: str
    raw_word: str
    normalized_word: str
    lemma: str
    normalized_lemma: str
    pos: str
    morph: str


@dataclass(frozen=True)
class MorphCountBundle:
    by_lemma: Counter[tuple[str, str]]
    by_book: Counter[tuple[str, str, str]]
    by_chapter: Counter[tuple[str, str, str, str]]
    by_verse: Counter[tuple[str, str, str, str]]
    display_lemmas: dict[str, Counter[str]]
    display_words: dict[tuple[str, str], Counter[str]]
    verse_refs: dict[tuple[str, str], set[str]]
    chapter_refs: dict[tuple[str, str], set[str]]
    book_refs: dict[tuple[str, str], set[str]]


def read_oshb_tokens(path: Path, *, corpus_label: str = "MT_WLC_MORPH") -> list[MorphToken]:
    tokens: list[MorphToken] = []
    files = [file for file in path.glob("*.xml") if file.is_file()]
    for file in sorted(files, key=lambda file: (OT_BOOK_ORDER.get(file.stem, 999), file.stem)):
        root = ET.parse(file).getroot()
        for verse in root.iter(OSIS_NS + "verse"):
            osis_id = verse.attrib.get("osisID", "")
            parts = osis_id.split(".")
            if len(parts) != 3:
                continue
            book, chapter, verse_num = parts
            ref = f"{book} {chapter}:{verse_num}"
            for word in verse.iter(OSIS_NS + "w"):
                raw_word = "".join(word.itertext())
                lemma = lexical_oshb_lemma(word.attrib.get("lemma", ""))
                morph = lexical_oshb_morph(word.attrib.get("morph", ""))
                pos = hebrew_pos(morph)
                tokens.append(
                    MorphToken(
                        corpus=corpus_label,
                        language="hebrew",
                        ref=ref,
                        book=book,
                        chapter=chapter,
                        verse=verse_num,
                        raw_word=raw_word,
                        normalized_word=normalize_hebrew(raw_word),
                        lemma=lemma,
                        normalized_lemma=lemma,
                        pos=pos,
                        morph=morph,
                    )
                )
    return tokens


def read_morphgnt_tokens(path: Path, *, corpus_label: str = "SBLGNT_MORPH") -> list[MorphToken]:
    tokens: list[MorphToken] = []
    files = [file for file in path.glob("*-morphgnt.txt") if file.is_file()]
    for file in sorted(files):
        with file.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 6:
                    continue
                code, pos_code, parse_code, raw_word, _normalized_word, _lemma_text = parts[:6]
                lemma = " ".join(parts[6:]) if len(parts) > 6 else _lemma_text
                book = MORPHGNT_BOOKS.get(code[:2], code[:2])
                chapter = str(int(code[2:4]))
                verse = str(int(code[4:6]))
                ref = f"{book} {chapter}:{verse}"
                tokens.append(
                    MorphToken(
                        corpus=corpus_label,
                        language="greek",
                        ref=ref,
                        book=book,
                        chapter=chapter,
                        verse=verse,
                        raw_word=raw_word,
                        normalized_word=normalize_greek(raw_word),
                        lemma=lemma,
                        normalized_lemma=normalize_greek(lemma),
                        pos=GREEK_POS.get(pos_code, pos_code),
                        morph=parse_code,
                    )
                )
    return tokens


def count_morph_tokens(
    tokens: list[MorphToken],
    *,
    content_pos: set[str] = CONTENT_POS,
) -> MorphCountBundle:
    by_lemma: Counter[tuple[str, str]] = Counter()
    by_book: Counter[tuple[str, str, str]] = Counter()
    by_chapter: Counter[tuple[str, str, str, str]] = Counter()
    by_verse: Counter[tuple[str, str, str, str]] = Counter()
    display_lemmas: dict[str, Counter[str]] = defaultdict(Counter)
    display_words: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    verse_refs: dict[tuple[str, str], set[str]] = defaultdict(set)
    chapter_refs: dict[tuple[str, str], set[str]] = defaultdict(set)
    book_refs: dict[tuple[str, str], set[str]] = defaultdict(set)

    for token in tokens:
        if token.pos not in content_pos:
            continue
        if not token.normalized_lemma:
            continue
        key = (token.pos, token.normalized_lemma)
        chapter_ref = f"{token.book} {token.chapter}"
        by_lemma[key] += 1
        by_book[(token.book, token.pos, token.normalized_lemma)] += 1
        by_chapter[(token.book, token.chapter, token.pos, token.normalized_lemma)] += 1
        by_verse[(token.ref, token.pos, token.normalized_lemma, token.raw_word)] += 1
        display_lemmas[token.normalized_lemma][token.lemma] += 1
        display_words[key][token.raw_word] += 1
        verse_refs[key].add(token.ref)
        chapter_refs[key].add(chapter_ref)
        book_refs[key].add(token.book)

    return MorphCountBundle(
        by_lemma=by_lemma,
        by_book=by_book,
        by_chapter=by_chapter,
        by_verse=by_verse,
        display_lemmas=dict(display_lemmas),
        display_words=dict(display_words),
        verse_refs=dict(verse_refs),
        chapter_refs=dict(chapter_refs),
        book_refs=dict(book_refs),
    )


def lexical_oshb_lemma(raw: str) -> str:
    if not raw:
        return ""
    return raw.split("/")[-1].split()[0]


def lexical_oshb_morph(raw: str) -> str:
    if not raw:
        return ""
    return raw.split("/")[-1]


def hebrew_pos(morph: str) -> str:
    if not morph:
        return ""
    code = morph[1] if morph.startswith("H") and len(morph) > 1 else morph[0]
    return HEBREW_POS.get(code, code)


def preferred_display(display_lemmas: dict[str, Counter[str]], normalized_lemma: str) -> str:
    examples = display_lemmas.get(normalized_lemma)
    if not examples:
        return ""
    return examples.most_common(1)[0][0]


def preferred_word(display_words: dict[tuple[str, str], Counter[str]], pos: str, normalized_lemma: str) -> str:
    examples = display_words.get((pos, normalized_lemma))
    if not examples:
        return ""
    return examples.most_common(1)[0][0]


def format_multiples(count: int) -> str:
    return ";".join(str(value) for value in multiples_for_count(count, DEFAULT_MULTIPLES))
