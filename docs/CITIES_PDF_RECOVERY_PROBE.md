# Cities PDF Recovery Probe

Status: live/archive PDF recovery probe only. This does not run ELS
searches, does not update the cached `reports/wrr_1994/` bundle, and
does not make claim-ready source decisions.

## Summary

| Item | Count |
| --- | ---: |
| PDF URLs probed | 35 |
| live PDF rows | 0 |
| live HTML/other rows | 35 |
| archived rows downloaded or cached | 12 |
| rows checked with CDX fallback | 2 |
| rows with CDX exact-URL candidates | 2 |
| archived PDF rows | 12 |
| usable PDF rows | 12 |
| unrecovered PDF rows | 23 |

Current PDF recovery status: `partial_pdf_sources_recovered`.

## Usable PDF Rows

| Label | Source pages | Selected | Pages | Text chars | SHA-256 | Source URL |
| --- | --- | --- | ---: | ---: | --- | --- |
| cities_pdf_wrr | torah_code_experiment_cities_aumann | archive | 10 | 0 | `a63419d9f20ba23f` | [url](https://www.torah-code.org/experiments/WRR.pdf) |
| cities_pdf_dp365a_appendix_6 | torah_code_experiment_cities_aumann | archive | 2 | 0 | `5d9949a0a348bcd9` | [url](https://www.torah-code.org/experiments/dp365A_appendix_6.pdf) |
| cities_pdf_dp365a_appendix_7 | torah_code_experiment_cities_aumann | archive | 5 | 0 | `7b7e2015bb628417` | [url](https://www.torah-code.org/experiments/dp365A_appendix_7.pdf) |
| cities_pdf_dp365a_p1_4 | torah_code_experiment_cities_aumann | archive | 4 | 6115 | `90fb6ff653d2fc97` | [url](https://www.torah-code.org/experiments/dp365A_p1-4.pdf) |
| cities_pdf_dp365a_p12_17 | torah_code_experiment_cities_aumann | archive | 6 | 37639 | `127d829147cbc1ec` | [url](https://www.torah-code.org/experiments/dp365A_p12-17.pdf) |
| cities_pdf_dp365a_p5_11 | torah_code_experiment_cities_aumann | archive | 7 | 18107 | `e89e869d452f4294` | [url](https://www.torah-code.org/experiments/dp365A_p5-11.pdf) |
| cities_pdf_dp365a_part_2_p105_111 | torah_code_experiment_cities_aumann | archive | 7 | 0 | `248d3ff6a9fd1042` | [url](https://www.torah-code.org/experiments/dp365A_part_2_p105-111.pdf) |
| cities_pdf_dp_365_1 | torah_code_experiment_cities_aumann | archive | 2 | 7044 | `ae09dc718ad2e798` | [url](https://www.torah-code.org/experiments/dp_365_1.pdf) |
| cities_pdf_dp_365_2 | torah_code_experiment_cities_aumann | archive | 2 | 6248 | `5301f21fa3c1b5b8` | [url](https://www.torah-code.org/experiments/dp_365_2.pdf) |
| cities_pdf_dp_365_4 | torah_code_experiment_cities_aumann | archive | 2 | 5759 | `4dc4119f30430dc2` | [url](https://www.torah-code.org/experiments/dp_365_4.pdf) |
| cities_pdf_communities_data | torah_code_experiment_cities_gans | archive | 8 | 30281 | `ac0b221064e144ca` | [url](https://www.torah-code.org/papers/communities_data.pdf) |
| cities_pdf_gans | torah_code_experiment_cities_gans | archive | 5 | 25846 | `212cb24f918b9a41` | [url](https://www.torah-code.org/papers/gans.pdf) |

## Unrecovered PDF Rows

| Label | Source pages | Live kind | Archive status | CDX candidates | URL |
| --- | --- | --- | --- | ---: | --- |
| cities_pdf_margcities | torah_code_experiment_cities_simon_mckay | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/Margcities.pdf) |
| cities_pdf_margoliot_cities_data | torah_code_experiment_cities_simon_mckay | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/Margoliot_Cities_Data.pdf) |
| cities_pdf_cities_comparison | torah_code_experiment_cities_simon_mckay | html | no_archived_snapshot | 0 | [url](https://www.torah-code.org/experiments/cities_comparison.pdf) |
| cities_pdf_dp364_appendix_3 | torah_code_experiment_cities_aumann | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/dp364_appendix_3.pdf) |
| cities_pdf_dp364_appendix_4 | torah_code_experiment_cities_aumann | html | no_archived_snapshot | 0 | [url](https://www.torah-code.org/experiments/dp364_appendix_4.pdf) |
| cities_pdf_dp364_appendix_5 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp364_appendix_5.pdf) |
| cities_pdf_dp364_short | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp364_short.pdf) |
| cities_pdf_dp365a_appendix_1 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp365A_appendix_1.pdf) |
| cities_pdf_dp365a_appendix_2 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp365A_appendix_2.pdf) |
| cities_pdf_dp365a_appendix_3 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp365A_appendix_3.pdf) |
| cities_pdf_dp365a_appendix_4 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp365A_appendix_4.pdf) |
| cities_pdf_dp365a_appendix_5 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp365A_appendix_5.pdf) |
| cities_pdf_dp365a_p17_24 | torah_code_experiment_cities_aumann | html | no_archived_snapshot | 0 | [url](https://www.torah-code.org/experiments/dp365A_p17-24.pdf) |
| cities_pdf_dp365a_part_2_p111_130 | torah_code_experiment_cities_aumann | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p111-130.pdf) |
| cities_pdf_dp365a_part_2_p131_139 | torah_code_experiment_cities_aumann | html | no_archived_snapshot | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p131-139.pdf) |
| cities_pdf_dp365a_part_2_p140_143 | torah_code_experiment_cities_aumann | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p140-143.pdf) |
| cities_pdf_dp365a_part_2_p144_152 | torah_code_experiment_cities_aumann | html | no_archived_snapshot | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p144-152.pdf) |
| cities_pdf_dp365a_part_2_p153_159 | torah_code_experiment_cities_aumann | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p153-159.pdf) |
| cities_pdf_dp365a_part_2_p90_96 | torah_code_experiment_cities_aumann | html | no_archived_snapshot | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p90-96.pdf) |
| cities_pdf_dp365a_part_2_p97_105 | torah_code_experiment_cities_aumann | html | archive_error:URLError | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_p97-105.pdf) |
| cities_pdf_dp365a_part_2_preface | torah_code_experiment_cities_aumann | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/dp365A_part_2_preface.pdf) |
| cities_pdf_dp_365_3 | torah_code_experiment_cities_aumann | html | archive_error:TimeoutError | 0 | [url](https://www.torah-code.org/experiments/dp_365_3.pdf) |
| cities_pdf_gans_original_report | torah_code_experiment_cities;torah_code_experiment_cities_aumann | html | archive_error:IncompleteRead | 0 | [url](https://www.torah-code.org/papers/gans_original_report.pdf) |

## Source Boundary

Recovered PDF bytes are source-shape inputs only. This probe verifies
whether linked Cities/Aumann/Simon-McKay PDFs can be fetched live or
through exact-URL Wayback snapshots. It does not perform OCR, city-name
normalization, ELS searches, compactness calculations, or p-level
verification.

Follow-up source-shape text classification lives in
`docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md`; that audit separates recovered PDFs
into extractable, zero-text, and garbled/non-Latin buckets without changing this
probe's recovery-only boundary.
