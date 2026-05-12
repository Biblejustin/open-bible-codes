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

HEBREW_ALBAM = {
    "א": "ל",
    "ב": "מ",
    "ג": "נ",
    "ד": "ס",
    "ה": "ע",
    "ו": "פ",
    "ז": "צ",
    "ח": "ק",
    "ט": "ר",
    "י": "ש",
    "כ": "ת",
    "ך": "ת",
    "ל": "א",
    "מ": "ב",
    "ם": "ב",
    "נ": "ג",
    "ן": "ג",
    "ס": "ד",
    "ע": "ה",
    "פ": "ו",
    "ף": "ו",
    "צ": "ז",
    "ץ": "ז",
    "ק": "ח",
    "ר": "ט",
    "ש": "י",
    "ת": "כ",
}

TRANSFORM_HEBREW_ATBASH = "hebrew_atbash"
TRANSFORM_HEBREW_ALBAM = "hebrew_albam"
TRANSFORM_PLAIN = "plain"
HEBREW_TRANSFORMS = {TRANSFORM_HEBREW_ATBASH, TRANSFORM_HEBREW_ALBAM}


def atbash_hebrew(text: str) -> str:
    """Apply Hebrew atbash letter substitution, preserving unmapped chars."""
    return "".join(HEBREW_ATBASH.get(char, char) for char in text)


def albam_hebrew(text: str) -> str:
    """Apply Hebrew albam letter substitution, preserving unmapped chars."""
    return "".join(HEBREW_ALBAM.get(char, char) for char in text)


def transform_text(text: str, transform: str) -> str:
    if transform == TRANSFORM_PLAIN:
        return text
    if transform == TRANSFORM_HEBREW_ATBASH:
        return atbash_hebrew(text)
    if transform == TRANSFORM_HEBREW_ALBAM:
        return albam_hebrew(text)
    raise ValueError(f"unsupported transform: {transform}")


def transform_corpus(corpus: Corpus, transform: str) -> Corpus:
    """Return a same-offset corpus with transformed letter stream only."""
    if transform == TRANSFORM_PLAIN:
        return Corpus(
            name=f"{corpus.name}:{transform}",
            language=corpus.language,
            keep_hebrew_final_forms=corpus.keep_hebrew_final_forms,
            text=corpus.text,
            verses=corpus.verses,
            position_to_verse=corpus.position_to_verse,
            words=corpus.words,
            position_to_word=corpus.position_to_word,
        )
    if transform in HEBREW_TRANSFORMS and corpus.language != "hebrew":
        raise ValueError(f"{transform} requires a Hebrew corpus")
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
