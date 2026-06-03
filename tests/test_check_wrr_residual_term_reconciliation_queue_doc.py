import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
from pathlib import Path

from scripts import check_wrr_residual_term_reconciliation_queue_doc as check


def test_current_wrr_residual_term_reconciliation_queue_doc_passes() -> None:
    assert check.validate_residual_term_reconciliation_queue_doc(check.DEFAULT_DOC) == []


def test_missing_wrr_residual_term_reconciliation_queue_doc_fails(
    tmp_path: Path,
) -> None:
    failures = check.validate_residual_term_reconciliation_queue_doc(
        tmp_path / "missing.md"
    )

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_incomplete_wrr_residual_term_reconciliation_queue_doc_fails(
    tmp_path: Path,
) -> None:
    doc = tmp_path / "WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md"
    doc.write_text("# WRR Residual Term Reconciliation Queue\n", encoding="utf-8")

    failures = check.validate_residual_term_reconciliation_queue_doc(doc)

    assert failures
    assert any("Unique unresolved terms" in failure for failure in failures)


def test_validate_residual_term_queue_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_residual_term_reconciliation_queue_doc(
        doc,
        queue=_queue_csv(tmp_path),
        summary=_summary_csv(tmp_path),
    )

    assert failures == []


def test_validate_residual_term_queue_rejects_queue_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_residual_term_reconciliation_queue_doc(
        doc,
        queue=_queue_csv(tmp_path, bad_need="source_transcription_or_row_alignment"),
        summary=_summary_csv(tmp_path),
    )

    assert any("source_transcription_or_row_alignment" in failure for failure in failures)


def test_validate_residual_term_queue_rejects_summary_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_residual_term_reconciliation_queue_doc(
        doc,
        queue=_queue_csv(tmp_path),
        summary=_summary_csv(
            tmp_path,
            bad_key=("source_flag", "wnp_chelm_spelling_context"),
        ),
    )

    assert any("source_flag wnp_chelm_spelling_context terms" in failure for failure in failures)


def test_validate_residual_term_queue_rejects_manifest_drift(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    payload = json.loads(check.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
    payload["term_rows"] = 99
    manifest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_residual_term_reconciliation_queue_doc(
        check.DEFAULT_DOC,
        queue=None,
        summary=None,
        manifest=manifest,
    )

    assert any("term_rows drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR residual term reconciliation doc failure" in capsys.readouterr().err


def _queue_csv(
    tmp_path: Path,
    *,
    bad_need: str | None = None,
) -> Path:
    path = tmp_path / "queue.csv"
    fieldnames = [
        "run_label",
        "priority_rank",
        "term_id",
        "term",
        "term_side",
        "residual_pairs",
        "frontier_pairs",
        "concepts",
        "impact_statuses",
        "row_ocr_pair_statuses",
        "review_buckets",
        "term_ocr_statuses",
        "source_flags",
        "source_review_action",
        "visual_review_action",
        "source_queue_rank",
        "source_queue_bucket",
        "source_queue_ocr_status",
        "source_queue_row_ocr_basis",
        "source_queue_best_variant_hits",
        "source_queue_best_variant_rule",
        "source_queue_best_variant_normalized",
        "source_queue_pair_ids",
        "pair_ids",
        "reconciliation_need",
        "read",
    ]
    rows: list[dict[str, str]] = [
        {
            "run_label": "all_lanes_cap1000",
            "priority_rank": "1",
            "term_id": check.EXPECTED_PRIORITY_ONE["term_id"],
            "term": check.EXPECTED_PRIORITY_ONE["term"],
            "term_side": check.EXPECTED_PRIORITY_ONE["term_side"],
            "residual_pairs": check.EXPECTED_PRIORITY_ONE["residual_pairs"],
            "frontier_pairs": check.EXPECTED_PRIORITY_ONE["frontier_pairs"],
            "concepts": "WRR2 32",
            "impact_statuses": "1 no_blocking_term_variant_hit",
            "row_ocr_pair_statuses": "1 mixed",
            "review_buckets": check.EXPECTED_PRIORITY_ONE["review_buckets"],
            "term_ocr_statuses": check.EXPECTED_PRIORITY_ONE["term_ocr_statuses"],
            "source_flags": check.EXPECTED_PRIORITY_ONE["source_flags"],
            "source_review_action": "source/pair-rule review",
            "visual_review_action": "",
            "source_queue_rank": "83",
            "source_queue_bucket": "ocr_not_matched_no_variant_lead",
            "source_queue_ocr_status": "not_matched",
            "source_queue_row_ocr_basis": "row",
            "source_queue_best_variant_hits": check.EXPECTED_PRIORITY_ONE[
                "source_queue_best_variant_hits"
            ],
            "source_queue_best_variant_rule": check.EXPECTED_PRIORITY_ONE[
                "source_queue_best_variant_rule"
            ],
            "source_queue_best_variant_normalized": "",
            "source_queue_pair_ids": check.EXPECTED_PRIORITY_ONE["pair_ids"],
            "pair_ids": check.EXPECTED_PRIORITY_ONE["pair_ids"],
            "reconciliation_need": check.EXPECTED_PRIORITY_ONE["reconciliation_need"],
            "read": "read",
        }
    ]
    rank = 2
    remaining = {
        need: dict(expected) for need, expected in check.EXPECTED_NEEDS.items()
    }
    remaining["source_policy_or_pair_rule_review"]["terms"] -= 1
    remaining["source_policy_or_pair_rule_review"]["residual_pairs"] -= 1
    remaining["source_policy_or_pair_rule_review"]["frontier_pairs"] -= 1
    for need, expected in remaining.items():
        terms = int(expected["terms"])
        residual_pairs = _distribute(int(expected["residual_pairs"]), terms)
        frontier_pairs = _distribute(int(expected["frontier_pairs"]), terms)
        for offset in range(terms):
            rows.append(
                {
                    "run_label": "all_lanes_cap1000",
                    "priority_rank": str(rank),
                    "term_id": f"term_{rank:02d}",
                    "term": "TERM",
                    "term_side": "appellation",
                    "residual_pairs": str(residual_pairs[offset]),
                    "frontier_pairs": str(frontier_pairs[offset]),
                    "concepts": f"WRR2 {rank:02d}",
                    "impact_statuses": "1 no_blocking_term_variant_hit",
                    "row_ocr_pair_statuses": "1 both_not_matched",
                    "review_buckets": "ocr_not_matched_no_variant_lead",
                    "term_ocr_statuses": "not_matched",
                    "source_flags": "",
                    "source_review_action": "",
                    "visual_review_action": "",
                    "source_queue_rank": str(rank),
                    "source_queue_bucket": "ocr_not_matched_no_variant_lead",
                    "source_queue_ocr_status": "not_matched",
                    "source_queue_row_ocr_basis": "row",
                    "source_queue_best_variant_hits": "0",
                    "source_queue_best_variant_rule": "none",
                    "source_queue_best_variant_normalized": "",
                    "source_queue_pair_ids": f"pair_{rank:02d}",
                    "pair_ids": f"pair_{rank:02d}",
                    "reconciliation_need": (
                        "method_or_pair_universe_review"
                        if need == bad_need
                        else need
                    ),
                    "read": "read",
                }
            )
            rank += 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _summary_csv(
    tmp_path: Path,
    *,
    bad_key: tuple[str, str] | None = None,
) -> Path:
    path = tmp_path / "summary.csv"
    fieldnames = [
        "run_label",
        "group",
        "value",
        "terms",
        "residual_pairs",
        "frontier_pairs",
        "read",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key, values in check.EXPECTED_SUMMARY.items():
            terms, residual_pairs, frontier_pairs = values
            if key == bad_key:
                terms += 1
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "group": key[0],
                    "value": key[1],
                    "terms": str(terms),
                    "residual_pairs": str(residual_pairs),
                    "frontier_pairs": str(frontier_pairs),
                    "read": "read",
                }
            )
    return path


def _distribute(total: int, count: int) -> list[int]:
    if count == 0:
        return []
    base, remainder = divmod(total, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]
