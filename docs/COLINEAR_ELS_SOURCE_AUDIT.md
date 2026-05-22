# Co-linear ELS Source Audit

Status: source-shape audit only. This is not an ELS result, not a
statistical test, and not a claim-ready co-linear ELS reproduction.

## Parsed Shape

| Item | Count |
| --- | ---: |
| paper PDF pages | 3 |
| attachments page PDF links | 8 |
| downloaded attachment PDFs | 8 |
| attachment PDF pages | 515 |
| attachments with expected row counts | 6 |
| expected rows in counted attachments | 8260 |
| observed rows in counted attachments | 8260 |
| PLS pair rows extracted | 6060 |
| PLS missing row indexes | 0 |
| roots rows extracted | 12830 |
| roots single-token rows | 2 |
| all_1698 rows extracted | 1698 |
| all_1698 hash-marker rows | 699 |
| reviewed subset rows extracted | 502 |
| reviewed subset rows with source positions | 389 |

## Attachment PDFs

| Attachment | Pages | Expected Rows | Observed Rows | Numeric Prefix | Hash Rows | Hebrew Lines |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pls | 135 | 6060 | 6060 | 6060 | 0 | 6060 |
| roots | 292 |  |  | 0 | 0 | 12830 |
| all_1698 | 46 | 1698 | 1698 | 999 | 699 | 3027 |
| res_113 | 14 | 113 | 113 | 113 | 0 | 649 |
| consul_138 | 5 | 138 | 138 | 138 | 0 | 319 |
| intersec_108 | 7 | 108 | 108 | 108 | 0 | 278 |
| comb_143 | 6 | 143 | 143 | 143 | 0 | 363 |
| att_heb | 10 |  |  | 0 | 0 | 273 |

## Protocol Anchors

Found anchors: 21 of 21.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| paper | `paper_co_linear_definition` | found | paper defines co-linear ELS relation |
| paper | `paper_pentateuch_min5_lexicon` | found | paper identifies Pentateuch words of length at least 5 |
| paper | `paper_skip_distance_2_to_1000` | found | paper states skip-distance range 2..1000 |
| paper | `paper_6060_pls_found` | found | paper reports 6,060 PLS rows |
| paper | `paper_p_level_6e_minus8` | found | paper reports p-level 6 x 10^-8 |
| attachments_page | `attachments_page_eight_pdf_links` | found | attachments page exposes 8 PDF links |
| attachments | `all_eight_attachment_pdfs_present` | found | all linked attachment PDFs are present locally |
| attachments | `pls_6060_rows_observed` | found | PLS attachment exposes 6,060 source rows |
| pls_pairs | `pls_pairs_6060_machine_rows` | found | PLS PDF extracted to 6,060 machine-readable pair rows |
| roots | `roots_rows_machine_extracted` | found | roots PDF extracted to raw rows with parsed root tokens |
| all_1698 | `all_1698_machine_rows_extracted` | found | all_1698 PDF extracted to 1,698 raw phrase/verse rows |
| attachments | `all_1698_rows_observed` | found | all_1698 attachment exposes 1,698 source rows |
| attachments | `review_sets_502_rows_observed` | found | four reviewed subset attachments expose 502 rows |
| review_sets | `review_sets_502_machine_rows` | found | four reviewed subset PDFs extracted to 502 raw rows |
| att_heb | `att_heb_research_goal` | found | Hebrew appendix states the research goal |
| att_heb | `att_heb_pair_population_rules` | found | Hebrew appendix states word-pair population rules |
| att_heb | `att_heb_pair_population_counts` | found | Hebrew appendix states source word and PLS pair counts |
| att_heb | `att_heb_identical_word_screen` | found | Hebrew appendix explains the identical-word verse screen |
| att_heb | `att_heb_root_relaxation_screen` | found | Hebrew appendix explains the shared-root relaxation screen |
| att_heb | `att_heb_1698_tested_population` | found | Hebrew appendix states the 1,698 tested pair/verse population |
| att_heb | `att_heb_language_matching_rules` | found | Hebrew appendix introduces phrase and meaning-match rules |

## Use Boundary

The paper and attachment files are usable as source-shape material for a
future co-linear ELS/verse protocol. This audit only records file coverage,
protocol anchors, table row counts, raw PLS pair rows, raw roots rows,
raw all_1698 phrase/verse rows, and raw reviewed subset rows. It does
not normalize Hebrew terms, select roots, compute ELSs, score verse
links, or evaluate controls. The att_heb appendix anchors document
method statements only.
