import csv
from pathlib import Path

from scripts import check_cities_claim_catalog_boundary as check


def test_current_cities_claim_catalog_boundary_passes() -> None:
    assert check.validate_cities_claim_catalog_boundary() == []


def test_missing_claim_row_fails(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    doc = tmp_path / "CLAIM_CATALOG.md"
    records = tmp_path / "records.csv"
    write_catalog(catalog, [])
    write_doc(doc)
    write_records(records, [])

    failures = check.validate_cities_claim_catalog_boundary(catalog, doc, records)

    assert failures == [
        f"{catalog} has 0 rows for cities_aumann_simon_mckay_source_chain, expected 1"
    ]


def test_promoted_claim_status_fails(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    doc = tmp_path / "CLAIM_CATALOG.md"
    records = tmp_path / "records.csv"
    row = valid_row()
    row["status"] = "controlled_review_candidate"
    write_catalog(catalog, [row])
    write_doc(doc)
    write_records(records, [])

    failures = check.validate_cities_claim_catalog_boundary(catalog, doc, records)

    assert any("status='controlled_review_candidate'" in failure for failure in failures)


def test_missing_expected_lock_record_fails(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    doc = tmp_path / "CLAIM_CATALOG.md"
    records = tmp_path / "records.csv"
    write_catalog(catalog, [valid_row()])
    write_doc(doc)
    write_records(records, [])

    failures = check.validate_cities_claim_catalog_boundary(catalog, doc, records)

    assert failures == [f"{records} has 0 populated rows, expected 14"]


def test_missing_doc_boundary_phrase_fails(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    doc = tmp_path / "CLAIM_CATALOG.md"
    records = tmp_path / "records.csv"
    write_catalog(catalog, [valid_row()])
    write_doc(doc, omit="14 populated lock rows")
    write_records(records, valid_records())

    failures = check.validate_cities_claim_catalog_boundary(catalog, doc, records)

    assert failures == [f"{doc} missing phrase: 14 populated lock rows"]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--catalog", str(tmp_path / "missing.csv")])

    assert code == 1
    assert "Cities claim-catalog boundary failure" in capsys.readouterr().err


def valid_row() -> dict[str, str]:
    return {
        "claim_id": check.CLAIM_ID,
        "claim_group": "torah_code_cities_source",
        "source_label": "Torah-code.org Cities/Aumann/Simon-McKay source chain",
        "source_url": "https://www.torah-code.org/experiments.html",
        "status": "under_specified",
        "language": "hebrew",
        "corpus_scope": "Cities/community source material",
        "terms": "Cities and community names",
        "spellings_or_forms": "not imported",
        "skip_or_rule": "not locked",
        "layout_or_metric": "compactness/proximity source rows",
        "current_reproduction": (
            "Source-chain audit and source-row lock handoff exist; current "
            "decision records have 14 populated lock rows and the transcription "
            "worksheet has 14 pending review rows with no source rows imported; "
            "OCR page review has 61 packet pages with 41 reviewed and "
            "20 unreviewed"
        ),
        "evidence": "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
        "notes": (
            "14 candidate pages are source-review only; no city-name normalization "
            "ELS searches compactness runs or p-levels; future transcription/import "
            "rows must cite evidence and pass preflight."
        ),
    }


def write_catalog(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "claim_id",
        "claim_group",
        "source_label",
        "source_url",
        "status",
        "language",
        "corpus_scope",
        "terms",
        "spellings_or_forms",
        "skip_or_rule",
        "layout_or_metric",
        "current_reproduction",
        "evidence",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_doc(path: Path, *, omit: str = "") -> None:
    phrases = [
        "Torah-code.org Cities/Aumann/Simon-McKay source chain",
        "Cities source-row lock handoff has 14 source-row lock candidate pages",
        "14 populated lock rows",
        "14 pending transcription-review rows",
        "no source rows imported",
        "no city-name normalization, ELS searches, compactness runs, or p-levels",
        "data/study/mappings/cities_source_row_lock_decisions.csv",
        "data/study/mappings/cities_source_transcription_decisions.csv",
        "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
        "61 OCR packet pages",
        "41 reviewed OCR packet pages",
        "20 unreviewed OCR packet pages",
    ]
    path.write_text(
        "\n".join(phrase for phrase in phrases if phrase != omit),
        encoding="utf-8",
    )


def valid_records() -> list[dict[str, str]]:
    return [
        {
            "decision_id": f"cities_source_row_lock_{index:03d}",
            "decision_status": "locked",
            "selected_action": "source_row_lock_ready",
        }
        for index in range(1, 15)
    ]


def write_records(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["decision_id", "decision_status", "selected_action"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
