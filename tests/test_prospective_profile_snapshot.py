from scripts.prospective_profile_snapshot import status_count_phrases


def test_status_count_phrases_sorts_status_counts() -> None:
    phrases = status_count_phrases(
        [
            {"status": "ready"},
            {"status": "blocked"},
            {"status": "ready"},
        ]
    )

    assert phrases == (
        "Tracked profiles: 3.",
        "`blocked`: 1.",
        "`ready`: 2.",
    )

