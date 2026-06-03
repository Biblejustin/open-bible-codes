import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
from pathlib import Path

from scripts import check_kjva_gutenberg_candidate_source_audit_doc as check


def test_current_kjva_gutenberg_source_audit_doc_passes() -> None:
    assert check.validate_kjva_gutenberg_candidate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_gutenberg_candidate_source_audit_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "KJV-complete metadata candidates: 1.",
        "KJV-complete metadata candidates: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_gutenberg_candidate_source_audit_doc(
        doc,
        rows=None,
        summary=None,
        anchors=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_rows_status_drift_fails(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    data = [
        {
            "source_id": "gutenberg_ebook_30_kjv_complete",
            "rdf_url": check.analyzer.KJV_RDF_URL,
            "final_url": check.analyzer.KJV_RDF_URL,
            "fetch_status": "fetched",
            "error": "",
            "bytes": "10",
            "sha256": "sha",
            "ebook_no": "30",
            "ebook_page_url": check.analyzer.KJV_EBOOK_PAGE_URL,
            "title": "The Bible, King James Version, Complete",
            "rights": "Public domain in the USA.",
            "issued": "1992-04-01",
            "downloads": "1",
            "description_count": "1",
            "descriptions": "desc",
            "plain_text_utf8_url_present": "False",
            "html_url_present": "True",
            "epub_url_present": "True",
            "apocrypha_marker_present": "False",
            "public_domain_usa_marker_present": "True",
            "source_audit_status": "source_candidate_not_confirmed",
            "source_use_status": "needs_source_use_policy_lock",
            "verse_numbered_import_ready": "False",
            "source_lock_ready_status": "not_source_lock_ready",
            "result_ready_status": "not_result_ready",
        },
        {
            "source_id": "gutenberg_ebook_124_deuterocanonical",
            "rdf_url": check.analyzer.APOCRYPHA_RDF_URL,
            "final_url": check.analyzer.APOCRYPHA_RDF_URL,
            "fetch_status": "fetched",
            "error": "",
            "bytes": "10",
            "sha256": "sha",
            "ebook_no": "124",
            "ebook_page_url": check.analyzer.APOCRYPHA_EBOOK_PAGE_URL,
            "title": "Deuterocanonical Books of the Bible Apocrypha",
            "rights": "Public domain in the USA.",
            "issued": "1994-04-01",
            "downloads": "1",
            "description_count": "1",
            "descriptions": "desc",
            "plain_text_utf8_url_present": "True",
            "html_url_present": "True",
            "epub_url_present": "True",
            "apocrypha_marker_present": "True",
            "public_domain_usa_marker_present": "True",
            "source_audit_status": "public_domain_apocrypha_metadata_component",
            "source_use_status": "needs_source_use_policy_lock",
            "verse_numbered_import_ready": "False",
            "source_lock_ready_status": "not_source_lock_ready",
            "result_ready_status": "not_result_ready",
        },
    ]
    with rows.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.analyzer.ROW_FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

    failures = check.validate_rows_csv(rows)

    assert any("plain_text_utf8_url_present drifted" in failure for failure in failures)
    assert any("source_audit_status drifted" in failure for failure in failures)
