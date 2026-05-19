# Greek Exact-Center Three-Source Preregistration

Status: locked prospective independent-source protocol.

This document freezes the next Greek exact-center extension study before the
three-source protocol is run. It is prospective for this protocol only. Earlier
TR_NT/SBLGNT and SBLGNT-only extension work remains exploratory or
previously-registered under its own documents.

## Question

Do any locked Greek theological terms produce same-skip phrase extensions that:

1. have exact-center surface context;
2. appear by exact extension key in BYZ_NT and at least one of TR_NT or SBLGNT;
3. remain unusual under 1000 shuffled-term and 1000 same-length random controls;
4. survive manual context and letter-path audit?

## Term List

Locked term file:

- `terms/greek_exact_center_cohort_terms.csv`

Scope:

- Greek terms only
- theological concepts, titles, worship terms, revelation terms, and apocalyptic symbols
- no modern people, geopolitical terms, local names, or ad hoc additions
- normalized length at least 4 in the protocol

The term file is a screening cohort, not a claim list.

## Source Texts

Primary source texts:

- TR_NT from `configs/example_ebible_grctr.toml`
- BYZ_NT from `configs/example_ebible_grcmt.toml`
- SBLGNT from `configs/example_sblgnt.toml`

BYZ_NT is the independent public Byzantine/Majority Text source added after the
first two-source cohort. It uses eBible GRCMT, identified upstream as
Robinson-Pierpont 2018 Byzantine Textform and labeled public domain by eBible.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_three_source.toml --resume
```

Locked search settings:

- corpora: TR_NT, BYZ_NT, and SBLGNT
- skip range: `2..50`
- direction: both
- minimum term length: 4
- surface-context hits only
- extension lookback/lookahead: 12 letters
- phrase lexicon length: up to 4 words
- include both-sided extensions
- max extensions per hit: 20
- extension summary filters:
  - minimum extension length: 3
  - minimum base-term length: 4
  - match kind prefix: `phrase_`
  - top rows per corpus: 1000

Locked control settings:

- exact-center surface context required
- exact extension-key overlap required across at least two corpora
- overlap group must include BYZ_NT
- targets deduped by corpus and extension key
- 1000 shuffled-term controls
- 1000 same-length same-corpus random controls
- same skip, direction, corpus, and extension settings as the observed row

## Primary Outputs

Expected local outputs:

- `reports/greek_exact_center_three_source/surface_context_hits.csv`
- `reports/greek_exact_center_three_source/extensions_tr_nt_top.csv`
- `reports/greek_exact_center_three_source/extensions_byz_nt_top.csv`
- `reports/greek_exact_center_three_source/extensions_sblgnt_top.csv`
- `reports/greek_exact_center_three_source/paired_controls_summary.csv`
- `reports/greek_exact_center_three_source/paired_controls_examples.csv`
- `reports/greek_exact_center_three_source/context_review_summary.csv`
- `reports/greek_exact_center_three_source/letter_paths.md`
- `reports/greek_exact_center_three_source/protocol_run.manifest.json`

The tracked follow-up report should be:

- `docs/GREEK_EXACT_CENTER_THREE_SOURCE_REPORT.md`

## Primary Outcome

Primary row-level outcome:

- `combined_min_q` from
  `reports/greek_exact_center_three_source/paired_controls_summary.csv`

Primary cohort-level outcome:

- count of rows with `combined_min_q <= 0.01` after the locked filters

The 1000/1000 p-value floor is:

- `1 / 1001 = 0.000999`

## Promotion Criteria

A row may be labeled only as `three_source_controlled_review_candidate` if:

1. exact-center base-term surface context;
2. exact extension-key overlap includes BYZ_NT and at least one other Greek NT text;
3. `combined_min_q <= 0.01`;
4. saved examples and letter paths;
5. full phrase location reported plainly as surface or hidden-path only;
6. warning flags reported;
7. status clearly says review candidate, not claim.

Rows present only in TR_NT and SBLGNT do not count as independent-source
support for this protocol.

No row may be promoted to:

- `confirmed_code`
- `conclusive evidence`
- `prophecy`
- `statistical discovery`

## Failure Criteria

The protocol produces no independent-source controlled review candidate if:

- no exact-center overlap row includes BYZ_NT;
- all BYZ_NT overlap rows have `combined_min_q > 0.01`;
- required examples or letter paths cannot be produced;
- the result depends on unregistered terms, changed skip ranges, changed top-row
  thresholds, or broadened matching rules.

## Reporting Rules

The tracked report must include:

- command used;
- git commit used;
- runtime;
- source text labels;
- term count;
- row counts at each stage;
- exact p/q values for every surviving row;
- overlap corpora for every surviving row;
- warning flags;
- pass/fail table against this preregistration;
- explicit statement that this is a locked screening protocol but not conclusive evidence of
  theological meaning.

## Interpretation Boundary

This study can identify independent-source controlled review candidates. It
cannot establish theological or prophetic claims by itself.
