# WRR Source-Transcription Evidence Packet

Status: diagnostic evidence packet for source-transcription residual terms.
It does not choose source corrections, row edits, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_transcription_evidence_packet --action-plan reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --row-ocr reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv --table2-bridge reports/wrr_1994/wrr_table2_source_bridge.csv --out reports/wrr_1994/wrr_source_transcription_evidence_packet.csv --row-summary-out reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv --markdown-out docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md --manifest-out reports/wrr_1994/wrr_source_transcription_evidence_packet.manifest.json
```

## Current Read

- Source-transcription action terms: 43.
- Residual pair links: 44.
- Minimum-frontier pair links: 35.
- Row clusters: 22.
- Evidence target: primary Table 2 row transcription or row-alignment evidence.
- Boundary: No automatic source correction; primary row transcription or row-alignment evidence must be locked before changing imported terms.

## Priority Row Clusters

| Rank | Row | Concept | Terms | Pairs | Frontier | Matched row terms | Action terms not matched |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | `06` | `WRR2 06` | 4 | 4 | 4 | `wrr2_06_app_01 M@$YH$M;wrr2_06_app_02 M@$YYHWH;wrr2_06_date_01 /KB/KSLW` | `wrr2_06_app_03 B@LM@$YH$M;wrr2_06_app_04 B@LM@$YYHWH;wrr2_06_app_05 ALY@ZRA$KNZY;wrr2_06_app_06 RBYALY@ZR` |
| 2 | `14` | `WRR2 14` | 3 | 3 | 3 | `wrr2_14_app_01 XWTYAYR;wrr2_14_date_01 /A/+BT` | `wrr2_14_app_02 B@LXWTYAYR;wrr2_14_app_03 YAYRXYYMBKRK;wrr2_14_app_05 RBYYAYRXYYM` |
| 3 | `24` | `WRR2 24` | 3 | 3 | 3 | `wrr2_24_app_03 @MDYN;wrr2_24_app_04 HRY@MDN;wrr2_24_app_05 HRY@MDYN;wrr2_24_app_08 @MDN;wrr2_24_date_01 /L/NYSN` | `wrr2_24_app_06 Y@QBY$RAL@MDN;wrr2_24_app_07 Y@QBY$RAL@MDYN;wrr2_24_app_09 RBYY@QBY$RAL` |
| 4 | `01` | `WRR2 01` | 2 | 2 | 2 | `wrr2_01_app_01 RBYABRHM;wrr2_01_app_02 HRABY;wrr2_01_app_03 HRBABD;wrr2_01_app_04 HRABD;wrr2_01_app_05 HA$KWL;wrr2_01_app_07 RABY;wrr2_01_app_09 RABD` | `wrr2_01_app_06 B@LHA$KWL;wrr2_01_app_08 HRBABBYTDYN` |
| 5 | `03` | `WRR2 03` | 2 | 2 | 2 | `wrr2_03_app_01 RBYABRHM;wrr2_03_app_02 HMLAK;wrr2_03_date_01 /YB/T$RY` | `wrr2_03_app_03 XSDLABRHM;wrr2_03_app_04 B@LXSDLABRHM` |
| 6 | `09` | `WRR2 09` | 2 | 2 | 2 | `wrr2_09_app_01 RBYDWD;wrr2_09_app_02 DWDNY+W;wrr2_09_app_05 NY+W;wrr2_09_date_01 /KX/+BT` | `wrr2_09_app_03 HKWZRYH$NY;wrr2_09_app_04 B@LHKWZRYH$NY` |
| 7 | `10` | `WRR2 10` | 2 | 2 | 2 | `wrr2_10_app_01 RBYXYYM;wrr2_10_date_01 /W/NYSN` | `wrr2_10_app_02 XYYMABWAL@PYH;wrr2_10_app_03 ABWAL@PYH` |
| 8 | `11` | `WRR2 11` | 2 | 2 | 2 | `wrr2_11_app_01 RBYXYYM;wrr2_11_app_02 BNBN$T;wrr2_11_app_05 XYYMBNBN$T;wrr2_11_date_01 /Y+/ALWL` | `wrr2_11_app_03 KNSTHGDWLH;wrr2_11_app_04 B@LKNSTHGDWLH` |
| 9 | `15` | `WRR2 15` | 2 | 2 | 2 | `wrr2_15_app_01 RBYYHWDH;wrr2_15_date_01 /H/X$WN` | `wrr2_15_app_02 YHWDHXSYD;wrr2_15_app_03 YHWDHHXSYD` |
| 10 | `22` | `WRR2 22` | 2 | 2 | 2 | `wrr2_22_app_01 XAGYZ;wrr2_22_app_02 B@LHLQ+;wrr2_22_app_03 HLQ+;wrr2_22_date_01 /KW/$B+` | `wrr2_22_app_04 Y$RALY@QB;wrr2_22_app_05 RBYY$RALY@QB` |
| 11 | `23` | `WRR2 23` | 2 | 2 | 2 | `wrr2_23_date_01 /KB/ALWL` | `wrr2_23_app_03 Y@QBSGL;wrr2_23_app_09 Y@QBMWLYN` |
| 12 | `25` | `WRR2 25` | 2 | 2 | 2 | `wrr2_25_app_01 RBYYCXQ;wrr2_25_app_02 HWRWWYC;wrr2_25_app_03 YCXQHLWY;wrr2_25_date_01 /W/AYR` | `wrr2_25_app_04 RBYAYCQLHMBWRGR;wrr2_25_app_05 YCXQHLWYAY$HWRWWYC` |
| 13 | `26` | `WRR2 26` | 2 | 2 | 1 | `wrr2_26_app_01 RBYMNXM;wrr2_26_app_02 QRWKML;wrr2_26_app_03 RBYM@NDL;wrr2_26_app_04 CMXCDQ;wrr2_26_date_01 /B/$B+` | `wrr2_26_app_05 B@LCMXCDQ;wrr2_26_app_06 MNXMM@NDL` |
| 14 | `27` | `WRR2 27` | 1 | 2 | 1 | `wrr2_27_app_01 RBYM$H;wrr2_27_app_02 ZKWTA;wrr2_27_app_03 ZKWTW;wrr2_27_app_04 M$HZKWT;wrr2_27_app_05 M$HZKWTA;wrr2_27_app_07 MHRMZKWT;wrr2_27_app_08 MHRMZ;wrr2_27_app_14 ZKWT;wrr2_27_date_02 /YW/T$RY` | `wrr2_27_app_13 B@LQWLHRMZ` |
| 15 | `02` | `WRR2 02` | 1 | 1 | 1 | `wrr2_02_app_01 RBYABRHM;wrr2_02_app_02 YCXQY;wrr2_02_app_03 ZR@ABRHM;wrr2_02_app_05 ABRHMYCXQY;wrr2_02_date_01 /YG/SYWN` | `wrr2_02_app_04 B@LZR@ABRHM` |
| 16 | `05` | `WRR2 05` | 1 | 1 | 1 | `wrr2_05_app_01 RBYAHRN;wrr2_05_date_01 /Y+/NYSN` | `wrr2_05_app_02 AHRNHGDWLMQRLYN` |
| 17 | `07` | `WRR2 07` | 1 | 1 | 1 | `wrr2_07_app_01 RBYDWD;wrr2_07_app_02 AWPNHYM;wrr2_07_app_05 DWDAWPNHYM;wrr2_07_date_01 /Z/T$RY` | `wrr2_07_app_04 MHRDAWPNHYM` |
| 18 | `16` | `WRR2 16` | 1 | 1 | 1 | `wrr2_16_app_01 RBYYHWDH;wrr2_16_app_02 MHRY@YA$;wrr2_16_app_04 @YA$;wrr2_16_date_01 /A/T$RY` | `wrr2_16_app_03 YHWDH@YA$` |
| 19 | `20` | `WRR2 20` | 1 | 1 | 1 | `wrr2_20_app_01 RBYYWSP;wrr2_20_app_02 TAWMYM;wrr2_20_app_03 PRYMGDYM;wrr2_20_app_05 YWSPTAWMYM;wrr2_20_date_01 /D/AYR` | `wrr2_20_app_04 B@LPRYMGDYM` |
| 20 | `30` | `WRR2 30` | 4 | 4 | 0 | `wrr2_30_app_01 AXH@R;wrr2_30_app_02 Y$RLBB;wrr2_30_date_01 /A/ADR` | `wrr2_30_app_03 M$NTXSYDYM;wrr2_30_app_04 B@LM$NTXSYDYM;wrr2_30_app_06 @MNWALXYRPALRYQY;wrr2_30_app_08 RBY@MNWALXYRPAL` |
| 21 | `32` | `WRR2 32` | 2 | 2 | 0 | `wrr2_32_app_01 RBY$LMH;wrr2_32_date_01 /KA/TMWZ` | `wrr2_32_app_02 MRKBTHM$NH;wrr2_32_app_03 B@LMRKBTHM$NH` |
| 22 | `29` | `WRR2 29` | 1 | 1 | 0 | `wrr2_29_app_01 RBY@ZRYH;wrr2_29_date_01 /A/ADRA` | `wrr2_29_app_02 @ZRYHPYGW` |

## Priority Terms

| Rank | Action rank | Term id | Term | Row | Pairs | Frontier | OCR status | Variant hits | Evidence read |
| ---: | ---: | --- | --- | --- | ---: | ---: | --- | ---: | --- |
| 1 | 2 | `wrr2_27_app_13` | `B@LQWLHRMZ` | `27` | 2 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 2 | 3 | `wrr2_01_app_06` | `B@LHA$KWL` | `01` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 3 | 4 | `wrr2_01_app_08` | `HRBABBYTDYN` | `01` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 4 | 5 | `wrr2_02_app_04` | `B@LZR@ABRHM` | `02` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 5 | 6 | `wrr2_03_app_03` | `XSDLABRHM` | `03` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 6 | 7 | `wrr2_03_app_04` | `B@LXSDLABRHM` | `03` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 7 | 8 | `wrr2_05_app_02` | `AHRNHGDWLMQRLYN` | `05` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 8 | 9 | `wrr2_06_app_03` | `B@LM@$YH$M` | `06` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 9 | 10 | `wrr2_06_app_04` | `B@LM@$YYHWH` | `06` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 10 | 11 | `wrr2_06_app_05` | `ALY@ZRA$KNZY` | `06` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 11 | 12 | `wrr2_06_app_06` | `RBYALY@ZR` | `06` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 12 | 13 | `wrr2_07_app_04` | `MHRDAWPNHYM` | `07` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 13 | 14 | `wrr2_09_app_03` | `HKWZRYH$NY` | `09` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 14 | 15 | `wrr2_09_app_04` | `B@LHKWZRYH$NY` | `09` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 15 | 16 | `wrr2_10_app_02` | `XYYMABWAL@PYH` | `10` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 16 | 17 | `wrr2_10_app_03` | `ABWAL@PYH` | `10` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 17 | 18 | `wrr2_11_app_03` | `KNSTHGDWLH` | `11` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 18 | 19 | `wrr2_11_app_04` | `B@LKNSTHGDWLH` | `11` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 19 | 20 | `wrr2_14_app_02` | `B@LXWTYAYR` | `14` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 20 | 21 | `wrr2_14_app_03` | `YAYRXYYMBKRK` | `14` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 21 | 22 | `wrr2_14_app_05` | `RBYYAYRXYYM` | `14` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 22 | 23 | `wrr2_15_app_02` | `YHWDHXSYD` | `15` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 23 | 24 | `wrr2_15_app_03` | `YHWDHHXSYD` | `15` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 24 | 25 | `wrr2_16_app_03` | `YHWDH@YA$` | `16` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 25 | 26 | `wrr2_20_app_04` | `B@LPRYMGDYM` | `20` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 26 | 27 | `wrr2_22_app_04` | `Y$RALY@QB` | `22` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 27 | 28 | `wrr2_22_app_05` | `RBYY$RALY@QB` | `22` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 28 | 29 | `wrr2_23_app_03` | `Y@QBSGL` | `23` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 29 | 30 | `wrr2_23_app_09` | `Y@QBMWLYN` | `23` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 30 | 31 | `wrr2_24_app_06` | `Y@QBY$RAL@MDN` | `24` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 31 | 32 | `wrr2_24_app_07` | `Y@QBY$RAL@MDYN` | `24` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 32 | 33 | `wrr2_24_app_09` | `RBYY@QBY$RAL` | `24` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 33 | 34 | `wrr2_25_app_04` | `RBYAYCQLHMBWRGR` | `25` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 34 | 35 | `wrr2_25_app_05` | `YCXQHLWYAY$HWRWWYC` | `25` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 35 | 36 | `wrr2_26_app_05` | `B@LCMXCDQ` | `26` | 1 | 1 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 36 | 37 | `wrr2_26_app_06` | `MNXMM@NDL` | `26` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 37 | 38 | `wrr2_29_app_02` | `@ZRYHPYGW` | `29` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 38 | 39 | `wrr2_30_app_03` | `M$NTXSYDYM` | `30` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 39 | 40 | `wrr2_30_app_04` | `B@LM$NTXSYDYM` | `30` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 40 | 41 | `wrr2_30_app_06` | `@MNWALXYRPALRYQY` | `30` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 41 | 42 | `wrr2_30_app_08` | `RBY@MNWALXYRPAL` | `30` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 42 | 43 | `wrr2_32_app_02` | `MRKBTHM$NH` | `32` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |
| 43 | 44 | `wrr2_32_app_03` | `B@LMRKBTHM$NH` | `32` | 1 | 0 | not_matched | 0 | no simple variant lead; needs primary row transcription or row-alignment evidence before any source edit |

## No-Input Boundary

- This packet is a row-transcription work order, not a correction set.
- Keep imported terms until citable primary row or row-alignment evidence is locked.
- No simple variant lead means do not infer a replacement from ordinary Genesis hits.
- Rows with multiple unresolved terms should be reviewed once by row, not term-by-term in isolation.
