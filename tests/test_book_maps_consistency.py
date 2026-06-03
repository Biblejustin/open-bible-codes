"""Cross-map consistency guards for the book tables.

These lock invariants across the four book maps that currently live in separate
modules (els.corpus, els.critical, els.morphology, els.books). They are pure
data checks -- no corpora needed -- and they guard the duplicate-order class of
bug (an earlier OT_BOOK_ORDER had `Ruth` twice) plus cross-map reference drift.
When the maps are eventually consolidated into els.books, these keep the move
honest.
"""

from __future__ import annotations

from els.books import ENGLISH_NAME_TO_CODE
from els.corpus import NT_BOOK_ORDER, OT_BOOK_ORDER
from els.critical import BOOK_TO_SBL
from els.morphology import MORPHGNT_BOOKS


def test_nt_order_is_contiguous_1_to_27() -> None:
    assert len(NT_BOOK_ORDER) == 27
    assert sorted(NT_BOOK_ORDER.values()) == list(range(1, 28))


def test_ot_order_is_contiguous_1_to_39_no_duplicates() -> None:
    # An earlier bug had `Ruth` mapped to two different orders; this guards it.
    assert len(OT_BOOK_ORDER) == 39
    assert sorted(OT_BOOK_ORDER.values()) == list(range(1, 40))


def test_morphgnt_codes_are_two_digit_and_name_valid_nt_books() -> None:
    assert len(MORPHGNT_BOOKS) == 27
    for code, sbl in MORPHGNT_BOOKS.items():
        assert len(code) == 2 and code.isdigit(), code
        assert sbl in NT_BOOK_ORDER, sbl


def test_book_to_sbl_targets_are_canonical_nt_books() -> None:
    # Every value BOOK_TO_SBL maps to must be a recognized NT book name.
    for source, sbl in BOOK_TO_SBL.items():
        assert sbl in NT_BOOK_ORDER, (source, sbl)


def test_english_name_map_covers_all_66_canonical_books() -> None:
    # Psalm/Psalms and Song of Solomon/Song of Songs are aliases, so distinct
    # codes collapse to the 66-book canon.
    assert len(set(ENGLISH_NAME_TO_CODE.values())) == 66
