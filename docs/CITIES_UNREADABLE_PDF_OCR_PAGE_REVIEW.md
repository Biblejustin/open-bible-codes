# Cities Unreadable PDF OCR Page Review

Status: manual page-image review record. This records reviewer labels for reviewed Cities OCR packet pages.
It does not track OCR body text, repair text, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.
No OCR body text appears in this doc, CSV, summary, or manifest.

Reproduce:

```bash
python3 -m scripts.build_cities_unreadable_pdf_ocr_page_review --packet reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv --decisions data/study/mappings/cities_ocr_page_review_decisions.csv --out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.csv --summary-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review_summary.csv --markdown-out docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md --manifest-out reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review.manifest.json
```

## Summary

- Packet pages: 61.
- Reviewed packet pages: 41.
- Unreviewed packet pages: 20.
- Review rows: 41.
- Reviewed pages: 41.
- OCR-empty pages reviewed: 2.
- Low-signal pages reviewed: 3.
- Visual-text-present pages: 40.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.
- Boundary: manual page-image review only; no OCR body text in tracked files, no repaired text, no source-row import, no city normalization, no ELS, no compactness, no p-level

## Page Decisions

| Rank | Label | Page | OCR status | Signal chars | Visual role | OCR read status | Source-row use | Decision | Notes |
| ---: | --- | ---: | --- | ---: | --- | --- | --- | --- | --- |
| 1 | cities_pdf_dp365a_appendix_6 | 1 | `page_ocr_text_detected` | 942 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 2 | cities_pdf_dp365a_appendix_6 | 2 | `page_ocr_text_detected` | 341 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 3 | cities_pdf_dp365a_appendix_7 | 1 | `page_ocr_text_detected` | 288 | `source_list_page` | `ocr_signal_present_for_list_page` | `no_source_row_use` | `no_source_row_import` | Visual list page present; row import blocked pending separate citable source-row lock. |
| 4 | cities_pdf_dp365a_appendix_7 | 2 | `page_ocr_text_detected` | 326 | `source_list_page` | `ocr_signal_present_for_list_page` | `no_source_row_use` | `no_source_row_import` | Visual list page present; row import blocked pending separate citable source-row lock. |
| 5 | cities_pdf_dp365a_appendix_7 | 3 | `page_ocr_text_detected` | 284 | `source_list_page` | `ocr_signal_present_for_list_page` | `no_source_row_use` | `no_source_row_import` | Visual list page present; row import blocked pending separate citable source-row lock. |
| 6 | cities_pdf_dp365a_appendix_7 | 4 | `page_ocr_text_detected` | 287 | `source_list_page` | `ocr_signal_present_for_list_page` | `no_source_row_use` | `no_source_row_import` | Visual list page present; row import blocked pending separate citable source-row lock. |
| 7 | cities_pdf_dp365a_appendix_7 | 5 | `page_ocr_text_detected` | 197 | `source_list_page` | `ocr_signal_present_for_list_page` | `no_source_row_use` | `no_source_row_import` | Visual list page present; row import blocked pending separate citable source-row lock. |
| 8 | cities_pdf_dp365a_p12_17 | 1 | `page_ocr_text_detected` | 1501 | `method_intro_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Method-introduction prose page; no tabular source-row import. |
| 9 | cities_pdf_dp365a_p12_17 | 2 | `page_ocr_text_detected` | 982 | `source_exception_notes_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Source-discrepancy examples page; requires separate citable row lock before any data use. |
| 10 | cities_pdf_dp365a_p12_17 | 3 | `page_ocr_text_detected` | 1292 | `source_exception_notes_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Source-discrepancy examples page; requires separate citable row lock before any data use. |
| 11 | cities_pdf_dp365a_p12_17 | 4 | `page_ocr_text_detected` | 1128 | `source_exception_notes_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Source-discrepancy examples page; requires separate citable row lock before any data use. |
| 12 | cities_pdf_dp365a_p12_17 | 5 | `page_ocr_text_detected` | 1316 | `source_exception_notes_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Source-discrepancy examples page; requires separate citable row lock before any data use. |
| 13 | cities_pdf_dp365a_p12_17 | 6 | `page_ocr_text_detected` | 1357 | `criteria_and_source_exception_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Criteria and source-discrepancy prose page; requires separate citable row lock before any data use. |
| 14 | cities_pdf_dp365a_p1_4 | 1 | `page_ocr_text_detected` | 921 | `method_toc_and_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Method table-of-contents and prose page; no source-row import. |
| 15 | cities_pdf_dp365a_p1_4 | 2 | `page_ocr_text_detected` | 1201 | `method_toc_and_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Method table-of-contents and prose page; no source-row import. |
| 16 | cities_pdf_dp365a_p1_4 | 3 | `page_ocr_empty` | 1 | `appendix_toc_or_index_page` | `ocr_empty_but_visual_text_present` | `no_source_row_use` | `no_source_row_import` | Short appendix or contents style page only; OCR empty does not block source table pages. |
| 17 | cities_pdf_dp365a_p1_4 | 4 | `page_ocr_empty` | 0 | `blank_or_separator_page` | `ocr_empty_matches_near_blank_page` | `no_source_row_use` | `no_source_row_import` | Near blank separator page with only page marker; no source-row use. |
| 18 | cities_pdf_dp365a_p5_11 | 1 | `page_ocr_text_detected` | 39 | `title_page` | `low_signal_ocr_matches_title_page` | `no_source_row_use` | `no_source_row_import` | Title page only; low OCR signal expected and not source-row-bearing. |
| 19 | cities_pdf_dp365a_p5_11 | 2 | `page_ocr_text_detected` | 899 | `method_prose_with_index_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Method prose with small index or outline; no source-row import. |
| 20 | cities_pdf_dp365a_p5_11 | 3 | `page_ocr_text_detected` | 1111 | `prose_with_source_table_page` | `ocr_signal_present_for_table_page` | `no_source_row_use` | `no_source_row_import` | Visual table present; row import blocked pending separate citable source-row lock. |
| 21 | cities_pdf_dp365a_p5_11 | 4 | `page_ocr_text_detected` | 883 | `source_table_page` | `ocr_signal_present_for_table_page` | `no_source_row_use` | `no_source_row_import` | Visual table present; row import blocked pending separate citable source-row lock. |
| 22 | cities_pdf_dp365a_p5_11 | 5 | `page_ocr_text_detected` | 901 | `source_table_page` | `ocr_signal_present_for_table_page` | `no_source_row_use` | `no_source_row_import` | Visual table present; row import blocked pending separate citable source-row lock. |
| 23 | cities_pdf_dp365a_p5_11 | 6 | `page_ocr_text_detected` | 372 | `source_table_and_notes_page` | `ocr_signal_present_for_table_page` | `no_source_row_use` | `no_source_row_import` | Visual table and notes present; row import blocked pending separate citable source-row lock. |
| 24 | cities_pdf_dp365a_p5_11 | 7 | `page_ocr_text_detected` | 535 | `method_notes_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Method notes page; no source-row import. |
| 25 | cities_pdf_dp365a_part_2_p105_111 | 1 | `page_ocr_text_detected` | 608 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 26 | cities_pdf_dp365a_part_2_p105_111 | 2 | `page_ocr_text_detected` | 1026 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 27 | cities_pdf_dp365a_part_2_p105_111 | 3 | `page_ocr_text_detected` | 1090 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 28 | cities_pdf_dp365a_part_2_p105_111 | 4 | `page_ocr_text_detected` | 832 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 29 | cities_pdf_dp365a_part_2_p105_111 | 5 | `page_ocr_text_detected` | 1192 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 30 | cities_pdf_dp365a_part_2_p105_111 | 6 | `page_ocr_text_detected` | 987 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 31 | cities_pdf_dp365a_part_2_p105_111 | 7 | `page_ocr_text_detected` | 293 | `appendix_prose_page` | `ocr_signal_present_for_prose_page` | `no_source_row_use` | `no_source_row_import` | Appendix prose page; no source-row import. |
| 32 | cities_pdf_wrr | 1 | `page_ocr_text_detected` | 3279 | `context_paper_title_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper title page; not Cities source-row material. |
| 33 | cities_pdf_wrr | 2 | `page_ocr_text_detected` | 3124 | `context_paper_figure_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper figure page; not Cities source-row material. |
| 34 | cities_pdf_wrr | 3 | `page_ocr_text_detected` | 4235 | `context_paper_prose_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper prose page; not Cities source-row material. |
| 35 | cities_pdf_wrr | 4 | `page_ocr_text_detected` | 2505 | `context_paper_table_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper table page; not Cities source-row material. |
| 36 | cities_pdf_wrr | 5 | `page_ocr_text_detected` | 2886 | `context_paper_table_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper table page; not Cities source-row material. |
| 37 | cities_pdf_wrr | 6 | `page_ocr_text_detected` | 3488 | `context_paper_prose_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper prose page; not Cities source-row material. |
| 38 | cities_pdf_wrr | 7 | `page_ocr_text_detected` | 3668 | `context_paper_formula_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper formula page; not Cities source-row material. |
| 39 | cities_pdf_wrr | 8 | `page_ocr_text_detected` | 3627 | `context_paper_formula_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper formula page; not Cities source-row material. |
| 40 | cities_pdf_wrr | 9 | `page_ocr_text_detected` | 2818 | `context_paper_chart_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper chart page; not Cities source-row material. |
| 41 | cities_pdf_wrr | 10 | `page_ocr_text_detected` | 1562 | `context_paper_reference_page` | `ocr_signal_present_for_context_page` | `no_source_row_use` | `no_source_row_import` | WRR context paper reference page; not Cities source-row material. |

## Unreviewed Packet Pages

These packet pages do not have page-image review decisions yet and do not feed the source-row lock queue.

| Label | Page | OCR status | Signal chars | Image path |
| --- | ---: | --- | ---: | --- |
| cities_pdf_dp364_short | 1 | `page_ocr_text_detected` | 440 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp364_short_p001.png |
| cities_pdf_dp364_short | 2 | `page_ocr_text_detected` | 518 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp364_short_p002.png |
| cities_pdf_dp364_short | 3 | `page_ocr_text_detected` | 2023 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp364_short_p003.png |
| cities_pdf_dp364_short | 4 | `page_ocr_text_detected` | 1689 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp364_short_p004.png |
| cities_pdf_dp364_short | 5 | `page_ocr_text_detected` | 1910 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp364_short_p005.png |
| cities_pdf_dp364_short | 6 | `page_ocr_text_detected` | 461 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp364_short_p006.png |
| cities_pdf_dp365a_appendix_2 | 1 | `page_ocr_text_detected` | 791 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p001.png |
| cities_pdf_dp365a_appendix_2 | 2 | `page_ocr_text_detected` | 668 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p002.png |
| cities_pdf_dp365a_appendix_2 | 3 | `page_ocr_text_detected` | 657 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p003.png |
| cities_pdf_dp365a_appendix_2 | 4 | `page_ocr_text_detected` | 695 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p004.png |
| cities_pdf_dp365a_appendix_2 | 5 | `page_ocr_text_detected` | 636 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p005.png |
| cities_pdf_dp365a_appendix_2 | 6 | `page_ocr_text_detected` | 632 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p006.png |
| cities_pdf_dp365a_appendix_2 | 7 | `page_ocr_text_detected` | 528 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p007.png |
| cities_pdf_dp365a_appendix_2 | 8 | `page_ocr_text_detected` | 569 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p008.png |
| cities_pdf_dp365a_appendix_2 | 9 | `page_ocr_text_detected` | 546 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p009.png |
| cities_pdf_dp365a_appendix_2 | 10 | `page_ocr_text_detected` | 682 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_2_p010.png |
| cities_pdf_dp365a_appendix_4 | 1 | `page_ocr_text_detected` | 934 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_4_p001.png |
| cities_pdf_dp365a_appendix_4 | 2 | `page_ocr_text_detected` | 496 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_4_p002.png |
| cities_pdf_dp365a_appendix_5 | 1 | `page_ocr_text_detected` | 555 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_5_p001.png |
| cities_pdf_dp365a_appendix_5 | 2 | `page_ocr_text_detected` | 453 | reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/page_images/cities_pdf_dp365a_appendix_5_p002.png |

## Boundary

- These rows are page-image review records only.
- OCR sidecars remain ignored local files and are not tracked source text.
- Source-row decisions require separate citable decision records.
- No reviewed page here changes source admissibility or creates city-name rows.
- Contact sheets and page images remain visual aids, not public source-text artifacts.
