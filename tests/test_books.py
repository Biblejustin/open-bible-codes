"""Lock the shared canonical book-name map."""

from __future__ import annotations

from els.books import ENGLISH_NAME_TO_CODE, canonical_book_code


def test_full_english_names_map_to_codes() -> None:
    assert canonical_book_code("Genesis") == "GEN"
    assert canonical_book_code("John") == "JHN"
    assert canonical_book_code("Revelation") == "REV"
    assert canonical_book_code("1 Corinthians") == "1CO"


def test_psalm_and_psalms_both_map() -> None:
    assert canonical_book_code("Psalm") == "PSA"
    assert canonical_book_code("Psalms") == "PSA"


def test_already_coded_or_unknown_passes_through() -> None:
    assert canonical_book_code("JHN") == "JHN"
    assert canonical_book_code("Unknownia") == "Unknownia"


def test_all_codes_are_three_chars() -> None:
    for code in ENGLISH_NAME_TO_CODE.values():
        assert len(code) == 3 and code.isupper()
