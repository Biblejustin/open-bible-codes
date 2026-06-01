import csv
import json

from scripts import build_kjva_next_result_gate as gate_builder
from scripts import check_kjva_next_result_gate_doc as check


def _write_csv(path, fieldnames, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _valid_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": gate_id,
            "area": "area",
            "status": (
                "rerun_only_ready"
                if gate_id == "current_rerun_reproducibility"
                else "blocked"
            ),
            "evidence_summary": "evidence",
            "required_before_result": "required",
            "next_action": "next",
            "result_boundary": "not_result_bearing",
        }
        for gate_id in check.REQUIRED_GATE_IDS
    ]


def _valid_summary() -> dict[str, object]:
    return {
        "gate_rows": "11",
        "rerun_only_ready_rows": "1",
        "blocked_rows": "10",
        "source_policy_blocker_rows": "7",
        "completed_lane_terms": "7",
        "completed_lane_observed_bridge_rows": "1",
        "completed_lane_significant_terms": "0",
        "nonbible_controls_at_or_above_observed": "1",
        "source_lock_ready": False,
        "fresh_terms_ready": False,
        "leakage_audit_ready": False,
        "fixed_controls_ready": False,
        "study_lock_ready": False,
        "result_allowed": False,
        "claim_status": "kjva_next_result_gate_blocks_new_output",
    }


def test_checker_accepts_generated_gate_doc(tmp_path) -> None:
    gates = _valid_gates()
    summary = _valid_summary()
    doc = tmp_path / "KJVA_NEXT_RESULT_GATE.md"
    gates_csv = tmp_path / "gates.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    gate_builder.write_markdown(doc, summary, gates)
    _write_csv(gates_csv, gate_builder.GATE_FIELDNAMES, gates)
    _write_csv(summary_csv, gate_builder.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "KJVA next-result gate only; no ELS result",
                "text_retention": "no Bible text written to tracked outputs",
                "summary": {"result_allowed": False},
                "outputs": {"markdown": str(doc)},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_kjva_next_result_gate_doc(
            doc,
            gates=gates_csv,
            summary=summary_csv,
            manifest=manifest,
        )
        == []
    )


def test_checker_rejects_result_allowed_overclaim(tmp_path) -> None:
    doc = tmp_path / "gate.md"
    doc.write_text(
        "# KJVA Next Result Gate\n\nThis result-bearing run is allowed.\n",
        encoding="utf-8",
    )

    failures = check.validate_kjva_next_result_gate_doc(
        doc,
        gates=None,
        summary=None,
        manifest=None,
    )

    assert any("overclaim" in failure or "missing phrase" in failure for failure in failures)
