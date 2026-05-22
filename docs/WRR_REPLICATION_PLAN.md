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
  candidate-domain enumeration for enclosing shorter-skip ambiguity,
  exact perturbed-ELS match checks,
  domain-weighted `Q(w,w')` summation over already-domain-labeled ELS rows,
  source-count WRR corrected-distance rank over already-computed perturbation
  proximities, `P1`, `P2`, permutation rank, and Bonferroni `rho0`.
- WRR expected-count skip-cap audit in `scripts/analyze_wrr_skip_caps.py`.
- WRR lock-prep pair eligibility table in
  `scripts/build_wrr_pair_eligibility_table.py`, joining imported pair rows,
  Genesis count smoke, expected-count skip caps, and nearest-pair audit
  metrics.
- WRR real-corpus domain-labeling diagnostic in
  `scripts/analyze_wrr_domain_labeling.py`, wired into
  `protocols/wrr_audit_counts.toml`, with undefined rows split by reason.
- WRR defined-domain-only ordinary `Q(w,w')` diagnostic in
  `scripts/analyze_wrr_ordinary_q.py`, wired into
  `protocols/wrr_audit_counts.toml`.
- WRR perturbation diagnostic in
  `scripts/analyze_wrr_perturbation_diagnostics.py`, wired into
  `protocols/wrr_audit_counts.toml`, now splitting in-bound perturbations from
  exact perturbed matches for ordinary-hit diagnostics.
- WRR perturbation pair-readiness join in
  `scripts/analyze_wrr_perturbation_pair_readiness.py`, wired into
  `protocols/wrr_audit_counts.toml`, summarizing whether lock-prep pairs pass
  the older ordinary-hit exact-perturbation threshold before pair-level
  perturbed `Q`. This is retained as a legacy diagnostic, not a direct-search
  readiness gate.
- WRR corrected-distance smoke driver in
  `scripts/analyze_wrr_corrected_distance.py`, wired into
  `protocols/wrr_audit_counts.toml`, generating exact perturbed rows by direct
  perturbed-letter search, labeling domains per perturbation triple, and
  applying the source-count `v/m` corrected-distance bridge. Current length-5..8
  cap-250 smoke output defines 28 corrected distances.
- WRR corrected-distance skip-cap variant comparison in
  `scripts/compare_wrr_corrected_distance_variants.py`, wired into
  `protocols/wrr_audit_counts.toml`, comparing term-printed, term-program, and
  fixed-250 settings. Current output defines 28 corrected distances for all
  three variants, each with maximum valid perturbation count 125.
- WRR corrected-distance aggregate diagnostic in
  `scripts/analyze_wrr_corrected_distance_aggregate.py`, wired into
  `protocols/wrr_audit_counts.toml`, computing P1/P2 over all defined
  corrected-distance values and P3/P4 over the smaller non-Rabbi-title sample.
  Current length-5..8 cap-250 smoke output has 28 defined values and diagnostic
  P1..P4 values; this is not claim-grade until the pair universe, `D(w)`, and
  permutation procedure are locked.
- Corrected-distance shard support in `scripts/analyze_wrr_corrected_distance.py`
  plus `scripts/merge_wrr_corrected_distance_shards.py`; see
  `docs/WRR_WINDOWS_SPLIT.md` and
  `protocols/wrr_corrected_distance_split_2.toml` for Mac/Windows split
  commands and local split/merge verification.
- High-cap corrected-distance split diagnostic in
  `protocols/wrr_corrected_distance_highcap_1000_split_2.toml`, rerunning the
  same smoke lane at `search-max-skip=1000` and joining term-level
  legacy ordinary-hit perturbation readiness output. Current local output
  defines 46 diagnostic corrected distances.
- Direct all-lane corrected-distance diagnostic in
  `protocols/wrr_corrected_distance_direct_all_lanes.toml`, testing all 182
  imported same-record WRR2 pairs. Current output defines 50 diagnostic
  corrected distances at cap 250 and 72 at cap 1000. The same protocol now
  includes a cap-1000 reported-program `D(w)` sensitivity run, which changes 0
  pair rows versus the printed-formula diagnostic; see
  `docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md`.
- WRR2 cross-pair grid in `scripts/build_wrr_cross_pair_grid.py` and
  `protocols/wrr_cross_pair_grid.toml`, crossing every imported appellation
  with every imported date for future date-label permutation diagnostics.
  Current cap-250 diagnostic output defines 1,423 corrected distances over
  5,208 generated rows. The 1,000-sample date-label permutation diagnostic
  ranks the 50 defined observed same-record distances at Bonferroni rho0
  `0.003996003996`. The current repo-defined WNP-excluded 999,999-permutation
  diagnostic ranks 48 defined observed c-values over 174 observed rows at
  Bonferroni rho0 `0.00086`; see `docs/WRR_CROSS_PAIR_GRID.md`.
- WRR claim-readiness gate in `scripts/check_wrr_claim_readiness.py`, wired
  into `protocols/wrr_audit_counts.toml`, keeping reproduction language blocked
  until pair universe, `D(w)`, full corrected distance, and permutation/aggregate
  statuses are locked.

Source audit:

- `docs/WRR_SOURCE_AUDIT.md`
- `docs/WRR_METHODOLOGY_GAPS.md`
- `docs/WRR_CORRECTED_DISTANCE_NOTES.md`

Newly tracked source context includes the MBBK 1999 `Statistical Science`
response, its data page, the Chance article, the Torah-code papers page,
Bombach/Gans/Haralick/Levitt/Rips/Schwartzman/Witztum papers, and their
available data/attachment files.

## Not Yet Built

Still needed:

- candidate pair-set reconciliation against the paper's declared sample; the
  current eligibility table is lock prep, and `163` is treated as the
  source-defined corrected-distance output count rather than a raw pair table;
- replication-grade generated or reviewed future file `terms/[wrr_1994_rabbis].csv`;
- replication-grade generated or reviewed future file `terms/[wrr_1994_dates].csv`;
- final `D(w)` formula decision between the printed WRR formula and the WRR
  program formula documented by MBBK;
- optimized full corrected-distance run over the final locked pair universe;
- WRR claim-grade aggregate runner for `P1`, `P2`, `P3`, and `P4` over all
  declared pairs once `c(w,w')` exists;
- claim-grade permutation driver that shuffles date/rabbi pairings under the
  declared rule, using the cross-pair corrected-distance matrix once locked;
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
