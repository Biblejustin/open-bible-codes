# BYZ_NT Source-Only Exact-Center Preregistration

Status: post-discovery source-specific follow-up.

This document freezes a narrow follow-up for the BYZ_NT source-only exact-center
row surfaced by the Greek pattern-presence matrix. It is not prospective with
respect to row discovery; it is prospective only with respect to the control and
context-review run below.

## Question

Does the BYZ_NT source-specific exact-center row remain unusual under 1000
shuffled-term and 1000 same-length random controls within BYZ_NT?

## Registered Row

| Field | Value |
| --- | --- |
| Corpus | BYZ_NT |
| Pattern key | `υιοσ|-46|backward|before_plus_term|ειουιοσ|ειουιοσ` (huios / eiouios; English: son / hidden extension form from huios) |
| Base term | `υιοσ` (huios; English: son) |
| Extension sequence | `ειουιοσ` (eiouios; English: hidden extension form from huios) |
| Source of row | `reports/greek_exact_center_four_source/extensions_byz_nt_top.csv` |
| Surface context source | `reports/greek_exact_center_four_source/surface_context_hits.csv` |

This is a source-specific row, not a cross-text row.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/byz_source_only_exact_center.toml --resume
```

Locked settings:

- include only the registered exact extension key;
- require exact-center surface context;
- corpus: BYZ_NT from `configs/example_ebible_grcmt.toml`;
- 1000 shuffled-term controls;
- 1000 same-length random controls;
- same skip, direction, and extension settings as the observed row;
- context review requires a control row.

## Outputs

- `reports/byz_source_only_exact_center/paired_controls_summary.csv`
- `reports/byz_source_only_exact_center/paired_controls_examples.csv`
- `reports/byz_source_only_exact_center/context_review_summary.csv`
- `reports/byz_source_only_exact_center/context_review.md`
- `reports/byz_source_only_exact_center/letter_paths.md`
- `reports/byz_source_only_exact_center/protocol_run.manifest.json`

Tracked follow-up report:

- `docs/BYZ_SOURCE_ONLY_EXACT_CENTER_REPORT.md`

## Promotion Boundary

The row may be labeled only as:

- `source_specific_review_candidate`

It may not be labeled:

- `cross_text_candidate`
- `confirmed_code`
- `proof`
- `prophecy`
- `statistical_discovery`

## Interpretation Boundary

A favorable result means the row deserves source-specific review inside BYZ_NT.
It does not imply that other Greek NT texts should contain the same pattern.
