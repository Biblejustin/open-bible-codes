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
