# Strong Full-Span Exact-Center Matrix Exports

This report records matrix/letter-path exports for the exact-center rows. It is
a review aid for table-style inspection of the hidden paths in both Bible and
control corpora.

## Reproduce

```bash
python3 -m scripts.build_dynamic_span_exact_center_extension_hits --corpus UHB --corpus EBIBLE_WLC --corpus KJV --corpus LXX --corpus TCG_NT
python3 -m scripts.build_dynamic_span_exact_center_extension_hits --out reports/dynamic_skip_focus/strong_full_span_exact_center_all_hits_compatible.csv --manifest-out reports/dynamic_skip_focus/strong_full_span_exact_center_all_hits_compatible.manifest.json
python3 -m els matrix --config configs/example_uhb.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.csv --corpus-label UHB --out reports/dynamic_skip_focus/exact_center_matrix/matrix_uhb_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_uhb_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_uhb.manifest.json
python3 -m els matrix --config configs/example_ebible_hebwlc.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.csv --corpus-label EBIBLE_WLC --out reports/dynamic_skip_focus/exact_center_matrix/matrix_ebible_wlc_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_ebible_wlc_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_ebible_wlc.manifest.json
python3 -m els matrix --config configs/example_ebible_engkjv.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.csv --corpus-label KJV --out reports/dynamic_skip_focus/exact_center_matrix/matrix_kjv_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_kjv_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_kjv.manifest.json
python3 -m els matrix --config configs/example_ebible_grclxx.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.csv --corpus-label LXX --out reports/dynamic_skip_focus/exact_center_matrix/matrix_lxx_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_lxx_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_lxx.manifest.json
python3 -m els matrix --config configs/example_ebible_grctcgnt.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.csv --corpus-label TCG_NT --out reports/dynamic_skip_focus/exact_center_matrix/matrix_tcg_nt_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_tcg_nt_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_tcg_nt.manifest.json
python3 -m els matrix --config configs/nonbible_hebrew_pby_bialik.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_all_hits_compatible.csv --corpus-label HEB_PBY_BIALIK --out reports/dynamic_skip_focus/exact_center_matrix/matrix_heb_pby_bialik_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_heb_pby_bialik_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_heb_pby_bialik.manifest.json
python3 -m els matrix --config configs/nonbible_english_pg_shakespeare.toml --hits reports/dynamic_skip_focus/strong_full_span_exact_center_all_hits_compatible.csv --corpus-label ENG_PG_SHAKESPEARE --out reports/dynamic_skip_focus/exact_center_matrix/matrix_eng_pg_shakespeare_letters.csv --summary-out reports/dynamic_skip_focus/exact_center_matrix/matrix_eng_pg_shakespeare_summary.csv --manifest-out reports/dynamic_skip_focus/exact_center_matrix/matrix_eng_pg_shakespeare.manifest.json
```

## Scope

| Corpus | Class | Exact-center paths | Matrix letter rows | Summary CSV | Letter CSV |
| --- | --- | ---: | ---: | --- | --- |
| UHB | Bible | 941 | 3,764 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_uhb_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_uhb_letters.csv` |
| EBIBLE_WLC | Bible | 75 | 300 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_ebible_wlc_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_ebible_wlc_letters.csv` |
| KJV | Bible | 492 | 2,460 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_kjv_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_kjv_letters.csv` |
| LXX | Bible | 70 | 420 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_lxx_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_lxx_letters.csv` |
| TCG_NT | Bible | 4 | 12 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_tcg_nt_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_tcg_nt_letters.csv` |
| HEB_PBY_BIALIK | Control | 8,210 | 32,840 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_heb_pby_bialik_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_heb_pby_bialik_letters.csv` |
| ENG_PG_SHAKESPEARE | Control | 2 | 10 | `reports/dynamic_skip_focus/exact_center_matrix/matrix_eng_pg_shakespeare_summary.csv` | `reports/dynamic_skip_focus/exact_center_matrix/matrix_eng_pg_shakespeare_letters.csv` |

Totals: 9,794 exact-center paths and 39,806 matrix letter rows. Bible rows
account for 1,582 paths and 6,956 letters; control rows account for 8,212 paths
and 32,850 letters.

## Example

The TCG_NT `Gog` exact-center row has four matrix summaries:

| Skip | Direction | Row width | Rows spanned | Columns spanned | Start | Center | End |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- |
| -4568 | backward | 4568 | 3 | 1 | REV 22:8 | REV 20:8 | REV 18:16 |
| -17 | backward | 17 | 3 | 1 | REV 20:8 | REV 20:8 | REV 20:8 |
| 17 | forward | 17 | 3 | 1 | REV 20:8 | REV 20:8 | REV 20:8 |
| 4568 | forward | 4568 | 3 | 1 | REV 18:16 | REV 20:8 | REV 22:8 |

## Read

- The default matrix row width is `abs(skip)`, so each ELS path forms a vertical
  column in that layout.
- The letter CSVs preserve each letter offset, row, column, ref, surface word,
  and normalized word.
- These exports are useful for manual table review, not statistical scoring by
  themselves.
- The control matrix rows are intentionally preserved because high-volume
  non-Bible exact-center paths are part of the comparison problem, not noise to
  hide.
