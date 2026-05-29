# Cities Source Page Line Crop Priority Review HTML

Status: local ignored HTML review aid for Cities source-page line-crop triage priorities.
The HTML file displays priority contact-sheet images only and embeds no OCR text or source-script text.
Tracked files contain no OCR body text or source-script body text.
Local ignored priority HTML review aid; HTML displays priority contact-sheet images only, tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_priority_review_html --priority-contact reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_contact_sheet.csv --html-out reports/cities_pdf_recovery_probe/source_page_line_crops/priority_review.html --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_html_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_HTML.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_html.manifest.json
```

## Current Read

- HTML priority review aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/priority_review.html`.
- HTML rows: 4.
- HTML embeds source text: `false`.
- HTML priority image rows: 4.
- Priority contact-sheet rows: 4.
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
- Boundary: Local ignored priority HTML review aid; HTML displays priority contact-sheet images only, tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Priority Counts

| Priority | Line crops | Sheet rows |
| --- | ---: | ---: |
| `priority_1_dense_text` | 120 | 1 |
| `priority_2_medium_text` | 71 | 1 |
| `priority_3_short_text` | 12 | 1 |
| `priority_4_no_text` | 0 | 1 |

## Boundary

- The ignored HTML file displays priority contact-sheet images only.
- The priority view is not transcription and does not decide row admissibility.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
