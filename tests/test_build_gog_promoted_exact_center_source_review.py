from els.corpus import Corpus, VerseSpan, WordSpan

from scripts.build_gog_promoted_exact_center_source_review import (
    bottom_line,
    exact_center_hits_for_surface_words,
    matches_at,
    summary_row,
)


def tiny_gog_corpus() -> Corpus:
    return Corpus(
        name="tiny",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αγωγβ",
        verses=(
            VerseSpan(
                source="tiny",
                ref="REV 20:8",
                book="REV",
                chapter="20",
                verse="8",
                raw_text="α Γωγ β",
                norm_start=0,
                norm_end=4,
                norm_length=5,
            ),
        ),
        position_to_verse=[0, 0, 0, 0, 0],
        words=(
            WordSpan("tiny", "REV 20:8", "REV", "20", "8", 1, "α", "α", 0, 0, 1),
            WordSpan("tiny", "REV 20:8", "REV", "20", "8", 2, "Γωγ", "γωγ", 1, 3, 3),
            WordSpan("tiny", "REV 20:8", "REV", "20", "8", 3, "β", "β", 4, 4, 1),
        ),
        position_to_word=[0, 1, 1, 1, 2],
    )


def test_matches_at_checks_bounds_and_stride() -> None:
    assert matches_at("αγωγβ", "γωγ", 1, 1)
    assert matches_at("αγωγβ", "γωγ", 3, -1)
    assert not matches_at("αγωγβ", "γωγ", 0, 2)
    assert not matches_at("αγωγβ", "γωγ", -1, 1)


def test_exact_center_hits_for_surface_words_finds_forward_and_backward_paths() -> None:
    corpus = tiny_gog_corpus()
    surface_words = (corpus.words[1],)

    hits = exact_center_hits_for_surface_words(
        corpus,
        "γωγ",
        "γωγ",
        surface_words,
        min_skip=1,
        max_skip=2,
    )

    assert len(hits) == 2
    assert sorted(hit.skip for hit in hits) == [-1, 1]
    assert {hit.center_ref for hit in hits} == {"REV 20:8"}
    assert {hit.center_normalized_word for hit in hits} == {"γωγ"}


def test_summary_row_reports_absent_hits() -> None:
    review = type(
        "Review",
        (),
        {
            "label": "TEST",
            "config": "configs/example_sblgnt.toml",
            "letters": 5,
            "normalized_term": "γωγ",
            "max_skip": 2,
            "surface_words": (tiny_gog_corpus().words[1],),
            "hits": (),
        },
    )()

    row = summary_row(review)

    assert row["surface_word_centers"] == 1
    assert row["exact_center_paths"] == 0
    assert row["read"] == "surface term present, but no exact-center hidden path found"


def test_bottom_line_separates_contextual_occurrence_from_frequency_strength() -> None:
    review = type(
        "Review",
        (),
        {
            "label": "TEST",
            "surface_words": (tiny_gog_corpus().words[1],),
            "hits": ("hit",),
        },
    )()

    text = "\n".join(bottom_line([review]))

    assert "contextually meaningful centered-self occurrence" in text
    assert "Frequency strength must be reported separately" in text
