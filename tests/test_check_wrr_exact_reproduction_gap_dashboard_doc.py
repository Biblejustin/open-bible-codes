import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
from pathlib import Path

from scripts import check_wrr_exact_reproduction_gap_dashboard_doc as check


def test_current_wrr_exact_gap_dashboard_doc_passes() -> None:
    assert check.validate_gap_dashboard_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_gap_dashboard_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if "Status: exact published WRR reproduction" not in phrase
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_gap_dashboard_doc(doc)

    assert any("Status: exact published WRR reproduction" in failure for failure in failures)


def test_forbidden_phrase_outside_list_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    text = "\n".join(check.REQUIRED_PHRASES)
    doc.write_text(text + "\nsource correction selected now.\n", encoding="utf-8")

    failures = check.validate_gap_dashboard_doc(doc)

    assert any("forbidden phrase outside boundary list" in failure for failure in failures)


def test_validate_dashboard_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_gap_dashboard_doc(
        doc,
        dashboard=_dashboard_csv(tmp_path),
        manifest=None,
    )

    assert failures == []


def test_validate_dashboard_rejects_item_value_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_gap_dashboard_doc(
        doc,
        dashboard=_dashboard_csv(tmp_path, bad_item="remaining_gap"),
        manifest=None,
    )

    assert any("remaining_gap value drifted" in failure for failure in failures)


def test_validate_dashboard_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "tool": "build_wrr_exact_reproduction_gap_dashboard",
                "dashboard_rows": 17,
                "gap_reason_rows": 3,
                "review_lane_rows": 4,
                "inputs": {
                    "action_summary": "reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv",
                    "defined_pair_summary": "reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv",
                    "gap_reasons": "reports/wrr_1994/wrr_defined_gap_reasons.csv",
                    "locked_report": "reports/wrr_1994/wrr_locked_method_report.csv",
                    "manual_decision_records": "data/study/mappings/wrr_manual_decision_records.csv",
                    "manual_register_summary": "reports/wrr_1994/wrr_manual_decision_register_summary.csv",
                    "remaining_checklist": "reports/wrr_1994/wrr_remaining_lane_review_checklist.csv",
                    "row_checklist": "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv",
                    "source_policy_checklist": "reports/wrr_1994/wrr_source_policy_review_checklist.csv",
                    "variant_upper_bound": "reports/wrr_1994/wrr_variant_gap_upper_bound.csv",
                },
                "outputs": {
                    "manifest_out": "reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.manifest.json",
                    "markdown_out": "docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md",
                    "out": "reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_gap_dashboard_doc(
        doc,
        dashboard=_dashboard_csv(tmp_path),
        manifest=manifest,
    )

    assert any("dashboard_rows drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR exact gap dashboard failure" in capsys.readouterr().err


def _dashboard_csv(tmp_path: Path, *, bad_item: str | None = None) -> Path:
    path = tmp_path / "dashboard.csv"
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
    return path
