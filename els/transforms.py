"""Deterministic text transforms for opt-in ELS search layers."""

from __future__ import annotations

from .corpus import Corpus


HEBREW_ATBASH = {
    "א": "ת",
    "ב": "ש",
    "ג": "ר",
    "ד": "ק",
    "ה": "צ",
    "ו": "פ",
    "ז": "ע",
    "ח": "ס",
    "ט": "נ",
    "י": "מ",
    "כ": "ל",
    "ך": "ל",
    "ל": "כ",
    "מ": "י",
    "ם": "י",
    "נ": "ט",
    "ן": "ט",
    "ס": "ח",
    "ע": "ז",
    "פ": "ו",
    "ף": "ו",
    "צ": "ה",
    "ץ": "ה",
    "ק": "ד",
    "ר": "ג",
    "ש": "ב",
    "ת": "א",
}

TRANSFORM_HEBREW_ATBASH = "hebrew_atbash"


def atbash_hebrew(text: str) -> str:
    """Apply Hebrew atbash letter substitution, preserving unmapped chars."""
    return "".join(HEBREW_ATBASH.get(char, char) for char in text)


def transform_text(text: str, transform: str) -> str:
    if transform == TRANSFORM_HEBREW_ATBASH:
        return atbash_hebrew(text)
    raise ValueError(f"unsupported transform: {transform}")


def transform_corpus(corpus: Corpus, transform: str) -> Corpus:
    """Return a same-offset corpus with transformed letter stream only."""
    if transform == TRANSFORM_HEBREW_ATBASH and corpus.language != "hebrew":
        raise ValueError("hebrew_atbash requires a Hebrew corpus")
    return Corpus(
        name=f"{corpus.name}:{transform}",
        language=corpus.language,
        keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
        text=transform_text(corpus.text, transform),
        verses=corpus.verses,
        position_to_verse=corpus.position_to_verse,
        words=corpus.words,
        position_to_word=corpus.position_to_word,
    )
