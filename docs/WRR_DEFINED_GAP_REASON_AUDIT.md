# WRR Defined Gap Reason Audit

Status: diagnostic-only failure taxonomy for the current WRR all-lane
corrected-distance outputs. It is not a WRR reproduction.

This report classifies why current rows fail the `c(w,w')` definedness
gate. It uses existing corrected-distance outputs and does not run a
new ELS search.

Reproduce:

```bash
python3 -m scripts.analyze_wrr_defined_gap_reasons --pair-summary reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv --pair-table reports/wrr_1994/wrr2_pair_eligibility_table.csv --out reports/wrr_1994/wrr_defined_gap_reasons.csv --term-out reports/wrr_1994/wrr_defined_gap_term_burden.csv --markdown-out docs/WRR_DEFINED_GAP_REASON_AUDIT.md --manifest-out reports/wrr_1994/wrr_defined_gap_reason_audit.manifest.json
```

## Reason Counts

| Run | Reason | Pairs | Run defined | Gap to source-cited count | Read |
| --- | --- | ---: | ---: | ---: | --- |
| all_lanes_cap250 | `defined` | 50 | 50 | 113 | corrected distance currently defined |
| all_lanes_cap250 | `ordinary_missing_appellation_hits` | 80 | 50 | 113 | ordinary pair blocked because appellation has zero ordinary hits in this run |
| all_lanes_cap250 | `ordinary_missing_date_hits` | 18 | 50 | 113 | ordinary pair blocked because date has zero ordinary hits in this run |
| all_lanes_cap250 | `ordinary_missing_both_terms` | 32 | 50 | 113 | ordinary pair blocked because both terms have zero ordinary hits in this run |
| all_lanes_cap250 | `under_minimum_valid_perturbations` | 2 | 50 | 113 | ordinary pair exists but fewer than minimum valid perturbations |
| all_lanes_cap1000 | `defined` | 72 | 72 | 91 | corrected distance currently defined |
| all_lanes_cap1000 | `ordinary_missing_appellation_hits` | 83 | 72 | 91 | ordinary pair blocked because appellation has zero ordinary hits in this run |
| all_lanes_cap1000 | `ordinary_missing_date_hits` | 12 | 72 | 91 | ordinary pair blocked because date has zero ordinary hits in this run |
| all_lanes_cap1000 | `ordinary_missing_both_terms` | 15 | 72 | 91 | ordinary pair blocked because both terms have zero ordinary hits in this run |
| all_lanes_cap1000_program | `defined` | 72 | 72 | 91 | corrected distance currently defined |
| all_lanes_cap1000_program | `ordinary_missing_appellation_hits` | 83 | 72 | 91 | ordinary pair blocked because appellation has zero ordinary hits in this run |
| all_lanes_cap1000_program | `ordinary_missing_date_hits` | 12 | 72 | 91 | ordinary pair blocked because date has zero ordinary hits in this run |
| all_lanes_cap1000_program | `ordinary_missing_both_terms` | 15 | 72 | 91 | ordinary pair blocked because both terms have zero ordinary hits in this run |

## Best Current Run

- `all_lanes_cap1000` defines 72 of 163 source-cited distances.
- Gap to the source-cited count remains 91.
- Ordinary-missing rows total 110; under-minimum rows total 0.

## Top Ordinary-Missing Terms In Best Run

| Side | Term id | Term | Normalized | Ordinary hits | Defined rows | Pairs blocked | Reasons |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| date | `wrr2_27_date_01` | `/+Z/T$RY` | `+ZT$RY` | 0 | 8 | 14 | `ordinary_missing_date_hits;ordinary_missing_both_terms` |
| date | `wrr2_06_date_01` | `/KB/KSLW` | `KBKSLW` | 0 | 41 | 6 | `ordinary_missing_date_hits;ordinary_missing_both_terms` |
| date | `wrr2_02_date_01` | `/YG/SYWN` | `YGSYWN` | 0 | 45 | 5 | `ordinary_missing_date_hits;ordinary_missing_both_terms` |
| appellation | `wrr2_27_app_04` | `M$HZKWT` | `M$HZKWT` | 0 | 6 | 2 | `ordinary_missing_appellation_hits;ordinary_missing_both_terms` |
| appellation | `wrr2_27_app_05` | `M$HZKWTA` | `M$HZKWT)` | 0 | 0 | 2 | `ordinary_missing_appellation_hits;ordinary_missing_both_terms` |
| appellation | `wrr2_27_app_06` | `M$HZKWTW` | `M$HZKWTW` | 0 | 1 | 2 | `ordinary_missing_appellation_hits;ordinary_missing_both_terms` |
| appellation | `wrr2_27_app_07` | `MHRMZKWT` | `MHRMZKWT` | 0 | 1 | 2 | `ordinary_missing_appellation_hits;ordinary_missing_both_terms` |
| appellation | `wrr2_27_app_13` | `B@LQWLHRMZ` | `B(LQWLHRMZ` | 0 | 0 | 2 | `ordinary_missing_appellation_hits;ordinary_missing_both_terms` |
| date | `wrr2_05_date_01` | `/Y+/NYSN` | `Y+NYSN` | 0 | 28 | 2 | `ordinary_missing_date_hits;ordinary_missing_both_terms` |
| appellation | `wrr2_01_app_01` | `RBYABRHM` | `RBY)BRHM` | 0 | 6 | 1 | `ordinary_missing_appellation_hits` |
| appellation | `wrr2_01_app_06` | `B@LHA$KWL` | `B(LH)$KWL` | 0 | 0 | 1 | `ordinary_missing_appellation_hits` |
| appellation | `wrr2_01_app_08` | `HRBABBYTDYN` | `HRB)BBYTDYN` | 0 | 0 | 1 | `ordinary_missing_appellation_hits` |

## Interpretation

- A row can only define corrected distance when the ordinary pair is valid
  and the minimum perturbation count is met.
- Zero ordinary hits for an imported appellation or date term is a source
  alignment problem before it is a permutation problem.
- This audit narrows the next WRR work toward term normalization, source
  row boundaries, and the final pair-universe rule.
