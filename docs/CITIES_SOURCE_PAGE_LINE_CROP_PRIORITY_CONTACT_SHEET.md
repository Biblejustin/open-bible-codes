# Cities Source Page Line Crop Priority Contact Sheet

Status: local visual contact sheets for Cities source-page line-crop triage priorities.
These contact sheets group crop images by priority without transcribing Hebrew or importing source rows.
Tracked files contain no OCR body text or source-script body text.
triage only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_priority_contact_sheet --triage reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.csv --base-dir reports/cities_pdf_recovery_probe/source_page_line_crops/priority_contact_sheets --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_contact_sheet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_contact_sheet_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_CONTACT_SHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_contact_sheet.manifest.json
```

## Current Read

- Priority contact sheets: 4.
- Priority contact sheets available: 4.
- Line crop rows: 203.
- Line crop images found: 203.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: priority contact sheets only; local line-crop images are visual review aids, no OCR body text or source-script body text in tracked files, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Contact Sheets

| Rank | Priority | Line crops | Image rows | Sheet | Dimensions |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | `priority_1_dense_text` | 120 | 120 | `reports/cities_pdf_recovery_probe/source_page_line_crops/priority_contact_sheets/priority_1_dense_text_line_crops.png` | 1008 x 18230 |
| 2 | `priority_2_medium_text` | 71 | 71 | `reports/cities_pdf_recovery_probe/source_page_line_crops/priority_contact_sheets/priority_2_medium_text_line_crops.png` | 1008 x 10782 |
| 3 | `priority_3_short_text` | 12 | 12 | `reports/cities_pdf_recovery_probe/source_page_line_crops/priority_contact_sheets/priority_3_short_text_line_crops.png` | 1008 x 1814 |
| 4 | `priority_4_no_text` | 0 | 0 | `reports/cities_pdf_recovery_probe/source_page_line_crops/priority_contact_sheets/priority_4_no_text_line_crops.png` | 1008 x 142 |

## Boundary

- Priority contact sheets are not transcription verification.
- Image review can speed visual sorting, but it does not read or import Hebrew source rows.
- Any future import still needs explicit source-row evidence and an import decision.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
