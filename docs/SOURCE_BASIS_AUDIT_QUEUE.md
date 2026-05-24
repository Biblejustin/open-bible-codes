# Source-Basis Audit Queue

Status: local metadata queue for version rows whose manuscript/source-basis
labels are intentionally coarse. This is not an edition-level textual-critical
audit.

## Scope

Inputs:

- `configs/biblegateway_english_versions.csv`
- `configs/ebible_english_controls.csv`
- `configs/door43_english_controls.csv`
- `configs/oet_english_controls.csv`
- `configs/otb_english_controls.csv`
- `configs/openbible_english_controls.csv`
- `configs/odr_english_controls.csv`
- `configs/supplemental_english_controls.csv`

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
Rows whose `ot_basis` or `nt_basis` says the upstream source basis is not
stated are usable only as English surface controls, not manuscript witnesses.

## Counts

| Manifest | Rows | `needs_audit` | `broad_tradition` |
| --- | ---: | ---: | ---: |
| BibleGateway English versions | 64 | 0 | 64 |
| eBible English controls | 44 | 0 | 44 |
| Door43 English controls | 2 | 0 | 2 |
| OET English controls | 2 | 0 | 2 |
| OTB English controls | 1 | 0 | 1 |
| Open.Bible English controls | 4 | 0 | 4 |
| Original Douay-Rheims English controls | 1 | 0 | 1 |
| Supplemental open English controls | 19 | 0 | 19 |

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

## Door43/OET/OTB/Open.Bible/ODR/Supplemental Control Rows Needing Audit

None after this pass.

## eBible Rows Audited This Pass

| Label | Basis status | Source evidence |
| --- | --- | --- |
| ASVBT | `broad_tradition` | eBible page identifies ASV conformed to Byzantine Text NT: <https://ebible.org/find/show.php?id=engasvbt> |
| BSB | `broad_tradition` | eBible/Berean pages support broad modern critical grouping: <https://ebible.org/find/show.php?id=engbsb> and <https://bereanbibles.com/about-berean-study-bible/greek-and-hebrew-sources/> |
| E2T | `broad_tradition` | eBible Easy to Translate English Jonah page supplies a CC BY-SA 4.0 source package; treat as Jonah-only easy-translation control: <https://ebible.org/find/show.php?id=enge2t> |
| FBV | `broad_tradition` | eBible Free Bible Version page supplies a CC BY-SA 4.0 source package; current local USFM import contains 66 books, so treat as a full free-translation control: <https://ebible.org/find/show.php?id=engfbv> |
| F35 | `broad_tradition` | eBible Family 35 NT page supplies a CC BY-SA 4.0 source package and identifies the Family 35 Greek NT basis: <https://ebible.org/find/show.php?id=engf35> |
| LSV | `broad_tradition` | eBible Literal Standard Version page supplies a CC BY-SA 4.0 source package; exact textual editions are not stated: <https://ebible.org/find/show.php?id=englsv> |
| MSB | `broad_tradition` | MajorityBible identifies BSB OT plus Robinson-Pierpont Byzantine Majority Text NT: <https://majoritybible.com/> |
| OEBCW | `broad_tradition` | OEB FAQ identifies public-domain English bases, WLC/Leningrad OT, and W&H/TCNT NT: <https://openenglishbible.org/faq/> |
| OEB | `broad_tradition` | Same source-basis evidence as OEBCW; U.S. spelling edition: <https://openenglishbible.org/faq/> |
| OURB | `broad_tradition` | eBible One Unity Resource Bible page supplies a CC BY-SA 4.0 source package; exact textual editions are not stated: <https://ebible.org/find/show.php?id=engourb> |
| BBE | `broad_tradition` | Local eBible source package identifies the Bible in Basic English; 1965 introduction says the translation was made from Hebrew and Greek: `data/raw/ebible/engBBE_usfm.zip` and <https://www.bible-researcher.com/basic.html> |
| NOY | `broad_tradition` | Local eBible source package identifies George Noyes Bible portions; Google Books title metadata identifies Noyes' NT as translated from Tischendorf's Greek text: `data/raw/ebible/engnoy_usfm.zip` and <https://books.google.com/books/about/The_New_Testament_Translated_from_the_Gr.html?id=lOJUAAAAcAAJ> |
| PEV | `broad_tradition` | Local eBible source package front matter says the PEV used Hebrew and Greek language study aids; exact editions are not stated: `data/raw/ebible/engPEV_usfm.zip` |
| T4T | `broad_tradition` | eBible Translation for Translators page supplies a CC BY-SA 4.0 source package; treat as implied-information translator-help control: <https://ebible.org/find/show.php?id=eng-t4t> |
| ULB | `broad_tradition` | eBible Unlocked Literal Bible page supplies a CC BY-SA 4.0 source package and describes a close original-language ASV-family update: <https://ebible.org/find/show.php?id=engULB> |
| OJB | `broad_tradition` | Local eBible source package identifies Tanakh and Orthodox Jewish Brit Chadasha presentation; exact textual editions are not stated: `data/raw/ebible/engojb_usfm.zip` |

## Door43/OET/OTB/Open.Bible/ODR/Supplemental Rows Audited This Pass

| Label | Basis status | Source evidence |
| --- | --- | --- |
| ULT | `broad_tradition` | Door43 manifest identifies ULT as an ASV-based open literal translation with UHB/UGNT source relations: <https://git.door43.org/unfoldingWord/en_ult> |
| UST | `broad_tradition` | Door43 manifest identifies UST as an open functional translation with T4T/UHB/UGNT source relations: <https://git.door43.org/unfoldingWord/en_ust> |
| OET-LV | `broad_tradition` | OET source-text page identifies OSHB/WLC for Hebrew and SRGNT/CNTR for Greek; OET license page identifies CC BY-SA 4.0: <https://OpenEnglishTranslation.Bible/Design/SourceTexts> and <https://OpenEnglishTranslation.Bible/About/Licence> |
| OET-RV | `broad_tradition` | Same OET source-basis and license evidence as OET-LV; RV cleaned USFM includes draft deuterocanon/apocrypha files: <https://github.com/Freely-Given-org/OpenEnglishTranslation--OET/tree/main/exportedFiles/cleanedUSFM/ReadersVersion> |
| OTB | `broad_tradition` | OTB repository README and license identify CC BY-SA 4.0 and provide verse-level `lang/en-GB` JSON, but the upstream manuscript/source-text basis is not stated; use as a surface English control only: <https://github.com/OpenTranslationBible/open-bible> |
| AFINT-EXP-AE, AFINT-EXP-BE | `broad_tradition` | Open.Bible AFINT explanatory paraphrase pages identify English New Testament USFM downloads and CC BY-SA license, but do not state the Greek source/manuscript basis; use as surface English controls only: <https://www.open.bible/bibles/69a307e295245b14e244c7a0> and <https://www.open.bible/bibles/69a307df95245b14e244c797> |
| AFINT-LIT-AE, AFINT-LIT-BE | `broad_tradition` | Open.Bible AFINT literal pages identify English New Testament USFM downloads and CC BY-SA license, but do not state the Greek source/manuscript basis; use as surface English controls only: <https://www.open.bible/bibles/69a307e995245b14e244c7b0> and <https://www.open.bible/bibles/69a307e695245b14e244c7a8> |
| ODR | `broad_tradition` | Original Douay-Rheims repository identifies a CC0 1.0 USFM/JSON dataset for the unmodified 1609 Old Testament and 1582 New Testament; use as a historical Latin Vulgate-line English control: <https://github.com/janvier-s/original-douay-rheims> |
| AKJV | `broad_tradition` | Official AKJV page identifies the version as a simple word-for-word KJV English update, placed in the public domain on November 8, 1999: <https://akjv.us/> |
| CPDV | `broad_tradition` | CrossWire CPDV module identifies the translation as public domain and based on Sixtine-Clementine Latin Vulgate editions; use as a modern Vulgate-line English control: <https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=CPDV> |
| ACV, NHEB, ROTHERHAM, MONTGOMERY, ETHERIDGE, WEYMOUTH, TYNDALE | `broad_tradition` | CrossWire module pages identify these texts as public-domain English Bible modules; import uses the corresponding Zefania XML packages and keeps exact source-edition claims broad unless stated by the module page: <https://crosswire.org/sword/modules/ModInfo.jsp?modName=ACV>, <https://crosswire.org/sword/modules/ModInfo.jsp?modName=NHEB>, <https://crosswire.org/sword/modules/ModInfo.jsp?modName=Rotherham>, <https://crosswire.org/sword/modules/ModInfo.jsp?modName=Montgomery>, <https://crosswire.org/sword/modules/ModInfo.jsp?modName=Etheridge>, <https://crosswire.org/sword/modules/ModInfo.jsp?modName=Weymouth>, and <https://crosswire.org/sword/modules/ModInfo.jsp?modName=Tyndale> |
| ANDERSON | `broad_tradition` | BibleCorps Anderson README identifies the public-domain 1864 Anderson New Testament source and Internet Archive facsimile; use as a historical Greek-NT English control: <https://github.com/BibleCorps/ENG-B1-Anderson1864-pd-USFM> |
| AV1611 | `broad_tradition` | BibleCorps AV1611 source preserves the 1611 Authorized Version wording and front matter; use as a historical KJV-line English control: <https://github.com/BibleCorps/ENG-B-AV1611-pd-PSFM> |
| AV1811 | `broad_tradition` | BibleCorps AV1811 source identifies the Paragraph Bible source as an 1838 public-domain Authorized Version edition; use as a historical KJV-line paragraphing control: <https://github.com/BibleCorps/ENG-B-AV1811-pd-Cambridge-Paragraph-Bible-PSFM> |
| DEB | `broad_tradition` | BibleCorps Dynamic English Bible README marks the text as checking/not ready; Door43 YAML metadata identifies CC BY-SA 4.0 and source relations, so use as a draft surface English control: <https://github.com/BibleCorps/ENG-B-DEB2020-cc-PSFM> |
| DRC1750 | `broad_tradition` | DRC1750 front matter identifies the electronic edition as public domain and translated from the Latin Vulgate, revised according to the Clementine edition; use as a historical Vulgate-line English control: <https://github.com/BibleCorps/ENG-B-DRC1750-pd-PSFM> |
| PET | `broad_tradition` | PET front matter identifies CC BY-SA 4.0 and describes PET as an English translation of the Indonesian Simple Translation Bible; use as a surface English NT control: <https://github.com/BibleCorps/ENG-B1-PET2016-cc-PSFM> |
| KENT, MCFADYEN, TCNT | `broad_tradition` | OpenEnglishBible's USFM base-text repository marks the files freely distributable; the OEB FAQ identifies Kent, McFadyen, and TCNT 1904 as public-domain English bases, with TCNT tied to the Westcott-Hort NT tradition: <https://github.com/openenglishbible/usfm-bibles> and <https://openenglishbible.org/faq/> |
| MOFFATT | `broad_tradition` | OpenEnglishBible's USFM base-text repository marks the available Moffatt OT-portion files freely distributable; use as partial OT surface controls only because exact source-text edition details are not stated: <https://github.com/openenglishbible/usfm-bibles> |

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
