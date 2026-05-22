# WRR Zero-Hit Variant Probe

Status: diagnostic-only one-edit probe for imported WRR2 terms with zero
Genesis hits in the count smoke run. It is not a source correction and
not a WRR reproduction.

Reproduce:

```bash
python3 -m scripts.analyze_wrr_zero_hit_variant_probe --config configs/example_koren_genesis.toml --counts reports/wrr_1994/wrr2_genesis_counts.csv --row-ocr reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv --min-skip 2 --max-skip 1000 --direction both --out reports/wrr_1994/wrr_zero_hit_variant_probe.csv --summary-out reports/wrr_1994/wrr_zero_hit_variant_probe_summary.csv --markdown-out docs/WRR_ZERO_HIT_VARIANT_PROBE.md --manifest-out reports/wrr_1994/wrr_zero_hit_variant_probe.manifest.json
```

## Summary

| Category | Zero terms | With variant hit | Without variant hit | Variant hit total |
| --- | ---: | ---: | ---: | ---: |
| wrr_appellation | 105 | 48 | 57 | 2981 |
| wrr_date | 7 | 7 | 0 | 1358 |

## Top Variant Hits

| Term id | Concept | Rule | Original | Variant | Row OCR | Hits |
| --- | --- | --- | --- | --- | --- | ---: |
| `wrr2_19_app_09` | `WRR2 19` | `delete_one@6` | `HMHRY+` | `HMHRY` | `matched` | 581 |
| `wrr2_09_date_01` | `WRR2 09` | `delete_one@3` | `KX+BT` | `KXBT` | `matched` | 410 |
| `wrr2_19_app_05` | `WRR2 19` | `delete_one@2` | `M+R)NY` | `MR)NY` | `matched` | 358 |
| `wrr2_28_app_02` | `WRR2 28` | `delete_one@3` | `MRGLYT` | `MRLYT` | `matched` | 280 |
| `wrr2_32_date_01` | `WRR2 32` | `delete_one@6` | `K)TMWZ` | `K)TMW` | `matched` | 223 |
| `wrr2_13_app_04` | `WRR2 13` | `delete_one@5` | `HMHRX$` | `HMHR$` | `not_matched` | 210 |
| `wrr2_19_date_01` | `WRR2 19` | `delete_one@6` | `YDTMWZ` | `YDTMW` | `matched` | 182 |
| `wrr2_13_app_04` | `WRR2 13` | `delete_one@4` | `HMHRX$` | `HMHX$` | `not_matched` | 112 |
| `wrr2_25_app_02` | `WRR2 25` | `delete_one@7` | `HWRWWYC` | `HWRWWY` | `matched` | 112 |
| `wrr2_13_app_04` | `WRR2 13` | `delete_one@6` | `HMHRX$` | `HMHRX` | `not_matched` | 99 |
| `wrr2_12_app_04` | `WRR2 12` | `delete_one@6` | `B(LHNS` | `B(LHN` | `matched` | 83 |
| `wrr2_06_date_01` | `WRR2 06` | `delete_one@4` | `KBKSLW` | `KBKLW` | `matched` | 73 |

## Interpretation

- Variant hits are leads for source-normalization review only.
- A hit here does not authorize replacing a WRR term or promoting a claim.
- Rows with row OCR matched but zero original hits remain source-rule
  and normalization questions before any permutation question.
