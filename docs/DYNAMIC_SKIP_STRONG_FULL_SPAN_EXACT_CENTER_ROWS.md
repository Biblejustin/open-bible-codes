# Dynamic Skip Exact-Center Rows

This report exports only hit rows where the normalized hidden term exactly
matches the normalized surface word at the ELS center.

## Reproduce

```bash
python3 -m scripts.export_dynamic_span_exact_center_rows --plan reports/dynamic_skip_focus/strong_bible_over_control_full_span_plan.csv --plan reports/dynamic_skip_focus/strong_control_exact_center_full_span_plan.csv --hit-file reports/dynamic_skip_focus/strong_bible_over_control_manageable_full_span_hits.csv --hit-file reports/dynamic_skip_focus/strong_control_manageable_exact_center_full_span_hits.csv --out reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv --summary reports/dynamic_skip_focus/strong_full_span_exact_center_rows_summary.csv --markdown-out docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ROWS.md
```

## Scope

- plan files: 2
- hit files: 2
- partition sources scanned: 365
- hit-file sources scanned: 2
- scanned hit rows: 356,494,786
- exact-center rows exported: 9,794
- exact row CSV: `reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv`
- summary CSV: `reports/dynamic_skip_focus/strong_full_span_exact_center_rows_summary.csv`

## Term Summary

| Corpus | Term | Source | Hits scanned | Exact center | Exact perM | Top center refs |
| --- | --- | --- | ---: | ---: | ---: | --- |
| HEB_PBY_BIALIK | `dyn_messiah_h` | `partition` | 110,129,394 | 7,059 | 64.097329 | PBY Bialik=7059 |
| HEB_PBY_BIALIK | `dyn_yeshua_h` | `partition` | 206,897,417 | 1,151 | 5.563143 | PBY Bialik=1151 |
| UHB | `dyn_yeshua_h` | `partition` | 11,151,829 | 941 | 84.380777 | NEH 8:17=85; EZR 2:2=83; EZR 3:9=73; EZR 2:6=73; NEH 9:5=70; NEH 12:8=69; EZR 10:18=68; NEH 7:11=67; NEH 9:4=66; EZR 2:36=63 |
| KJV | `dyn_jesus_e` | `partition` | 79,657 | 492 | 6,176.481665 | MAT 4:10=4; MRK 10:5=4; MAT 8:34=3; MAT 2:1=3; LUK 17:17=3; MAT 18:1=3; LUK 9:42=3; MAT 12:15=3; MRK 5:27=3; MAT 21:24=3 |
| EBIBLE_WLC | `dyn_messiah_h` | `partition` | 5,252,863 | 75 | 14.277928 | 2SA 1:21=33; 2SA 23:1=30; LAM 4:20=11; DAN 9:26=1 |
| LXX | `dyn_jesus_g` | `partition` | 243,700 | 70 | 287.238408 | JOS 8:3=5; JOS 22:7=3; JOS 18:3=3; JOS 10:24=2; JOS 5:13=2; JOS 24:30=2; JOS 6:16=2; NEH 9:5=2; JOS 4:20=2; JOS 9:2=2 |
| TCG_NT | `dyn_gog_g` | `partition` | 2,000,884 | 4 | 1.999116 | REV 20:8=4 |
| ENG_PG_SHAKESPEARE | `dyn_jesus_e` | `partition` | 87,353 | 2 | 22.895607 | PG Shakespeare=2 |
| GRC_PERSEUS_HERODOTUS | `dyn_gog_g` | `partition` | 3,079,794 | 0 | 0.000000 |  |
| GRC_PERSEUS_HERODOTUS | `dyn_jesus_g` | `hit_file` | 16,741 | 0 | 0.000000 |  |
| KJV | `dyn_netanyahu_e` | `hit_file` | 27 | 0 | 0.000000 |  |
| KJV | `dyn_simsberry_e` | `hit_file` | 2 | 0 | 0.000000 |  |
| LXX | `dyn_russia_g` | `partition` | 2,218,044 | 0 | 0.000000 |  |
| LXX | `dyn_vance_g` | `partition` | 14,641,657 | 0 | 0.000000 |  |
| TCG_NT | `dyn_magog_g` | `hit_file` | 3,271 | 0 | 0.000000 |  |
| TR_NT | `dyn_netanyahu_g` | `hit_file` | 1 | 0 | 0.000000 |  |
| UXLC | `dyn_iran_h` | `partition` | 692,152 | 0 | 0.000000 |  |

## Read

- Exact-center rows are review flags, not claim evidence by themselves.
- A high exact-center rate can reflect ordinary surface vocabulary in the corpus.
- Use this with language-matched controls and version/source distribution.
- Non-Bible controls can use source-level center refs; use `center_source`, `center_word_index`, and offsets in the row CSV for exact local traceability.
