import csv
from pathlib import Path

from scripts import check_source_basis_audit_queue as check


def test_current_source_basis_queue_passes() -> None:
    assert check.validate_source_basis_queue() == []


def test_validate_source_basis_queue_rejects_stale_doc_counts(tmp_path) -> None:
    biblegateway = tmp_path / "biblegateway.csv"
    ebible = tmp_path / "ebible.csv"
    door43, oet, otb, openbible, odr = write_empty_control_manifests(tmp_path)
    audit_queue = tmp_path / "queue.md"
    write_manifest(
        biblegateway,
        [
            {
                "label": "KJV",
                "coverage": "full",
                "ot_basis": "Masoretic/KJV lineage",
                "nt_basis": "Textus Receptus/KJV lineage",
                "source_family": "KJV/TR tradition",
                "basis_status": "broad_tradition",
            }
        ],
    )
    write_manifest(
        ebible,
        [
            {
                "label": "ASV",
                "coverage": "full",
                "ot_basis": "Masoretic/RV lineage",
                "nt_basis": "critical/RV-Westcott-Hort lineage",
                "source_family": "critical/RV tradition",
                "basis_status": "broad_tradition",
                "source_id": "eng-asv",
                "source_url": "https://ebible.org/Scriptures/eng-asv_usfm.zip",
                "details_url": "https://ebible.org/find/show.php?id=eng-asv",
                "license_label": "public-domain-marked by eBible",
            }
        ],
    )
    audit_queue.write_text(
        "\n".join(
            [
                "| Manifest | Rows | `needs_audit` | `broad_tradition` |",
                "| --- | ---: | ---: | ---: |",
                "| BibleGateway English versions | 2 | 0 | 2 |",
                "| eBible English controls | 1 | 0 | 1 |",
                "| Door43 English controls | 0 | 0 | 0 |",
                "| OET English controls | 0 | 0 | 0 |",
                "| OTB English controls | 0 | 0 | 0 |",
                "| Open.Bible English controls | 0 | 0 | 0 |",
                "| Original Douay-Rheims English controls | 0 | 0 | 0 |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_source_basis_queue(
        biblegateway_manifest=biblegateway,
        ebible_controls=ebible,
        door43_controls=door43,
        oet_controls=oet,
        otb_controls=otb,
        openbible_controls=openbible,
        odr_controls=odr,
        audit_queue=audit_queue,
    )

    assert len(failures) == 1
    assert failures[0].startswith("audit queue counts do not match manifests:")


def test_validate_source_basis_queue_rejects_needs_audit_rows(tmp_path) -> None:
    biblegateway = tmp_path / "biblegateway.csv"
    ebible = tmp_path / "ebible.csv"
    door43, oet, otb, openbible, odr = write_empty_control_manifests(tmp_path)
    audit_queue = tmp_path / "queue.md"
    write_manifest(
        biblegateway,
        [
            {
                "label": "DEMO",
                "coverage": "full",
                "ot_basis": "unknown",
                "nt_basis": "unknown",
                "source_family": "unknown",
                "basis_status": "needs_audit",
            }
        ],
    )
    write_manifest(ebible, [])
    audit_queue.write_text(
        "\n".join(
            [
                "| Manifest | Rows | `needs_audit` | `broad_tradition` |",
                "| --- | ---: | ---: | ---: |",
                "| BibleGateway English versions | 1 | 1 | 0 |",
                "| eBible English controls | 0 | 0 | 0 |",
                "| Door43 English controls | 0 | 0 | 0 |",
                "| OET English controls | 0 | 0 | 0 |",
                "| OTB English controls | 0 | 0 | 0 |",
                "| Open.Bible English controls | 0 | 0 | 0 |",
                "| Original Douay-Rheims English controls | 0 | 0 | 0 |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_source_basis_queue(
        biblegateway_manifest=biblegateway,
        ebible_controls=ebible,
        door43_controls=door43,
        oet_controls=oet,
        otb_controls=otb,
        openbible_controls=openbible,
        odr_controls=odr,
        audit_queue=audit_queue,
    )

    assert failures == ["needs_audit rows remain: BibleGateway English versions:DEMO"]
    assert (
        check.validate_source_basis_queue(
            biblegateway_manifest=biblegateway,
            ebible_controls=ebible,
            door43_controls=door43,
            oet_controls=oet,
            otb_controls=otb,
            openbible_controls=openbible,
            odr_controls=odr,
            audit_queue=audit_queue,
            allow_needs_audit=True,
        )
        == []
    )


def test_validate_source_basis_queue_rejects_bad_ebible_metadata(tmp_path) -> None:
    biblegateway = tmp_path / "biblegateway.csv"
    ebible = tmp_path / "ebible.csv"
    door43, oet, otb, openbible, odr = write_empty_control_manifests(tmp_path)
    audit_queue = tmp_path / "queue.md"
    write_manifest(biblegateway, [])
    write_manifest(
        ebible,
        [
            {
                "label": "ASV",
                "coverage": "full",
                "ot_basis": "Masoretic/RV lineage",
                "nt_basis": "critical/RV-Westcott-Hort lineage",
                "source_family": "critical/RV tradition",
                "basis_status": "broad_tradition",
                "source_id": "",
                "source_url": "https://example.test/asv.zip",
                "details_url": "https://ebible.org/find/show.php",
                "license_label": "public domain",
            }
        ],
    )
    audit_queue.write_text(
        "\n".join(
            [
                "| Manifest | Rows | `needs_audit` | `broad_tradition` |",
                "| --- | ---: | ---: | ---: |",
                "| BibleGateway English versions | 0 | 0 | 0 |",
                "| eBible English controls | 1 | 0 | 1 |",
                "| Door43 English controls | 0 | 0 | 0 |",
                "| OET English controls | 0 | 0 | 0 |",
                "| OTB English controls | 0 | 0 | 0 |",
                "| Open.Bible English controls | 0 | 0 | 0 |",
                "| Original Douay-Rheims English controls | 0 | 0 | 0 |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_source_basis_queue(
        biblegateway_manifest=biblegateway,
        ebible_controls=ebible,
        door43_controls=door43,
        oet_controls=oet,
        otb_controls=otb,
        openbible_controls=openbible,
        odr_controls=odr,
        audit_queue=audit_queue,
    )

    assert failures == [
        "eBible English controls row 2: missing source_id",
        "eBible English controls row 2: invalid source_url",
        "eBible English controls row 2: invalid details_url",
        "eBible English controls row 2: missing eBible license_label",
    ]


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "label",
        "coverage",
        "ot_basis",
        "nt_basis",
        "source_family",
        "basis_status",
        "source_id",
        "source_url",
        "details_url",
        "license_label",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_empty_control_manifests(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    door43 = tmp_path / "door43.csv"
    oet = tmp_path / "oet.csv"
    otb = tmp_path / "otb.csv"
    openbible = tmp_path / "openbible.csv"
    odr = tmp_path / "odr.csv"
    write_manifest(door43, [])
    write_manifest(oet, [])
    write_manifest(otb, [])
    write_manifest(openbible, [])
    write_manifest(odr, [])
    return door43, oet, otb, openbible, odr
