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


def test_missing_required_constant_value_fails(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    write_constants(terms / "meaningful_constants.csv", values=[7, 12, 22])

    failures = check.validate_term_files(terms)

    assert any(
        failure.startswith(f"{terms / 'meaningful_constants.csv'} missing required values:")
        for failure in failures
    )


def test_duplicate_constant_values_fail(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    write_constants(
        terms / "meaningful_constants.csv",
        values=[7, 7, 12, 22, 26, 40, 42, 50, 70, 144, 666],
    )

    failures = check.validate_term_files(terms)

    assert f"{terms / 'meaningful_constants.csv'} has duplicate values" in failures


def test_missing_required_gematria_scheme_fails(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    write_gematria_schemes(
        terms / "gematria_schemes.toml",
        [
            {
                "scheme_id": "hebrew_standard",
                "language": "hebrew",
                "implementation": "els.gematria.hebrew_standard",
                "status": "implemented",
            }
        ],
    )

    failures = check.validate_term_files(terms)

    assert (
        f"{terms / 'gematria_schemes.toml'} missing required schemes: greek_standard"
        in failures
    )


def test_bad_gematria_scheme_metadata_fails(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    write_gematria_schemes(
        terms / "gematria_schemes.toml",
        [
            {
                "scheme_id": "hebrew_standard",
                "language": "latin",
                "implementation": "els.bad.hebrew_standard",
                "status": "planned",
            },
            {
                "scheme_id": "greek_standard",
                "language": "greek",
                "implementation": "els.gematria.greek_standard",
                "status": "implemented",
            },
        ],
    )

    failures = check.validate_term_files(terms)

    scheme_path = terms / "gematria_schemes.toml"
    assert f"{scheme_path}:scheme 1 unsupported language: latin" in failures
    assert f"{scheme_path}:scheme 1 bad implementation: hebrew_standard" in failures
    assert f"{scheme_path}:scheme 1 status not implemented: hebrew_standard" in failures


def test_invalid_gematria_scheme_toml_reports_failure(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    scheme_path = terms / "gematria_schemes.toml"
    scheme_path.write_text("[[schemes]\n", encoding="utf-8")

    failures = check.validate_term_files(terms)

    assert any(
        failure.startswith(f"{scheme_path} is invalid TOML:")
        for failure in failures
    )


def test_gematria_schemes_top_level_must_be_list(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    scheme_path = terms / "gematria_schemes.toml"
    scheme_path.write_text('schemes = "bad"\n', encoding="utf-8")

    failures = check.validate_term_files(terms)

    assert f"{scheme_path} schemes must be a list" in failures


def test_gematria_scheme_entries_must_be_tables(tmp_path: Path) -> None:
    terms = make_terms_dir(tmp_path)
    write_term_csv(
        terms / "demo.csv",
        [{"term_id": "demo_h", "language": "hebrew", "term": "אור"}],
    )
    scheme_path = terms / "gematria_schemes.toml"
    scheme_path.write_text('schemes = ["bad"]\n', encoding="utf-8")

    failures = check.validate_term_files(terms)

    assert f"{scheme_path}:scheme 1 must be a table" in failures


def make_terms_dir(tmp_path: Path) -> Path:
    terms = tmp_path / "terms"
    terms.mkdir()
    write_constants(terms / "meaningful_constants.csv")
    write_gematria_schemes(
        terms / "gematria_schemes.toml",
        [
            {
                "scheme_id": "hebrew_standard",
                "language": "hebrew",
                "implementation": "els.gematria.hebrew_standard",
                "status": "implemented",
            },
            {
                "scheme_id": "greek_standard",
                "language": "greek",
                "implementation": "els.gematria.greek_standard",
                "status": "implemented",
            },
        ],
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


def write_constants(path: Path, *, values: list[int] | None = None) -> None:
    fieldnames = ["constant_id", "value", "label", "category", "notes"]
    values = (
        values
        if values is not None
        else [7, 12, 22, 26, 40, 42, 50, 70, 144, 666]
    )
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


def write_gematria_schemes(path: Path, schemes: list[dict[str, str]]) -> None:
    blocks = []
    for scheme in schemes:
        blocks.append(
            "\n".join(
                [
                    "[[schemes]]",
                    f'scheme_id = "{scheme["scheme_id"]}"',
                    f'language = "{scheme["language"]}"',
                    f'implementation = "{scheme["implementation"]}"',
                    f'status = "{scheme["status"]}"',
                ]
            )
        )
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
