import csv
import json
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_collation as audit
from scripts import check_kjva_hakkaac_apocrypha_collation_doc as check


def test_current_collation_doc_passes() -> None:
    failures = check.validate_kjva_hakkaac_apocrypha_collation_doc()

    assert failures == []


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    doc.write_text("# KJVA Hakkaac Apocrypha Collation Audit\n", encoding="utf-8")

    failures = check.validate_kjva_hakkaac_apocrypha_collation_doc(
        doc,
        verse_rows=None,
        book_rows=None,
        blocker_rows=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_verse_drift_ref_change_fails(tmp_path: Path) -> None:
    path = tmp_path / "verses.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit.VERSE_FIELDNAMES)
        writer.writeheader()
        for index in range(5720):
            writer.writerow(
                {
                    "ref": "SIR 19:2" if index == 0 else f"TOB 1:{index}",
                    "book": "SIR" if index == 0 else "TOB",
                    "chapter": "19" if index == 0 else "1",
                    "verse": "2" if index == 0 else str(index),
                    "source_url": "url",
                    "source_status": "http_200",
                    "local_norm_len": "1",
                    "hakkaac_norm_len": "2" if index == 0 else "1",
                    "norm_len_delta": "1" if index == 0 else "0",
                    "local_norm_sha256": "x",
                    "hakkaac_norm_sha256": "y" if index == 0 else "x",
                    "first_diff_offset": "0" if index == 0 else "",
                    "status": "length_drift" if index == 0 else "exact_normalized_match",
                }
            )

    failures = check.validate_verse_rows(path)

    assert any("drift ref changed" in failure for failure in failures)


def test_summary_drift_fails(tmp_path: Path) -> None:
    path = tmp_path / "summary.csv"
    row = {
        "source_use_decision": "approved_ignored_local_collation_only",
        "private_text_path": "data/private/hakkaac_kjva_apocrypha/verses.csv",
        "pages_fetched": "14",
        "local_verses": "5720",
        "hakkaac_verses": "5720",
        "comparable_refs": "5720",
        "exact_normalized_verse_matches": "5720",
        "length_match_hash_drift_verses": "0",
        "length_drift_verses": "0",
        "missing_hakkaac_refs": "0",
        "missing_local_refs": "0",
        "exact_book_stream_matches": "14",
        "book_stream_drift_books": "0",
        "local_norm_letters": "593090",
        "hakkaac_norm_letters": "593090",
        "norm_len_delta": "0",
        "apocrypha_stream_hash_match": "True",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "ignored_local_collation_audit_only_not_result_bearing",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary(path)

    assert any("exact_normalized_verse_matches drifted" in failure for failure in failures)
    assert any("hakkaac_norm_letters drifted" in failure for failure in failures)


def test_manifest_boundary_drift_fails(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "bad",
                "text_retention": "raw Hakkaac text only in ignored data/private output",
                "source_use_decision": "approved ignored local import for collation only",
                "outputs": {"markdown": "doc.md"},
            }
        ),
        encoding="utf-8",
    )

    failures = check.validate_manifest(manifest, doc=Path("doc.md"))

    assert any("claim_boundary drifted" in failure for failure in failures)
