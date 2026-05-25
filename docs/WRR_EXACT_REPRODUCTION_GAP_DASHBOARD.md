# WRR Exact Reproduction Gap Dashboard

Status: exact published WRR reproduction is not closed.

This dashboard starts from the locked local WRR method report and shows
what still blocks exact published reproduction language.
It does not select source corrections, pair exclusions, replacement spellings, or method changes.

## Reproduce

```bash
python3 -m scripts.build_wrr_exact_reproduction_gap_dashboard --locked-report reports/wrr_1994/wrr_locked_method_report.csv --defined-pair-summary reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv --gap-reasons reports/wrr_1994/wrr_defined_gap_reasons.csv --variant-upper-bound reports/wrr_1994/wrr_variant_gap_upper_bound.csv --action-summary reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv --manual-register-summary reports/wrr_1994/wrr_manual_decision_register_summary.csv --source-policy-checklist reports/wrr_1994/wrr_source_policy_review_checklist.csv --row-checklist reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --remaining-checklist reports/wrr_1994/wrr_remaining_lane_review_checklist.csv --out reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv --markdown-out docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md --manifest-out reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.manifest.json
```

## Gap Summary

| Metric | Value |
| --- | --- |
| Source-cited defined distances | 163 |
| Current defined distances | 72 |
| Remaining 163-distance gap | 91 |
| Residual gap after simple-variant upper bound | 40 |
| Manual decision rows | 37 |
| Manual action terms | 58 |
| Manual frontier pair links | 40 |

## Gap Reasons

| Reason | Pairs | Read |
| --- | ---: | --- |
| ordinary_missing_appellation_hits | 83 | ordinary pair blocked because appellation has zero ordinary hits in this run |
| ordinary_missing_date_hits | 12 | ordinary pair blocked because date has zero ordinary hits in this run |
| ordinary_missing_both_terms | 15 | ordinary pair blocked because both terms have zero ordinary hits in this run |

## Review Lanes

| Lane | Terms | Residual pairs | Frontier pairs | Evidence required |
| --- | ---: | ---: | ---: | --- |
| `source_policy_or_pair_rule_review` | 1 | 1 | 1 | citable source-policy or pair-rule evidence for whether the flagged appellation belongs in the selected pair universe |
| `source_transcription_or_row_alignment` | 43 | 44 | 35 | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead |
| `page_image_near_match_review` | 3 | 3 | 2 | page-image inspection against near-match OCR before treating the term as source text or method blocker |
| `method_or_pair_universe_review` | 11 | 11 | 2 | method and pair-universe review because OCR already matched but ordinary hits remain absent |

## Recommended Next Items

| Rank | Item | Action |
| ---: | --- | --- |
| 1 | source-policy/pair-rule: wrr2_32_app_05 $LMHMX@LMA | cite primary source/pair-rule evidence before changing working source |
| 2 | source-transcription row clusters: row 06, row 14, row 24, row 01, row 03 | review row images for 35 frontier pair links before term edits |
| 3 | page-image near-match terms | inspect 2 frontier near-match terms before source correction |
| 4 | method/pair-universe zero ordinary-hit terms | review 2 frontier OCR-matched terms for method or pair-universe explanation |
| 5 | report language | keep exact-published reproduction caveat attached until the 163-distance gap is explained |

## Boundary

- Keep the locked local WRR report unchanged unless a separate decision record changes source or method policy.
- Do not describe the local result as exact published WRR reproduction.
- Do not promote WNP/context flags, OCR near matches, or simple variant leads into corrections without citable source evidence.
- This dashboard is a review map, not a reproduction result.
