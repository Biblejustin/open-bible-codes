# WRR D(w) Formula Sensitivity

Status: sensitivity packet for the selected printed `D(w)` main rule.

This compares the printed WRR skip-cap formula and the reported WRR-program
formula across existing corrected-distance outputs.

## Reproduce

```bash
python3 -m scripts.analyze_wrr_dw_formula_sensitivity --skip-summary reports/wrr_1994/wrr2_skip_caps_summary.csv --variants reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv --direct-printed-summary reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv --direct-program-summary reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged_summary.csv --direct-printed reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv --direct-program reports/wrr_1994/direct_all/highcap_1000_program/wrr2_corrected_distance_all_lanes_merged.csv --out reports/wrr_1994/wrr_dw_formula_sensitivity.csv --changed-out reports/wrr_1994/wrr_dw_formula_changed_pairs.csv --markdown-out docs/WRR_DW_FORMULA_SENSITIVITY.md --manifest-out reports/wrr_1994/wrr_dw_formula_sensitivity.manifest.json
```

## Summary

| Scope | Rows | Printed defined | Program defined | Changed pairs | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| skip_cap_profile | 120 |  |  |  | profile only; printed D(w) selected as main |
| smoke_length_5_8_cap250 | 86 | 28 | 28 |  | smoke lane sensitivity; printed D(w) main, program sensitivity |
| all_lanes_cap1000 | 182 | 72 | 72 | 0 | row-level printed/program comparison; printed D(w) main, program sensitivity |

## Skip-Cap Profile

| Measure | Count |
| --- | ---: |
| Program cap below printed | 13 |
| Program cap equal printed | 107 |
| Program cap above printed | 0 |
| Printed target-unreached rows | 55 |
| Program target-unreached rows | 55 |

## Changed Pairs

No pair rows changed between all-lane cap-1000 printed and program formula outputs.

## Interpretation

- Printed `D(w)` is the selected main rule for current WRR diagnostics.
- Current all-lane cap-1000 diagnostics show no row-level printed/program difference.
- Reported-program `D(w)` remains required sensitivity output.
