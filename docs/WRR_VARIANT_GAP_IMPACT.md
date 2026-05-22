# WRR Variant Gap Impact

Status: diagnostic-only join from current blocked WRR pair rows to
zero-hit one-edit variant leads. It is not a source correction, not a
term replacement, and not a WRR reproduction.

Reproduce:

```bash
python3 -m scripts.analyze_wrr_variant_gap_impact --blocked-pairs reports/wrr_1994/wrr_defined_gap_blocked_pairs.csv --variants reports/wrr_1994/wrr_zero_hit_variant_probe.csv --out reports/wrr_1994/wrr_variant_gap_impact.csv --summary-out reports/wrr_1994/wrr_variant_gap_impact_summary.csv --markdown-out docs/WRR_VARIANT_GAP_IMPACT.md --manifest-out reports/wrr_1994/wrr_variant_gap_impact.manifest.json
```

## Best Current Run

- Best run label: `all_lanes_cap1000`.

| Impact status | Pairs | Row OCR pair statuses | Top concepts |
| --- | ---: | --- | --- |
| `all_blocking_terms_have_variant_hit` | 51 | `31 both_matched, 5 both_not_matched, 15 mixed` | `WRR2 27 17, WRR2 19 3, WRR2 26 3, WRR2 02 2, WRR2 06 2` |
| `no_blocking_term_variant_hit` | 50 | `9 both_matched, 2 both_not_matched, 39 mixed` | `WRR2 19 4, WRR2 30 4, WRR2 11 3, WRR2 14 3, WRR2 20 3` |
| `some_blocking_terms_have_variant_hit` | 9 | `2 both_matched, 1 both_not_matched, 6 mixed` | `WRR2 06 4, WRR2 02 3, WRR2 05 1, WRR2 27 1` |

## Top Variant-Lead Blocked Pairs

| Pair | Concept | Reason | Blocking terms | Variant hits | Variant rules |
| --- | --- | --- | --- | --- | --- |
| `wrr2_01_app_01__wrr2_01_date_01` | `WRR2 01` | `ordinary_missing_appellation_hits` | `RBYABRHM` | `4` | `delete_one@2:RY)BRHM` |
| `wrr2_02_app_01__wrr2_02_date_01` | `WRR2 02` | `ordinary_missing_both_terms` | `RBYABRHM;/YG/SYWN` | `4;68` | `delete_one@2:RY)BRHM;delete_one@2:YSYWN` |
| `wrr2_02_app_02__wrr2_02_date_01` | `WRR2 02` | `ordinary_missing_date_hits` | `/YG/SYWN` | `68` | `delete_one@2:YSYWN` |
| `wrr2_03_app_01__wrr2_03_date_01` | `WRR2 03` | `ordinary_missing_appellation_hits` | `RBYABRHM` | `4` | `delete_one@2:RY)BRHM` |
| `wrr2_05_app_01__wrr2_05_date_01` | `WRR2 05` | `ordinary_missing_date_hits` | `/Y+/NYSN` | `28` | `delete_one@2:YNYSN` |
| `wrr2_06_app_01__wrr2_06_date_01` | `WRR2 06` | `ordinary_missing_date_hits` | `/KB/KSLW` | `73` | `delete_one@4:KBKLW` |
| `wrr2_06_app_02__wrr2_06_date_01` | `WRR2 06` | `ordinary_missing_both_terms` | `M@$YYHWH;/KB/KSLW` | `14;73` | `delete_one@2:M$YYHWH;delete_one@4:KBKLW` |
| `wrr2_09_app_02__wrr2_09_date_01` | `WRR2 09` | `ordinary_missing_appellation_hits` | `DWDNY+W` | `7` | `delete_one@6:DWDNYW` |
| `wrr2_13_app_02__wrr2_13_date_01` | `WRR2 13` | `ordinary_missing_appellation_hits` | `XYYM$BTY` | `4` | `delete_one@1:YYM$BTY` |
| `wrr2_16_app_02__wrr2_16_date_01` | `WRR2 16` | `ordinary_missing_appellation_hits` | `MHRY@YA$` | `5` | `delete_one@2:MRY(Y)$` |
| `wrr2_17_app_01__wrr2_17_date_01` | `WRR2 17` | `ordinary_missing_appellation_hits` | `RBYYHWSP` | `2` | `delete_one@7:RBYYHWP` |
| `wrr2_18_app_01__wrr2_18_date_01` | `WRR2 18` | `ordinary_missing_appellation_hits` | `RBYYHW$@` | `4` | `delete_mater@6:RBYYH$(` |

## Interpretation

- This only prioritizes source-review work.
- A variant lead does not make the original pair valid.
- Claim-grade work still needs source transcription and pair-rule locks.
