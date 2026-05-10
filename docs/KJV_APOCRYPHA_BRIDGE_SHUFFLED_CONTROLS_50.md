# KJVA Apocrypha Bridge Shuffled Controls (50 Samples)

Status: shuffled-insertion controls. This is not a claim report.

The control keeps the canonical prefix and apocrypha/deuterocanon block
length fixed, but shuffles the block letters before counting bridge rows.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_shuffled_controls --canonical-label KJVA --canonical-config configs/example_ebible_engkjv_apocrypha.toml --observed reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --terms terms/english_search_terms.csv --samples 50 --seed 20260509 --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --resume-samples --out reports/kjv_apocrypha_bridge_shuffled_controls_50/sample_summary.csv --summary-out reports/kjv_apocrypha_bridge_shuffled_controls_50/summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md --manifest-out reports/kjv_apocrypha_bridge_shuffled_controls_50/manifest.json
```

## Summary

- observed bridge rows: 350
- shuffled samples: 50
- shuffled min/mean/max: 155 / 186.06 / 216
- shuffled samples >= observed: 0
- empirical p_ge: 0.019608

## Samples

| Sample | Seed | Bridge rows | Terms | C→A | A→C | Multi |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 20260509 | 172 | 57 | 81 | 91 | 0 |
| 2 | 20260510 | 185 | 64 | 93 | 92 | 0 |
| 3 | 20260511 | 168 | 57 | 84 | 84 | 0 |
| 4 | 20260512 | 184 | 61 | 90 | 94 | 0 |
| 5 | 20260513 | 178 | 68 | 88 | 90 | 0 |
| 6 | 20260514 | 192 | 65 | 85 | 107 | 0 |
| 7 | 20260515 | 216 | 62 | 100 | 116 | 0 |
| 8 | 20260516 | 175 | 56 | 91 | 84 | 0 |
| 9 | 20260517 | 200 | 58 | 105 | 95 | 0 |
| 10 | 20260518 | 169 | 57 | 74 | 95 | 0 |
| 11 | 20260519 | 191 | 57 | 89 | 102 | 0 |
| 12 | 20260520 | 187 | 56 | 99 | 88 | 0 |
| 13 | 20260521 | 186 | 69 | 109 | 77 | 0 |
| 14 | 20260522 | 191 | 62 | 95 | 96 | 0 |
| 15 | 20260523 | 194 | 56 | 103 | 91 | 0 |
| 16 | 20260524 | 191 | 58 | 102 | 89 | 0 |
| 17 | 20260525 | 206 | 67 | 100 | 106 | 0 |
| 18 | 20260526 | 166 | 57 | 89 | 77 | 0 |
| 19 | 20260527 | 189 | 65 | 87 | 102 | 0 |
| 20 | 20260528 | 211 | 67 | 103 | 108 | 0 |
| 21 | 20260529 | 193 | 63 | 103 | 90 | 0 |
| 22 | 20260530 | 197 | 60 | 96 | 101 | 0 |
| 23 | 20260531 | 205 | 61 | 113 | 92 | 0 |
| 24 | 20260532 | 155 | 53 | 61 | 94 | 0 |
| 25 | 20260533 | 193 | 61 | 92 | 101 | 0 |
| 26 | 20260534 | 176 | 63 | 81 | 95 | 0 |
| 27 | 20260535 | 208 | 61 | 103 | 105 | 0 |
| 28 | 20260536 | 161 | 54 | 71 | 90 | 0 |
| 29 | 20260537 | 185 | 65 | 88 | 97 | 0 |
| 30 | 20260538 | 204 | 67 | 103 | 101 | 0 |
| 31 | 20260539 | 183 | 50 | 83 | 100 | 0 |
| 32 | 20260540 | 180 | 55 | 87 | 93 | 0 |
| 33 | 20260541 | 194 | 59 | 87 | 107 | 0 |
| 34 | 20260542 | 159 | 62 | 82 | 77 | 0 |
| 35 | 20260543 | 190 | 67 | 96 | 94 | 0 |
| 36 | 20260544 | 175 | 60 | 83 | 92 | 0 |
| 37 | 20260545 | 185 | 54 | 91 | 94 | 0 |
| 38 | 20260546 | 209 | 62 | 101 | 108 | 0 |
| 39 | 20260547 | 187 | 63 | 76 | 111 | 0 |
| 40 | 20260548 | 199 | 61 | 103 | 96 | 0 |
| 41 | 20260549 | 172 | 61 | 88 | 84 | 0 |
| 42 | 20260550 | 201 | 61 | 91 | 110 | 0 |
| 43 | 20260551 | 175 | 57 | 81 | 94 | 0 |
| 44 | 20260552 | 190 | 59 | 86 | 104 | 0 |
| 45 | 20260553 | 181 | 58 | 92 | 89 | 0 |
| 46 | 20260554 | 175 | 55 | 78 | 97 | 0 |
| 47 | 20260555 | 162 | 59 | 70 | 92 | 0 |
| 48 | 20260556 | 183 | 61 | 86 | 97 | 0 |
| 49 | 20260557 | 193 | 66 | 90 | 103 | 0 |
| 50 | 20260558 | 182 | 54 | 86 | 96 | 0 |

## Read

This is a calibration control. With finite samples, the add-one
empirical p-value remains resolution-limited. Treat the result as
background calibration, not claim evidence.
