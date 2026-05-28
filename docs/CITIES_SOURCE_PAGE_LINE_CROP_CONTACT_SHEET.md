# Cities Source Page Line Crop Contact Sheet

Status: local visual contact sheets for Cities source-page line-crop review.
These contact sheets help review crop order and row shape without transcribing Hebrew or importing source rows.
Tracked files contain no OCR body text or source-script body text.
worksheet only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_contact_sheet --packet reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv --base-dir reports/cities_pdf_recovery_probe/source_page_line_crops/contact_sheets --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_contact_sheet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_contact_sheet_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_CONTACT_SHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_contact_sheet.manifest.json
```

## Current Read

- Table pages: 4.
- Line crop rows: 203.
- Line crop images found: 203.
- Contact sheets: 4.
- Contact sheets available: 4.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: contact sheets only; local line-crop images are visual review aids, no OCR body text or source-script body text in tracked files, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Contact Sheets

| Rank | Transcription id | Page | Line crops | Image rows | Sheet | Dimensions |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 1 | `cities_source_transcription_001` | 3 | 44 | 44 | `reports/cities_pdf_recovery_probe/source_page_line_crops/contact_sheets/cities_source_transcription_001_line_crops.png` | 1008 x 6502 |
| 2 | `cities_source_transcription_002` | 4 | 55 | 55 | `reports/cities_pdf_recovery_probe/source_page_line_crops/contact_sheets/cities_source_transcription_002_line_crops.png` | 1008 x 8130 |
| 3 | `cities_source_transcription_003` | 5 | 54 | 54 | `reports/cities_pdf_recovery_probe/source_page_line_crops/contact_sheets/cities_source_transcription_003_line_crops.png` | 1008 x 7982 |
| 4 | `cities_source_transcription_004` | 6 | 50 | 50 | `reports/cities_pdf_recovery_probe/source_page_line_crops/contact_sheets/cities_source_transcription_004_line_crops.png` | 1008 x 7390 |

## Boundary

- Contact sheets are not transcription verification.
- Image review can sort crops by visual role, but it does not read or import Hebrew source rows.
- Any future import still needs explicit source-row evidence and an import decision.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
