# Final Report Highlights

Status: compact final-report table assembled from locked report artifacts.
This is not a new ELS search and it does not promote rows to public claims.

## Reproduce

```bash
python3 -m scripts.build_final_report_highlights --centered-summary reports/centered_occurrence_index/presence_summary.csv --claim-catalog claims/claim_catalog.csv --out reports/final_report_highlights/highlights.csv --markdown-out docs/FINAL_REPORT_HIGHLIGHTS.md --manifest-out reports/final_report_highlights/manifest.json
```

## Summary

- highlight rows: 5
- controlled or partial catalog rows: 11
- contextual_occurrence_frequency_cautioned: 1
- occurrence_background_pressure: 2
- occurrence_hold_for_referent_or_controls: 1
- occurrence_review_candidate_not_claim: 1

## Highlight Rows

| Rank | Status | Term | Center | Corpora | Occurrence type | Paths | Read |
| ---: | --- | --- | --- | --- | --- | ---: | --- |
| 1 | contextual_occurrence_frequency_cautioned | `γωγ` | REV 20:8 Gog | BYZ_NT;SBLGNT;TCG_NT;TR_NT | `centered_self_exact_word` | 14 | List occurrence: hidden `γωγ` centered at REV 20:8 Gog; contextual occurrence frequency cautioned. |
| 2 | occurrence_background_pressure | `ישוע` | EZR 10:18 יֵשׁ֤וּעַ | UHB | `centered_self_exact_word` | 68 | List occurrence: hidden `ישוע` centered at EZR 10:18 יֵשׁ֤וּעַ; occurrence background pressure. |
| 3 | occurrence_background_pressure | `משיח` | 2SA 1:21 מָשִׁ֥יחַ | EBIBLE_WLC | `centered_self_exact_word` | 33 | List occurrence: hidden `משיח` centered at 2SA 1:21 מָשִׁ֥יחַ; occurrence background pressure. |
| 4 | occurrence_hold_for_referent_or_controls | `ιησουσ` | JOS 8:3 Ἰησοῦς | LXX | `centered_self_exact_word` | 5 | List occurrence: hidden `ιησουσ` centered at JOS 8:3 Ἰησοῦς; occurrence hold for referent or controls. |
| 5 | occurrence_review_candidate_not_claim | `jesus` | MAT 4:10 Jesus | KJV | `centered_self_exact_word` | 4 | List occurrence: hidden `jesus` centered at MAT 4:10 Jesus; occurrence review candidate not claim. |

## Catalog Rows To Keep Beside The Highlights

| Claim ID | Status | Current read | Evidence |
| --- | --- | --- | --- |
| `doxa_exact_center_extension` | `controlled_review_candidate` | Four-source 5000/5000 and 20000/20000 follow-ups passed registered q <= 0.01 review gates; the 20000/20000 run has combined q = 0.0009 in all four sources and all-control q <= 0.05 | `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md` |
| `gog_rev_20_8_centered_occurrence` | `controlled_review_candidate` | Hidden Greek Gog centers on open Gog at Rev 20:8 across all four compared Greek NT source labels; matched length-3 controls caution against frequency promotion | `docs/CENTERED_OCCURRENCE_INDEX.md` |
| `greek_expanded_surface_followup` | `controlled_review_candidate` | Selected rows pass letter-path audit and all-available same-length controls with q 0.032258 | `docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md` |
| `all_codes_yom_yhwh_compound_extension` | `controlled_review_candidate` | Selected key passed locked 5000/5000 confirmatory controls in all five MT-family sources with conservative all-control q = 0.003599 | `docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md` |
| `greek_surface_length4_vocab_controls` | `partially_reproducible` | Length-4 rows reproduce but generated vocabulary controls overlap every target and no target survives study-level q <= 0.05 | `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md` |
| `modern_geopolitical_short_forms` | `partially_reproducible` | Short forms are often present and version-stable where present but representative paired controls do not support a claim | `docs/WIDE_FOCUS_PAIRED_CONTROLS.md` |
| `local_business_place_terms` | `partially_reproducible` | Cowboy alone has ordinary controlled hits; Cowboy Catering/Catering/Simscorner remain absent; Simsberry has one MAM-only exact row | `docs/WIDE_FOCUS_EXACT_PRESENCE.md` |
| `lxx_apocrypha_bridge_boundary` | `partially_reproducible` | LXX boundary rows reproduce but same-length non-Bible controls are comparable and 100 shuffled controls include 16 samples at or above observed with p_ge 0.168317 | `docs/APOCRYPHA_BRIDGE_STUDY.md` |
| `kjva_apocrypha_bridge_boundary` | `controlled_review_candidate` | KJVA bridge pass found 350 rows versus non-Bible controls of 182 140 and 168; term review found 48 of 81 bridge terms above all three same-length non-Bible term controls; 250 total shuffled controls produced 149 to 236 rows with p_ge 0.003984; 1000 term shuffled controls found 8 of 81 terms above every shuffled sample and 15 terms with BH q_ge <= 0.05; locked 5000 post-screen confirmatory controls over those 15 terms found all 15 at BH q_ge <= 0.01 and 3 above every shuffled sample | `docs/APOCRYPHA_BRIDGE_STUDY.md` |
| `critical_omission_breakage` | `partially_reproducible` | Initial omitted-verse breakage and critical-surface variant reports exist | `docs/CRITICAL_OMISSION_BREAKS.md` |
| `word_multiples_omissions` | `partially_reproducible` | Initial word and morphology multiple reports exist | `docs/WORD_COUNTS_STUDY.md` |

## Read

- This table is a presentation layer over the centered-occurrence index and claim catalog.
- A row appears here because it is useful for final-report review, not because it is claim-level.
- Frequency and control reads should be carried into any public writeup beside the occurrence.
