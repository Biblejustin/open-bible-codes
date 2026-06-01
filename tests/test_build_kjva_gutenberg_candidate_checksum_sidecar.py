from scripts import build_kjva_gutenberg_candidate_checksum_sidecar as sidecar


def _source_rows() -> list[dict[str, str]]:
    return [
        {
            "source_id": "gutenberg_ebook_30_kjv_complete",
            "ebook_no": "30",
            "final_url": "https://example.test/30.rdf",
            "ebook_page_url": "https://example.test/30",
            "title": "KJV",
            "rights": "Public domain in the USA.",
            "sha256": "a" * 64,
            "bytes": "10",
            "plain_text_utf8_url_present": "True",
            "source_use_status": "needs_source_use_policy_lock",
        },
        {
            "source_id": "gutenberg_ebook_124_deuterocanonical",
            "ebook_no": "124",
            "final_url": "https://example.test/124.rdf",
            "ebook_page_url": "https://example.test/124",
            "title": "Apocrypha",
            "rights": "Public domain in the USA.",
            "sha256": "b" * 64,
            "bytes": "20",
            "plain_text_utf8_url_present": "True",
            "source_use_status": "needs_source_use_policy_lock",
        },
    ]


def _prep_summary() -> dict[str, str]:
    return {
        "kjv_plain_text_sha256": "c" * 64,
        "kjv_plain_text_bytes": "111",
        "apocrypha_plain_text_sha256": "d" * 64,
        "apocrypha_plain_text_bytes": "222",
    }


def test_build_checksum_rows_joins_plain_text_hashes() -> None:
    rows = sidecar.build_checksum_rows(_source_rows(), _prep_summary())

    assert len(rows) == 2
    assert rows[0]["component"] == "kjv_66_book_component"
    assert rows[0]["plain_text_sha256"] == "c" * 64
    assert rows[1]["component"] == "apocrypha_deuterocanon_component"
    assert rows[1]["plain_text_sha256"] == "d" * 64
    assert rows[1]["lock_status"] == "checksum_record_ready_not_source_locked"


def test_build_summary_keeps_checksum_sidecar_non_result_bearing() -> None:
    rows = sidecar.build_checksum_rows(_source_rows(), _prep_summary())
    source_summary = {
        "metadata_fetches_ok": "2",
        "source_use_ready_pages": "0",
        "verse_import_ready_pages": "0",
    }

    summary = sidecar.build_summary(rows, source_summary, _prep_summary())

    assert summary["source_rows"] == 2
    assert summary["public_domain_usa_rows"] == 2
    assert summary["plain_text_rows"] == 2
    assert summary["checksum_records_ready"] == 2
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "checksum_sidecar_only_not_result_bearing"
