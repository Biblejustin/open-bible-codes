# WRR Method-Lane Wide-Skip Probe

Status: diagnostic probe for OCR-matched WRR method-lane terms.
It does not choose source corrections, method changes, or pair exclusions.

## Setup

```bash
python3 -m scripts.analyze_wrr_method_lane_wide_skip --method-packet reports/wrr_1994/wrr_method_pair_universe_evidence_packet.csv --config configs/example_koren_genesis.toml --max-skip 5000 --direction both --jobs 1 --out reports/wrr_1994/wrr_method_lane_wide_skip_probe.csv --summary-out reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv --markdown-out docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md --manifest-out reports/wrr_1994/wrr_method_lane_wide_skip_probe.manifest.json
```

## Current Read

- method-lane terms: 11.
- max skip probed: 5000.
- profile skips: 250;1000;2500;5000.
- terms with any wider-skip hit: 0.
- terms still zero through max skip: 11.
- total hits through max skip: 0.
- boundary: Wide-skip hits are diagnostic only; no source correction, method change, or pair exclusion is selected.

## Term Results

| Rank | Term id | Term | Hits <=1000 | Hits <=5000 | First hit | Read |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | `wrr2_12_app_05` | `XYYMKPWSY` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 2 | `wrr2_28_app_05` | `M$HMRGLYT` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 3 | `wrr2_07_app_05` | `DWDAWPNHYM` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 4 | `wrr2_31_app_09` | `$LWMMZRXY` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 5 | `wrr2_20_app_03` | `PRYMGDYM` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 6 | `wrr2_20_app_05` | `YWSPTAWMYM` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 7 | `wrr2_11_app_05` | `XYYMBNBN$T` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 8 | `wrr2_19_app_03` | `YWSP+RNY` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 9 | `wrr2_19_app_10` | `YWSPM+RNY` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 10 | `wrr2_02_app_03` | `ZR@ABRHM` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |
| 11 | `wrr2_02_app_05` | `ABRHMYCXQY` | 0 | 0 | none | No ordinary Genesis ELS hit found through skip 5000; this is not a near-cap miss under the wide-skip probe. |

## Cautions

- This is a cap-sensitivity diagnostic, not a WRR reproduction result.
- Absence through wider skips does not establish that the source row is wrong.
- No row here changes the locked local WRR method report.
- Exact published reproduction remains caveated by the documented 163-distance gap.
