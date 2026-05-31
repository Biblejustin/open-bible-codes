from scripts.build_control_pilot_report import build_report


def test_build_report_summarizes_control_bands() -> None:
    full_targets = [_target_row("MT_WLC", "a", 4, 10) for _ in range(3)]
    pilot_targets = [_target_row("MT_WLC", "a", 4, 10)]
    controls = [_control_row("MT_WLC", "a", "paired_uncorrected_p_le_0.05", "0.04", "0.2")]

    text = build_report(
        full_targets=full_targets,
        pilot_targets=pilot_targets,
        controls=controls,
        title="Pilot",
        description="Demo.",
    )

    assert "| Full control target rows | 3 |" in text
    assert "| Pilot target rows | 1 |" in text
    assert "| `paired_uncorrected_p_le_0.05` | 1 |" in text


def _target_row(corpus: str, term_id: str, length: int, hits: int) -> dict[str, str]:
    return {
        "concept": term_id.title(),
        "corpus": corpus,
        "term_set": "demo",
        "term_id": term_id,
        "category": "demo",
        "term_language": "hebrew",
        "term": term_id,
        "normalized_term": term_id,
        "normalized_length": str(length),
        "hit_count": str(hits),
        "status": "counted",
    }


def _control_row(
    corpus: str,
    term_id: str,
    band: str,
    p_value: str,
    q_value: str,
) -> dict[str, str]:
    row = _target_row(corpus, term_id, 4, 10)
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

