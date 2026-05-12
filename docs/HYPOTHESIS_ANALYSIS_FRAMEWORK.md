# ELS Hypothesis Analysis Framework

## Hypothesis

The working hypothesis is that the original-language biblical text is
providentially meaningful at the letter level. If that hypothesis is true, ELS
patterns may be one mechanism by which intentional structure becomes detectable
once we have enough compute to search exhaustively.

This project does not treat English translation results as the core test of
that hypothesis. English KJV and other English versions can be searched and may
produce interesting patterns, but English absence does not invalidate an
original Hebrew/Greek claim.

## Evidence Order

1. Hebrew and Greek Bible corpora are primary.
2. Text-family and version distribution matters. A pattern can be meaningful if
   it appears in one textual source and not another; the result should be
   recorded by source rather than flattened into present/absent.
3. English Bible corpora are secondary translation screens.
4. Non-Bible Hebrew, Greek, and English controls are required background checks.

## Hit Collection Rule

The collection rule is broad: gather hidden-path hits first, then annotate them.
Surface context is not a gate.

Each hit should be classified into strata:

- `hidden_path_only`: hidden ELS path found, with no required surface echo.
- `center_word_exact`: hidden term is centered on the same normalized surface
  word.
- `center_word_same_concept`: hidden term is centered on a related concept.
- `center_word_same_category`: hidden term is centered on a broader related
  category.
- `center_verse_*`: center verse discusses the same or related term.
- `span_*`: the text between the ELS start and end discusses the same or
  related term.
- `same_skip_extension`: adjacent letters at the same interval create a longer
  word or phrase before/after the base term.

The rare case where hidden and surface text match exactly is important, but it
is not the only important case. Hidden-path-only rows remain part of the
dataset.

Final reports should list centered-self and relevant-center occurrences because
they happen, then attach frequency/control reads as interpretation context.
Counts can warn that a pattern is common, but they should not delete a real
occurrence from the review list.

## Extended Match Strata

The existing strata stay in place. The following strata widen what the toolkit
can record, but none should enter routine claim language without a predeclared
rule, a matched control family, and a registered review gate.

### Tier 1: External-Claim Audit Strata

These strata answer claim families already cataloged in external-source audits
such as Bible Code Digest, Bible-codes.org, Cosmic Codes, Isaiah 53 claims, and
WRR-style geometry.

- `matrix_cluster_at_width_W`: two or more declared cohort terms hit within one
  matrix cell or its 8-neighborhood at wrap width `W`.
- `matrix_orthogonal`: hidden terms intersect on the same matrix row or column.
- `matrix_diagonal`: hidden terms intersect on the same matrix diagonal.
- `matrix_adjacent_row`: hidden terms fall within a declared row-distance.
- `atbash_path`: hidden term found after deterministic Hebrew atbash
  substitution.
- `atbash_centered_self`: atbash-substituted hidden term centers on its
  pre-substitution surface word, or the reverse.
- `albam_path`: hidden term found after deterministic albam substitution.
- `cipher_layered_pair`: term found in plain text while its cipher form appears
  as a hidden path at the same anchor.
- `cross_skip_pair_at_word`: two terms at different skips share the same center
  word.
- `cross_skip_pair_at_letter`: two terms at different skips share a letter
  position.
- `cross_skip_pair_within_N_letters`: two terms at different skips have
  endpoints within a declared letter distance.
- `boundary_start_verse`, `boundary_start_chapter`, `boundary_start_book`:
  hidden path starts at the beginning of a verse, chapter, or book.
- `boundary_end_verse`, `boundary_end_chapter`, `boundary_end_book`: hidden path
  ends at the end of a verse, chapter, or book.
- `boundary_both_endpoints`: both endpoints land on the same declared boundary
  class.

Matrix strata require the exact row-width or cylinder rule to be locked before
the run. Cipher strata require the same substitution pass on Bible and control
corpora. Boundary strata require controls with comparable structural breaks:
verse/chapter/book for Bible texts and paragraph/section/book breaks for
non-Bible corpora.

Implementation note: Hebrew atbash is available as an opt-in deterministic
corpus transform in `els/transforms.py`. It is not part of routine searches
unless a protocol explicitly declares the transform and its matched controls.

### Tier 2: Interpretive Anchoring Strata

- `canonical_first_occurrence`: first hidden occurrence of the term in
  canonical order within the declared search family.
- `canonical_first_in_thematic_chapter`: first occurrence lands in a
  predeclared thematically loaded chapter for the term.
- `author_in_own_book`: hidden author name centers in a book traditionally
  attributed to that author.
- `protagonist_in_own_narrative`: hidden protagonist name centers in the
  declared narrative arc for that protagonist.
- `nt_quotation_anchor`: hidden term centers on an OT word modified, expanded,
  or reused in a declared NT quotation.
- `nt_quotation_span`: hidden term span overlaps the OT verse(s) cited by the
  NT.
- `forward_only`: term appears forward in the declared corpus/search family but
  not backward.
- `backward_only`: term appears backward but not forward.
- `bidirectional_present`: term appears in both directions.
- `direction_imbalance_score`: continuous forward/backward ratio for downstream
  filtering.

Thematic chapters, author books, protagonist ranges, and OT-in-NT quotation
anchors must be declared in data files before any density or promotion report is
computed.

### Tier 3: Methodological Strata

- `low_bigram_surprise`: hidden term uses only common host-language bigrams.
- `high_bigram_surprise`: hidden term contains at least one rare host-language
  bigram under a locked threshold.
- `skip_equals_meaningful_constant`: skip matches a locked constant such as 7,
  12, 22, 26, 40, 50, 70, 144, or 666.
- `skip_equals_term_gematria`: skip equals the hidden term's gematria under a
  declared scheme.
- `skip_equals_center_word_gematria`: skip equals the center surface word's
  gematria under a declared scheme.
- `cohort_cluster_density_window_N`: distinct hidden terms from a declared
  cohort center inside a sliding window of `N` words.
- `cohort_full_house`: every term in a declared cohort has at least one centered
  hit inside the window.

### Tier 4: Declared Future Variants

- `word_skip_ELS`: every `K`th word rather than every `K`th letter.
- `acrostic_pattern`: term formed from the first letter of consecutive surface
  words.
- `telestic_pattern`: term formed from the last letter of consecutive surface
  words.
- `lxx_vs_mt_semantic_divergence`: ELS locus tracks either MT consonants or LXX
  semantics where the two diverge.
- `root_only_match`: hidden Hebrew root accepted as a centered match for a
  surface inflection of that root.
- `term_absence_at_thematic_chapter`: relevant term absent at all declared skips
  in a chapter where it would be expected.
- `chapter_position_bias`: hidden patterns concentrate in chapter-initial or
  chapter-final verses more than controls.
- `letter_frequency_anomaly`: hidden term uses individually rare host-language
  letters.

## Extended-Strata Implementation Order

1. `boundary_*`: offset-based annotation on existing hit rows.
2. `forward_only`, `backward_only`, and `bidirectional_present`: metadata over
   existing hits.
3. `canonical_first_occurrence`: post-processing pass over indexed hits.
4. `author_in_own_book`: add an author-to-book mapping and reuse centered
   strata.
5. `cross_skip_pair_at_word`: promote pair compactness into typed hit metadata.
6. `matrix_cluster_at_width_W`: implement locked geometry for visual claims.
7. `atbash_path`: add deterministic transform layer with matched controls.
8. `nt_quotation_anchor`: add OT-in-NT quotation anchor data.
9. Bigram, meaningful-constant, gematria, and cohort-density strata as separate
   preregistered studies.

## Extended-Strata Data Dependencies

- `terms/thematic_chapters.csv`
- `terms/author_book_mapping.csv`
- `terms/protagonist_narrative_mapping.csv`
- `data/study/ot_in_nt_quotations.csv`
- `data/study/bigram_frequencies/{language}_{corpus}.csv`
- `terms/meaningful_constants.csv`
- `terms/gematria_schemes.toml`
- `terms/cohorts/`

Each file must be locked before the corresponding stratum is used for promotion
or claim-level language.

## Full-Span Rule

Full-span searches are valid search targets. We cannot decide that a full-span
run is uninteresting before searching it.

The practical distinction is storage:

- Bounded skip ranges can retain full hit metadata as CSV.
- Full-span count runs can be searched quickly with the compiled pair-index
  counter.
- Full-span all-hit exports may be enormous for short terms. Those should be
  stored as partitioned or compressed hit files, with full metadata materialized
  first for rare and medium-density terms.

## Control Requirement

Every Bible search family should have a matching non-Bible control family:

- Hebrew Bible texts vs large Hebrew non-Bible texts.
- Greek Bible texts vs large Greek non-Bible texts.
- English Bible texts vs large English non-Bible texts.

Compare using:

- raw hit counts,
- legal search-space size,
- hits per million legal positions,
- expected hits under corpus-specific letter frequencies,
- Bible/control rate ratios,
- empirical rank against shuffled-letter, shuffled-term, and real-word controls,
- source/version distribution,
- context-stratum enrichment.

## Interpretation Boundary

Support for the hypothesis would look like a predeclared pattern family that is
more concentrated in primary Hebrew/Greek Bible corpora than in language-matched
controls, survives correction for search-space size and multiple testing, and
has meaningful source/context distribution.

Failure in KJV or another translation does not decide the original-language
hypothesis. Strong non-Bible background rates do not automatically disprove it,
but they raise the bar for any claim.

## Skeptical-Source Response

The CRI critique audit in `docs/CRI_ELS_CRITIQUE_AUDIT.md` is treated as a
methodological challenge this project must answer. In practice that means:

- no after-the-fact movement from hit discovery to claim language;
- no unbounded spelling variants without a declared spelling audit;
- no matrix or cluster claim without a declared metric;
- no prediction claim without archived source timing;
- no claim-level language without language-matched controls and correction for
  the full tested search space.
