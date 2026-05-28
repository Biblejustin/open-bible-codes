# Cities Source Page Line Crop Triage

Status: no-input visual triage for Cities source-page line crops.
It ranks crop images by layout and OCR-count signal only; it does not read Hebrew, transcribe rows, or import source rows.
Tracked files contain no OCR body text or source-script body text.
triage only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_triage --packet reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.manifest.json
```

## Current Read

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
- Boundary: triage only; no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Counts

| Transcription id | Triage rows |
| --- | ---: |
| `cities_source_transcription_001` | 44 |
| `cities_source_transcription_002` | 55 |
| `cities_source_transcription_003` | 54 |
| `cities_source_transcription_004` | 50 |

## Priority Buckets

| Priority | Rows | Meaning |
| --- | ---: | --- |
| `priority_1_dense_text` | 120 | strongest visual review candidates by count signal |
| `priority_2_medium_text` | 71 | likely text rows needing page context |
| `priority_3_short_text` | 12 | short labels, markers, or weak line boxes |
| `priority_4_no_text` | 0 | no OCR-count signal in the line box |

## Review Rule

- This triage is a queue order, not transcription.
- A dense crop can still be a header, note, or noise.
- A short crop can still matter if page context says it does.
- Any future import still needs readable row/column evidence and an explicit source-row import decision.
