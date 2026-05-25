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
    failures = check.validate_source_row_coverage_packet_doc(doc)
    assert any("No row here changes" in failure for failure in failures)
