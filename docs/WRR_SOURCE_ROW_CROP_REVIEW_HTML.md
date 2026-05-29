# WRR Source Row Crop Review HTML

Status: local ignored HTML review aid for WRR source-row crops.
The HTML file displays source-row crop images only and embeds no OCR text or source-script text.
Tracked files contain no OCR body text or source-script body text.
Local ignored WRR source-row crop HTML review aid; HTML displays row-crop images only, tracked files contain no OCR body text or source-script body text, no row transcription, no source correction, no pair exclusion, no method change

Reproduce:

```bash
python3 -m scripts.build_wrr_source_row_crop_review_html --crop-packet reports/wrr_1994/wrr_source_row_crop_packet.csv --html-out reports/wrr_1994/wrr_source_row_crop_review.html --summary-out reports/wrr_1994/wrr_source_row_crop_review_html_summary.csv --markdown-out docs/WRR_SOURCE_ROW_CROP_REVIEW_HTML.md --manifest-out reports/wrr_1994/wrr_source_row_crop_review_html.manifest.json
```

## Current Read

- HTML crop review aid: `reports/wrr_1994/wrr_source_row_crop_review.html`.
- HTML rows: 22.
- HTML embeds source text: `false`.
- HTML crop image rows: 22.
- Source-row crop rows: 22.
- Auto crops available: 22.
- Manual crop rows: 4.
- Action terms: 43.
- Frontier pairs: 35.
- Row transcriptions: 0.
- Source corrections: 0.
- Pair exclusions: 0.
- Method changes: 0.
- Boundary: Local ignored WRR source-row crop HTML review aid; HTML displays row-crop images only, tracked files contain no OCR body text or source-script body text, no row transcription, no source correction, no pair exclusion, no method change

## Row Crops

| Rank | Row | Terms | Frontier | Auto crop |
| ---: | --- | ---: | ---: | --- |
| 1 | `06` | 4 | 4 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row06_auto.png` |
| 2 | `14` | 3 | 3 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row14_auto.png` |
| 3 | `24` | 3 | 3 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row24_auto.png` |
| 4 | `01` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row01_auto.png` |
| 5 | `03` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row03_auto.png` |
| 6 | `09` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row09_auto.png` |
| 7 | `10` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row10_auto.png` |
| 8 | `11` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row11_auto.png` |
| 9 | `15` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row15_auto.png` |
| 10 | `22` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row22_auto.png` |
| 11 | `23` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row23_auto.png` |
| 12 | `25` | 2 | 2 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row25_auto.png` |
| 13 | `26` | 2 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row26_auto.png` |
| 14 | `27` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row27_auto.png` |
| 15 | `02` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row02_auto.png` |
| 16 | `05` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row05_auto.png` |
| 17 | `07` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row07_auto.png` |
| 18 | `16` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row16_auto.png` |
| 19 | `20` | 1 | 1 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row20_auto.png` |
| 20 | `30` | 4 | 0 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row30_auto.png` |
| 21 | `32` | 2 | 0 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row32_auto.png` |
| 22 | `29` | 1 | 0 | `reports/wrr_1994/source_review_crops_auto/wrr_table2_row29_auto.png` |

## Boundary

- The ignored HTML file displays generated row-crop images only.
- The crop view is not transcription and does not decide source-row admissibility.
- Future source changes still require readable transcription, row/column alignment evidence, and an explicit decision record.
- No row here changes the working WRR source, excludes a pair, changes method rules, or locks replacement spellings.
