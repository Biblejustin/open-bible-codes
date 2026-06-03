import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
from pathlib import Path

from scripts import check_wrr_cross_pair_grid_doc as check


def test_current_wrr_cross_pair_grid_doc_passes() -> None:
    assert check.validate_cross_pair_grid_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_cross_pair_grid_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_permutation_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CROSS_PAIR_GRID.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if phrase != "| rho P1 | 0.019722 |"
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_cross_pair_grid_doc(doc)

    assert any("0.019722" in failure for failure in failures)


def test_validate_cross_pair_grid_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_cross_pair_grid_doc(
        doc,
        **_csv_paths(tmp_path),
    )

    assert failures == []


def test_validate_cross_pair_grid_rejects_grid_summary_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)
    paths = _csv_paths(tmp_path, bad_grid_key="pairs")

    failures = check.validate_cross_pair_grid_doc(doc, **paths)

    assert any("grid summary pairs drifted" in failure for failure in failures)


def test_validate_cross_pair_grid_rejects_permutation_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)
    paths = _csv_paths(tmp_path, bad_cap1000_999999_key="rho_p2")

    failures = check.validate_cross_pair_grid_doc(doc, **paths)

    assert any("cap-1000 999999 permutation rho_p2 drifted" in failure for failure in failures)


def test_validate_cross_pair_grid_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)
    paths = _csv_paths(tmp_path)
    manifest = tmp_path / "cap1000_999999.manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "tool": "analyze_wrr_cross_pair_permutations.py",
                "input": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                "parameters": {
                    "permutations": 999999,
                    "seed": 1994,
                    "p1_threshold": 0.2,
                    "candidate_lane": [],
                    "pair_review_status": [],
                    "exclude_pair_review_status": [],
                    "sample_output_limit": 0,
                },
                "summary": {
                    **check.EXPECTED_CAP1000_999999,
                    "rho_p2": "drifted",
                },
                "outputs": {
                    "csv": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_observed_only.csv",
                    "summary": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_summary.csv",
                    "markdown": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999.md",
                    "manifest": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999.manifest.json",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    paths["cap1000_999999_manifest"] = manifest

    failures = check.validate_cross_pair_grid_doc(doc, **paths)

    assert any("cap-1000 999999 manifest summary.rho_p2" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR cross-pair grid doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "WRR_CROSS_PAIR_GRID.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _csv_paths(
    tmp_path: Path,
    *,
    bad_grid_key: str | None = None,
    bad_cap1000_999999_key: str | None = None,
) -> dict[str, Path]:
    return {
        "grid_summary": _one_row_csv(
            tmp_path / "grid_summary.csv",
            check.EXPECTED_GRID_SUMMARY,
            bad_key=bad_grid_key,
        ),
        "cap250_summary": _one_row_csv(
            tmp_path / "cap250_summary.csv",
            check.EXPECTED_CAP250_SUMMARY,
        ),
        "cap250_aggregate": _one_row_csv(
            tmp_path / "cap250_aggregate.csv",
            check.EXPECTED_CAP250_AGGREGATE,
        ),
        "cap250_permutation": _one_row_csv(
            tmp_path / "cap250_permutation.csv",
            check.EXPECTED_CAP250_PERMUTATION,
        ),
        "cap250_no_wnp_999999": _one_row_csv(
            tmp_path / "cap250_no_wnp_999999.csv",
            check.EXPECTED_CAP250_NO_WNP_999999,
        ),
        "cap1000_summary": _one_row_csv(
            tmp_path / "cap1000_summary.csv",
            check.EXPECTED_CAP1000_SUMMARY,
        ),
        "cap1000_aggregate": _one_row_csv(
            tmp_path / "cap1000_aggregate.csv",
            check.EXPECTED_CAP1000_AGGREGATE,
        ),
        "cap1000_permutation": _one_row_csv(
            tmp_path / "cap1000_permutation.csv",
            check.EXPECTED_CAP1000_PERMUTATION,
        ),
        "cap1000_999999": _one_row_csv(
            tmp_path / "cap1000_999999.csv",
            check.EXPECTED_CAP1000_999999,
            bad_key=bad_cap1000_999999_key,
        ),
        "grid_manifest": None,
        "cap250_summary_manifest": None,
        "cap250_aggregate_manifest": None,
        "cap250_permutation_manifest": None,
        "cap250_no_wnp_999999_manifest": None,
        "cap1000_summary_manifest": None,
        "cap1000_aggregate_manifest": None,
        "cap1000_permutation_manifest": None,
        "cap1000_999999_manifest": None,
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
