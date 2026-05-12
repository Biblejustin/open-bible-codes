from els.letter_stats import BigramProfile


def test_bigram_profile_flags_rare_term_bigrams() -> None:
    profile = BigramProfile.from_text("ababababababababcd")
    result = profile.classify_term("cd")

    assert result.stratum == "high_bigram_surprise"
    assert result.evidence == "cd:1"
    assert result.min_count == 1


def test_bigram_profile_flags_all_common_term_bigrams() -> None:
    profile = BigramProfile.from_text("ababababababababcd")
    result = profile.classify_term("ab")

    assert result.stratum == "low_bigram_surprise"
    assert "ab:" in result.evidence
    assert result.max_count is not None


def test_bigram_profile_has_no_stratum_for_short_terms() -> None:
    profile = BigramProfile.from_text("abababab")
    result = profile.classify_term("a")

    assert result.stratum == ""
    assert result.evidence == ""
