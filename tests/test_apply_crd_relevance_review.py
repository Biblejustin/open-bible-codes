from pathlib import Path

from scripts.apply_crd_relevance_review import main


def test_apply_review_queue_writes_locked_dictionary(tmp_path: Path) -> None:
    queue = tmp_path / "queue.csv"
    queue.write_text(
        "review_rank,source_file,term_id,concept,category,language,term,notes,"
        "surface_keywords_reviewed,concept_codes_reviewed,verse_refs_reviewed,"
        "book_scope_reviewed,reviewer,review_notes\n"
        "1,terms/demo.csv,alpha,Alpha,demo,english,alpha,test,"
        "alpha;aleph,alpha-code,Gen 1:1,Genesis,Justin,reviewed\n",
        encoding="utf-8",
    )
    out = tmp_path / "reviewed.toml"

    code = main(
        [
            "--queue",
            str(queue),
            "--out",
            str(out),
            "--locked-by",
            "Justin",
            "--reviewer",
            "Justin",
            "--require-reviewer",
        ]
    )

    text = out.read_text(encoding="utf-8")
    assert code == 0
    assert 'term_id = "alpha"' in text
    assert 'surface_keywords = ["alpha", "aleph"]' in text
    assert 'concept_codes = ["alpha-code"]' in text

