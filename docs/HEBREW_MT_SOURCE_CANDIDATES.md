# Hebrew MT Source Candidates

Last reviewed: 2026-05-22.

This note answers the practical question: "Are there different Hebrew MT
versions we can pull in?" The current repo already has several MT-family streams
for version-presence analysis. More sources should be admitted only when they
add either textual independence, useful packaging/versification comparison, or
auditable licensing value.

## Current Imported Streams

| Source ID | Config | Textual role | Release posture |
| --- | --- | --- | --- |
| `MT_WLC` | `configs/example_oshb_wlc.toml` | Open Scriptures / Westminster Leningrad Codex XML stream. Baseline full MT source. | Public-domain WLC text plus CC BY 4.0 OSHB lemma/morphology metadata. |
| `UXLC` | `configs/example_uxlc.toml` | Unicode/XML Leningrad Codex from Tanach.us, ketiv-first by default. | Open copying note from Tanach.us; used as Leningrad/WLC comparison source. |
| `MAM` | `configs/example_mam.toml` | Miqra according to the Masorah, Aleppo-centered reader edition where available. | CC BY-SA 4.0 path through MAM / Hebrew Wikisource. |
| `EBIBLE_WLC` | `configs/example_ebible_hebwlc.toml` | eBible packaging of Hebrew WLC. | Public-domain-marked package; mainly packaging and versification check. |
| `UHB` | `configs/example_uhb.toml` | unfoldingWord Hebrew Bible, derived MT-family USFM stream. | CC BY-SA 4.0 with attribution/trademark requirements. |
| `STEP_TAHOT` | `configs/example_step_tahot.toml` | STEP/Tyndale selected Hebrew OT stream. | Optional CC BY 4.0 source; not a pure Leningrad ketiv stream. |
| `MICHIGAN_TORAH` | `configs/example_michigan_torah.toml` | Michigan-Claremont Torah files used for WRR/Koren-style audit comparisons. | Research/audit stream, Torah-only, not a full MT replacement. |

## Candidate Ranking

### 1. Sefaria MAM variants

Sefaria's current source/license page lists the Hebrew Torah and Tanakh text as
Miqra according to the Masorah under CC BY-SA. That is compatible with the MAM
family already imported here.

Decision: do not add as a new independent corpus yet. It is probably another
packaging/segmentation route into MAM, not a materially distinct Hebrew MT text.
It may be useful later for an importer cross-check if we want to compare
Sefaria segmentation, API behavior, or chapter/verse normalization.

Useful source:

- `https://lite.sefaria.org/sources-and-licenses`

### 2. STEP Bible TAHOT data

STEPBible-Data is useful because the public repository describes the data as CC
BY 4.0 and includes `TAHOT`, a Leningrad-codex-based Hebrew OT stream with tags
and corrections. The selected TAHOT files also carry `CC BY` in the filenames
and header.

Decision: optional importer added in `scripts/download_step_tahot.py`. The
standalone alignment audit and version-presence follow-ups are now complete; see
`docs/STEP_TAHOT_SOURCE_AUDIT.md`, `docs/STEP_TAHOT_VERSION_PRESENCE_REVIEW.md`,
`docs/STEP_TAHOT_SCREENING_VERSION_PRESENCE.md`, and
`docs/STEP_TAHOT_FINAL_GATE.md`. Keep it out of baseline Leningrad-family
reports. TAHOT's header says the selected text may follow qere, restore missing
text, and include LXX-preserved additions converted to Hebrew from BHS/BHK
apparatus. That makes it useful as a translator-selected MT-adjacent stream, but
not as a pure Leningrad ketiv stream.

Use:

```bash
python3 -m scripts.download_step_tahot
python3 -m els stats --config configs/example_step_tahot.toml
```

Current audit summary:

- `docs/STEP_TAHOT_SOURCE_AUDIT.md`

Useful source:

- `https://github.com/STEPBible/STEPBible-Data`

### 3. CrossWire WLC module

CrossWire's WLC module page currently labels the module public domain and says
the text traces through Westminster / Tanach.us. This is open enough to consider
for a packaging comparison.

Decision: lower priority. It is unlikely to add independent textual evidence
beyond WLC/UXLC/eBible WLC. Add only if we want a SWORD-module importer or an
external packaging checksum check.

Useful sources:

- `https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=WLC`
- `https://www.crosswire.org/sword/copyright/ModInfoCopyright.jsp?modName=WLC`

### 4. Translator's Hebrew Bible / THB

THB documents WLC text as public domain and OSHB morphology as CC BY 4.0. It is
useful as an external source-audit reference, but it appears to integrate the
same WLC/OSHB base already used here for MT.

Decision: do not add as a primary MT corpus. Revisit only if THB exposes a
stable download format with clear text-field provenance that differs from our
existing OSHB/WLC stream.

Useful source:

- `https://hebrewbible.dev/license/`

### 5. ETCBC / BHSA

BHSA is excellent for linguistic and morphology analysis, but it has been
documented in this repo as CC BY-NC 4.0. That does not fit the open-release goal
without separate permission.

Decision: keep out of distributable paths. It can be considered only as a
private/local optional analysis source.

### 6. Proprietary or permission-limited Tanakh editions

Koren, Mechon Mamre, and similar editions may be textually interesting, but they
should not be imported into an open release path unless their terms explicitly
permit the intended reuse and redistribution.

Decision: do not ingest for distributable data without separate permission.

## Current Admission Boundary

Do not add another Hebrew corpus immediately. The current STEP_TAHOT audits
already answer the previous source-admission question:

- `STEP_TAHOT` loads as 39 books, 23,261 verses, and 1,197,732 normalized
  letters.
- Against `MT_WLC`, 23,011 refs align; 20,037 are equal and 2,974 differ.
- In broader Hebrew screening, 379 rows were `STEP_TAHOT`-only.
- The final gate found real screening rows were `STEP_TAHOT`-only at 2.449%
  while null/frequency controls were `STEP_TAHOT`-only at 2.388%.
- All `STEP_TAHOT`-only rows remain held as selected-reading policy paths or
  source-specific L-only paths, not claim rows.

Future Hebrew source work should be a new source-admission audit only if it adds
textual independence, packaging/versification coverage that changes a concrete
question, or licensing value. Do not treat `STEP_TAHOT` as a plain MT duplicate
or as claim-strengthening evidence.

## Source Admission Checklist

Every new Hebrew source should enter through this checklist before a downloader
lands:

- Source URL and exact raw file path.
- License URL and compatibility note.
- Required attribution.
- Edition/manuscript basis.
- Raw checksum and download date in manifest.
- Verse-count and book-order audit.
- Normalization policy.
- Ketiv/qere policy.
- Treatment of paragraph markers, apparatus, notes, and additions.
- Comparison against existing corpora by verse count, normalized length, and
  exact-hit version-presence behavior.
