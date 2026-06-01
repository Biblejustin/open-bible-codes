import csv
import json

from scripts import build_wrr_no_input_handoff_status as builder
from scripts import check_wrr_no_input_handoff_status_doc as check


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
        "claim_readiness_rows": 4,
        "claim_readiness_ready_rows": 4,
        "claim_blocker_rows": 0,
        "source_cited_defined_distances": "163",
        "current_defined_distances": "72",
        "remaining_gap": "91",
        "review_lanes": 4,
        "residual_action_terms": 58,
        "residual_pairs": 59,
        "frontier_pairs": 40,
        "manual_decision_rows": 37,
        "manual_action_terms": 58,
        "manual_residual_pairs": 59,
        "manual_frontier_pairs": 40,
        "source_transcription_row_clusters": 22,
        "source_transcription_action_terms": 43,
        "page_image_terms": 3,
        "method_pair_universe_terms": 11,
        "wide_skip_max": "5000",
        "wide_skip_total_hits": 0,
        "new_result_allowed": False,
        "exact_reproduction_ready": False,
        "claim_boundary": builder.CLAIM_BOUNDARY,
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
                    "no" if status_id == "local_claim_readiness" else "yes"
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
    doc = tmp_path / "WRR_NO_INPUT_HANDOFF_STATUS.md"
    status = tmp_path / "status.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    builder.write_markdown(doc, summary, rows)
    _write_csv(status, builder.STATUS_FIELDNAMES, rows)
    _write_csv(summary_csv, builder.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "WRR no-input handoff only; no new result",
                "text_retention": "no Bible text written to tracked outputs",
                "summary": {
                    "new_result_allowed": False,
                    "exact_reproduction_ready": False,
                },
                "outputs": {"markdown": str(doc)},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_no_input_handoff_status_doc(
            doc,
            status=status,
            summary=summary_csv,
            manifest=manifest,
        )
        == []
    )


def test_checker_rejects_new_result_allowed_overclaim(tmp_path) -> None:
    doc = tmp_path / "handoff.md"
    doc.write_text(
        "# WRR No-Input Handoff Status\n\nNew WRR result allowed: 1.\n",
        encoding="utf-8",
    )

    failures = check.validate_no_input_handoff_status_doc(
        doc,
        status=None,
        summary=None,
        manifest=None,
    )

    assert any("overclaim" in failure or "missing phrase" in failure for failure in failures)


def test_checker_rejects_summary_drift(tmp_path) -> None:
    summary = _summary()
    summary["remaining_gap"] = "90"
    summary_csv = tmp_path / "summary.csv"
    _write_csv(summary_csv, builder.SUMMARY_FIELDNAMES, [summary])

    failures = check.validate_summary_csv(summary_csv)

    assert any("remaining_gap drifted" in failure for failure in failures)
