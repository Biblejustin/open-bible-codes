# Cities Source Row Lock Worksheet

Status: worksheet plus current Cities source-row lock decision-record status.
It reads the source-row lock queue and optional decision records but does not update either file.
No OCR body text or source-script body text appears in this doc, CSV, or manifest.
worksheet only; no OCR body text, no source-row transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

Reproduce:

```bash
python3 -m scripts.build_cities_source_row_lock_worksheet --queue reports/cities_pdf_recovery_probe/cities_source_row_lock_queue.csv --records-template data/study/mappings/cities_source_row_lock_decisions.csv --out reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.csv --markdown-out docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.manifest.json
```

## Current Read

- Worksheet rows: 14.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Target records file: `data/study/mappings/cities_source_row_lock_decisions.csv`.
- Recorded decision rows: 2.
- Locked decision rows: 2.
- Unrecorded decision rows: 12.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.
- Recorded selected actions: source_row_lock_ready=2.

## Lock Row Fields

`decision_id,queue_lock_rank,label,page_number,page_class,decision_status,selected_action,evidence_citation,evidence_summary,locked_by,locked_at,notes`

The worksheet gives exact `decision_id`, queue fields, evidence prompts, and current record fields when a lock row exists.
A future lock row may mark a page ready for source-row work, but this worksheet itself never imports or transcribes source rows.
`docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md` joins these decision ids to recovered PDF metadata and page-image paths without source text.

## Decision Meanings

- `source_row_lock_ready` means page evidence can support later source-row extraction; this worksheet still imports nothing.
- `no_source_row_import` means do not use this page for source-row extraction.
- `exclude_page_from_source_rows` means explicitly keep this page out of any later source-row set.
- `deferred_no_lock` means no lock decision yet; leave row blocked.

## Worksheet

| Decision id | Rank | Label | Page | Class | Role | Record status | Recorded action | Evidence prompt | Suggested actions |
| --- | ---: | --- | ---: | --- | --- | --- | --- | --- | --- |
| `cities_source_row_lock_001` | 1 | cities_pdf_dp365a_p5_11 | 3 | `table_candidate_page` | `prose_with_source_table_page` | `locked` | `source_row_lock_ready` | cite PDF/archive checksum, page image, table scope, and row/column boundary method; do not transcribe row text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_002` | 2 | cities_pdf_dp365a_p5_11 | 4 | `table_candidate_page` | `source_table_page` | `locked` | `source_row_lock_ready` | cite PDF/archive checksum, page image, table scope, and row/column boundary method; do not transcribe row text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_003` | 3 | cities_pdf_dp365a_p5_11 | 5 | `table_candidate_page` | `source_table_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, table scope, and row/column boundary method; do not transcribe row text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_004` | 4 | cities_pdf_dp365a_p5_11 | 6 | `table_candidate_page` | `source_table_and_notes_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, table scope, and row/column boundary method; do not transcribe row text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_005` | 5 | cities_pdf_dp365a_appendix_7 | 1 | `source_list_candidate_page` | `source_list_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and list scope; do not transcribe list rows here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_006` | 6 | cities_pdf_dp365a_appendix_7 | 2 | `source_list_candidate_page` | `source_list_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and list scope; do not transcribe list rows here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_007` | 7 | cities_pdf_dp365a_appendix_7 | 3 | `source_list_candidate_page` | `source_list_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and list scope; do not transcribe list rows here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_008` | 8 | cities_pdf_dp365a_appendix_7 | 4 | `source_list_candidate_page` | `source_list_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and list scope; do not transcribe list rows here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_009` | 9 | cities_pdf_dp365a_appendix_7 | 5 | `source_list_candidate_page` | `source_list_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and list scope; do not transcribe list rows here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_010` | 10 | cities_pdf_dp365a_p12_17 | 2 | `exception_note_candidate_page` | `source_exception_notes_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and note scope; decide future source-row effect without body text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_011` | 11 | cities_pdf_dp365a_p12_17 | 3 | `exception_note_candidate_page` | `source_exception_notes_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and note scope; decide future source-row effect without body text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_012` | 12 | cities_pdf_dp365a_p12_17 | 4 | `exception_note_candidate_page` | `source_exception_notes_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and note scope; decide future source-row effect without body text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_013` | 13 | cities_pdf_dp365a_p12_17 | 5 | `exception_note_candidate_page` | `source_exception_notes_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and note scope; decide future source-row effect without body text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
| `cities_source_row_lock_014` | 14 | cities_pdf_dp365a_p12_17 | 6 | `exception_note_candidate_page` | `criteria_and_source_exception_page` | `unrecorded` | `` | cite PDF/archive checksum, page image, and note scope; decide future source-row effect without body text here | `no_source_row_import;source_row_lock_ready;exclude_page_from_source_rows;deferred_no_lock` |
