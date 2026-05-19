# Greek Exact-Center Cohort Preregistration

Status: locked prospective cohort protocol.

This document freezes the next broader Greek exact-center extension study before
the new protocol is run. It is prospective for this cohort protocol and term
list. It does not make earlier exploratory extension work prospective.

## Question

Do any locked Greek theological terms produce same-skip phrase extensions that:

1. have exact-center surface context;
2. appear by exact extension key in both TR_NT and SBLGNT;
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
- SBLGNT from `configs/example_sblgnt.toml`

No other Greek NT text is part of this preregistration.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_cohort.toml --resume
```

Locked search settings:

- corpora: TR_NT and SBLGNT
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
- exact cross-text extension-key overlap required
- targets deduped by corpus and extension key
- 1000 shuffled-term controls
- 1000 same-length same-corpus random controls
- same skip, direction, corpus, and extension settings as the observed row

## Primary Outputs

Expected local outputs:

- `reports/greek_exact_center_cohort/surface_context_hits.csv`
- `reports/greek_exact_center_cohort/extensions_tr_nt_top.csv`
- `reports/greek_exact_center_cohort/extensions_sblgnt_top.csv`
- `reports/greek_exact_center_cohort/paired_controls_summary.csv`
- `reports/greek_exact_center_cohort/paired_controls_examples.csv`
- `reports/greek_exact_center_cohort/context_review_summary.csv`
- `reports/greek_exact_center_cohort/letter_paths.md`
- `reports/greek_exact_center_cohort/protocol_run.manifest.json`

The tracked follow-up report should be:

- `docs/GREEK_EXACT_CENTER_COHORT_REPORT.md`

The first locked cohort report is tracked there.

## Primary Outcome

Primary row-level outcome:

- `combined_min_q` from `reports/greek_exact_center_cohort/paired_controls_summary.csv`

Primary cohort-level outcome:

- count of rows with `combined_min_q <= 0.01` after the locked filters

The 1000/1000 p-value floor is:

- `1 / 1001 = 0.000999`

## Promotion Criteria

A row may be labeled only as `controlled_review_candidate` if all criteria pass:

1. exact-center base-term surface context;
2. exact extension-key overlap in both TR_NT and SBLGNT;
3. `combined_min_q <= 0.01`;
4. saved examples and letter paths;
5. full phrase location reported plainly as surface or hidden-path only;
6. warning flags reported;
7. synthetic extension baseline cautions cited;
8. status clearly says review candidate, not claim.

No row may be promoted to:

- `confirmed_code`
- `conclusive evidence`
- `prophecy`
- `statistical discovery`

## Failure Criteria

The cohort produces no controlled review candidate if:

- no exact-center cross-text rows are found;
- all rows have `combined_min_q > 0.01`;
- required examples or letter paths cannot be produced;
- the result depends on unregistered terms, changed skip ranges, changed top-row
  thresholds, or broadened matching rules.

## Reporting Rules

The cohort report must include:

- command used;
- git commit used;
- runtime;
- source text labels;
- term count;
- row counts at each stage;
- exact p/q values for every surviving row;
- warning flags;
- pass/fail table against this preregistration;
- explicit statement that this is a locked cohort protocol but not conclusive evidence of
  theological meaning.

## Interpretation Boundary

This study can identify controlled review candidates. It cannot establish
theological or prophetic claims by itself.

Any stronger claim needs a separately registered claim standard before further
searching.
