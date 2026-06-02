import csv
from pathlib import Path

from scripts import check_wrr_method_status_doc as check


def test_current_wrr_method_status_doc_passes() -> None:
    assert check.validate_method_status_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_method_status_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_exact_published_reproduction_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_method_status_doc(doc)

    assert any("not an exact published WRR reproduction" in failure for failure in failures)


def test_validate_method_status_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_method_status_doc(
        doc,
        status=_status_csv(tmp_path),
        manifest=None,
    )

    assert failures == []


def test_validate_method_status_rejects_status_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_method_status_doc(
        doc,
        status=_status_csv(tmp_path, bad_area="Pair universe"),
        manifest=None,
    )

    assert any("Pair universe status drifted" in failure for failure in failures)


def test_validate_method_status_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        """
{
  "inputs": {
    "corrected_distance_aggregate": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_aggregate.csv",
    "corrected_distance_variants": "reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv",
    "cross_pair_permutation_summary": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_1000_summary.csv",
    "cross_pair_recommended_permutation_summary": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_summary.csv",
    "defined_gap_reasons": "reports/wrr_1994/wrr_defined_gap_reasons.csv",
    "defined_pair_summary": "reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv",
    "dw_formula_sensitivity": "reports/wrr_1994/wrr_dw_formula_sensitivity.csv",
    "highcap_corrected_distance_summary": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv",
    "highcap_pair_readiness_summary": "reports/wrr_1994/highcap_1000/wrr2_perturbation_pair_readiness_summary.csv",
    "highcap_perturbation_summary": "reports/wrr_1994/highcap_1000/wrr2_perturbation_diagnostics_summary.csv",
    "pair_summary": "reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv",
    "primary_result_table": "reports/wrr_1994/wrr_primary_result_table.csv",
    "skip_summary": "reports/wrr_1994/wrr2_skip_caps_summary.csv",
    "source_policy_scenarios": "reports/wrr_1994/wrr_source_policy_scenarios.csv",
    "source_policy_term_impacts": "reports/wrr_1994/wrr_source_policy_term_impacts.csv",
    "table2_bridge_summary": "reports/wrr_1994/wrr_table2_source_bridge_summary.csv",
    "table2_ocr_summary": "reports/wrr_1994/wrr_primary_table2_ocr_probe_summary.csv",
    "table2_row_ocr_summary": "reports/wrr_1994/wrr_primary_table2_row_ocr_probe_summary.csv",
    "text_source": "reports/wrr_1994/koren_genesis_text_source.csv",
    "variant_gap_summary": "reports/wrr_1994/wrr_variant_gap_impact_summary.csv",
    "variant_residual_summary": "reports/wrr_1994/wrr_variant_residual_review_summary.csv",
    "zero_hit_variant_summary": "reports/wrr_1994/wrr_zero_hit_variant_probe_summary.csv"
  },
  "outputs": {
    "csv": "reports/wrr_1994/wrr_method_status.csv",
    "manifest": "reports/wrr_1994/wrr_method_status.manifest.json",
    "markdown": "docs/WRR_METHOD_STATUS.md"
  },
  "rows": 5,
  "tool": "build_wrr_method_status.py"
}
""".lstrip(),
        encoding="utf-8",
    )

    failures = check.validate_method_status_doc(
        doc,
        status=_status_csv(tmp_path),
        manifest=manifest,
    )

    assert any("rows drifted" in failure for failure in failures)


def test_validate_method_status_rejects_invalid_manifest_json(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{", encoding="utf-8")

    failures = check.validate_method_status_doc(
        doc,
        status=_status_csv(tmp_path),
        manifest=manifest,
    )

    assert any("is invalid JSON" in failure for failure in failures)


def test_validate_method_status_rejects_manifest_json_array(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("[]", encoding="utf-8")

    failures = check.validate_method_status_doc(
        doc,
        status=_status_csv(tmp_path),
        manifest=manifest,
    )

    assert any("JSON root must be an object" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR method-status doc failure" in capsys.readouterr().err


def _status_csv(tmp_path: Path, *, bad_area: str | None = None) -> Path:
    path = tmp_path / "status.csv"
    fieldnames = check.FIELDNAMES
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for area, status in check.EXPECTED_STATUS.items():
            writer.writerow(
                {
                    "decision_area": area,
                    "status": "drifted" if area == bad_area else status,
                    "current_read": "read",
                    "evidence": "evidence",
                    "next_action": "next",
                }
            )
    return path
