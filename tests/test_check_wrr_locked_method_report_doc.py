import csv
from pathlib import Path

from scripts import check_wrr_locked_method_report_doc as check


def test_current_wrr_locked_method_report_doc_passes() -> None:
    assert check.validate_locked_method_report_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_locked_method_report_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if "Status: locked local WRR method report" not in phrase
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_locked_method_report_doc(doc)

    assert any("locked local WRR method report" in failure for failure in failures)


def test_forbidden_phrase_outside_list_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    text = "\n".join(check.REQUIRED_PHRASES)
    doc.write_text(text + "\nThis proves WRR now.\n", encoding="utf-8")

    failures = check.validate_locked_method_report_doc(doc)

    assert any("forbidden phrase outside forbidden-language list" in failure for failure in failures)


def test_validate_locked_method_report_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_locked_method_report_doc(
        doc,
        report=_report_csv(tmp_path),
        manifest=None,
    )

    assert failures == []


def test_validate_locked_method_report_rejects_value_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_locked_method_report_doc(
        doc,
        report=_report_csv(tmp_path, bad_item="defined_c_values"),
        manifest=None,
    )

    assert any("defined_c_values value drifted" in failure for failure in failures)


def test_validate_locked_method_report_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        """
{
  "inputs": {
    "corrected_distance_aggregate": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_aggregate.csv",
    "corrected_distance_summary": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv",
    "defined_pair_summary": "reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv",
    "lock_options": "reports/wrr_1994/wrr_lock_options.csv",
    "manual_worksheet": "reports/wrr_1994/wrr_manual_decision_record_worksheet.csv",
    "method_status": "reports/wrr_1994/wrr_method_status.csv",
    "permutation_summary": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_summary.csv",
    "primary_result_table": "reports/wrr_1994/wrr_primary_result_table.csv",
    "readiness": "reports/wrr_1994/wrr_claim_readiness.csv"
  },
  "manual_decision_rows": 37,
  "method_status_rows": 6,
  "outputs": {
    "manifest_out": "reports/wrr_1994/wrr_locked_method_report.manifest.json",
    "markdown_out": "docs/WRR_LOCKED_METHOD_REPORT.md",
    "out": "reports/wrr_1994/wrr_locked_method_report.csv"
  },
  "report_rows": 16,
  "tool": "build_wrr_locked_method_report"
}
""".lstrip(),
        encoding="utf-8",
    )

    failures = check.validate_locked_method_report_doc(
        doc,
        report=_report_csv(tmp_path),
        manifest=manifest,
    )

    assert any("report_rows drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR locked-method report failure" in capsys.readouterr().err


def _report_csv(tmp_path: Path, *, bad_item: str | None = None) -> Path:
    path = tmp_path / "report.csv"
    fieldnames = check.FIELDNAMES
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item, (section, value, status) in check.EXPECTED_ROWS.items():
            writer.writerow(
                {
                    "section": section,
                    "item": item,
                    "value": "drifted" if item == bad_item else value,
                    "status": status,
                    "evidence": "evidence",
                    "source": "source.csv",
                }
            )
        for (section, item), (value, status) in check.EXPECTED_DUPLICATE_ITEMS.items():
            writer.writerow(
                {
                    "section": section,
                    "item": item,
                    "value": "drifted" if item == bad_item else value,
                    "status": status,
                    "evidence": "evidence",
                    "source": "source.csv",
                }
            )
    return path
