# SBLGNT Source-Only Exact-Center Report

Status: source-specific review candidates, not cross-text candidates.

This report records the first run after
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md` and
`protocols/sblgnt_source_only_exact_center.toml` were committed.

## Run

| Field | Value |
| --- | --- |
| Preregistration commit | `b2c3b88` |
| Command | `python3 -m scripts.run_protocol protocols/sblgnt_source_only_exact_center.toml --resume` |
| Protocol | `protocols/sblgnt_source_only_exact_center.toml` |
| Started UTC | `2026-05-05T02:08:06.680260+00:00` |
| Ended UTC | `2026-05-05T02:15:07.018500+00:00` |
| Runtime | 420.312s |
| Status | success |

Step timings:

| Step | Runtime |
| --- | ---: |
| paired_controls | 420.029s |
| context_review | 0.282s |

## Scope

| Field | Value |
| --- | --- |
| Corpus | SBLGNT |
| Registered rows | 2 |
| Control samples | 1000 shuffled-term; 1000 same-length random |
| P-value floor | `0.000999` |
| Cross-text requirement | not part of this source-only follow-up |

Prerequisite local outputs came from `protocols/greek_exact_center_cohort.toml`.

## Results

| Term | Center | Extension | Matched phrase ref | Score | Term-any p | Random-any p | Combined p | Combined q | Flags |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `αιμα` (haima; English: blood) | Rev 17:6 | `ναιμανο` (naimano; English: hidden extension form from haima) | Luke 4:27 | 3311 | 0.080919 | 0.000999 | 0.000999 | 0.000999 | `extension_min_p_adjusted;low_random_same_type_variance;short_base_term` |
| `υιος` (huios; English: son) | Luke 19:9 | `ουουιοσ` (ouhuios; English: hidden extension form from huios) | Matt 17:9; Matt 26:24; Mark 14:21; John 4:46 | 3214 | 0.032967 | 0.002997 | 0.000999 | 0.000999 | `extension_min_p_adjusted;low_random_same_type_variance;short_base_term` |

Both rows stayed at the 1000/1000 control floor.

## Context Read

`αιμα` (haima; English: blood):

- center passage: Rev 17:6
- exact-center surface context: `αἵματος` (haimatos; English: of blood) appears in the center/hit passage
- hidden extension sequence: `ναιμανο` (naimano; English: hidden extension form from haima)
- matched phrase: `Ναιμὰν ὁ` (Naiman ho; English: Naaman the)
- matched phrase reference: Luke 4:27
- full matched phrase is not surface text in the Rev 17:5-6 hit/extension span

`υιος` (huios; English: son):

- center passage: Luke 19:9
- exact-center surface context: `υἱὸς` (huios; English: son) appears in Luke 19:9-10
- hidden extension sequence: `ουουιοσ` (ouhuios; English: hidden extension form from huios)
- matched phrase: `οὗ ὁ υἱὸς` (hou ho huios; English: of whom the son)
- matched phrase references: Matt 17:9; Matt 26:24; Mark 14:21; John 4:46
- full matched phrase is not surface text in the Luke 19:8-10 hit/extension span

Letter paths are saved in:

- `reports/sblgnt_source_only_exact_center/letter_paths.md`

## Preregistration Check

| Criterion | `αιμα` (haima; English: blood) | `υιος` (huios; English: son) | Note |
| --- | --- | --- | --- |
| Registered row present | pass | pass | Both rows found |
| Exact-center surface context | pass | pass | Both center passages contain the base term as surface text |
| `combined_min_q <= 0.01` | pass | pass | Both rows are `0.000999` |
| Examples and letter paths generated | pass | pass | Generated in local ignored reports |
| Full phrase location reported | pass | pass | Both are hidden-path only in the hit/extension span |
| Source-only boundary stated | pass | pass | This report does not claim cross-text support |

## Interpretation

Both rows qualify only as:

- `source_specific_review_candidate`

They do not qualify as:

- `controlled_cross_text_candidate`
- `confirmed_code`
- `proof`
- `prophecy`
- `statistical discovery`

The result is worth internal review because both rows have exact-center surface
context and favorable 1000/1000 controls within SBLGNT. The result remains weak
for external claims because both rows are source-only, short-base-term rows, and
the full matched phrases are hidden-path only in the hit spans.

## Next Step

The next useful move is not to promote these rows. It is either:

- add independent Greek NT sources and rerun a locked cross-text cohort; or
- create a formal source-specific study standard that explains why source-only
  rows should be examined despite the weaker evidence boundary.
