# Cities Source Page Line Crop Band Review HTML

Status: local ignored HTML review aid for Cities source-page line-crop coordinate bands.
The HTML file displays band contact-sheet images only and embeds no OCR text or source-script text.
Tracked files contain no OCR body text or source-script body text.
Local ignored band HTML review aid; HTML displays band contact-sheet images only, tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_band_review_html --band-contact reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_contact_sheet.csv --html-out reports/cities_pdf_recovery_probe/source_page_line_crops/band_review.html --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_html_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_HTML.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_html.manifest.json
```

## Current Read

- HTML band review aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/band_review.html`.
- HTML rows: 16.
- HTML embeds source text: `false`.
- HTML band image rows: 16.
- Band contact-sheet rows: 16.
- Band contact sheets available: 16.
- Line crop rows: 203.
- Line crop images found: 203.
- Unique table pages: 4.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: Local ignored band HTML review aid; HTML displays band contact-sheet images only, tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Counts

| Transcription id | Band rows |
| --- | ---: |
| `cities_source_transcription_001` | 7 |
| `cities_source_transcription_002` | 2 |
| `cities_source_transcription_003` | 2 |
| `cities_source_transcription_004` | 5 |

## Boundary

- The ignored HTML file displays band contact-sheet images only.
- The band view is not transcription and does not decide row admissibility.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
