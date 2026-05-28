# Cities Source Page Line Crop Triage HTML

Status: local ignored HTML triage aid for Cities source-page line crops.
The HTML file displays line-crop images in priority order and embeds no OCR text or source-script text.
Tracked files contain no OCR body text or source-script body text.
triage only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_triage_html --triage reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.csv --html-out reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_triage.html --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage_html_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE_HTML.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage_html.manifest.json
```

## Current Read

- HTML triage aid: `reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_triage.html`.
- HTML rows: 203.
- HTML embeds source text: `false`.
- HTML line-crop image rows: 203.
- HTML priority sections: 4.
- Line-crop triage rows: 203.
- Unique table pages: 4.
- Crop images available: 203.
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
- Boundary: Local ignored HTML triage aid; HTML displays line-crop images in priority order only, tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Counts

| Transcription id | Triage rows |
| --- | ---: |
| `cities_source_transcription_001` | 44 |
| `cities_source_transcription_002` | 55 |
| `cities_source_transcription_003` | 54 |
| `cities_source_transcription_004` | 50 |

## Boundary

- The ignored HTML file displays crop images in priority order only.
- The priority order is not transcription and does not decide row admissibility.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
