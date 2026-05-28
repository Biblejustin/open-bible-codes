# Cities Source Page Line Crop Packet

Status: local line-crop review packet for Cities table candidate pages.
Tracked files contain no OCR body text or source-script body text.
This does not verify a transcription, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_line_crop_packet --packet reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet.csv --base-dir reports/cities_pdf_recovery_probe/source_page_line_crops --tessdata-dir reports/wrr_1994/tessdata --language heb --psm 4 --out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_LINE_CROP_PACKET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_line_crop_packet.manifest.json
```

## Current Read

- Table candidate pages: 4.
- Line crop rows: 203.
- Line crops available: 203.
- TSV sidecars: 4.
- OCR words represented by line boxes: 1511.
- OCR Hebrew letters represented by line boxes: 4934.
- Language: `heb`.
- PSM: `4`.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: Line crops are local review aids only; tracked files contain no OCR body text or source-script body text, no verified transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Counts

| Transcription id | Line crops |
| --- | ---: |
| `cities_source_transcription_001` | 44 |
| `cities_source_transcription_002` | 55 |
| `cities_source_transcription_003` | 54 |
| `cities_source_transcription_004` | 50 |

## Boundary

- Line crops are local review aids, not verified row transcriptions.
- TSV sidecars may contain OCR text locally; tracked files do not.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
