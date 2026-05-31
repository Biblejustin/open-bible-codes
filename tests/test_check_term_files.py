import csv
from pathlib import Path

from scripts import check_term_files as check


def test_current_term_files_pass() -> None:
    assert check.validate_term_files() == []


def test_duplicate_term_id_fails(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [
            {"term_id": "same_h", "language": "hebrew", "term": "אור"},
            {"term_id": "same_h", "language": "hebrew", "term": "שלום"},
        ],
    )

    failures = check.validate_term_files(terms)

    assert f"{terms / 'demo.csv'}:3 duplicate term_id: same_h" in failures


def test_unsupported_language_fails(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_l", "language": "latin", "term": "lux"}],
    )

    failures = check.validate_term_files(terms)

    assert f"{terms / 'demo.csv'}:2 unsupported language: latin" in failures


def test_empty_normalization_needs_explicit_note(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "digits_h", "language": "hebrew", "term": "666"}],
    )

    failures = check.validate_term_files(terms)

    assert f"{terms / 'demo.csv'}:2 normalizes to empty letters: digits_h" in failures


def make_terms_dir(tmp_path: Path) -> Path:
    terms = tmp_path / "terms"
    terms.mkdir()
    write_constants(terms / "meaningful_constants.csv")
    (terms / "gematria_schemes.toml").write_text(
        """
[[schemes]]
scheme_id = "hebrew_standard"
language = "hebrew"
implementation = "els.gematria.hebrew_standard"
status = "implemented"

[[schemes]]
scheme_id = "greek_standard"
language = "greek"
implementation = "els.gematria.greek_standard"
status = "implemented"
""".lstrip(),
        encoding="utf-8",
    )
    return terms


def write_term_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["term_id", "concept", "category", "language", "term", "notes"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            full = {
                "term_id": row["term_id"],
                "concept": row.get("concept", "Demo"),
                "category": row.get("category", "demo"),
                "language": row["language"],
                "term": row["term"],
                "notes": row.get("notes", ""),
            }
            writer.writerow(full)


def write_constants(path: Path) -> None:
    fieldnames = ["constant_id", "value", "label", "category", "notes"]
    values = [7, 12, 22, 26, 40, 42, 50, 70, 144, 666]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for value in values:
            writer.writerow(
                {
                    "constant_id": f"c_{value}",
                    "value": str(value),
                    "label": str(value),
                    "category": "demo",
                    "notes": "",
                }
            )
