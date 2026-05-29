# Cities Source Page Line Crop Priority Review Worksheet

Status: priority-ordered worksheet for future Cities source-page line-crop review.
It joins triage rank, crop image paths, and priority contact sheet paths without transcribing Hebrew or importing source rows.
No OCR body text or source-script body text appears in this doc, CSV, or manifest.
priority worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_priority_review_worksheet --triage reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.csv --priority-contact reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_contact_sheet.csv --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_WORKSHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet.manifest.json
```

## Current Read

- Priority review rows: 203.
- Unique table pages: 4.
- Priority contact sheets: 4.
- Priority contact sheets available: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Review state: `pending_priority_line_crop_review`.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: priority worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Priority Counts

| Priority | Review rows |
| --- | ---: |
| `priority_1_dense_text` | 120 |
| `priority_2_medium_text` | 71 |
| `priority_3_short_text` | 12 |
| `priority_4_no_text` | 0 |

## Worksheet Scope

- This worksheet organizes visual review in triage priority order only.
- Priority order is not transcription and is not source-row verification.
- Every row still needs visual role classification and readable source evidence before import.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
