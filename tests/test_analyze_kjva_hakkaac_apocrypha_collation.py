import csv
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_collation as audit
from scripts.analyze_kjva_hakkaac_apocrypha_boundary_candidate import TextPayload
from scripts.analyze_kjva_hakkaac_apocrypha_marker_coverage import HakkaacBook


def test_extract_chapter_verse_text_stops_before_navigation() -> None:
    items = [
        "Sirach 19",
        "KJV",
        "▽",
        "1",
        "first verse",
        "2",
        "second verse",
        "Sirach |",
        "Old Testament",
    ]

    assert audit.extract_chapter_verse_text(items, "Sirach 19") == {
        1: "first verse",
        2: "second verse",
    }


def test_parse_hakkaac_book_normalizes_verse_text() -> None:
    book = HakkaacBook("TOB", "Tobit", "Tobit", "Tobit")
    payload = TextPayload(
        "<h3>Tobit 1</h3><span>▽</span><sup>1</sup><p>Alpha, beta!</p>".encode(
            "utf-8"
        ),
        "https://example.test/KJV_Tobit.html",
        "http_200",
    )

    records = audit.parse_hakkaac_book(book, payload, {1: 1})

    assert len(records) == 1
    assert records[0].ref == "TOB 1:1"
    assert records[0].norm_text == "alphabeta"


def test_build_verse_rows_classifies_exact_and_drift() -> None:
    local = {
        "TOB 1:1": audit.VerseRecord("TOB 1:1", "TOB", 1, 1, "abc", "abc", "local", "local_csv"),
        "TOB 1:2": audit.VerseRecord("TOB 1:2", "TOB", 1, 2, "abc", "abc", "local", "local_csv"),
    }
    hakkaac = {
        "TOB 1:1": audit.VerseRecord("TOB 1:1", "TOB", 1, 1, "abc", "abc", "url", "http_200"),
        "TOB 1:2": audit.VerseRecord("TOB 1:2", "TOB", 1, 2, "abcd", "abcd", "url", "http_200"),
    }

    rows = audit.build_verse_rows(local, hakkaac)

    assert [row["status"] for row in rows] == ["exact_normalized_match", "length_drift"]
    assert rows[1]["norm_len_delta"] == 1
    assert rows[1]["first_diff_offset"] == "3"


def test_write_private_verses_writes_text_only_to_private_path(tmp_path: Path) -> None:
    path = tmp_path / "private" / "verses.csv"
    records = {
        "TOB 1:1": audit.VerseRecord("TOB 1:1", "TOB", 1, 1, "Alpha", "alpha", "url", "http_200")
    }

    audit.write_private_verses(path, records)

    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["raw_text"] == "Alpha"
    assert rows[0]["normalized_text"] == "alpha"
