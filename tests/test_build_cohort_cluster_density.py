import csv
import json
from pathlib import Path

from scripts.build_cohort_cluster_density import (
    Cohort,
    PositionedHit,
    cohort_window_rows,
    main,
    positioned_cohort_hits,
    summarize_rows,
    word_ordinal_for_row,
)


def occurrence(
    term_id: str,
    ordinal: int,
    *,
    corpus: str = "TINY",
    concept: str = "",
) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": concept or term_id.upper(),
        "corpus": corpus,
        "corpus_class": "bible",
        "center_ref": f"Test 1:{ordinal}",
        "center_word": term_id,
        "center_word_ordinal": str(ordinal),
    }


def test_word_ordinal_for_row_uses_explicit_zero() -> None:
    assert word_ordinal_for_row(occurrence("alpha", 0), word_indexes={}) == 0


def test_positioned_cohort_hits_filters_declared_terms() -> None:
    cohort = Cohort(cohort_id="demo", source=Path("terms/demo.csv"), terms={"alpha": "Alpha", "beta": "Beta"})
    rows = [occurrence("alpha", 10), occurrence("gamma", 11)]

    hits = positioned_cohort_hits(rows, cohorts=[cohort], corpora={})

    assert len(hits) == 1
    assert hits[0].cohort_id == "demo"
    assert hits[0].word_ordinal == 10


def test_cohort_window_rows_finds_distinct_terms_in_window() -> None:
    cohort = Cohort(cohort_id="demo", source=Path("terms/demo.csv"), terms={"alpha": "Alpha", "beta": "Beta"})
    hits = [
        PositionedHit(occurrence("alpha", 10), "demo", "terms/demo.csv", len(cohort.terms), 10),
        PositionedHit(occurrence("beta", 15), "demo", "terms/demo.csv", len(cohort.terms), 15),
        PositionedHit(occurrence("alpha", 100), "demo", "terms/demo.csv", len(cohort.terms), 100),
    ]

    rows = cohort_window_rows(hits, window_words=10, min_distinct_terms=2, max_windows=100)

    assert len(rows) == 1
    assert rows[0]["term_ids"] == "alpha;beta"
    assert rows[0]["cohort_full_house"] == "yes"
    assert rows[0]["strata"] == "cohort_cluster_density_window_N"


def test_summarize_rows_counts_max_distinct_terms() -> None:
    cohort = Cohort(cohort_id="demo", source=Path("terms/demo.csv"), terms={"alpha": "Alpha", "beta": "Beta"})
    hits = [
        PositionedHit(occurrence("alpha", 10), "demo", "terms/demo.csv", len(cohort.terms), 10),
        PositionedHit(occurrence("beta", 15), "demo", "terms/demo.csv", len(cohort.terms), 15),
    ]
    rows = cohort_window_rows(hits, window_words=10, min_distinct_terms=2, max_windows=100)

    summary = summarize_rows(rows)

    assert {"bucket": "cohort_id", "value": "demo", "windows": 1, "max_distinct_term_count": 2} in summary
    assert {"bucket": "corpus", "value": "TINY", "windows": 1, "max_distinct_term_count": 2} in summary


def test_main_writes_outputs(tmp_path: Path) -> None:
    occurrences = tmp_path / "occurrences.csv"
    cohort = tmp_path / "demo_terms.csv"
    out = tmp_path / "windows.csv"
    summary = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    rows = [occurrence("alpha", 10), occurrence("beta", 15)]
    with occurrences.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with cohort.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["term_id", "concept"])
        writer.writeheader()
        writer.writerow({"term_id": "alpha", "concept": "Alpha"})
        writer.writerow({"term_id": "beta", "concept": "Beta"})

    assert (
        main(
            [
                "--occurrences",
                str(occurrences),
                "--cohort",
                str(cohort),
                "--window-words",
                "10",
                "--out",
                str(out),
                "--summary-out",
                str(summary),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )

    assert "alpha;beta" in out.read_text(encoding="utf-8")
    assert "demo_terms" in summary.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["window_rows"] == 1
