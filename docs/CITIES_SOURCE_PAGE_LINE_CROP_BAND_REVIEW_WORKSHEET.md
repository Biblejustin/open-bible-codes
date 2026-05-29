# Cities Source Page Line Crop Band Review Worksheet

Status: no-input worksheet for future Cities source-page line-crop band review.
It reduces the 203 line crops into coordinate bands for later human visual review.
No OCR body text or source-script body text appears in this doc, CSV, or manifest.
band review worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_band_review_worksheet --band-map reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map.csv --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_worksheet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_worksheet_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_WORKSHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_worksheet.manifest.json
```

## Current Read

- Band review rows: 16.
- Source line rows represented: 203.
- Unique table pages: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Review state: `pending_band_visual_review`.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: band review worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Bands

| Transcription id | Review bands |
| --- | ---: |
| `cities_source_transcription_001` | 7 |
| `cities_source_transcription_002` | 2 |
| `cities_source_transcription_003` | 2 |
| `cities_source_transcription_004` | 5 |

## Review Rows

| Review rank | Page | Lines | Crop rows | Dominant priority |
| ---: | --- | --- | ---: | --- |
| 1 | `cities_source_transcription_001` | 1-1 | 1 | `priority_2_medium_text` |
| 2 | `cities_source_transcription_001` | 2-2 | 1 | `priority_1_dense_text` |
| 3 | `cities_source_transcription_001` | 3-15 | 13 | `priority_1_dense_text` |
| 4 | `cities_source_transcription_001` | 16-19 | 4 | `priority_1_dense_text` |
| 5 | `cities_source_transcription_001` | 20-20 | 1 | `priority_2_medium_text` |
| 6 | `cities_source_transcription_001` | 21-26 | 6 | `priority_1_dense_text` |
| 7 | `cities_source_transcription_001` | 27-44 | 18 | `priority_1_dense_text` |
| 8 | `cities_source_transcription_002` | 1-27 | 27 | `priority_1_dense_text` |
| 9 | `cities_source_transcription_002` | 28-55 | 28 | `priority_1_dense_text` |
| 10 | `cities_source_transcription_003` | 1-2 | 2 | `priority_1_dense_text` |
| 11 | `cities_source_transcription_003` | 3-54 | 52 | `priority_1_dense_text` |
| 12 | `cities_source_transcription_004` | 1-2 | 2 | `priority_1_dense_text` |
| 13 | `cities_source_transcription_004` | 3-7 | 5 | `priority_1_dense_text` |
| 14 | `cities_source_transcription_004` | 8-9 | 2 | `priority_1_dense_text` |
| 15 | `cities_source_transcription_004` | 10-12 | 3 | `priority_1_dense_text` |
| 16 | `cities_source_transcription_004` | 13-50 | 38 | `priority_2_medium_text` |

## Boundary

- This worksheet organizes coordinate-band review only.
- A band review row is not a verified source row, table row, transcription, or city-name record.
- Any future import still needs readable row evidence and an explicit import decision.
