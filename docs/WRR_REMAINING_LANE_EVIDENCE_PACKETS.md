# WRR Remaining-Lane Evidence Packets

Status: diagnostic evidence packet for page-image and method residual lanes.
It does not choose source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_remaining_lane_evidence_packets --action-plan reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --row-ocr reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv --out reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv --summary-out reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv --markdown-out docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md --manifest-out reports/wrr_1994/wrr_remaining_lane_evidence_packets.manifest.json
```

## Current Read

- Remaining-lane action terms: 14.
- Residual pair links: 14.
- Minimum-frontier pair links: 4.
- Boundary: No automatic source correction or method change; page-image, method, or pair-universe evidence must be locked first.

## Lane Summary

| Lane | Terms | Pairs | Frontier | Concepts | Evidence required |
| --- | ---: | ---: | ---: | ---: | --- |
| `page_image_near_match_review` | 3 | 3 | 2 | 2 | page-image inspection against near-match OCR |
| `method_or_pair_universe_review` | 11 | 11 | 2 | 8 | method or pair-universe review for OCR-matched missing ordinary hits |

## Action Terms

| Rank | Lane | Term id | Term | Row | Pairs | Frontier | OCR status | Near match | Evidence read |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | `page_image_near_match_review` | `wrr2_19_app_11` | `YWSP+RANY` | `19` | 1 | 1 | not_matched | `d=1 יוספטרני` | near OCR exists, but page image must decide whether it is source evidence |
| 2 | `page_image_near_match_review` | `wrr2_19_app_12` | `YWSPM+RANY` | `19` | 1 | 1 | not_matched | `d=1 יוספמטרני` | near OCR exists, but page image must decide whether it is source evidence |
| 3 | `page_image_near_match_review` | `wrr2_31_app_07` | `$M$` | `31` | 1 | 0 | not_matched | `d=1 שרש` | near OCR exists, but page image must decide whether it is source evidence |
| 4 | `method_or_pair_universe_review` | `wrr2_02_app_03` | `ZR@ABRHM` | `02` | 1 | 1 | matched | `d=0 זרעאברהמ` | OCR matched the imported term; investigate method or pair universe before source edits |
| 5 | `method_or_pair_universe_review` | `wrr2_02_app_05` | `ABRHMYCXQY` | `02` | 1 | 1 | matched | `d=0 אברהמיצחקי` | OCR matched the imported term; investigate method or pair universe before source edits |
| 6 | `method_or_pair_universe_review` | `wrr2_07_app_05` | `DWDAWPNHYM` | `07` | 1 | 0 | matched | `d=0 דודאופנהימ` | OCR matched the imported term; investigate method or pair universe before source edits |
| 7 | `method_or_pair_universe_review` | `wrr2_11_app_05` | `XYYMBNBN$T` | `11` | 1 | 0 | matched | `d=0 חיימבנבנשת` | OCR matched the imported term; investigate method or pair universe before source edits |
| 8 | `method_or_pair_universe_review` | `wrr2_12_app_05` | `XYYMKPWSY` | `12` | 1 | 0 | matched | `d=0 חיימכפוסי` | OCR matched the imported term; investigate method or pair universe before source edits |
| 9 | `method_or_pair_universe_review` | `wrr2_19_app_03` | `YWSP+RNY` | `19` | 1 | 0 | matched | `d=0 יוספטרני` | OCR matched the imported term; investigate method or pair universe before source edits |
| 10 | `method_or_pair_universe_review` | `wrr2_19_app_10` | `YWSPM+RNY` | `19` | 1 | 0 | matched | `d=0 יוספמטרני` | OCR matched the imported term; investigate method or pair universe before source edits |
| 11 | `method_or_pair_universe_review` | `wrr2_20_app_03` | `PRYMGDYM` | `20` | 1 | 0 | matched | `d=0 פרימגדימ` | OCR matched the imported term; investigate method or pair universe before source edits |
| 12 | `method_or_pair_universe_review` | `wrr2_20_app_05` | `YWSPTAWMYM` | `20` | 1 | 0 | matched | `d=0 יוספתאומימ` | OCR matched the imported term; investigate method or pair universe before source edits |
| 13 | `method_or_pair_universe_review` | `wrr2_28_app_05` | `M$HMRGLYT` | `28` | 1 | 0 | matched | `d=0 משהמרגלית` | OCR matched the imported term; investigate method or pair universe before source edits |
| 14 | `method_or_pair_universe_review` | `wrr2_31_app_09` | `$LWMMZRXY` | `31` | 1 | 0 | matched | `d=0 שלוממזרחי` | OCR matched the imported term; investigate method or pair universe before source edits |

## No-Input Boundary

- Page-image near-match rows need page-image review before source edits.
- OCR-matched method rows need method or pair-universe explanation before source edits.
- No remaining-lane term changes the working source automatically.
