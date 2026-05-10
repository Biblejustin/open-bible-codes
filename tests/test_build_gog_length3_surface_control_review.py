from els.corpus import Corpus, VerseSpan, WordSpan
from scripts.build_gog_length3_surface_control_review import (
    SourceResult,
    TermResult,
    matched_surface_terms,
    read_lines,
    summary_table,
    summary_rows_for_results,
)


def corpus_with_words(words: list[str]) -> Corpus:
    text = "".join(words)
    corpus_words = []
    position_to_word = []
    offset = 0
    for index, word in enumerate(words):
        corpus_words.append(
            WordSpan(
                source="tiny",
                ref=f"REF {index + 1}",
                book="REF",
                chapter=str(index + 1),
                verse="1",
                word_index=1,
                raw_word=word,
                normalized_word=word,
                norm_start=offset,
                norm_end=offset + len(word) - 1,
                norm_length=len(word),
            )
        )
        position_to_word.extend([index] * len(word))
        offset += len(word)
    return Corpus(
        name="tiny",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(
            VerseSpan(
                source="tiny",
                ref="REF 1",
                book="REF",
                chapter="1",
                verse="1",
                raw_text=" ".join(words),
                norm_start=0,
                norm_end=len(text) - 1,
                norm_length=len(text),
            ),
        ),
        position_to_verse=[0] * len(text),
        words=tuple(corpus_words),
        position_to_word=position_to_word,
    )


def test_matched_surface_terms_requires_length_and_occurrence_count_in_all_sources() -> None:
    corpora = {
        "A": corpus_with_words(["γωγ", "abc", "abc", "δεζ"]),
        "B": corpus_with_words(["γωγ", "abc", "δεζ"]),
    }

    terms = matched_surface_terms(corpora, length=3, occurrences_per_source=1)

    assert terms == ["γωγ", "δεζ"]


def test_summary_rows_rank_target_lowest_against_controls() -> None:
    results = [
        TermResult(
            term="aaa",
            is_target=False,
            sources=(
                SourceResult("A", 10, 1, ("h1", "h2")),
                SourceResult("B", 10, 1, ("h3",)),
            ),
        ),
        TermResult(
            term="γωγ",
            is_target=True,
            sources=(
                SourceResult("A", 10, 1, ("h1",)),
                SourceResult("B", 10, 1, ()),
            ),
        ),
    ]

    rows = summary_rows_for_results(results, target="γωγ")
    by_term = {row["term"]: row for row in rows}

    assert [row["term"] for row in rows] == ["aaa", "γωγ"]
    assert by_term["γωγ"]["total_exact_center_paths"] == 1
    assert by_term["γωγ"]["rank_desc"] == 2
    assert by_term["γωγ"]["rank_asc"] == 1
    assert by_term["γωγ"]["controls_gt_target"] == 1
    assert by_term["aaa"]["read"] == "matched control exceeds target"


def test_read_lines_preserve_contextual_occurrence_despite_frequency_caution() -> None:
    text = "\n".join(read_lines())

    assert "contextual finding to preserve" in text
    assert "frequency caution" in text


def test_summary_table_displays_original_language_terms() -> None:
    lines = summary_table(
        [
            {
                "rank_desc": 1,
                "rank_asc": 1,
                "term": "γωγ",
                "is_target": True,
                "total_exact_center_paths": 14,
                "source_counts": "TR_NT:2",
                "read": "target term",
            }
        ]
    )

    assert "`γωγ` (Gog; English: Gog)" in "\n".join(lines)
