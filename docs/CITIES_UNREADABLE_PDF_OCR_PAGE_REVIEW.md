# Cities Unreadable PDF OCR Page Review

Status: manual page-image review record. This records reviewer labels for the first priority Cities OCR pages.
It does not track OCR body text, repair text, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.
No OCR body text appears in this doc, CSV, summary, or manifest.

Reproduce:

```bash
python3 -m scripts.build_cities_unreadable_pdf_ocr_page_review --packet reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv --decisions data/study/mappings/cities_ocr_page_review_decisions.csv --out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.csv --summary-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review_summary.csv --markdown-out docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md --manifest-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.manifest.json
```

## Summary

- Review rows: 3.
- Reviewed pages: 3.
- OCR-empty pages reviewed: 2.
- Low-signal pages reviewed: 3.
- Visual-text-present pages: 2.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.
- Boundary: manual page-image review only; no OCR body text in tracked files, no repaired text, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Decisions

| Rank | Label | Page | OCR status | Signal chars | Visual role | OCR read status | Source-row use | Decision | Notes |
| ---: | --- | ---: | --- | ---: | --- | --- | --- | --- | --- |
| 1 | cities_pdf_dp365a_p1_4 | 3 | `page_ocr_empty` | 1 | `appendix_toc_or_index_page` | `ocr_empty_but_visual_text_present` | `no_source_row_use` | `no_source_row_import` | Short appendix or contents style page only; OCR empty does not block source table pages. |
| 2 | cities_pdf_dp365a_p1_4 | 4 | `page_ocr_empty` | 0 | `blank_or_separator_page` | `ocr_empty_matches_near_blank_page` | `no_source_row_use` | `no_source_row_import` | Near blank separator page with only page marker; no source-row use. |
| 3 | cities_pdf_dp365a_p5_11 | 1 | `page_ocr_text_detected` | 39 | `title_page` | `low_signal_ocr_matches_title_page` | `no_source_row_use` | `no_source_row_import` | Title page only; low OCR signal expected and not source-row-bearing. |

## Boundary

- These rows are page-image review records only.
- OCR sidecars remain ignored local files and are not tracked source text.
- Source-row decisions require separate citable decision records.
- No reviewed page here changes source admissibility or creates city-name rows.
- Contact sheets and page images remain visual aids, not public source-text artifacts.
