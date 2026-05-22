# WRR Claim Blocker Packet

Status: no-input diagnostics exhausted for claim-grade WRR reproduction.

This packet does not choose disputed WRR method policy. It gathers the
claim-readiness blockers, current lock options, and WNP/context source
queue flags into one handoff artifact.

## Reproduce

```bash
python3 -m scripts.build_wrr_claim_blocker_packet --readiness reports/wrr_1994/wrr_claim_readiness.csv --lock-options reports/wrr_1994/wrr_lock_options.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --method-status reports/wrr_1994/wrr_method_status.csv --source-policy-scenarios reports/wrr_1994/wrr_source_policy_scenarios.csv --out reports/wrr_1994/wrr_claim_blocker_packet.csv --markdown-out docs/WRR_CLAIM_BLOCKER_PACKET.md --manifest-out reports/wrr_1994/wrr_claim_blocker_packet.manifest.json
```

## Blockers

| Area | Status | Blocker | Input needed |
| --- | --- | --- | --- |
| Pair universe | `open` | Pair universe: status open is not claim-ready; requires one of locked,source_locked | select pair-universe/source-review policy |
| D(w) skip-cap formula | `open` | D(w) skip-cap formula: status open is not claim-ready; requires one of locked,source_locked | select printed WRR formula or reported WRR-program formula |
| Corrected distance c(w,w') | `smoke_only` | Corrected distance c(w,w'): status smoke_only is not claim-ready; requires one of defined_full_run,full_run_locked | requires locked pair universe and D(w) formula first |
| Aggregate statistic and permutation | `diagnostic_not_claim_grade` | Aggregate statistic and permutation: status diagnostic_not_claim_grade is not claim-ready; requires one of claim_grade_ready,permutation_locked | requires locked pair universe, D(w), and full corrected-distance run first |

## No-Input Boundary

| Area | Current read | Available options | No-input next |
| --- | --- | --- | --- |
| Pair universe | The 163 count is best treated as defined-distance output, not raw pair count. | all imported WRR2 same-record pairs [candidate_input_only]; appellation length >= 5 rows [near_count_not_lock]; single Zacut appellation exclusion [diagnostic_only]; WNP/context flagged source-review queue [diagnostic_source_review_context]; defined-distance output interpretation [recommended_working_interpretation] | diagnostic review can continue, but claim-grade reproduction must not promote a pair universe without source policy |
| D(w) skip-cap formula | Printed and reported-program formulas are both implemented; final choice remains source decision. | printed WRR formula [primary_text_default]; reported WRR-program formula [sensitivity_variant] | keep printed/program sensitivity visible; do not pick final formula without source policy |
| Corrected distance c(w,w') | Direct perturbed-letter smoke driver now produces defined corrected distances in the current candidate lane, but this remains diagnostic until the pair universe and D(w) formula are locked. |  | diagnostic full-lane runs can continue only as diagnostics until upstream locks exist |
| Aggregate statistic and permutation | Published Table 3 ranks are source-audited; local diagnostic P1..P4 and date-permutation runs exist, including a repo-defined 999,999 run, but this is not an exact WRR reproduction. |  | keep date-label permutation diagnostics separate from WRR reproduction language |

## Source Policy Scenario Impact

| Scenario | Type | Excluded pairs | Remaining >=5 | Gap >=5 vs 163 | Remaining 5..8 |
| --- | --- | ---: | ---: | ---: | ---: |
| keep_all_working_source | `baseline` | 0 | 165 | -2 | 86 |
| exclude_wnp_zacut_only | `diagnostic_exclusion` | 8 | 157 | 6 | 78 |
| exclude_book_title_only | `diagnostic_exclusion` | 1 | 164 | -1 | 86 |
| review_chelm_spelling_only | `review_only` | 0 | 165 | -2 | 86 |
| exclude_all_source_review_flags | `diagnostic_exclusion` | 11 | 154 | 9 | 78 |

## Flagged Source-Review Rows

| Rank | Term id | Term | Bucket | Flags | Action |
| ---: | --- | --- | --- | --- | --- |
| 2 | `wrr2_30_app_05` | `B@LY$RLBB` | `ocr_not_matched_with_variant_lead` | `wnp_book_title_appellation_dispute` | source/title-prefix rule review before source correction |
| 5 | `wrr2_32_app_04` | `$LMHMXLMA` | `ocr_not_matched_with_variant_lead` | `wnp_chelm_spelling_context` | source/pair-rule review; do not decide from OCR crop alone |
| 7 | `wrr2_27_app_06` | `M$HZKWTW` | `ocr_near_match_with_variant_lead` | `wnp_disputed_zacut_appellation` | diagnostic flag only; do not exclude without source-lock policy |
| 12 | `wrr2_27_app_05` | `M$HZKWTA` | `ocr_matched_with_variant_lead` | `wnp_disputed_zacut_appellation` | diagnostic flag only; do not exclude without source-lock policy |
| 83 | `wrr2_32_app_05` | `$LMHMX@LMA` | `ocr_not_matched_no_variant_lead` | `wnp_chelm_spelling_context` | source/pair-rule review; do not decide from OCR crop alone |

## Interpretation

- This is a decision packet, not a reproduction result.
- Further diagnostics can stay useful, but claim-grade wording requires a source policy.
- No pair exclusion or D(w) formula is chosen here.
