from types import SimpleNamespace

from scripts import analyze_kjva_gutenberg_candidate_source as analyzer


def _args() -> SimpleNamespace:
    return SimpleNamespace(
        rdf_url=analyzer.RDF_URL,
        ebook_page_url=analyzer.EBOOK_PAGE_URL,
    )


def test_analyze_rdf_marks_public_domain_candidate() -> None:
    raw = b"""<?xml version="1.0"?>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:pgterms="http://www.gutenberg.org/2009/pgterms/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <pgterms:ebook rdf:about="ebooks/30">
    <dcterms:title>The Bible, King James Version, Complete</dcterms:title>
    <dcterms:rights>Public domain in the USA.</dcterms:rights>
    <dcterms:issued>1992-04-01</dcterms:issued>
    <pgterms:downloads>1</pgterms:downloads>
    <dcterms:description>From many editions.</dcterms:description>
  </pgterms:ebook>
  <pgterms:file rdf:about="https://www.gutenberg.org/ebooks/30.txt.utf-8" />
</rdf:RDF>"""
    fetched = analyzer.FetchedRdf(raw=raw, final_url=analyzer.RDF_URL, fetch_status="fetched")

    row = analyzer.analyze_rdf(_args(), fetched)

    assert row["source_audit_status"] == "public_domain_kjv_complete_metadata_needs_apocrypha_coverage_probe"
    assert row["public_domain_usa_marker_present"] is True
    assert row["plain_text_utf8_url_present"] is True
    assert row["apocrypha_marker_present"] is False
    assert row["source_use_status"] == "needs_source_use_policy_lock"
    assert row["result_ready_status"] == "not_result_ready"


def test_build_summary_keeps_non_result_boundary() -> None:
    row = {
        "fetch_status": "fetched",
        "public_domain_usa_marker_present": True,
        "source_audit_status": "public_domain_kjv_complete_metadata_needs_apocrypha_coverage_probe",
        "apocrypha_marker_present": False,
        "plain_text_utf8_url_present": True,
        "source_use_status": "needs_source_use_policy_lock",
        "source_lock_ready_status": "not_source_lock_ready",
        "verse_numbered_import_ready": False,
        "result_ready_status": "not_result_ready",
    }

    summary = analyzer.build_summary([row])

    assert summary["public_domain_usa_pages"] == 1
    assert summary["kjv_complete_metadata_candidates"] == 1
    assert summary["apocrypha_marker_pages"] == 0
    assert summary["source_lock_ready_pages"] == 0
    assert summary["result_ready_pages"] == 0
