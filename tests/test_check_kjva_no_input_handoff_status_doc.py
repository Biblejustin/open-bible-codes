import csv
import json

from scripts import build_kjva_no_input_handoff_status as builder
from scripts import check_kjva_no_input_handoff_status_doc as check


def _write_csv(path, fieldnames, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _summary() -> dict[str, object]:
    return {
        "status_rows": 9,
        "handoff_ready_rows": 9,
        "manual_input_needed_rows": 8,
        "gate_rows": 11,
        "rerun_only_ready_rows": 1,
        "blocked_gate_rows": 10,
        "source_policy_blocker_rows": 7,
        "policy_option_rows": 5,
        "policy_ready_options": 2,
        "blocked_options": 3,
        "checksum_records_ready": 2,
        "current_rerun_locked": True,
        "candidate_source_audit_rows": 4,
        "candidate_source_verse_import_ready_pages": 0,
        "candidate_source_result_ready_pages": 0,
        "crosswire_possible_independent_kjva_candidates": 1,
        "gutenberg_split_kjv_apocrypha_metadata_candidates": 1,
        "wikisource_source_candidate_pages": 1,
        "open_bibles_kjv_paths": 1,
        "open_bibles_apocrypha_paths": 0,
        "open_bibles_deuterocanon_paths": 0,
        "source_use_ready_pages": 0,
        "source_lock_ready": False,
        "result_allowed": False,
        "completed_lane_terms": 7,
        "completed_lane_observed_bridge_rows": 1,
        "completed_lane_significant_terms": 0,
        "nonbible_controls_at_or_above_observed": 1,
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": 0,
        "gutenberg_manasseh_local_markers": 15,
        "hakkaac_exact_normalized_verse_matches": 5719,
        "hakkaac_total_verses": 5720,
        "hakkaac_length_drift_verses": 1,
        "split_source_role_rows": 7,
        "split_source_blocker_rows": 6,
        "fresh_terms_ready": False,
        "leakage_audit_ready": False,
        "fixed_controls_ready": False,
        "study_lock_ready": False,
        "claim_status": builder.CLAIM_BOUNDARY,
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    for status_id in check.REQUIRED_STATUS_IDS:
        rows.append(
            {
                "status_id": status_id,
                "area": "area",
                "current_status": "status",
                "current_value": "value",
                "handoff_ready": "yes",
                "manual_input_needed": (
                    "no" if status_id == "current_rerun_baseline" else "yes"
                ),
                "next_action": "next",
                "boundary": "boundary",
                "source": "source.csv",
            }
        )
    return rows


def test_checker_accepts_generated_handoff_doc(tmp_path) -> None:
    summary = _summary()
    rows = _rows()
    doc = tmp_path / "KJVA_NO_INPUT_HANDOFF_STATUS.md"
    status = tmp_path / "status.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    builder.write_markdown(doc, summary, rows)
    _write_csv(status, builder.STATUS_FIELDNAMES, rows)
    _write_csv(summary_csv, builder.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "KJVA no-input handoff only; no new result",
                "text_retention": "no Bible text written to tracked outputs",
                "summary": {
                    "result_allowed": False,
                    "source_lock_ready": False,
                },
                "outputs": {"markdown": str(doc)},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_kjva_no_input_handoff_status_doc(
            doc,
            status=status,
            summary=summary_csv,
            manifest=manifest,
        )
        == []
    )


def test_checker_rejects_result_allowed_overclaim(tmp_path) -> None:
    doc = tmp_path / "handoff.md"
    doc.write_text(
        "# KJVA No-Input Handoff Status\n\nResult allowed: 1.\n",
        encoding="utf-8",
    )

    failures = check.validate_kjva_no_input_handoff_status_doc(
        doc,
        status=None,
        summary=None,
        manifest=None,
    )

    assert any("overclaim" in failure or "missing phrase" in failure for failure in failures)


def test_checker_rejects_summary_drift(tmp_path) -> None:
    summary = _summary()
    summary["result_allowed"] = True
    summary_csv = tmp_path / "summary.csv"
    _write_csv(summary_csv, builder.SUMMARY_FIELDNAMES, [summary])

    failures = check.validate_summary_csv(summary_csv)

    assert any("result_allowed drifted" in failure for failure in failures)
