# Bible Code Digest Source Audit

Source family: [Bible Code Digest](https://biblecodedigest.com/).

Status: source review and screening-list expansion. This is not a reproduction
claim.

## Purpose

Bible Code Digest is useful for this project because it gives public examples
of the kinds of ELS claims readers may ask about: named terms, passage-centered
clusters, same-skip extensions, matrix-style layouts, and surface-text
relationships. The source is not directly reusable as data. Exact spellings,
skip limits, row widths, and selection rules still need claim-by-claim
pre-registration before any reproduction status can move above
`under_specified`.

## Reviewed Pages

- [home page index](https://biblecodedigest.com/)
- [Yeshua Messiah extensions](https://biblecodedigest.com/page.php/620)
- [extensions methodology](https://biblecodedigest.com/page_PageID_474.html)
- [Who is like God overview](https://biblecodedigest.com/page.php/352)
- [King David underscoring](https://biblecodedigest.com/page.php/420)
- [major clusters index](https://biblecodedigest.com/page.php/199)
- [research guidelines](https://biblecodedigest.com/page.php/273)

Search-result snippets and the site index also point to BCD pages on Isaiah 53,
Psalm 22, Ezekiel 40, Shimon Peres, Obama, terrorism, earthquakes, economic
crisis, climate, and other topic clusters. Those are treated as source leads,
not locked claim specifications.

## Methodology Items To Track

The following BCD method shapes map to capabilities we already have or should
keep explicit:

- same-skip before and after extensions;
- compound extensions where adjacent letters form a longer hidden word or
  phrase;
- low-skip matrix review;
- passage-centered clusters such as Isaiah 53, Psalm 22, Ezekiel 38-40, and
  Proverbs 30:4;
- surface-text relationship checks, especially centered word, same verse, same
  passage, and start-to-end span relevance;
- underscoring or repeated-line visual effects;
- comparison against randomized or non-Bible controls;
- claim-by-claim spelling audits because many source examples are rendered as
  images or transliterated summaries.

Existing project coverage:

- `docs/ELS_EXTENSIONS.md` covers same-skip extensions.
- `docs/MATRIX_TABLES.md` covers matrix export.
- `docs/CENTERED_OCCURRENCE_INDEX.md` covers occurrence-first centered and
  relevant-surface rows.
- `docs/ELS_CONTROLS.md` and follow-up control reports cover null comparisons.

## Added Screening Terms

The BCD-specific term list is:

- `terms/bible_code_digest_claim_terms.csv`

The list is Hebrew-only for now because the BCD claim family mostly concerns
Hebrew Bible/Tanakh searches. Rows are intentionally source-tagged with `bcd_`
IDs. Some rows are provisional Hebrew renderings where the BCD page names an
English topic but does not provide machine-readable Hebrew in the reviewed page.

Term groups added:

- Yeshua/Messiah and Isaiah 53/Psalm 22 phrase themes;
- "Who is like God" and Proverbs 30:4 question-style themes;
- King David and David-context terms;
- Ezekiel 38-40 war/Gog-Magog/Temple themes;
- Shimon Peres and Israeli politics terms;
- Obama and 2008 U.S. election terms;
- terrorism and 9/11-adjacent terms;
- Gaza and Hamas terms;
- global economic crisis terms;
- disaster and climate terms;
- religion-comparison terms such as Buddha, Muhammad, Moses, and Aaron.

## Claim Catalog Additions

The claim catalog records BCD families as `under_specified`, not reproduced:

- Yeshua/Messiah extensions;
- Isaiah 53 and Psalm 22 Yeshua clusters;
- King David underscoring;
- Ezekiel 38-40 war/Temple cluster;
- "Who is like God" question-style searches;
- Shimon Peres politics claims;
- Obama/election/political cluster claims;
- disaster, terrorism, and economic-crisis topical clusters.

## Reproduction Requirements

Before any BCD row can move out of `under_specified`, lock:

1. exact source page and archived page copy;
2. exact Hebrew spelling or phrase form;
3. source corpus and normalization rules;
4. skip range and direction;
5. row width or matrix construction rule when relevant;
6. cluster/proximity metric;
7. extension length and allowed before/after/compound forms;
8. control family and multiple-testing correction.

## Cautions

- BCD pages often present results visually. A screenshot or page title is not
  enough to reconstruct the exact search.
- English topic labels are not necessarily Hebrew spellings.
- Similar-looking matrix clusters can arise from broad term choice, short terms,
  many row widths, and post-selection.
- This audit adds declared screening inputs and claim leads only. It does not
  validate any BCD result.
