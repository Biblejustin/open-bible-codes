import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

from pathlib import Path

from scripts import check_manual_review_queue as check


def test_current_manual_review_queue_passes() -> None:
    assert check.validate_manual_review_queue(check.DEFAULT_DOC) == []


def test_missing_guard_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "MANUAL_REVIEW_QUEUE.md"
    doc.write_text("Status: navigation aid.\n", encoding="utf-8")

    failures = check.validate_manual_review_queue(doc)

    assert any("missing guard phrase" in failure for failure in failures)


def test_missing_evidence_link_fails(tmp_path: Path) -> None:
    doc = tmp_path / "MANUAL_REVIEW_QUEUE.md"
    text = "\n".join(check.REQUIRED_PHRASES + check.REQUIRED_ROW_FAMILIES)
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_manual_review_queue(doc)

    assert any("missing evidence link" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "manual review queue failure" in capsys.readouterr().err


def test_packet_shape_matches_current_reports() -> None:
    shape, failures = check.load_review_packet_shape(check.ReviewPacketPaths())

    assert failures == []
    assert shape is not None
    assert shape.expected_doc_lines() == (
        "83 selected review rows.",
        "310 path-summary rows.",
        "1,394 letter rows.",
        "0 path mismatches.",
        "69 rows with same-skip extensions.",
        "13 rows with compound same-skip extensions.",
    )


def test_stale_packet_shape_line_fails(tmp_path: Path) -> None:
    shape, failures = check.load_review_packet_shape(check.ReviewPacketPaths())
    assert failures == []
    assert shape is not None
    doc = tmp_path / "MANUAL_REVIEW_QUEUE.md"
    evidence_links = [f"`{path}`" for path in check.REQUIRED_EVIDENCE_PATHS]
    stale_lines = list(shape.expected_doc_lines())
    stale_lines[0] = "82 selected review rows."
    text = "\n".join(
        check.REQUIRED_PHRASES
        + check.REQUIRED_ROW_FAMILIES
        + tuple(evidence_links)
        + tuple(stale_lines)
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_manual_review_queue(doc)

    assert any("missing packet-shape line: 83 selected review rows." in f for f in failures)


def test_packet_shape_detects_internal_csv_mismatch(tmp_path: Path) -> None:
    review_summary = tmp_path / "review_summary.csv"
    path_summary = tmp_path / "path_summary.csv"
    letter_paths = tmp_path / "letter_paths.csv"
    review_summary.write_text(
        "\n".join(
            (
                "path_rows,letter_rows,path_mismatch_rows,extension_rows,compound_extension",
                "2,1,0,1,True",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    path_summary.write_text("selection_rank\n1\n", encoding="utf-8")
    letter_paths.write_text("selection_rank\n1\n", encoding="utf-8")

    shape, failures = check.load_review_packet_shape(
        check.ReviewPacketPaths(review_summary, path_summary, letter_paths)
    )

    assert shape is not None
    assert any("path_rows total 2 != path_summary rows 1" in f for f in failures)
