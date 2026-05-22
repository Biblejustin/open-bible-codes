# WRR Claim Blocker Packet

Status: full corrected-distance run selected; aggregate/permutation still not claim-grade.

This packet records the selected WRR working policy and gathers the
remaining claim-readiness blockers, current lock options, WNP/context source
queue flags, and visual triage notes into one handoff artifact.

## Reproduce

```bash
python3 -m scripts.build_wrr_claim_blocker_packet --readiness reports/wrr_1994/wrr_claim_readiness.csv --lock-options reports/wrr_1994/wrr_lock_options.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --method-status reports/wrr_1994/wrr_method_status.csv --source-policy-scenarios reports/wrr_1994/wrr_source_policy_scenarios.csv --source-policy-term-impacts reports/wrr_1994/wrr_source_policy_term_impacts.csv --dw-formula-sensitivity reports/wrr_1994/wrr_dw_formula_sensitivity.csv --out reports/wrr_1994/wrr_claim_blocker_packet.csv --markdown-out docs/WRR_CLAIM_BLOCKER_PACKET.md --manifest-out reports/wrr_1994/wrr_claim_blocker_packet.manifest.json
```

## Blockers

| Area | Status | Blocker | Input needed |
| --- | --- | --- | --- |
| Aggregate statistic and permutation | `diagnostic_not_claim_grade` | Aggregate statistic and permutation: status diagnostic_not_claim_grade is not claim-ready; requires one of claim_grade_ready,permutation_locked | lock aggregate/permutation procedure over full corrected-distance output |

## No-Input Boundary

| Area | Current read | Available options | No-input next |
| --- | --- | --- | --- |
| Aggregate statistic and permutation | Published Table 3 ranks are source-audited; local diagnostic P1..P4 and date-permutation runs exist, including a repo-defined 999,999 run, but this is not an exact WRR reproduction. |  | keep date-label permutation diagnostics separate from WRR reproduction language |

## Source Policy Scenario Impact

| Scenario | Type | Excluded pairs | Remaining >=5 | Gap >=5 vs 163 | Remaining 5..8 |
| --- | --- | ---: | ---: | ---: | ---: |
| keep_all_working_source | `baseline` | 0 | 165 | -2 | 86 |
| exclude_wnp_zacut_only | `diagnostic_exclusion` | 8 | 157 | 6 | 78 |
| exclude_book_title_only | `diagnostic_exclusion` | 1 | 164 | -1 | 86 |
| review_chelm_spelling_only | `review_only` | 0 | 165 | -2 | 86 |
| exclude_all_source_review_flags | `diagnostic_exclusion` | 11 | 154 | 9 | 78 |

## Single-Term Source Policy Impact

| Term id | Term | Flags | Affected >=5 pairs | Remaining >=5 | Gap >=5 vs 163 | Read |
| --- | --- | --- | ---: | ---: | ---: | --- |
| wrr2_27_app_02 | ZKWTA | wnp_disputed_zacut_appellation | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| wrr2_27_app_03 | ZKWTW | wnp_disputed_zacut_appellation | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| wrr2_27_app_05 | M$HZKWTA | wnp_disputed_zacut_appellation | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| wrr2_27_app_06 | M$HZKWTW | wnp_disputed_zacut_appellation | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |

## D(w) Formula Sensitivity

| Scope | Rows | Printed defined | Program defined | Changed pairs | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| skip_cap_profile | 120 |  |  |  | profile only; printed D(w) selected as main |
| smoke_length_5_8_cap250 | 86 | 28 | 28 |  | smoke lane sensitivity; printed D(w) main, program sensitivity |
| all_lanes_cap1000 | 182 | 72 | 72 | 0 | row-level printed/program comparison; printed D(w) main, program sensitivity |

## Visual Triage Highlights

| Rank | Term id | Note | Action |
| ---: | --- | --- | --- |
| 1 | `wrr2_23_app_04` | primary page row visibly contains Yaakov Ha-Levi wording; row OCR missed it | treat as visual OCR miss until a locked transcription says otherwise |
| 2 | `wrr2_30_app_05` | primary Hebrew name cell visibly contains Yosher Levav text without visible B@L prefix | review title-prefix/appellation rule before any source correction |
| 3 | `wrr2_23_app_05` | primary page row visibly contains Maharil Segal wording; row OCR missed it | treat as visual OCR miss until a locked transcription says otherwise |
| 4 | `wrr2_28_app_04` | primary Hebrew name cell visibly contains Pnei Moshe text without visible B@L prefix | review title-prefix/appellation rule before any source correction |
| 5 | `wrr2_32_app_04` | English label says of-Chelm; visible primary Hebrew cell supports Rabbi Shelomo only in this pass | review source/pair rule before using this as a Hebrew-cell match |
| 6 | `wrr2_27_date_01` | primary page row visibly contains 16 Tishri date forms; row OCR has near match | check page image before treating as source difference |
| 7 | `wrr2_27_app_06` | primary page row visibly contains Moshe/Zacut forms; row OCR has near match | check WNP Zacut dispute and page image before treating as source difference |

## Flagged Source-Review Rows

| Rank | Term id | Term | Bucket | Flags | Action |
| ---: | --- | --- | --- | --- | --- |
| 2 | `wrr2_30_app_05` | `B@LY$RLBB` | `ocr_not_matched_with_variant_lead` | `wnp_book_title_appellation_dispute` | source/title-prefix rule review; visual notes show title text without visible B@L prefix |
| 5 | `wrr2_32_app_04` | `$LMHMXLMA` | `ocr_not_matched_with_variant_lead` | `wnp_chelm_spelling_context` | source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass |
| 7 | `wrr2_27_app_06` | `M$HZKWTW` | `ocr_near_match_with_variant_lead` | `wnp_disputed_zacut_appellation` | diagnostic flag only; do not exclude without source-lock policy |
| 12 | `wrr2_27_app_05` | `M$HZKWTA` | `ocr_matched_with_variant_lead` | `wnp_disputed_zacut_appellation` | diagnostic flag only; do not exclude without source-lock policy |
| 83 | `wrr2_32_app_05` | `$LMHMX@LMA` | `ocr_not_matched_no_variant_lead` | `wnp_chelm_spelling_context` | source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass |

## Interpretation

- This is a decision packet, not a reproduction result.
- Pair universe lock: keep_all_working_source; WNP/context and visual-review flags do not exclude pairs automatically.
- D(w) lock: printed WRR formula main; reported-program formula remains sensitivity output.
- No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change.
