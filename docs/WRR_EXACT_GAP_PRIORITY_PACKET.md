# WRR Exact Gap Priority Packet

Status: no-input priority packet for the exact-published WRR reproduction gap.

This packet ranks current evidence tasks. It does not select source corrections, pair exclusions, replacement spellings, or method changes.

## Setup

```bash
python3 -m scripts.build_wrr_exact_gap_priority_packet
```

## Current Boundary

| Metric | Value |
| --- | ---: |
| Source-cited defined distances | 163 |
| Current defined distances | 72 |
| Remaining 163-distance gap | 91 |
| Review lanes | 4 |
| Source-row clusters | 22 |

## Priority Lanes

| Priority | Lane | Value | Evidence required | Boundary |
| ---: | --- | --- | --- | --- |
| 1 | `source_policy_or_pair_rule_review` | 1 terms; 1 residual pairs; 1 frontier pairs | citable source-policy or pair-rule evidence for whether the flagged appellation belongs in the selected pair universe | keep term in working source; no automatic correction or exclusion without citable rule |
| 2 | `source_transcription_or_row_alignment` | 43 terms; 44 residual pairs; 35 frontier pairs | primary table row transcription or row-alignment evidence for the imported term; current queue has no simple variant lead | keep imported term; do not correct transcription until primary row evidence is locked |
| 3 | `page_image_near_match_review` | 3 terms; 3 residual pairs; 2 frontier pairs | page-image inspection against near-match OCR before treating the term as source text or method blocker | keep imported term; do not treat near OCR as correction without page-image review |
| 4 | `method_or_pair_universe_review` | 11 terms; 11 residual pairs; 2 frontier pairs | method and pair-universe review because OCR already matched but ordinary hits remain absent | keep source row; investigate ordinary-hit method or pair universe before source edits |

## Source-Row Clusters

Full CSV includes 22 row clusters. Top clusters by action terms; review rank is from the source-row checklist:

| Review rank | Row | Value | Read |
| ---: | --- | --- | --- |
| 1 | row 06 WRR2 06 | 4 action terms; 4 residual pairs; 4 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 20 | row 30 WRR2 30 | 4 action terms; 4 residual pairs; 0 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 2 | row 14 WRR2 14 | 3 action terms; 3 residual pairs; 3 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 3 | row 24 WRR2 24 | 3 action terms; 3 residual pairs; 3 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 4 | row 01 WRR2 01 | 2 action terms; 2 residual pairs; 2 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 5 | row 03 WRR2 03 | 2 action terms; 2 residual pairs; 2 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 6 | row 09 WRR2 09 | 2 action terms; 2 residual pairs; 2 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 7 | row 10 WRR2 10 | 2 action terms; 2 residual pairs; 2 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 8 | row 11 WRR2 11 | 2 action terms; 2 residual pairs; 2 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |
| 9 | row 15 WRR2 15 | 2 action terms; 2 residual pairs; 2 frontier pairs | multi-term row cluster; review row image/alignment once before term edits |

## Remaining And Method Lanes

| Section | Item | Value | Boundary | Read |
| --- | --- | --- | --- | --- |
| remaining_lane | `page_image_near_match_review` | 3 terms; 3 residual pairs; 2 frontier pairs | No automatic source correction or method change; page-image, method, or pair-universe evidence must be locked first. | near OCR exists, but page image must decide whether it is source evidence |
| remaining_lane | `method_or_pair_universe_review` | 11 terms; 11 residual pairs; 2 frontier pairs | No automatic source correction or method change; page-image, method, or pair-universe evidence must be locked first. | OCR matched the imported term; investigate method or pair universe before source edits |
| method_pair_universe | `ocr_matched_zero_ordinary_hits` | 11 OCR-matched terms; 11 zero high-cap appellation-hit terms; 2 both-side-zero pairs | do not treat OCR-matched missing ordinary hits as source corrections | OCR matched all method-lane terms, but current Koren Genesis ordinary-hit search still leaves them undefined. |

## Gap Reasons

| Reason | Pairs | Read |
| --- | ---: | --- |
| `ordinary_missing_appellation_hits` | 83 | ordinary pair blocked because appellation has zero ordinary hits in this run |
| `ordinary_missing_date_hits` | 12 | ordinary pair blocked because date has zero ordinary hits in this run |
| `ordinary_missing_both_terms` | 15 | ordinary pair blocked because both terms have zero ordinary hits in this run |

## Cautions

- This is an evidence-priority packet, not an exact published WRR reproduction result.
- Do not describe the local locked-method result as exact published reproduction.
- Do not promote OCR near matches, WNP/context flags, or zero-hit method diagnostics into source edits without citable source evidence.
- Raw lane counts are review workload counts, not statistical significance tests.
