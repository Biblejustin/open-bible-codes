# Cities Source Page Review Bundle

Status: no-input page-image review bundle for locked Cities source pages.
It verifies page-image paths and dimensions for later manual transcription review.
No OCR body text or source-script body text appears in this doc, CSV, summary, or manifest.
It does not import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.

Reproduce:

```bash
python3 -m scripts.build_cities_source_page_review_bundle --worksheet reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.csv --out reports/cities_pdf_recovery_probe/cities_source_page_review_bundle.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_page_review_bundle_summary.csv --markdown-out docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_page_review_bundle.manifest.json
```

## Current Read

- Bundle rows: 14.
- Page images found: 14.
- Page images missing: 0.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: Page-image review bundle only; no OCR body text, no source-script body text, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Bundle

| Rank | Transcription id | Label | Page | Class | Image | Size | Next manual action |
| ---: | --- | --- | ---: | --- | --- | --- | --- |
| 1 | `cities_source_transcription_001` | cities_pdf_dp365a_p5_11 | 3 | `table_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p003.png` | 1700x2200 | prepare row/column transcription plan before importing table rows |
| 2 | `cities_source_transcription_002` | cities_pdf_dp365a_p5_11 | 4 | `table_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p004.png` | 1700x2200 | prepare row/column transcription plan before importing table rows |
| 3 | `cities_source_transcription_003` | cities_pdf_dp365a_p5_11 | 5 | `table_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p005.png` | 1700x2200 | prepare row/column transcription plan before importing table rows |
| 4 | `cities_source_transcription_004` | cities_pdf_dp365a_p5_11 | 6 | `table_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p006.png` | 1700x2200 | prepare row/column transcription plan before importing table rows |
| 5 | `cities_source_transcription_005` | cities_pdf_dp365a_appendix_7 | 1 | `source_list_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p001.png` | 1700x2200 | prepare source-list transcription plan before importing list rows |
| 6 | `cities_source_transcription_006` | cities_pdf_dp365a_appendix_7 | 2 | `source_list_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p002.png` | 1700x2200 | prepare source-list transcription plan before importing list rows |
| 7 | `cities_source_transcription_007` | cities_pdf_dp365a_appendix_7 | 3 | `source_list_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p003.png` | 1700x2200 | prepare source-list transcription plan before importing list rows |
| 8 | `cities_source_transcription_008` | cities_pdf_dp365a_appendix_7 | 4 | `source_list_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p004.png` | 1700x2200 | prepare source-list transcription plan before importing list rows |
| 9 | `cities_source_transcription_009` | cities_pdf_dp365a_appendix_7 | 5 | `source_list_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p005.png` | 1700x2200 | prepare source-list transcription plan before importing list rows |
| 10 | `cities_source_transcription_010` | cities_pdf_dp365a_p12_17 | 2 | `exception_note_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p002.png` | 1700x2200 | prepare exception-note interpretation plan before changing source rows |
| 11 | `cities_source_transcription_011` | cities_pdf_dp365a_p12_17 | 3 | `exception_note_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p003.png` | 1700x2200 | prepare exception-note interpretation plan before changing source rows |
| 12 | `cities_source_transcription_012` | cities_pdf_dp365a_p12_17 | 4 | `exception_note_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p004.png` | 1700x2200 | prepare exception-note interpretation plan before changing source rows |
| 13 | `cities_source_transcription_013` | cities_pdf_dp365a_p12_17 | 5 | `exception_note_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p005.png` | 1700x2200 | prepare exception-note interpretation plan before changing source rows |
| 14 | `cities_source_transcription_014` | cities_pdf_dp365a_p12_17 | 6 | `exception_note_candidate_page` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p006.png` | 1700x2200 | prepare exception-note interpretation plan before changing source rows |

## Boundary

- Page-image existence is not transcription verification.
- Page dimensions are review logistics only.
- Future source-row use still requires readable transcription, row/column alignment evidence, and an explicit import decision record.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
