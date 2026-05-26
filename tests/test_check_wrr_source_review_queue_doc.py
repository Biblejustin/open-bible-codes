import csv
from pathlib import Path

from scripts import check_wrr_source_review_queue_doc as check


def test_current_wrr_source_review_queue_doc_passes() -> None:
    assert check.validate_source_review_queue_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_review_queue_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_queue_counts_fail(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_REVIEW_QUEUE.md"
    phrases = [
        phrase
        for phrase in check.REQUIRED_PHRASES
        if "ocr_not_matched_no_variant_lead" not in phrase
    ]
    doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    failures = check.validate_source_review_queue_doc(doc)

    assert any("ocr_not_matched_no_variant_lead" in failure for failure in failures)


def test_missing_visual_review_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_REVIEW_QUEUE.md"
    phrases = [
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase != "Visual-review notes do not exclude pairs automatically."
    ]
    doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    failures = check.validate_source_review_queue_doc(doc)

    assert any("Visual-review notes do not exclude" in failure for failure in failures)


def test_validate_source_review_queue_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_review_queue_doc(
        doc,
        queue=_queue_csv(tmp_path),
        summary=_summary_csv(tmp_path),
    )

    assert failures == []


def test_validate_source_review_queue_rejects_queue_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_review_queue_doc(
        doc,
        queue=_queue_csv(tmp_path, drop_last=True),
        summary=_summary_csv(tmp_path),
    )

    assert any("expected 97" in failure for failure in failures)


def test_validate_source_review_queue_rejects_summary_drift(tmp_path: Path) -> None:
    doc = _doc(tmp_path)

    failures = check.validate_source_review_queue_doc(
        doc,
        queue=_queue_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_bucket="ocr_not_matched_no_variant_lead"),
    )

    assert any("ocr_not_matched_no_variant_lead terms" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source-review queue doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "WRR_SOURCE_REVIEW_QUEUE.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _queue_csv(tmp_path: Path, *, drop_last: bool = False) -> Path:
    path = tmp_path / "queue.csv"
    fieldnames = [
        "run_label",
        "priority_rank",
        "review_bucket",
        "term_side",
        "term_id",
        "term",
        "row_ocr_status",
        "blocking_pairs",
        "best_variant_hit_count",
        "source_review_flags",
        "source_review_note",
        "source_review_action",
        "visual_review_note",
        "visual_review_action",
        "pair_ids",
        "read",
    ]
    rows: list[dict[str, str]] = []
    rank = 1
    for bucket, expected in check.EXPECTED_SUMMARY.items():
        terms, _, _, row_ocr_statuses = expected
        ocr_status = row_ocr_statuses.split(" ", 1)[1]
        for _ in range(int(terms)):
            rank_text = str(rank)
            term_id = f"term_{rank:02d}"
            variant_hits = "0"
            if rank_text in check.EXPECTED_TOP_RANKS:
                term_id, bucket, ocr_status, variant_hits = check.EXPECTED_TOP_RANKS[
                    rank_text
                ]
            row = {
                "run_label": "all_lanes_cap1000",
                "priority_rank": rank_text,
                "review_bucket": bucket,
                "term_side": "appellation",
                "term_id": term_id,
                "term": "TERM",
                "row_ocr_status": ocr_status,
                "blocking_pairs": "1",
                "best_variant_hit_count": variant_hits,
                "source_review_flags": "",
                "source_review_note": "",
                "source_review_action": "",
                "visual_review_note": "",
                "visual_review_action": "",
                "pair_ids": f"pair_{rank:02d}",
                "read": "read",
            }
            if rank_text in check.EXPECTED_FLAGGED_RANKS:
                expected_term, flag = check.EXPECTED_FLAGGED_RANKS[rank_text]
                row["term_id"] = expected_term
                row["source_review_flags"] = flag
                row["source_review_note"] = "note"
                row["source_review_action"] = "action"
            if rank_text in check.EXPECTED_VISUAL_RANKS:
                expected_term, action = check.EXPECTED_VISUAL_RANKS[rank_text]
                row["term_id"] = expected_term
                row["visual_review_note"] = "note"
                row["visual_review_action"] = action
            rows.append(row)
            rank += 1
    if drop_last:
        rows = rows[:-1]
    return _write_csv(path, fieldnames, rows)


def _summary_csv(tmp_path: Path, *, bad_bucket: str | None = None) -> Path:
    path = tmp_path / "summary.csv"
    fieldnames = [
        "run_label",
        "review_bucket",
        "terms",
        "blocking_pairs",
        "variant_hit_total",
        "row_ocr_statuses",
        "source_review_flags",
    ]
    rows = []
    for bucket, expected in check.EXPECTED_SUMMARY.items():
        terms, blocking_pairs, variant_hit_total, row_ocr_statuses = expected
        rows.append(
            {
                "run_label": "all_lanes_cap1000",
                "review_bucket": bucket,
                "terms": str(int(terms) + 1 if bucket == bad_bucket else terms),
                "blocking_pairs": blocking_pairs,
                "variant_hit_total": variant_hit_total,
                "row_ocr_statuses": row_ocr_statuses,
                "source_review_flags": "",
            }
        )
    return _write_csv(path, fieldnames, rows)


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
