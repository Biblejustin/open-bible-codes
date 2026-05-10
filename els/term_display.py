"""Reader-facing display helpers for Hebrew and Greek report terms."""

from __future__ import annotations

import unicodedata


KNOWN_TERMS: dict[str, tuple[str, str]] = {
    "γωγ": ("Gog", "Gog"),
    "ιησουσ": ("Iesous", "Jesus/Joshua"),
    "δοξα": ("doxa", "glory"),
    "δοξανωσ": ("doxanos", "hidden extension form from doxa"),
    "ισαακ": ("Isaak", "Isaac"),
    "τερας": ("teras", "wonder"),
    "ανομια": ("anomia", "lawlessness"),
    "ישוע": ("Yeshua", "Yeshua/Jeshua"),
    "משיח": ("Mashiach", "Messiah/anointed one"),
    "יוםיהוה": ("yom YHWH", "day of YHWH"),
    "יומיהוה": ("yom YHWH", "day of YHWH"),
    "היומיהוה": ("hayom YHWH", "the day of YHWH"),
}

GREEK_MAP = {
    "α": "a",
    "β": "b",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "e",
    "θ": "th",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "υ": "u",
    "φ": "ph",
    "χ": "ch",
    "ψ": "ps",
    "ω": "o",
}

HEBREW_MAP = {
    "א": "",
    "ב": "b",
    "ג": "g",
    "ד": "d",
    "ה": "h",
    "ו": "w",
    "ז": "z",
    "ח": "ch",
    "ט": "t",
    "י": "y",
    "כ": "k",
    "ך": "k",
    "ל": "l",
    "מ": "m",
    "ם": "m",
    "נ": "n",
    "ן": "n",
    "ס": "s",
    "ע": "",
    "פ": "p",
    "ף": "p",
    "צ": "ts",
    "ץ": "ts",
    "ק": "q",
    "ר": "r",
    "ש": "sh",
    "ת": "t",
}


def display_term(value: str, *, english: str | None = None) -> str:
    """Return a Markdown display string with transliteration and English gloss when useful."""
    text = value.strip()
    if not text:
        return ""
    if not (contains_hebrew(text) or contains_greek(text)):
        return f"`{text}`"

    key = normalized_script_key(text)
    transliteration, fallback_english = KNOWN_TERMS.get(key, ("", ""))
    if not transliteration:
        transliteration = transliterate(text)
    gloss = english or fallback_english
    if gloss:
        return f"`{text}` ({transliteration}; English: {gloss})"
    return f"`{text}` ({transliteration})"


def display_center(ref: str, center_word: str) -> str:
    if contains_hebrew(center_word) or contains_greek(center_word):
        return " ".join(part for part in [ref, display_term(center_word)] if part)
    return " ".join(part for part in [ref, center_word] if part)


def contains_hebrew(value: str) -> bool:
    return any("\u0590" <= char <= "\u05ff" for char in value)


def contains_greek(value: str) -> bool:
    return any("\u0370" <= char <= "\u03ff" or "\u1f00" <= char <= "\u1fff" for char in value)


def transliterate(value: str) -> str:
    key = normalized_script_key(value)
    if contains_greek(value):
        return "".join(GREEK_MAP.get(char, char if char.isspace() else "") for char in key).strip()
    if contains_hebrew(value):
        return "".join(HEBREW_MAP.get(char, char if char.isspace() else "") for char in key).strip()
    return value


def normalized_script_key(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    chars = []
    for char in decomposed:
        if unicodedata.combining(char):
            continue
        if char == "ς":
            chars.append("σ")
        elif "\u0590" <= char <= "\u05ff" or "\u0370" <= char <= "\u03ff":
            chars.append(char)
    return "".join(chars)
