from scripts.build_gog_magog_pair_prospective_report import report_markdown


def test_locked_rule_displays_gog_magog_with_transliteration_and_gloss() -> None:
    text = report_markdown(
        [
            {
                "corpus": "MT_WLC",
                "left_hits": "1",
                "right_hits": "1",
                "observed_pairs_within_gap": "1",
                "observed_overlap_pairs": "1",
                "observed_best_span_gap": "0",
                "term_pairs_p_ge": "1",
                "random_pairs_p_ge": "1",
                "combined_min_q": "1",
                "pair_band": "not_unusual",
                "read": "control can match or exceed target",
            }
        ],
        [],
        [],
    )

    assert "`גוג` (Gog; English: Gog) / `מגוג` (Magog; English: Magog)" in text
