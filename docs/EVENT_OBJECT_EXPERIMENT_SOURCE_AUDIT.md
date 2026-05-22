# Event/Object Experiment Source Audit

Status: source-shape audit only. This is not an ELS result, not a
statistical test, and not a claim-ready replication.

## Parsed Shape

| Item | Count |
| --- | ---: |
| source files scanned | 8 |
| HTML files | 5 |
| PDF files | 3 |
| total PDF pages | 59 |
| PDF files with extractable text | 3 |
| protocol-table pages | 3 |
| reported significant follow-up pages | 1 |
| reported non-significant pages | 2 |
| under-construction pages | 1 |
| Sons of Haman keyword rows | 12 |
| Pumbedita numbered source rows | 20 |
| Auschwitz numbered source rows | 32 |
| Auschwitz topic keyword rows | 1 |
| machine data rows extracted | 65 |
| Ark tutorial PDF pages | 57 |

## Declared Status

| Experiment | Source Files | Data Rows | Declared Status | Notes |
| --- | ---: | ---: | --- | --- |
| sons_of_haman | 2 | 12 | reported_significant_followup_after_non_significant_original | main page says original test was not significant; data page lists Hebrew keywords and reports p-value 16.5/10000 for follow-up |
| pumbedita | 2 | 20 | reported_non_significant | source page reports failed significance test; PDF has Amoraim spelling rows |
| auschwitz | 2 | 32 | reported_non_significant_replication | source page cites Witztum probability but reports local replication not significant |
| ark | 2 |  | under_construction | source page is under construction and links a tutorial PDF, not a completed experiment data sheet |

## Protocol Anchors

Found anchors: 10 of 10.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| sons_of_haman | `original_results_not_significant` | found | main page reports non-significant original test |
| sons_of_haman | `followup_p_value_16_5_of_10000` | found | data page reports follow-up p-value |
| sons_of_haman | `followup_trials_10000` | found | data page reports 10000 trials |
| pumbedita | `pumbedita_non_significant` | found | Pumbedita page reports no significant result |
| pumbedita | `pumbedita_pdf_20_rows` | found | Pumbedita PDF has 20 numbered source rows |
| auschwitz | `witztum_probability_1_of_1000000` | found | Auschwitz page cites Witztum probability |
| auschwitz | `auschwitz_non_significant_replication` | found | Auschwitz page reports local replication not significant |
| auschwitz | `auschwitz_pdf_32_rows` | found | Auschwitz PDF has 32 numbered subcamp rows |
| ark | `ark_under_construction` | found | Ark page contains under-construction marker |
| ark | `ark_tutorial_pdf_57_pages` | found | Ark tutorial PDF has 57 pages |

## Use Boundary

This audit records source availability, source shape, row counts, and
declared status for event/object experiment pages. It also exports
machine-readable source rows from the available keyword lists and data
PDFs. It does not normalize Hebrew spellings, choose variants, run ELS
hits, evaluate controls, or verify any reported p-value.
