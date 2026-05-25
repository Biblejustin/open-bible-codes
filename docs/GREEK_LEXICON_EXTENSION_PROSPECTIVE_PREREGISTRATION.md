# Greek Lexicon Extension Prospective Preregistration

Status: historical preregistration for a completed lane. The result-producing
extension run finished and is now context-cautioned review material, not claim
evidence.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `greek_lexicon_extension_prospective` |
| Study status | completed context-cautioned review material |
| Source packet | `docs/GREEK_LEXICON_PROSPECTIVE_SOURCE.md` |
| Source term file | `terms/greek_lexicon_prospective_terms.csv` |
| Clean locked term file | `terms/greek_lexicon_extension_terms_clean_lock.csv` |
| Lock protocol | `protocols/greek_lexicon_extension_prospective_lock.toml` |
| Lock manifest | `reports/study_locks/greek_lexicon_extension_prospective.manifest.json` |

## Question

Do fresh, lexicon-derived Greek headwords from Strong's Greek Dictionary produce
four-source exact-center, same-skip extension rows in the Greek New Testament
corpora more often than matched term and random controls?

This is intentionally separate from the existing `doxa` follow-up. Existing
`doxa` and Greek surface rows remain prior evidence and are excluded before this
study can produce any result-bearing outputs.

## Term List

Source builder:

```bash
python3 -m scripts.build_greek_lexicon_prospective_terms --download
```

Source rows:

- parsed Strong Greek entries: 5523;
- length >= 5 deduped source rows: 5038;
- strict prior-evidence drops: 29;
- clean locked rows: 5009.

Clean-lock command:

```bash
python3 -m scripts.filter_prospective_terms \
  --candidate terms/greek_lexicon_prospective_terms.csv \
  --audit reports/study_locks/greek_lexicon_extension_prior_evidence_audit.csv \
  --out terms/greek_lexicon_extension_terms_clean_lock.csv \
  --summary-out reports/study_locks/greek_lexicon_extension_terms_clean_lock.summary.json \
  --min-normalized-length 5 \
  --min-remaining 1000
```

Clean audit must pass before any result search:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/greek_lexicon_extension_terms_clean_lock.csv \
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
  --out reports/study_locks/greek_lexicon_extension_clean_audit.csv \
  --summary-out reports/study_locks/greek_lexicon_extension_clean_audit.csv.summary.json \
  --fail-on-match
```

Current clean audit status: passed, 0 overlap rows.

## Source Texts

Compared Greek New Testament source labels:

- `TR_NT` from `configs/example_ebible_grctr.toml`;
- `BYZ_NT` from `configs/example_ebible_grcmt.toml`;
- `TCG_NT` from `configs/example_ebible_grctcgnt.toml`;
- `SBLGNT` from `configs/example_sblgnt.toml`.

The study records exact source presence. A row that appears in fewer than all
four sources may be useful for review, but it does not satisfy the primary
all-source rule.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..50` |
| Direction | `both` |
| Minimum normalized length | `5` |
| Candidate rule | all-source exact-center same-skip extension row |
| Context rule | extension row must retain exact-center target placement |
| Stage A controls | 5000 matched term controls and 5000 random controls |
| Stage B controls | 20000 matched term controls and 20000 random controls for any Stage A survivor |
| Correction method | Benjamini-Hochberg across all selected rows in the registered family |
| Prior-evidence exclusion | exact and substring overlap with registered Greek prior evidence |

## Lock Manifest

Build the non-result lock packet:

```bash
python3 -m scripts.run_protocol \
  protocols/greek_lexicon_extension_prospective_lock.toml --resume
```

Preflight command used before the result-producing run:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_PREREGISTRATION.md \
  --manifest reports/study_locks/greek_lexicon_extension_prospective.manifest.json \
  --protocol protocols/greek_lexicon_extension_prospective_lock.toml \
  --clean-term-audit reports/study_locks/greek_lexicon_extension_clean_audit.csv.summary.json
```

The preflight was required after the lock files were committed, because it
requires a clean git working tree.

## Completed Result Run

The registered result-producing protocols reused
`scripts.analyze_extension_paired_controls` and the same extension/control
family as the existing exact-center extension studies, but with
`terms/greek_lexicon_extension_terms_clean_lock.csv` as the locked target pool.

Stage A kept compute bounded. Stage B confirmed apparent Stage A survivors with
a larger fixed control budget before any row could be called a review
candidate. The completed report is
`docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md`.

## Primary Outcome

Primary row-level outcome:

- all four Greek NT corpora preserve the exact-center same-skip extension row;
- Stage B corrected q value is at most 0.05.

Primary study-level outcome:

- at least one row survives the registered all-source extension rule and
  Benjamini-Hochberg correction after the Stage B confirmation budget.

## Cautions

Raw hit counts are not significance tests. This lane must not promote any row
without the matched term controls, random controls, and correction above.

Large lexicon pools increase the chance of ordinary matches. The clean lock
only protects against reuse of already seen Greek terms and strings; it does
not make future rows meaningful by itself.

Any future local surface-context effect, self-lexeme effect, or obvious
dictionary-headword artifact must stay review-only even if it clears an initial
numeric screen.
