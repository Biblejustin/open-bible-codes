import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
from pathlib import Path

from scripts import build_no_input_blocker_summary as builder
from scripts import check_no_input_blocker_summary_doc as checker


def test_current_no_input_blocker_summary_doc_passes() -> None:
    assert checker.validate_no_input_blocker_summary_doc() == []


def test_checker_rejects_result_allowed_lane(tmp_path: Path) -> None:
    doc = tmp_path / "summary.md"
    status = tmp_path / "status.csv"
    summary = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    doc.write_text("\n".join(checker.REQUIRED_PHRASES), encoding="utf-8")
    _write_csv(
        status,
        builder.LANE_FIELDNAMES,
        [
            _lane("wrr", "0"),
            _lane("cities", "1"),
            _lane("kjva", "0"),
        ],
    )
    _write_csv(
        summary,
        builder.SUMMARY_FIELDNAMES,
        [
            {
                "lane_rows": "3",
                "total_status_rows": "26",
                "total_manual_input_needed_rows": "22",
                "result_allowed_lanes": "1",
                "blocked_result_lanes": "2",
                "wrr_remaining_gap": "91",
                "cities_pending_transcription_rows": "14",
                "kjva_blocked_gate_rows": "10",
                "claim_boundary": builder.CLAIM_BOUNDARY,
            }
        ],
    )
    manifest.write_text(
        json.dumps(
            {
                "tool": "scripts.build_no_input_blocker_summary",
                "claim_boundary": "no-input blocker summary only; no result-bearing output",
                "text_retention": "no Bible text written to tracked outputs",
                "outputs": {"markdown": str(doc)},
                "summary": {"result_allowed_lanes": 1},
            }
        ),
        encoding="utf-8",
    )

    failures = checker.validate_no_input_blocker_summary_doc(
        doc, status=status, summary=summary, manifest=manifest
    )

    assert any("result_allowed" in failure for failure in failures)
    assert any("result_allowed_lanes" in failure for failure in failures)


def _lane(lane_id: str, result_allowed: str) -> dict[str, str]:
    return {
        "lane_id": lane_id,
        "lane_name": lane_id,
        "status_rows": "1",
        "manual_input_needed_rows": "1",
        "result_allowed": result_allowed,
        "primary_blocker": "blocked",
        "next_human_input": "manual",
        "source_status": "blocked",
        "summary_source": "summary.csv",
        "status_source": "status.csv",
    }


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
