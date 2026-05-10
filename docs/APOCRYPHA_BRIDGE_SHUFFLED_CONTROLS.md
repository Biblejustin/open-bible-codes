# LXX Apocrypha Bridge Shuffled Controls (5 Samples)

Status: shuffled-insertion controls. This is not a claim report.

The control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, but shuffles the block letters before counting bridge rows.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_shuffled_controls --canonical-label LXX --canonical-config configs/example_ebible_grclxx.toml --observed reports/apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --samples 5 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/apocrypha_bridge_shuffled_controls/sample_summary.csv --summary-out reports/apocrypha_bridge_shuffled_controls/summary.csv --markdown-out docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md --manifest-out reports/apocrypha_bridge_shuffled_controls/manifest.json
```

## Summary

- observed bridge rows: 62
- shuffled samples: 5
- shuffled min/mean/max: 50 / 52.0 / 57
- shuffled samples >= observed: 0
- empirical p_ge: 0.166667

## Samples

| Sample | Seed | Bridge rows | Terms | C→A | A→C | Multi |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20260509 | 50 | 16 | 23 | 27 | 0 |
| 2 | 20260510 | 51 | 22 | 26 | 25 | 0 |
| 3 | 20260511 | 52 | 21 | 30 | 22 | 0 |
| 4 | 20260512 | 50 | 19 | 22 | 28 | 0 |
| 5 | 20260513 | 57 | 25 | 27 | 30 | 0 |

## Read

This is a calibration control. With finite samples, the add-one
empirical p-value remains resolution-limited. Treat the result as
background calibration, not claim evidence.
