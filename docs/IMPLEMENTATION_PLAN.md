# Implementation Plan

## Goals

- Open-license ELS research toolkit.
- Hebrew and Greek parity across MT/WLC, LXX, TR NT, and critical Greek NT corpora.
- Reproducible inputs, settings, manifests, outputs, and report indexes.
- No copied code from disputed or unclear projects.
- No bundled copyrighted Bible texts.
- Forward and backward ELS search with signed skips.
- Hit-level audit data: start ref, end ref, center ref, center word, offsets, direction, skip, and source.
- Surface-context checks: center verse, hit span, same concept, same category, and nearby related terms.
- Same-skip extension checks: words or short phrases before/after an ELS hit.
- Fixed theological, historical, modern-name, date, Table-of-Nations, and claim-specific term lists.
- Gematria and year/date encodings for Hebrew and Greek where method is declared up front.
- Related-name studies: intertwined hits, nearby hits, same-passage hits, same-chapter hits, and overlapping spans.
- Textual-tradition comparison: MT vs LXX where possible, TR vs critical NT, and omitted-verse breakage.
- Post-baseline apocrypha/deuterocanon comparison: add declared apocrypha witnesses only after the current report set is frozen, then rerun the same ELS, centered-occurrence, surface-context, extension, version-presence, and control checks as a separate source family.
- Apocrypha bridge-completion study: find partial canonical-text ELS paths that become complete only when apocrypha/deuterocanon material is inserted into the declared full text stream.
- Content-word counting by total, book, chapter, and verse with multiple checks for 3, 7, 12, 40, 49, 50, and 70.
- Check whether omitted/variant readings break word-count multiples or ELS patterns.
- Reproduce well-known public ELS claims from scratch where inputs and rules can be stated without copying disputed code or data.
- Maintain a claim catalog: source, claimed text, terms, spellings, skips, layout, metric, corpus, and reproduction status.
- Matrix/table analysis: row-width layouts, wrapped tables, term intersections, and visual/exportable coordinates.
- Compactness scoring for term pairs, clusters, and surface-context relationships.
- Spelling/appellation audit: alternate spellings, titles, transliterations, Hebrew/Greek variants, and selection sensitivity.
- Text sensitivity audit: variants, book boundaries, spaces, final forms, accents, breathings, and normalization choices.
- Control corpora and null models: shuffled letters, shuffled verses, comparable non-Biblical texts, and randomized term lists.
- Declared null-control and frequency-anchor term lists for count calibration.
- Multiple-testing correction and pre-registered protocol support to reduce cherry-picking.
- Long-phrase and famous-media-claim testing with transparent positive and negative results.
- Skip motif studies for 7, 49, 50, 70, and other declared symbolic distances.
- Claim grading: reproducible, partially reproducible, not reproducible, under-specified, or license-blocked.
- Publish negative results alongside positive results.

## Phase 1: Core Search

- Normalize Hebrew and Greek.
- Build a continuous letter stream from configured texts.
- Search terms by signed skip.
- Export exact offsets, refs, source names, and normalized sequences.

Status: initial version built; broad Hebrew and focused Greek NT claim-term lists compiled; same-skip extension scanner built; conservative claim catalog started; matrix coordinate export added.

## Phase 2: Corpus Import

- Keep generic CSV/text import.
- Add import helpers only for clearly licensed sources.
- Track source name, license, URL, edition, and checksum.
- Keep raw texts ignored by git unless source license permits redistribution.

Status: generic CSV/text import built.

## Phase 3: Statistics

- Fixed protocol file: terms, skip bounds, text, normalization, null model.
- Letter-shuffle control.
- Verse-shuffle control.
- Comparable control text support.
- JSON summary for observed vs null counts.

Status: letter-shuffle and term-shuffle controls built; public baseline protocol,
report index, shared p-value helpers, Benjamini-Hochberg q-values, and
search-space calibration helpers added.

## Phase 4: WRR-Style Tools

- Minimal ELS detection by term.
- Dynamic skip cap by expected hit count.
- 2D cylindrical row layout.
- ELS-to-ELS and ELS-to-surface-letter distance.
- Pair permutation tests.

Status: partially built. Minimal ELS detection, pair-distance queues, explicit
pair compactness fields, matrix coordinate export, and expected-hit skip
planning exist. Cylindrical pair distance is available as a WRR-style building
block. Shared empirical tail-probability helpers are in place. WRR-specific
replication requirements are tracked in `docs/WRR_REPLICATION_PLAN.md`;
aggregate statistics and permutation tests remain planned.

## Phase 5: Validation

- Unit tests for normalization and skip math.
- Golden toy fixtures.
- Compare against public papers/examples by re-entering formulas, not copying code.
- Performance tests on whole Bible corpora.

Status: unit tests, schema tests, protocol-resume tests, performance benchmark
script, and generated-report smoke paths are in place.

## Release Rules

- MIT code license.
- Source-text licenses documented separately.
- No generated report claims significance unless protocol was fixed before running.
