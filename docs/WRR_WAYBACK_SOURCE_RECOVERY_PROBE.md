# WRR Wayback Source Recovery Probe

Status: archived-source recovery probe only. This does not run ELS searches,
does not update the cached `reports/wrr_1994/` bundle, and does not make
claim-ready source decisions.

## Summary

| Item | Count |
| --- | ---: |
| Wayback URLs probed | 18 |
| unique research concepts probed | 9 |
| rows with archived snapshot | 5 |
| rows checked with CDX fallback | 14 |
| rows with CDX exact-URL candidates | 1 |
| rows recovered through CDX fallback | 1 |
| archived files downloaded or cached | 5 |
| rows where expected label appeared | 5 |
| unrelated slot/gambling markers | 0 |
| usable archived source rows | 5 |
| usable archived concepts | 5 |
| missing archived concepts | 4 |

Current archive recovery status: `partial_archived_sources_recovered`.

## Usable Archived Concepts

| Concept | Label | Timestamp | Title | Archived source |
| --- | --- | --- | --- | --- |
| research_program_1 | torah_code_research_program_1_shtml | 20220921212759 | Torah Codes -- Research Program | [snapshot](https://web.archive.org/web/20220921212759id_/http://www.torah-code.org/research/research_1.shtml) |
| research_program_2 | torah_code_research_program_2_shtml | 20090125122256 | Torah Codes -- Research Program | [snapshot](https://web.archive.org/web/20090125122256id_/http://www.torah-code.org:80/research/research_2.shtml) |
| model_overview | torah_code_research_model_overview_shtml | 20160615070555 | Torah Codes -- The Model | [snapshot](https://web.archive.org/web/20160615070555id_/http://www.torah-code.org:80/research/research_2a.shtml) |
| geometric_model_level_1 | torah_code_research_geometric_model_level_1_shtml | 20150728045249 | Torah Codes -- The Geometric Model | [snapshot](https://web.archive.org/web/20150728045249id_/http://www.torah-code.org:80/research/research_3.shtml) |
| els_model_level_1 | torah_code_research_els_model_level_1_shtml | 20150728045254 | Torah Codes -- ELS Model Level 1 | [snapshot](https://web.archive.org/web/20150728045254id_/http://www.torah-code.org:80/research/research_3c.shtml) |

## Missing Archived Concepts

| Concept | Read |
| --- | --- |
| els_model_level_2 | no usable archived source recovered in this probe |
| els_model_level_3 | no usable archived source recovered in this probe |
| geometric_model_level_2 | no usable archived source recovered in this probe |
| geometric_model_level_3 | no usable archived source recovered in this probe |

## Probe Rows

| Label | Available | Source | Timestamp | CDX candidates | Expected Text | Spam Marker | Bytes | SHA-256 | Status |
| --- | --- | --- | --- | ---: | --- | --- | ---: | --- | --- |
| torah_code_research_program_1_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_program_1_shtml | True | availability_closest | 20220921212759 | 0 | True | False | 10423 | `0c1b9806f557db57` | usable_archived_source |
| torah_code_research_program_2_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_program_2_shtml | True | cdx_fallback | 20090125122256 | 3 | True | False | 8536 | `4ba0a3a929e36a3d` | usable_archived_source |
| torah_code_research_model_overview_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_model_overview_shtml | True | availability_closest | 20160615070555 | 0 | True | False | 9885 | `8b96e9f680933611` | usable_archived_source |
| torah_code_research_geometric_model_level_1_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_geometric_model_level_1_shtml | True | availability_closest | 20150728045249 | 0 | True | False | 9058 | `c01daa7f0fbd0cb8` | usable_archived_source |
| torah_code_research_geometric_model_level_2_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_geometric_model_level_2_shtml | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_geometric_model_level_3_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_geometric_model_level_3_shtml | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_els_model_level_1_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_els_model_level_1_shtml | True | availability_closest | 20150728045254 | 0 | True | False | 9776 | `7e4f22c6edfdb0f3` | usable_archived_source |
| torah_code_research_els_model_level_2_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_els_model_level_2_shtml | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_els_model_level_3_html | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |
| torah_code_research_els_model_level_3_shtml | False |  |  | 0 | False | False | 0 |  | no_archived_snapshot |

## Source Boundary

This archive probe recovers research-program and model-context pages when
Wayback has a clean snapshot. It first checks the Wayback closest-snapshot
endpoint and then falls back to CDX exact-URL 200-capture rows when the
closest endpoint returns no archived snapshot. The CDX fallback did not
recover the missing level-2/3 geometric-model or ELS-model pages in this
run, and it does not resolve WRR residual appellation normalization or
pair-rule questions.
