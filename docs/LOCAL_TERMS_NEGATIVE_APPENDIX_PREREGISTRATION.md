# Local Terms Negative Appendix Preregistration

Status: locked local curiosity appendix; not claim-level evidence.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `local_terms_negative_appendix` |
| Study status | negative/curiosity appendix |
| Lock manifest | `reports/study_locks/local_terms_negative_appendix.manifest.json` |
| Report document | `docs/LOCAL_TERMS_APPENDIX_REPORT.md` |

## Question

Do the fixed local pastor-business and church-location terms produce exact ELS
presence rows in the selected Hebrew and Greek sources under skip `2..250`,
direction `both`, and minimum normalized length `4`?

This appendix documents presence, absence, source-specific rows, and
representative controls for nonzero rows. It is not a theological or statistical
claim lane.

## Term List

Locked term file:

- `terms/local_terms_appendix.csv`

Rules:

- source term files: fixed local curiosity terms copied from the declared
  modern/local term list;
- language: `hebrew/greek`;
- normalized minimum length: `4`;
- dedupe rule: `language + normalized term`;
- excluded prior rows/forms: wide-focus local rows and modern/geopolitical
  screening rows are prior evidence.

## Source Texts

Corpus/source labels:

- `MT_WLC` from `configs/example_oshb_wlc.toml`;
- `UHB` from `configs/example_uhb.toml`;
- `TR_NT` from `configs/example_ebible_grctr.toml`;
- `SBLGNT` from `configs/example_sblgnt.toml`.

These are broad corpus-presence sources, not aligned textual-critical editions
for claim promotion.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..250` |
| Direction | `both` |
| Minimum normalized length | `4` |
| Candidate selection rule | `exact ELS presence/absence rows` |
| Context rule | `negative appendix; no interpretive promotion` |
| Control budget | `1000 shuffled-term and 1000 random controls for nonzero representative rows` |
| Correction method | `Benjamini-Hochberg across representative control rows` |

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/local_terms_appendix.toml --resume
```

Expected outputs:

- `reports/local_terms_appendix/hebrew_term_summary.csv`;
- `reports/local_terms_appendix/greek_term_summary.csv`;
- `reports/local_terms_appendix/paired_controls_summary.csv`;
- `docs/LOCAL_TERMS_APPENDIX_REPORT.md`;
- `reports/local_terms_appendix/protocol_run.manifest.json`.

## Primary Outcome

Primary row-level outcome:

- presence/absence and representative-control q value when a row is nonzero.

Primary study-level outcome:

- transparent negative/curiosity appendix; no claim-level outcome.

## Candidate Labels

Allowed labels:

- `negative_appendix_row`;
- `source_specific_review_row`;
- `ordinary_controlled_hit`;
- `absent`.

Disallowed labels:

- `confirmed_code`;
- `proof`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Failure Criteria

The appendix fails if:

- the term file or protocol changes after locking without a new manifest;
- nonzero rows are interpreted without representative controls;
- absent rows are omitted from the report;
- wording promotes any local row beyond curiosity/negative appendix status.

## Reporting Rules

The report must include:

- command used;
- source text labels;
- term count;
- exact presence/absence rows;
- representative-control status for nonzero rows;
- explicit statement that this is a curiosity appendix, not proof of meaning.

## Interpretation Boundary

This appendix may document what happened for local curiosity terms. It cannot
establish theological, prophetic, historical, or statistical claims.
