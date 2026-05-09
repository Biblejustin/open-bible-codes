# TheWordNotes ELS Source Audit

Source: [Equidistant Letter Sequences [ELS]](https://www.thewordnotes.com/els.pdf),
TheWordNotes.com.

Status: public source audit and screening-list expansion. This is not a
reproduction report.

## Why This Source Matters

This PDF is a compact positive ELS source built mainly from Grant Jeffrey and
Yacov Rambsel material. It is useful because it gives several claim families
with more detail than ordinary web summaries:

- source-sensitivity claim: ELS works only with the Masoretic Hebrew Text and
  Greek Received Text underlying the KJV;
- common Torah/YHWH book-opening examples;
- Israel, Eden, tree-name, Judah-to-David, Hanukkah/Hasmonean, Zedekiah/Matanya,
  Sadat, Hitler/Auschwitz, French Revolution, rabbis-and-dates, and Aaron
  clusters;
- Rambsel Yeshua/Messiah examples in Genesis, Isaiah 53, Zechariah, Leviticus,
  Psalm 41, Ruth, Isaiah 61, and Daniel 9;
- an Isaiah 52-54 table listing Yeshua, Messiah, disciples, Mary, cross,
  Passover, Galilee, Caiaphas, Annas, bread, wine, water, servant, seed, and
  atonement-lamb terms;
- an explicit warning against using ELS for future prediction;
- an explicit note that three table entries had transcription issues in the
  author's own validation attempt.

## Added Screening Terms

The companion term list is:

- `terms/thewordnotes_els_claim_terms.csv`

The list preserves terms and phrases named by the PDF. It is intentionally
source-tagged with `twn_` IDs. Some Hebrew renderings are provisional where the
PDF gives English descriptions or visibly corrupted Hebrew extraction.

## Claim Families To Track

The claim catalog records these source families as `under_specified`, not
reproduced:

- TheWordNotes / Grant Jeffrey historical clusters;
- TheWordNotes / Rambsel Yeshua examples;
- TheWordNotes Isaiah 52-54 Rambsel table;
- TheWordNotes source-version claim.

The common Torah skip examples already have an engine sanity-check path in
`docs/COMMON_EDLS_TEST.md`, but this PDF still belongs in the source trail
because it repeats the popular presentation and adds related examples.

## Reproduction Requirements

Before elevating any row:

1. lock the exact source text edition, including whether this means Koren,
   Michigan-Claremont, OSHB WLC, another Masoretic stream, or a specific TR
   Greek source;
2. transcribe the exact Hebrew/Greek target string from the source;
3. lock book, chapter, verse, start word, start letter, skip, and direction;
4. verify the letter path against a source with reproducible normalization;
5. distinguish exact ELS claims from broad cluster claims;
6. run same-length real-word and shuffled controls;
7. record source/version distribution;
8. preserve any transcription mismatch as an audit finding rather than fixing it
   silently.

## Methodology Notes

This source reinforces several existing project rules:

- source/version distribution matters;
- hidden-path-only rows can be collected but need controls before claim language;
- passage relevance is meaningful metadata but not a substitute for a declared
  statistic;
- exact letter-path audit is mandatory when a source gives word/letter/skip
  details;
- future-event prediction is out of scope for claim promotion.

## Cautions

- The PDF is a secondary compilation, not a primary machine-readable dataset.
- Several Hebrew strings are hard to extract cleanly from the PDF.
- Some cited claims are broad clusters without full geometry.
- The source itself notes transcription problems in three Rambsel-table rows.
- These additions expand the audit surface; they do not validate the claims.
