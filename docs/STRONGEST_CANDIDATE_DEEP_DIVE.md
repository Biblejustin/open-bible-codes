# Strongest Candidate Deep Dive

Status: deterministic review packet built from locked report artifacts.
This is not a new ELS search and it does not upgrade any row to claim-grade evidence.

## Reproduce

```bash
python3 -m scripts.build_strongest_candidate_deep_dive --claim-catalog claims/claim_catalog.csv --out reports/strongest_candidate_deep_dive/candidates.csv --markdown-out docs/STRONGEST_CANDIDATE_DEEP_DIVE.md --manifest-out reports/strongest_candidate_deep_dive/manifest.json
```

## Summary

- candidate rows: 5
- recommended first move: lock the next prospective doxa-style Greek extension study before inspecting new candidates
- main caution: all rows below are post-discovery or occurrence-review rows except where explicitly marked as prospective

## Ranked Candidates

| Rank | Candidate | Decision | Control read | Limit | Next action |
| ---: | --- | --- | --- | --- | --- |
| 1 | `doxa_exact_center_extension` | `advance_to_next_prospective_lock` | 4 sources; 20000 term controls and 20000 random controls per source; max combined q 0.0009; max all-control q 0.042998. | Post-discovery follow-up; full extension phrase is hidden-path only and not surface text in the hit passage. | Lock a prospective Greek extension study before inspecting new rows; reuse same four Greek NT sources, same metric, same term/random control families. |
| 2 | `all_codes_yom_yhwh_compound_extension` | `advance_after_doxa_or_pair_with_hebrew_lock` | 5 MT-family sources; 5000 term controls and 5000 random controls per source; max combined q 0.0002; max all-control q 0.004799. | Post-discovery follow-up from broad all-codes queue; review candidate not claim. | Lock a Hebrew compound-extension prospective cohort with the same source-family rule before adding or ranking new Hebrew extension rows. |
| 3 | `gog_rev_20_8_centered_occurrence` | `hold_as_context_occurrence_not_claim` | length-3 matched-control rank desc 25/asc 1; controls above target 24; not frequency-promoted | Occurrence-first review row; preserve in final occurrence list but do not promote as a claim. | Keep in final occurrence list; any stronger promotion needs a longer Gog/Magog paired metric with declared controls. |
| 4 | `greek_expanded_surface_followup` | `secondary_candidate_needs_prospective_surface_lock` | 3 selected terms; max observed all-source patterns 1; max all-source q 0.032258 under all-available real-word controls. | Post-screen follow-up from previously observed surface queue; not prospective discovery or claim. | Fold into next Greek prospective design only if terms, surface rule, and same-length control pool are frozen before observing candidates. |
| 5 | `kjva_apocrypha_bridge_boundary` | `do_not_promote_without_new_prospective_success` | Post-screen confirmatory: 15/15 terms at q <= 0.01, 3 above every shuffled sample. Prospective lock: 1 bridge row, 0/7 terms at q <= 0.05. | Post-screen follow-up candidate only; 15 registered confirmatory terms pass BH q_ge <= 0.01 under 5000 samples but no center-word exact bridge rows and this is not original prospective discovery. | Treat as methods case study; do not promote unless a new prospective term lock produces independent control support. |

## Detail Rows

### 1. Greek doxa four-source exact-center extension

- Candidate ID: `doxa_exact_center_extension`
- Status: `controlled_review_candidate`
- Language: `greek`
- Evidence read: Four-source 5000/5000 and 20000/20000 follow-ups passed registered q <= 0.01 review gates; the 20000/20000 run has combined q = 0.0009 in all four sources and all-control q <= 0.05
- Control read: 4 sources; 20000 term controls and 20000 random controls per source; max combined q 0.0009; max all-control q 0.042998.
- Context read: Exact-center context at 2TH 3:1 around κυριου; base surface appears in center verse; full extension phrase is hidden-path-only.
- Limit: Post-discovery follow-up; full extension phrase is hidden-path only and not surface text in the hit passage.
- Next action: Lock a prospective Greek extension study before inspecting new rows; reuse same four Greek NT sources, same metric, same term/random control families.
- Primary artifact: `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`
- Supporting artifacts: `reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv; reports/doxa_four_source_confirmatory_followup/context_review_summary.csv; reports/doxa_four_source_confirmatory_followup/report.manifest.json`

### 2. Hebrew Day of YHWH compound extension

- Candidate ID: `all_codes_yom_yhwh_compound_extension`
- Status: `controlled_review_candidate`
- Language: `hebrew`
- Evidence read: Selected key passed locked 5000/5000 confirmatory controls in all five MT-family sources with conservative all-control q = 0.004799
- Control read: 5 MT-family sources; 5000 term controls and 5000 random controls per source; max combined q 0.0002; max all-control q 0.004799.
- Context read: Same overlap key across EBIBLE_WLC,MAM,MT_WLC,UHB,UXLC; skip 4 forward; extension היומיהוה; matched refs LEV 9:4; 2KI 2:3; 2KI 2:5.
- Limit: Post-discovery follow-up from broad all-codes queue; review candidate not claim.
- Next action: Lock a Hebrew compound-extension prospective cohort with the same source-family rule before adding or ranking new Hebrew extension rows.
- Primary artifact: `docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`
- Supporting artifacts: `reports/all_codes_compound_extension_confirmatory/summary.csv; reports/all_codes_compound_extension_confirmatory/manifest.json; reports/all_codes_compound_extension_confirmatory/examples.csv`

### 3. Greek Gog centered on open Gog at Rev 20:8

- Candidate ID: `gog_rev_20_8_centered_occurrence`
- Status: `controlled_review_candidate`
- Language: `greek`
- Evidence read: Hidden Greek Gog centers on open Gog at Rev 20:8 across all four compared Greek NT source labels; matched length-3 controls caution against frequency promotion
- Control read: length-3 matched-control rank desc 25/asc 1; controls above target 24; not frequency-promoted
- Context read: 4 Greek NT sources; 14 exact-center paths; center REV 20:8=4 Gog; context Rev 20:8 Gog/Magog context.
- Limit: Occurrence-first review row; preserve in final occurrence list but do not promote as a claim.
- Next action: Keep in final occurrence list; any stronger promotion needs a longer Gog/Magog paired metric with declared controls.
- Primary artifact: `docs/CENTERED_OCCURRENCE_INDEX.md`
- Supporting artifacts: `reports/centered_occurrence_index/centered_occurrences.csv; reports/centered_occurrence_index/presence_summary.csv; reports/centered_occurrence_index/manifest.json`

### 4. Greek expanded exact-center surface follow-up

- Candidate ID: `greek_expanded_surface_followup`
- Status: `controlled_review_candidate`
- Language: `greek`
- Evidence read: Selected rows pass letter-path audit and all-available same-length controls with q 0.032258
- Control read: 3 selected terms; max observed all-source patterns 1; max all-source q 0.032258 under all-available real-word controls.
- Context read: Selected terms appear across BYZ_NT, SBLGNT, TCG_NT, TR_NT; selected rows include Isaac, Wonder, and Lawlessness.
- Limit: Post-screen follow-up from previously observed surface queue; not prospective discovery or claim.
- Next action: Fold into next Greek prospective design only if terms, surface rule, and same-length control pool are frozen before observing candidates.
- Primary artifact: `docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`
- Supporting artifacts: `reports/greek_expanded_surface_available_control_evaluation/summary.csv; reports/greek_expanded_surface_triage/selected_patterns.csv; reports/greek_expanded_surface_followup/report.manifest.json`

### 5. KJVA Apocrypha bridge boundary

- Candidate ID: `kjva_apocrypha_bridge_boundary`
- Status: `controlled_review_candidate`
- Language: `english`
- Evidence read: KJVA bridge pass found 350 rows versus non-Bible controls of 182 140 and 168; term review found 48 of 81 bridge terms above all three same-length non-Bible term controls; 250 total shuffled controls produced 149 to 236 rows with p_ge 0.003984; 1000 term shuffled controls found 8 of 81 terms above every shuffled sample and 15 terms with BH q_ge <= 0.05; locked 5000 post-screen confirmatory controls over those 15 terms found all 15 at BH q_ge <= 0.01 and 3 above every shuffled sample
- Control read: Post-screen confirmatory: 15/15 terms at q <= 0.01, 3 above every shuffled sample. Prospective lock: 1 bridge row, 0/7 terms at q <= 0.05.
- Context read: Boundary mechanics reproduce, but current independent prospective bridge read is weak/negative.
- Limit: Post-screen follow-up candidate only; 15 registered confirmatory terms pass BH q_ge <= 0.01 under 5000 samples but no center-word exact bridge rows and this is not original prospective discovery.
- Next action: Treat as methods case study; do not promote unless a new prospective term lock produces independent control support.
- Primary artifact: `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`
- Supporting artifacts: `reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_summary.csv; reports/kjv_apocrypha_bridge_prospective/term_summary.csv; reports/kjv_apocrypha_bridge_prospective/bridge_summary.csv; docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`

## Cautions

- Strongest here means strongest current review candidate inside this repo, not evidence of design.
- Post-discovery control support is useful for triage, but prospective locks carry more evidential weight.
- Short terms, hidden-path-only extensions, translation-boundary effects, and source-family dependence remain separate risks.
