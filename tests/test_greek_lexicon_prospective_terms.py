import csv
from pathlib import Path

from els.normalization import normalize_text
from scripts import build_greek_lexicon_prospective_terms as builder


SAMPLE_XML = """<?xml version='1.0' encoding='utf-8'?>
<strongsdictionary>
  <entries>
    <entry strongs="00002">
      <strongs>2</strongs>
      <greek BETA="*)AARW/N" unicode="Ἀαρών" translit="Aarṓn" />
      <strongs_derivation>of Hebrew origin</strongs_derivation>
      <strongs_def>Aaron, the brother of Moses</strongs_def>
      <kjv_def>:--Aaron.</kjv_def>
    </entry>
    <entry strongs="00003">
      <strongs>3</strongs>
      <greek BETA="*)ABADDW/N" unicode="Ἀβαδδών" translit="Abaddṓn" />
      <strongs_derivation>of Hebrew origin</strongs_derivation>
      <strongs_def>a destroying angel</strongs_def>
      <kjv_def>:--Abaddon.</kjv_def>
    </entry>
    <entry strongs="00004">
      <strongs>4</strongs>
      <greek BETA="A)BARH/S" unicode="ἀβαρής" translit="abarḗs" />
      <strongs_derivation>from a negative particle</strongs_derivation>
      <strongs_def>weightless, i.e. not burdensome</strongs_def>
      <kjv_def>:--from being burdensome.</kjv_def>
    </entry>
    <entry strongs="00005">
      <strongs>5</strongs>
      <greek BETA="*)ABBA=" unicode="Ἀββᾶ" translit="Abbâ" />
      <strongs_derivation>of Chaldee origin</strongs_derivation>
      <strongs_def>father as a vocative</strongs_def>
    </entry>
    <entry strongs="00006">
      <strongs>6</strongs>
      <greek BETA="*)ABADDW/N" unicode="Ἀβαδδών" translit="Abaddṓn" />
      <strongs_def>duplicate normalized headword</strongs_def>
    </entry>
  </entries>
</strongsdictionary>
"""


def test_parse_strongs_greek_uses_first_greek_headword(tmp_path) -> None:
    path = tmp_path / "strongsgreek.xml"
    path.write_text(SAMPLE_XML, encoding="utf-8")

    entries = builder.parse_strongs_greek(path)

    assert [entry.strong_id for entry in entries] == ["G00002", "G00003", "G00004", "G00005", "G00006"]
    assert entries[1].term == "Ἀβαδδών"
    assert entries[1].normalized == normalize_text("Ἀβαδδών", "greek")


def test_build_terms_filters_short_and_dedupes_by_normalized_headword(tmp_path) -> None:
    path = tmp_path / "strongsgreek.xml"
    path.write_text(SAMPLE_XML, encoding="utf-8")
    entries = builder.parse_strongs_greek(path)

    rows = builder.build_terms(entries, min_normalized_length=5)

    assert [row.term_id for row in rows] == ["glex_g00002", "glex_g00003", "glex_g00004"]
    assert rows[0].category == "strongs_greek_semitic_origin"
    assert "strong_ids=G00003,G00006" in rows[1].notes


def test_write_terms_schema(tmp_path) -> None:
    out = tmp_path / "terms.csv"
    terms = [
        builder.Term(
            term_id="glex_g00003",
            concept="a destroying angel",
            category="strongs_greek_semitic_origin",
            language="greek",
            term="Ἀβαδδών",
            notes="source=test",
        )
    ]

    builder.write_terms(out, terms)

    with out.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [
        {
            "term_id": "glex_g00003",
            "concept": "a destroying angel",
            "category": "strongs_greek_semitic_origin",
            "language": "greek",
            "term": "Ἀβαδδών",
            "notes": "source=test",
        }
    ]


def test_tracked_greek_lexicon_terms_are_clean_source_rows() -> None:
    path = Path("terms/greek_lexicon_prospective_terms.csv")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    normalized = [normalize_text(row["term"], "greek") for row in rows]
    categories = {row["category"] for row in rows}

    assert len(rows) == 5038
    assert len(normalized) == len(set(normalized))
    assert all(len(value) >= builder.MIN_NORMALIZED_LENGTH for value in normalized)
    assert categories <= {"strongs_greek_lexicon", "strongs_greek_semitic_origin"}


def test_tracked_greek_lexicon_clean_lock_count() -> None:
    path = Path("terms/greek_lexicon_extension_terms_clean_lock.csv")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    normalized = [normalize_text(row["term"], "greek") for row in rows]

    assert len(rows) == 5009
    assert len(normalized) == len(set(normalized))
