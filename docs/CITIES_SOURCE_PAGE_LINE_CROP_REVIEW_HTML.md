# Cities Source Page Line Crop Review HTML

Status: local ignored HTML review aid for Cities source-page line crops.
The HTML file displays line-crop images only and embeds no OCR text or source-script text.
Tracked files contain no OCR body text or source-script body text.
This does not verify a transcription, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_review_html --packet reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv --html-out reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_review.html --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_html_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_HTML.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_html.manifest.json
```

## Current Read

- HTML review aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_review.html`.
- HTML rows: 203.
- HTML embeds source text: `false`.
- HTML line-crop image rows: 203.
- HTML pages: 4.
- Line crop packet rows: 203.
- Line crop images found: 203.
- Unique table pages: 4.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: Local ignored HTML review aid; HTML displays line-crop images only, tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Counts

| Transcription id | Line crops |
| --- | ---: |
| `cities_source_transcription_001` | 44 |
| `cities_source_transcription_002` | 55 |
| `cities_source_transcription_003` | 54 |
| `cities_source_transcription_004` | 50 |

## Boundary

- The ignored HTML file displays line-crop images only; tracked files do not contain OCR body text or source-script body text.
- Line crop images are review aids, not verified transcriptions.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
