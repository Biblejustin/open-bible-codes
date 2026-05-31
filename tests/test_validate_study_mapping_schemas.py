from pathlib import Path

from scripts import validate_study_mapping_schemas as mappings


def schema_by_name(filename: str) -> mappings.MappingSchema:
    return next(schema for schema in mappings.SCHEMAS if schema.filename == filename)


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


def test_unexpected_column_fails(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "thematic_chapters.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[0].required_columns)
        + ",extra_notes\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("unexpected columns: extra_notes" in failure for failure in failures)


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


def test_locked_at_must_be_iso_date(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "author_book_mapping.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[1].required_columns)
        + "\n"
        + "isaiah_author,isaiah_h,Isaiah,hebrew,Isa,Isa 1:1,Isa 66:24,"
        + "traditional,notes,reviewer,05/12/2026\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("locked_at must be an ISO date" in failure for failure in failures)


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


def test_scope_refs_must_match_declared_book(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "protagonist_narrative_mapping.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[2].required_columns)
        + "\n"
        + "moses_narrative,moses_h,Moses,hebrew,Exod,Exod 1:1,Deut 34:12,"
        + "notes,reviewer,2026-05-12\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("scope_end_ref book must match book: Exod" in failure for failure in failures)


def test_scope_refs_must_be_ordered(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    path = tmp_path / "author_book_mapping.csv"
    path.write_text(
        ",".join(mappings.SCHEMAS[1].required_columns)
        + "\n"
        + "isaiah_author,isaiah_h,Isaiah,hebrew,Isa,Isa 66:24,Isa 1:1,"
        + "traditional,notes,reviewer,2026-05-12\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("scope_start_ref must be <= scope_end_ref" in failure for failure in failures)


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


def test_root_policy_requires_analyzer_provenance(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    schema = schema_by_name("hebrew_root_policy.csv")
    path = tmp_path / "hebrew_root_policy.csv"
    path.write_text(
        ",".join(schema.required_columns)
        + "\n"
        + "root_love,love_h,Love,hebrew,אהבה,אהבה,אהב,standard,,source,notes,reviewer,2026-05-12\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("missing value for analyzer" in failure for failure in failures)


def test_wrr_manual_decision_records_require_evidence_and_lock(tmp_path: Path) -> None:
    write_all_headers(tmp_path)
    schema = schema_by_name("wrr_manual_decision_records.csv")
    path = tmp_path / schema.filename
    path.write_text(
        ",".join(schema.required_columns)
        + "\n"
        + "wrr_decision_001,1,source_policy_pair_rule,pending_source_policy_pair_rule_lock,"
        + "Chelm source-policy/pair-rule target,docs/WRR_MANUAL_DECISION_REGISTER.md,"
        + "accepted_keep,no_source_change,,,reviewer,2026-05-22,notes\n",
        encoding="utf-8",
    )

    failures = mappings.validate_mapping_dir(tmp_path)

    assert any("missing value for evidence_citation" in failure for failure in failures)
    assert any("missing value for evidence_summary" in failure for failure in failures)
