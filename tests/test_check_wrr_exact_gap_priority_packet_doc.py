from pathlib import Path

from scripts import check_wrr_exact_gap_priority_packet_doc as checker


def test_validate_priority_packet_doc_accepts_required_text(tmp_path: Path) -> None:
    doc = tmp_path / "packet.md"
    doc.write_text(
        "\n".join(
            [
                "# WRR Exact Gap Priority Packet",
                "Status: no-input priority packet for the exact-published WRR reproduction gap.",
                "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
                "Source-cited defined distances | 163",
                "Current defined distances | 72",
                "Remaining 163-distance gap | 91",
                "| 2 | `source_transcription_or_row_alignment` | 43 terms; 44 residual pairs; 35 frontier pairs |",
                "Full CSV includes 22 row clusters.",
                "| remaining_lane | `method_or_pair_universe_review` | 11 terms; 11 residual pairs; 2 frontier pairs |",
                "| method_pair_universe | `ocr_matched_zero_ordinary_hits` | 11 OCR-matched terms;",
                "This is an evidence-priority packet, not an exact published WRR reproduction result.",
                "Do not describe the local locked-method result as exact published reproduction.",
            ]
        ),
        encoding="utf-8",
    )

    assert checker.validate_priority_packet_doc(doc) == []


def test_validate_priority_packet_doc_rejects_forbidden_claim(tmp_path: Path) -> None:
    doc = tmp_path / "packet.md"
    doc.write_text(
        "\n".join(
            [
                "# WRR Exact Gap Priority Packet",
                "Status: no-input priority packet for the exact-published WRR reproduction gap.",
                "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
                "Source-cited defined distances | 163",
                "Current defined distances | 72",
                "Remaining 163-distance gap | 91",
                "| 2 | `source_transcription_or_row_alignment` | 43 terms; 44 residual pairs; 35 frontier pairs |",
                "Full CSV includes 22 row clusters.",
                "| remaining_lane | `method_or_pair_universe_review` | 11 terms; 11 residual pairs; 2 frontier pairs |",
                "| method_pair_universe | `ocr_matched_zero_ordinary_hits` | 11 OCR-matched terms;",
                "This is an evidence-priority packet, not an exact published WRR reproduction result.",
                "Do not describe the local locked-method result as exact published reproduction.",
                "exact published WRR reproduced",
            ]
        ),
        encoding="utf-8",
    )

    assert any(
        "forbidden phrase outside caution list" in failure
        for failure in checker.validate_priority_packet_doc(doc)
    )
