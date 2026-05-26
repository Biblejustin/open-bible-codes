import json
from pathlib import Path

from scripts import check_wrr_exact_gap_priority_packet_doc as checker


def _required_doc(tmp_path: Path) -> Path:
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
    return doc


def _summary_csv(tmp_path: Path, *, gap: str = "91") -> Path:
    summary = tmp_path / "summary.csv"
    summary.write_text(
        "\n".join(
            [
                "metric,value,source",
                "source_cited_defined_distances,163,dashboard.csv",
                "current_defined_distances,72,dashboard.csv",
                f"remaining_163_distance_gap,{gap},dashboard.csv",
                "review_lanes,4,actions.csv",
                "source_row_clusters,22,rows.csv",
            ]
        ),
        encoding="utf-8",
    )
    return summary


def _packet_csv(tmp_path: Path, *, include_source_policy: bool = True) -> Path:
    rows = [
        "section,priority,item,value,status,evidence_required,no_input_boundary,source,read",
        (
            "gap,1,remaining_163_distance_gap,"
            "72 current defined distances vs 163 source-cited; gap 91,"
            "exact_published_reproduction_open,evidence,"
            "keep local locked-method result separate from exact published WRR reproduction,"
            "dashboard.csv,read"
        ),
    ]
    if include_source_policy:
        rows.append(
            "review_lane,1,source_policy_or_pair_rule_review,"
            "1 terms; 1 residual pairs; 1 frontier pairs,"
            "evidence_needed_no_source_change_selected,evidence,"
            "keep term in working source; no automatic correction or exclusion without citable rule,"
            "actions.csv,read"
        )
    rows.extend(
        [
            (
                "review_lane,2,source_transcription_or_row_alignment,"
                "43 terms; 44 residual pairs; 35 frontier pairs,"
                "evidence_needed_no_source_change_selected,evidence,"
                "keep imported term; do not correct transcription until primary row evidence is locked,"
                "actions.csv,read"
            ),
            (
                "review_lane,3,page_image_near_match_review,"
                "3 terms; 3 residual pairs; 2 frontier pairs,"
                "evidence_needed_no_source_change_selected,evidence,"
                "keep imported term; do not treat near OCR as correction without page-image review,"
                "actions.csv,read"
            ),
            (
                "review_lane,4,method_or_pair_universe_review,"
                "11 terms; 11 residual pairs; 2 frontier pairs,"
                "evidence_needed_no_source_change_selected,evidence,"
                "keep source row; investigate ordinary-hit method or pair universe before source edits,"
                "actions.csv,read"
            ),
        ]
    )
    rows.extend(
        [
            (
                f"source_row_cluster,{index},row {index:02d} WRR2 {index:02d},"
                "1 action terms; 1 residual pairs; 1 frontier pairs,"
                "needs_primary_row_evidence,evidence,"
                "No automatic source correction; primary row evidence must be locked,"
                "rows.csv,read"
            )
            for index in range(1, 23)
        ]
    )
    packet = tmp_path / "packet.csv"
    packet.write_text("\n".join(rows), encoding="utf-8")
    return packet


def test_validate_priority_packet_doc_accepts_required_text(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    assert checker.validate_priority_packet_doc(doc, packet=None, summary=None) == []


def test_validate_priority_packet_doc_rejects_forbidden_claim(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)
    doc.write_text(
        doc.read_text(encoding="utf-8") + "\nexact published WRR reproduced",
        encoding="utf-8",
    )

    assert any(
        "forbidden phrase outside caution list" in failure
        for failure in checker.validate_priority_packet_doc(
            doc, packet=None, summary=None
        )
    )


def test_validate_priority_packet_doc_accepts_matching_csvs(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    assert (
        checker.validate_priority_packet_doc(
            doc,
            packet=_packet_csv(tmp_path),
            summary=_summary_csv(tmp_path),
        )
        == []
    )


def test_validate_priority_packet_doc_rejects_summary_drift(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = checker.validate_priority_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        summary=_summary_csv(tmp_path, gap="90"),
    )

    assert any("remaining_163_distance_gap" in failure for failure in failures)


def test_validate_priority_packet_doc_rejects_missing_lane(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = checker.validate_priority_packet_doc(
        doc,
        packet=_packet_csv(tmp_path, include_source_policy=False),
        summary=_summary_csv(tmp_path),
    )

    assert any(
        "missing review lane source_policy_or_pair_rule_review" in failure
        for failure in failures
    )


def test_validate_priority_packet_doc_rejects_manifest_drift(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    data = json.loads(checker.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
    data["rows"] = 99
    manifest.write_text(json.dumps(data) + "\n", encoding="utf-8")

    failures = checker.validate_priority_packet_doc(
        checker.DEFAULT_DOC,
        packet=None,
        summary=None,
        manifest=manifest,
    )

    assert any("rows drifted" in failure for failure in failures)
