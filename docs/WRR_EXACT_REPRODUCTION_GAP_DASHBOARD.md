# WRR Exact Reproduction Gap Dashboard

Status: exact published WRR reproduction is not closed.

This dashboard starts from the locked local WRR method report and shows
what still blocks exact published reproduction language.
It does not select source corrections, pair exclusions, replacement spellings, or method changes.

## Reproduce

```bash
python3 -m scripts.build_wrr_exact_reproduction_gap_dashboard --locked-report reports/wrr_1994/wrr_locked_method_report.csv --defined-pair-summary reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv --gap-reasons reports/wrr_1994/wrr_defined_gap_reasons.csv --variant-upper-bound reports/wrr_1994/wrr_variant_gap_upper_bound.csv --action-summary reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv --manual-register-summary reports/wrr_1994/wrr_manual_decision_register_summary.csv --manual-decision-records data/study/mappings/wrr_manual_decision_records.csv --source-policy-checklist reports/wrr_1994/wrr_source_policy_review_checklist.csv --row-checklist reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --remaining-checklist reports/wrr_1994/wrr_remaining_lane_review_checklist.csv --out reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv --markdown-out docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md --manifest-out reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.manifest.json
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
| Locked manual decision records | 37 |
| Unlocked manual decision records | 0 |
| Recorded selected actions | method_lock=11; no_source_change=26 |

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

## Manual Lock Status

| Lock | Status | Action | Evidence read |
| --- | --- | --- | --- |
| Chelm source-policy/pair-rule target | locked | no_source_change | Kept working source unchanged because WNP Chełm context supports review scope while local row OCR does not lock the Chełm forms as source-cell text |
| row 06 | locked | no_source_change | Kept working source unchanged for row 06 because row-aligned OCR/probe evidence is not sufficient evidence for source correction and secondary WRR2 row alignment remains the working source |
| wrr2_19_app_11 | locked | no_source_change | Kept working source unchanged because WRR ASCII A is treated as aleph not a vowel point and the page/OCR near-match does not justify correcting the imported aleph spelling |
| wrr2_02_app_03 | locked | method_lock | Locked current method result because OCR matched the imported term but both appellation and date have zero high-cap ordinary hits so the pair remains ordinary_not_valid under current rules |

## Recommended Next Items

| Rank | Item | Action |
| ---: | --- | --- |
| 1 | post-lock reporting boundary | all current manual review rows are locked; keep source unchanged and describe the residual gap as exact-reproduction work, not pending source edits |
| 2 | exact-published gap language | keep exact-published reproduction caveat attached until the 163-distance gap is explained |

## Boundary

- Keep the locked local WRR report unchanged unless a separate decision record changes source or method policy.
- Do not describe the local result as exact published WRR reproduction.
- Do not promote WNP/context flags, OCR near matches, or simple variant leads into corrections without citable source evidence.
- This dashboard is a review map, not a reproduction result.
