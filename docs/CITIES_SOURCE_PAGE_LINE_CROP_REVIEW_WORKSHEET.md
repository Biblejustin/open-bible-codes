# Cities Source Page Line Crop Review Worksheet

Status: no-input worksheet for future Cities source-page line-crop review.
It organizes local line-crop images for later human visual review but does not transcribe rows or import source rows.
No OCR body text or source-script body text appears in this doc, CSV, or manifest.
worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_review_worksheet --packet reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv --html-review-aid reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_review.html --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_worksheet.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_WORKSHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_worksheet.manifest.json
```

## Current Read

- Line-crop review rows: 203.
- Unique table pages: 4.
- Table-candidate page rows: 203.
- Crop images available: 203.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Review state: `pending_line_crop_review`.
- Local HTML review aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_review.html`.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Counts

| Transcription id | Line-crop review rows |
| --- | ---: |
| `cities_source_transcription_001` | 44 |
| `cities_source_transcription_002` | 55 |
| `cities_source_transcription_003` | 54 |
| `cities_source_transcription_004` | 50 |

## Worksheet Scope

- This worksheet organizes visual review only.
- Line crops are not verified source rows.
- Human review must decide whether each crop is table row, header, note, noise, or needs wider context.
- Readable transcription, row/column alignment evidence, and an explicit import decision are still required before any source row can be imported.
