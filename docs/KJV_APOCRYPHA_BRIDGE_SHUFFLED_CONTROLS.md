# KJVA Apocrypha Bridge Shuffled Controls (5 Samples)

Status: shuffled-insertion controls. This is not a claim report.

The control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, but shuffles the block letters before counting bridge rows.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_shuffled_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/english_search_terms.csv --samples 5 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_bridge_shuffled_controls/sample_summary.csv --summary-out reports/kjv_apocrypha_bridge_shuffled_controls/summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md --manifest-out reports/kjv_apocrypha_bridge_shuffled_controls/manifest.json
```

## Summary

- observed bridge rows: 350
- shuffled samples: 5
- shuffled min/mean/max: 168 / 177.4 / 185
- shuffled samples >= observed: 0
- empirical p_ge: 0.166667

## Samples

| Sample | Seed | Bridge rows | Terms | C→A | A→C | Multi |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20260509 | 172 | 57 | 81 | 91 | 0 |
| 2 | 20260510 | 185 | 64 | 93 | 92 | 0 |
| 3 | 20260511 | 168 | 57 | 84 | 84 | 0 |
| 4 | 20260512 | 184 | 61 | 90 | 94 | 0 |
| 5 | 20260513 | 178 | 68 | 88 | 90 | 0 |

## Read

This is a calibration control. With finite samples, the add-one
empirical p-value remains resolution-limited. Treat the result as
background calibration, not claim evidence.
