# Source-Basis Audit Queue

Status: local metadata queue for version rows whose manuscript/source-basis
labels are intentionally coarse. This is not an edition-level textual-critical
audit.

## Scope

Inputs:

- `configs/biblegateway_english_versions.csv`
- `configs/ebible_english_controls.csv`

Fields already tracked:

- `ot_basis`
- `nt_basis`
- `source_family`
- `basis_status`
- `notes`

Rows marked `broad_tradition` may be used as broad grouping labels. Rows
marked `needs_audit` should not be used for edition-level claims until checked
against publisher introductions, official source notes, or other primary
edition documentation.

## Counts

| Manifest | Rows | `needs_audit` | `broad_tradition` |
| --- | ---: | ---: | ---: |
| BibleGateway English versions | 64 | 22 | 42 |
| eBible English controls | 37 | 0 | 37 |

## BibleGateway Rows Needing Audit

| Label | Current family | Current note |
| --- | --- | --- |
| AMP | modern critical tradition | Lockman translation; exact editions should be publisher-audited |
| AMPC | modern critical tradition | Classic Lockman edition; exact editions should be publisher-audited |
| CJB | mixed Jewish-Christian tradition | Track as mixed until source-basis audit |
| CEV | modern critical tradition | American Bible Society translation; audit exact editions |
| DLNT | NT-only critical tradition | NT only |
| ERV | modern critical tradition | Official eBible ERV source; copyrighted local-only text; audit exact editions |
| EASY | modern critical tradition | Audit exact edition/source notes |
| EXB | modern critical tradition | Expanded NCV-related presentation; audit exact source notes |
| GW | modern critical tradition | Official eBible GW source; copyrighted local-only text; audit exact edition/source notes |
| ICB | modern critical tradition | NCV-family simplified translation; audit exact basis |
| ISV | modern critical tradition | Audit exact edition/source notes |
| PHILLIPS | NT-only paraphrase/translation | NT only |
| JUB | Reformation/TR tradition | Audit exact relationship to Spanish/Reformation sources |
| MSG | modern paraphrase | Treat as paraphrase surface comparison |
| MOUNCE | NT-only critical tradition | NT only; audit exact Greek edition |
| NOG | modern critical tradition | GOD'S WORD-related names edition; audit exact basis |
| NCB | Catholic critical tradition | Audit edition/source notes |
| NCV | modern critical tradition | Audit exact edition/source notes |
| NLV | modern simplified tradition | Audit exact edition/source notes |
| NTFE | NT-only critical/paraphrase tradition | NT only |
| VOICE | modern paraphrase | Treat as paraphrase surface comparison |
| WE | NT-only simplified tradition | NT only |

## eBible Control Rows Needing Audit

None after this pass.

## eBible Rows Audited This Pass

| Label | Basis status | Source evidence |
| --- | --- | --- |
| ASVBT | `broad_tradition` | eBible page identifies ASV conformed to Byzantine Text NT: <https://ebible.org/find/show.php?id=engasvbt> |
| BSB | `broad_tradition` | eBible/Berean pages support broad modern critical grouping: <https://ebible.org/find/show.php?id=engbsb> and <https://bereanbibles.com/about-berean-study-bible/greek-and-hebrew-sources/> |
| MSB | `broad_tradition` | MajorityBible identifies BSB OT plus Robinson-Pierpont Byzantine Majority Text NT: <https://majoritybible.com/> |
| OEBCW | `broad_tradition` | OEB FAQ identifies public-domain English bases, WLC/Leningrad OT, and W&H/TCNT NT: <https://openenglishbible.org/faq/> |
| OEB | `broad_tradition` | Same source-basis evidence as OEBCW; U.S. spelling edition: <https://openenglishbible.org/faq/> |
| BBE | `broad_tradition` | Local eBible source package identifies the Bible in Basic English; 1965 introduction says the translation was made from Hebrew and Greek: `data/raw/ebible/engBBE_usfm.zip` and <https://www.bible-researcher.com/basic.html> |
| NOY | `broad_tradition` | Local eBible source package identifies George Noyes Bible portions; Google Books title metadata identifies Noyes' NT as translated from Tischendorf's Greek text: `data/raw/ebible/engnoy_usfm.zip` and <https://books.google.com/books/about/The_New_Testament_Translated_from_the_Gr.html?id=lOJUAAAAcAAJ> |
| PEV | `broad_tradition` | Local eBible source package front matter says the PEV used Hebrew and Greek language study aids; exact editions are not stated: `data/raw/ebible/engPEV_usfm.zip` |
| OJB | `broad_tradition` | Local eBible source package identifies Tanakh and Orthodox Jewish Brit Chadasha presentation; exact textual editions are not stated: `data/raw/ebible/engojb_usfm.zip` |

## Checked But Still Queued

| Label | Reason |
| --- | --- |
| ERV | eBible/BibleGateway pages identify World Bible Translation Center/Bible League ownership and copyright, but not exact OT/NT textual bases: <https://ebible.org/find/show.php?id=engerv> |
| GW | eBible/BibleGateway pages describe accuracy against ancient texts, but do not identify exact OT/NT textual bases: <https://ebible.org/find/show.php?id=enggw> |

## Audit Rules

- Prefer publisher/source introductions over secondary summaries.
- Record exact edition or revision year when available.
- Separate OT basis, NT basis, and canon/Apocrypha coverage.
- Keep paraphrase/translation distinction visible.
- Do not treat English translation source basis as a manuscript witness in the
  same way as MT/LXX/Greek NT source texts.
- Leave `basis_status=needs_audit` when evidence is broad, ambiguous, or
  publisher wording is not checked.

## Suggested Next Pass

1. For BibleGateway `ERV` and `GW`, look for publisher introductions
   beyond the eBible/BibleGateway metadata pages already checked.
2. Continue publisher-source checks for the remaining BibleGateway
   `needs_audit` rows.
3. Leave missing private-only BibleGateway rows as metadata-only until lawful
   local texts are available.
