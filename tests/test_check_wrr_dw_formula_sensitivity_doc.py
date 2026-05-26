import csv
from pathlib import Path

from scripts import check_wrr_dw_formula_sensitivity_doc as check


def test_current_wrr_dw_formula_sensitivity_doc_passes() -> None:
    assert check.validate_dw_formula_sensitivity_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_dw_formula_sensitivity_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_all_lanes_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_DW_FORMULA_SENSITIVITY.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:-6]) + "\n", encoding="utf-8")

    failures = check.validate_dw_formula_sensitivity_doc(doc)

    assert any("all_lanes_cap1000" in failure for failure in failures)


def test_validate_dw_formula_sensitivity_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_dw_formula_sensitivity_doc(
        doc,
        sensitivity=_sensitivity_csv(tmp_path),
        changed_pairs=_changed_pairs_csv(tmp_path),
    )

    assert failures == []


def test_validate_dw_formula_sensitivity_rejects_summary_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_dw_formula_sensitivity_doc(
        doc,
        sensitivity=_sensitivity_csv(tmp_path, bad_scope="all_lanes_cap1000"),
        changed_pairs=_changed_pairs_csv(tmp_path),
    )

    assert any("all_lanes_cap1000 changed_pairs" in failure for failure in failures)


def test_validate_dw_formula_sensitivity_rejects_changed_pairs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_dw_formula_sensitivity_doc(
        doc,
        sensitivity=_sensitivity_csv(tmp_path),
        changed_pairs=_changed_pairs_csv(tmp_path, add_row=True),
    )

    assert any("expected 0 changed pairs" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR D(w) formula sensitivity doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "WRR_DW_FORMULA_SENSITIVITY.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _sensitivity_csv(tmp_path: Path, *, bad_scope: str | None = None) -> Path:
    path = tmp_path / "sensitivity.csv"
    fieldnames = [
        "scope",
        "row_count",
        "printed_formula",
        "program_formula",
        "printed_defined_corrected_distances",
        "program_defined_corrected_distances",
        "fixed_250_defined_corrected_distances",
        "printed_ordinary_not_valid_pairs",
        "program_ordinary_not_valid_pairs",
        "printed_under_minimum_valid_pairs",
        "program_under_minimum_valid_pairs",
        "changed_pairs",
        "program_cap_lt_printed",
        "program_cap_eq_printed",
        "program_cap_gt_printed",
        "target_unreached_rows",
        "program_target_unreached_rows",
        "diagnostic_read",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for scope, expected in check.EXPECTED_SCOPE_ROWS.items():
            row = {field: "" for field in fieldnames}
            row.update(expected)
            row["scope"] = scope
            row["diagnostic_read"] = "printed D(w) main"
            if scope == bad_scope:
                row["changed_pairs"] = "drifted"
            writer.writerow(row)
    return path


def _changed_pairs_csv(tmp_path: Path, *, add_row: bool = False) -> Path:
    path = tmp_path / "changed_pairs.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.CHANGED_PAIR_FIELDNAMES)
        writer.writeheader()
        if add_row:
            writer.writerow({field: "x" for field in check.CHANGED_PAIR_FIELDNAMES})
    return path
