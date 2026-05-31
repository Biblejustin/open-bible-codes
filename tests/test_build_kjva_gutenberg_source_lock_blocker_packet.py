from pathlib import Path

from scripts import build_kjva_gutenberg_source_lock_blocker_packet as packet


def test_parse_apocrypha_markers_and_spans_records_markers_without_text() -> None:
    text = "\n".join(
        [
            "The Book of Sirach (or Ecclesiasticus)",
            "",
            "1:1 first",
            "1:2 second",
            "The Prayer of Manasses",
            "",
            "unmarked prose",
            "The First Book of the Maccabees",
            "1:1 first",
        ]
    )

    markers, spans = packet.parse_apocrypha_markers_and_spans(text)

    assert [(m.chapter, m.verse, m.line) for m in markers["SIR"]] == [
        (1, 1, 3),
        (1, 2, 4),
    ]
    assert markers["MAN"] == []
    assert spans["MAN"].start_line == 5
    assert spans["MAN"].end_line == 7


def test_build_sirach_marker_diff_finds_missing_local_marker() -> None:
    source = [
        packet.MarkerRecord("SIR", 10, "chapter_verse", 44, 22),
        packet.MarkerRecord("SIR", 20, "chapter_verse", 45, 1),
    ]
    local = [
        packet.LocalMarkerRecord("SIR", "SIR 44:22", 44, 22),
        packet.LocalMarkerRecord("SIR", "SIR 44:23", 44, 23),
        packet.LocalMarkerRecord("SIR", "SIR 45:1", 45, 1),
    ]

    rows = packet.build_sirach_marker_diff(source, local)

    assert rows == [
        {
            "book": "SIR",
            "local_ref": "SIR 44:23",
            "chapter": "44",
            "verse": "23",
            "status": "missing_source_marker",
            "source_line": "",
            "previous_source_marker": "SIR 44:22@line 10",
            "next_source_marker": "SIR 45:1@line 20",
            "notes": "present in local KJVA marker list; absent from Gutenberg marker list",
        }
    ]


def test_build_boundary_options_keeps_result_boundary_closed() -> None:
    source_markers = {"SIR": [], "MAN": []}
    source_spans = {"MAN": packet.SectionSpan("MAN", 100, 120)}
    local_markers = {
        "SIR": [packet.LocalMarkerRecord("SIR", "SIR 44:23", 44, 23)],
        "MAN": [packet.LocalMarkerRecord("MAN", "MAN 1:1", 1, 1)],
    }

    rows = packet.build_boundary_options(source_markers, source_spans, local_markers)

    assert len(rows) == 5
    assert {row["book"] for row in rows} == {"SIR", "MAN"}
    assert all(row["result_boundary"] == "not_result_bearing" for row in rows)
    assert "manasseh_defer_until_citable_marked_source" in {
        row["option_id"] for row in rows
    }


def test_load_local_markers_filters_books(tmp_path: Path) -> None:
    csv_path = tmp_path / "kjva.csv"
    csv_path.write_text(
        "ref,book,chapter,verse,text\n"
        "SIR 44:23,SIR,44,23,x\n"
        "MAN 1:1,MAN,1,1,x\n"
        "GEN 1:1,GEN,1,1,x\n",
        encoding="utf-8",
    )

    rows = packet.load_local_markers(csv_path, books=("SIR", "MAN"))

    assert [row.ref for row in rows["SIR"]] == ["SIR 44:23"]
    assert [row.ref for row in rows["MAN"]] == ["MAN 1:1"]


def test_summary_keeps_blocker_packet_non_result_bearing() -> None:
    class Payload:
        status = "read_local"
        source_mode = "ignored_local_path"
        final_url = "/tmp/source.txt"
        raw = b"abc"

    summary = packet.build_summary(
        payload=Payload(),
        source_markers={"SIR": [], "MAN": []},
        source_spans={"MAN": packet.SectionSpan("MAN", 10, 12)},
        local_markers={
            "SIR": [packet.LocalMarkerRecord("SIR", "SIR 44:23", 44, 23)],
            "MAN": [packet.LocalMarkerRecord("MAN", "MAN 1:1", 1, 1)],
        },
        marker_diff=[
            {
                "book": "SIR",
                "local_ref": "SIR 44:23",
                "chapter": "44",
                "verse": "23",
                "status": "missing_source_marker",
                "source_line": "",
                "previous_source_marker": "",
                "next_source_marker": "",
                "notes": "",
            }
        ],
        boundary_options=[
            packet.option("MAN", "issue", "option", "recommended", "rec", "blocker")
        ],
    )

    assert summary["sirach_gap_refs"] == "SIR 44:23"
    assert summary["manasseh_source_markers"] == 0
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "blocker_packet_only_not_result_bearing"
