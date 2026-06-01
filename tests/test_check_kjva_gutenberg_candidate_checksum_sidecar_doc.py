import csv
import json

from scripts import build_kjva_gutenberg_candidate_checksum_sidecar as sidecar
from scripts import check_kjva_gutenberg_candidate_checksum_sidecar_doc as check


def _write_csv(path, fieldnames, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _checksum_rows() -> list[dict[str, str]]:
    return [
        {
            "source_id": "gutenberg_ebook_30_kjv_complete",
            "component": "kjv_66_book_component",
            "ebook_no": "30",
            "metadata_url": "https://example.test/30.rdf",
            "source_page_url": "https://example.test/30",
            "title": "KJV",
            "rights": "Public domain in the USA.",
            "rdf_sha256": "a" * 64,
            "rdf_bytes": "10",
            "plain_text_sha256": check.EXPECTED_KJV_PLAIN_SHA,
            "plain_text_bytes": "111",
            "plain_text_utf8_url_present": "True",
            "source_use_status": "needs_source_use_policy_lock",
            "checksum_role": "candidate_identifier_only",
            "lock_status": "checksum_record_ready_not_source_locked",
            "result_boundary": "not_result_bearing",
        },
        {
            "source_id": "gutenberg_ebook_124_deuterocanonical",
            "component": "apocrypha_deuterocanon_component",
            "ebook_no": "124",
            "metadata_url": "https://example.test/124.rdf",
            "source_page_url": "https://example.test/124",
            "title": "Apocrypha",
            "rights": "Public domain in the USA.",
            "rdf_sha256": "b" * 64,
            "rdf_bytes": "20",
            "plain_text_sha256": check.EXPECTED_APOCRYPHA_PLAIN_SHA,
            "plain_text_bytes": "222",
            "plain_text_utf8_url_present": "True",
            "source_use_status": "needs_source_use_policy_lock",
            "checksum_role": "candidate_identifier_only",
            "lock_status": "checksum_record_ready_not_source_locked",
            "result_boundary": "not_result_bearing",
        },
    ]


def _summary() -> dict[str, object]:
    return {
        "source_rows": 2,
        "metadata_fetches_ok": "2",
        "public_domain_usa_rows": 2,
        "plain_text_rows": 2,
        "checksum_records_ready": 2,
        "kjv_plain_text_sha256": check.EXPECTED_KJV_PLAIN_SHA,
        "apocrypha_plain_text_sha256": check.EXPECTED_APOCRYPHA_PLAIN_SHA,
        "source_use_ready_pages": "0",
        "verse_import_ready_pages": "0",
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "checksum_sidecar_only_not_result_bearing",
    }


def test_checker_accepts_generated_checksum_sidecar(tmp_path) -> None:
    doc = tmp_path / "KJVA_GUTENBERG_CANDIDATE_CHECKSUM_SIDECAR.md"
    checksums = tmp_path / "checksums.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"
    rows = _checksum_rows()
    summary = _summary()

    sidecar.write_markdown(doc, summary, rows)
    _write_csv(checksums, sidecar.CHECKSUM_FIELDNAMES, rows)
    _write_csv(summary_csv, sidecar.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "checksum sidecar only; no ELS result",
                "text_retention": "no Bible text written to tracked outputs",
                "outputs": {"markdown": str(doc)},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_kjva_gutenberg_candidate_checksum_sidecar_doc(
            doc,
            checksums=checksums,
            summary=summary_csv,
            manifest=manifest,
        )
        == []
    )


def test_checker_rejects_source_use_overclaim(tmp_path) -> None:
    doc = tmp_path / "sidecar.md"
    doc.write_text(
        "# KJVA Gutenberg Candidate Checksum Sidecar\n\n"
        "This source-use approved result is ready.\n",
        encoding="utf-8",
    )

    failures = check.validate_kjva_gutenberg_candidate_checksum_sidecar_doc(
        doc,
        checksums=None,
        summary=None,
        manifest=None,
    )

    assert any("overclaim" in failure or "missing phrase" in failure for failure in failures)
