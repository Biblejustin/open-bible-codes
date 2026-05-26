import csv
from pathlib import Path

from scripts import check_wrr_source_row_coverage_packet_doc as check


def test_current_wrr_source_row_coverage_packet_doc_passes() -> None:
    assert check.validate_source_row_coverage_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_coverage_packet_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_COVERAGE_PACKET.md"
    doc.write_text("# WRR Source Row Coverage Packet\n", encoding="utf-8")
    failures = check.validate_source_row_coverage_packet_doc(
        doc,
        packet=None,
        summary=None,
    )
    assert any("No row here changes" in failure for failure in failures)


def test_matching_csvs_pass(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    assert (
        check.validate_source_row_coverage_packet_doc(
            doc,
            packet=_packet_csv(tmp_path),
            summary=_summary_csv(tmp_path),
        )
        == []
    )


def test_summary_drift_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_coverage_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        summary=_summary_csv(tmp_path, action_terms="42"),
    )

    assert any("action_terms" in failure for failure in failures)


def test_packet_direct_visual_term_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_coverage_packet_doc(
        doc,
        packet=_packet_csv(tmp_path, direct_visual_rank=1),
        summary=_summary_csv(tmp_path),
    )

    assert any("has direct visual term" in failure for failure in failures)


def _required_doc(root: Path) -> Path:
    doc = root / "packet.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _summary_csv(root: Path, *, action_terms: str = "43") -> Path:
    path = root / "summary.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "read"])
        writer.writeheader()
        for metric, value in {
            **check.EXPECTED_SUMMARY,
            "action_terms": action_terms,
        }.items():
            writer.writerow({"metric": metric, "value": value, "read": "test"})
    return path


def _packet_csv(root: Path, *, direct_visual_rank: int | None = None) -> Path:
    path = root / "packet.csv"
    fieldnames = [
        "run_label",
        "row_rank",
        "row_number",
        "concept",
        "action_terms",
        "residual_pairs",
        "frontier_pairs",
        "action_term_ids",
        "direct_visual_terms",
        "related_visual_terms",
        "visual_note_count",
        "coverage_state",
        "next_manual_action",
        "no_input_boundary",
    ]
    action_counts = [4, 3, 3] + [2] * 10 + [1] * 6 + [4, 2, 1]
    frontier_counts = [4, 3, 3] + [2] * 9 + [1] * 7 + [0, 0, 0]
    related_ranks = {11, 14, 20, 21}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 23):
            action_terms = action_counts[index - 1]
            direct_terms = "covered_term" if direct_visual_rank == index else ""
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "row_rank": str(index),
                    "row_number": f"{index:02d}",
                    "concept": f"WRR2 {index:02d}",
                    "action_terms": str(action_terms),
                    "residual_pairs": str(action_terms),
                    "frontier_pairs": str(frontier_counts[index - 1]),
                    "action_term_ids": ";".join(
                        f"term_{index}_{offset}" for offset in range(action_terms)
                    ),
                    "direct_visual_terms": direct_terms,
                    "related_visual_terms": (
                        "related_a;related_b" if index in related_ranks else ""
                    ),
                    "visual_note_count": "2" if index in related_ranks else "0",
                    "coverage_state": (
                        "related_row_visual_triage_only"
                        if index in related_ranks
                        else "no_related_visual_triage"
                    ),
                    "next_manual_action": "review primary row image",
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                }
            )
    return path
