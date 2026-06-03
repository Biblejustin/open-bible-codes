import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
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
        manifest=None,
    )

    assert failures == []


def test_validate_dw_formula_sensitivity_rejects_summary_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_dw_formula_sensitivity_doc(
        doc,
        sensitivity=_sensitivity_csv(tmp_path, bad_scope="all_lanes_cap1000"),
        changed_pairs=_changed_pairs_csv(tmp_path),
        manifest=None,
    )

    assert any("all_lanes_cap1000 changed_pairs" in failure for failure in failures)


def test_validate_dw_formula_sensitivity_rejects_changed_pairs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_dw_formula_sensitivity_doc(
        doc,
        sensitivity=_sensitivity_csv(tmp_path),
        changed_pairs=_changed_pairs_csv(tmp_path, add_row=True),
        manifest=None,
    )

    assert any("expected 0 changed pairs" in failure for failure in failures)


def test_validate_dw_formula_sensitivity_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "tool": "analyze_wrr_dw_formula_sensitivity.py",
                "changed_pairs": 1,
                "summary_rows": 3,
                "inputs": {
                    "direct_printed": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv",
                    "direct_printed_summary": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv",
                    "direct_program": "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged.csv",
                    "direct_program_summary": "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged_summary.csv",
                    "skip_summary": "reports/wrr_1994/wrr2_skip_caps_summary.csv",
                    "variants": "reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv",
                },
                "outputs": {
                    "changed_out": "reports/wrr_1994/wrr_dw_formula_changed_pairs.csv",
                    "manifest_out": "reports/wrr_1994/wrr_dw_formula_sensitivity.manifest.json",
                    "markdown_out": "docs/WRR_DW_FORMULA_SENSITIVITY.md",
                    "out": "reports/wrr_1994/wrr_dw_formula_sensitivity.csv",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_dw_formula_sensitivity_doc(
        doc,
        sensitivity=_sensitivity_csv(tmp_path),
        changed_pairs=_changed_pairs_csv(tmp_path),
        manifest=manifest,
    )

    assert any("changed_pairs drifted" in failure for failure in failures)


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
    fieldnames = check.SUMMARY_FIELDNAMES
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
