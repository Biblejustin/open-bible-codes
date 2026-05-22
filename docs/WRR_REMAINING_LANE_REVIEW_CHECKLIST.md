# WRR Remaining-Lane Review Checklist

Status: no-input checklist for page-image and method/pair-universe review.
It does not choose source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_remaining_lane_review_checklist --packet reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv --summary reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv --out reports/wrr_1994/wrr_remaining_lane_review_checklist.csv --markdown-out docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md --manifest-out reports/wrr_1994/wrr_remaining_lane_review_checklist.manifest.json
```

## Current Read

- Remaining-lane checklist terms: 14.
- Residual pair links: 14.
- Minimum-frontier pair links: 4.
- Page-image terms: 3.
- Method/pair-universe terms: 11.
- Boundary: No source correction, method change, or pair exclusion is selected by this checklist.

## Lane Summary

| Lane | Terms | Pairs | Frontier | Evidence required |
| --- | ---: | ---: | ---: | --- |
| `page_image_near_match_review` | 3 | 3 | 2 | page-image inspection against near-match OCR |
| `method_or_pair_universe_review` | 11 | 11 | 2 | method or pair-universe review for OCR-matched missing ordinary hits |

## Checklist

| Rank | Lane | State | Term id | Term | Row | Pairs | Frontier | Near match | Next manual action |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `page_image_near_match_review` | `pending_page_image_lock` | `wrr2_19_app_11` | `YWSP+RANY` | `19` | 1 | 1 | `d=1 יוספטרני` | inspect page image before any source correction |
| 2 | `page_image_near_match_review` | `pending_page_image_lock` | `wrr2_19_app_12` | `YWSPM+RANY` | `19` | 1 | 1 | `d=1 יוספמטרני` | inspect page image before any source correction |
| 3 | `page_image_near_match_review` | `pending_page_image_lock` | `wrr2_31_app_07` | `$M$` | `31` | 1 | 0 | `d=1 שרש` | inspect page image before any source correction |
| 4 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_02_app_03` | `ZR@ABRHM` | `02` | 1 | 1 | `d=0 זרעאברהמ` | resolve method or pair universe before frontier pair decision |
| 5 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_02_app_05` | `ABRHMYCXQY` | `02` | 1 | 1 | `d=0 אברהמיצחקי` | resolve method or pair universe before frontier pair decision |
| 6 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_07_app_05` | `DWDAWPNHYM` | `07` | 1 | 0 | `d=0 דודאופנהימ` | review after frontier method rows unless scope changes |
| 7 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_11_app_05` | `XYYMBNBN$T` | `11` | 1 | 0 | `d=0 חיימבנבנשת` | review after frontier method rows unless scope changes |
| 8 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_12_app_05` | `XYYMKPWSY` | `12` | 1 | 0 | `d=0 חיימכפוסי` | review after frontier method rows unless scope changes |
| 9 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_19_app_03` | `YWSP+RNY` | `19` | 1 | 0 | `d=0 יוספטרני` | review after frontier method rows unless scope changes |
| 10 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_19_app_10` | `YWSPM+RNY` | `19` | 1 | 0 | `d=0 יוספמטרני` | review after frontier method rows unless scope changes |
| 11 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_20_app_03` | `PRYMGDYM` | `20` | 1 | 0 | `d=0 פרימגדימ` | review after frontier method rows unless scope changes |
| 12 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_20_app_05` | `YWSPTAWMYM` | `20` | 1 | 0 | `d=0 יוספתאומימ` | review after frontier method rows unless scope changes |
| 13 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_28_app_05` | `M$HMRGLYT` | `28` | 1 | 0 | `d=0 משהמרגלית` | review after frontier method rows unless scope changes |
| 14 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_31_app_09` | `$LWMMZRXY` | `31` | 1 | 0 | `d=0 שלוממזרחי` | review after frontier method rows unless scope changes |

## Required Decision Record

- Page-image near-match rows need cited page-image transcription evidence.
- Method rows need an explicit method or pair-universe explanation for zero ordinary hits.
- Preserve the working source until that decision record exists.
