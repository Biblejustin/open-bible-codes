# WRR Method/Pair-Universe Evidence Packet

Status: diagnostic packet for OCR-matched WRR residual terms.
It does not choose source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_method_pair_universe_evidence_packet --remaining-packet reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --counts reports/wrr_1994/wrr2_genesis_counts.csv --corrected-distance reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged.csv --out reports/wrr_1994/wrr_method_pair_universe_evidence_packet.csv --summary-out reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv --markdown-out docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md --manifest-out reports/wrr_1994/wrr_method_pair_universe_evidence_packet.manifest.json
```

## Current Read

- Method/pair-universe action terms: 11.
- OCR-matched terms: 11.
- Zero skip-250 appellation counts: 11.
- Zero high-cap appellation ordinary hits: 11.
- Both sides zero high-cap ordinary hits: 2.
- Boundary: No source correction or method change is selected; OCR-matched zero-hit terms remain a method/pair-universe diagnostic.

## Action Terms

| Rank | Term id | Term | Pair | App hits 250 | App hits 1000 | Date hits 1000 | Valid perturbations | Status | Read |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | `wrr2_12_app_05` | `XYYMKPWSY` | `wrr2_12_app_05__wrr2_12_date_01` | 0 | 0 | 10 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 2 | `wrr2_28_app_05` | `M$HMRGLYT` | `wrr2_28_app_05__wrr2_28_date_01` | 0 | 0 | 10 | 1 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 3 | `wrr2_07_app_05` | `DWDAWPNHYM` | `wrr2_07_app_05__wrr2_07_date_01` | 0 | 0 | 9 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 4 | `wrr2_31_app_09` | `$LWMMZRXY` | `wrr2_31_app_09__wrr2_31_date_01` | 0 | 0 | 8 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 5 | `wrr2_20_app_03` | `PRYMGDYM` | `wrr2_20_app_03__wrr2_20_date_01` | 0 | 0 | 7 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 6 | `wrr2_20_app_05` | `YWSPTAWMYM` | `wrr2_20_app_05__wrr2_20_date_01` | 0 | 0 | 7 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 7 | `wrr2_11_app_05` | `XYYMBNBN$T` | `wrr2_11_app_05__wrr2_11_date_01` | 0 | 0 | 4 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 8 | `wrr2_19_app_03` | `YWSP+RNY` | `wrr2_19_app_03__wrr2_19_date_01` | 0 | 0 | 1 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 9 | `wrr2_19_app_10` | `YWSPM+RNY` | `wrr2_19_app_10__wrr2_19_date_01` | 0 | 0 | 1 | 0 | ordinary_not_valid | OCR matched the appellation, but the appellation has zero ordinary Genesis hits under current search rules; not a quick source correction. |
| 10 | `wrr2_02_app_03` | `ZR@ABRHM` | `wrr2_02_app_03__wrr2_02_date_01` | 0 | 0 | 0 | 0 | ordinary_not_valid | OCR matched the appellation, but both sides have zero high-cap ordinary hits in the current run; investigate method and pair universe. |
| 11 | `wrr2_02_app_05` | `ABRHMYCXQY` | `wrr2_02_app_05__wrr2_02_date_01` | 0 | 0 | 0 | 0 | ordinary_not_valid | OCR matched the appellation, but both sides have zero high-cap ordinary hits in the current run; investigate method and pair universe. |

## No-Input Boundary

- OCR match is not enough to define a WRR corrected distance.
- Zero ordinary hits keep these rows in method or pair-universe review.
- No row here changes the working source or excludes a pair automatically.
