import csv
from pathlib import Path

from scripts import check_kjva_gutenberg_source_lock_blocker_packet_doc as check


def test_current_kjva_gutenberg_source_lock_blocker_packet_doc_passes() -> None:
    assert check.validate_kjva_gutenberg_source_lock_blocker_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_gutenberg_source_lock_blocker_packet_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Sirach gap: `SIR 44:23`.",
        "Sirach gap: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_gutenberg_source_lock_blocker_packet_doc(
        doc,
        marker_diff=None,
        boundary_options=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_marker_diff_drift_fails(tmp_path: Path) -> None:
    marker_diff = tmp_path / "marker_diff.csv"
    row = {
        "book": "SIR",
        "local_ref": "SIR 44:24",
        "chapter": "44",
        "verse": "24",
        "status": "missing_source_marker",
        "source_line": "",
        "previous_source_marker": "SIR 44:22@line 10",
        "next_source_marker": "SIR 45:1@line 20",
        "notes": "",
    }
    with marker_diff.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=check.packet.MARKER_DIFF_FIELDNAMES,
        )
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_marker_diff_csv(marker_diff)

    assert any("local_ref drifted" in failure for failure in failures)
    assert any("verse drifted" in failure for failure in failures)


def test_boundary_options_result_boundary_drift_fails(tmp_path: Path) -> None:
    boundary_options = tmp_path / "boundary_options.csv"
    rows = [
        {
            "book": "SIR",
            "issue": "issue",
            "option_id": option_id,
            "recommendation_status": "recommended",
            "recommendation": "rec",
            "blocker": "blocker",
            "result_boundary": "not_result_bearing",
        }
        for option_id in {
            "sirach_defer_until_citable_collation",
            "sirach_do_not_auto_insert_marker",
            "manasseh_defer_until_citable_marked_source",
            "manasseh_exclude_until_policy_lock",
            "manasseh_manual_split_requires_review",
        }
    ]
    rows[0]["result_boundary"] = "result_bearing"
    with boundary_options.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=check.packet.BOUNDARY_OPTION_FIELDNAMES,
        )
        writer.writeheader()
        writer.writerows(rows)

    failures = check.validate_boundary_options_csv(boundary_options)

    assert any("result-bearing option row" in failure for failure in failures)


def test_summary_status_drift_fails(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    row = {
        "source_status": "fetched",
        "source_mode": "network_fetch",
        "source_url_or_path": "url",
        "apocrypha_plain_text_bytes": "1",
        "apocrypha_plain_text_sha256": "hash",
        "raw_text_retained": "False",
        "sirach_source_markers": "1392",
        "sirach_local_markers": "1393",
        "sirach_missing_source_marker_count": "0",
        "sirach_extra_source_marker_count": "0",
        "sirach_gap_refs": "",
        "manasseh_source_section_detected": "True",
        "manasseh_source_section_start_line": "1",
        "manasseh_source_section_end_line": "2",
        "manasseh_source_markers": "0",
        "manasseh_local_markers": "15",
        "manasseh_boundary_option_rows": "3",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "blocker_packet_only_not_result_bearing",
    }
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.packet.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(summary)

    assert any("sirach_missing_source_marker_count drifted" in failure for failure in failures)
    assert any("sirach_gap_refs drifted" in failure for failure in failures)
