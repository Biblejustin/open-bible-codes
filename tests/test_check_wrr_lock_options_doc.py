import csv
import json
from pathlib import Path

from scripts import check_wrr_lock_options_doc as check


def test_current_wrr_lock_options_doc_passes() -> None:
    assert check.validate_lock_options_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_lock_options_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_decision_aid_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_lock_options_doc(doc)

    assert any("decision aid" in failure for failure in failures)


def test_missing_no_input_posture_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase != "No source-review flag or visual-review note excludes a pair automatically."
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_lock_options_doc(doc)

    assert any("visual-review note excludes" in failure for failure in failures)


def test_validate_lock_options_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_lock_options_doc(
        doc,
        options=_options_csv(tmp_path),
        manifest=None,
    )

    assert failures == []


def test_validate_lock_options_rejects_status_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_lock_options_doc(
        doc,
        options=_options_csv(tmp_path, bad_option="printed WRR formula"),
        manifest=None,
    )

    assert any("printed WRR formula status drifted" in failure for failure in failures)


def test_validate_lock_options_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "tool": "build_wrr_lock_options",
                "inputs": {
                    "direct_all_lanes_1000": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv",
                    "direct_all_lanes_1000_program": "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged.csv",
                    "direct_all_lanes_1000_program_summary": "reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged_summary.csv",
                    "direct_all_lanes_1000_summary": "reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv",
                    "direct_all_lanes_250_summary": "reports/wrr_1994/direct_all/wrr2_corrected_distance_all_lanes_250_summary.csv",
                    "pair_summary": "reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv",
                    "recommended_permutation": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_summary.csv",
                    "skip_summary": "reports/wrr_1994/wrr2_skip_caps_summary.csv",
                    "source_policy_scenarios": "reports/wrr_1994/wrr_source_policy_scenarios.csv",
                    "source_policy_term_impacts": "reports/wrr_1994/wrr_source_policy_term_impacts.csv",
                    "source_review_summary": "reports/wrr_1994/wrr_source_review_queue_summary.csv",
                    "variants": "reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv",
                },
                "outputs": {
                    "markdown_out": "docs/WRR_LOCK_OPTIONS.md",
                    "out": "reports/wrr_1994/wrr_lock_options.csv",
                },
                "rows": 8,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_lock_options_doc(
        doc,
        options=_options_csv(tmp_path),
        manifest=manifest,
    )

    assert any("rows drifted" in failure for failure in failures)


def test_validate_lock_options_rejects_invalid_manifest_json(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{", encoding="utf-8")

    failures = check.validate_lock_options_doc(
        doc,
        options=_options_csv(tmp_path),
        manifest=manifest,
    )

    assert any("is invalid JSON" in failure for failure in failures)


def test_validate_lock_options_rejects_manifest_json_array(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("[]", encoding="utf-8")

    failures = check.validate_lock_options_doc(
        doc,
        options=_options_csv(tmp_path),
        manifest=manifest,
    )

    assert any("JSON root must be an object" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR lock-options doc failure" in capsys.readouterr().err


def _options_csv(tmp_path: Path, *, bad_option: str | None = None) -> Path:
    path = tmp_path / "options.csv"
    fieldnames = check.FIELDNAMES
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for option, (area, status, claim_boundary) in check.EXPECTED_OPTIONS.items():
            writer.writerow(
                {
                    "area": area,
                    "option": option,
                    "status": "drifted" if option == bad_option else status,
                    "evidence": "evidence",
                    "recommendation": "recommendation",
                    "claim_boundary": claim_boundary,
                }
            )
    return path
