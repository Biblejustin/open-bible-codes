import csv
import json
from pathlib import Path

from scripts import check_english_missing_verse_attribution_doc as check


def test_validate_accepts_consistent_fixture(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    summary = tmp_path / "summary.csv"
    missing_refs = tmp_path / "missing_refs.csv"
    context = tmp_path / "context.csv"
    manifest = tmp_path / "manifest.json"

    manifest.write_text(
        json.dumps(
            {
                "included_versions": 1,
                "missing_versions": 2,
                "versions_with_missing_kjv_refs": 1,
                "known_nt_disputed_kjv_ref_rows": 1,
                "versions_with_known_nt_disputed_kjv_refs": 1,
                "other_reference_gap_rows": 1,
                "context_hit_rows": 1,
                "context_missing_verse_attributed_rows": 0,
            }
        ),
        encoding="utf-8",
    )
    write_csv(
        summary,
        [
            "version_label",
            "version_name",
            "missing_kjv_refs",
            "known_nt_disputed_kjv_refs",
            "other_reference_gaps",
            "result",
        ],
        [
            {
                "version_label": "TST",
                "version_name": "Test",
                "missing_kjv_refs": "2",
                "known_nt_disputed_kjv_refs": "1",
                "other_reference_gaps": "1",
                "result": "seed_scan_not_run",
            }
        ],
    )
    write_csv(
        missing_refs,
        ["version_label", "ref", "kjv_norm_length", "ref_gap_category"],
        [
            {
                "version_label": "TST",
                "ref": "ACT 8:37",
                "kjv_norm_length": "40",
                "ref_gap_category": "known_nt_disputed_kjv_ref",
            },
            {
                "version_label": "TST",
                "ref": "NUM 1:21",
                "kjv_norm_length": "40",
                "ref_gap_category": "other_reference_gap",
            },
        ],
    )
    write_csv(
        context,
        [
            "corpus",
            "normalized_term",
            "start_ref",
            "end_ref",
            "missing_refs_in_augmented_span",
            "missing_verse_attribution",
        ],
        [
            {
                "corpus": "TST",
                "normalized_term": "disciple",
                "start_ref": "1TH 2:14",
                "end_ref": "1TH 3:1",
                "missing_refs_in_augmented_span": "",
                "missing_verse_attribution": "not_missing_verse_related",
            }
        ],
    )
    doc.write_text(
        "\n".join(
            [
                "# English Missing-Verse Attribution",
                "`protocols/english_missing_verse_attribution.toml`",
                "`scripts/analyze_english_missing_verse_attribution.py`",
                "Available BibleGateway-overlap English versions checked: 1.",
                "Missing BibleGateway versions skipped: 2.",
                "Versions with at least one KJV reference absent: 1.",
                "Reference-gap rows: 2.",
                "Known New Testament disputed KJV-reference rows: 1 across 1 versions.",
                "Current context-review rows checked: 1.",
                "Context-review rows attributed to missing verses: 0.",
                "current reviewed English hits are not explained by missing-verse gaps",
                "Reference gaps are broader than textual omissions.",
                "Comma Johanneum",
            ]
        ),
        encoding="utf-8",
    )

    assert (
        check.validate(
            doc=doc,
            summary=summary,
            missing_refs=missing_refs,
            context=context,
            manifest=manifest,
        )
        == []
    )


def test_validate_rejects_category_count_drift(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    summary = tmp_path / "summary.csv"
    missing_refs = tmp_path / "missing_refs.csv"
    context = tmp_path / "context.csv"
    manifest = tmp_path / "manifest.json"

    manifest.write_text(
        json.dumps(
            {
                "included_versions": 0,
                "missing_versions": 0,
                "versions_with_missing_kjv_refs": 0,
                "known_nt_disputed_kjv_ref_rows": 99,
                "versions_with_known_nt_disputed_kjv_refs": 0,
                "other_reference_gap_rows": 0,
                "context_hit_rows": 0,
                "context_missing_verse_attributed_rows": 0,
            }
        ),
        encoding="utf-8",
    )
    write_csv(
        summary,
        [
            "version_label",
            "version_name",
            "missing_kjv_refs",
            "known_nt_disputed_kjv_refs",
            "other_reference_gaps",
            "result",
        ],
        [],
    )
    write_csv(missing_refs, ["version_label", "ref", "kjv_norm_length", "ref_gap_category"], [])
    write_csv(
        context,
        [
            "corpus",
            "normalized_term",
            "start_ref",
            "end_ref",
            "missing_refs_in_augmented_span",
            "missing_verse_attribution",
        ],
        [],
    )
    doc.write_text("", encoding="utf-8")

    failures = check.validate(
        doc=doc,
        summary=summary,
        missing_refs=missing_refs,
        context=context,
        manifest=manifest,
    )

    assert "known disputed ref count does not match manifest" in failures


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
