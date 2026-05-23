# Private English Versions

## Scope

This project can compare generated English ELS search terms across:

- `KJV`: public eBible KJV config.
- `AMPC`: local user-supplied Amplified Bible Classic Edition text.
- `NLT`: local user-supplied New Living Translation text.
- `MSG`: local user-supplied The Message text.
- `TPT`: local user-supplied The Passion Translation text.
- `NIV`: local user-supplied New International Version text.

Only config stubs are tracked. The AMPC, NLT, MSG, TPT, and NIV source text must stay
local under `data/private/`, which is ignored by git.

The full BibleGateway English-version list is tracked in
`configs/biblegateway_english_versions.csv`. That manifest contains 64 English
entries from `https://www.biblegateway.com/versions/`, using KJV as the public
baseline and local CSV hooks for every other listed English version.

The manifest also wires public-domain eBible sources for these BibleGateway
labels when available, and official eBible local-only sources where eBible
publishes downloadable source packages. Examples include:

- `ASV`
- `BSB`
- `DARBY`
- `DRA`
- `E2T`
- `ERV`
- `FBV`
- `F35`
- `GNV`
- `GW`
- `KJV`
- `LSV`
- `NET`
- `OURB`
- `OJB`
- `T4T`
- `ULB`
- `WEB`
- `WYC`
- `YLT`

Additional local-only BibleGateway labels can be populated from Bolls static
translation ZIPs. The importer uses the documented full-translation files, not
chapter scraping:

```bash
python3 -m scripts.import_bolls_translation --slug ESV --label ESV
```

Current Bolls-populated BibleGateway labels:

- `AMP` from Bolls `AMP`
- `CJB` from Bolls `CJB`
- `NKJV` from Bolls `NKJV`
- `RSV` from Bolls `RSV`
- `TLV` from Bolls `TLV`
- `LSB` from Bolls `LSB`
- `NASB1995` from Bolls `NASB`
- `ESV` from Bolls `ESV`
- `MEV` from Bolls `MEV`
- `NABRE` from Bolls `NABRE`
- `CSB` from Bolls `CSB17`
- `CEV` from Bolls `CEVD`
- `CEB` from Bolls `CEB`
- `GNT` from Bolls `GNTD`
- `ISV` from Bolls `ISV`
- `NLV` from Bolls `NLV`
- `NRSVCE` from Bolls `NRSVCE`
- `RSVCE` from Bolls `RSV2CE`

Copyrighted eBible-sourced versions are still treated as local-only corpora:
the source text remains under ignored `data/raw/` and `data/processed/`, and
public outputs must follow the upstream permission limits. Copyrighted
BibleGateway versions without an available lawful source package remain
private-only CSV hooks and are not active blockers. The working English corpus
set is whatever is already available locally or from a lawful source package
with clear permission; do not scrape BibleGateway text to fill missing rows.
Bolls-sourced ZIPs, extracted CSVs, and manifests stay under ignored
`data/private/`.

Door43 open English controls are tracked separately in
`configs/door43_english_controls.csv` for ULT and UST. Their raw and processed
texts remain local under ignored `data/raw/door43/` and
`data/processed/door43/`.

The manifest also tracks broad source-basis metadata:

- `ot_basis`
- `nt_basis`
- `source_family`
- `basis_status`

These fields are coarse tradition labels, not edition-level textual-critical
claims. Rows marked `needs_audit` should be verified against publisher
introductions before being used in public argumentation. For ELS work they are
mainly grouping fields: for example KJV/TR-family, modern critical, Vulgate,
Catholic critical, Byzantine/Majority, paraphrase, or NT-only.

Validate current source-basis metadata and queue counts with:

```bash
python3 -m scripts.check_source_basis_audit_queue
```

## Local File Layout

Expected files:

```text
data/private/english/nlt.csv
data/private/english/ampc.csv
data/private/english/msg.csv
data/private/english/tpt.csv
data/private/english/niv.csv
data/private/english/<biblegateway-label>.csv
data/private/english/source_files/bolls_<slug>.zip
```

Expected CSV header:

```csv
ref,book,chapter,verse,text
```

Rows may be verse-level or passage-level, but corpus order must already be
canonical Bible order. ELS letters are taken from `text`; references are used
only for reporting. If a local export uses different column names, update the
matching config:

- `configs/local_nlt.toml`
- `configs/local_ampc.toml`
- `configs/local_msg.toml`
- `configs/local_tpt.toml`
- `configs/local_niv.toml`

## Run

Validate local files:

```bash
python3 -m els stats --config configs/local_nlt.toml
python3 -m els stats --config configs/local_ampc.toml
python3 -m els stats --config configs/local_msg.toml
python3 -m els stats --config configs/local_tpt.toml
python3 -m els stats --config configs/local_niv.toml
```

Run KJV + private English comparison:

```bash
python3 -m scripts.run_protocol protocols/private_english_versions.toml --resume
```

Run the broader BibleGateway English-version comparison over every available
local CSV:

```bash
python3 -m scripts.run_protocol protocols/biblegateway_english_versions.toml --resume
```

The broader protocol skips missing local CSVs by default and writes
`reports/biblegateway_english_versions/missing_versions.csv`. Add
`--require-all` to `scripts.run_biblegateway_english_versions` when a complete
64-version local set should be mandatory.

Current refreshed scope:

- 34 available BibleGateway-overlap English versions.
- 30 missing BibleGateway English rows skipped.
- AMPC, NLT, MSG, TPT, and NIV private hooks are populated locally but remain
  ignored by git.
- TPT remains outside the BibleGateway manifest.

Main local outputs:

- `reports/private_english_versions/english_search_terms_counts.csv`
- `reports/private_english_versions/version_presence.csv`
- `reports/private_english_versions/version_presence.md`
- `reports/biblegateway_english_versions/version_presence.csv`
- `reports/biblegateway_english_versions/version_presence.md`

Those reports are ignored by git. Do not commit generated rows containing long
copyrighted verse context.

## Copyright Discipline

AMPC, NLT, MSG, TPT, and NIV are not public-domain texts. This repo does not include
their source text, a downloader, or generated full-text extracts. Treat these
configs as private analysis hooks for text you have lawful access to. Public
writeups should quote only within each publisher's stated limits and should not
redistribute the underlying corpus.

Publisher permission pages:

- NLT and MSG: `https://www.tyndale.com/permissions`
- AMPC: `https://www.harpercollinschristian.com/permissions/`
- TPT: `https://www.thepassiontranslation.com/permissions/`
- NIV: `https://www.biblica.com/permissions/`

## Interpretation Cautions

This protocol reports whether the same normalized English search term has ELS
hits in each observed English version at skip `2..100`. It does not prove that
the same source-language pattern exists across translations. Absence can also
reflect different wording, missing coverage, or partial local corpora such as
TPT editions that do not contain the full Bible.
