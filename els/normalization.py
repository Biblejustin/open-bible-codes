"""Script-aware text normalization for ELS search."""

from __future__ import annotations

import unicodedata


HEBREW_FINALS = {
    "ך": "כ",
    "ם": "מ",
    "ן": "נ",
    "ף": "פ",
    "ץ": "צ",
}

HEBREW_LETTERS = {chr(codepoint) for codepoint in range(0x05D0, 0x05EB)}
GREEK_LETTERS = set("αβγδεζηθικλμνξοπρστυφχψωϝϛϙϡ")
ENGLISH_LETTERS = set("abcdefghijklmnopqrstuvwxyz")
MICHIGAN_LETTERS = set(")BGDHWZX+YKLMNS(PCQR$T")
MODIFIED_MICHIGAN_TO_STANDARD = {
    "A": ")",
    "@": "(",
    "#": "$",
    "&": "$",
}
HEBREW_TO_MICHIGAN = {
    "א": ")",
    "ב": "B",
    "ג": "G",
    "ד": "D",
    "ה": "H",
    "ו": "W",
    "ז": "Z",
    "ח": "X",
    "ט": "+",
    "י": "Y",
    "כ": "K",
    "ך": "K",
    "ל": "L",
    "מ": "M",
    "ם": "M",
    "נ": "N",
    "ן": "N",
    "ס": "S",
    "ע": "(",
    "פ": "P",
    "ף": "P",
    "צ": "C",
    "ץ": "C",
    "ק": "Q",
    "ר": "R",
    "ש": "$",
    "ת": "T",
}
GREEK_EQUIVALENTS = {
    "ς": "σ",
    "ϲ": "σ",
    "Ϲ": "σ",
}


def _strip_marks(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(
        char for char in decomposed if not unicodedata.category(char).startswith("M")
    )


def normalize_hebrew(text: str, *, keep_final_forms: bool = False) -> str:
    """Return Hebrew letters only, without vowel/cantillation marks."""
    stripped = _strip_marks(text)
    letters: list[str] = []
    for char in stripped:
        if char not in HEBREW_LETTERS:
            continue
        if keep_final_forms:
            letters.append(char)
        else:
            letters.append(HEBREW_FINALS.get(char, char))
    return "".join(letters)


def normalize_greek(text: str) -> str:
    """Return Greek letters only, without accent/breathing marks."""
    stripped = _strip_marks(text).lower()
    letters: list[str] = []
    for char in stripped:
        char = GREEK_EQUIVALENTS.get(char, char)
        if char in GREEK_LETTERS:
            letters.append(char)
    return "".join(letters)


def normalize_michigan(text: str) -> str:
    """Return Michigan-Claremont Hebrew transliteration letters only."""
    stripped = _strip_marks(text)
    letters: list[str] = []
    for char in stripped:
        if char in HEBREW_TO_MICHIGAN:
            letters.append(HEBREW_TO_MICHIGAN[char])
            continue
        char = char.upper()
        if char in MODIFIED_MICHIGAN_TO_STANDARD:
            letters.append(MODIFIED_MICHIGAN_TO_STANDARD[char])
            continue
        if char in MICHIGAN_LETTERS:
            letters.append(char)
    return "".join(letters)


def normalize_english(text: str) -> str:
    """Return English letters only, lowercased and without marks."""
    stripped = _strip_marks(text).lower()
    return "".join(char for char in stripped if char in ENGLISH_LETTERS)


def normalize_text(
    text: str,
    language: str,
    *,
    keep_hebrew_final_forms: bool = False,
) -> str:
    if language == "hebrew":
        return normalize_hebrew(text, keep_final_forms=keep_hebrew_final_forms)
    if language == "greek":
        return normalize_greek(text)
    if language == "english":
        return normalize_english(text)
    if language in {"michigan", "michigan_claremont"}:
        return normalize_michigan(text)
    raise ValueError(f"unsupported language: {language}")
