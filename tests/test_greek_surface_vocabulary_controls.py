from types import SimpleNamespace

from scripts import build_greek_surface_vocabulary_controls as vocab


def test_selected_target_rows_keep_source_metadata() -> None:
    rows = vocab.selected_target_rows(
        [
            {
                "term_id": "amen_g",
                "concept": "Amen",
                "category": "liturgical",
                "language": "greek",
                "term": "ἀμήν",
                "notes": "source note",
            }
        ],
        [{"term_id": "amen_g"}],
    )

    assert rows == [
        {
            "term_id": "amen_g",
            "concept": "Amen",
            "category": "liturgical",
            "language": "greek",
            "term": "ἀμήν",
            "notes": "source note; selected length-4 target retained for vocabulary-control run",
        }
    ]


def test_vocabulary_control_rows_require_source_presence_and_exclude_targets() -> None:
    corpora = {
        "A": corpus_with_words("ψυχη", "αμην", "μονο"),
        "B": corpus_with_words("ψυχη", "αμην"),
        "C": corpus_with_words("ψυχη", "αμην"),
        "D": corpus_with_words("ψυχη", "αμην"),
    }

    rows, summary = vocab.vocabulary_control_rows(
        corpora,
        [
            {
                "term_id": "amen_g",
                "concept": "Amen",
                "category": "liturgical",
                "language": "greek",
                "term": "αμην",
                "notes": "",
            }
        ],
        min_length=4,
        max_length=4,
        min_sources=4,
    )

    assert [row["term"] for row in rows] == ["ψυχη"]
    assert rows[0]["language"] == "greek"
    assert rows[0]["category"].startswith("surface_vocabulary_control_")
    assert summary["control_terms"] == 1


def test_write_markdown_displays_original_language_terms(tmp_path) -> None:
    path = tmp_path / "vocab.md"
    vocab.write_markdown(
        path,
        [
            {
                "term_id": "amen_g",
                "concept": "Amen",
                "category": "liturgical",
                "language": "greek",
                "term": "ἀμήν",
                "notes": "",
            }
        ],
        [
            {
                "term_id": "control_g",
                "concept": "Soul",
                "category": "surface_vocabulary_control",
                "language": "greek",
                "term": "ψυχη",
                "notes": "generated",
            }
        ],
        {"unique_normalized_words": 1},
        SimpleNamespace(
            source_terms="terms.csv",
            selected="selected.csv",
            out="out.csv",
            min_length=4,
            max_length=4,
            min_sources=4,
        ),
    )

    text = path.read_text(encoding="utf-8")
    assert "`αμην` (amen; English: Amen)" in text
    assert "`ψυχη` (psuche; English: Soul)" in text


def corpus_with_words(*words: str):
    return SimpleNamespace(
        words=tuple(
            SimpleNamespace(normalized_word=word, ref=f"R{index}")
            for index, word in enumerate(words, start=1)
        )
    )
