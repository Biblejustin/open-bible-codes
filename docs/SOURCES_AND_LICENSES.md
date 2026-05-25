# Sources And Licenses

## Code

Open Bible Codes code: MIT License.

Prior-art code audits:

- Amandasaurus/Rory `biblecode`: `https://github.com/amandasaurus/biblecode`.
  Reviewed as public implementation context only. GitHub detects AGPL-3.0 from
  `LICENCE`, while `Cargo.toml` says AGPL-1.0 and points at
  `https://github.com/rory/biblecode`. Do not copy or derive code into this
  MIT-licensed project without a separate compatible grant.

Public methodology and claim-source pages:

- Bible-codes.org `What are Bible Codes?` and linked source pages:
  `https://www.bible-codes.org/what-are-Bible-codes.htm`. Reviewed as public
  claim and methodology context only. No site text or code is redistributed as
  source data.

## Bible Texts

Raw texts are excluded from git by default.

Allowed source paths:

- Public domain texts.
- Open-license texts compatible with intended release.
- Private local texts used only for private analysis.

Required metadata for distributable corpora:

- Source name.
- Edition/manuscript basis.
- URL or publication detail.
- License.
- Download date.
- File checksum.
- Normalization choices.

## Lexicons And Term Sources

Strong's Greek Dictionary XML:

- `scripts/build_greek_lexicon_prospective_terms.py`
- `terms/greek_lexicon_prospective_terms.csv`
- `terms/greek_lexicon_extension_terms_clean_lock.csv`

This source uses `morphgnt/strongs-dictionary-xml`. The upstream README states
that the XML release is under the Creative Commons CC0 waiver. Raw XML stays
under ignored `data/raw/`; the tracked term CSVs contain deduped Greek
headwords and source metadata for prospective study locking.

Bootstrap all current public source paths:

```bash
python3 -m scripts.bootstrap_public_sources
```

Bootstrap large non-Bible background-control source paths separately:

```bash
python3 -m scripts.download_nonbible_controls
```

Private English translation hooks:

- `configs/local_nlt.toml`
- `configs/local_msg.toml`
- `configs/local_tpt.toml`
- `configs/local_niv.toml`
- `configs/biblegateway_english_versions.csv`

These configs point at user-supplied CSV files under `data/private/english/`.
That directory is ignored by git. Do not add downloaders, bundled text, or
generated full-text extracts for copyrighted English versions.

Open/CC eBible English controls:

- `configs/ebible_english_controls.csv`
- `scripts/download_ebible_english_controls.py`
- `protocols/ebible_english_controls.toml`

These controls use eBible USFM packages marked public-domain, CC BY 4.0, or
CC BY-SA 4.0 by eBible. Raw and processed source text stays under ignored
`data/raw/` and `data/processed/`; generated reports stay under ignored
`reports/`.

Use:

```bash
python3 -m scripts.download_ebible_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/ebible_english_controls.toml --resume
python3 -m scripts.run_protocol protocols/english_version_control_triage.toml --resume
```

Open Door43 English controls:

- `configs/door43_english_controls.csv`
- `scripts/download_door43_english_controls.py`
- `protocols/door43_english_controls.toml`

These controls use unfoldingWord ULT and UST source packages under CC BY-SA
4.0. Raw and processed source text stays under ignored `data/raw/` and
`data/processed/`; generated reports stay under ignored `reports/`.

Use:

```bash
python3 -m scripts.download_door43_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/door43_english_controls.toml --resume
```

Open English Translation controls:

- `configs/oet_english_controls.csv`
- `scripts/download_oet_english_controls.py`
- `protocols/oet_english_controls.toml`

These controls use the OET cleaned USFM files from the public OET repository.
The OET license page and repository README identify the Bible text as CC BY-SA
4.0. Raw and processed source text stays under ignored `data/raw/` and
`data/processed/`; generated reports stay under ignored `reports/`.

Use:

```bash
python3 -m scripts.download_oet_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/oet_english_controls.toml --resume
```

Open Translation Bible English control:

- `configs/otb_english_controls.csv`
- `scripts/download_otb_english_controls.py`
- `protocols/otb_english_controls.toml`

This control uses the OTB English `lang/en-GB` chapter JSON from the public
OTB repository. The repository README and `LICENCE.md` identify the text as
CC BY-SA 4.0. The upstream manuscript/source-text basis is not stated, so this
is an English surface control only, not a manuscript-tradition witness. Raw and
processed source text stays under ignored `data/raw/` and `data/processed/`;
generated reports stay under ignored `reports/`.

Use:

```bash
python3 -m scripts.download_otb_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/otb_english_controls.toml --resume
```

Open.Bible English controls:

- `configs/openbible_english_controls.csv`
- `scripts/download_openbible_english_controls.py`
- `protocols/openbible_english_controls.toml`

These controls use Open.Bible AFINT New Testament USFM downloads. The product
pages identify the downloads as English New Testament resources under CC BY-SA.
The upstream manuscript/source-text basis is not stated, so these are English
surface controls only, not manuscript-tradition witnesses. Raw and processed
source text stays under ignored `data/raw/` and `data/processed/`; generated
reports stay under ignored `reports/`.

Use:

```bash
python3 -m scripts.download_openbible_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/openbible_english_controls.toml --resume
```

Original Douay-Rheims English control:

- `configs/odr_english_controls.csv`
- `scripts/download_odr_english_controls.py`
- `protocols/odr_english_controls.toml`

This control uses the Original Douay-Rheims repository's USFM files. The
repository README and `LICENSE` identify the dataset as CC0 1.0 Universal. The
source is a historical Latin Vulgate-line English control, not a Greek/Hebrew
manuscript witness. Raw and processed source text stays under ignored
`data/raw/` and `data/processed/`; generated reports stay under ignored
`reports/`.

Use:

```bash
python3 -m scripts.download_odr_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/odr_english_controls.toml --resume
```

Supplemental open English controls:

- `configs/supplemental_english_controls.csv`
- `scripts/download_supplemental_english_controls.py`
- `protocols/supplemental_english_controls.toml`

These controls currently add AKJV from the official AKJV text ZIP, CPDV from
the CrossWire CPDV source archive, six BibleCorps source archives, eight
Zefania/CrossWire public-domain modules, and four OpenEnglishBible base-text
folders. The official AKJV page identifies the AKJV as public domain and based
on the KJV; the CrossWire CPDV, ACV, NHEB, Rotherham, Montgomery, Etheridge,
Weymouth, Tyndale, and RWebster module pages identify those modules as
public-domain source texts. CPDV is translated from Latin Vulgate editions;
Etheridge is a Syriac/Peshitta-line English NT; Tyndale is a partial
historical English control; RWebster is a KJV/Webster-line revision. ACV,
NHEB, Rotherham, Montgomery, and Weymouth stay broad English surface controls
unless their module pages state exact source-edition details.
BibleCorps metadata identifies Anderson, AV1611, AV1811, and DRC1750 as
public-domain source text, and DEB/PET as CC BY-SA 4.0 sources.
OpenEnglishBible's USFM repository marks the Kent, McFadyen, Moffatt, and TCNT
base files freely distributable; the OEB FAQ identifies TCNT 1904, Kent, and
McFadyen as public-domain OEB base texts and TCNT as Westcott-Hort NT
tradition. Raw and processed source text stays under ignored `data/raw/` and
`data/processed/`; generated reports stay under ignored `reports/`.

Use:

```bash
python3 -m scripts.download_supplemental_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/supplemental_english_controls.toml --resume
```

Generic eBible USFM import:

```bash
python3 -m scripts.download_ebible_usfm --source grclxx
python3 -m scripts.download_ebible_usfm --source grctr
python3 -m scripts.download_ebible_usfm --source grcmt
python3 -m scripts.download_ebible_usfm --source grctcgnt
python3 -m scripts.download_ebible_usfm --source eng-kjv2006
python3 -m scripts.download_ebible_usfm --source eng-kjv
python3 -m scripts.download_ebible_usfm --source eng-asv
python3 -m scripts.download_ebible_usfm --source engDBY
python3 -m scripts.download_ebible_usfm --source engDRA
python3 -m scripts.download_ebible_usfm --source engerv
python3 -m scripts.download_ebible_usfm --source enggnv
python3 -m scripts.download_ebible_usfm --source enggw
python3 -m scripts.download_ebible_usfm --source engnet
python3 -m scripts.download_ebible_usfm --source engojb
python3 -m scripts.download_ebible_usfm --source engwebp
python3 -m scripts.download_ebible_usfm --source engWycliffe
python3 -m scripts.download_ebible_usfm --source engylt
```

## Current Source Choices

### MT

Preferred full MT input:

- Open Scriptures Hebrew Bible / OSHB WLC XML files.
- Repository: `https://github.com/openscriptures/morphhb`
- WLC text: public domain.
- OSHB lemma/morphology data: CC BY 4.0.

Use:

```bash
python3 -m scripts.download_oshb_wlc
```

Additional MT comparison input:

- Unicode/XML Leningrad Codex / UXLC.
- Site: `https://www.tanach.us/`
- Manuscript basis: Leningrad Codex, forked from WLC 4.20 and updated against
  LC images.
- License note: Tanach.us states that all biblical Hebrew text in any format may
  be viewed or copied without restriction; cite Tanach.us.
- Current importer uses ketiv by default for the ELS stream because ELS should
  normally follow the written consonantal text. `qere_mode = "qere"` or
  `"both"` can be configured for declared comparison runs.

Use:

```bash
python3 -m scripts.download_uxlc
python3 -m els stats --config configs/example_uxlc.toml
```

Additional MT comparison input:

- Miqra according to the Masorah / MAM.
- Basis: Aleppo Codex plus Leningrad and related manuscripts where needed.
- License: CC BY-SA 4.0.
- Source path: `https://bdenckla.github.io/MAM-with-doc/`, attributed to
  Hebrew Wikisource.
- This is a Masorah-reader edition counterpoint to Leningrad-only WLC/UXLC.
- The importer reads only the verse text column; documentation cells are not
  included in the ELS stream.

Use:

```bash
python3 -m scripts.download_mam
python3 -m els stats --config configs/example_mam.toml
```

Additional WLC packaging check:

- eBible Hebrew WLC.
- Site: `https://ebible.org/details.php?id=hebwlc`
- eBible marks this package public domain.
- This is not expected to be a materially independent MT edition. Treat it as a
  packaging/versification comparison source against OSHB WLC and UXLC.
- The importer strips standalone Hebrew paragraph markers (`פ` (pe; English: open paragraph marker) / `ס` (samekh; English: closed paragraph marker)) from the
  USFM verse text before ELS normalization.

Use:

```bash
python3 -m scripts.download_ebible_hebwlc
python3 -m els stats --config configs/example_ebible_hebwlc.toml
```

Additional MT-family comparison input:

- unfoldingWord Hebrew Bible / UHB.
- Source: `https://git.door43.org/unfoldingWord/hbo_uhb`
- Current importer pins tag `v2.1.30`.
- License: CC BY-SA 4.0, with unfoldingWord trademark notice requirements.
- Basis: UHB states that it is based on Open Scriptures Hebrew Bible / WLC,
  with USFM 3.0 encoding, ULT-style versification, selected ketiv/qere choices,
  and some alternate readings.
- Treat this as a derived MT-family stream useful for version-distribution
  analysis, not as a clean Leningrad packaging duplicate.
- The importer strips USFM markers, notes, crossrefs, word attributes, and
  Hebrew paragraph markers before ELS normalization.

Use:

```bash
python3 -m scripts.download_uhb
python3 -m els stats --config configs/example_uhb.toml
```

Optional MT-adjacent comparison input:

- STEP Bible TAHOT selected Hebrew OT.
- Source: `https://github.com/STEPBible/STEPBible-Data`
- Source folder: `Translators Amalgamated OT+NT`
- License: repository and selected TAHOT files are marked CC BY 4.0; credit
  STEP Bible linked to `www.STEPBible.org`.
- Basis: TAHOT describes its Hebrew stream as Leningrad-codex based through
  Westminster/OpenScriptures, corrected from color scans, with morphology and
  semantic tags.
- Important limitation: TAHOT's own header says the selected text may follow
  qere, restore missing text, and include LXX-preserved additions converted to
  Hebrew from BHS/BHK apparatus. Treat it as a selected translator stream, not a
  pure Leningrad ketiv stream.
- The importer groups TAHOT word rows by English reference and preserves
  pointed Hebrew in CSV; normal corpus loading strips vowel/cantillation marks.

Use:

```bash
python3 -m scripts.download_step_tahot
python3 -m els stats --config configs/example_step_tahot.toml
```

Audit summary: `docs/STEP_TAHOT_SOURCE_AUDIT.md`.

Do not ingest for distributable data without separate permission:

- Mechon Mamre. Their copying page restricts use to private study/teaching and
  does not permit publication or redistribution without written permission.

Research-only candidate:

- ETCBC/BHSA. Useful for linguistic annotations and fixed historical data
  versions, but licensed CC BY-NC 4.0, so it should stay out of open commercial
  release paths unless permission is obtained.

Additional MT-family source candidates and admission criteria are tracked in
`docs/HEBREW_MT_SOURCE_CANDIDATES.md`. Sefaria MAM variants and CrossWire WLC
remain useful mostly as packaging/segmentation checks against sources already
imported here.

### Koren Torah

Used for common Torah-code examples:

- Brendan McKay ANU Koren Torah files.
- Michigan-Claremont transliteration.
- Five Torah book files only.
- The WRR audit protocol fingerprints the local Koren Genesis config, raw
  compressed source file, decompressed text, and normalized stream in
  `reports/wrr_1994/koren_genesis_text_source.md`.

Use:

```bash
python3 -m scripts.download_koren_torah
```

### WRR Data Audit Files

WRR replication source-audit files are downloaded into ignored reports output,
not committed:

```bash
python3 -m scripts.run_protocol protocols/wrr_source_import.toml --resume
```

Current external sources:

- WRR 1994 paper PDF from the Notre Dame-hosted reading mirror cited in
  `docs/WRR_SOURCE_AUDIT.md`.
- WRR famous-rabbis plain-text lists from the ANU/McKay Bible Codes Refuted
  data page.
- WRR/Nations discussion pages from Dror Bar-Natan's University of Toronto
  pages, used only as source-audit context for the cited 163-distance
  description.
- Modified Michigan-Claremont transliteration key from the same site.
- WNP/McKay-Bar-Natan critique pages in modified Michigan-Claremont notation
  and English transliteration from the same site.
- MBBK 1999 response paper, its linked data page, and the Chance article from
  Brendan McKay's Bible Codes Refuted pages, used as source-method context for
  corrected-distance details and critique.
- Torah-code.org papers and data pages, including Haralick protocol papers,
  Bombach/Gans/Levitt/Rips/Witztum papers, and associated data PDFs, used as
  source-audit context and possible future test leads.
- Torah-code.org experiments pages and linked data/report PDFs, including the
  personal-statement page, American Presidents, Israeli Prime Ministers,
  Cities/Aumann/Simon-McKay, Sons of Haman, Pumbedita, Auschwitz, and Ark
  pages. These are source-audit and protocol-design leads only; do not treat
  them as claim-ready evidence without a separately locked protocol and source
  parser.
- Torah-code.org research-program pages, used as methodology and simulation
  design context for model-driven ELS tests. These pages are not raw Bible text
  and not statistical evidence by themselves.

### Copyrighted Source-Audit Books

Some source-audit work uses user-supplied copyrighted books or PDFs as claim
leads. These files are not committed and are not redistributed by this project.

- Chuck Missler, `Cosmic Codes`, reviewed from a user-supplied PDF only. The
  audit summary is `docs/COSMIC_CODES_AUDIT.md`; short declared search terms
  are in `terms/cosmic_codes_claim_terms.csv`.

### Public Methodology Sources

- Felcjo Ringo, "Bible Codes: Making an Algorithm to Find Hidden Word
  Sequences in Text", Medium, reviewed as algorithm/control context in
  `docs/FELCJO_RINGO_ALGORITHM_AUDIT.md`. The linked GitHub repository is not
  imported and its license is not assumed.
- Institute for Biblical & Scientific Studies, "Bible Codes", reviewed as ELS
  critique, source-variation, and non-ELS code context in
  `docs/BIBLE_AND_SCIENCE_CODES_AUDIT.md`.
- Religions Wiki, "Argument from scriptural codes", reviewed as broad
  scriptural-code critique and methodology context in
  `docs/RELIGIONS_WIKI_SCRIPTURAL_CODES_AUDIT.md`. The page states Creative
  Commons Attribution-ShareAlike 2.5 availability.

These files are secondary audit sources. They do not by themselves make a WRR
replication claim-ready. See `docs/WRR_SOURCE_AUDIT.md`.

### Critical Greek NT

Preferred open critical-text proxy:

- SBL Greek New Testament.
- Repository: `https://github.com/Faithlife/SBLGNT`
- License: CC BY 4.0.

Use:

```bash
python3 -m scripts.download_sblgnt
```

### Greek NT Morphology

Preferred lemma/POS source:

- MorphGNT SBLGNT.
- Repository: `https://github.com/morphgnt/sblgnt`
- SBLGNT text is under the SBLGNT EULA.
- Morphological parsing and lemmatization: CC BY-SA 3.0.
- Keep raw MorphGNT data outside git unless release licensing is reviewed.

Use:

```bash
python3 -m scripts.download_morphgnt_sblgnt
```

Modern transliteration spellings were checked against live web references where needed; keep variants explicit in `terms/modern_names_dates.csv`.

### TR Greek NT

Current local TR source:

- Local-only config: `configs/tr_codex_bible.local.toml`
- This config is ignored by git because it points to a machine-local source.

Preferred public TR source path:

- Use `scripts/download_ebible_grctr.py` to download eBible Greek Textus Receptus USFM and convert it to CSV.
- eBible's GRCTR details page currently labels the text public domain and says the manuscript-comparison footnotes were dedicated to the public domain.
- The generated manifest records source URL, details URL, download time, checksum, and verse count.

Use:

```bash
python3 -m scripts.download_ebible_grctr
python3 -m els stats --config configs/example_ebible_grctr.toml
```

Useful upstream reference:

- eBible GRCTR details page: `https://ebible.org/details.php?id=grctr`

### Byzantine Greek NT

Preferred public Byzantine/Majority Text source path:

- Use `scripts/download_ebible_grcmt.py` to download eBible Greek Majority
  Text NT USFM and convert it to CSV.
- eBible's GRCMT details page currently labels the text public domain and
  identifies it as the Robinson-Pierpont 2018 Byzantine Textform.
- The generated manifest records source URL, details URL, download time,
  checksum, and verse count.

Use:

```bash
python3 -m scripts.download_ebible_grcmt
python3 -m els stats --config configs/example_ebible_grcmt.toml
```

Useful upstream references:

- eBible GRCMT details page: `https://ebible.org/bible/details.php?id=grcmt`
- Robinson-Pierpont Byzantine Textform license note:
  `https://byzantinetext.com/study/editions/robinson-pierpont/`
- ByzTxt public download page: `https://www.byztxt.com/download/`

### Text-Critical Greek NT

Preferred public text-critical Greek NT source path:

- Use `scripts/download_ebible_grctcgnt.py` to download eBible Text-Critical
  Greek NT USFM and convert it to CSV.
- eBible's GRCTCGNT details page currently labels the text public domain and
  describes it as "The New Testament in Ancient Greek with critical text notes."
- The details page says the edition is based on the Robinson-Pierpont 2018
  Byzantine Textform and includes critical text notes.
- The importer strips USFM notes and crossrefs, so the derived CSV contains
  verse text only.
- The generated manifest records source URL, details URL, download time,
  checksum, and verse count.

Use:

```bash
python3 -m scripts.download_ebible_grctcgnt
python3 -m els stats --config configs/example_ebible_grctcgnt.toml
```

Useful upstream reference:

- eBible GRCTCGNT details page: `https://ebible.org/details.php?id=grctcgnt`

### English KJV

Preferred public English source path:

- Use `scripts/download_ebible_engkjv.py` to download eBible English KJV USFM
  and convert it to CSV.
- eBible's ENGKJV / `eng-kjv2006` details page labels the package public
  domain and identifies it as the standardized 1769 King James / Authorized
  Version, protocanon only, with Strong's numbers added.
- The details page notes UK Crown printing restrictions but says the work is
  public domain outside the UK.
- The generated manifest records source URL, details URL, download time,
  checksum, and verse count.

Use:

```bash
python3 -m scripts.download_ebible_engkjv
python3 -m els stats --config configs/example_ebible_engkjv.toml
```

Useful upstream reference:

- eBible English KJV details page: `https://ebible.org/find/show.php?id=eng-kjv2006`

### English KJV + Apocrypha

Separate public English apocrypha source path:

- Use `scripts/download_ebible_engkjv_apocrypha.py` to download eBible
  `eng-kjv` USFM and convert it to CSV.
- eBible labels `eng-kjv` as public domain outside UK Crown printing
  restrictions and describes it as the standardized 1769 KJV with
  Apocrypha/Deuterocanon.
- This corpus is intentionally separate from `eng-kjv2006` so existing KJV
  baselines remain 66-book unless a protocol explicitly selects KJVA.

Use:

```bash
python3 -m scripts.download_ebible_engkjv_apocrypha
python3 -m els stats --config configs/example_ebible_engkjv_apocrypha.toml
```

Useful upstream reference:

- eBible KJV + Apocrypha details page: `https://ebible.org/find/show.php?id=eng-kjv`

### Non-Bible Control Corpora

Non-Bible controls are kept separate from Bible-source bootstrap:

- Project Ben-Yehuda public-domain dump for Hebrew literature controls.
  Source: `https://github.com/projectbenyehuda/public_domain_dump`
  The repository README says the dump contains public-domain Hebrew works and
  may be freely reused. Current configs use `txt_stripped` author directories
  for Haim Nahman Bialik, Yosef Haim Brenner, and Ahad Ha'am.
- PerseusDL canonical Greek literature for Greek controls.
  Source: `https://github.com/PerseusDL/canonical-greekLit`
  The repository states CC BY-SA 4.0 unless otherwise indicated. Current
  configs use Homer Iliad, Homer Odyssey, and Herodotus Histories.
- Project Gutenberg for English controls.
  Sources: `https://www.gutenberg.org/ebooks/100`,
  `https://www.gutenberg.org/ebooks/2600`, and
  `https://www.gutenberg.org/ebooks/2701`.
  Each page currently marks the work public domain in the USA. Current configs
  use Shakespeare, War and Peace, and Moby Dick.

Use:

```bash
python3 -m scripts.download_nonbible_controls
python3 -m scripts.run_protocol protocols/nonbible_control_counts.toml --resume
```

Study notes: `docs/NONBIBLE_CONTROL_CORPORA.md`.

### LXX

Current local LXX source:

- Local-only config: `configs/lxx_codex_bible.local.toml`
- This config is ignored by git because it points to a machine-local source.

Preferred public LXX source path:

- Use `scripts/download_ebible_grclxx.py` to download eBible GRCLXX USFM and convert it to CSV.
- eBible's GRCLXX details page currently labels the text public domain and links the USFM package.
- GRCLXX also carries an upstream Orthodox Media Network notice; preserve it in release notes if distributing a derived corpus.
- The generated manifest records source URL, details URL, download time, checksum, and verse count.
- Do not commit the current local `ot_full.csv` directly until its full source chain and license metadata are copied into this repo.

Use:

```bash
python3 -m scripts.download_ebible_grclxx
python3 -m els stats --config configs/example_ebible_grclxx.toml
```

Useful upstream references:

- eBible GRCLXX details page: `https://ebible.org/details.php?id=grclxx`
- eBible Brenton Greek details page: `https://ebible.org/details.php?id=grcbrent`

Local provenance currently inspected:

- private local `SOURCE_PROVENANCE.md`
- private local `NOTICE.md`

## Existing ELS Projects

Do not copy source code or generated datasets from existing ELS projects unless license is clear and compatible.

Use them only as:

- Feature inventory.
- Independent comparison target.
- Bibliographic/context reference.
