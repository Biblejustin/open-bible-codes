# WRR Manual Decision Record Worksheet

Status: no-input worksheet for future WRR manual decision records.
It does not populate `data/study/mappings/wrr_manual_decision_records.csv`.
Header-only current status means no correction, transcription, method change, replacement lock, or pair exclusion has been selected.

Reproduce:

```bash
python3 -m scripts.build_wrr_manual_decision_record_worksheet --register reports/wrr_1994/wrr_manual_decision_register.csv --records-template data/study/mappings/wrr_manual_decision_records.csv --out reports/wrr_1994/wrr_manual_decision_record_worksheet.csv --markdown-out docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md --manifest-out reports/wrr_1994/wrr_manual_decision_record_worksheet.manifest.json
```

## Current Read

- Worksheet rows: 37.
- Source-policy/pair-rule rows: 1.
- Source-transcription row-cluster rows: 22.
- Page-image rows: 3.
- Method/pair-universe rows: 11.
- Target records file: `data/study/mappings/wrr_manual_decision_records.csv`.

## Lock Row Fields

`decision_id,register_decision_rank,decision_lane,review_state,decision_target,source_checklist,decision_status,selected_action,evidence_citation,evidence_summary,locked_by,locked_at,notes`

The worksheet gives exact `decision_id` and register fields. Evidence, selected action, reviewer, and lock date still require manual input.

## Worksheet

| Decision id | Rank | Lane | State | Target | Checklist | Evidence prompt | Suggested actions |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `wrr_decision_001` | 1 | `source_policy_pair_rule` | `pending_source_policy_pair_rule_lock` | `Chelm source-policy/pair-rule target` | `docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md` | cite primary source and pair-rule evidence before changing the working source | `no_source_change;source_policy_correction;pair_rule_change;deferred_no_lock` |
| `wrr_decision_002` | 2 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 06` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_003` | 3 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 14` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_004` | 4 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 24` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_005` | 5 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 01` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_006` | 6 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 03` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_007` | 7 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 09` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_008` | 8 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 10` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_009` | 9 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 11` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_010` | 10 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 15` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_011` | 11 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 22` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_012` | 12 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 23` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_013` | 13 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 25` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_014` | 14 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 02` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_015` | 15 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 05` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_016` | 16 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 07` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_017` | 17 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 16` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_018` | 18 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 20` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_019` | 19 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 26` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_020` | 20 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 27` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_021` | 21 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 29` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_022` | 22 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 30` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_023` | 23 | `source_transcription_row_cluster` | `pending_manual_source_lock` | `row 32` | `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` | cite row image or source-list transcription plus row/column alignment evidence | `no_source_change;row_transcription_update;pair_exclusion;deferred_no_lock` |
| `wrr_decision_024` | 24 | `page_image_near_match` | `pending_page_image_lock` | `wrr2_19_app_11` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | cite page-image transcription evidence | `no_source_change;source_correction;pair_exclusion;deferred_no_lock` |
| `wrr_decision_025` | 25 | `page_image_near_match` | `pending_page_image_lock` | `wrr2_19_app_12` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | cite page-image transcription evidence | `no_source_change;source_correction;pair_exclusion;deferred_no_lock` |
| `wrr_decision_026` | 26 | `page_image_near_match` | `pending_page_image_lock` | `wrr2_31_app_07` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | cite page-image transcription evidence | `no_source_change;source_correction;pair_exclusion;deferred_no_lock` |
| `wrr_decision_027` | 27 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_02_app_03` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_028` | 28 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_02_app_05` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_029` | 29 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_07_app_05` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_030` | 30 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_11_app_05` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_031` | 31 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_12_app_05` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_032` | 32 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_19_app_03` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_033` | 33 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_19_app_10` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_034` | 34 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_20_app_03` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_035` | 35 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_20_app_05` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_036` | 36 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_28_app_05` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
| `wrr_decision_037` | 37 | `method_pair_universe` | `pending_method_pair_universe_lock` | `wrr2_31_app_09` | `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` | explain zero ordinary hits with explicit method or pair-universe evidence | `method_lock;pair_universe_lock;pair_exclusion;deferred_no_lock` |
