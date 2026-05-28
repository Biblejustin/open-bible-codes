# Cities Source Page OCR Review HTML

Status: local ignored HTML review aid for locked Cities source-page OCR.
The HTML file embeds OCR sidecar text so image/text comparison can happen locally.
Tracked files contain no OCR body text or source-script body text.
This does not import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_ocr_review_html --packet reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_packet.csv --html-out reports/cities_pdf_recovery_probe/source_page_ocr_review/source_page_ocr_review.html --summary-out reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_html_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_OCR_REVIEW_HTML.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_html.manifest.json
```

## Current Read

- HTML review aid: `reports/cities_pdf_recovery_probe/source_page_ocr_review/source_page_ocr_review.html`.
- HTML rows: 14.
- HTML embeds OCR text: `true`.
- HTML embedded OCR text rows: 14.
- Page images found: 14.
- OCR text sidecars: 14.
- Pages with OCR text: 14.
- OCR Hebrew letters: 14408.
- OCR words: 3939.
- OCR lines: 596.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: Local ignored HTML review aid; HTML embeds OCR sidecar text for manual comparison, tracked files contain no OCR body text or source-script body text, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Order

| Rank | Transcription id | Label | Page | Class | Status |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `cities_source_transcription_001` | cities_pdf_dp365a_p5_11 | 3 | `table_candidate_page` | `source_page_ocr_text_detected` |
| 2 | `cities_source_transcription_002` | cities_pdf_dp365a_p5_11 | 4 | `table_candidate_page` | `source_page_ocr_text_detected` |
| 3 | `cities_source_transcription_003` | cities_pdf_dp365a_p5_11 | 5 | `table_candidate_page` | `source_page_ocr_text_detected` |
| 4 | `cities_source_transcription_004` | cities_pdf_dp365a_p5_11 | 6 | `table_candidate_page` | `source_page_ocr_text_detected` |
| 5 | `cities_source_transcription_005` | cities_pdf_dp365a_appendix_7 | 1 | `source_list_candidate_page` | `source_page_ocr_text_detected` |
| 6 | `cities_source_transcription_006` | cities_pdf_dp365a_appendix_7 | 2 | `source_list_candidate_page` | `source_page_ocr_text_detected` |
| 7 | `cities_source_transcription_007` | cities_pdf_dp365a_appendix_7 | 3 | `source_list_candidate_page` | `source_page_ocr_text_detected` |
| 8 | `cities_source_transcription_008` | cities_pdf_dp365a_appendix_7 | 4 | `source_list_candidate_page` | `source_page_ocr_text_detected` |
| 9 | `cities_source_transcription_009` | cities_pdf_dp365a_appendix_7 | 5 | `source_list_candidate_page` | `source_page_ocr_text_detected` |
| 10 | `cities_source_transcription_010` | cities_pdf_dp365a_p12_17 | 2 | `exception_note_candidate_page` | `source_page_ocr_text_detected` |
| 11 | `cities_source_transcription_011` | cities_pdf_dp365a_p12_17 | 3 | `exception_note_candidate_page` | `source_page_ocr_text_detected` |
| 12 | `cities_source_transcription_012` | cities_pdf_dp365a_p12_17 | 4 | `exception_note_candidate_page` | `source_page_ocr_text_detected` |
| 13 | `cities_source_transcription_013` | cities_pdf_dp365a_p12_17 | 5 | `exception_note_candidate_page` | `source_page_ocr_text_detected` |
| 14 | `cities_source_transcription_014` | cities_pdf_dp365a_p12_17 | 6 | `exception_note_candidate_page` | `source_page_ocr_text_detected` |

## Boundary

- The ignored HTML file may display OCR text; tracked files do not.
- OCR text is a review aid, not verified transcription.
- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
