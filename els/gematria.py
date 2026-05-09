"""Basic Hebrew numeral helpers for date terms."""

from __future__ import annotations


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
