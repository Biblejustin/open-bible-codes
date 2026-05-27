# WRR Claim Blocker Packet

Status: no current claim-readiness blockers under selected local WRR lock policy.

This packet records the selected WRR working policy and gathers the
remaining claim-readiness blockers, current lock options, WNP/context source
queue flags, and visual triage notes into one handoff artifact.

## Reproduce

```bash
python3 -m scripts.build_wrr_claim_blocker_packet --readiness reports/wrr_1994/wrr_claim_readiness.csv --lock-options reports/wrr_1994/wrr_lock_options.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --method-status reports/wrr_1994/wrr_method_status.csv --source-policy-scenarios reports/wrr_1994/wrr_source_policy_scenarios.csv --source-policy-term-impacts reports/wrr_1994/wrr_source_policy_term_impacts.csv --dw-formula-sensitivity reports/wrr_1994/wrr_dw_formula_sensitivity.csv --variant-residual-summary reports/wrr_1994/wrr_variant_residual_review_summary.csv --variant-residual-packet reports/wrr_1994/wrr_variant_residual_review_packet.csv --residual-term-summary reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv --residual-term-queue reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv --method-pair-universe-summary reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv --method-lane-wide-skip-summary reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv --source-transcription-row-summary reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv --remaining-lane-summary reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv --remaining-lane-packet reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv --out reports/wrr_1994/wrr_claim_blocker_packet.csv --markdown-out docs/WRR_CLAIM_BLOCKER_PACKET.md --manifest-out reports/wrr_1994/wrr_claim_blocker_packet.manifest.json
```

## Blockers

| Area | Status | Blocker | Input needed |
| --- | --- | --- | --- |
| None | `ready` | Current method-status rows satisfy the claim-readiness gate. | none |

## No-Input Boundary

| Area | Current read | Available options | No-input next |
| --- | --- | --- | --- |
| None | All required areas are ready under the selected local lock policy. |  | continue reporting exact-WRR caveats explicitly |

## Exact-WRR Residual Caveat

The local lock policy is claim-ready for repo-defined reporting, but exact published WRR reproduction still has a residual source/method gap after the generous simple-variant upper bound.

| Group | Value | Pairs | Read |
| --- | --- | ---: | --- |
| `residual_pool` | `candidate_pairs_not_closed_by_all-blocker_simple_variants` | 59 | at least 40 rows from this pool need source-rule or method resolution to reach the source-cited count |
| `review_frontier` | `minimum_residual_frontier` | 40 | frontier is a deterministic review priority, not a selected correction set |
| `impact_status` | `no_blocking_term_variant_hit` | 50 | residual-pool breakdown; diagnostic only |
| `impact_status` | `some_blocking_terms_have_variant_hit` | 9 | residual-pool breakdown; diagnostic only |
| `row_ocr_pair_status` | `both_matched` | 11 | residual-pool breakdown; diagnostic only |
| `row_ocr_pair_status` | `both_not_matched` | 3 | residual-pool breakdown; diagnostic only |
| `row_ocr_pair_status` | `mixed` | 45 | residual-pool breakdown; diagnostic only |
| `frontier_impact_status` | `no_blocking_term_variant_hit` | 31 | minimum-frontier breakdown; diagnostic only |
| `frontier_impact_status` | `some_blocking_terms_have_variant_hit` | 9 | minimum-frontier breakdown; diagnostic only |
| `frontier_row_ocr_pair_status` | `both_matched` | 2 | minimum-frontier breakdown; diagnostic only |
| `frontier_row_ocr_pair_status` | `both_not_matched` | 3 | minimum-frontier breakdown; diagnostic only |
| `frontier_row_ocr_pair_status` | `mixed` | 35 | minimum-frontier breakdown; diagnostic only |
| `unresolved_term_side` | `appellation` | 59 | unresolved-term breakdown; diagnostic only |
| `unresolved_term_bucket` | `ocr_matched_no_variant_lead` | 11 | unresolved-term breakdown; diagnostic only |
| `unresolved_term_bucket` | `ocr_near_match_no_variant_lead` | 3 | unresolved-term breakdown; diagnostic only |
| `unresolved_term_bucket` | `ocr_not_matched_no_variant_lead` | 45 | unresolved-term breakdown; diagnostic only |
| `unresolved_source_flag` | `wnp_chelm_spelling_context` | 1 | unresolved-term breakdown; diagnostic only |

### Residual Frontier Sample

| Rank | Pair | Concept | Impact | Row OCR | Unresolved terms | Flags |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `wrr2_27_app_13__wrr2_27_date_01` | `WRR2 27` | `some_blocking_terms_have_variant_hit` | `both_not_matched` | `B@LQWLHRMZ` |  |
| 2 | `wrr2_02_app_04__wrr2_02_date_01` | `WRR2 02` | `some_blocking_terms_have_variant_hit` | `mixed` | `B@LZR@ABRHM` |  |
| 3 | `wrr2_05_app_02__wrr2_05_date_01` | `WRR2 05` | `some_blocking_terms_have_variant_hit` | `mixed` | `AHRNHGDWLMQRLYN` |  |
| 4 | `wrr2_06_app_03__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `B@LM@$YH$M` |  |
| 5 | `wrr2_06_app_04__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `B@LM@$YYHWH` |  |
| 6 | `wrr2_06_app_05__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `ALY@ZRA$KNZY` |  |
| 7 | `wrr2_06_app_06__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `RBYALY@ZR` |  |
| 8 | `wrr2_02_app_03__wrr2_02_date_01` | `WRR2 02` | `some_blocking_terms_have_variant_hit` | `both_matched` | `ZR@ABRHM` |  |
| 9 | `wrr2_02_app_05__wrr2_02_date_01` | `WRR2 02` | `some_blocking_terms_have_variant_hit` | `both_matched` | `ABRHMYCXQY` |  |
| 10 | `wrr2_32_app_05__wrr2_32_date_01` | `WRR2 32` | `no_blocking_term_variant_hit` | `mixed` | `$LMHMX@LMA` | `wnp_chelm_spelling_context` |

### Residual Term Queue

The queue compresses repeated residual pair blockers into unique unresolved terms. It is a diagnostic review order, not a correction set or exclusion policy.

| Group | Value | Terms | Residual pairs | Frontier pairs | Read |
| --- | --- | ---: | ---: | ---: | --- |
| `residual_terms` | `unique_unresolved_terms` | 58 | 59 | 40 | unique unresolved term targets collapsed from residual pair rows |
| `term_side` | `appellation` | 58 | 59 | 40 | residual term queue breakdown; diagnostic only |
| `review_bucket` | `ocr_matched_no_variant_lead` | 11 | 11 | 2 | residual term queue breakdown; diagnostic only |
| `review_bucket` | `ocr_near_match_no_variant_lead` | 3 | 3 | 2 | residual term queue breakdown; diagnostic only |
| `review_bucket` | `ocr_not_matched_no_variant_lead` | 44 | 45 | 36 | residual term queue breakdown; diagnostic only |
| `term_ocr_status` | `matched` | 11 | 11 | 2 | residual term queue breakdown; diagnostic only |
| `term_ocr_status` | `not_matched` | 47 | 48 | 38 | residual term queue breakdown; diagnostic only |
| `source_flag` | `wnp_chelm_spelling_context` | 1 | 1 | 1 | residual term queue breakdown; diagnostic only |
| `reconciliation_need` | `method_or_pair_universe_review` | 11 | 11 | 2 | residual term queue breakdown; diagnostic only |
| `reconciliation_need` | `page_image_near_match_review` | 3 | 3 | 2 | residual term queue breakdown; diagnostic only |
| `reconciliation_need` | `source_policy_or_pair_rule_review` | 1 | 1 | 1 | residual term queue breakdown; diagnostic only |
| `reconciliation_need` | `source_transcription_or_row_alignment` | 43 | 44 | 35 | residual term queue breakdown; diagnostic only |

### Top Residual Term Targets

| Rank | Term id | Term | Need | Pairs | Frontier | Buckets | Source flags |
| ---: | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `source_policy_or_pair_rule_review` | 1 | 1 | `ocr_not_matched_no_variant_lead` | `wnp_chelm_spelling_context` |
| 2 | `wrr2_27_app_13` | `B@LQWLHRMZ` | `source_transcription_or_row_alignment` | 2 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 3 | `wrr2_01_app_06` | `B@LHA$KWL` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 4 | `wrr2_01_app_08` | `HRBABBYTDYN` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 5 | `wrr2_02_app_04` | `B@LZR@ABRHM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 6 | `wrr2_03_app_03` | `XSDLABRHM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 7 | `wrr2_03_app_04` | `B@LXSDLABRHM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 8 | `wrr2_05_app_02` | `AHRNHGDWLMQRLYN` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 9 | `wrr2_06_app_03` | `B@LM@$YH$M` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |
| 10 | `wrr2_06_app_04` | `B@LM@$YYHWH` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  |

### Source-Transcription Row Evidence Summary

| Row clusters | Action terms | Residual pairs | Frontier pairs | Top row | Read |
| ---: | ---: | ---: | ---: | --- | --- |
| 22 | 43 | 44 | 35 | `06` | review multi-term rows once by row before term edits |

### Source-Transcription Priority Rows

| Rank | Row | Concept | Terms | Pairs | Frontier | Action terms not matched |
| ---: | --- | --- | ---: | ---: | ---: | --- |
| 1 | `06` | `WRR2 06` | 4 | 4 | 4 | wrr2_06_app_03 B@LM@$YH$M;wrr2_06_app_04 B@LM@$YYHWH;wrr2_06_app_05 ALY@ZRA$KNZY;wrr2_06_app_06 RBYALY@ZR |
| 2 | `14` | `WRR2 14` | 3 | 3 | 3 | wrr2_14_app_02 B@LXWTYAYR;wrr2_14_app_03 YAYRXYYMBKRK;wrr2_14_app_05 RBYYAYRXYYM |
| 3 | `24` | `WRR2 24` | 3 | 3 | 3 | wrr2_24_app_06 Y@QBY$RAL@MDN;wrr2_24_app_07 Y@QBY$RAL@MDYN;wrr2_24_app_09 RBYY@QBY$RAL |
| 4 | `01` | `WRR2 01` | 2 | 2 | 2 | wrr2_01_app_06 B@LHA$KWL;wrr2_01_app_08 HRBABBYTDYN |
| 5 | `03` | `WRR2 03` | 2 | 2 | 2 | wrr2_03_app_03 XSDLABRHM;wrr2_03_app_04 B@LXSDLABRHM |

### Page-Image Near-Match Evidence Summary

| Terms | Residual pairs | Frontier pairs | Concepts | Read |
| ---: | ---: | ---: | ---: | --- |
| 3 | 3 | 2 | 2 | near OCR exists, but page image must decide whether it is source evidence |

### Page-Image Near-Match Terms

| Rank | Term id | Term | Row | Near match | Visual note |
| ---: | --- | --- | --- | --- | --- |
| 1 | `wrr2_19_app_11` | `YWSP+RANY` | `19` | `d=1 יוספטרני` | primary page row visibly contains Maharit/Trani forms including Yosef Trani; row OCR has one-edit near match |
| 2 | `wrr2_19_app_12` | `YWSPM+RANY` | `19` | `d=1 יוספמטרני` | primary page row visibly contains Maharit/Trani forms including Matrani/Mitrani variants; row OCR has one-edit near match |
| 3 | `wrr2_31_app_07` | `$M$` | `31` | `d=1 שרש` | primary page row visibly contains Rabbi Shalom Sharabi forms including Sar Shalom and MaharaSHaSH; exact SMSh form is not settled by this crop |

### Method/Pair-Universe Evidence Summary

| Terms | Pairs | OCR matched | Zero skip-250 | Zero high-cap | Both sides zero | Read |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 11 | 11 | 11 | 11 | 11 | 2 | OCR matched all method-lane terms, but current Koren Genesis ordinary-hit search still leaves them undefined. |

### Method-Lane Wide-Skip Probe

This extends the ordinary Genesis ELS probe for OCR-matched method-lane terms beyond the selected cap. It is diagnostic only; it does not change the locked pair universe.

| Terms | Max skip | Direction | Any-hit terms | Zero-through-max terms | Total hits | Read |
| ---: | ---: | --- | ---: | ---: | ---: | --- |
| 11 | 5000 | `both` | 0 | 11 | 0 | All 11 OCR-matched method-lane terms remain absent through skip 5000; the method lane is not explained by a small cap extension. |

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
| 84 | `wrr2_19_app_11` | primary page row visibly contains Maharit/Trani forms including Yosef Trani; row OCR has one-edit near match | keep as page-image near-match until a locked transcription resolves the aleph spelling |
| 85 | `wrr2_19_app_12` | primary page row visibly contains Maharit/Trani forms including Matrani/Mitrani variants; row OCR has one-edit near match | keep as page-image near-match until a locked transcription resolves the aleph spelling |
| 86 | `wrr2_31_app_07` | primary page row visibly contains Rabbi Shalom Sharabi forms including Sar Shalom and MaharaSHaSH; exact SMSh form is not settled by this crop | keep as page-image or pair-rule review before any source correction |

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
- Exact published WRR reproduction remains caveated by the residual source/method gap after the simple-variant upper bound.
- Residual term priority is a review order, not a correction set or pair-exclusion list.
- D(w) lock: printed WRR formula main; reported-program formula remains sensitivity output.
- Aggregate/permutation lock: keep-all cap1000 999,999 date-label permutation over the full selected-universe corrected-distance output.
- No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change.
