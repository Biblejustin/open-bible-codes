from pathlib import Path

from scripts.scaffold_crd_relevance_dictionary import main


def test_scaffold_writes_blank_dictionary_entry(tmp_path: Path) -> None:
    terms = tmp_path / "terms.csv"
    terms.write_text(
        "term_id,concept,category,language,term,notes\n"
        "alpha,Alpha,demo,english,alpha,test\n",
        encoding="utf-8",
    )
    out = tmp_path / "dictionary.toml"
    queue = tmp_path / "queue.csv"

    code = main(["--term-file", str(terms), "--out", str(out), "--queue-out", str(queue)])

    assert code == 0
    assert 'term_id = "alpha"' in out.read_text(encoding="utf-8")
    assert "surface_keywords_reviewed" in queue.read_text(encoding="utf-8")

