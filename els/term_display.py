"""Reader-facing display helpers for Hebrew and Greek report terms."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
import unicodedata


KNOWN_TERMS: dict[str, tuple[str, str]] = {
    "γωγ": ("Gog", "Gog"),
    "ιησουσ": ("Iesous", "Jesus/Joshua"),
    "αιμα": ("haima", "blood"),
    "ναιμανο": ("naimano", "hidden extension form from haima"),
    "δοξα": ("doxa", "glory"),
    "δοξανωσ": ("doxanos", "hidden extension form from doxa"),
    "ισαακ": ("Isaak", "Isaac"),
    "τερασ": ("teras", "wonder"),
    "ανομια": ("anomia", "lawlessness"),
    "υιοσ": ("huios", "son"),
    "ουουιοσ": ("ouhuios", "hidden extension form from huios"),
    "ειουιοσ": ("eiouios", "hidden extension form from huios"),
    "μαρια": ("Maria", "Mary"),
    "ταφοσ": ("taphos", "tomb"),
    "σωτηρ": ("soter", "savior"),
    "ανεστη": ("aneste", "he is risen"),
    "κρισισ": ("krisis", "judgment"),
    "ιουδασ": ("Ioudas", "Judas"),
    "κυριοσ": ("kyrios", "Lord"),
    "πετροσ": ("Petros", "Peter"),
    "θηριον": ("therion", "beast"),
    "δρακων": ("drakon", "dragon"),
    "ιωαννησ": ("Ioannes", "John"),
    "πιλατοσ": ("Pilatos", "Pilate"),
    "χριστοσ": ("Christos", "Christ"),
    "ερχεται": ("erchetai", "he is coming"),
    "ναοσ": ("naos", "temple"),
    "θεοσ": ("theos", "God"),
    "σιων": ("Sion", "Zion"),
    "φωσ": ("phos", "light"),
    "νομοσ": ("nomos", "law"),
    "αμνοσ": ("amnos", "lamb"),
    "ελαμ": ("Elam", "Elam"),
    "νωε": ("Noe", "Noah"),
    "ουλ": ("Oul", "Hul"),
    "σημ": ("Sem", "Shem"),
    "σαλα": ("Sala", "Shelah"),
    "χαμ": ("Cham", "Ham"),
    "ελισα": ("Elisa", "Elishah"),
    "ιωυαν": ("Iouan", "Javan"),
    "ευιλα": ("Euila", "Havilah"),
    "αδαμα": ("Adama", "Admah"),
    "μασση": ("Masse", "Mesha"),
    "ישוע": ("Yeshua", "Yeshua/Jeshua"),
    "יהוה": ("YHWH", "YHWH"),
    "ישראל": ("Yisrael", "Israel"),
    "אלהים": ("Elohim", "God/Elohim"),
    "אדני": ("Adonai", "Lord"),
    "משיח": ("Mashiach", "Messiah/anointed one"),
    "גוג": ("Gog", "Gog"),
    "מגוג": ("Magog", "Magog"),
    "יוםיהוה": ("yom YHWH", "day of YHWH"),
    "יומיהוה": ("yom YHWH", "day of YHWH"),
    "היומיהוה": ("hayom YHWH", "the day of YHWH"),
    "אור": ("or", "light"),
    "מות": ("mavet", "death"),
    "אמת": ("emet", "truth"),
    "משה": ("Moshe", "Moses"),
    "מלך": ("melekh", "king"),
    "נח": ("Noach", "Noah"),
    "שם": ("Shem", "Shem"),
    "חם": ("Cham", "Ham"),
    "חת": ("Chet", "Heth"),
    "מש": ("Mash", "Mash"),
    "יון": ("Yavan", "Javan/Greece"),
    "ארם": ("Aram", "Aram"),
    "משא": ("Mesha", "Mesha"),
    "חוי": ("Chivvi", "Hivite"),
    "מדי": ("Madai", "Media"),
    "להבים": ("Lehabim", "Lehabim"),
    "נינוה": ("Nineveh", "Nineveh"),
    "אלישה": ("Elishah", "Elishah"),
    "לודים": ("Ludim", "Ludim"),
    "חוילה": ("Havilah", "Havilah"),
    "און": ("aven", "lawlessness/iniquity"),
    "בבל": ("Bavel", "Babylon"),
    "חיה": ("chayah", "beast/living creature"),
    "תו": ("tav", "mark/sign"),
    "עד": ("ed", "witness"),
    "צר": ("tsar", "foe/adversary"),
}

TERM_FILES_DIR = Path(__file__).resolve().parents[1] / "terms"

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


def display_term(value: str, *, english: str | None = None, transliteration: str | None = None) -> str:
    """Return a Markdown display string with transliteration and English gloss when useful."""
    text = value.strip()
    if not text:
        return ""
    if not (contains_hebrew(text) or contains_greek(text)):
        return f"`{text}`"

    key = normalized_script_key(text)
    known_transliteration, fallback_english = known_term_display(key)
    transliteration = transliteration or known_transliteration or transliterate(text)
    gloss = english or fallback_english
    if gloss:
        return f"`{text}` ({transliteration}; English: {gloss})"
    return f"`{text}` ({transliteration})"


def known_term_display(key: str) -> tuple[str, str]:
    """Return display metadata for a normalized script key."""
    if key in KNOWN_TERMS:
        return KNOWN_TERMS[key]
    return csv_known_terms().get(key, ("", ""))


@lru_cache(maxsize=1)
def csv_known_terms() -> dict[str, tuple[str, str]]:
    """Load unambiguous Hebrew/Greek term concepts from committed term CSVs.

    Report builders often only have a normalized term value by the time they
    render Markdown. This fallback keeps those searched terms reader-facing
    without guessing for ambiguous duplicate entries.
    """
    if not TERM_FILES_DIR.exists():
        return {}

    concepts_by_key: dict[str, set[str]] = {}
    for path in sorted(TERM_FILES_DIR.glob("*.csv")):
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    term = row.get("term", "").strip()
                    concept = row.get("concept", "").strip()
                    if not term or not concept:
                        continue
                    if not (contains_hebrew(term) or contains_greek(term)):
                        continue
                    key = normalized_script_key(term)
                    if key:
                        concepts_by_key.setdefault(key, set()).add(concept)
        except (OSError, csv.Error, UnicodeDecodeError):
            continue

    return {key: ("", sorted(concepts)[0]) for key, concepts in concepts_by_key.items() if len(concepts) == 1}


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
