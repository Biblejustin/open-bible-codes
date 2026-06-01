from scripts import build_kjva_current_source_lock_sidecar as sidecar


def test_build_book_shape_counts_and_hashes_books() -> None:
    rows = [
        {"book": "GEN", "ref": "GEN 1:1", "text": "In the beginning"},
        {"book": "GEN", "ref": "GEN 1:2", "text": "And the earth"},
        {"book": "TOB", "ref": "TOB 1:1", "text": "Tobit text"},
    ]

    book_rows = sidecar.build_book_shape(rows)

    assert [row["book"] for row in book_rows] == ["GEN", "TOB"]
    assert book_rows[0]["verses"] == 2
    assert book_rows[0]["first_ref"] == "GEN 1:1"
    assert book_rows[0]["last_ref"] == "GEN 1:2"
    assert book_rows[0]["is_apocrypha"] is False
    assert book_rows[1]["is_apocrypha"] is True
    assert len(book_rows[0]["stream_sha256"]) == 64


def test_build_summary_keeps_sidecar_non_result_bearing(tmp_path) -> None:
    csv_path = tmp_path / "kjva.csv"
    csv_path.write_text("ref,book,chapter,verse,text\nTOB 1:1,TOB,1,1,x\n", encoding="utf-8")
    source_manifest = {
        "source_id": "eng-kjv",
        "source_name": "eBible English KJV + Apocrypha",
        "source_url": "https://example.test/source.zip",
        "details_url": "https://example.test/details",
        "license": "public-domain-marked by eBible",
        "downloaded_at": "2026-01-01T00:00:00+00:00",
        "zip_sha256": "a" * 64,
        "zip_bytes": 123,
    }
    book_rows = [
        {
            "book": "TOB",
            "verses": 1,
            "normalized_letters": 1,
            "is_apocrypha": True,
        }
    ]

    summary = sidecar.build_summary(csv_path, source_manifest, book_rows)

    assert summary["source_id"] == "eng-kjv"
    assert summary["book_count"] == 1
    assert summary["verse_count"] == 1
    assert summary["apocrypha_book_count"] == 1
    assert summary["apocrypha_verse_count"] == 1
    assert summary["rerun_baseline_locked"] is True
    assert summary["independent_source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "current_source_rerun_sidecar_only_not_result_bearing"
