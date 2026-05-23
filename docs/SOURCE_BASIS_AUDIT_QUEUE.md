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
| BibleGateway English versions | 64 | 0 | 64 |
| eBible English controls | 38 | 0 | 38 |

## Validation

```bash
python3 -m scripts.check_source_basis_audit_queue
```

The formal report preflight also runs this check and fails if manifest counts
drift from this document, source metadata is malformed, or `needs_audit` rows
return without explicitly changing the validation policy.

## BibleGateway Rows Needing Audit

None after this pass.

## BibleGateway Rows Audited This Pass

| Labels | Basis status | Source evidence |
| --- | --- | --- |
| AMP, AMPC | `broad_tradition` | BibleGateway/Lockman notes identify Hebrew/Aramaic and Greek source-text work; AMPC also identifies ASV plus Kittel Hebrew and Westcott-Hort/Nestle Greek checks. |
| CJB | `broad_tradition` | BibleGateway/Stern notes identify OT relationship to the 1917 JPS and NT translation from ancient Greek. |
| CEV, GW, ICB, ISV, NCB, NLV, NOG, VOICE | `broad_tradition` | BibleGateway version notes support broad original-language or ancient-text grouping, with exact editions left unstated where not supplied. |
| DLNT, PHILLIPS, MOUNCE, NTFE | `broad_tradition` | BibleGateway version notes support broad Greek NT grouping, with exact Greek editions not stated. |
| ERV, EASY, NCV | `broad_tradition` | BibleGateway version notes identify specific or semi-specific modern critical source bases, including BHS/Biblia Hebraica, UBS/NA Greek, and DSS/Septuagint checks where documented. |
| EXB | `broad_tradition` | BibleGateway/Thomas Nelson notes identify EXB as NCV-family with original-language transparency. |
| JUB | `broad_tradition` | BibleStudyTools/JUB notes identify Hebrew/Greek-to-Spanish Reina-Valera lineage plus Tyndale/KJV comparison. |
| MSG | `broad_tradition` | BibleGateway/NavPress notes identify original-language work; keep as paraphrase surface comparison, not manuscript witness. |
| WE | `broad_tradition` | BibleGateway/CourseBible notes identify Annie Cressman simplified NT with revisions kept in line with the Authorized Version; treat as indirect English simplified control, not direct Greek witness. |

## eBible Control Rows Needing Audit

None after this pass.

## eBible Rows Audited This Pass

| Label | Basis status | Source evidence |
| --- | --- | --- |
| ASVBT | `broad_tradition` | eBible page identifies ASV conformed to Byzantine Text NT: <https://ebible.org/find/show.php?id=engasvbt> |
| BSB | `broad_tradition` | eBible/Berean pages support broad modern critical grouping: <https://ebible.org/find/show.php?id=engbsb> and <https://bereanbibles.com/about-berean-study-bible/greek-and-hebrew-sources/> |
| FBV | `broad_tradition` | eBible Free Bible Version page supplies a CC BY-SA 4.0 source package; treat as partial NT/Psalms free-translation control: <https://ebible.org/find/show.php?id=engfbv> |
| MSB | `broad_tradition` | MajorityBible identifies BSB OT plus Robinson-Pierpont Byzantine Majority Text NT: <https://majoritybible.com/> |
| OEBCW | `broad_tradition` | OEB FAQ identifies public-domain English bases, WLC/Leningrad OT, and W&H/TCNT NT: <https://openenglishbible.org/faq/> |
| OEB | `broad_tradition` | Same source-basis evidence as OEBCW; U.S. spelling edition: <https://openenglishbible.org/faq/> |
| BBE | `broad_tradition` | Local eBible source package identifies the Bible in Basic English; 1965 introduction says the translation was made from Hebrew and Greek: `data/raw/ebible/engBBE_usfm.zip` and <https://www.bible-researcher.com/basic.html> |
| NOY | `broad_tradition` | Local eBible source package identifies George Noyes Bible portions; Google Books title metadata identifies Noyes' NT as translated from Tischendorf's Greek text: `data/raw/ebible/engnoy_usfm.zip` and <https://books.google.com/books/about/The_New_Testament_Translated_from_the_Gr.html?id=lOJUAAAAcAAJ> |
| PEV | `broad_tradition` | Local eBible source package front matter says the PEV used Hebrew and Greek language study aids; exact editions are not stated: `data/raw/ebible/engPEV_usfm.zip` |
| OJB | `broad_tradition` | Local eBible source package identifies Tanakh and Orthodox Jewish Brit Chadasha presentation; exact textual editions are not stated: `data/raw/ebible/engojb_usfm.zip` |

## Checked But Still Queued

None after this pass.

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

1. Leave missing private-only BibleGateway rows as metadata-only unless a lawful
   local text or source package with clear permission is available.
