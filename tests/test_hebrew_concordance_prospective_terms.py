import csv
from collections import Counter
from pathlib import Path

from els.normalization import normalize_text
from scripts import build_hebrew_concordance_prospective_terms as builder


def test_normalized_step_strong_uses_main_non_affix_ids() -> None:
    assert builder.normalized_step_strong("H0430G") == "H430"
    assert builder.normalized_step_strong("H7225G_A") == "H7225"
    assert builder.normalized_step_strong("H9003") == ""
    assert builder.normalized_step_strong("") == ""


def test_build_terms_dedupes_by_normalized_headword() -> None:
    entries = [
        builder.StrongEntry("H9", "אבדה", "אבדה", "lost thing", "n-f", "abedah", "heb"),
        builder.StrongEntry("H10", "אבדה", "אבדה", "destruction", "n-f", "abaddoh", "heb"),
        builder.StrongEntry("H20", "אבטיח", "אבטיח", "watermelon", "n-m", "abattiach", "heb"),
        builder.StrongEntry("H30", "אב", "אב", "father", "n-m", "ab", "heb"),
    ]

    rows = builder.build_terms(
        entries,
        step_counts=Counter({"H9": 2, "H10": 3, "H20": 1, "H30": 10}),
        min_normalized_length=4,
        require_step_count=True,
    )

    assert [row.term_id for row in rows] == ["hcon_h0009", "hcon_h0020"]
    assert "strong_ids=H9,H10" in rows[0].notes
    assert "step_tahot_count=5" in rows[0].notes


def test_tracked_hebrew_concordance_terms_have_expected_counts() -> None:
    path = Path("terms/hebrew_concordance_prospective_terms.csv")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    normalized = [normalize_text(row["term"], "hebrew") for row in rows]
    categories = Counter(row["category"] for row in rows)

    assert len(rows) == 3843
    assert len(normalized) == len(set(normalized))
    assert categories == {
        "strong_proper_names": 1787,
        "strong_nouns": 1725,
        "strong_adjectives": 295,
        "strong_particles_other": 21,
        "strong_verbs": 15,
    }


def test_tracked_hebrew_concordance_clean_lock_count() -> None:
    path = Path("terms/hebrew_concordance_prospective_terms_clean_lock.csv")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    normalized = [normalize_text(row["term"], "hebrew") for row in rows]

    assert len(rows) == 3577
    assert len(normalized) == len(set(normalized))


def test_hebrew_concordance_report_tracks_initial_control_state() -> None:
    text = Path("docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md").read_text(
        encoding="utf-8"
    )

    assert "| Target rows | 3577 |" in text
    assert "| Representative control target rows | 6790 |" in text
    assert "| Rows with representative controls | 3398 |" in text
    assert "87 rows only clear an uncorrected p<=0.05 screen" in text
    assert "0 rows have adjusted representative-control support" in text


def test_hebrew_concordance_uncorrected_queue_tracks_no_claim_read() -> None:
    text = Path("docs/HEBREW_CONCORDANCE_UNCORRECTED_QUEUE.md").read_text(encoding="utf-8")

    assert "| Queue rows | 87 |" in text
    assert "| Adjusted-support rows | 0 |" in text
    assert "| Shared representative q value | 0.819154 |" in text
    assert "manual-review prompts, not evidence rows" in text
    assert "`hcon_h4968`" in text
