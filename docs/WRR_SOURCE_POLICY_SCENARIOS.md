# WRR Source Policy Scenario Impact

Status: diagnostic-only scenario impact. No source policy is selected.

This report counts what would happen to the current WRR2 pair-eligibility
table under several named source-review policies. It does not apply any
policy to the repo outputs and is not claim-grade reproduction evidence.

## Reproduce

```bash
python3 -m scripts.analyze_wrr_source_policy_scenarios --pair-table reports/wrr_1994/wrr2_pair_eligibility_table.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --expected-published-pairs 163 --out reports/wrr_1994/wrr_source_policy_scenarios.csv --pair-out reports/wrr_1994/wrr_source_policy_scenario_pairs.csv --term-impact-out reports/wrr_1994/wrr_source_policy_term_impacts.csv --markdown-out docs/WRR_SOURCE_POLICY_SCENARIOS.md --manifest-out reports/wrr_1994/wrr_source_policy_scenarios.manifest.json
```

## Summary

| Scenario | Type | Excl pairs | Review pairs | Remain >=5 | Remain 5..8 | Gap >=5 vs 163 | Gap 5..8 vs 163 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| keep_all_working_source | `baseline` | 0 | 0 | 165 | 86 | -2 | 77 |
| exclude_wnp_zacut_only | `diagnostic_exclusion` | 8 | 0 | 157 | 78 | 6 | 85 |
| exclude_book_title_only | `diagnostic_exclusion` | 1 | 0 | 164 | 86 | -1 | 77 |
| review_chelm_spelling_only | `review_only` | 0 | 2 | 165 | 86 | -2 | 77 |
| exclude_all_source_review_flags | `diagnostic_exclusion` | 11 | 0 | 154 | 78 | 9 | 85 |

## Flagged Terms

| Term id | Term | Side | Flags | Basis | Action |
| --- | --- | --- | --- | --- | --- |
| `wrr2_27_app_02` | `ZKWTA` | `appellation` | `wnp_disputed_zacut_appellation` | `pair_table_wnp_flag` |  |
| `wrr2_27_app_03` | `ZKWTW` | `appellation` | `wnp_disputed_zacut_appellation` | `pair_table_wnp_flag` |  |
| `wrr2_27_app_05` | `M$HZKWTA` | `appellation` | `wnp_disputed_zacut_appellation` | `pair_table_wnp_flag;source_queue` | diagnostic flag only; do not exclude without source-lock policy |
| `wrr2_27_app_06` | `M$HZKWTW` | `appellation` | `wnp_disputed_zacut_appellation` | `pair_table_wnp_flag;source_queue` | diagnostic flag only; do not exclude without source-lock policy |
| `wrr2_30_app_05` | `B@LY$RLBB` | `appellation` | `wnp_book_title_appellation_dispute` | `source_queue` | source/title-prefix rule review before source correction |
| `wrr2_32_app_04` | `$LMHMXLMA` | `appellation` | `wnp_chelm_spelling_context` | `source_queue` | source/pair-rule review; do not decide from OCR crop alone |
| `wrr2_32_app_05` | `$LMHMX@LMA` | `appellation` | `wnp_chelm_spelling_context` | `source_queue` | source/pair-rule review; do not decide from OCR crop alone |

## Single-Term Impact

| Term id | Term | Flags | Affected pairs | Remain >=5 if excluded | Gap vs 163 | Read |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `wrr2_27_app_02` | `ZKWTA` | `wnp_disputed_zacut_appellation` | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| `wrr2_27_app_03` | `ZKWTW` | `wnp_disputed_zacut_appellation` | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| `wrr2_27_app_05` | `M$HZKWTA` | `wnp_disputed_zacut_appellation` | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| `wrr2_27_app_06` | `M$HZKWTW` | `wnp_disputed_zacut_appellation` | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |
| `wrr2_30_app_05` | `B@LY$RLBB` | `wnp_book_title_appellation_dispute` | 1 | 164 | -1 | single-term diagnostic only; no source policy selected |
| `wrr2_32_app_04` | `$LMHMXLMA` | `wnp_chelm_spelling_context` | 1 | 164 | -1 | single-term diagnostic only; no source policy selected |
| `wrr2_32_app_05` | `$LMHMX@LMA` | `wnp_chelm_spelling_context` | 1 | 164 | -1 | single-term diagnostic only; no source policy selected |

## Impact Rows

| Scenario | Action | Pair | Concept | Flags | Lane |
| --- | --- | --- | --- | --- | --- |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_02__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_02__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_03__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_03__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_05__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_05__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_06__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_wnp_zacut_only` | `excluded` | `wrr2_27_app_06__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_book_title_only` | `excluded` | `wrr2_30_app_05__wrr2_30_date_01` | WRR2 30 | `wnp_book_title_appellation_dispute` | `appellation_min_length_candidate` |
| `review_chelm_spelling_only` | `review_only_no_exclusion` | `wrr2_32_app_04__wrr2_32_date_01` | WRR2 32 | `wnp_chelm_spelling_context` | `appellation_min_length_candidate` |
| `review_chelm_spelling_only` | `review_only_no_exclusion` | `wrr2_32_app_05__wrr2_32_date_01` | WRR2 32 | `wnp_chelm_spelling_context` | `appellation_min_length_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_02__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_02__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_03__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_03__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_05__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_05__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_06__wrr2_27_date_01` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_27_app_06__wrr2_27_date_02` | WRR2 27 | `wnp_disputed_zacut_appellation` | `length_5_8_smoke_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_30_app_05__wrr2_30_date_01` | WRR2 30 | `wnp_book_title_appellation_dispute` | `appellation_min_length_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_32_app_04__wrr2_32_date_01` | WRR2 32 | `wnp_chelm_spelling_context` | `appellation_min_length_candidate` |
| `exclude_all_source_review_flags` | `excluded` | `wrr2_32_app_05__wrr2_32_date_01` | WRR2 32 | `wnp_chelm_spelling_context` | `appellation_min_length_candidate` |

## Interpretation

- `keep_all_working_source` is the current diagnostic baseline.
- Exclusion scenarios show count impact only; they are not selected policies.
- `review_chelm_spelling_only` keeps pair counts stable and records review scope.
- Claim-grade WRR language still needs an explicit source policy and D(w) lock.
