# Cities Source Row Lock Queue

Status: source-row lock planning record from reviewed OCR page roles.
It does not import source rows, track OCR body text, normalize city names, run ELS searches, compute compactness, or verify p-levels.
No OCR body text or source-script body text appears in this doc, CSV, summary, or manifest.

Reproduce:

```bash
python3 -m scripts.build_cities_source_row_lock_queue --page-review reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.csv --out reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_row_lock_queue_summary.csv --markdown-out docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.manifest.json
```

## Summary

- Queue rows: 14.
- Unique labels: 3.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.
- Boundary: source-row lock planning only; no OCR body text, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Candidate Pages

| Rank | Label | Page | Role | Class | OCR status | Signal chars | Lock status | Next action |
| ---: | --- | ---: | --- | --- | --- | ---: | --- | --- |
| 1 | cities_pdf_dp365a_p5_11 | 3 | `prose_with_source_table_page` | `table_candidate_page` | `page_ocr_text_detected` | 1111 | `needs_citable_source_row_lock` | page has visual table material; needs citable source-row lock before use |
| 2 | cities_pdf_dp365a_p5_11 | 4 | `source_table_page` | `table_candidate_page` | `page_ocr_text_detected` | 883 | `needs_citable_source_row_lock` | page has visual table material; needs citable source-row lock before use |
| 3 | cities_pdf_dp365a_p5_11 | 5 | `source_table_page` | `table_candidate_page` | `page_ocr_text_detected` | 901 | `needs_citable_source_row_lock` | page has visual table material; needs citable source-row lock before use |
| 4 | cities_pdf_dp365a_p5_11 | 6 | `source_table_and_notes_page` | `table_candidate_page` | `page_ocr_text_detected` | 372 | `needs_citable_source_row_lock` | page has visual table and note material; needs citable source-row lock before use |
| 5 | cities_pdf_dp365a_appendix_7 | 1 | `source_list_page` | `source_list_candidate_page` | `page_ocr_text_detected` | 288 | `needs_citable_source_row_lock` | page has visual list material; needs citable source-row lock before use |
| 6 | cities_pdf_dp365a_appendix_7 | 2 | `source_list_page` | `source_list_candidate_page` | `page_ocr_text_detected` | 326 | `needs_citable_source_row_lock` | page has visual list material; needs citable source-row lock before use |
| 7 | cities_pdf_dp365a_appendix_7 | 3 | `source_list_page` | `source_list_candidate_page` | `page_ocr_text_detected` | 284 | `needs_citable_source_row_lock` | page has visual list material; needs citable source-row lock before use |
| 8 | cities_pdf_dp365a_appendix_7 | 4 | `source_list_page` | `source_list_candidate_page` | `page_ocr_text_detected` | 287 | `needs_citable_source_row_lock` | page has visual list material; needs citable source-row lock before use |
| 9 | cities_pdf_dp365a_appendix_7 | 5 | `source_list_page` | `source_list_candidate_page` | `page_ocr_text_detected` | 197 | `needs_citable_source_row_lock` | page has visual list material; needs citable source-row lock before use |
| 10 | cities_pdf_dp365a_p12_17 | 2 | `source_exception_notes_page` | `exception_note_candidate_page` | `page_ocr_text_detected` | 982 | `needs_citable_source_row_lock` | page has source-exception notes; needs separate citable decision before use |
| 11 | cities_pdf_dp365a_p12_17 | 3 | `source_exception_notes_page` | `exception_note_candidate_page` | `page_ocr_text_detected` | 1292 | `needs_citable_source_row_lock` | page has source-exception notes; needs separate citable decision before use |
| 12 | cities_pdf_dp365a_p12_17 | 4 | `source_exception_notes_page` | `exception_note_candidate_page` | `page_ocr_text_detected` | 1128 | `needs_citable_source_row_lock` | page has source-exception notes; needs separate citable decision before use |
| 13 | cities_pdf_dp365a_p12_17 | 5 | `source_exception_notes_page` | `exception_note_candidate_page` | `page_ocr_text_detected` | 1316 | `needs_citable_source_row_lock` | page has source-exception notes; needs separate citable decision before use |
| 14 | cities_pdf_dp365a_p12_17 | 6 | `criteria_and_source_exception_page` | `exception_note_candidate_page` | `page_ocr_text_detected` | 1357 | `needs_citable_source_row_lock` | page has criteria and source-exception notes; needs separate citable decision before use |

## Boundary

- This queue names page locations only.
- It does not transcribe city rows, names, dates, spellings, or OCR body text.
- Candidate pages still need a separate citable source-row lock before any source data can be used.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
