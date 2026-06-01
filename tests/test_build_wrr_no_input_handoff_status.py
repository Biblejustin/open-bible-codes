import csv
import json
from pathlib import Path

from scripts import build_wrr_no_input_handoff_status as handoff


def test_build_summary_consolidates_current_wrr_blockers() -> None:
    summary = handoff.build_summary(_inputs())

    assert summary["claim_readiness_rows"] == 4
    assert summary["claim_readiness_ready_rows"] == 4
    assert summary["claim_blocker_rows"] == 0
    assert summary["source_cited_defined_distances"] == "163"
    assert summary["current_defined_distances"] == "72"
    assert summary["remaining_gap"] == "91"
    assert summary["review_lanes"] == 4
    assert summary["residual_action_terms"] == 58
    assert summary["residual_pairs"] == 59
    assert summary["frontier_pairs"] == 40
    assert summary["manual_decision_rows"] == 37
    assert summary["manual_action_terms"] == 58
    assert summary["source_transcription_row_clusters"] == 22
    assert summary["source_transcription_action_terms"] == 43
    assert summary["page_image_terms"] == 3
    assert summary["method_pair_universe_terms"] == 11
    assert summary["wide_skip_total_hits"] == 0
    assert summary["new_result_allowed"] is False


def test_build_status_rows_keep_boundary_and_manual_inputs_visible() -> None:
    args = handoff.build_parser().parse_args([])
    summary = handoff.build_summary(_inputs())
    rows = handoff.build_status_rows(summary, _inputs(), args)

    by_id = {row["status_id"]: row for row in rows}
    assert len(rows) == 9
    assert by_id["local_claim_readiness"]["manual_input_needed"] == "no"
    assert by_id["exact_published_reproduction_gap"]["manual_input_needed"] == "yes"
    assert by_id["method_wide_skip_probe"]["current_status"] == "diagnostic_complete_no_hits"
    assert "not exact published WRR reproduction" in by_id["local_claim_readiness"]["boundary"]
    assert sum(row["manual_input_needed"] == "yes" for row in rows) == 8


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "status.csv"
    summary = tmp_path / "summary.csv"
    markdown = tmp_path / "handoff.md"
    manifest = tmp_path / "manifest.json"

    code = handoff.main(
        [
            "--claim-readiness",
            str(paths["claim_readiness"]),
            "--claim-blockers",
            str(paths["claim_blockers"]),
            "--exact-gap-summary",
            str(paths["exact_gap_summary"]),
            "--action-summary",
            str(paths["action_summary"]),
            "--row-summary",
            str(paths["row_summary"]),
            "--remaining-summary",
            str(paths["remaining_summary"]),
            "--manual-summary",
            str(paths["manual_summary"]),
            "--method-summary",
            str(paths["method_summary"]),
            "--method-wide-skip-summary",
            str(paths["method_wide_skip_summary"]),
            "--out",
            str(out),
            "--summary-out",
            str(summary),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))
    assert rows[0]["status_id"] == "local_claim_readiness"
    summary_rows = list(csv.DictReader(summary.open(encoding="utf-8", newline="")))
    assert summary_rows[0]["claim_boundary"] == handoff.CLAIM_BOUNDARY
    text = markdown.read_text(encoding="utf-8")
    assert "Status: consolidated no-input handoff." in text
    assert "Remaining gap: 91." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "scripts.build_wrr_no_input_handoff_status"
    assert payload["status_rows"] == 9


def _inputs() -> handoff.LoadedInputs:
    return handoff.LoadedInputs(
        claim_readiness=[
            {"decision_area": f"area {index}", "ready": "true"}
            for index in range(4)
        ],
        claim_blockers=[],
        exact_gap_summary=[
            {"metric": "source_cited_defined_distances", "value": "163"},
            {"metric": "current_defined_distances", "value": "72"},
            {"metric": "remaining_163_distance_gap", "value": "91"},
        ],
        action_summary=[
            _action("source_policy_or_pair_rule_review", 1, 1, 1),
            _action("source_transcription_or_row_alignment", 43, 44, 35),
            _action("page_image_near_match_review", 3, 3, 2),
            _action("method_or_pair_universe_review", 11, 11, 2),
        ],
        row_summary=[
            {
                "row_rank": str(index + 1),
                "action_terms": "2" if index < 21 else "1",
                "residual_pairs": "0",
                "frontier_pairs": "0",
            }
            for index in range(22)
        ],
        remaining_summary=[
            {
                "action_lane": "page_image_near_match_review",
                "action_terms": "3",
                "residual_pairs": "3",
                "frontier_pairs": "2",
            }
        ],
        manual_summary=[
            {
                "decision_lane": "source_policy_pair_rule",
                "decision_rows": "1",
                "action_terms": "1",
                "residual_pairs": "1",
                "frontier_pairs": "1",
            },
            {
                "decision_lane": "source_transcription_row_cluster",
                "decision_rows": "22",
                "action_terms": "43",
                "residual_pairs": "44",
                "frontier_pairs": "35",
            },
            {
                "decision_lane": "page_image_near_match",
                "decision_rows": "3",
                "action_terms": "3",
                "residual_pairs": "3",
                "frontier_pairs": "2",
            },
            {
                "decision_lane": "method_pair_universe",
                "decision_rows": "11",
                "action_terms": "11",
                "residual_pairs": "11",
                "frontier_pairs": "2",
            },
        ],
        method_summary=[
            {
                "action_terms": "11",
                "residual_pairs": "11",
                "frontier_pairs": "2",
            }
        ],
        method_wide_skip_summary=[
            {
                "max_skip": "5000",
                "total_hits_through_max": "0",
                "read": "All 11 terms remain zero.",
            }
        ],
    )


def _action(lane: str, terms: int, pairs: int, frontier: int) -> dict[str, str]:
    return {
        "action_lane": lane,
        "terms": str(terms),
        "residual_pairs": str(pairs),
        "frontier_pairs": str(frontier),
        "evidence_required": f"evidence for {lane}",
        "no_input_boundary": f"boundary for {lane}",
    }


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    inputs = _inputs()
    paths = {
        "claim_readiness": tmp_path / "claim_readiness.csv",
        "claim_blockers": tmp_path / "claim_blockers.csv",
        "exact_gap_summary": tmp_path / "exact_gap_summary.csv",
        "action_summary": tmp_path / "action_summary.csv",
        "row_summary": tmp_path / "row_summary.csv",
        "remaining_summary": tmp_path / "remaining_summary.csv",
        "manual_summary": tmp_path / "manual_summary.csv",
        "method_summary": tmp_path / "method_summary.csv",
        "method_wide_skip_summary": tmp_path / "method_wide_skip_summary.csv",
    }
    _write_csv(paths["claim_readiness"], ["decision_area", "ready"], inputs.claim_readiness)
    _write_csv(paths["claim_blockers"], ["decision_area", "ready"], inputs.claim_blockers)
    _write_csv(paths["exact_gap_summary"], ["metric", "value"], inputs.exact_gap_summary)
    _write_csv(
        paths["action_summary"],
        [
            "action_lane",
            "terms",
            "residual_pairs",
            "frontier_pairs",
            "evidence_required",
            "no_input_boundary",
        ],
        inputs.action_summary,
    )
    _write_csv(
        paths["row_summary"],
        ["row_rank", "action_terms", "residual_pairs", "frontier_pairs"],
        inputs.row_summary,
    )
    _write_csv(
        paths["remaining_summary"],
        ["action_lane", "action_terms", "residual_pairs", "frontier_pairs"],
        inputs.remaining_summary,
    )
    _write_csv(
        paths["manual_summary"],
        [
            "decision_lane",
            "decision_rows",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
        ],
        inputs.manual_summary,
    )
    _write_csv(
        paths["method_summary"],
        ["action_terms", "residual_pairs", "frontier_pairs"],
        inputs.method_summary,
    )
    _write_csv(
        paths["method_wide_skip_summary"],
        ["max_skip", "total_hits_through_max", "read"],
        inputs.method_wide_skip_summary,
    )
    return paths


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
