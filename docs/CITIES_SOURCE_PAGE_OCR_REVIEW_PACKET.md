# Cities Source Page OCR Review Packet

Status: local Hebrew OCR review packet for locked Cities source pages.
OCR text sidecars are local ignored review aids only.
Tracked files contain no OCR body text or source-script body text.
This does not import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_ocr_review_packet --bundle reports/cities_pdf_recovery_probe/cities_source_page_review_bundle.csv --base-dir reports/cities_pdf_recovery_probe/source_page_ocr_review --tessdata-dir reports/wrr_1994/tessdata --language heb --psm 4 --out reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_OCR_REVIEW_PACKET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet.manifest.json
```

## Current Read

- Source-page OCR rows: 14.
- Page images found: 14.
- Page images missing: 0.
- OCR pages attempted: 14.
- Pages with OCR text: 14.
- Pages with low OCR text: 0.
- Pages with empty OCR text: 0.
- OCR errors: 0.
- Missing OCR dependency rows: 0.
- OCR text sidecars: 14.
- OCR text signal chars: 14872.
- OCR Hebrew letters: 14408.
- OCR words: 3939.
- OCR lines: 596.
- Language: `heb`.
- PSM: `4`.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: Source-page OCR review packet only; OCR text sidecars are ignored local review aids, no OCR body text or source-script body text in tracked files, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Packet Rows

| Rank | Transcription id | Label | Page | Class | Status | Hebrew letters | Words | Sidecar | Next manual action |
| ---: | --- | --- | ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | `cities_source_transcription_001` | cities_pdf_dp365a_p5_11 | 3 | `table_candidate_page` | `source_page_ocr_text_detected` | 1507 | 369 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_001.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 2 | `cities_source_transcription_002` | cities_pdf_dp365a_p5_11 | 4 | `table_candidate_page` | `source_page_ocr_text_detected` | 1197 | 386 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_002.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 3 | `cities_source_transcription_003` | cities_pdf_dp365a_p5_11 | 5 | `table_candidate_page` | `source_page_ocr_text_detected` | 1215 | 379 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_003.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 4 | `cities_source_transcription_004` | cities_pdf_dp365a_p5_11 | 6 | `table_candidate_page` | `source_page_ocr_text_detected` | 1015 | 355 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_004.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 5 | `cities_source_transcription_005` | cities_pdf_dp365a_appendix_7 | 1 | `source_list_candidate_page` | `source_page_ocr_text_detected` | 390 | 119 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_005.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 6 | `cities_source_transcription_006` | cities_pdf_dp365a_appendix_7 | 2 | `source_list_candidate_page` | `source_page_ocr_text_detected` | 372 | 116 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_006.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 7 | `cities_source_transcription_007` | cities_pdf_dp365a_appendix_7 | 3 | `source_list_candidate_page` | `source_page_ocr_text_detected` | 331 | 106 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_007.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 8 | `cities_source_transcription_008` | cities_pdf_dp365a_appendix_7 | 4 | `source_list_candidate_page` | `source_page_ocr_text_detected` | 345 | 110 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_008.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 9 | `cities_source_transcription_009` | cities_pdf_dp365a_appendix_7 | 5 | `source_list_candidate_page` | `source_page_ocr_text_detected` | 253 | 79 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_009.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 10 | `cities_source_transcription_010` | cities_pdf_dp365a_p12_17 | 2 | `exception_note_candidate_page` | `source_page_ocr_text_detected` | 1252 | 302 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_010.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 11 | `cities_source_transcription_011` | cities_pdf_dp365a_p12_17 | 3 | `exception_note_candidate_page` | `source_page_ocr_text_detected` | 1661 | 406 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_011.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 12 | `cities_source_transcription_012` | cities_pdf_dp365a_p12_17 | 4 | `exception_note_candidate_page` | `source_page_ocr_text_detected` | 1425 | 363 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_012.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 13 | `cities_source_transcription_013` | cities_pdf_dp365a_p12_17 | 5 | `exception_note_candidate_page` | `source_page_ocr_text_detected` | 1700 | 429 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_013.txt` | manual compare ignored OCR sidecar to page image; do not import rows |
| 14 | `cities_source_transcription_014` | cities_pdf_dp365a_p12_17 | 6 | `exception_note_candidate_page` | `source_page_ocr_text_detected` | 1745 | 420 | `reports/cities_pdf_recovery_probe/source_page_ocr_review/ocr_text/cities_source_transcription_014.txt` | manual compare ignored OCR sidecar to page image; do not import rows |

## Boundary

- OCR sidecar availability is not transcription verification.
- OCR counts are review logistics only; the tracked packet does not quote source text.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
