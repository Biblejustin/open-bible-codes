# WRR Manual Decision Register

Status: consolidated lane register for WRR manual-decision records.
It defines decision ranks, lanes, targets, and evidence requirements; current lock status lives in `data/study/mappings/wrr_manual_decision_records.csv`.
It does not choose source corrections, row transcriptions, pair exclusions, replacement locks, or method changes.

Reproduce:

```bash
python3 -m scripts.build_wrr_manual_decision_register --source-policy reports/wrr_1994/wrr_source_policy_review_checklist.csv --row-checklist reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --remaining reports/wrr_1994/wrr_remaining_lane_review_checklist.csv --out reports/wrr_1994/wrr_manual_decision_register.csv --summary-out reports/wrr_1994/wrr_manual_decision_register_summary.csv --markdown-out docs/WRR_MANUAL_DECISION_REGISTER.md --manifest-out reports/wrr_1994/wrr_manual_decision_register.manifest.json
```

## Current Read

- Manual decision rows: 37.
- Action terms represented: 58.
- Residual pair links represented: 59.
- Minimum-frontier pair links represented: 40.
- Source-policy/pair-rule decision rows: 1.
- Source-transcription row-cluster decision rows: 22.
- Page-image decision rows: 3.
- Method/pair-universe decision rows: 11.
- Boundary: No source correction, row transcription, pair exclusion, replacement lock, or method change is selected by this register.

## Lane Summary

| Lane | Decisions | Terms | Pairs | Frontier | State |
| --- | ---: | ---: | ---: | ---: | --- |
| `source_policy_pair_rule` | 1 | 1 | 1 | 1 | `pending_source_policy_pair_rule_lock` |
| `source_transcription_row_cluster` | 22 | 43 | 44 | 35 | `pending_manual_source_lock` |
| `page_image_near_match` | 3 | 3 | 3 | 2 | `pending_page_image_lock` |
| `method_pair_universe` | 11 | 11 | 11 | 2 | `pending_method_pair_universe_lock` |

## Decision Register

| Rank | Lane | State | Target | Concept | Row | Terms | Pairs | Frontier | Checklist | Next manual action |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | `source_policy_pair_rule` | `pending_source_policy_pair_rule_lock` | `Chelm source-policy/pair-rule target` | `WRR2 32` | `32` | 1 | 1 | 1 | `docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md` | cite primary source/pair-rule evidence before changing working source |
| 2 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 06` | `WRR2 06` | `06` | 4 | 4 | 4 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 3 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 14` | `WRR2 14` | `14` | 3 | 3 | 3 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 4 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 24` | `WRR2 24` | `24` | 3 | 3 | 3 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 5 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 01` | `WRR2 01` | `01` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 6 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 03` | `WRR2 03` | `03` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 7 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 09` | `WRR2 09` | `09` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 8 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 10` | `WRR2 10` | `10` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 9 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 11` | `WRR2 11` | `11` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 10 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 15` | `WRR2 15` | `15` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 11 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 22` | `WRR2 22` | `22` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 12 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 23` | `WRR2 23` | `23` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 13 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 25` | `WRR2 25` | `25` | 2 | 2 | 2 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 14 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 02` | `WRR2 02` | `02` | 1 | 1 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image before any frontier pair decision |
| 15 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 05` | `WRR2 05` | `05` | 1 | 1 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image before any frontier pair decision |
| 16 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 07` | `WRR2 07` | `07` | 1 | 1 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image before any frontier pair decision |
| 17 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 16` | `WRR2 16` | `16` | 1 | 1 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image before any frontier pair decision |
| 18 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 20` | `WRR2 20` | `20` | 1 | 1 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image before any frontier pair decision |
| 19 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 26` | `WRR2 26` | `26` | 2 | 2 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image once before individual term decisions |
| 20 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 27` | `WRR2 27` | `27` | 1 | 2 | 1 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review row image before any frontier pair decision |
| 21 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 29` | `WRR2 29` | `29` | 1 | 1 | 0 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review after frontier rows unless policy scope changes |
| 22 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 30` | `WRR2 30` | `30` | 4 | 4 | 0 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review after frontier rows unless policy scope changes |
| 23 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 32` | `WRR2 32` | `32` | 2 | 2 | 0 | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | review after frontier rows unless policy scope changes |
| 24 | `page_image_near_match` | `pending_page_image_lock` | `wrr2_19_app_11` | `WRR2 19` | `19` | 1 | 1 | 1 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | inspect page image before any source correction |
| 25 | `page_image_near_match` | `pending_page_image_lock` | `wrr2_19_app_12` | `WRR2 19` | `19` | 1 | 1 | 1 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | inspect page image before any source correction |
| 26 | `page_image_near_match` | `pending_page_image_lock` | `wrr2_31_app_07` | `WRR2 31` | `31` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | inspect page image before any source correction |
| 27 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_02_app_03` | `WRR2 02` | `02` | 1 | 1 | 1 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | resolve method or pair universe before frontier pair decision |
| 28 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_02_app_05` | `WRR2 02` | `02` | 1 | 1 | 1 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | resolve method or pair universe before frontier pair decision |
| 29 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_07_app_05` | `WRR2 07` | `07` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 30 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_11_app_05` | `WRR2 11` | `11` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 31 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_12_app_05` | `WRR2 12` | `12` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 32 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_19_app_03` | `WRR2 19` | `19` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 33 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_19_app_10` | `WRR2 19` | `19` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 34 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_20_app_03` | `WRR2 20` | `20` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 35 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_20_app_05` | `WRR2 20` | `20` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 36 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_28_app_05` | `WRR2 28` | `28` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |
| 37 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_31_app_09` | `WRR2 31` | `31` | 1 | 1 | 0 | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | review after frontier method rows unless scope changes |

## Required Decision Records

- Source-policy/pair-rule rows need citable source and pair-rule evidence.
- Source-transcription row clusters need cited row image or source-list transcription plus row/column alignment evidence.
- Page-image rows need cited page-image transcription evidence.
- Method/pair-universe rows need an explicit explanation for zero ordinary hits.
- Use `data/study/mappings/wrr_manual_decision_records.csv` for current lock status.
- This register remains the rank/lane/target inventory for those records.
