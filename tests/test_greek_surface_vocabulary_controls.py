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


def corpus_with_words(*words: str):
    return SimpleNamespace(
        words=tuple(
            SimpleNamespace(normalized_word=word, ref=f"R{index}")
            for index, word in enumerate(words, start=1)
        )
    )
