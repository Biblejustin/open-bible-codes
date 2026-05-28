# Cities Source Row Lock Evidence Packet

Status: diagnostic evidence packet for Cities source-row lock candidates.
It joins decision ids to PDF/source metadata and page-image paths without OCR body text.
It does not transcribe rows, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.
No OCR body text or source-script body text appears in this doc, CSV, summary, or manifest.
The local checker verifies every packet row points to an existing recovered PDF and page-image artifact.

Reproduce:

```bash
python3 -m scripts.build_cities_source_row_lock_evidence_packet --worksheet reports/cities_pdf_recovery_probe/cities_source_row_lock_worksheet.csv --source-queue reports/cities_pdf_recovery_probe/cities_source_review_queue.csv --out reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.csv --summary-out reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_summary.csv --markdown-out docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md --manifest-out reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.manifest.json
```

## Current Read

- Evidence rows: 14.
- Unique labels: 3.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Recorded decision rows: 0.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.
- Boundary: diagnostic evidence packet only; no OCR body text, no source-row transcription, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Evidence Rows

| Rank | Decision id | Label | Page | Class | Source | SHA256 | Page image | Record status | Evidence required |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | `cities_source_row_lock_001` | cities_pdf_dp365a_p5_11 | 3 | `table_candidate_page` | archive | `e89e869d452f` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p003.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_001; do not transcribe body text |
| 2 | `cities_source_row_lock_002` | cities_pdf_dp365a_p5_11 | 4 | `table_candidate_page` | archive | `e89e869d452f` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p004.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_002; do not transcribe body text |
| 3 | `cities_source_row_lock_003` | cities_pdf_dp365a_p5_11 | 5 | `table_candidate_page` | archive | `e89e869d452f` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p005.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_003; do not transcribe body text |
| 4 | `cities_source_row_lock_004` | cities_pdf_dp365a_p5_11 | 6 | `table_candidate_page` | archive | `e89e869d452f` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p5_11_p006.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_004; do not transcribe body text |
| 5 | `cities_source_row_lock_005` | cities_pdf_dp365a_appendix_7 | 1 | `source_list_candidate_page` | archive | `7b7e2015bb62` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p001.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_005; do not transcribe body text |
| 6 | `cities_source_row_lock_006` | cities_pdf_dp365a_appendix_7 | 2 | `source_list_candidate_page` | archive | `7b7e2015bb62` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p002.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_006; do not transcribe body text |
| 7 | `cities_source_row_lock_007` | cities_pdf_dp365a_appendix_7 | 3 | `source_list_candidate_page` | archive | `7b7e2015bb62` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p003.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_007; do not transcribe body text |
| 8 | `cities_source_row_lock_008` | cities_pdf_dp365a_appendix_7 | 4 | `source_list_candidate_page` | archive | `7b7e2015bb62` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p004.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_008; do not transcribe body text |
| 9 | `cities_source_row_lock_009` | cities_pdf_dp365a_appendix_7 | 5 | `source_list_candidate_page` | archive | `7b7e2015bb62` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_7_p005.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_009; do not transcribe body text |
| 10 | `cities_source_row_lock_010` | cities_pdf_dp365a_p12_17 | 2 | `exception_note_candidate_page` | archive | `127d829147cb` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p002.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_010; do not transcribe body text |
| 11 | `cities_source_row_lock_011` | cities_pdf_dp365a_p12_17 | 3 | `exception_note_candidate_page` | archive | `127d829147cb` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p003.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_011; do not transcribe body text |
| 12 | `cities_source_row_lock_012` | cities_pdf_dp365a_p12_17 | 4 | `exception_note_candidate_page` | archive | `127d829147cb` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p004.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_012; do not transcribe body text |
| 13 | `cities_source_row_lock_013` | cities_pdf_dp365a_p12_17 | 5 | `exception_note_candidate_page` | archive | `127d829147cb` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p005.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_013; do not transcribe body text |
| 14 | `cities_source_row_lock_014` | cities_pdf_dp365a_p12_17 | 6 | `exception_note_candidate_page` | archive | `127d829147cb` | `reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_p12_17_p006.png` | `unrecorded` | verify archived PDF checksum, rendered page image, visual page role, and admissibility for cities_source_row_lock_014; do not transcribe body text |

## Boundary

- This packet collects evidence locations only.
- Page images and recovered PDFs remain supporting artifacts; this doc does not copy their body text.
- A future decision record must cite page evidence before any source rows can be imported.
- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.
