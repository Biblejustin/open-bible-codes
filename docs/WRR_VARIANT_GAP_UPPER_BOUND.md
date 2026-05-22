# WRR Variant Gap Upper Bound

Status: diagnostic-only upper bound. This does not replace terms, does
not authorize source corrections, and is not a WRR reproduction.

Reproduce:

```bash
python3 -m scripts.analyze_wrr_variant_gap_upper_bound --defined-pair-summary reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv --variant-gap-summary reports/wrr_1994/wrr_variant_gap_impact_summary.csv --out reports/wrr_1994/wrr_variant_gap_upper_bound.csv --markdown-out docs/WRR_VARIANT_GAP_UPPER_BOUND.md --manifest-out reports/wrr_1994/wrr_variant_gap_upper_bound.manifest.json
```

## Upper-Bound Table

| Run | Current defined | Gap to 163 | All blockers have simple variant | Some blockers | No blockers | Upper-bound defined | Residual gap | Gap coverage % | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| all_lanes_cap250 | 50 | 113 | 71 | 18 | 41 | 121 | 42 | 62.83 | simple one-edit variant leads cannot close the current defined-distance gap |
| all_lanes_cap1000 | 72 | 91 | 51 | 9 | 50 | 123 | 40 | 56.04 | simple one-edit variant leads cannot close the current defined-distance gap |
| all_lanes_cap1000_program | 72 | 91 | 51 | 9 | 50 | 123 | 40 | 56.04 | simple one-edit variant leads cannot close the current defined-distance gap |

## Current Read

- Best current run: `all_lanes_cap1000`.
- Current defined distances: 72 of 163.
- Simple one-edit variant leads cover all blockers for at most 51 blocked pairs.
- Even if every covered simple variant lead were valid source evidence, the upper bound is 123 defined distances.
- Residual gap after that upper bound: 40.
- Therefore simple one-edit variants alone cannot explain the full 163-distance count gap under the current run.
- This is source-review triage only; accepting any variant still requires a citable source rule.
