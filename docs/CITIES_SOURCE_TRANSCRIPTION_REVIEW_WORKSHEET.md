# Cities Source Transcription Review Worksheet

Status: no-input worksheet for future Cities source-row transcription review.
It organizes locked source pages for later readable transcription review but does not transcribe rows or import source rows.
No OCR body text or source-script body text appears in this doc, CSV, or manifest.
worksheet only; no OCR body text, no source-script body text, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_transcription_review_worksheet --evidence-packet reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.csv --records-template data/study/mappings/cities_source_transcription_decisions.csv --out reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.csv --markdown-out docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_transcription_review_worksheet.manifest.json
```

## Current Read

- Rows needing transcription review: 14.
- Locked source pages: 14.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Target records file: `data/study/mappings/cities_source_transcription_decisions.csv`.
- Transcription decision rows recorded: 0.
- Unrecorded transcription decision rows: 14.
- Review state: `pending_readable_transcription`.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Required evidence: readable Hebrew transcription plus row/column alignment evidence and explicit import decision record.

## Decision Record Fields

`transcription_decision_id,source_lock_decision_id,source_label,page_number,page_class,decision_status,selected_action,evidence_citation,evidence_summary,locked_by,locked_at,notes`

## Worksheet

| Rank | Transcription id | Source-lock id | Label | Page | Class | Role | State | Next manual action |
| ---: | --- | --- | --- | ---: | --- | --- | --- | --- |
| 1 | `cities_source_transcription_001` | `cities_source_row_lock_001` | cities_pdf_dp365a_p5_11 | 3 | `table_candidate_page` | `prose_with_source_table_page` | `pending_readable_transcription` | prepare row/column transcription plan before importing table rows |
| 2 | `cities_source_transcription_002` | `cities_source_row_lock_002` | cities_pdf_dp365a_p5_11 | 4 | `table_candidate_page` | `source_table_page` | `pending_readable_transcription` | prepare row/column transcription plan before importing table rows |
| 3 | `cities_source_transcription_003` | `cities_source_row_lock_003` | cities_pdf_dp365a_p5_11 | 5 | `table_candidate_page` | `source_table_page` | `pending_readable_transcription` | prepare row/column transcription plan before importing table rows |
| 4 | `cities_source_transcription_004` | `cities_source_row_lock_004` | cities_pdf_dp365a_p5_11 | 6 | `table_candidate_page` | `source_table_and_notes_page` | `pending_readable_transcription` | prepare row/column transcription plan before importing table rows |
| 5 | `cities_source_transcription_005` | `cities_source_row_lock_005` | cities_pdf_dp365a_appendix_7 | 1 | `source_list_candidate_page` | `source_list_page` | `pending_readable_transcription` | prepare source-list transcription plan before importing list rows |
| 6 | `cities_source_transcription_006` | `cities_source_row_lock_006` | cities_pdf_dp365a_appendix_7 | 2 | `source_list_candidate_page` | `source_list_page` | `pending_readable_transcription` | prepare source-list transcription plan before importing list rows |
| 7 | `cities_source_transcription_007` | `cities_source_row_lock_007` | cities_pdf_dp365a_appendix_7 | 3 | `source_list_candidate_page` | `source_list_page` | `pending_readable_transcription` | prepare source-list transcription plan before importing list rows |
| 8 | `cities_source_transcription_008` | `cities_source_row_lock_008` | cities_pdf_dp365a_appendix_7 | 4 | `source_list_candidate_page` | `source_list_page` | `pending_readable_transcription` | prepare source-list transcription plan before importing list rows |
| 9 | `cities_source_transcription_009` | `cities_source_row_lock_009` | cities_pdf_dp365a_appendix_7 | 5 | `source_list_candidate_page` | `source_list_page` | `pending_readable_transcription` | prepare source-list transcription plan before importing list rows |
| 10 | `cities_source_transcription_010` | `cities_source_row_lock_010` | cities_pdf_dp365a_p12_17 | 2 | `exception_note_candidate_page` | `source_exception_notes_page` | `pending_readable_transcription` | prepare exception-note interpretation plan before changing source rows |
| 11 | `cities_source_transcription_011` | `cities_source_row_lock_011` | cities_pdf_dp365a_p12_17 | 3 | `exception_note_candidate_page` | `source_exception_notes_page` | `pending_readable_transcription` | prepare exception-note interpretation plan before changing source rows |
| 12 | `cities_source_transcription_012` | `cities_source_row_lock_012` | cities_pdf_dp365a_p12_17 | 4 | `exception_note_candidate_page` | `source_exception_notes_page` | `pending_readable_transcription` | prepare exception-note interpretation plan before changing source rows |
| 13 | `cities_source_transcription_013` | `cities_source_row_lock_013` | cities_pdf_dp365a_p12_17 | 5 | `exception_note_candidate_page` | `source_exception_notes_page` | `pending_readable_transcription` | prepare exception-note interpretation plan before changing source rows |
| 14 | `cities_source_transcription_014` | `cities_source_row_lock_014` | cities_pdf_dp365a_p12_17 | 6 | `exception_note_candidate_page` | `criteria_and_source_exception_page` | `pending_readable_transcription` | prepare exception-note interpretation plan before changing source rows |

## Boundary

- This worksheet organizes review work only.
- Locked source pages are not source rows.
- A future decision record must cite readable transcription and row/column alignment evidence before any source row can be imported.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
