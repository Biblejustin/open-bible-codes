import csv
import json
from pathlib import Path

from scripts import build_wrr_exact_reproduction_gap_dashboard as dashboard


def test_build_dashboard_rows_summarizes_gap_and_review_lanes(tmp_path: Path) -> None:
    args = dashboard.build_parser().parse_args(_argv(tmp_path))
    rows = dashboard.build_dashboard_rows(_inputs(), args)

    by_key = {(row["section"], row["item"]): row for row in rows}
    assert by_key[("gap", "source_cited_defined_distances")]["value"] == "163"
    assert by_key[("gap", "current_defined_distances")]["value"] == "72"
    assert by_key[("gap", "remaining_gap")]["value"] == "91"
    assert by_key[("variant_upper_bound", "residual_after_simple_variants")]["value"] == "40"
    assert by_key[("manual_locks", "manual_decision_inventory")]["value"] == (
        "37 rows; 58 action terms; 40 frontier pair links"
    )
    assert by_key[("review_lane", "source_policy_or_pair_rule_review")]["value"] == (
        "1 terms; 1 residual pairs; 1 frontier pairs"
    )
    assert by_key[("review_lane", "source_transcription_or_row_alignment")]["value"] == (
        "43 terms; 44 residual pairs; 35 frontier pairs"
    )
    assert by_key[
        ("recommended_next", "source-policy/pair-rule: wrr2_32_app_05 $LMHMX@LMA")
    ]["status"] == "no_source_change"
    assert by_key[
        (
            "recommended_next",
            "source-transcription row clusters: row 06, row 14, row 24, row 01, row 03",
        )
    ]["value"] == "organize_evidence_only"


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "dashboard.csv"
    markdown = tmp_path / "dashboard.md"
    manifest = tmp_path / "manifest.json"

    code = dashboard.main(
        [
            "--locked-report",
            str(paths["locked"]),
            "--defined-pair-summary",
            str(paths["defined"]),
            "--gap-reasons",
            str(paths["gap_reasons"]),
            "--variant-upper-bound",
            str(paths["upper_bound"]),
            "--action-summary",
            str(paths["action"]),
            "--manual-register-summary",
            str(paths["manual"]),
            "--source-policy-checklist",
            str(paths["source_policy"]),
            "--row-checklist",
            str(paths["rows"]),
            "--remaining-checklist",
            str(paths["remaining"]),
            "--out",
            str(out),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    assert out.exists()
    csv_rows = list(csv.DictReader(out.open("r", encoding="utf-8", newline="")))
    assert csv_rows[0]["section"] == "status"
    text = markdown.read_text(encoding="utf-8")
    assert "Status: exact published WRR reproduction is not closed." in text
    assert "Remaining 163-distance gap | 91" in text
    assert "| `source_policy_or_pair_rule_review` | 1 | 1 | 1 |" in text
    assert "source-transcription row clusters: row 06, row 14, row 24, row 01, row 03" in text
    assert "This dashboard is a review map, not a reproduction result." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "build_wrr_exact_reproduction_gap_dashboard"
    assert payload["dashboard_rows"] == len(csv_rows)


def _argv(tmp_path: Path) -> list[str]:
    return [
        "--locked-report",
        str(tmp_path / "locked.csv"),
        "--defined-pair-summary",
        str(tmp_path / "defined.csv"),
        "--gap-reasons",
        str(tmp_path / "gap.csv"),
        "--variant-upper-bound",
        str(tmp_path / "upper.csv"),
        "--action-summary",
        str(tmp_path / "action.csv"),
        "--manual-register-summary",
        str(tmp_path / "manual.csv"),
        "--source-policy-checklist",
        str(tmp_path / "source.csv"),
        "--row-checklist",
        str(tmp_path / "rows.csv"),
        "--remaining-checklist",
        str(tmp_path / "remaining.csv"),
    ]


def _inputs() -> dashboard.LoadedInputs:
    return dashboard.LoadedInputs(
        locked_report=[
            {"section": "status", "item": "report_status", "value": "locked_local"},
        ],
        defined_pair_summary=[
            {
                "run_label": "all_lanes_cap1000",
                "defined": "72",
                "source_cited_defined_distances": "163",
                "defined_gap_to_source_cited": "91",
                "status": "diagnostic_only_not_wrr_reproduction",
            }
        ],
        gap_reasons=[
            {
                "run_label": "all_lanes_cap1000",
                "reason": "defined",
                "pairs": "72",
                "read": "corrected distance currently defined",
            },
            {
                "run_label": "all_lanes_cap1000",
                "reason": "ordinary_missing_appellation_hits",
                "pairs": "83",
                "read": "appellation has zero ordinary hits",
            },
        ],
        variant_upper_bound=[
            {
                "run_label": "all_lanes_cap1000",
                "residual_gap_after_simple_variant_upper_bound": "40",
                "status": "diagnostic_upper_bound_not_source_correction",
                "read": "simple variants cannot close the gap",
            }
        ],
        action_summary=[
            {
                "action_lane": "source_policy_or_pair_rule_review",
                "terms": "1",
                "residual_pairs": "1",
                "frontier_pairs": "1",
                "evidence_required": "source-policy evidence",
            },
            {
                "action_lane": "source_transcription_or_row_alignment",
                "terms": "43",
                "residual_pairs": "44",
                "frontier_pairs": "35",
                "evidence_required": "row image evidence",
            },
        ],
        manual_register_summary=[
            {
                "decision_rows": "37",
                "action_terms": "58",
                "residual_pairs": "59",
                "frontier_pairs": "40",
            }
        ],
        source_policy_checklist=[
            {
                "term_id": "wrr2_32_app_05",
                "term": "$LMHMX@LMA",
                "next_manual_action": "cite source/pair-rule evidence",
            }
        ],
        row_checklist=[
            {"row_rank": "1", "row_number": "06", "frontier_pairs": "4"},
            {"row_rank": "2", "row_number": "14", "frontier_pairs": "3"},
            {"row_rank": "3", "row_number": "24", "frontier_pairs": "3"},
            {"row_rank": "4", "row_number": "01", "frontier_pairs": "2"},
            {"row_rank": "5", "row_number": "03", "frontier_pairs": "2"},
        ],
        remaining_checklist=[
            {
                "checklist_rank": "1",
                "action_lane": "page_image_near_match_review",
                "frontier_pairs": "1",
            },
            {
                "checklist_rank": "2",
                "action_lane": "method_or_pair_universe_review",
                "frontier_pairs": "1",
            },
        ],
    )


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "locked": tmp_path / "locked.csv",
        "defined": tmp_path / "defined.csv",
        "gap_reasons": tmp_path / "gap.csv",
        "upper_bound": tmp_path / "upper.csv",
        "action": tmp_path / "action.csv",
        "manual": tmp_path / "manual.csv",
        "source_policy": tmp_path / "source.csv",
        "rows": tmp_path / "rows.csv",
        "remaining": tmp_path / "remaining.csv",
    }
    inputs = _inputs()
    _write(paths["locked"], inputs.locked_report)
    _write(paths["defined"], inputs.defined_pair_summary)
    _write(paths["gap_reasons"], inputs.gap_reasons)
    _write(paths["upper_bound"], inputs.variant_upper_bound)
    _write(paths["action"], inputs.action_summary)
    _write(paths["manual"], inputs.manual_register_summary)
    _write(paths["source_policy"], inputs.source_policy_checklist)
    _write(paths["rows"], inputs.row_checklist)
    _write(paths["remaining"], inputs.remaining_checklist)
    return paths


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
