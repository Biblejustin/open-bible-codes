# Amandasaurus Biblecode Prior-Art Audit

Source: [amandasaurus/biblecode](https://github.com/amandasaurus/biblecode),
GitHub repository. Checked May 9, 2026.

Repository snapshot reviewed:

- owner/repo: `amandasaurus/biblecode`
- default branch: `master`
- latest reviewed commit: `8d70d55a8a2bb8f556755d9ab20b86d96c0ce979`
- primary language: Rust
- stated purpose: find equidistant letter sequences in texts
- license note: GitHub detects `AGPL-3.0` from `LICENCE`; `Cargo.toml` says
  `AGPL-1.0` and points at `https://github.com/rory/biblecode`.

Status: public implementation/prior-art audit. This is not a reproduction
report, and no code from this repository is imported or derived.

## Why This Source Matters

This source is useful as a small, concrete implementation reference for
popular-style ELS searching:

- it explicitly frames the tool around Michael Drosnin's `The Bible Code`;
- it suggests Project Gutenberg KJV as sample plaintext input;
- it normalizes by keeping alphabetic characters and lowercasing;
- it indexes character positions before searching;
- it derives signed skip values from first-letter and second-letter positions;
- it suppresses ordinary adjacent text by skipping step `1`;
- it searches arbitrary plain-text files rather than only biblical corpora;
- it prints matrix-like local context around the hidden-letter path;
- it caps displayed hits with an example `take(10)` style loop;
- it can accept a second search string after the first match, but does not
  implement a proximity/statistical relationship between the two terms.

## Project Relevance

The implementation reinforces several project choices already made here:

- English/KJV plaintext controls should be treated as first-class comparison
  streams, not only Hebrew and Greek;
- normalization rules must be declared because they change the letter stream;
- signed skips and backward paths need to be tracked explicitly;
- visual matrix/context output is useful for review, but it is not a statistic;
- "find first few examples" tools are not enough for claim evaluation;
- term-pair searches require a declared proximity rule, not just two independent
  ELS searches;
- license compatibility must be checked before any code reuse.

## Methodology Notes

The reviewed code's algorithm differs from this project's current search
engine. It enumerates candidate skips from positions of the first two letters
of the requested term, then checks the rest of the sequence. This is simple
and useful for a small command-line finder, but it is not the lane/Aho-Corasick
batch approach used here for large term lists and full-corpus reporting.

The local-context output is still a useful report-design cue. For any promoted
row, this project should keep both forms:

1. machine-readable coordinates, verses, center word, surface context, and
   control statistics;
2. human-readable matrix or letter-path display for review.

## License And Reuse Notes

Do not copy code from this repository into this MIT-licensed project. Treat it
only as public prior-art context unless a compatible license grant is obtained.

The license metadata is internally inconsistent between the repository's
detected license and `Cargo.toml`. That strengthens the reason to avoid code
reuse and keep this as a methodology audit only.

## Claim-Catalog Handling

The claim catalog records this as an `under_specified` methodology-source row,
not as a positive Bible-code claim. It contributes implementation and reporting
ideas, not claim evidence.

## Cautions

- This is a small educational implementation, not a statistical study.
- KJV/Gutenberg sample input is useful for comparison, but it does not test the
  Hebrew/Greek letter-by-letter inspiration hypothesis directly.
- The example code does not define row-width scoring, multiple-comparison
  correction, matched controls, or version-distribution handling.
- The second-term feature is independent follow-up search, not an intertwined
  or passage-centered pair metric.
