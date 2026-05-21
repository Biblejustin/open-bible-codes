import csv
from pathlib import Path

from els.normalization import normalize_text
from scripts import build_user_requested_prospective_terms as builder


def _tracked_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _term_rows(terms: list[builder.Term]) -> list[dict[str, str]]:
    return [term.__dict__ for term in terms]


def test_user_requested_builder_counts_and_categories() -> None:
    greek_rows = builder.build_greek_terms()
    hebrew_rows = builder.build_hebrew_terms()

    assert len(greek_rows) == 443
    assert len(hebrew_rows) == 68
    assert {row.category for row in greek_rows} >= {
        "christ_genealogy",
        "disciples",
        "gospel_women",
        "gospel_people",
        "user_supplied_greek_terms",
    }
    assert {row.category for row in hebrew_rows} >= {
        "christ_genealogy",
        "disciples",
        "gospel_women",
        "gospel_people",
    }


def test_user_requested_terms_are_deduped_by_normalized_surface() -> None:
    for language, rows in [
        ("greek", builder.build_greek_terms()),
        ("hebrew", builder.build_hebrew_terms()),
    ]:
        normalized = [normalize_text(row.term, language) for row in rows]
        term_ids = [row.term_id for row in rows]
        assert len(normalized) == len(set(normalized))
        assert len(term_ids) == len(set(term_ids))
        assert all(term_id.isascii() for term_id in term_ids)


def test_tracked_user_requested_term_files_match_builder() -> None:
    assert _tracked_rows(builder.GREEK_OUT) == _term_rows(builder.build_greek_terms())
    assert _tracked_rows(builder.HEBREW_OUT) == _term_rows(builder.build_hebrew_terms())
