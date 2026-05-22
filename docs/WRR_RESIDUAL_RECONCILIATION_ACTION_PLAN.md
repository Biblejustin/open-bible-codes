# WRR Residual Reconciliation Action Plan

Status: diagnostic action plan from the residual unique-term queue.
It does not select source corrections, exclude pairs, or reproduce WRR.

Reproduce:

```bash
python3 -m scripts.build_wrr_residual_reconciliation_action_plan --residual-term-queue reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv --out reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv --summary-out reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv --markdown-out docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md --manifest-out reports/wrr_1994/wrr_residual_reconciliation_action_plan.manifest.json
```

## Current Read

- Action terms: 58.
- Residual pair links: 59.
- Minimum-frontier pair links: 40.

## Action Lanes

| Action lane | Terms | Residual pairs | Frontier pairs | Evidence required | Boundary |
| --- | ---: | ---: | ---: | --- | --- |
| `source_policy_or_pair_rule_review` | 1 | 1 | 1 | citable source-policy or pair-rule evidence for whether the flagged appellation belongs in the selected pair universe | keep term in working source; no automatic correction or exclusion without citable rule |
| `source_transcription_or_row_alignment` | 43 | 44 | 35 | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead | keep imported term; do not correct transcription until primary row evidence is locked |
| `page_image_near_match_review` | 3 | 3 | 2 | page-image inspection against near-match OCR before treating the term as source text or method blocker | keep imported term; do not treat near OCR as correction without page-image review |
| `method_or_pair_universe_review` | 11 | 11 | 2 | method and pair-universe review because OCR already matched but ordinary hits remain absent | keep source row; investigate ordinary-hit method or pair universe before source edits |

## Priority Actions

| Rank | Lane | Term id | Term | Pairs | Frontier | Source flags | Evidence required |
| ---: | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `source_policy_or_pair_rule_review` | `wrr2_32_app_05` | `$LMHMX@LMA` | 1 | 1 | `wnp_chelm_spelling_context` | citable source-policy or pair-rule evidence for whether the flagged appellation belongs in the selected pair universe |
| 2 | `source_transcription_or_row_alignment` | `wrr2_27_app_13` | `B@LQWLHRMZ` | 2 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 3 | `source_transcription_or_row_alignment` | `wrr2_01_app_06` | `B@LHA$KWL` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 4 | `source_transcription_or_row_alignment` | `wrr2_01_app_08` | `HRBABBYTDYN` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 5 | `source_transcription_or_row_alignment` | `wrr2_02_app_04` | `B@LZR@ABRHM` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 6 | `source_transcription_or_row_alignment` | `wrr2_03_app_03` | `XSDLABRHM` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 7 | `source_transcription_or_row_alignment` | `wrr2_03_app_04` | `B@LXSDLABRHM` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 8 | `source_transcription_or_row_alignment` | `wrr2_05_app_02` | `AHRNHGDWLMQRLYN` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 9 | `source_transcription_or_row_alignment` | `wrr2_06_app_03` | `B@LM@$YH$M` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 10 | `source_transcription_or_row_alignment` | `wrr2_06_app_04` | `B@LM@$YYHWH` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 11 | `source_transcription_or_row_alignment` | `wrr2_06_app_05` | `ALY@ZRA$KNZY` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 12 | `source_transcription_or_row_alignment` | `wrr2_06_app_06` | `RBYALY@ZR` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 13 | `source_transcription_or_row_alignment` | `wrr2_07_app_04` | `MHRDAWPNHYM` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 14 | `source_transcription_or_row_alignment` | `wrr2_09_app_03` | `HKWZRYH$NY` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 15 | `source_transcription_or_row_alignment` | `wrr2_09_app_04` | `B@LHKWZRYH$NY` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 16 | `source_transcription_or_row_alignment` | `wrr2_10_app_02` | `XYYMABWAL@PYH` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 17 | `source_transcription_or_row_alignment` | `wrr2_10_app_03` | `ABWAL@PYH` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 18 | `source_transcription_or_row_alignment` | `wrr2_11_app_03` | `KNSTHGDWLH` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 19 | `source_transcription_or_row_alignment` | `wrr2_11_app_04` | `B@LKNSTHGDWLH` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 20 | `source_transcription_or_row_alignment` | `wrr2_14_app_02` | `B@LXWTYAYR` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 21 | `source_transcription_or_row_alignment` | `wrr2_14_app_03` | `YAYRXYYMBKRK` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 22 | `source_transcription_or_row_alignment` | `wrr2_14_app_05` | `RBYYAYRXYYM` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 23 | `source_transcription_or_row_alignment` | `wrr2_15_app_02` | `YHWDHXSYD` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 24 | `source_transcription_or_row_alignment` | `wrr2_15_app_03` | `YHWDHHXSYD` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 25 | `source_transcription_or_row_alignment` | `wrr2_16_app_03` | `YHWDH@YA$` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 26 | `source_transcription_or_row_alignment` | `wrr2_20_app_04` | `B@LPRYMGDYM` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 27 | `source_transcription_or_row_alignment` | `wrr2_22_app_04` | `Y$RALY@QB` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 28 | `source_transcription_or_row_alignment` | `wrr2_22_app_05` | `RBYY$RALY@QB` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 29 | `source_transcription_or_row_alignment` | `wrr2_23_app_03` | `Y@QBSGL` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| 30 | `source_transcription_or_row_alignment` | `wrr2_23_app_09` | `Y@QBMWLYN` | 1 | 1 |  | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |

## No-Input Boundary

- This plan is a review work order, not a source correction set.
- Keep all residual terms in the working source until citable row, policy, or method evidence is locked.
- Source-policy flags need citable pair-rule evidence before any source-lock change.
- OCR-matched/no-variant terms should move to method or pair-universe review before source edits.
