import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
from pathlib import Path

from scripts import check_kjva_current_source_lock_sidecar_doc as check


def test_current_kjva_current_source_lock_sidecar_doc_passes() -> None:
    assert check.validate_kjva_current_source_lock_sidecar_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_current_source_lock_sidecar_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Books: 80.",
        "Books: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_current_source_lock_sidecar_doc(
        doc,
        book_shape=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_summary_count_drift_fails(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    row = {
        "source_id": "eng-kjv",
        "source_name": "eBible English KJV + Apocrypha",
        "source_url": "https://ebible.org/Scriptures/eng-kjv_usfm.zip",
        "details_url": "https://ebible.org/find/show.php?id=eng-kjv",
        "license": "public-domain-marked by eBible; preserve upstream notice",
        "downloaded_at": "2026-05-09T03:04:25.467342+00:00",
        "zip_sha256": check.EXPECTED_ZIP_SHA256,
        "zip_bytes": "2770418",
        "csv_path": "data/processed/ebible/eng-kjv.csv",
        "csv_sha256": check.EXPECTED_CSV_SHA256,
        "csv_bytes": "5705852",
        "book_count": "79",
        "verse_count": "36822",
        "apocrypha_book_count": "14",
        "apocrypha_verse_count": "5720",
        "apocrypha_normalized_letters": "593090",
        "full_book_order": check.EXPECTED_FULL_ORDER,
        "apocrypha_book_order": check.EXPECTED_APOCRYPHA_ORDER,
        "rerun_baseline_locked": "True",
        "independent_source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "current_source_rerun_sidecar_only_not_result_bearing",
    }
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.sidecar.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(summary)

    assert any("book_count drifted" in failure for failure in failures)
