# WRR Post-Lock Reporting Boundary

Status: post-lock reporting boundary locked.

This document separates allowed local locked-method language from forbidden exact-published reproduction language.
It does not select source corrections, pair exclusions, replacement spellings, or method changes.

## Reproduce

```bash
python3 -m scripts.build_wrr_post_lock_reporting_boundary --claim-readiness reports/wrr_1994/wrr_claim_readiness.csv --locked-method-report reports/wrr_1994/wrr_locked_method_report.csv --dashboard reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv --priority-packet reports/wrr_1994/wrr_exact_gap_priority_packet.csv --manual-decision-records data/study/mappings/wrr_manual_decision_records.csv --out reports/wrr_1994/wrr_post_lock_reporting_boundary.csv --markdown-out docs/WRR_POST_LOCK_REPORTING_BOUNDARY.md --manifest-out reports/wrr_1994/wrr_post_lock_reporting_boundary.manifest.json
```

## Current Boundary

| Boundary | Status | Value |
| --- | --- | --- |
| Local locked-method result | `ready` | 4 readiness gates ready; locked local WRR method report; not an exact published WRR reproduction |
| Exact published WRR reproduction | `forbidden` | 72 of 163 defined; gap 91 |
| Manual decision records | `all_current_manual_reviews_locked` | 37 locked; 0 unlocked; method_lock=11; no_source_change=26 |
| Source changes | `none_selected` | 26 no_source_change rows |
| Method locks | `locked` | 11 method_lock rows |
| Remaining 163-distance gap | `open` | 91 |
| Simple-variant residual gap | `open` | 40 |

## Allowed Wording

- Local locked-method result: allowed with caveats.
- It may be described as locked local selected-policy evidence under keep_all_working_source, printed D(w), cap1000 corrected distances, and a 999999 date-label permutation.
- Exact published reproduction remains caveated by the 163-distance gap, not pending source-edit choices.

## Forbidden Wording

- Do not say exact published WRR reproduced.
- Do not say the residual gap is closed.
- Do not say source corrections, pair exclusions, replacement spellings, or method changes have been selected.

## Cautions

- This is a reporting boundary, not a new statistical result.
- Current manual decision records keep 26 no_source_change rows and 11 method_lock rows.
- Future source or method changes require a separate decision record before any report language changes.
