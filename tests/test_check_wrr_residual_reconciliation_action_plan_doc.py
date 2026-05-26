import csv
from pathlib import Path

from scripts import check_wrr_residual_reconciliation_action_plan_doc as check


def test_current_wrr_residual_reconciliation_action_plan_doc_passes() -> None:
    assert check.validate_residual_reconciliation_action_plan_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_residual_reconciliation_action_plan_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase
        != "keep term in working source; no automatic correction or exclusion without citable rule"
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_residual_reconciliation_action_plan_doc(doc)

    assert any("automatic correction" in failure for failure in failures)


def test_validate_action_plan_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_residual_reconciliation_action_plan_doc(
        doc,
        plan=_plan_csv(tmp_path),
        summary=_summary_csv(tmp_path),
    )

    assert failures == []


def test_validate_action_plan_rejects_plan_row_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_residual_reconciliation_action_plan_doc(
        doc,
        plan=_plan_csv(tmp_path, drop_last=True),
        summary=_summary_csv(tmp_path),
    )

    assert any("has 57 rows" in failure for failure in failures)


def test_validate_action_plan_rejects_summary_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_residual_reconciliation_action_plan_doc(
        doc,
        plan=_plan_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_lane="method_or_pair_universe_review"),
    )

    assert any("method_or_pair_universe_review terms" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR residual reconciliation action-plan failure" in capsys.readouterr().err


def _plan_csv(tmp_path: Path, *, drop_last: bool = False) -> Path:
    path = tmp_path / "plan.csv"
    fieldnames = [
        "run_label",
        "action_rank",
        "action_lane",
        "term_id",
        "term",
        "term_side",
        "residual_pairs",
        "frontier_pairs",
        "term_priority_rank",
        "review_buckets",
        "term_ocr_statuses",
        "source_flags",
        "source_queue_rank",
        "source_queue_ocr_status",
        "source_queue_best_variant_hits",
        "source_queue_best_variant_rule",
        "source_review_action",
        "visual_review_action",
        "pair_ids",
        "evidence_required",
        "no_input_boundary",
        "read",
    ]
    rows: list[dict[str, str]] = []
    rank = 1
    for lane, locks in check.LANE_LOCKS.items():
        residual_pairs = _distribute(int(locks["residual_pairs"]), int(locks["terms"]))
        frontier_pairs = _distribute(int(locks["frontier_pairs"]), int(locks["terms"]))
        for offset in range(int(locks["terms"])):
            rows.append(
                {
                    "run_label": "all_lanes_cap1000",
                    "action_rank": str(rank),
                    "action_lane": lane,
                    "term_id": f"term_{rank:02d}",
                    "term": "TERM",
                    "term_side": "appellation",
                    "residual_pairs": str(residual_pairs[offset]),
                    "frontier_pairs": str(frontier_pairs[offset]),
                    "term_priority_rank": str(rank),
                    "review_buckets": "ocr_not_matched_no_variant_lead",
                    "term_ocr_statuses": "not_matched",
                    "source_flags": "",
                    "source_queue_rank": str(rank),
                    "source_queue_ocr_status": "not_matched",
                    "source_queue_best_variant_hits": "0",
                    "source_queue_best_variant_rule": "none",
                    "source_review_action": "",
                    "visual_review_action": "",
                    "pair_ids": f"pair_{rank:02d}",
                    "evidence_required": str(locks["evidence_required"]),
                    "no_input_boundary": str(locks["no_input_boundary"]),
                    "read": "read",
                }
            )
            rank += 1
    if drop_last:
        rows = rows[:-1]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _summary_csv(tmp_path: Path, *, bad_lane: str | None = None) -> Path:
    path = tmp_path / "summary.csv"
    fieldnames = [
        "run_label",
        "action_lane",
        "terms",
        "residual_pairs",
        "frontier_pairs",
        "evidence_required",
        "no_input_boundary",
        "read",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for lane, locks in check.LANE_LOCKS.items():
            terms = int(locks["terms"]) + (1 if lane == bad_lane else 0)
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "action_lane": lane,
                    "terms": str(terms),
                    "residual_pairs": str(locks["residual_pairs"]),
                    "frontier_pairs": str(locks["frontier_pairs"]),
                    "evidence_required": str(locks["evidence_required"]),
                    "no_input_boundary": str(locks["no_input_boundary"]),
                    "read": "read",
                }
            )
    return path


def _distribute(total: int, count: int) -> list[int]:
    base, remainder = divmod(total, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]
