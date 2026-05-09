# BYZ_NT Source-Only Exact-Center Report

Status: source-specific review candidate, not cross-text candidate.

This report records the first run after
`docs/BYZ_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md` and
`protocols/byz_source_only_exact_center.toml` were committed.

## Run

| Field | Value |
| --- | --- |
| Preregistration commit | `212e345` |
| Command | `python3 -m scripts.run_protocol protocols/byz_source_only_exact_center.toml --resume` |
| Protocol | `protocols/byz_source_only_exact_center.toml` |
| Started UTC | `2026-05-05T04:06:30.936591+00:00` |
| Ended UTC | `2026-05-05T04:10:07.986914+00:00` |
| Runtime | 217.047s |
| Status | success |

Step timings:

| Step | Runtime |
| --- | ---: |
| paired_controls | 216.753s |
| context_review | 0.294s |

## Scope

| Field | Value |
| --- | --- |
| Corpus | BYZ_NT |
| Registered row | `υιοσ|-46|backward|before_plus_term|ειουιοσ|ειουιοσ` |
| Control samples | 1000 shuffled-term; 1000 same-length random |
| P-value floor | `0.000999` |
| Cross-text requirement | not part of this source-only follow-up |

Prerequisite local outputs came from
`protocols/greek_exact_center_four_source.toml`.

## Result

| Term | Center | Extension | Matched phrase refs | Score | Term-any p | Random-any p | Combined p | Combined q | Flags |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `υιος` | Acts 16:1 | `ειουιοσ` | Mark 1:11; Mark 3:11; Luke 3:22; Luke 22:70; John 1:49 | 3215 | 0.043956 | 0.004995 | 0.000999 | 0.000999 | `extension_min_p_adjusted;short_base_term` |

The row stayed at the 1000/1000 control floor.

## Context Read

`υιος`:

- center passage: Acts 16:1;
- exact-center surface context: `υιοσ` appears in Acts 16:1;
- hit span: Acts 15:41 through Acts 16:2;
- hidden extension sequence: `ειουιοσ`;
- matched phrase: `εἶ ὁ υἱός` / `ει ο υιοσ`;
- matched phrase references: Mark 1:11; Mark 3:11; Luke 3:22; Luke 22:70;
  John 1:49;
- full matched phrase is not surface text in the Acts 15:41-16:3
  hit/extension span.

Letter paths are saved in:

- `reports/byz_source_only_exact_center/letter_paths.md`

## Preregistration Check

| Criterion | Result | Note |
| --- | --- | --- |
| Registered row present | pass | BYZ_NT `υιος|-46` row found |
| Exact-center surface context | pass | Acts 16:1 contains `υιοσ` as surface text |
| `combined_min_q <= 0.01` | pass | q = `0.000999` |
| Examples and letter paths generated | pass | Generated in local ignored reports |
| Full phrase location reported | pass | Hidden-path only in the hit/extension span |
| Source-only boundary stated | pass | This report does not claim cross-text support |

## Interpretation

This row qualifies only as:

- `source_specific_review_candidate`

It does not qualify as:

- `controlled_cross_text_candidate`
- `confirmed_code`
- `proof`
- `prophecy`
- `statistical_discovery`

The result is worth internal review because it has exact-center surface context
and favorable 1000/1000 controls within BYZ_NT. It remains weak for external
claims because it is source-only, short-base-term, and hidden-path only in the
hit span.
