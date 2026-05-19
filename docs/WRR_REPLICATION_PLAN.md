# WRR 1994 Replication Plan

Status: planned, not yet reproduced.

Target paper:

- Witztum, Rips, and Rosenberg, "Equidistant Letter Sequences in the Book of Genesis," `Statistical Science` 9:3, 1994.
- DOI: `10.1214/ss/1177010393`

## Goal

Build a clean-room, open-license replication path for the WRR-style Genesis
rabbi/date experiment without copying disputed code or unclear term data.

## Locked Inputs Needed

Before any result can be called a WRR reproduction, the repo needs:

- exact Genesis source text and normalization rule;
- exact 32 rabbi/appellation list from a citable source;
- exact Hebrew date encodings paired to those rabbis;
- exact row-width or cylinder rule;
- exact distance/compactness formula;
- exact aggregate statistic;
- exact permutation/randomization procedure;
- declared correction or ranking rule before looking at results.

## Existing Building Blocks

Already implemented:

- signed forward/backward ELS search;
- minimal-hit and skip-cap helpers;
- matrix coordinate export;
- cylindrical pair distance;
- pair compactness columns;
- empirical tail p-value helpers;
- Benjamini-Hochberg q-value helpers;
- protocol manifests with input/output fingerprints.
- external WRR plain-text list importer in `scripts/import_wrr_terms.py`.
- WRR imported-term Genesis count smoke in `protocols/wrr_audit_counts.toml`.
- WRR same-record appellation/date pair audit smoke in `scripts/analyze_wrr_pair_audit.py`.
- top WRR pair-audit control screen in `scripts/analyze_wrr_pair_controls.py`.
- WRR appendix-compatible length `5..8` audit/control smoke in the same protocol.
- WRR statistic arithmetic helpers in `els/wrr.py` for skip-window expectation,
  conservative supplied-row domain labeling for unambiguous shorter-skip cases,
  domain-weighted `Q(w,w')` summation over already-domain-labeled ELS rows,
  strict WRR 1994 corrected-distance rank over already-computed perturbation
  proximities, `P1`, `P2`, permutation rank, and Bonferroni `rho0`.
- WRR expected-count skip-cap audit in `scripts/analyze_wrr_skip_caps.py`.
- WRR lock-prep pair eligibility table in
  `scripts/build_wrr_pair_eligibility_table.py`, joining imported pair rows,
  Genesis count smoke, expected-count skip caps, and nearest-pair audit
  metrics.

Source audit:

- `docs/WRR_SOURCE_AUDIT.md`
- `docs/WRR_METHODOLOGY_GAPS.md`
- `docs/WRR_CORRECTED_DISTANCE_NOTES.md`

## Not Yet Built

Still needed:

- canonical pair-set reconciliation against the paper's declared sample; the
  current eligibility table is lock prep, not the canonical 163-distance table;
- replication-grade generated or reviewed future file `terms/[wrr_1994_rabbis].csv`;
- replication-grade generated or reviewed future file `terms/[wrr_1994_dates].csv`;
- WRR real-corpus domain-labeling driver, enclosing-span policy, and full
  corrected-distance implementation for `c(w,w')`;
- WRR aggregate runner for `P1`, `P2`, `P3`, and `P4` over all declared pairs
  once `c(w,w')` exists;
- permutation driver that shuffles date/rabbi pairings under the declared rule;
- report that labels each run as reproduction, failed reproduction, or
  under-specified.

## Rules For Adding Terms

Do not add an informal "starter" WRR term list as if it were canonical. Rabbinic
abbreviations already in `terms/hebrew_claim_terms.csv` are useful for screening,
but they are not enough for WRR reproduction.

When the exact source list is added, each row should include:

- `term_id`
- `concept`
- `category`
- `language`
- `term`
- source note naming the source and whether the row is an appellation or date

## Report Standard

Any WRR report should include:

- all skipped or ambiguous terms;
- all spelling/date variants rejected before the run;
- exact source text checksum;
- full command line;
- examples for nearest pairs;
- permutation sample count;
- observed aggregate score;
- empirical p-value with add-one smoothing;
- clear caution that post-hoc spelling or metric edits invalidate the run.
