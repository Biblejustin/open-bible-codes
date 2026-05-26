# WRR Source Row Crop Packet

Status: no-input row-crop packet for WRR source-row review.
It writes local review crops only; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_row_crop_packet --row-checklist reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --tsv reports/wrr_1994/wrr_primary_table2_row_ocr.tsv --image reports/wrr_1994/wrr_primary_table2_page-06.png --crop-dir reports/wrr_1994/source_review_crops_auto --manual-crop-dir reports/wrr_1994/source_review_crops --out reports/wrr_1994/wrr_source_row_crop_packet.csv --summary-out reports/wrr_1994/wrr_source_row_crop_packet_summary.csv --markdown-out docs/WRR_SOURCE_ROW_CROP_PACKET.md --contact-sheet-out reports/wrr_1994/wrr_source_row_crop_contact_sheet.png --contact-sheet-markdown-out docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md --manifest-out reports/wrr_1994/wrr_source_row_crop_packet.manifest.json
```

## Current Read

- Source rows: 22.
- Auto row crops available: 22.
- Contact sheet available: true at `reports/wrr_1994/wrr_source_row_crop_contact_sheet.png`.
- Existing manual crop rows in checklist: 4.
- Action terms: 43.
- Frontier pairs: 35.
- Boundary: Crops are review aids only; no row transcription, source correction, pair exclusion, or method change is selected by this packet.

## Row Crops

| Rank | Row | Terms | Frontier | Auto crop | Manual crops | Next action |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 1 | `06` | 4 | 4 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row06_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 2 | `14` | 3 | 3 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row14_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 3 | `24` | 3 | 3 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row24_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 4 | `01` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row01_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 5 | `03` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row03_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 6 | `09` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row09_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 7 | `10` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row10_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 8 | `11` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row11_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 9 | `15` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row15_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 10 | `22` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row22_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 11 | `23` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row23_auto.png` | 1 | inspect generated crop against source row before any frontier source decision |
| 12 | `25` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row25_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 13 | `26` | 2 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row26_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 14 | `27` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row27_auto.png` | 1 | inspect generated crop against source row before any frontier source decision |
| 15 | `02` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row02_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 16 | `05` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row05_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 17 | `07` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row07_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 18 | `16` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row16_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 19 | `20` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row20_auto.png` | 0 | inspect generated crop against source row before any frontier source decision |
| 20 | `30` | 4 | 0 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row30_auto.png` | 1 | keep crop as later review aid unless policy scope changes |
| 21 | `32` | 2 | 0 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row32_auto.png` | 1 | keep crop as later review aid unless policy scope changes |
| 22 | `29` | 1 | 0 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row29_auto.png` | 0 | keep crop as later review aid unless policy scope changes |

## Boundary

- These crops are generated from the current local Table 2 page render.
- Crop availability is not transcription verification.
- Manual visual notes remain triage notes unless a separate decision record cites source evidence.
- No row here changes the working WRR source or excludes a pair automatically.
