# WRR Source-Policy Review Checklist

Status: no-input checklist for Chełm source-policy/pair-rule review.
It does not choose a source correction, exclude a pair, or lock a replacement.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_policy_review_checklist --packet reports/wrr_1994/wrr_source_policy_evidence_packet.csv --context reports/wrr_1994/wrr_source_policy_evidence_context.csv --summary reports/wrr_1994/wrr_source_policy_evidence_summary.csv --out reports/wrr_1994/wrr_source_policy_review_checklist.csv --markdown-out docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md --manifest-out reports/wrr_1994/wrr_source_policy_review_checklist.manifest.json
```

## Current Read

- Source-policy checklist terms: 1.
- Residual pair links: 1.
- Minimum-frontier pair links: 1.
- Related source-review rows: 2.
- Related scenario-pair rows: 4.
- WNP context blocks: 3.
- Boundary: No source correction, pair exclusion, or replacement lock is selected by this checklist.

## Checklist

| Rank | State | Term id | Term | Concept | Source flags | Pairs | Frontier | Next manual action |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | --- |
| 1 | `pending_source_policy_pair_rule_lock` | `wrr2_32_app_05` | `$LMHMX@LMA` | `WRR2 32` | `wnp_chelm_spelling_context` | 1 | 1 | cite primary source/pair-rule evidence before changing working source |

## Context Blocks

| Context | Source ref | Source terms | Read |
| --- | --- | --- | --- |
| `wnp_chelm_spelling_argument` | `reports/wrr_1994/wnp_en.html:608-619` | `clma; cilma; wlmh clma; wlmh cilma` | WNP discusses Chelma spellings and says the practical additions are cilma and wlmh clma under the 5-8 letter filter. |
| `wnp_chelm_appellation_table` | `reports/wrr_1994/wnp_en.html:931-935` | `rby wlmh; cilma; wlmh clma` | WNP table context lists row 32 with rby wlmh plus cilma and wlmh clma. |
| `wnp_chelm_bibliography_context` | `reports/wrr_1994/wnp_en.html:1052-1054` | `r' wlmh cilma; mrkbt hmwnh` | WNP bibliography context cites a Brik biography title using wlmh cilma. |

## Required Decision Record

- Citable primary source/pair-rule evidence is required before changing the working source.
- The record must say whether Chełm forms belong in the Hebrew source cell, a source-policy note, or neither.
- Preserve the working source until that decision record exists.
