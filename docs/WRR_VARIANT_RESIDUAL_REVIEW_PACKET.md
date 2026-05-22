# WRR Variant Residual Review Packet

Status: diagnostic-only residual review packet after the simple-variant upper bound.
It does not select source corrections, replace terms, or reproduce WRR.

Reproduce:

```bash
python3 -m scripts.build_wrr_variant_residual_review_packet --blocked-pairs reports/wrr_1994/wrr_defined_gap_blocked_pairs.csv --variant-impact reports/wrr_1994/wrr_variant_gap_impact.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --upper-bound reports/wrr_1994/wrr_variant_gap_upper_bound.csv --out reports/wrr_1994/wrr_variant_residual_review_packet.csv --summary-out reports/wrr_1994/wrr_variant_residual_review_summary.csv --markdown-out docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md --manifest-out reports/wrr_1994/wrr_variant_residual_review_packet.manifest.json
```

## Current Read

- Best current run: `all_lanes_cap1000`.
- Current defined distances: 72 of 163.
- Generous simple-variant upper bound: 123 defined distances.
- Residual needed after that upper bound: 40.
- Residual candidate pool: 59 pairs.
- Residual slack: 19 pairs.
- Therefore at least 40 pairs still need source-rule or method resolution even after the generous simple-variant upper bound.

## Residual Summary

| Group | Value | Pairs | Read |
| --- | --- | ---: | --- |
| `residual_pool` | `candidate_pairs_not_closed_by_all-blocker_simple_variants` | 59 | at least residual_needed rows from this pool need source-rule or method resolution to reach the source-cited count |
| `review_frontier` | `minimum_residual_frontier` | 40 | frontier is a deterministic review priority, not a selected correction set |
| `impact_status` | `no_blocking_term_variant_hit` | 50 | residual-pool breakdown; diagnostic only |
| `impact_status` | `some_blocking_terms_have_variant_hit` | 9 | residual-pool breakdown; diagnostic only |
| `row_ocr_pair_status` | `both_matched` | 11 | residual-pool breakdown; diagnostic only |
| `row_ocr_pair_status` | `both_not_matched` | 3 | residual-pool breakdown; diagnostic only |
| `row_ocr_pair_status` | `mixed` | 45 | residual-pool breakdown; diagnostic only |

## Priority Frontier

| Rank | Frontier | Pair | Concept | Impact | Row OCR | Unresolved terms | Buckets | Flags |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `true` | `wrr2_27_app_13__wrr2_27_date_01` | `WRR2 27` | `some_blocking_terms_have_variant_hit` | `both_not_matched` | `B@LQWLHRMZ` | `ocr_not_matched_no_variant_lead` |  |
| 2 | `true` | `wrr2_02_app_04__wrr2_02_date_01` | `WRR2 02` | `some_blocking_terms_have_variant_hit` | `mixed` | `B@LZR@ABRHM` | `ocr_not_matched_no_variant_lead` |  |
| 3 | `true` | `wrr2_05_app_02__wrr2_05_date_01` | `WRR2 05` | `some_blocking_terms_have_variant_hit` | `mixed` | `AHRNHGDWLMQRLYN` | `ocr_not_matched_no_variant_lead` |  |
| 4 | `true` | `wrr2_06_app_03__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `B@LM@$YH$M` | `ocr_not_matched_no_variant_lead` |  |
| 5 | `true` | `wrr2_06_app_04__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `B@LM@$YYHWH` | `ocr_not_matched_no_variant_lead` |  |
| 6 | `true` | `wrr2_06_app_05__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `ALY@ZRA$KNZY` | `ocr_not_matched_no_variant_lead` |  |
| 7 | `true` | `wrr2_06_app_06__wrr2_06_date_01` | `WRR2 06` | `some_blocking_terms_have_variant_hit` | `mixed` | `RBYALY@ZR` | `ocr_not_matched_no_variant_lead` |  |
| 8 | `true` | `wrr2_02_app_03__wrr2_02_date_01` | `WRR2 02` | `some_blocking_terms_have_variant_hit` | `both_matched` | `ZR@ABRHM` | `ocr_matched_no_variant_lead` |  |
| 9 | `true` | `wrr2_02_app_05__wrr2_02_date_01` | `WRR2 02` | `some_blocking_terms_have_variant_hit` | `both_matched` | `ABRHMYCXQY` | `ocr_matched_no_variant_lead` |  |
| 10 | `true` | `wrr2_32_app_05__wrr2_32_date_01` | `WRR2 32` | `no_blocking_term_variant_hit` | `mixed` | `$LMHMX@LMA` | `ocr_not_matched_no_variant_lead` | `wnp_chelm_spelling_context` |
| 11 | `true` | `wrr2_01_app_06__wrr2_01_date_01` | `WRR2 01` | `no_blocking_term_variant_hit` | `both_not_matched` | `B@LHA$KWL` | `ocr_not_matched_no_variant_lead` |  |
| 12 | `true` | `wrr2_01_app_08__wrr2_01_date_01` | `WRR2 01` | `no_blocking_term_variant_hit` | `both_not_matched` | `HRBABBYTDYN` | `ocr_not_matched_no_variant_lead` |  |
| 13 | `true` | `wrr2_23_app_03__wrr2_23_date_01` | `WRR2 23` | `no_blocking_term_variant_hit` | `mixed` | `Y@QBSGL` | `ocr_not_matched_no_variant_lead` |  |
| 14 | `true` | `wrr2_03_app_03__wrr2_03_date_01` | `WRR2 03` | `no_blocking_term_variant_hit` | `mixed` | `XSDLABRHM` | `ocr_not_matched_no_variant_lead` |  |
| 15 | `true` | `wrr2_03_app_04__wrr2_03_date_01` | `WRR2 03` | `no_blocking_term_variant_hit` | `mixed` | `B@LXSDLABRHM` | `ocr_not_matched_no_variant_lead` |  |
| 16 | `true` | `wrr2_07_app_04__wrr2_07_date_01` | `WRR2 07` | `no_blocking_term_variant_hit` | `mixed` | `MHRDAWPNHYM` | `ocr_not_matched_no_variant_lead` |  |
| 17 | `true` | `wrr2_09_app_03__wrr2_09_date_01` | `WRR2 09` | `no_blocking_term_variant_hit` | `mixed` | `HKWZRYH$NY` | `ocr_not_matched_no_variant_lead` |  |
| 18 | `true` | `wrr2_09_app_04__wrr2_09_date_01` | `WRR2 09` | `no_blocking_term_variant_hit` | `mixed` | `B@LHKWZRYH$NY` | `ocr_not_matched_no_variant_lead` |  |
| 19 | `true` | `wrr2_10_app_02__wrr2_10_date_01` | `WRR2 10` | `no_blocking_term_variant_hit` | `mixed` | `XYYMABWAL@PYH` | `ocr_not_matched_no_variant_lead` |  |
| 20 | `true` | `wrr2_10_app_03__wrr2_10_date_01` | `WRR2 10` | `no_blocking_term_variant_hit` | `mixed` | `ABWAL@PYH` | `ocr_not_matched_no_variant_lead` |  |
| 21 | `true` | `wrr2_11_app_03__wrr2_11_date_01` | `WRR2 11` | `no_blocking_term_variant_hit` | `mixed` | `KNSTHGDWLH` | `ocr_not_matched_no_variant_lead` |  |
| 22 | `true` | `wrr2_11_app_04__wrr2_11_date_01` | `WRR2 11` | `no_blocking_term_variant_hit` | `mixed` | `B@LKNSTHGDWLH` | `ocr_not_matched_no_variant_lead` |  |
| 23 | `true` | `wrr2_14_app_02__wrr2_14_date_01` | `WRR2 14` | `no_blocking_term_variant_hit` | `mixed` | `B@LXWTYAYR` | `ocr_not_matched_no_variant_lead` |  |
| 24 | `true` | `wrr2_14_app_03__wrr2_14_date_01` | `WRR2 14` | `no_blocking_term_variant_hit` | `mixed` | `YAYRXYYMBKRK` | `ocr_not_matched_no_variant_lead` |  |
| 25 | `true` | `wrr2_14_app_05__wrr2_14_date_01` | `WRR2 14` | `no_blocking_term_variant_hit` | `mixed` | `RBYYAYRXYYM` | `ocr_not_matched_no_variant_lead` |  |

## Interpretation

- The frontier is deterministic triage, not a correction set.
- Rows outside the first 40 remain relevant because the 59-row pool has only 19 slack pairs.
- Partial-variant rows are ranked first because one blocker has a simple variant lead and one blocker remains unresolved.
- No-variant rows are the harder residual pool; they need source transcription, pair-rule, or method evidence beyond simple one-edit variant leads.
