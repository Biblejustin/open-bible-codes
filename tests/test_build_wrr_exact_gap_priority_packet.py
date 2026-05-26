import csv
import json
from pathlib import Path

from scripts import build_wrr_exact_gap_priority_packet as packet


def test_build_priority_rows_summarizes_gap_and_lanes(tmp_path: Path) -> None:
    args = packet.build_parser().parse_args(_argv(tmp_path))
    rows = packet.build_priority_rows(_inputs(), args)

    by_key = {(row["section"], row["item"]): row for row in rows}
    assert by_key[("gap", "remaining_163_distance_gap")]["value"] == (
        "72 current defined distances vs 163 source-cited; gap 91"
    )
    assert by_key[("review_lane", "source_transcription_or_row_alignment")][
        "value"
    ] == "43 terms; 44 residual pairs; 35 frontier pairs"
    assert by_key[("source_row_cluster", "row 06 WRR2 06")]["value"] == (
        "4 action terms; 4 residual pairs; 4 frontier pairs"
    )
    assert by_key[("remaining_lane", "method_or_pair_universe_review")]["value"] == (
        "11 terms; 11 residual pairs; 1 frontier pairs"
    )
    assert by_key[("method_pair_universe", "ocr_matched_zero_ordinary_hits")][
        "value"
    ] == "11 OCR-matched terms; 11 zero high-cap appellation-hit terms; 2 both-side-zero pairs"
    assert by_key[("gap_reason", "ordinary_missing_appellation_hits")]["value"] == "83"


def test_main_writes_csv_summary_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "packet.csv"
    summary = tmp_path / "summary.csv"
    markdown = tmp_path / "packet.md"
    manifest = tmp_path / "manifest.json"

    code = packet.main(
        [
            "--dashboard",
            str(paths["dashboard"]),
            "--action-summary",
            str(paths["action"]),
            "--row-summary",
            str(paths["rows"]),
            "--remaining-summary",
            str(paths["remaining"]),
            "--method-summary",
            str(paths["method"]),
            "--gap-reasons",
            str(paths["gap_reasons"]),
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
    csv_rows = list(csv.DictReader(out.open("r", encoding="utf-8", newline="")))
    assert csv_rows[0]["section"] == "gap"
    summary_rows = list(csv.DictReader(summary.open("r", encoding="utf-8", newline="")))
    assert summary_rows[2]["metric"] == "remaining_163_distance_gap"
    assert summary_rows[2]["value"] == "91"
    text = markdown.read_text(encoding="utf-8")
    assert "Status: no-input priority packet" in text
    assert "Remaining 163-distance gap | 91" in text
    assert "Full CSV includes 1 row clusters." in text
    assert "review rank is from the source-row checklist" in text
    assert "| Review rank | Row | Value | Read |" in text
    assert "not an exact published WRR reproduction result" in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "build_wrr_exact_gap_priority_packet"
    assert payload["rows"] == len(csv_rows)


def _argv(tmp_path: Path) -> list[str]:
    return [
        "--dashboard",
        str(tmp_path / "dashboard.csv"),
        "--action-summary",
        str(tmp_path / "action.csv"),
        "--row-summary",
        str(tmp_path / "rows.csv"),
        "--remaining-summary",
        str(tmp_path / "remaining.csv"),
        "--method-summary",
        str(tmp_path / "method.csv"),
        "--gap-reasons",
        str(tmp_path / "gap_reasons.csv"),
    ]


def _inputs() -> packet.LoadedInputs:
    return packet.LoadedInputs(
        dashboard=[
            {"section": "gap", "item": "source_cited_defined_distances", "value": "163"},
            {"section": "gap", "item": "current_defined_distances", "value": "72"},
            {"section": "gap", "item": "remaining_gap", "value": "91"},
        ],
        action_summary=[
            {
                "run_label": "all_lanes_cap1000",
                "action_lane": "source_transcription_or_row_alignment",
                "terms": "43",
                "residual_pairs": "44",
                "frontier_pairs": "35",
                "evidence_required": "primary table row transcription",
                "no_input_boundary": "keep imported term",
                "read": "largest residual mass",
            }
        ],
        row_summary=[
            {
                "run_label": "all_lanes_cap1000",
                "row_rank": "1",
                "row_number": "06",
                "concept": "WRR2 06",
                "action_terms": "4",
                "residual_pairs": "4",
                "frontier_pairs": "4",
                "evidence_required": "primary row evidence",
                "no_input_boundary": "no automatic source correction",
                "read": "multi-term row cluster",
            }
        ],
        remaining_summary=[
            {
                "run_label": "all_lanes_cap1000",
                "action_lane": "method_or_pair_universe_review",
                "action_terms": "11",
                "residual_pairs": "11",
                "frontier_pairs": "1",
                "evidence_required": "method or pair-universe review",
                "no_input_boundary": "no automatic method change",
                "read": "OCR matched imported term",
            }
        ],
        method_summary=[
            {
                "run_label": "all_lanes_cap1000",
                "ocr_matched_terms": "11",
                "zero_highcap_appellation_terms": "11",
                "both_sides_zero_highcap_pairs": "2",
                "read": "OCR matched all method-lane terms",
            }
        ],
        gap_reasons=[
            {
                "run_label": "all_lanes_cap1000",
                "reason": "defined",
                "pairs": "72",
                "read": "defined",
            },
            {
                "run_label": "all_lanes_cap1000",
                "reason": "ordinary_missing_appellation_hits",
                "pairs": "83",
                "read": "ordinary pair blocked",
            },
        ],
    )


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "dashboard": tmp_path / "dashboard.csv",
        "action": tmp_path / "action.csv",
        "rows": tmp_path / "rows.csv",
        "remaining": tmp_path / "remaining.csv",
        "method": tmp_path / "method.csv",
        "gap_reasons": tmp_path / "gap_reasons.csv",
    }
    inputs = _inputs()
    _write(paths["dashboard"], ["section", "item", "value"], inputs.dashboard)
    _write(
        paths["action"],
        [
            "run_label",
            "action_lane",
            "terms",
            "residual_pairs",
            "frontier_pairs",
            "evidence_required",
            "no_input_boundary",
            "read",
        ],
        inputs.action_summary,
    )
    _write(
        paths["rows"],
        [
            "run_label",
            "row_rank",
            "row_number",
            "concept",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
            "evidence_required",
            "no_input_boundary",
            "read",
        ],
        inputs.row_summary,
    )
    _write(
        paths["remaining"],
        [
            "run_label",
            "action_lane",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
            "evidence_required",
            "no_input_boundary",
            "read",
        ],
        inputs.remaining_summary,
    )
    _write(
        paths["method"],
        [
            "run_label",
            "ocr_matched_terms",
            "zero_highcap_appellation_terms",
            "both_sides_zero_highcap_pairs",
            "read",
        ],
        inputs.method_summary,
    )
    _write(paths["gap_reasons"], ["run_label", "reason", "pairs", "read"], inputs.gap_reasons)
    return paths


def _write(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
