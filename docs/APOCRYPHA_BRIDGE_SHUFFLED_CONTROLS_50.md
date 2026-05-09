# LXX Apocrypha Bridge Shuffled Controls

Status: shuffled-insertion controls. This is not a claim report.

The control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, but shuffles the block letters before counting bridge rows.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_shuffled_controls --canonical-label LXX --canonical-config configs/example_ebible_grclxx.toml --observed reports/apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --samples 50 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --out reports/apocrypha_bridge_shuffled_controls_50/sample_summary.csv --summary-out reports/apocrypha_bridge_shuffled_controls_50/summary.csv --markdown-out docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md --manifest-out reports/apocrypha_bridge_shuffled_controls_50/manifest.json
```

## Summary

- observed bridge rows: 62
- shuffled samples: 50
- shuffled min/mean/max: 36 / 53.9 / 73
- shuffled samples >= observed: 9
- empirical p_ge: 0.196078

## Samples

| Sample | Seed | Bridge rows | Terms | C→A | A→C | Multi |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20260509 | 50 | 16 | 23 | 27 | 0 |
| 2 | 20260510 | 51 | 22 | 26 | 25 | 0 |
| 3 | 20260511 | 52 | 21 | 30 | 22 | 0 |
| 4 | 20260512 | 50 | 19 | 22 | 28 | 0 |
| 5 | 20260513 | 57 | 25 | 27 | 30 | 0 |
| 6 | 20260514 | 57 | 23 | 32 | 25 | 0 |
| 7 | 20260515 | 51 | 19 | 26 | 25 | 0 |
| 8 | 20260516 | 41 | 18 | 24 | 17 | 0 |
| 9 | 20260517 | 57 | 22 | 28 | 29 | 0 |
| 10 | 20260518 | 68 | 23 | 32 | 36 | 0 |
| 11 | 20260519 | 54 | 23 | 27 | 27 | 0 |
| 12 | 20260520 | 49 | 18 | 28 | 21 | 0 |
| 13 | 20260521 | 64 | 25 | 41 | 23 | 0 |
| 14 | 20260522 | 52 | 21 | 36 | 16 | 0 |
| 15 | 20260523 | 58 | 25 | 25 | 33 | 0 |
| 16 | 20260524 | 42 | 16 | 19 | 23 | 0 |
| 17 | 20260525 | 46 | 20 | 23 | 23 | 0 |
| 18 | 20260526 | 53 | 19 | 22 | 31 | 0 |
| 19 | 20260527 | 66 | 19 | 33 | 33 | 0 |
| 20 | 20260528 | 40 | 16 | 14 | 26 | 0 |
| 21 | 20260529 | 48 | 20 | 26 | 22 | 0 |
| 22 | 20260530 | 42 | 16 | 23 | 19 | 0 |
| 23 | 20260531 | 73 | 25 | 41 | 32 | 0 |
| 24 | 20260532 | 53 | 21 | 29 | 24 | 0 |
| 25 | 20260533 | 66 | 20 | 33 | 33 | 0 |
| 26 | 20260534 | 57 | 16 | 24 | 33 | 0 |
| 27 | 20260535 | 64 | 21 | 39 | 25 | 0 |
| 28 | 20260536 | 52 | 23 | 20 | 32 | 0 |
| 29 | 20260537 | 56 | 17 | 28 | 28 | 0 |
| 30 | 20260538 | 58 | 19 | 35 | 23 | 0 |
| 31 | 20260539 | 73 | 24 | 37 | 36 | 0 |
| 32 | 20260540 | 47 | 23 | 23 | 24 | 0 |
| 33 | 20260541 | 49 | 17 | 22 | 27 | 0 |
| 34 | 20260542 | 48 | 20 | 26 | 22 | 0 |
| 35 | 20260543 | 57 | 20 | 31 | 26 | 0 |
| 36 | 20260544 | 50 | 17 | 31 | 19 | 0 |
| 37 | 20260545 | 36 | 18 | 15 | 21 | 0 |
| 38 | 20260546 | 58 | 22 | 31 | 27 | 0 |
| 39 | 20260547 | 55 | 18 | 27 | 28 | 0 |
| 40 | 20260548 | 45 | 18 | 20 | 25 | 0 |
| 41 | 20260549 | 47 | 15 | 22 | 25 | 0 |
| 42 | 20260550 | 47 | 18 | 25 | 22 | 0 |
| 43 | 20260551 | 57 | 23 | 28 | 29 | 0 |
| 44 | 20260552 | 56 | 16 | 20 | 36 | 0 |
| 45 | 20260553 | 59 | 25 | 31 | 28 | 0 |
| 46 | 20260554 | 47 | 16 | 19 | 28 | 0 |
| 47 | 20260555 | 57 | 21 | 35 | 22 | 0 |
| 48 | 20260556 | 63 | 25 | 31 | 32 | 0 |
| 49 | 20260557 | 62 | 20 | 28 | 34 | 0 |
| 50 | 20260558 | 55 | 22 | 31 | 24 | 0 |

## Read

This is a calibration control. With finite samples, the add-one
empirical p-value remains resolution-limited. Treat the result as
background calibration, not claim evidence.
