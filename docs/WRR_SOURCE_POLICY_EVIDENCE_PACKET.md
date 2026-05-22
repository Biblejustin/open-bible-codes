# WRR Source-Policy Evidence Packet

Status: diagnostic evidence packet for source-policy residual terms.
It does not choose a source correction, exclude a pair, or lock a replacement.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_policy_evidence_packet --action-plan reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --row-ocr reports/wrr_1994/wrr_primary_table2_row_ocr_probe.csv --scenario-pairs reports/wrr_1994/wrr_source_policy_scenario_pairs.csv --table2-bridge reports/wrr_1994/wrr_table2_source_bridge.csv --wnp-html reports/wrr_1994/wnp_en.html --out reports/wrr_1994/wrr_source_policy_evidence_packet.csv --source-context-out reports/wrr_1994/wrr_source_policy_evidence_context.csv --summary-out reports/wrr_1994/wrr_source_policy_evidence_summary.csv --markdown-out docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md --manifest-out reports/wrr_1994/wrr_source_policy_evidence_packet.manifest.json
```

## Current Read

- Priority source-policy terms: 1.
- Related source-review rows: 2.
- Related scenario-pair rows: 4.
- WNP context blocks: 3.
- Boundary: No automatic correction or exclusion; source-policy targets need citable pair-rule evidence before changing the working source.

## Priority Source-Policy Targets

| Rank | Term id | Term | Concept | Source flags | Residual pairs | Frontier pairs | Evidence read |
| ---: | --- | --- | --- | --- | ---: | ---: | --- |
| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `WRR2 32` | `wnp_chelm_spelling_context` | 1 | 1 | wrr2_32_app_05 is a Chełm spelling-context target; local evidence supports review scope, while row OCR still leaves the pair-rule/source-cell decision open |

## Related Source-Queue Context

| Term id | Term | OCR status | Variant hits | Source action | Visual action |
| --- | --- | --- | ---: | --- | --- |
| `wrr2_32_app_04` | `$LMHMXLMA` | not_matched | 1 | source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass | review source/pair rule before using this as a Hebrew-cell match |
| `wrr2_32_app_05` | `$LMHMX@LMA` | not_matched | 0 | source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass |  |

## Row OCR Context

| Term id | Term | Category | OCR status | Column OCR read |
| --- | --- | --- | --- | --- |
| `wrr2_32_app_01` | `RBY$LMH` | wrr_appellation | matched | `רבישלמהה` |
| `wrr2_32_app_02` | `MRKBTHM$NH` | wrr_appellation | not_matched | `רבישלמהה` |
| `wrr2_32_app_03` | `B@LMRKBTHM$NH` | wrr_appellation | not_matched | `רבישלמהה` |
| `wrr2_32_app_04` | `$LMHMXLMA` | wrr_appellation | not_matched | `רבישלמהה` |
| `wrr2_32_app_05` | `$LMHMX@LMA` | wrr_appellation | not_matched | `רבישלמהה` |
| `wrr2_32_date_01` | `/KA/TMWZ` | wrr_date | matched | `כאתמוזבכאתמוזכאבתמוז` |

## Local WNP Context

| Context | Source ref | Source terms | Read |
| --- | --- | --- | --- |
| `wnp_chelm_spelling_argument` | `reports/wrr_1994/wnp_en.html:608-619` | `clma; cilma; wlmh clma; wlmh cilma` | WNP discusses Chelma spellings and says the practical additions are cilma and wlmh clma under the 5-8 letter filter. |
| `wnp_chelm_appellation_table` | `reports/wrr_1994/wnp_en.html:931-935` | `rby wlmh; cilma; wlmh clma` | WNP table context lists row 32 with rby wlmh plus cilma and wlmh clma. |
| `wnp_chelm_bibliography_context` | `reports/wrr_1994/wnp_en.html:1052-1054` | `r' wlmh cilma; mrkbt hmwnh` | WNP bibliography context cites a Brik biography title using wlmh cilma. |

## Scenario Status

| Scenario | Pair id | Action | Review status | Candidate lane |
| --- | --- | --- | --- | --- |
| `review_chelm_spelling_only` | `wrr2_32_app_04__wrr2_32_date_01` | review_only_no_exclusion | needs_primary_source_pair_rule | appellation_min_length_candidate |
| `review_chelm_spelling_only` | `wrr2_32_app_05__wrr2_32_date_01` | review_only_no_exclusion | needs_primary_source_pair_rule | appellation_min_length_candidate |
| `exclude_all_source_review_flags` | `wrr2_32_app_04__wrr2_32_date_01` | excluded | needs_primary_source_pair_rule | appellation_min_length_candidate |
| `exclude_all_source_review_flags` | `wrr2_32_app_05__wrr2_32_date_01` | excluded | needs_primary_source_pair_rule | appellation_min_length_candidate |

## No-Input Boundary

- No automatic correction or exclusion comes from this packet.
- Row OCR supports the visible Rabbi Shelomo baseline and date in this pass; it does not lock the Chełm forms.
- WNP context supports why the Chełm forms are in review scope, not a final pair-rule decision.
- Keep the working source unchanged until source/pair-rule review is citable enough to lock.
