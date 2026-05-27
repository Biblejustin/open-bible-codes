import csv
import json
from pathlib import Path

from scripts import check_wrr_claim_blocker_packet_doc as check


def test_current_wrr_claim_blocker_packet_doc_passes() -> None:
    assert check.validate_blocker_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_blocker_packet_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_no_input_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_BLOCKER_PACKET.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_blocker_packet_doc(doc)

    assert any("no current claim-readiness blockers" in failure for failure in failures)


def test_missing_visual_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_BLOCKER_PACKET.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase
        != "No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change."
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_blocker_packet_doc(doc)

    assert any("visual-review note excludes" in failure for failure in failures)


def test_validate_blocker_packet_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_blocker_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        readiness=_readiness_csv(tmp_path),
        source_queue=_source_queue_csv(tmp_path),
        variant_residual_summary=_variant_summary_csv(tmp_path),
        residual_term_summary=_residual_term_summary_csv(tmp_path),
        source_transcription_row_summary=_row_summary_csv(tmp_path),
        remaining_lane_summary=_remaining_lane_summary_csv(tmp_path),
    )

    assert failures == []


def test_validate_blocker_packet_rejects_packet_rows(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_blocker_packet_doc(
        doc,
        packet=_packet_csv(tmp_path, add_blocker=True),
        readiness=_readiness_csv(tmp_path),
        source_queue=_source_queue_csv(tmp_path),
        variant_residual_summary=_variant_summary_csv(tmp_path),
        residual_term_summary=_residual_term_summary_csv(tmp_path),
        source_transcription_row_summary=_row_summary_csv(tmp_path),
        remaining_lane_summary=_remaining_lane_summary_csv(tmp_path),
    )

    assert any("expected 0 ready-state blockers" in failure for failure in failures)


def test_validate_blocker_packet_rejects_readiness_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_blocker_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        readiness=_readiness_csv(tmp_path, bad_area="Pair universe"),
        source_queue=_source_queue_csv(tmp_path),
        variant_residual_summary=_variant_summary_csv(tmp_path),
        residual_term_summary=_residual_term_summary_csv(tmp_path),
        source_transcription_row_summary=_row_summary_csv(tmp_path),
        remaining_lane_summary=_remaining_lane_summary_csv(tmp_path),
    )

    assert any("Pair universe no longer ready" in failure for failure in failures)


def test_validate_blocker_packet_rejects_source_queue_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_blocker_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        readiness=_readiness_csv(tmp_path),
        source_queue=_source_queue_csv(tmp_path, bad_flags=True),
        variant_residual_summary=_variant_summary_csv(tmp_path),
        residual_term_summary=_residual_term_summary_csv(tmp_path),
        source_transcription_row_summary=_row_summary_csv(tmp_path),
        remaining_lane_summary=_remaining_lane_summary_csv(tmp_path),
    )

    assert any("source review flag counts drifted" in failure for failure in failures)


def test_validate_blocker_packet_rejects_summary_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_blocker_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        readiness=_readiness_csv(tmp_path),
        source_queue=_source_queue_csv(tmp_path),
        variant_residual_summary=_variant_summary_csv(
            tmp_path,
            bad_key=("review_frontier", "minimum_residual_frontier"),
        ),
        residual_term_summary=_residual_term_summary_csv(tmp_path),
        source_transcription_row_summary=_row_summary_csv(tmp_path),
        remaining_lane_summary=_remaining_lane_summary_csv(tmp_path),
    )

    assert any("review_frontier minimum_residual_frontier" in failure for failure in failures)


def test_validate_blocker_packet_rejects_manifest_drift(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    payload = json.loads(check.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
    payload["blocker_rows"] = 99
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_blocker_packet_doc(
        check.DEFAULT_DOC,
        packet=None,
        readiness=None,
        source_queue=None,
        variant_residual_summary=None,
        residual_term_summary=None,
        source_transcription_row_summary=None,
        remaining_lane_summary=None,
        manifest=manifest,
    )

    assert any("blocker_rows drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR claim-blocker packet failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    path = tmp_path / "WRR_CLAIM_BLOCKER_PACKET.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return path


def _packet_csv(tmp_path: Path, *, add_blocker: bool = False) -> Path:
    rows = []
    if add_blocker:
        rows.append({field: "x" for field in check.PACKET_FIELDNAMES})
    return _write_csv(tmp_path / "packet.csv", check.PACKET_FIELDNAMES, rows)


def _readiness_csv(tmp_path: Path, *, bad_area: str | None = None) -> Path:
    rows = []
    for area, status in check.EXPECTED_READINESS.items():
        rows.append(
            {
                "decision_area": area,
                "status": status,
                "required_statuses": "required",
                "ready": "false" if area == bad_area else "true",
                "current_read": "read",
                "evidence": "evidence",
                "blocker": "",
            }
        )
    return _write_csv(
        tmp_path / "readiness.csv",
        [
            "decision_area",
            "status",
            "required_statuses",
            "ready",
            "current_read",
            "evidence",
            "blocker",
        ],
        rows,
    )


def _source_queue_csv(tmp_path: Path, *, bad_flags: bool = False) -> Path:
    by_rank: dict[str, dict[str, str]] = {}
    for rank, (term_id, flag) in check.EXPECTED_FLAGGED_TERMS.items():
        by_rank[rank] = {
            "priority_rank": rank,
            "term_id": term_id,
            "source_review_flags": "" if bad_flags and rank == "83" else flag,
            "source_review_action": "action",
            "visual_review_note": "",
            "visual_review_action": "",
        }
    for rank, (term_id, action) in check.EXPECTED_VISUAL_TERMS.items():
        row = by_rank.setdefault(
            rank,
            {
                "priority_rank": rank,
                "term_id": term_id,
                "source_review_flags": "",
                "source_review_action": "",
                "visual_review_note": "",
                "visual_review_action": "",
            },
        )
        row["term_id"] = term_id
        row["visual_review_note"] = "note"
        row["visual_review_action"] = action
    rows = [by_rank[rank] for rank in sorted(by_rank, key=int)]
    return _write_csv(
        tmp_path / "source_queue.csv",
        [
            "priority_rank",
            "term_id",
            "source_review_flags",
            "source_review_action",
            "visual_review_note",
            "visual_review_action",
        ],
        rows,
    )


def _variant_summary_csv(
    tmp_path: Path,
    *,
    bad_key: tuple[str, str] | None = None,
) -> Path:
    rows = []
    for key, pairs in check.EXPECTED_VARIANT_RESIDUAL.items():
        rows.append(
            {
                "run_label": "all_lanes_cap1000",
                "group": key[0],
                "value": key[1],
                "pairs": str(int(pairs) + 1 if key == bad_key else pairs),
                "residual_needed": "40",
                "candidate_pool_pairs": "59",
                "residual_slack_pairs": "19",
                "read": "read",
            }
        )
    return _write_csv(
        tmp_path / "variant_summary.csv",
        [
            "run_label",
            "group",
            "value",
            "pairs",
            "residual_needed",
            "candidate_pool_pairs",
            "residual_slack_pairs",
            "read",
        ],
        rows,
    )


def _residual_term_summary_csv(tmp_path: Path) -> Path:
    rows = []
    for key, values in check.EXPECTED_RESIDUAL_TERM_SUMMARY.items():
        terms, residual_pairs, frontier_pairs = values
        rows.append(
            {
                "run_label": "all_lanes_cap1000",
                "group": key[0],
                "value": key[1],
                "terms": terms,
                "residual_pairs": residual_pairs,
                "frontier_pairs": frontier_pairs,
                "read": "read",
            }
        )
    return _write_csv(
        tmp_path / "residual_term_summary.csv",
        [
            "run_label",
            "group",
            "value",
            "terms",
            "residual_pairs",
            "frontier_pairs",
            "read",
        ],
        rows,
    )


def _row_summary_csv(tmp_path: Path) -> Path:
    rows = [
        {
            "run_label": "all_lanes_cap1000",
            "row_rank": "1",
            "row_number": "06",
            "concept": "WRR2 06",
            "action_terms": "4",
            "residual_pairs": "4",
            "frontier_pairs": "4",
        }
    ]
    action_terms = _distribute(39, 21)
    residual_pairs = _distribute(40, 21)
    frontier_pairs = _distribute(31, 21)
    for index in range(21):
        rank = index + 2
        rows.append(
            {
                "run_label": "all_lanes_cap1000",
                "row_rank": str(rank),
                "row_number": f"{rank:02d}",
                "concept": f"WRR2 {rank:02d}",
                "action_terms": str(action_terms[index]),
                "residual_pairs": str(residual_pairs[index]),
                "frontier_pairs": str(frontier_pairs[index]),
            }
        )
    return _write_csv(
        tmp_path / "row_summary.csv",
        [
            "run_label",
            "row_rank",
            "row_number",
            "concept",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
        ],
        rows,
    )


def _remaining_lane_summary_csv(tmp_path: Path) -> Path:
    rows = []
    for lane, values in check.EXPECTED_REMAINING_LANES.items():
        action_terms, residual_pairs, frontier_pairs = values
        rows.append(
            {
                "run_label": "all_lanes_cap1000",
                "action_lane": lane,
                "action_terms": action_terms,
                "residual_pairs": residual_pairs,
                "frontier_pairs": frontier_pairs,
                "concepts": "1",
                "evidence_required": "evidence",
                "no_input_boundary": "boundary",
                "read": "read",
            }
        )
    return _write_csv(
        tmp_path / "remaining_lane_summary.csv",
        [
            "run_label",
            "action_lane",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
            "concepts",
            "evidence_required",
            "no_input_boundary",
            "read",
        ],
        rows,
    )


def _write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> Path:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _distribute(total: int, count: int) -> list[int]:
    base, remainder = divmod(total, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]
