# Open Bible Codes Findings Overview

Status: reader summary over the whole project. This page does not run a new
search and does not raise any result to a public claim.

Main source pages:

- `docs/START_HERE.md`
- `docs/FINAL_REPORT.md`
- `docs/FINAL_REPORT_HIGHLIGHTS.md`
- `docs/CLAIM_CATALOG.md`
- `docs/CONSOLIDATED_FINDINGS.md`

## Bottom Line

The project can find hidden letter paths in Bible texts and compare them across
Hebrew, Greek, and English sources. It can also test whether those paths look
unusual compared with control searches.

The current answer is careful:

- real hidden-letter paths exist;
- some rows are worth review;
- controls explain many rows that first look striking;
- short words and names create many hits;
- no current row should be presented as a public claim.

The strongest result is not one single code. The strongest result is the
method: the project now records the source text, spelling, skip, direction,
center word, context, and control result instead of relying on raw hit counts.

## Common Terms

ELS means equidistant letter sequence. It means reading every same-numbered
letter. A skip of `5` reads every fifth letter. A skip of `-5` reads backward
every fifth letter.

Corpus means the text being searched. Examples include a Hebrew Bible text, a
Greek New Testament text, or an English Bible translation.

Witness means a source text or textual tradition being compared. For example,
two Greek New Testament witnesses may differ in wording or in which verses they
include.

Control means a comparison search. Controls ask whether similar or random
terms produce the same kind of result. A result that looks special before
controls may look ordinary after controls.

Adjusted result means the project corrected for running many tests. This is
important because a large search can create a few interesting-looking rows by
volume alone.

## What The Project Finds Reliably

The search engine reliably finds and records hidden-letter paths. It also keeps
the surrounding evidence:

- where the path starts, centers, and ends;
- which source text contains it;
- which source texts do not contain it;
- whether the center word is related to the hidden term;
- whether the path survives controls;
- whether the path depends on a text variant or omitted verse.

That makes the project useful as a research ledger. It can separate "the path
exists" from "the path is unusual."

## Current Highlight Rows

The final-report highlight table keeps five occurrence rows in view. These are
not public claims. They are rows worth preserving because they have useful
context.

| Hidden term | Center | Main read |
| --- | --- | --- |
| Greek `γωγ` (Gog) | Rev 20:8 `Gog` | Centers on the open word `Gog` across four Greek New Testament sources, but length-3 controls keep it cautious. |
| Hebrew `ישוע` (Yeshua/Jeshua) | Ezra 10:18 `Yeshua` | Real centered-self occurrence, with strong background caution. |
| Hebrew `משיח` (Messiah/anointed one) | 2 Sam 1:21 `Messiah/anointed one` | Real centered-self occurrence, with background caution. |
| Greek `ιησουσ` (Jesus/Joshua) | Josh 8:3 `Jesus/Joshua` in the LXX | Real centered-self occurrence; the passage refers to Joshua. |
| English `jesus` | Matt 4:10 `Jesus` in KJV | Real English translation occurrence; secondary to original-language work. |

The main point: these rows are worth listing, but they still carry control and
context cautions.

## Stronger Review Material

Some rows have stronger follow-up support than ordinary raw hits.

Greek `δοξα` (doxa; glory) has a four-source extension follow-up. The same key
appears in TR_NT, BYZ_NT, TCG_NT, and SBLGNT. Large follow-up controls passed
the registered review gates. This remains a controlled review candidate,
because it came from earlier screening.

Hebrew `יום יהוה` (yom YHWH; day of YHWH) has a compound-extension follow-up
across five MT-family Hebrew sources. The locked 5000/5000 controls kept the
selected row favorable. This is strong post-discovery review material, not a
prospective public claim.

The KJV with Apocrypha bridge study is also a stronger follow-up area. The
KJVA bridge rows stood above several shuffled-control layers. This raises
follow-up priority, but it is still post-screen work.

Greek expanded surface rows such as `ανομια` (lawlessness), `ισαακ` (Isaac),
and `τερασ` (wonder) passed some review filters. They remain review candidates,
not public claims.

## Results That Look Weak

Several areas are useful because they tell us what not to overstate.

Modern names and geopolitical terms are weak overall. Short forms like Trump,
Vance, Iran, USA, and NATO can produce many hits because short strings are
dense. Longer phrases such as United States, United Nations, European Union,
Cowboy Catering, and similar local terms are absent or effectively absent in
the observed Hebrew and Greek screens.

The Hebrew Gog/Magog pair study was negative under its locked controls. Gog and
Magog remain important biblical terms, and the Greek Rev 20:8 Gog occurrence
is still worth listing. But the Hebrew pair-control lane did not produce a
controlled review candidate.

The Gospel people and genealogy study also stayed cautious. It screened names
from Christ's genealogy, disciples, Gospel women, and other Gospel figures. It
found many paths, but none survived adjusted representative controls.

Broad skip searches and full-span searches create enormous hit counts. They
are useful for building review queues, but raw volume grows quickly when the
skip range gets wider. Raw volume by itself should not be treated as meaning.

## Text-Variant And Omission Work

The project also tests how source-text differences affect hidden-letter paths.

The TR-vs-SBLGNT omission-break study asks whether hidden paths in the Textus
Receptus break when verses absent from SBLGNT are removed. The shared engine
does find broken paths, but the null model is cautionary: the actual omitted
blocks did not break more TR hidden paths than matched random verse blocks in
the current run.

This makes the omission work useful as a source-sensitivity audit, not as a
positive claim.

The newer Gospel-name omission check found 50 broken Greek TR paths in the
locked Gospel people/genealogy cohort at minimum length 4. All 50 broke
because a used letter was inside an omitted TR verse block. This is a text
sensitivity result, not a strength result.

## WRR Status

WRR means Witztum-Rips-Rosenberg, the famous-rabbis Bible-code study.

The repository now has a serious local WRR workstream: source audits, term
imports, corrected-distance diagnostics, locked local method reports, and
decision packets. But exact published WRR reproduction is still not complete.

The main blocker is the gap between the source-cited 163 defined-distance
count and the current repo-defined count. The project now tracks that gap
plainly instead of hiding it.

Current read: local locked-method evidence exists, but exact published WRR
reproduction remains caveated.

## How To Read A Result

Use three questions.

First: does the hidden path exist in the stated source text?

Second: what does it touch? Look at the center word, nearby words, passage, and
source witnesses.

Third: do controls make it unusual? If controls produce similar results, the
row should stay in review status.

Most mistakes happen when raw occurrence is treated as strength. This project
keeps those separate.

## Current Project Read

The project has real occurrence findings and review candidates.

It does not currently have a result that should be promoted as a public claim.

That is still useful progress. The project can now:

- reproduce simple sanity-check examples;
- collect hidden-letter paths across many sources;
- compare source traditions;
- run matched and shuffled controls;
- mark weak and negative results;
- keep source, method, and license limits visible.

## Best Next Steps

The best next work is not to make the claims broader. It is to keep improving
review quality:

- inspect the strongest review candidates by context;
- keep source locks and spelling locks strict;
- avoid changing terms after seeing results;
- use controls before promoting any row;
- keep public wording conservative.

For deeper detail, use `docs/FINAL_REPORT.md`, then
`docs/CLAIM_CATALOG.md`, then `docs/CONSOLIDATED_FINDINGS.md`.
