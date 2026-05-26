import csv
from pathlib import Path

from scripts import check_wrr_direct_all_lanes_doc as check


def test_current_wrr_direct_all_lanes_doc_passes() -> None:
    assert check.validate_direct_all_lanes_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_direct_all_lanes_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_cap1000_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:-8]) + "\n", encoding="utf-8")

    failures = check.validate_direct_all_lanes_doc(doc)

    assert any("cap 1000" in failure for failure in failures)


def test_validate_direct_all_lanes_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_direct_all_lanes_doc(doc, **_csv_paths(tmp_path))

    assert failures == []


def test_validate_direct_all_lanes_rejects_summary_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)
    paths = _csv_paths(tmp_path, bad_cap1000_key="defined_corrected_distances")

    failures = check.validate_direct_all_lanes_doc(doc, **paths)

    assert any("cap-1000 summary defined_corrected_distances" in failure for failure in failures)


def test_validate_direct_all_lanes_rejects_dw_sensitivity_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)
    paths = _csv_paths(tmp_path, bad_dw_key="changed_pairs")

    failures = check.validate_direct_all_lanes_doc(doc, **paths)

    assert any("all_lanes_cap1000 changed_pairs" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR direct all-lane doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _csv_paths(
    tmp_path: Path,
    *,
    bad_cap1000_key: str | None = None,
    bad_dw_key: str | None = None,
) -> dict[str, Path]:
    return {
        "cap250_summary": _one_row_csv(
            tmp_path / "cap250_summary.csv",
            check.EXPECTED_CAP250_SUMMARY,
        ),
        "cap1000_summary": _one_row_csv(
            tmp_path / "cap1000_summary.csv",
            check.EXPECTED_CAP1000_SUMMARY,
            bad_key=bad_cap1000_key,
        ),
        "cap1000_aggregate": _one_row_csv(
            tmp_path / "cap1000_aggregate.csv",
            check.EXPECTED_CAP1000_AGGREGATE,
        ),
        "program_summary": _one_row_csv(
            tmp_path / "program_summary.csv",
            check.EXPECTED_PROGRAM_SUMMARY,
        ),
        "dw_sensitivity": _dw_sensitivity_csv(tmp_path, bad_key=bad_dw_key),
    }


def _one_row_csv(
    path: Path,
    expected: dict[str, str],
    *,
    bad_key: str | None = None,
) -> Path:
    row = dict(expected)
    if bad_key:
        row[bad_key] = "drifted"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(expected))
        writer.writeheader()
        writer.writerow(row)
    return path


def _dw_sensitivity_csv(tmp_path: Path, *, bad_key: str | None = None) -> Path:
    path = tmp_path / "dw_sensitivity.csv"
    row = {
        **check.EXPECTED_DW_SENSITIVITY_ALL_LANES,
        "diagnostic_read": "row-level printed/program comparison; printed D(w) main",
    }
    if bad_key:
        row[bad_key] = "drifted"
    fieldnames = [
        "scope",
        "row_count",
        "printed_formula",
        "program_formula",
        "printed_defined_corrected_distances",
        "program_defined_corrected_distances",
        "printed_ordinary_not_valid_pairs",
        "program_ordinary_not_valid_pairs",
        "printed_under_minimum_valid_pairs",
        "program_under_minimum_valid_pairs",
        "changed_pairs",
        "diagnostic_read",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)
    return path
