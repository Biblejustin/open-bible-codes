from pathlib import Path

from scripts import validate_study_mapping_schemas as mappings


def write_all_headers(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for schema in mappings.SCHEMAS:
        path = root / schema.filename
        path.write_text(",".join(schema.required_columns) + "\n", encoding="utf-8")


def test_header_only_mapping_templates_validate() -> None:
    failures = mappings.validate_mapping_dir(Path("data/study/mappings"))

    assert failures == []


def test_missing_required_column_fails(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "thematic_chapters.csv"
    path.write_text(
        "mapping_id,term_id,concept,language,book,chapter_start,notes,locked_by,locked_at\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("missing required columns: chapter_end" in failure for failure in failures)


def test_populated_mapping_requires_locked_fields(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "author_book_mapping.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[1].required_columns)
        + "\n"
        + "isaiah_author,isaiah_h,Isaiah,hebrew,Isa,Isa 1:1,Isa 66:24,,notes,reviewer,2026-05-12\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("missing value for tradition" in failure for failure in failures)


def test_duplicate_mapping_ids_fail(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "protagonist_narrative_mapping.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[2].required_columns)
        + "\n"
        + "moses_narrative,moses_h,Moses,hebrew,Exod,Exod 1:1,Deut 34:12,notes,reviewer,2026-05-12\n"
        + "moses_narrative,moses_h,Moses,hebrew,Deut,Deut 1:1,Deut 34:12,notes,reviewer,2026-05-12\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("duplicate mapping_id: moses_narrative" in failure for failure in failures)


def test_thematic_chapter_range_must_be_ordered(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "thematic_chapters.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[0].required_columns)
        + "\n"
        + "isaiah_53_servant,servant_h,Servant,hebrew,Isa,54,53,notes,reviewer,2026-05-12\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("chapter_start must be <= chapter_end" in failure for failure in failures)
