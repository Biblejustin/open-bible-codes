# WRR Residual Term Reconciliation Queue

Status: diagnostic-only unique-term queue from the residual pair packet.
It does not select source corrections, exclude pairs, or reproduce WRR.

Reproduce:

```bash
python3 -m scripts.build_wrr_residual_term_reconciliation_queue --residual-packet reports/wrr_1994/wrr_variant_residual_review_packet.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --out reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv --summary-out reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv --markdown-out docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md --manifest-out reports/wrr_1994/wrr_residual_term_reconciliation_queue.manifest.json
```

## Current Read

- Unique unresolved terms: 58.
- Residual pair links represented: 59.
- Minimum-frontier pair links represented: 40.

## Summary

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

## Priority Terms

| Rank | Term id | Term | Need | Pairs | Frontier | Buckets | Source flags | Read |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `source_policy_or_pair_rule_review` | 1 | 1 | `ocr_not_matched_no_variant_lead` | `wnp_chelm_spelling_context` | term carries source-policy context; need citable rule before inclusion/exclusion changes |
| 2 | `wrr2_27_app_13` | `B@LQWLHRMZ` | `source_transcription_or_row_alignment` | 2 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 3 | `wrr2_01_app_06` | `B@LHA$KWL` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 4 | `wrr2_01_app_08` | `HRBABBYTDYN` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 5 | `wrr2_02_app_04` | `B@LZR@ABRHM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 6 | `wrr2_03_app_03` | `XSDLABRHM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 7 | `wrr2_03_app_04` | `B@LXSDLABRHM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 8 | `wrr2_05_app_02` | `AHRNHGDWLMQRLYN` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 9 | `wrr2_06_app_03` | `B@LM@$YH$M` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 10 | `wrr2_06_app_04` | `B@LM@$YYHWH` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 11 | `wrr2_06_app_05` | `ALY@ZRA$KNZY` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 12 | `wrr2_06_app_06` | `RBYALY@ZR` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 13 | `wrr2_07_app_04` | `MHRDAWPNHYM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 14 | `wrr2_09_app_03` | `HKWZRYH$NY` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 15 | `wrr2_09_app_04` | `B@LHKWZRYH$NY` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 16 | `wrr2_10_app_02` | `XYYMABWAL@PYH` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 17 | `wrr2_10_app_03` | `ABWAL@PYH` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 18 | `wrr2_11_app_03` | `KNSTHGDWLH` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 19 | `wrr2_11_app_04` | `B@LKNSTHGDWLH` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 20 | `wrr2_14_app_02` | `B@LXWTYAYR` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 21 | `wrr2_14_app_03` | `YAYRXYYMBKRK` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 22 | `wrr2_14_app_05` | `RBYYAYRXYYM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 23 | `wrr2_15_app_02` | `YHWDHXSYD` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 24 | `wrr2_15_app_03` | `YHWDHHXSYD` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 25 | `wrr2_16_app_03` | `YHWDH@YA$` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 26 | `wrr2_20_app_04` | `B@LPRYMGDYM` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 27 | `wrr2_22_app_04` | `Y$RALY@QB` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 28 | `wrr2_22_app_05` | `RBYY$RALY@QB` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 29 | `wrr2_23_app_03` | `Y@QBSGL` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |
| 30 | `wrr2_23_app_09` | `Y@QBMWLYN` | `source_transcription_or_row_alignment` | 1 | 1 | `ocr_not_matched_no_variant_lead` |  | term has no simple variant lead and did not match row OCR; check primary row transcription/alignment |

## Source-Policy Context

| Rank | Term id | Term | Flags | Action |
| ---: | --- | --- | --- | --- |
| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `wnp_chelm_spelling_context` | source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass |

## Interpretation

- This queue compresses repeated residual pair blockers into unique unresolved terms.
- Term priority is a review order, not a correction set.
- Source-policy flags require citable pair-rule evidence before any source-lock change.
- OCR-matched/no-variant terms are likely method or pair-universe blockers, not quick transcription fixes.
