# Protocol Index

Protocols root: `protocols`
Protocols indexed: 95

## Analysis

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| boundary_alignment | Summarize ELS start/end verse, chapter, and book boundary flags from the match-strata i... | 1 |  | reports/boundary_alignment | `boundary_alignment.toml` |
| canonical_first_summary | Summarize canonical-first centered occurrences from the match-strata index. | 1 |  | reports/canonical_first_summary | `canonical_first_summary.toml` |
| chapter_position_bias | Summarize first/last chapter and book center-verse flags from the match-strata index. | 1 |  | reports/chapter_position_bias | `chapter_position_bias.toml` |
| cross_skip_summary | Summarize cross-skip pair strata from the match-strata index. | 1 |  | reports/cross_skip_summary | `cross_skip_summary.toml` |
| direction_asymmetry | Summarize forward/backward direction strata from the match-strata index. | 1 |  | reports/direction_asymmetry | `direction_asymmetry.toml` |
| greek_exact_center_cohort | Locked Greek theological exact-center cross-text extension cohort. | 8 | terms/greek_exact_center_cohort_terms.csv | reports/greek_exact_center_cohort | `greek_exact_center_cohort.toml` |
| greek_exact_center_four_source | Locked Greek exact-center extension cohort with added text-critical Greek NT source. | 12 | terms/greek_exact_center_cohort_terms.csv | reports/greek_exact_center_four_source | `greek_exact_center_four_source.toml` |
| greek_exact_center_three_source | Locked Greek exact-center extension cohort with independent Byzantine NT source. | 10 | terms/greek_exact_center_cohort_terms.csv | reports/greek_exact_center_three_source | `greek_exact_center_three_source.toml` |
| greek_expanded_surface_triage | Post-screen triage for expanded Greek exact-center surface rows. | 1 | terms/greek_expanded_prospective_terms.csv | reports/greek_expanded_surface_triage | `greek_expanded_surface_triage.toml` |
| greek_nt_claim_version_presence | Capped exact ELS hit-pattern presence for Greek NT claim terms across Greek NT corpora. | 1 | terms/greek_nt_claim_terms.csv | reports/greek_nt_claim_version_presence | `greek_nt_claim_version_presence.toml` |
| hebrew_claim_version_presence | Capped exact ELS hit-pattern presence for declared Hebrew claim terms across MT-family ... | 1 | terms/hebrew_claim_terms.csv | reports/hebrew_claim_version_presence | `hebrew_claim_version_presence.toml` |
| hebrew_hit_version_presence | Capped exact ELS hit-pattern presence across Hebrew MT-family corpora. | 1 | terms/modern_names_dates.csv | reports/hebrew_hit_version_presence | `hebrew_hit_version_presence.toml` |
| hebrew_modern_geopolitical_version_presence | Broad Hebrew modern/geopolitical/local/date exact ELS hit-pattern presence across MT-fa... | 1 | terms/modern_names_dates.csv | reports/hebrew_modern_geopolitical_version_presence | `hebrew_modern_geopolitical_version_presence.toml` |
| hebrew_theology_all_codes_collection | Relaxed all-codes collection for the Hebrew theology cohort with center-word surface fl... | 3 | terms/hebrew_theology_prospective_terms.csv | reports/hebrew_theology_all_codes | `hebrew_theology_all_codes_collection.toml` |
| local_terms_appendix | Negative/curiosity appendix for fixed local pastor-business and church-location terms. | 5 | terms/local_terms_appendix.csv | reports/local_terms_appendix | `local_terms_appendix.toml` |
| match_strata_index | Annotate centered occurrences with extended post-search strata that do not widen search... | 1 | terms/meaningful_constants.csv | reports/match_strata_index | `match_strata_index.toml` |
| modern_focus_extensions | Capped same-skip extension screen for modern names, places, and local terms. | 11 | terms/modern_names_dates.csv | reports/modern_extension_screen | `modern_focus_extensions.toml` |
| mt_version_comparison | Compare normalized Hebrew MT-family verse text across MT_WLC, UXLC, MAM, eBible WLC, an... | 1 |  | reports/mt_version_comparison | `mt_version_comparison.toml` |
| notable_passage_gaps | Record declared notable passages where selected ELS terms are absent, sparse, or presen... | 1 | terms/notable_passage_gap_terms.csv | reports/notable_passage_gaps | `notable_passage_gaps.toml` |
| review_flag_summary | Summarize meaningful-skip and rarity review flags from the match-strata index. | 1 |  | reports/review_flag_summary | `review_flag_summary.toml` |
| step_tahot_version_presence | Run focused modern/local exact-hit version presence with STEP_TAHOT included as a separ... | 2 | terms/modern_names_dates.csv | reports/step_tahot_version_presence | `step_tahot_version_presence.toml` |
| thematic_chapter_absence | Run term-absence checks over locked thematic chapter mappings only. | 1 |  | reports/thematic_chapter_absence | `thematic_chapter_absence.toml` |
| version_presence_extensions | Same-skip extension screen for bounded all-source version-presence hit queues. | 10 |  | reports/version_presence_extensions | `version_presence_extensions.toml` |
| wide_focus_exact_presence | Capped exact-hit version-presence review for the focused wide-search terms. | 2 | terms/modern_names_dates.csv, terms/prophetic_terms.csv | reports/wide_focus_exact_presence | `wide_focus_exact_presence.toml` |

## Audit

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| churchages_statistics_audit | Compare published ChurchAges observed KJV ELS counts against letter-frequency expected ... | 1 |  | reports/churchages_statistics | `churchages_statistics_audit.toml` |
| cohort_cluster_density_audit | Post-process centered occurrences for declared-cohort word-window density candidates. | 1 | terms/biblical_tribes.csv | reports/cohort_cluster_density | `cohort_cluster_density_audit.toml` |
| greek_expanded_surface_letter_paths | Letter-path audit sheet for tightened Greek exact-center surface rows. | 1 |  | reports/greek_expanded_surface_letter_paths | `greek_expanded_surface_letter_paths.toml` |
| hebrew_albam_audit | Opt-in Hebrew ALBAM transformed-text ELS audit for declared Jeremiah cryptogram terms. | 9 | terms/hebrew_atbash_audit_terms.csv | reports/hebrew_albam_audit | `hebrew_albam_audit.toml` |
| hebrew_atbash_audit | Opt-in Hebrew Atbash transformed-text ELS audit for declared Jeremiah cryptogram terms. | 9 | terms/hebrew_atbash_audit_terms.csv | reports/hebrew_atbash_audit | `hebrew_atbash_audit.toml` |
| step_tahot_policy_hits | Audit STEP_TAHOT-only exact-hit rows against TAHOT source-type policy. | 2 |  | reports/step_tahot_policy_hits, reports/step_tahot_screening_version_presence | `step_tahot_policy_hits.toml` |
| step_tahot_source_audit | Download STEP TAHOT and compare it against current Hebrew MT-family corpora. | 2 |  | reports/mt_version_comparison_step_tahot | `step_tahot_source_audit.toml` |
| word_edge_pattern_audit | Opt-in consecutive-word acrostic and telestic audit for declared Hebrew word-edge terms. | 9 | terms/word_edge_pattern_audit_terms.csv | reports/word_edge_patterns | `word_edge_pattern_audit.toml` |
| word_skip_term_audit | Opt-in full word-token every-Kth-word audit for declared Hebrew phrases. | 9 | terms/word_skip_term_audit_terms.csv | reports/word_skip_terms | `word_skip_term_audit.toml` |

## Baseline

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| public_baseline | Public-source baseline for MT WLC, LXX GRCLXX, TR GRCTR, and SBLGNT. | 30 | terms/modern_names_dates.csv, terms/prophetic_terms.csv, terms/table_of_nations.csv, te... | reports, reports/protocols/public_baseline | `public_baseline.toml` |

## Controls

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| all_codes_compound_extension_confirmatory | Locked 5000/5000 post-discovery confirmatory controls for the selected all-codes יום יה... | 1 |  | reports/all_codes_compound_extension_confirmatory | `all_codes_compound_extension_confirmatory.toml` |
| all_codes_compound_extension_controls | Post-screen paired controls for selected all-codes compound same-skip extensions. | 1 |  | reports/all_codes_compound_extension_controls | `all_codes_compound_extension_controls.toml` |
| apocrypha_bridge_shuffled_controls_100 | Run 100-sample shuffled apocrypha/deuterocanon bridge controls for LXX and KJVA bridge ... | 2 | terms/english_search_terms.csv, terms/greek_nt_claim_terms.csv, terms/prophetic_terms.c... | reports/apocrypha_bridge_shuffled_controls_100, reports/kjv_apocrypha_bridge_shuffled_c... | `apocrypha_bridge_shuffled_controls_100.toml` |
| apocrypha_bridge_shuffled_controls_50 | Run 50-sample shuffled apocrypha/deuterocanon bridge controls for LXX and KJVA bridge c... | 2 | terms/english_search_terms.csv, terms/greek_nt_claim_terms.csv, terms/prophetic_terms.c... | reports/apocrypha_bridge_shuffled_controls_50, reports/kjv_apocrypha_bridge_shuffled_co... | `apocrypha_bridge_shuffled_controls_50.toml` |
| apocrypha_bridge_study | Run the apocrypha/deuterocanon coverage audit, bounded bridge scan, surface-context rev... | 14 | terms/english_search_terms.csv, terms/greek_nt_claim_terms.csv, terms/prophetic_terms.c... | reports/apocrypha_bridge_candidates, reports/apocrypha_bridge_completion_review, report... | `apocrypha_bridge_study.toml` |
| byz_source_only_exact_center | Post-discovery 1000/1000 controls for BYZ_NT source-only exact-center extension row. | 2 |  | reports/byz_source_only_exact_center | `byz_source_only_exact_center.toml` |
| extension_deep_controls | Slow 1000/1000 paired-control follow-up for the exact-center cross-text Greek NT extens... | 1 |  | reports | `extension_deep_controls.toml` |
| external_claim_source_all_codes_collection | Relaxed all-codes collection for external-source claim and critique term lists across B... | 4 | terms/bible_and_science_codes_terms.csv, terms/bible_code_digest_claim_terms.csv, terms... | reports/external_claim_source_all_codes | `external_claim_source_all_codes_collection.toml` |
| external_claim_source_counts | Count external-source claim and critique term lists across Bible corpora and language-m... | 2 | terms/bible_and_science_codes_terms.csv, terms/bible_code_digest_claim_terms.csv, terms... | reports/external_claim_source_counts | `external_claim_source_counts.toml` |
| greek_control_version_presence | Capped exact ELS hit-pattern presence for Greek null and frequency controls across Gree... | 1 | terms/frequency_anchors.csv, terms/null_controls.csv | reports/greek_control_version_presence | `greek_control_version_presence.toml` |
| greek_exact_center_final_gate | Consolidate Greek exact-center version presence, controls, context, and synthetic basel... | 1 |  | reports/greek_exact_center_final_gate | `greek_exact_center_final_gate.toml` |
| greek_expanded_surface_available_control_evaluation | Exploratory all-available real-word matched-control evaluation for tightened Greek surf... | 2 | terms/greek_expanded_prospective_terms.csv | reports/greek_expanded_surface_available_control_evaluation, reports/greek_expanded_sur... | `greek_expanded_surface_available_control_evaluation.toml` |
| greek_expanded_surface_control_evaluation | Exploratory matched-control evaluation for tightened Greek surface rows. | 1 |  | reports/greek_expanded_surface_control_evaluation | `greek_expanded_surface_control_evaluation.toml` |
| greek_expanded_surface_control_pool | Real-word surface-frequency control pool for tightened expanded Greek surface rows. | 1 | terms/greek_expanded_prospective_terms.csv | reports/greek_expanded_surface_control_pool | `greek_expanded_surface_control_pool.toml` |
| greek_pattern_versions | Consolidate Greek exact-center pattern presence and source-specific control status. | 1 |  | reports/greek_pattern_versions | `greek_pattern_versions.toml` |
| greek_surface_length4_vocabulary_controls | Post-discovery length-4 Greek surface follow-up against generated real surface-vocabula... | 6 | terms/greek_surface_prospective_terms.csv | reports/greek_surface_length4_vocab_controls | `greek_surface_length4_vocabulary_controls.toml` |
| hebrew_control_version_presence | Capped exact ELS hit-pattern presence for Hebrew null and frequency controls across MT-... | 1 | terms/frequency_anchors.csv, terms/null_controls.csv | reports/hebrew_control_version_presence | `hebrew_control_version_presence.toml` |
| hebrew_modern_geopolitical_controlled_review | Join the broad Hebrew modern/geopolitical MT-family version-presence run with represent... | 3 | terms/modern_names_dates.csv | reports/hebrew_modern_geopolitical_controlled_review | `hebrew_modern_geopolitical_controlled_review.toml` |
| hebrew_screening_controlled_review | Join the broader Hebrew screening MT-family version-presence run with representative pa... | 3 | terms/biblical_calendar.csv, terms/biblical_festivals.csv, terms/biblical_tribes.csv, t... | reports/hebrew_screening_controlled_review | `hebrew_screening_controlled_review.toml` |
| kjv_apocrypha_bridge_confirmatory_controls_5000 | Locked 5000-sample post-screen confirmatory shuffled controls for 15 KJVA apocrypha bri... | 1 | terms/kjv_apocrypha_bridge_confirmatory_terms.csv | reports/kjv_apocrypha_bridge_confirmatory_controls_5000 | `kjv_apocrypha_bridge_confirmatory_controls_5000.toml` |
| kjv_apocrypha_bridge_shuffled_controls_250 | Run 250-sample shuffled apocrypha/deuterocanon bridge controls for KJVA bridge candidates. | 1 | terms/english_search_terms.csv | reports/kjv_apocrypha_bridge_shuffled_controls_250 | `kjv_apocrypha_bridge_shuffled_controls_250.toml` |
| kjv_apocrypha_bridge_term_review | Summarize KJVA apocrypha/deuterocanon bridge terms against term-level controls. | 1 |  | reports/kjv_apocrypha_bridge_term_review | `kjv_apocrypha_bridge_term_review.toml` |
| kjv_apocrypha_bridge_term_shuffled_controls_100 | Run 100-sample term-level shuffled apocrypha/deuterocanon bridge controls for KJVA brid... | 1 | terms/english_search_terms.csv | reports/kjv_apocrypha_bridge_term_shuffled_controls_100 | `kjv_apocrypha_bridge_term_shuffled_controls_100.toml` |
| kjv_apocrypha_bridge_term_shuffled_controls_1000 | Run 1000-sample term-level shuffled apocrypha/deuterocanon bridge controls for KJVA bri... | 1 | terms/english_search_terms.csv | reports/kjv_apocrypha_bridge_term_shuffled_controls_1000 | `kjv_apocrypha_bridge_term_shuffled_controls_1000.toml` |
| kjv_apocrypha_bridge_term_shuffled_controls_300 | Run 300-sample term-level shuffled apocrypha/deuterocanon bridge controls for KJVA brid... | 1 | terms/english_search_terms.csv | reports/kjv_apocrypha_bridge_term_shuffled_controls_300 | `kjv_apocrypha_bridge_term_shuffled_controls_300.toml` |
| nonbible_control_counts | Skip 2..100 screening counts against large non-Bible Hebrew, Greek, and English control... | 1 | terms/biblical_calendar.csv, terms/biblical_festivals.csv, terms/biblical_tribes.csv, t... | reports/nonbible_controls | `nonbible_control_counts.toml` |
| real_report_run | Formal report assembly run over locked STEP_TAHOT, Greek exact-center, doxa follow-ups,... | 41 | terms/bible_and_science_codes_terms.csv, terms/bible_code_digest_claim_terms.csv, terms... | reports, reports/all_codes_compound_extension_confirmatory, reports/all_codes_compound_... | `real_report_run.toml` |
| sblgnt_source_only_exact_center | Post-discovery 1000/1000 controls for SBLGNT source-only exact-center extension rows. | 2 |  | reports/sblgnt_source_only_exact_center | `sblgnt_source_only_exact_center.toml` |
| step_tahot_control_policy_hits | Audit STEP_TAHOT-only control rows against TAHOT source-type policy. | 2 |  | reports/step_tahot_control_policy_hits, reports/step_tahot_control_version_presence | `step_tahot_control_policy_hits.toml` |
| step_tahot_control_version_presence | Capped exact ELS hit-pattern presence for Hebrew null/frequency controls across MT-fami... | 1 | terms/frequency_anchors.csv, terms/null_controls.csv | reports/step_tahot_control_version_presence | `step_tahot_control_version_presence.toml` |
| step_tahot_final_gate | Consolidate STEP_TAHOT source-only real-term rows, source-policy audits, and control co... | 1 |  | reports/step_tahot_final_gate | `step_tahot_final_gate.toml` |
| targeted_version_presence | Join requested modern/geopolitical/local exact version-presence rows with available con... | 3 | terms/modern_names_dates.csv, terms/prophetic_terms.csv | reports | `targeted_version_presence.toml` |
| wide_focus_paired_controls | Representative paired controls for nonzero wide-focus count rows. | 1 |  | reports | `wide_focus_paired_controls.toml` |

## Follow-Up

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| all_codes_followup_context | Center/span text excerpts for selected Hebrew, Greek, and English all-codes rows. | 1 |  | reports/all_codes_followup_context | `all_codes_followup_context.toml` |
| all_codes_followup_extensions | Same-skip before/after extension audit for selected all-codes rows. | 1 |  | reports/all_codes_followup_extensions | `all_codes_followup_extensions.toml` |
| all_codes_followup_letter_paths | Letter-path audit sheet for selected Hebrew, Greek, and English all-codes follow-up rows. | 1 |  | reports/all_codes_followup_letter_paths | `all_codes_followup_letter_paths.toml` |
| all_codes_followup_review | Compact manual-review packet for selected Hebrew and Greek all-codes rows. | 1 |  | reports/all_codes_followup_review | `all_codes_followup_review.toml` |
| all_codes_followup_selection | Compact manual-review follow-up selection from relaxed all-codes triage queues. | 1 |  | reports/all_codes_followup_selection | `all_codes_followup_selection.toml` |
| doxa_four_source_claim_followup | Locked 5000/5000 four-source follow-up for the strongest Greek exact-center doxa extens... | 2 |  | reports/doxa_four_source_claim_followup | `doxa_four_source_claim_followup.toml` |
| doxa_four_source_confirmatory_followup | Locked 20000/20000 confirmatory follow-up for the strongest Greek exact-center doxa ext... | 2 |  | reports/doxa_four_source_confirmatory_followup | `doxa_four_source_confirmatory_followup.toml` |
| greek_expanded_surface_followup | Compact post-screen follow-up report for selected Greek exact-center surface rows. | 1 |  | reports/greek_expanded_surface_followup | `greek_expanded_surface_followup.toml` |

## Partitions

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| dynamic_skip_focus_counts | Full-distance dynamic-skip counts for selected Hebrew, Greek, and English focus terms. | 12 | terms/dynamic_skip_focus_terms.csv | reports/dynamic_skip_focus | `dynamic_skip_focus_counts.toml` |

## Prospective

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| centered_relevance_density | Locked deterministic Centered-Relevance Density run for the Gog/Magog prospective Hebre... | 2 | terms/gog_magog_pair_prospective_terms.csv | reports/crd | `centered_relevance_density.toml` |
| gog_magog_pair_prospective | Locked prospective Hebrew Gog/Magog same-chapter same-signed-skip pair-control study ov... | 5 | terms/gog_magog_pair_prospective_terms.csv | reports/gog_magog_pair_prospective | `gog_magog_pair_prospective.toml` |
| greek_expanded_prospective_exact_center | Prospective expanded Greek exact-center extension screen over new declared terms. | 10 | terms/greek_expanded_prospective_terms.csv | reports/greek_expanded_prospective_exact_center | `greek_expanded_prospective_exact_center.toml` |
| greek_expanded_surface_queue | Post-screen exact-center surface queue from the expanded Greek prospective run. | 1 |  | reports/greek_expanded_surface_queue | `greek_expanded_surface_queue.toml` |
| greek_surface_length4_followup | Post-discovery follow-up for length-4 all-source Greek surface rows exposed by the lock... | 4 | terms/greek_surface_prospective_terms.csv | reports/greek_surface_length4_followup | `greek_surface_length4_followup.toml` |
| greek_surface_prospective | Locked Greek surface prospective exact-center screen after removing prior selected rows. | 7 | terms/greek_surface_prospective_terms.csv | reports/greek_surface_prospective | `greek_surface_prospective.toml` |
| hebrew_modern_geopolitical_prospective | Locked Hebrew modern/geopolitical exact-version presence and representative-control rep... | 4 | terms/hebrew_modern_geopolitical_prospective_terms.csv | reports/hebrew_modern_geopolitical_prospective | `hebrew_modern_geopolitical_prospective.toml` |
| hebrew_theology_prospective | Locked Hebrew theology registered follow-up exact-version and representative-control sc... | 4 | terms/hebrew_theology_prospective_terms.csv | reports/hebrew_theology_prospective | `hebrew_theology_prospective.toml` |

## Replication

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| wrr_audit_counts | WRR2 imported-term count and same-record pair smoke on Koren Genesis; not the WRR stati... | 13 |  | reports/wrr_1994 | `wrr_audit_counts.toml` |
| wrr_source_import | Download external WRR audit files and convert WRR2 into repo term rows. | 3 |  | reports/wrr_1994 | `wrr_source_import.toml` |

## Screening

| Name | Description | Steps | Terms | Output Roots | Path |
| --- | --- | ---: | --- | --- | --- |
| broad_search | Broader skip 2..100 screening run across every declared term list. | 3 | terms/biblical_calendar.csv, terms/biblical_festivals.csv, terms/biblical_narrative_nam... | reports/broad_search | `broad_search.toml` |
| english_kjv_screening | English KJV skip 2..100 screening run over generated English search terms. | 1 | terms/english_search_terms.csv | reports/english_kjv_screening | `english_kjv_screening.toml` |
| english_screening_all_codes_collection | Relaxed all-codes collection for the broad English KJV screening cohort with center-wor... | 4 | terms/english_search_terms.csv | reports/db, reports/english_screening_all_codes | `english_screening_all_codes_collection.toml` |
| greek_screening_all_codes_collection | Relaxed all-codes collection for the broad Greek screening cohort with center-word surf... | 4 | terms/biblical_festivals.csv, terms/biblical_narrative_names.csv, terms/biblical_prophe... | reports/db, reports/greek_screening_all_codes | `greek_screening_all_codes_collection.toml` |
| greek_screening_version_presence | Capped exact ELS hit-pattern presence for broader Greek screening terms across Greek NT... | 1 | terms/biblical_festivals.csv, terms/biblical_narrative_names.csv, terms/biblical_prophe... | reports/greek_screening_version_presence | `greek_screening_version_presence.toml` |
| hebrew_screening_all_codes_collection | Relaxed all-codes collection for the broad Hebrew screening cohort with center-word sur... | 4 | terms/biblical_calendar.csv, terms/biblical_festivals.csv, terms/biblical_narrative_nam... | reports/db, reports/hebrew_screening_all_codes | `hebrew_screening_all_codes_collection.toml` |
| hebrew_screening_version_presence | Capped exact ELS hit-pattern presence for broader Hebrew screening terms across MT-fami... | 1 | terms/biblical_calendar.csv, terms/biblical_festivals.csv, terms/biblical_narrative_nam... | reports/hebrew_screening_version_presence | `hebrew_screening_version_presence.toml` |
| step_tahot_screening_version_presence | Run broader Hebrew exact-hit version presence with STEP_TAHOT included as a separate so... | 2 | terms/biblical_calendar.csv, terms/biblical_festivals.csv, terms/biblical_narrative_nam... | reports/step_tahot_screening_version_presence | `step_tahot_screening_version_presence.toml` |
| wide_focus_search | Focused skip 2..250 screening run for modern/geopolitical/local and prophetic terms. | 3 | terms/modern_names_dates.csv, terms/prophetic_terms.csv | reports/wide_focus_search | `wide_focus_search.toml` |
