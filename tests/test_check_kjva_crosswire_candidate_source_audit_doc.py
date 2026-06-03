import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
from pathlib import Path

from scripts import check_kjva_crosswire_candidate_source_audit_doc as check


def test_current_kjva_crosswire_source_audit_doc_passes() -> None:
    assert check.validate_kjva_crosswire_candidate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_crosswire_candidate_source_audit_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Possible independent KJVA metadata candidates: 1.",
        "Possible independent KJVA metadata candidates: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_crosswire_candidate_source_audit_doc(
        doc,
        rows=None,
        summary=None,
        anchors=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_rows_status_drift_fails(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    row = {field: "" for field in check.analyzer.ROW_FIELDNAMES}
    row.update(
        {
            "source_id": "crosswire_gitlab_kjva_osis",
            "repo_url": check.analyzer.PROJECT_WEB_URL,
            "project_fetch_status": "fetched",
            "tree_fetch_status": "fetched",
            "readme_fetch_status": "fetched",
            "kjva_conf_fetch_status": "fetched",
            "kjvdc_conf_fetch_status": "fetched",
            "default_branch": "master",
            "tree_path_count": "9",
            "tree_paths": "README.md;kjv.osis.xml;kjva.osis.xml;kjvdc.xml",
            "kjv_osis_path_present": "True",
            "kjva_osis_path_present": "False",
            "kjvdc_xml_path_present": "True",
            "kjvdc_conf_path_present": "True",
            "kjva_conf_path_present": "True",
            "builder_script_present": "True",
            "readme_sha": "sha",
            "readme_size": "100",
            "readme_public_domain_marker_present": "True",
            "readme_kjvdc_marker_present": "True",
            "readme_kjva_osis_marker_present": "True",
            "kjva_distribution_license": "GPL",
            "kjvdc_distribution_license": "General public license for distribution for any purpose",
            "kjva_crown_rights_marker_present": "True",
            "kjvdc_crown_rights_marker_present": "True",
            "source_audit_status": "source_candidate_not_confirmed",
            "source_use_status": "needs_rights_review",
            "verse_numbered_import_ready": "False",
            "source_lock_ready_status": "not_source_lock_ready",
            "result_ready_status": "not_result_ready",
        }
    )
    with rows.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.analyzer.ROW_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_rows_csv(rows)

    assert any("kjva_osis_path_present drifted" in failure for failure in failures)
    assert any("source_audit_status drifted" in failure for failure in failures)
