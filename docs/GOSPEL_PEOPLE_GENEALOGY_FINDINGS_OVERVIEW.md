# Gospel People And Genealogy Findings Overview

Status: reader summary. This page explains the current Gospel people and
genealogy results in ordinary terms. It does not replace the locked reports.

Source reports:

- `docs/GOSPEL_PEOPLE_GENEALOGY_PROSPECTIVE_REPORT.md`
- `docs/CRITICAL_OMISSION_BREAKS_GOSPEL_PEOPLE_GENEALOGY.md`
- `docs/GOSPEL_PEOPLE_GENEALOGY_PROSPECTIVE_PREREGISTRATION.md`

## Bottom Line

We tested names connected to the Gospels: people in the genealogy of Christ,
disciples, Gospel women, and other named Gospel figures.

The main result is cautious:

- the searches found many hidden-letter paths;
- most paths are best treated as ordinary search results, not special findings;
- no row passed the adjusted control test;
- seven rows were interesting before adjustment, but not after it;
- the TR/SBLGNT omission check found 50 hidden-letter paths that depend on
  verses present in the TR but absent from SBLGNT.

So the useful finding is not "we found a settled code." The useful finding is
that the locked test ran cleanly, the results were measured, and the controls
kept the interpretation conservative.

## Terms Used Here

ELS means equidistant letter sequence. In simple terms, it means reading every
same-numbered letter. If the skip is `5`, the search reads every fifth letter.
If the skip is `-5`, it reads backward every fifth letter.

TR means Textus Receptus. It is the Greek New Testament tradition used behind
the King James Version New Testament.

SBLGNT means SBL Greek New Testament. It is a modern critical Greek New
Testament.

Control means comparison test. Here, controls ask whether similar terms or
random terms produce similar results. Controls help separate an interesting row
from something that happens often in this kind of search.

Adjusted control test means the control result was corrected for many tests
being run at once. That matters because a big search can produce a few
interesting-looking rows just by volume.

## What Was Tested

The study used a locked list of Gospel-related names before looking at the
results. This matters because changing the list after seeing results can make a
search look stronger than it really is.

The locked list included:

- names from the Matthew and Luke genealogies;
- disciples and apostle-associated names;
- named Gospel women;
- other named people in the Gospels;
- Greek forms and selected Hebrew forms.

The main search used skip `2..100`, forward and backward. Short forms below
four normalized letters did not enter the main controlled endpoint.

## Main Search Results

The main Gospel people/genealogy report had 114 result rows.

| Item | Count |
| --- | ---: |
| Rows reviewed | 114 |
| Rows with representative controls | 81 |
| Rows not unusual under controls | 74 |
| Rows interesting before adjustment only | 7 |
| Rows with adjusted control support | 0 |

In ordinary terms: the search found many paths, but the control tests did not
support raising any row above review status.

The seven unadjusted rows can still be read as review prompts. They should not
be treated as strong results.

## Text-Omission Check

A second check asked a different question.

Some verses appear in the TR but are absent from SBLGNT. The check asked:

If those TR-only verse blocks are removed, which Gospel-name hidden-letter
paths break?

This does not measure whether the path is unusual. It measures whether a path
depends on those disputed or omitted TR verse blocks.

| Item | Count |
| --- | ---: |
| Greek term rows loaded | 98 |
| Minimum normalized length | 4 |
| TR hidden-letter hits searched | 11,860 |
| Hits crossing omitted verse blocks | 50 |
| Broken hits | 50 |
| Broken because a used letter was removed | 50 |
| Broken by spacing only | 0 |
| Terms with at least one break | 16 |

In ordinary terms: all 50 broken paths used at least one letter inside an
omitted TR verse block.

## Largest Omission-Break Rows

The biggest break counts came from short or common forms.

| Term ID | Name | Normalized Form | Broken Hits |
| --- | --- | --- | ---: |
| `gpg_anna_g` | Anna | `αννα` | 18 |
| `gpg_enos_g` | Enosh | `ενωσ` | 6 |
| `gpg_booz_g` | Boaz | `βοεσ` | 3 |
| `gpg_thara_g` | Terah | `θαρα` | 3 |
| `gpg_aram_g` | Ram/Aram | `αραμ` | 2 |
| `gpg_achaz_g` | Ahaz | `αχασ` | 2 |
| `gpg_achim_g` | Achim | `αχιμ` | 2 |
| `gpg_mary_g` | Mary | `μαρια` | 2 |

The top omitted verse blocks by broken hits were:

| Omitted Verse | Broken Hits |
| --- | ---: |
| `MRK 9:46` | 12 |
| `LUK 23:17` | 9 |
| `JHN 5:4` | 6 |
| `MRK 15:28` | 4 |
| `ACT 24:7` | 3 |
| `ROM 16:26` | 3 |
| `ROM 16:27` | 3 |

## How To Read This

Read the main result as negative on strength but useful on method.

The study did what it was supposed to do:

- it locked the terms first;
- it ran the same rules across sources;
- it used controls;
- it reported weak and negative rows instead of hiding them;
- it kept the omission-break check separate from the control-strength check.

That is a good outcome for a research tool. It tells us what the current data
does and does not support.

## What This Does Not Say

This page does not say that the Gospel-name rows are meaningful hidden messages.
It does not say that one Greek New Testament tradition is authenticated by the
counts. It does not say that an omission break is bad or suspicious.

It says something narrower:

- exact source text matters;
- short names can create many hits;
- controls are necessary;
- this locked Gospel-name run did not produce adjusted control support;
- some TR hidden-letter paths depend on verses not present in SBLGNT.

## Next Useful Step

The most useful next step is not to broaden the claim. It is to inspect the
seven unadjusted rows and the 50 omission-break examples as review material,
with the same caution used in the locked reports.
