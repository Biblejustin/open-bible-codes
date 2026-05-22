# WRR Defined Pair-Set Audit

Status: diagnostic-only pair-universe pressure audit, not a WRR reproduction.

This report joins the current working pair table to existing direct
corrected-distance outputs. It asks which imported same-record pairs
currently produce defined `c(w,w')` values and how far those counts remain
from the source-cited second-list distance count.

## Reproduce

```bash
python3 -m scripts.analyze_wrr_defined_pair_set --pair-summary reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv --pair-table reports/wrr_1994/wrr2_pair_eligibility_table.csv --out reports/wrr_1994/wrr_defined_pair_set_audit.csv --summary-out reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv --markdown-out docs/WRR_DEFINED_PAIR_SET_AUDIT.md --manifest-out reports/wrr_1994/wrr_defined_pair_set_audit.manifest.json
```

## Run Summary

| Run | Pairs | Defined | Gap to source-cited count | Ordinary not valid | Under minimum | Other | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| all_lanes_cap250 | 182 | 50 | 113 | 130 | 2 | 0 | diagnostic_only_not_wrr_reproduction |
| all_lanes_cap1000 | 182 | 72 | 91 | 110 | 0 | 0 | diagnostic_only_not_wrr_reproduction |
| all_lanes_cap1000_program | 182 | 72 | 91 | 110 | 0 | 0 | diagnostic_only_not_wrr_reproduction |

## Candidate-Lane Breakdown

| Run | Candidate lane | Pairs | Defined | Ordinary not valid | Under minimum |
| --- | --- | ---: | ---: | ---: | ---: |
| all_lanes_cap250 | `appellation_min_length_candidate` | 79 | 10 | 69 | 0 |
| all_lanes_cap250 | `excluded_by_appellation_min_length` | 17 | 12 | 5 | 0 |
| all_lanes_cap250 | `length_5_8_smoke_candidate` | 86 | 28 | 56 | 2 |
| all_lanes_cap1000 | `appellation_min_length_candidate` | 79 | 12 | 67 | 0 |
| all_lanes_cap1000 | `excluded_by_appellation_min_length` | 17 | 14 | 3 | 0 |
| all_lanes_cap1000 | `length_5_8_smoke_candidate` | 86 | 46 | 40 | 0 |
| all_lanes_cap1000_program | `appellation_min_length_candidate` | 79 | 12 | 67 | 0 |
| all_lanes_cap1000_program | `excluded_by_appellation_min_length` | 17 | 14 | 3 | 0 |
| all_lanes_cap1000_program | `length_5_8_smoke_candidate` | 86 | 46 | 40 | 0 |

## Review-Status Breakdown

| Run | Review status | Pairs | Defined | Ordinary not valid | Under minimum |
| --- | --- | ---: | ---: | ---: | ---: |
| all_lanes_cap250 | `diagnostic_exclusion_candidate_not_locked` | 8 | 2 | 6 | 0 |
| all_lanes_cap250 | `needs_primary_source_pair_rule` | 174 | 48 | 124 | 2 |
| all_lanes_cap1000 | `diagnostic_exclusion_candidate_not_locked` | 8 | 2 | 6 | 0 |
| all_lanes_cap1000 | `needs_primary_source_pair_rule` | 174 | 70 | 104 | 0 |
| all_lanes_cap1000_program | `diagnostic_exclusion_candidate_not_locked` | 8 | 2 | 6 | 0 |
| all_lanes_cap1000_program | `needs_primary_source_pair_rule` | 174 | 70 | 104 | 0 |

## WNP Zacut Diagnostic Breakdown

| Run | WNP Zacut flag | Pairs | Defined | Ordinary not valid | Under minimum |
| --- | --- | ---: | ---: | ---: | ---: |
| all_lanes_cap250 | `False` | 174 | 48 | 124 | 2 |
| all_lanes_cap250 | `True` | 8 | 2 | 6 | 0 |
| all_lanes_cap1000 | `False` | 174 | 70 | 104 | 0 |
| all_lanes_cap1000 | `True` | 8 | 2 | 6 | 0 |
| all_lanes_cap1000_program | `False` | 174 | 70 | 104 | 0 |
| all_lanes_cap1000_program | `True` | 8 | 2 | 6 | 0 |

## Read

- Best current run: `all_lanes_cap1000` defines 72 of 163.
- Gap to the source-cited count remains 91.
- The missing mass is ordinary-not-valid, not an under-minimum-valid edge case.
- Candidate-lane and WNP-Zacut rows are diagnostic pressure only; they do
  not establish a source-locked pair rule.
- Visual-review notes do not change pair inclusion until an explicit
  source policy is selected.
- Claim language stays blocked by `docs/WRR_CLAIM_READINESS.md`.
