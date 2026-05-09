from pathlib import Path

from els.normalization import normalize_text
from scripts import build_greek_expanded_prospective_terms as builder


def test_expanded_terms_exclude_prior_exact_center_normalized_terms() -> None:
    rows = builder.build_rows(Path("terms"), min_length=4)
    existing = builder.existing_normalized_terms(Path("terms/greek_exact_center_cohort_terms.csv"))
    produced = {normalize_text(row["term"], "greek") for row in rows}

    assert rows
    assert produced.isdisjoint(existing)


def test_expanded_terms_are_deduped_by_normalized_form_and_id() -> None:
    rows = builder.build_rows(Path("terms"), min_length=4)
    normalized = [normalize_text(row["term"], "greek") for row in rows]
    term_ids = [row["term_id"] for row in rows]

    assert len(normalized) == len(set(normalized))
    assert len(term_ids) == len(set(term_ids))


def test_expanded_terms_include_source_notes() -> None:
    rows = builder.build_rows(Path("terms"), min_length=4)

    assert all("source=" in row["notes"] for row in rows)
    assert all(row["term_id"].startswith("gpx_") for row in rows)
