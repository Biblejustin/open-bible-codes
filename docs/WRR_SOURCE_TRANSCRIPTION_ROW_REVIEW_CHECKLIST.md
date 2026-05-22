# WRR Source-Transcription Row Review Checklist

Status: no-input checklist for row-level source-transcription review.
It does not choose row transcriptions, source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_transcription_row_review_checklist --row-summary reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv --out reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --markdown-out docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md --manifest-out reports/wrr_1994/wrr_source_transcription_row_review_checklist.manifest.json
```

## Current Read

- Row review clusters: 22.
- Source-transcription action terms: 43.
- Residual pair links: 44.
- Minimum-frontier pair links: 35.
- Review state: `pending_manual_source_lock`.
- Boundary: No row transcription, source correction, pair exclusion, or method change is selected by this checklist.

## Row Checklist

| Rank | Row | Concept | State | Terms | Pairs | Frontier | Terms to verify | Next manual action |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | `06` | `WRR2 06` | `pending_manual_source_lock` | 4 | 4 | 4 | `wrr2_06_app_03 B@LM@$YH$M;wrr2_06_app_04 B@LM@$YYHWH;wrr2_06_app_05 ALY@ZRA$KNZY;wrr2_06_app_06 RBYALY@ZR` | review row image once before individual term decisions |
| 2 | `14` | `WRR2 14` | `pending_manual_source_lock` | 3 | 3 | 3 | `wrr2_14_app_02 B@LXWTYAYR;wrr2_14_app_03 YAYRXYYMBKRK;wrr2_14_app_05 RBYYAYRXYYM` | review row image once before individual term decisions |
| 3 | `24` | `WRR2 24` | `pending_manual_source_lock` | 3 | 3 | 3 | `wrr2_24_app_06 Y@QBY$RAL@MDN;wrr2_24_app_07 Y@QBY$RAL@MDYN;wrr2_24_app_09 RBYY@QBY$RAL` | review row image once before individual term decisions |
| 4 | `01` | `WRR2 01` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_01_app_06 B@LHA$KWL;wrr2_01_app_08 HRBABBYTDYN` | review row image once before individual term decisions |
| 5 | `03` | `WRR2 03` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_03_app_03 XSDLABRHM;wrr2_03_app_04 B@LXSDLABRHM` | review row image once before individual term decisions |
| 6 | `09` | `WRR2 09` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_09_app_03 HKWZRYH$NY;wrr2_09_app_04 B@LHKWZRYH$NY` | review row image once before individual term decisions |
| 7 | `10` | `WRR2 10` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_10_app_02 XYYMABWAL@PYH;wrr2_10_app_03 ABWAL@PYH` | review row image once before individual term decisions |
| 8 | `11` | `WRR2 11` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_11_app_03 KNSTHGDWLH;wrr2_11_app_04 B@LKNSTHGDWLH` | review row image once before individual term decisions |
| 9 | `15` | `WRR2 15` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_15_app_02 YHWDHXSYD;wrr2_15_app_03 YHWDHHXSYD` | review row image once before individual term decisions |
| 10 | `22` | `WRR2 22` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_22_app_04 Y$RALY@QB;wrr2_22_app_05 RBYY$RALY@QB` | review row image once before individual term decisions |
| 11 | `23` | `WRR2 23` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_23_app_03 Y@QBSGL;wrr2_23_app_09 Y@QBMWLYN` | review row image once before individual term decisions |
| 12 | `25` | `WRR2 25` | `pending_manual_source_lock` | 2 | 2 | 2 | `wrr2_25_app_04 RBYAYCQLHMBWRGR;wrr2_25_app_05 YCXQHLWYAY$HWRWWYC` | review row image once before individual term decisions |
| 13 | `26` | `WRR2 26` | `pending_manual_source_lock` | 2 | 2 | 1 | `wrr2_26_app_05 B@LCMXCDQ;wrr2_26_app_06 MNXMM@NDL` | review row image once before individual term decisions |
| 14 | `27` | `WRR2 27` | `pending_manual_source_lock` | 1 | 2 | 1 | `wrr2_27_app_13 B@LQWLHRMZ` | review row image before any frontier pair decision |
| 15 | `02` | `WRR2 02` | `pending_manual_source_lock` | 1 | 1 | 1 | `wrr2_02_app_04 B@LZR@ABRHM` | review row image before any frontier pair decision |
| 16 | `05` | `WRR2 05` | `pending_manual_source_lock` | 1 | 1 | 1 | `wrr2_05_app_02 AHRNHGDWLMQRLYN` | review row image before any frontier pair decision |
| 17 | `07` | `WRR2 07` | `pending_manual_source_lock` | 1 | 1 | 1 | `wrr2_07_app_04 MHRDAWPNHYM` | review row image before any frontier pair decision |
| 18 | `16` | `WRR2 16` | `pending_manual_source_lock` | 1 | 1 | 1 | `wrr2_16_app_03 YHWDH@YA$` | review row image before any frontier pair decision |
| 19 | `20` | `WRR2 20` | `pending_manual_source_lock` | 1 | 1 | 1 | `wrr2_20_app_04 B@LPRYMGDYM` | review row image before any frontier pair decision |
| 20 | `30` | `WRR2 30` | `pending_manual_source_lock` | 4 | 4 | 0 | `wrr2_30_app_03 M$NTXSYDYM;wrr2_30_app_04 B@LM$NTXSYDYM;wrr2_30_app_06 @MNWALXYRPALRYQY;wrr2_30_app_08 RBY@MNWALXYRPAL` | review after frontier rows unless policy scope changes |
| 21 | `32` | `WRR2 32` | `pending_manual_source_lock` | 2 | 2 | 0 | `wrr2_32_app_02 MRKBTHM$NH;wrr2_32_app_03 B@LMRKBTHM$NH` | review after frontier rows unless policy scope changes |
| 22 | `29` | `WRR2 29` | `pending_manual_source_lock` | 1 | 1 | 0 | `wrr2_29_app_02 @ZRYHPYGW` | review after frontier rows unless policy scope changes |

## Required Decision Record

- Cite the primary row image or source-list row transcription used.
- State row and column alignment evidence.
- Record keep, correct, exclude, or method/pair-universe decision outside this checklist.
- Preserve the working source until that decision record exists.
