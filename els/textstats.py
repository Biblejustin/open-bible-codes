"""Shared text-statistics helpers for the textual-witness analysis scripts.

These started life inside individual scripts (analyze_heptadic_counts,
analyze_panin_claims) and were copied between siblings as the family grew. They
live here so a verse map, a consonant filter, or a gematria table is defined
once. Behavior is identical to the original in-script definitions.
"""

from __future__ import annotations

from .normalization import normalize_greek

GREEK_VOWELS = set("αεηιουω")

# Standard Hebrew gematria (mispar hechrachi); final forms take their base value.
HEB_GEMATRIA = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
    "י": 10, "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50,
    "ס": 60, "ע": 70, "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200,
    "ש": 300, "ת": 400,
}
# Greek isopsephy; final sigma is folded to sigma by normalize_greek already.
GRK_ISOPSEPHY = {
    "α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ζ": 7, "η": 8, "θ": 9,
    "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60, "ο": 70, "π": 80,
    "ρ": 100, "σ": 200, "τ": 300, "υ": 400, "φ": 500, "χ": 600, "ψ": 700, "ω": 800,
}

# OSHB Strong's numbers for the number-seven word family (seven, seventh,
# seventy, week, sevenfold), disambiguated from the homographs swear (7650),
# satisfied (7646-9), oath (7621), and the names Beersheba (884) and
# Bathsheba (1339), which share the consonants but not the sense.
HEBREW_SEVEN_STRONGS = frozenset({"7651", "7637", "7657", "7620", "7659", "7658"})


def verse_map(corpus) -> dict[tuple[str, str, str], str]:
    """Map a loaded corpus to (BOOK, chapter, verse) -> raw verse text."""
    out = {}
    for v in corpus.verses:
        out[(str(v.book).upper(), str(v.chapter), str(v.verse))] = v.raw_text
    return out


def hebrew_letters(text: str) -> str:
    """Consonantal Hebrew letters only (strip vowel points, cantillation, markers)."""
    return "".join(c for c in text if "א" <= c <= "ת")


def greek_tokens(text: str) -> list[str]:
    """Normalized Greek tokens (accents stripped, lowercased, final sigma folded)."""
    return [w for tok in text.replace("¶", " ").split() if (w := normalize_greek(tok))]


def greek_letter_counts(tokens: list[str]) -> tuple[int, int, int]:
    """(letters, vowels, consonants) over normalized Greek tokens."""
    letters = sum(len(t) for t in tokens)
    vowels = sum(1 for t in tokens for c in t if c in GREEK_VOWELS)
    return letters, vowels, letters - vowels


def is_heptad(n: int) -> bool:
    """True when n is a nonzero multiple of seven."""
    return n != 0 and n % 7 == 0


def gematria(letters: str, table: dict[str, int]) -> int:
    """Sum the table values of the letters; unmapped characters contribute nothing."""
    return sum(table.get(c, 0) for c in letters)
