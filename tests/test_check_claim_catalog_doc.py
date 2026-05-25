import csv
from pathlib import Path

from scripts import check_claim_catalog_doc as check


def test_current_claim_catalog_doc_passes() -> None:
    assert check.validate_claim_catalog_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    write_catalog(catalog, 1)

    failures = check.validate_claim_catalog_doc(catalog, tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_entry_total_must_match_catalog_rows(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    doc = tmp_path / "CLAIM_CATALOG.md"
    write_catalog(catalog, 2)
    doc.write_text(
        "\n".join(
            [
                "# Claim Catalog",
                "",
                "- `claims/claim_catalog.csv`",
                "",
                "## Current Entries",
                "",
                "| Group | Status | Entries | Current read |",
                "| --- | --- | ---: | --- |",
                "| Demo | `reproducible` | 1 | read |",
                "",
            ]
        ),
        encoding="utf-8",
    )

    failures = check.validate_claim_catalog_doc(catalog, doc)

    assert failures == [f"{doc} Current Entries total is 1, but {catalog} has 2 rows"]


def test_unknown_status_fails(tmp_path: Path) -> None:
    catalog = tmp_path / "claims.csv"
    doc = tmp_path / "CLAIM_CATALOG.md"
    write_catalog(catalog, 1)
    doc.write_text(
        "\n".join(
            [
                "# Claim Catalog",
                "",
                "- `claims/claim_catalog.csv`",
                "",
                "## Current Entries",
                "",
                "| Group | Status | Entries | Current read |",
                "| --- | --- | ---: | --- |",
                "| Demo | `promoted` | 1 | read |",
                "",
            ]
        ),
        encoding="utf-8",
    )

    failures = check.validate_claim_catalog_doc(catalog, doc)

    assert failures == [f"{doc} has unknown Current Entries status: promoted"]


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--doc", str(tmp_path / "missing.md")])

    assert code == 1
    assert "claim-catalog doc failure" in capsys.readouterr().err


def write_catalog(path: Path, rows: int) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "claim_id",
                "claim_group",
                "source_label",
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
            ],
        )
        writer.writeheader()
        for index in range(rows):
            writer.writerow(
                {
                    "claim_id": f"claim_{index}",
                    "claim_group": "demo",
                    "source_label": "Demo",
                    "status": "reproducible",
                    "language": "english",
                    "corpus_scope": "demo",
                    "terms": "demo",
                    "spellings_or_forms": "demo",
                    "skip_or_rule": "demo",
                    "layout_or_metric": "demo",
                    "current_reproduction": "demo",
                    "evidence": "docs/CLAIM_CATALOG.md",
                    "notes": "demo",
                }
            )
