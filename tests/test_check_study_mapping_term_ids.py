import csv
from pathlib import Path

from scripts import check_study_mapping_term_ids as check


def test_current_study_mapping_term_ids_pass() -> None:
    assert check.validate_mapping_term_ids() == []


def test_unknown_mapping_term_id_fails(tmp_path: Path) -> None:
    mappings = tmp_path / "mappings"
    terms = tmp_path / "terms"
    mappings.mkdir()
    terms.mkdir()
    write_csv(
        terms / "terms.csv",
        ["term_id", "concept"],
        [{"term_id": "known_h", "concept": "Known"}],
    )
    for filename, column in check.MAPPING_TERM_COLUMNS:
        write_csv(
            mappings / filename,
            [column],
            [{column: "missing_h" if filename == "thematic_chapters.csv" else "known_h"}],
        )

    failures = check.validate_mapping_term_ids(mappings, terms)

    assert failures == [
        f"{mappings / 'thematic_chapters.csv'}:2 unknown term_id: missing_h"
    ]


def test_missing_term_id_column_fails(tmp_path: Path) -> None:
    mappings = tmp_path / "mappings"
    terms = tmp_path / "terms"
    mappings.mkdir()
    terms.mkdir()
    write_csv(terms / "terms.csv", ["term_id"], [{"term_id": "known_h"}])
    write_csv(mappings / "thematic_chapters.csv", ["wrong"], [{"wrong": "known_h"}])
    for filename, column in check.MAPPING_TERM_COLUMNS[1:]:
        write_csv(mappings / filename, [column], [{column: "known_h"}])

    failures = check.validate_mapping_term_ids(mappings, terms)

    assert failures == [
        f"{mappings / 'thematic_chapters.csv'} missing required term-id column: term_id"
    ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
