"""Basic Hebrew numeral and gematria helpers for date and skip studies."""

from __future__ import annotations

import unicodedata


HEBREW_ONES = {
    1: "א",
    2: "ב",
    3: "ג",
    4: "ד",
    5: "ה",
    6: "ו",
    7: "ז",
    8: "ח",
    9: "ט",
}

HEBREW_TENS = {
    10: "י",
    20: "כ",
    30: "ל",
    40: "מ",
    50: "נ",
    60: "ס",
    70: "ע",
    80: "פ",
    90: "צ",
}

HEBREW_HUNDREDS = {
    100: "ק",
    200: "ר",
    300: "ש",
    400: "ת",
}

HEBREW_STANDARD_VALUES = {
    **{letter: value for value, letter in HEBREW_ONES.items()},
    **{letter: value for value, letter in HEBREW_TENS.items()},
    **{letter: value for value, letter in HEBREW_HUNDREDS.items()},
    "ך": 20,
    "ם": 40,
    "ן": 50,
    "ף": 80,
    "ץ": 90,
}

GREEK_STANDARD_VALUES = {
    "α": 1,
    "β": 2,
    "γ": 3,
    "δ": 4,
    "ε": 5,
    "ϛ": 6,
    "ς": 200,
    "ζ": 7,
    "η": 8,
    "θ": 9,
    "ι": 10,
    "κ": 20,
    "λ": 30,
    "μ": 40,
    "ν": 50,
    "ξ": 60,
    "ο": 70,
    "π": 80,
    "ϟ": 90,
    "ρ": 100,
    "σ": 200,
    "τ": 300,
    "υ": 400,
    "φ": 500,
    "χ": 600,
    "ψ": 700,
    "ω": 800,
    "ϡ": 900,
}

HEBREW_LANGUAGES = {"hebrew", "michigan"}
GREEK_LANGUAGES = {"greek"}


def _strip_marks(value: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value.lower())
        if unicodedata.category(char) != "Mn"
    )


def hebrew_standard_value(text: str) -> int:
    """Standard Hebrew gematria sum, ignoring unmapped characters."""
    return sum(HEBREW_STANDARD_VALUES.get(char, 0) for char in text)


def greek_standard_value(text: str) -> int:
    """Standard Greek isopsephy sum, ignoring unmapped characters."""
    return sum(GREEK_STANDARD_VALUES.get(char, 0) for char in _strip_marks(text))


def standard_gematria_value(text: str, language: str = "") -> tuple[str, int]:
    """Return the standard scheme and value for Hebrew or Greek text."""
    language = language.strip().lower()
    if language in HEBREW_LANGUAGES:
        return "hebrew_standard", hebrew_standard_value(text)
    if language in GREEK_LANGUAGES:
        return "greek_standard", greek_standard_value(text)
    if any(char in HEBREW_STANDARD_VALUES for char in text):
        return "hebrew_standard", hebrew_standard_value(text)
    stripped = _strip_marks(text)
    if any(char in GREEK_STANDARD_VALUES for char in stripped):
        return "greek_standard", greek_standard_value(stripped)
    return "", 0


def hebrew_number(value: int) -> str:
    """Canonical Hebrew numeral letters for 1..999, without punctuation."""
    if value <= 0 or value > 999:
        raise ValueError("hebrew_number supports 1..999")

    letters: list[str] = []
    hundreds = value // 100
    remainder = value % 100
    while hundreds >= 4:
        letters.append(HEBREW_HUNDREDS[400])
        hundreds -= 4
    if hundreds:
        letters.append(HEBREW_HUNDREDS[hundreds * 100])

    if remainder == 15:
        letters.append("טו")
    elif remainder == 16:
        letters.append("טז")
    else:
        tens = remainder // 10
        ones = remainder % 10
        if tens:
            letters.append(HEBREW_TENS[tens * 10])
        if ones:
            letters.append(HEBREW_ONES[ones])

    return "".join(letters)


def hebrew_year_remainder(year: int) -> str:
    """Common Jewish-year style: omit thousands, e.g. 5785 -> תשפה."""
    return hebrew_number(year % 1000)


def hebrew_year_compact(year: int) -> str:
    """Compact thousands style, e.g. 2024 -> בכד, punctuation omitted."""
    thousands = year // 1000
    remainder = year % 1000
    if thousands <= 0:
        return hebrew_number(year)
    return HEBREW_ONES[thousands] + hebrew_number(remainder)


def hebrew_year_additive(year: int) -> str:
    """Pure additive value, e.g. 2024 -> תתתתתכד."""
    if year <= 0:
        raise ValueError("year must be positive")
    letters: list[str] = []
    remainder = year
    while remainder >= 400:
        letters.append("ת")
        remainder -= 400
    if remainder:
        letters.append(hebrew_number(remainder))
    return "".join(letters)
