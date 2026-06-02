from pathlib import Path

from scripts import check_crd_relevance_dictionary as check
from scripts.classify_centered_relevance import sha256_file


def test_main_accepts_reviewed_dictionary_with_expected_hash(
    tmp_path: Path, capsys
) -> None:
    terms = write_terms(tmp_path)
    dictionary = write_dictionary(tmp_path)

    code = check.main(
        [
            "--dictionary",
            str(dictionary),
            "--term-file",
            str(terms),
            "--expected-sha256",
            sha256_file(dictionary),
            "--require-reviewed",
        ]
    )

    stdout = capsys.readouterr().out
    assert code == 0
    assert "entries=1" in stdout
    assert "missing_entries=0" in stdout


def test_main_reports_hash_mismatch(tmp_path: Path, capsys) -> None:
    terms = write_terms(tmp_path)
    dictionary = write_dictionary(tmp_path)

    code = check.main(
        [
            "--dictionary",
            str(dictionary),
            "--term-file",
            str(terms),
            "--expected-sha256",
            "bad",
        ]
    )

    stderr = capsys.readouterr().err
    assert code == 1
    assert "dictionary sha256 mismatch" in stderr


def test_main_reports_invalid_toml(tmp_path: Path, capsys) -> None:
    terms = write_terms(tmp_path)
    dictionary = tmp_path / "dictionary.toml"
    dictionary.write_text("[[entries]\n", encoding="utf-8")

    code = check.main(
        [
            "--dictionary",
            str(dictionary),
            "--term-file",
            str(terms),
        ]
    )

    stderr = capsys.readouterr().err
    assert code == 1
    assert "dictionary invalid TOML:" in stderr


def write_terms(root: Path) -> Path:
    terms = root / "terms.csv"
    terms.write_text(
        "term_id,concept,category,language,term,notes\n"
        "term,Term,category,english,term,test\n",
        encoding="utf-8",
    )
    return terms


def write_dictionary(root: Path) -> Path:
    dictionary = root / "dictionary.toml"
    dictionary.write_text(
        "\n".join(
            [
                "[metadata]",
                'schema_version = "1"',
                'locked_by = "reviewer"',
                'locked_at = "2026-05-09"',
                'sha256 = "locked-later"',
                'drafted_with = "human"',
                "",
                "[[entries]]",
                'term_id = "term"',
                'surface_keywords = ["term"]',
                "concept_codes = []",
                "verse_refs = []",
                "",
                "[entries.provenance]",
                'author = "reviewer"',
                'lock_date = "2026-05-09"',
                'reviewer = "Justin"',
                'notes = "reviewed"',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return dictionary
