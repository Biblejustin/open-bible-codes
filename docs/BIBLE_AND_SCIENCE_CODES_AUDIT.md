# Bible and Science Codes Source Audit

Source: [Bible Codes](http://bibleandscience.com/bible/codes.htm), Institute
for Biblical & Scientific Studies / Bible and Science.

Status: public critique and methodology audit. This is not a reproduction
report.

## Why This Source Matters

This page is useful because it gathers several objections and alternative
code-types in one compact source:

- ELS examples are presented historically through Weissmandel, WRR/Rips, Drosnin,
  and Grant Jeffrey;
- the page argues that large non-Bible books can also produce apparent ELS
  results, citing the Koran and `Moby Dick`;
- it flags provocative negative phrases such as "there is no God" and "God is
  dead" as a warning against over-interpreting raw ELS hits;
- it emphasizes manuscript-level instability by naming the Aleppo Codex,
  Leningrad Codex, Cairo Pentateuch, Damascus Pentateuch, Dead Sea Scrolls, and
  4Q Samuel;
- it distinguishes ELS from legitimate non-ELS biblical structures, including
  alphabetic acrostics, Esther acrostics, Atbash-style cryptograms, and gematria.

## Added Screening Terms

The companion term list is:

- `terms/bible_and_science_codes_terms.csv`

The rows use `bns_` IDs. This is a stress/control list, not a positive claim
list. It intentionally includes source-variation labels, non-Bible controls,
and non-ELS code terms.

## Claim Families To Track

The claim catalog records these source families as `under_specified`, not
reproduced:

- Bible and Science ELS critique/control examples;
- Bible and Science textual-variation guardrails;
- Bible and Science legitimate non-ELS code examples.

## Methodology Notes

This source reinforces several project rules:

- raw ELS hits are expected in sufficiently long texts;
- negative and nonsensical phrases should be tracked as controls;
- source/version distribution is not optional for letter-level claims;
- ELS, acrostic, cryptogram, and gematria methods need separate pipelines;
- a method that can "prove" contradictory phrases needs controls before
  interpretive language.

## Reproduction Requirements

Before elevating any Bible-and-Science-related row:

1. lock the exact claim source and text edition;
2. separate ELS claims from acrostic, Atbash, and gematria claims;
3. define source/version comparison rules for letter-level variation;
4. include non-Bible text controls and negative-phrase controls;
5. preserve digit-only gematria as word-count/gematria metadata, not ELS text
   rows;
6. correct for all declared examples in the critique family.

## Cautions

- The source is a critique page, not a primary data file.
- Several examples are English summaries of Hebrew phenomena.
- The page links to outside critiques and articles that should be audited
  independently before being treated as claim sources.
- These additions expand the control and audit surface; they do not validate or
  invalidate any ELS claim by themselves.
