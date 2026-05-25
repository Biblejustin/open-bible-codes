# Greek Lexicon Prospective Source

Status: historical source packet for the completed Greek lexicon extension
lane. No ELS result search is run by this document; the completed result report
is `docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md`.

## Source

The source is `morphgnt/strongs-dictionary-xml`, specifically
`strongsgreek.xml`.

The upstream README states that the XML release is under the Creative Commons
CC0 waiver. Raw XML is cached under ignored `data/raw/` and is not committed.
The tracked derivative term files contain only the selected Greek headwords and
source metadata needed for reproducible study setup.

Source commands:

```bash
python3 -m scripts.build_greek_lexicon_prospective_terms --download
```

Generated source files:

- `data/raw/morphgnt/strongs-dictionary-xml/strongsgreek.xml` (ignored raw XML);
- `terms/greek_lexicon_prospective_terms.csv`;
- `reports/study_locks/greek_lexicon_prospective_terms.summary.json` (ignored summary).

## Method

The builder reads each `<entry>` in the Strong's Greek XML and takes the first
direct `<greek unicode="...">` element as the headword. Later Greek elements
inside definitions or derivations are not treated as headwords.

Rows are normalized with `normalize_text(..., "greek")`. Empty rows and rows
with normalized length below 5 are excluded. Duplicate normalized headwords are
deduplicated by keeping the lowest Strong number as the row identity and
recording all matching Strong IDs in `notes`.

Output schema:

- `term_id`;
- `concept`;
- `category`;
- `language`;
- `term`;
- `notes`.

## Results

Current generated source list:

| Metric | Value |
| --- | ---: |
| Raw parsed Strong entries | 5523 |
| Source term rows, length >= 5 | 5038 |
| `strongs_greek_lexicon` rows | 4821 |
| `strongs_greek_semitic_origin` rows | 217 |

The strict prior-evidence filter removed 29 source rows, leaving
`terms/greek_lexicon_extension_terms_clean_lock.csv` with 5009 rows.

## Audit

The lock audit compares the source terms against prior Greek extension and
surface evidence:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/greek_lexicon_prospective_terms.csv \
  --evidence reports/greek_exact_center_four_source/extensions_tr_nt_top.csv \
  --evidence reports/greek_exact_center_four_source/extensions_byz_nt_top.csv \
  --evidence reports/greek_exact_center_four_source/extensions_tcg_nt_top.csv \
  --evidence reports/greek_exact_center_four_source/extensions_sblgnt_top.csv \
  --evidence reports/greek_expanded_prospective_exact_center/extensions_tr_nt_top.csv \
  --evidence reports/greek_expanded_prospective_exact_center/extensions_byz_nt_top.csv \
  --evidence reports/greek_expanded_prospective_exact_center/extensions_tcg_nt_top.csv \
  --evidence reports/greek_expanded_prospective_exact_center/extensions_sblgnt_top.csv \
  --evidence reports/greek_expanded_surface_triage/selected_patterns.csv \
  --evidence reports/greek_surface_new_terms/selected_patterns.csv \
  --evidence reports/greek_surface_prospective/selected_patterns.csv \
  --evidence reports/extension_exact_center_deep_controls_summary.csv \
  --evidence reports/extension_exact_center_final_gate_summary.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/greek_lexicon_extension_prior_evidence_audit.csv \
  --summary-out reports/study_locks/greek_lexicon_extension_prior_evidence_audit.csv.summary.json
```

Current audit result:

| Metric | Value |
| --- | ---: |
| Candidate rows | 5038 |
| Evidence values | 132 |
| Prior-overlap rows | 131 |
| Exact overlap rows | 13 |
| Substring review rows | 118 |
| Dropped term IDs | 29 |
| Clean-lock rows | 5009 |
| Clean-lock overlap rows | 0 |

## Cautions

This is a term-source lock, not evidence by itself. Strong's headwords are a
large dictionary-like pool, so the completed result search needed predeclared
controls and correction before any row could even become review material.

The source list is lexicon-derived, not a morphology-tagged frequency list.
Some headwords may be rare, proper names, spelling variants, or dictionary forms
that do not surface often in every Greek New Testament corpus.

The clean filter removes direct and substring reuse from registered prior
evidence. It does not guarantee that a hit is meaningful; it only avoids
reusing already seen terms or local text strings as a new prospective claim.
