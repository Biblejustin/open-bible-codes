# WRR Source Audit

Status: secondary source path identified; canonical WRR pair table not locked.

## Sources Found

- Primary paper PDF:
  `https://academicweb.nd.edu/~rwilliam/ndonly/readings/Methods/06-ContentAnalysis/Equidistant%20Letter%20Sequences%20in%20the%20Book%20of%20Genesis%201994.pdf`
- WRR/Nations discussion page citing 163 famous-rabbi second-list distances:
  `https://www.math.utoronto.ca/drorbn/Codes/Nations/main_gir.html`
- WRR/Nations discussion page in modified Michigan-Claremont notation:
  `https://www.math.utoronto.ca/drorbn/Codes/Nations/main_mc.html`
- Plain-text data page maintained by Brendan McKay:
  `https://users.cecs.anu.edu.au/~bdm/codes/statsci/data.html`
- WRR first-list plain text:
  `https://users.cecs.anu.edu.au/~bdm/codes/statsci/WRR1.txt`
- WRR second-list plain text:
  `https://users.cecs.anu.edu.au/~bdm/codes/statsci/WRR2.txt`
- Emanuel/Assaf second-list plain text:
  `https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE2a.txt`
- Emanuel corrected second-list plain text:
  `https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE2b.txt`
- Emanuel/Assaf third-list plain text:
  `https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE3.txt`
- Modified Michigan-Claremont transliteration key:
  `https://users.cecs.anu.edu.au/~bdm/codes/MC.html`
- WNP/McKay-Bar-Natan critique page in modified Michigan-Claremont notation:
  `https://users.cecs.anu.edu.au/~bdm/codes/WNP/main_mc.html`
- WNP/McKay-Bar-Natan critique page in English transliteration:
  `https://users.cecs.anu.edu.au/~bdm/codes/WNP/main_en.html`
- Browser-based Bible Codes app page advertised in search/cache results:
  `https://bible-codes.github.io/`
- Browser app source repository advertised in search/cache results:
  `https://github.com/bible-codes/bible-codes.github.io`

## Current Assessment

The WRR paper itself is the citation target for the claim. It states that the
tested sample was the second personality list, that the text was Genesis in the
Koren edition, and that the significance calculation used 999,999 random
permutations. Its Appendix A.3 says the length-5..8 second-list sample consists
of 298 word pairs. Later WRR/Nations discussion material describes the result
as 163 distances. The current audit treats those as different stages: 298
candidate word pairs before the corrected-distance eligibility screen, and 163
defined distances after that screen. The extracted PDF text is not reliable
enough for a machine-ready Hebrew term list because Hebrew table text is
garbled by PDF/OCR extraction.

The ANU/McKay data page provides plain-text WRR lists in a modified
Michigan-Claremont transliteration. That is useful for a reproducible import
path, but it is a secondary critical source rather than the WRR paper itself.

The browser app appears in search/cache results as an Apache-2.0 repository with
a WRR replication interface. In the current audit check, however, the GitHub API
and `git ls-remote` did not expose a cloneable repository at the advertised
path, and the GitHub Pages URL returned a 404 page. Treat this as an
inaccessible source candidate, not an admissible data source. Do not import data
from cached search snippets or screenshots; require a live source URL, stable
file path, license, and checksum before using it as a cross-check.

The TorahBibleCodes repository is visible, but its README asserts restrictive
reuse terms and alleges copyright issues around the browser app. It should not
be copied into this project. Any future comparison against that tool should be
black-box only: run separately, cite observed output, and keep source code/data
out of this repository unless licensing is independently cleared.

## Repo Work Added

`scripts/download_wrr_sources.py` downloads the external audit/source files into
ignored `reports/wrr_1994/` output and records byte counts plus SHA-256 hashes.

`scripts/import_wrr_terms.py` converts an external WRR-style plain-text list
into the repo term CSV schema without committing the source data itself.

`scripts/analyze_wrr_source_shapes.py` summarizes the raw ANU famous-rabbis
source files so the 163-distance mismatch is visible before any metric work.

Example:

```bash
python3 -m scripts.download_wrr_sources \
  --out-dir reports/wrr_1994 \
  --manifest-out reports/wrr_1994/sources.manifest.json

python3 scripts/import_wrr_terms.py \
  --source reports/wrr_1994/WRR2.txt \
  --out reports/wrr_1994/wrr2_terms.csv
```

Protocol:

```bash
python3 -m scripts.run_protocol protocols/wrr_source_import.toml --resume
```

Observed smoke run against the ANU `WRR2.txt` file:

| Item | Count |
| --- | ---: |
| parsed personality records | 32 |
| undated records | 2 |
| default emitted rows | 199 |
| default appellation rows | 168 |
| default date rows | 31 |

The undated record indexes are 4 and 8 in the parsed list, matching the
browser-app note that those records lack recorded death dates.

Latest protocol smoke output:

- `reports/wrr_1994/wrr_1994_paper.pdf`
- `reports/wrr_1994/WRR1.txt`
- `reports/wrr_1994/WRR2.txt`
- `reports/wrr_1994/SE2a.txt`
- `reports/wrr_1994/SE2b.txt`
- `reports/wrr_1994/SE3.txt`
- `reports/wrr_1994/mc_key.html`
- `reports/wrr_1994/wrr_nations_main_mc.html`
- `reports/wrr_1994/wrr_nations_main_gir.html`
- `reports/wrr_1994/wnp_mc.html`
- `reports/wrr_1994/wnp_en.html`
- `reports/wrr_1994/sources.manifest.json`
- `reports/wrr_1994/koren_genesis_text_source.csv`
- `reports/wrr_1994/koren_genesis_text_source.md`
- `reports/wrr_1994/koren_genesis_text_source.manifest.json`
- `reports/wrr_1994/wrr_source_shapes.csv`
- `reports/wrr_1994/wrr_source_shapes_summary.csv`
- `reports/wrr_1994/wrr_source_shapes.md`
- `reports/wrr_1994/wrr2_terms.csv`

Latest source hashes:

| Label | Bytes | SHA-256 |
| --- | ---: | --- |
| `wrr_1994_paper.pdf` | 1,467,241 | `f7632fce3e1f9aba3c3fdcb62be8ee258c4cad60074d148259c5f0c4e6e97bb3` |
| `WRR1.txt` | 2,016 | `7879343bb78ced3b20db0d232579762ed76bd7bd2b1ec198a2eef9871dde69fb` |
| `WRR2.txt` | 2,038 | `927c133d6d3a57aa06d57518f8a89137292654056b51433a08a0480c7d245be5` |
| `SE2a.txt` | 1,776 | `89ba88172d2d9c127b5f19549b04d8913de3431c4a5879854af2849b7f1d69b2` |
| `SE2b.txt` | 2,463 | `83882e279641a65ce138adea810b4e832c5b971a1cbc97886403d32a6c4bd70d` |
| `SE3.txt` | 1,506 | `79120ebddef32568ded34f5664dcff89f022e835a857296c9bc8a345c2e55073` |
| `mc_key.html` | 596 | `764308981d8bd3f46be4d5080d8af2ad0a74926e2f4467f67852d43fe9221b61` |
| `wrr_nations_main_mc.html` | 120,206 | `a09b855bdce7e5b8c33348af3397f990f148273649ca4374f2bee6fdc733e453` |
| `wrr_nations_main_gir.html` | 123,040 | `99668560235904f741b6b53c234fe2a07716988e7e4b8e6abdb1ce2bc136ecf6` |
| `wnp_mc.html` | 55,318 | `19f5edad5ab6108c08144350f89db78c938f56741b5b3d12036b2ea1450266c2` |
| `wnp_en.html` | 58,461 | `96584d966002eb9f88ebe06cd31ed9802a9437131b726a04e8d384d5be830d99` |

Generated rows use:

- `category=wrr_appellation` for rabbi appellations;
- `category=wrr_date` for date encodings;
- `language=michigan`;
- one shared `concept` per personality record.

## Koren Genesis Text Lock

The WRR smoke path now fingerprints the exact Koren Genesis stream used by
`configs/example_koren_genesis.toml`:

| Item | Value |
| --- | --- |
| config SHA-256 | `21ec51fc542f32d652de517fd66daab24afb3ac35d56441b7777c3885d564a9e` |
| raw `genesis.koren.gz` bytes | 43,596 |
| raw `genesis.koren.gz` SHA-256 | `35e8e9a0752f6b127e7c081a2ca680a63f9851516d65ca102928102783836ea7` |
| decompressed source bytes | 115,803 |
| decompressed source SHA-256 | `3b45732824972890c4a702da5cd01b72a91576917bab1850c2b6f13888e2cdff` |
| normalized Genesis letters | 78,064 |
| parsed Genesis verses | 2,075 |
| normalized text SHA-256 | `b26028e02b921fd18a3f5669fa6db38aa500e516926e9f19ad65a6e32ddc3540` |

This locks the local text stream for audit reproducibility. It does not resolve
the still-open WRR pair-table, corrected-distance, or permutation-method gaps.

## Source Shape Diagnostic

The ANU/McKay famous-rabbis files now have a separate raw shape diagnostic:

| Source | Records | Undated | Appellations | Dates | Raw same-record pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| `WRR1.txt` | 34 | 1 | 166 | 39 | 193 |
| `WRR2.txt` | 32 | 2 | 174 | 31 | 182 |
| `SE2a.txt` | 32 | 3 | 111 | 35 | 117 |
| `SE2b.txt` | 33 | 4 | 157 | 35 | 171 |
| `SE3.txt` | 26 | 0 | 78 | 29 | 84 |

None of the currently downloaded ANU famous-rabbis files exposes 163 raw
same-record appellation/date pairs by simple record combinatorics. The source
discussion pages cite 163 second-list distances, while `WRR2.txt` has 182 raw
same-record combinations before metric eligibility is applied. The 1994 paper's
298 word-pair statement adds another count that has to be reconciled: the
paper-count is a candidate sample size, while the 163 count appears to be a
defined-distance count after the corrected-distance criteria are applied. This
strengthens the current read that the WRR second-list distance table is not
directly recoverable from these plain-text files by count alone.

The WNP critique pages explicitly note that WRR computations were restricted to
appellations totaling 5-8 letters, and separately dispute several Rabbi II-27
Moshe Zacut spellings (`ZKWT)`, `ZKWTW`, `M$H ZKWT)`, `M$H ZKWTW`). In the
current imported table, filtering only appellations shorter than 5 letters
leaves 165 same-record pairs, two above the source-cited 163 distances. Because
Rabbi II-27 has two date rows, excluding one length-eligible Rabbi II-27
appellation would move 165 to 163. Excluding all four WNP-disputed Zacut
appellations would remove eight pairs and overshoot to 157. That is only a
diagnostic clue. The project does not currently apply any Zacut-specific
exclusion because the WNP page is a critical alternative-source discussion, not
a canonical WRR pair table.

## Count Smoke

The imported list can be counted against Koren Genesis with:

```bash
python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume
```

Generated local outputs:

- `reports/wrr_1994/wrr2_genesis_counts.csv`
- `reports/wrr_1994/wrr2_genesis_count_summary.csv`
- `reports/wrr_1994/wrr2_genesis_top_counts.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit_examples.csv`, whose example
  rows include diagnostic WRR 1994 fixed-hit `alpha` values.
- `reports/wrr_1994/wrr2_genesis_count_summary.md`
- `reports/wrr_1994/wrr2_genesis_pair_audit_summary.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit_concepts.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit_examples.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit.md`
- `reports/wrr_1994/wrr2_genesis_pair_controls.csv`
- `reports/wrr_1994/wrr2_genesis_pair_controls.md`
- `reports/wrr_1994/wrr2_genesis_pair_audit_len_5_8_summary.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit_len_5_8_concepts.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit_len_5_8_examples.csv`
- `reports/wrr_1994/wrr2_genesis_pair_audit_len_5_8.md`
- `reports/wrr_1994/wrr2_genesis_pair_controls_len_5_8.csv`
- `reports/wrr_1994/wrr2_genesis_pair_controls_len_5_8.md`
- `reports/wrr_1994/wrr2_skip_caps.csv`
- `reports/wrr_1994/wrr2_skip_caps_summary.csv`
- `reports/wrr_1994/wrr2_skip_caps.md`
- `reports/wrr_1994/wrr2_pair_table_reconciliation.csv`
- `reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv`
- `reports/wrr_1994/wrr2_pair_table_reconciliation.md`
- `reports/wrr_1994/wrr2_pair_eligibility_table.csv`
- `reports/wrr_1994/wrr2_pair_eligibility_summary.csv`
- `reports/wrr_1994/wrr2_pair_eligibility_table.md`
- `reports/wrr_1994/wrr2_perturbation_diagnostics.csv`
- `reports/wrr_1994/wrr2_perturbation_diagnostics_summary.csv`
- `reports/wrr_1994/wrr2_perturbation_diagnostics.md`

This is still only a source/import smoke test. It is not the WRR distance
statistic and should not be cited as a reproduction. Current methodology
blockers are tracked in `docs/WRR_METHODOLOGY_GAPS.md`.

Latest smoke run:

| Item | Count |
| --- | ---: |
| Koren Genesis normalized letters | 78,064 |
| Koren Genesis parsed verses | 2,075 |
| imported rows | 199 |
| counted rows at min length 3 | 196 |
| zero-hit rows | 112 |
| appellation rows | 168 |
| appellation total hits | 13,043 |
| date rows | 31 |
| date total hits | 4,383 |

Top raw rows are short terms such as `$M$`, `W)YR`, and `R)BY`. That is a
useful sanity check for the importer and count engine, not evidence for the WRR
claim.

The current run normalizes the modified Michigan-Claremont source key correctly:
`A` maps to standard Michigan `)` for Alef, and `@` maps to `(` for Ayin.

Same-record pair audit smoke:

| Item | Count |
| --- | ---: |
| pair-audited concepts after min-length filter | 30 |
| appellation/date pair rows | 182 |
| pair rows with close hits within 500 letters | 40 |
| pair rows with strict same-chapter/same-skip close hits | 5 |
| all close pairs within 500 letters | 15,630 |
| overlap pairs | 7,048 |
| strict close pairs | 24 |
| pair-audit step runtime | 1.172s |

The pair audit only checks nearest ELS hit proximity for imported rows. It does
not implement WRR's aggregate distance statistic, rank transform, or permutation
test. Dense short forms dominate the top rows, so this remains an audit
artifact.

Top-pair control smoke:

| Item | Count |
| --- | ---: |
| selected top pair rows | 20 |
| term controls per row | 100 |
| random controls per row | 20 |
| rows not unusual after controls | 18 |
| rows uncorrected-only | 2 |
| rows with adjusted q signal | 0 |
| pair-control step runtime | 14.554s |

The two uncorrected-only rows have adjusted q-values of at least `0.19802`, so
the control smoke does not promote any top raw WRR2 pair row. This is still a
post-audit diagnostic, not WRR's declared statistic.

WRR appendix-compatible length `5..8` pair smoke:

| Item | Count |
| --- | ---: |
| pair-audited concepts after length filter | 22 |
| appellation/date pair rows | 86 |
| pair rows with close hits within 500 letters | 18 |
| pair rows with strict same-chapter/same-skip close hits | 0 |
| all close pairs within 500 letters | 105 |
| overlap pairs | 46 |
| strict close pairs | 0 |
| rows not unusual after controls | 14 |
| rows uncorrected-only after controls | 4 |
| rows with adjusted q signal | 0 |
| length-filtered audit runtime | 0.713s |
| length-filtered control runtime | 1.261s |

This length-filtered pass is closer to the WRR appendix rule that retained
words of length 5 through 8 for corrected-distance calculation. It still uses
the repo's nearest-hit pair audit and control screen, not WRR's corrected
distance `c(w,w')`, aggregate `P1..P4`, or permutation-rank procedure.

WRR expected-count skip-cap audit for length `5..8` rows:

| Item | Count |
| --- | ---: |
| length-filtered rows | 120 |
| unique normalized terms | 109 |
| rows with estimated `D(w) <= 250` | 16 |
| rows with `D(w) <= 500` but `> 250` | 7 |
| rows with `D(w) <= 1000` but `> 500` | 17 |
| rows with `D(w) > 1000` | 80 |
| rows not reaching expected 10 by word-max skip | 55 |
| rows with zero observed hits at max skip 250 | 56 |
| skip-cap audit runtime | 0.693s |

This matters because the pair/control smoke above uses `max_skip=250`, while
the WRR appendix describes term-specific `D(w)` caps based on expected ELS
counts. A full corrected-distance implementation needs per-term caps rather
than the broad-search cap.

WRR pair-table reconciliation:

| Item | Count |
| --- | ---: |
| source records parsed from `WRR2.txt` | 32 |
| undated source records skipped by importer | 2 |
| source appellations | 174 |
| source dates | 31 |
| source same-record pairs | 182 |
| imported same-record pairs | 182 |
| appellation length >= 5 same-record pairs | 165 |
| WNP-disputed Zacut appellation rows | 4 |
| pair delta if all WNP-disputed Zacut rows are excluded | 8 |
| pairs after all WNP-disputed Zacut rows are excluded | 157 |
| pairs after one Zacut appellation exclusion | 163 |
| gap after one Zacut appellation exclusion | 0 |
| length-filtered same-record pairs | 86 |
| source-cited second-list distances | 163 |
| imported-pair gap to cited distance count | -19 |
| appellation-length gap to cited distance count | -2 |
| length-filtered gap to cited distance count | 77 |

This is the current concrete mismatch: the secondary `WRR2.txt` source imports
to 182 same-record appellation/date combinations, while WRR discussion sources
cite 163 second-list distances. Filtering out only appellations shorter than 5
letters yields 165 combinations, only two above the cited count, while the
repo's current 5..8-letter audit filter reduces those rows to 86. Neither
count is the locked WRR second-list distance table. The Zacut diagnostic now
shows why a single length-eligible Zacut appellation exclusion would close the
numeric gap, while excluding every WNP-disputed Zacut row would not.

WRR pair-eligibility lock-prep table:

| Item | Count |
| --- | ---: |
| imported same-record pair rows | 182 |
| concepts | 30 |
| appellation length >= 5 pair rows | 165 |
| length 5..8 smoke-lane pair rows | 86 |
| WNP Zacut diagnostic pair rows | 8 |
| zero-hit pair rows at smoke cap | 129 |
| pair rows with at least one skip-cap target unreached term | 155 |
| pair rows with close hits within 500 letters | 40 |
| pair rows with strict same-chapter/same-skip close hits | 5 |
| status | `lock_prep_only_not_canonical` |

This table gives the next reviewer a row-by-row pair id, source term ids,
normalized lengths, Genesis smoke hit counts, expected-count skip caps,
nearest-pair metrics, and eligibility notes. It still does not select the
canonical 163-distance WRR pair set.

WRR perturbation boundary diagnostic for length `5..8` rows:

| Item | Count |
| --- | ---: |
| length-filtered rows | 120 |
| unique normalized terms | 109 |
| perturbation triples | 125 |
| rows with sampled hits | 64 |
| rows without sampled hits | 56 |
| sampled hits | 447 |
| rows with sample under 10 valid perturbations | 0 |
| minimum in-bound perturbations in sample | 125 |
| ordinary in-bound failures | 0 |
| perturbation diagnostic runtime | 3.977s |

This only checks whether sampled ordinary ELS rows have enough in-bound
last-three-gap perturbations to avoid the source-described boundary blocker.
It does not compute proximity `Q(w,w')`, corrected distance `c(w,w')`, or a
permutation statistic.

## Statistic Helpers

`els/wrr.py` now implements the WRR-independent arithmetic around the missing
corrected distance:

- the appendix skip-window count `(D - 1)(2L - (k - 1)(D + 2))`;
- expected ELS count and integral skip-cap selection for a target expected hit
  count;
- `P1` as the binomial upper tail for `c(w,w') <= 0.2`;
- `P2` as the product-of-uniforms transform;
- permutation-rank `rho` with half-weighted ties;
- Bonferroni `rho0 = 4 min(rho_i)`.
- WRR perturbation triples, perturbed offsets, first-ten row widths,
  conservative supplied-row domain labeling for unambiguous shorter-skip cases,
  domain-weighted `Q(w,w')` summation for domain-labeled ELS rows, and the
  corrected-distance rank step for already-computed perturbation proximities,
  including the strict WRR 1994 `v/m` rank and the tie-aware methodology-page
  diagnostic rank.

These helpers are tested, but they still need real `c(w,w')` values from a
future corrected-distance implementation before they can produce WRR `P1..P4`.
Source-backed implementation notes for that missing corrected-distance layer
are tracked in `docs/WRR_CORRECTED_DISTANCE_NOTES.md`.

By default, records with no date rows are skipped because they cannot form a
rabbi/date pair. Use `--include-undated` only for source auditing.

## Not Yet Claim-Ready

Do not move WRR from `under_specified` until:

- the imported plain-text list is cross-checked against the primary paper table
  or another citable transcription;
- the WRR distance metric is implemented and tested against toy fixtures;
- the permutation procedure is implemented with saved seeds and manifests;
- the output report labels disagreements with the published result.
