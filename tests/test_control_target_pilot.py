import csv
from pathlib import Path

from els.protocol_runner import load_protocol
from scripts.build_control_pilot_report import build_report
from scripts.select_control_target_pilot import select_pilot_rows


def test_select_pilot_rows_forces_top_rows_then_stratifies() -> None:
    rows = [
        target_row("MT_WLC", "top1", 4, 1000, "names"),
        target_row("MT_WLC", "top2", 4, 900, "names"),
        target_row("MT_WLC", "len5", 5, 100, "nouns"),
        target_row("MT_WLC", "len6", 6, 50, "verbs"),
        target_row("UHB", "utop1", 4, 800, "names"),
        target_row("UHB", "ulen5", 5, 70, "nouns"),
        target_row("UHB", "zero", 5, 0, "nouns"),
    ]

    selected = select_pilot_rows(rows, per_corpus=3, top_per_corpus=1)

    selected_keys = {(row["corpus"], row["term_id"]) for row in selected}
    assert ("MT_WLC", "top1") in selected_keys
    assert ("UHB", "utop1") in selected_keys
    assert ("UHB", "zero") not in selected_keys
    assert sum(1 for row in selected if row["corpus"] == "MT_WLC") == 3
    assert sum(1 for row in selected if row["corpus"] == "UHB") == 2


def test_control_pilot_report_counts_rows_and_bands() -> None:
    text = build_report(
        full_targets=[target_row("MT_WLC", "a", 4, 10, "names") for _ in range(10)],
        pilot_targets=[
            target_row("MT_WLC", "a", 4, 10, "names"),
            target_row("UHB", "b", 5, 5, "nouns"),
        ],
        controls=[
            control_row("MT_WLC", "a", "paired_uncorrected_p_le_0.05", "0.02", "0.20"),
            control_row("UHB", "b", "not_unusual", "0.50", "1.0"),
        ],
        title="Pilot",
        description="Demo pilot.",
    )

    assert "| Full control target rows | 10 |" in text
    assert "| Pilot target rows | 2 |" in text
    assert "| `paired_uncorrected_p_le_0.05` | 1 |" in text
    assert "rows with uncorrected `combined_min_p_ge <= 0.05`: 1" in text


def test_hebrew_concordance_control_pilot_protocol_shape() -> None:
    protocol = load_protocol("protocols/hebrew_concordance_words_control_pilot.toml")
    step_ids = [step["id"] for step in protocol["steps"]]
    paired = protocol["steps"][1]
    report = protocol["steps"][2]

    assert protocol["name"] == "hebrew_concordance_words_control_pilot"
    assert step_ids == ["select_targets", "paired_controls", "pilot_report"]
    assert paired["argv"][paired["argv"].index("--term-shuffle-samples") + 1] == "1000"
    assert paired["argv"][paired["argv"].index("--random-samples") + 1] == "1000"
    assert "docs/HEBREW_CONCORDANCE_WORDS_CONTROL_PILOT_REPORT.md" in report["outputs"]


def test_real_pilot_target_selection_count_when_source_exists() -> None:
    path = Path("reports/hebrew_concordance_words_prospective/control_targets.csv")
    if not path.exists():
        return
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    selected = select_pilot_rows(rows, per_corpus=100, top_per_corpus=20)

    assert len(selected) == 200
    assert {row["corpus"] for row in selected} == {"MT_WLC", "UHB"}


def target_row(
    corpus: str,
    term_id: str,
    length: int,
    hits: int,
    category: str,
) -> dict[str, str]:
    return {
        "concept": term_id.title(),
        "corpus": corpus,
        "term_set": "targeted_version_presence",
        "term_id": term_id,
        "category": category,
        "term_language": "hebrew",
        "term": term_id,
        "normalized_term": term_id,
        "normalized_length": str(length),
        "hit_count": str(hits),
        "status": "counted" if hits else "absent",
    }


def control_row(
    corpus: str,
    term_id: str,
    band: str,
    p_value: str,
    q_value: str,
) -> dict[str, str]:
    row = target_row(corpus, term_id, 4, 10, "names")
    row.update(
        {
            "observed_hits": row["hit_count"],
            "term_shuffle_samples": "1000",
            "random_samples": "1000",
            "term_shuffle_p_ge": p_value,
            "random_p_ge": "0.8",
            "combined_min_p_ge": p_value,
            "combined_min_q_value": q_value,
            "paired_band": band,
            "read": "demo",
        }
    )
    return row
