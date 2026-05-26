import csv
from pathlib import Path

from scripts import check_wrr_source_visual_review_notes_doc as check


def test_current_wrr_source_visual_review_notes_doc_passes() -> None:
    assert check.validate_source_visual_review_notes_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_visual_review_notes_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_scope_warning_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_VISUAL_REVIEW_NOTES.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:-1]) + "\n", encoding="utf-8")

    failures = check.validate_source_visual_review_notes_doc(doc)

    assert any("visual-review note excludes" in failure for failure in failures)


def test_missing_term_change_warning_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_VISUAL_REVIEW_NOTES.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase != "None of these notes authorize changing WRR terms or claiming reproduction."
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_source_visual_review_notes_doc(doc)

    assert any("authorize changing WRR terms" in failure for failure in failures)


def test_missing_visual_review_row_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_VISUAL_REVIEW_NOTES.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "| `wrr2_31_app_07` `$M$` |",
        "| `missing_31_app_07` `$M$` |",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_source_visual_review_notes_doc(doc)

    assert any("wrr2_31_app_07" in failure for failure in failures)


def test_validate_source_visual_review_notes_accepts_matching_queue(
    tmp_path: Path,
) -> None:
    failures = check.validate_source_visual_review_notes_doc(
        _doc(tmp_path),
        queue=_queue_csv(tmp_path),
    )

    assert failures == []


def test_validate_source_visual_review_notes_rejects_queue_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_source_visual_review_notes_doc(
        _doc(tmp_path),
        queue=_queue_csv(tmp_path, bad_term="wrr2_23_app_04"),
    )

    assert any("wrr2_23_app_04 visual_review_action drifted" in failure for failure in failures)


def test_validate_source_visual_review_notes_rejects_missing_visual_row(
    tmp_path: Path,
) -> None:
    failures = check.validate_source_visual_review_notes_doc(
        _doc(tmp_path),
        queue=_queue_csv(tmp_path, drop_term="wrr2_31_app_07"),
    )

    assert any("expected 10" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source visual-review notes doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "WRR_SOURCE_VISUAL_REVIEW_NOTES.md"
    lines = list(check.REQUIRED_PHRASES)
    for term_id, expected in check.EXPECTED_VISUAL_ROWS.items():
        lines.append(
            f"| `{term_id}` `{expected['term']}` | {expected['row_numbers']} | "
            f"{expected['visual_review_note']} | {expected['visual_review_action']} |"
        )
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return doc


def _queue_csv(
    tmp_path: Path,
    *,
    bad_term: str | None = None,
    drop_term: str | None = None,
) -> Path:
    path = tmp_path / "wrr_source_review_queue.csv"
    fieldnames = [
        "run_label",
        "priority_rank",
        "review_bucket",
        "term_side",
        "term_id",
        "term",
        "row_numbers",
        "row_ocr_status",
        "source_review_flags",
        "source_review_action",
        "visual_review_note",
        "visual_review_action",
    ]
    rows = []
    for term_id, expected in check.EXPECTED_VISUAL_ROWS.items():
        if term_id == drop_term:
            continue
        row = {
            "run_label": "all_lanes_cap1000",
            "priority_rank": expected["priority_rank"],
            "review_bucket": expected["review_bucket"],
            "term_side": "date" if term_id.endswith("_date_01") else "appellation",
            "term_id": term_id,
            "term": expected["term"],
            "row_numbers": expected["row_numbers"],
            "row_ocr_status": expected["row_ocr_status"],
            "source_review_flags": expected["source_review_flags"],
            "source_review_action": expected["source_review_action"],
            "visual_review_note": expected["visual_review_note"],
            "visual_review_action": expected["visual_review_action"],
        }
        if term_id == bad_term:
            row["visual_review_action"] = "changed"
        rows.append(row)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
