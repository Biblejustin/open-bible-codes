# Cities Source Page Line Crop Band Map

Status: coordinate-only band map for Cities source-page line crops.
It groups adjacent line crops when vertical gaps are below the configured threshold.
No OCR body text or source-script body text appears in this doc, CSV, or manifest.
band map only; coordinate grouping of line crops, no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_band_map --packet reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv --triage reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.csv --gap-threshold 40 --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_MAP.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_map.manifest.json
```

## Current Read

- Gap threshold: 40 px.
- Band rows: 16.
- Source line rows: 203.
- Unique table pages: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: band map only; coordinate grouping of line crops, no OCR body text, no source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Bands

| Transcription id | Bands |
| --- | ---: |
| `cities_source_transcription_001` | 7 |
| `cities_source_transcription_002` | 2 |
| `cities_source_transcription_003` | 2 |
| `cities_source_transcription_004` | 5 |

## Band Rows

| Band | Page | Lines | Crop rows | Top-bottom | Dominant priority |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `cities_source_transcription_001` | 1-1 | 1 | 191-213 | `priority_2_medium_text` |
| 2 | `cities_source_transcription_001` | 2-2 | 1 | 331-372 | `priority_1_dense_text` |
| 3 | `cities_source_transcription_001` | 3-15 | 13 | 425-844 | `priority_1_dense_text` |
| 4 | `cities_source_transcription_001` | 16-19 | 4 | 890-1011 | `priority_1_dense_text` |
| 5 | `cities_source_transcription_001` | 20-20 | 1 | 1056-1079 | `priority_2_medium_text` |
| 6 | `cities_source_transcription_001` | 21-26 | 6 | 1123-1311 | `priority_1_dense_text` |
| 7 | `cities_source_transcription_001` | 27-44 | 18 | 1386-1989 | `priority_1_dense_text` |
| 8 | `cities_source_transcription_002` | 1-27 | 27 | 192-1050 | `priority_1_dense_text` |
| 9 | `cities_source_transcription_002` | 28-55 | 28 | 1090-1980 | `priority_1_dense_text` |
| 10 | `cities_source_transcription_003` | 1-2 | 2 | 192-247 | `priority_1_dense_text` |
| 11 | `cities_source_transcription_003` | 3-54 | 52 | 298-1983 | `priority_1_dense_text` |
| 12 | `cities_source_transcription_004` | 1-2 | 2 | 188-250 | `priority_1_dense_text` |
| 13 | `cities_source_transcription_004` | 3-7 | 5 | 298-449 | `priority_1_dense_text` |
| 14 | `cities_source_transcription_004` | 8-9 | 2 | 492-551 | `priority_1_dense_text` |
| 15 | `cities_source_transcription_004` | 10-12 | 3 | 592-683 | `priority_1_dense_text` |
| 16 | `cities_source_transcription_004` | 13-50 | 38 | 724-1978 | `priority_2_medium_text` |

## Boundary

- Band grouping uses local crop coordinates only.
- A band is not a verified source row, table row, transcription, or city-name record.
- Any future source import still needs readable row evidence and an explicit import decision.
