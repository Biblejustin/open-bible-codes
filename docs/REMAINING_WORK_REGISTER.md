# Remaining Work Register

Status: operational register after the 34-version English-source refresh, the
empty English seed survivor gate, the English source-basis audit, reader-report
hygiene, locked-report reruns, volatility cleanup, WRR single-term
source-policy propagation, Torah-code research-model source-status cleanup,
Greek follow-up status refreshes, and Hebrew MT/STEP_TAHOT source-status
cleanup, prospective-lane validator tightening, source-audit preflight guard
coverage, prospective-lane validation in report preflight, source-basis audit
queue guarding, English source-basis preflight inputs, formal source-basis
queue validation, source-basis validation documentation, and formal preflight
metadata-check documentation, study-tooling preflight coverage, and
preregistration placeholder guarding, CRD relevance-lock guarding,
manual-review queue preflight guarding, WRR readiness-doc guarding, WRR
blocker-packet preflight guarding, WRR lock-options preflight guarding, and
WRR method-status preflight guarding, WRR source-recovery probing, WRR
source-recovery probe guarding, `.shtml` research-source alternate probing,
and hypothesis-testing source-status auditing/guarding, plus WRR
defined-distance diagnostic doc guarding, WRR variant-gap doc guarding, and
WRR variant-gap method-status evidence propagation, WRR source-review queue doc
guarding, WRR D(w) formula sensitivity doc guarding, and WRR source-policy
scenario doc guarding, WRR cross-pair grid doc guarding, and WRR direct
all-lane diagnostic doc guarding, and WRR source visual-review notes doc
guarding, WRR source visual-review row triage refinement, and WRR
source-review queue visual-triage action propagation, with downstream WRR
source-policy and blocker-packet action refresh, and non-exclusion visual
triage fields in the WRR source-review queue, WRR support docs, WRR source
audit, claim catalog, WRR method-status evidence, WRR source-policy scenario
docs, WRR defined pair-set diagnostic docs, WRR cross-pair diagnostics, and
WRR variant residual review-packet guarding, plus WRR residual method-status,
blocker-packet, and unresolved-term burden propagation, and WRR Wayback
source-recovery probing/guarding, English corpus deferred-policy guarding, WRR
public handoff doc guarding, WRR
remaining-lane/source-policy/manual-decision checklist consolidation, and WRR
manual decision-record lock propagation, public-handoff lock-status cleanup,
checklist boundary wording cleanup, public claim-language preflight guarding,
doc-command reference preflight guarding, final-report support-doc reference
guarding, real-report preflight input drift guarding, a clean real-report
protocol rerun/cache check at commit `253b104`, and manual-review packet-shape
drift guarding, plus prospective-readiness, next-lock, and study-lock workflow
doc guard coverage, Greek second-cohort readiness guarding, consolidated
findings prospective-boundary guarding, generated lane-status freshness
guarding, final-report assembly-boundary guarding, final-report highlights
freshness guarding, centered-occurrence index freshness guarding, strongest
candidate deep-dive freshness guarding, claim-catalog summary guarding,
real-report run doc guarding, final-report assembly direct gating,
top-reader summary doc direct gating, prospective workflow direct gating,
public/no-input handoff doc direct gating, imported preflight check-script
input guarding, reader-doc check target consolidation, KJVA source-doc direct
gating,
research missing model pages audit doc guarding, WRR-adjacent source audit
family doc guarding, real-report source-audit preflight documentation,
critical-omission follow-up doc guarding, KJVA apocrypha prospective boundary
and next-replication planning guarding, WRR support-doc local-lock boundary
cleanup plus formal preflight guarding, and WRR source-audit
local-lock boundary guarding, WRR source-audit register refresh,
protocol README WRR handoff-status guarding, WRR exact-gap priority-packet
guarding, WRR source-row coverage packet guarding, WRR source-row crop packet
guarding, WRR source-row crop contact-sheet guarding, WRR source-row OCR word
packet guarding, WRR source-row review bundle guarding, WRR source-row bundle
public-doc synchronization, exact-gap review-rank wording cleanup, and
CSV-backed locks for the WRR exact-gap priority packet, method/pair-universe
evidence packet, remaining-lane evidence packet, and source-row coverage
packet, plus source-row crop packet, contact-sheet image, OCR word packet, and
all-script exact-test and check-script wiring release guards, plus a
metadata-only CrossWire KJVA source-candidate audit, Project Gutenberg
split-source metadata audit, Project Gutenberg heading-level coverage probe,
source-status rollup refresh, and public-reader package handoff export
guarding, Start Here/README reader-link package guarding, and public-reader
package start-list alignment.
The WRR method-lane wide-skip probe is now guarded, included in the real-report
run, carried into the exact-gap/blocker packets, and mirrored in public
reader-facing WRR wording.
The Cities source-row lock evidence packet doc is now CSV/manifest-guarded
against builder row output, summary rows, manifest metadata, no-source-row-use
locks, and source-script leakage.
The Cities unreadable-PDF review doc is now CSV/manifest-guarded against
builder row output, summary rows, manifest metadata, route/next-action drift,
and source-script leakage.
The Cities unreadable-PDF OCR feasibility doc is now CSV/manifest-guarded
against row schema, OCR parameter drift, recomputed summary totals, manifest
metadata, and source-script leakage.
The Cities unreadable-PDF OCR review packet doc is now CSV/manifest-guarded
against packet schema, OCR sidecar path scope, recomputed summary totals,
manifest metadata, and source-script leakage.
The Cities unreadable-PDF OCR review checklist doc is now CSV/manifest-guarded
against checklist schema, contact-sheet path scope, recomputed summary totals,
manifest contact-summary metadata, and source-script leakage.
The Cities unreadable-PDF OCR page-review doc is now CSV/manifest-guarded
against builder-derived decision rows, summary rows, manifest inputs,
no-source-row-use locks, and source-script leakage.
The Cities OCR page-review decision file is now directly guarded against
schema drift, source-row-use drift, source-script text, and missing packet-page
links before page-review output is rebuilt.
`make study-mapping-schemas` now runs the full mapping guard set: generic
schema validation, WRR manual decision records, Cities OCR page-review
decisions, Cities source-row lock decisions, and Cities source-transcription
decision records.
The generic study-mapping schema validator now rejects unexpected columns and
non-ISO `locked_at` dates so populated mapping rows cannot silently drift
outside the locked CSV shape.
`make fast-validate` and `make public-release-check` now run
`make study-mapping-schemas`, so the mapping guard suite is part of both dirty
handoff validation and clean release validation.
`docs/EXPANDED_STRATA_TOOLING.md` now describes the current split between
conservative seed rows and header-only mapping templates instead of implying
all mapping-dependent strata remain empty.
`docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`, `docs/MATCH_TYPE_EXTENSION_STATUS.md`,
and `docs/REAL_REPORT_RUN.md` now use the same study-mapping wording: some
files contain conservative seed rows, others remain header-only, and the
guarded entry point is `make study-mapping-schemas`.
The README and validator docstring now describe current guarded study-mapping
CSV files instead of treating the mapping layer as future-only.
The generic study-mapping validator now also checks author/protagonist scoped
refs: start/end refs must parse, match the declared `book`, and stay in
ascending order within that book.
`scripts/check_study_mapping_term_ids.py` now guards populated
thematic/author/protagonist mapping rows against orphaned term IDs, and the
check is wired into `make study-mapping-schemas`, report preflight, and the
real-report protocol inputs.
`scripts/check_term_files.py` now moves term CSV/schema normalization checks
out of tests alone and into release/report gates: it validates required term
columns, per-file duplicate `term_id` values, supported languages,
normalization-empty rows, meaningful constants, and implemented gematria
schemes before public release or real-report assembly.
`scripts/check_corpus_configs.py` now moves corpus-config TOML shape checks
into release/report gates without requiring ignored/private source files to
exist; it validates config name/language/source tables, supported source
formats, and required CSV/text source fields before public release or
real-report assembly.
`scripts/check_protocol_files.py` now moves protocol TOML schema checks into
release/report gates without running protocols; it loads every tracked protocol
through `els.protocol_runner`, catching bad step shape and duplicate protocol
names before public release or real-report assembly.
The WRR cross-pair grid doc is now CSV/manifest-guarded against grid-shape,
corrected-distance, aggregate, permutation-summary, manifest input/output, and
count drift.
The WRR direct all-lane diagnostic doc is now CSV/manifest-guarded against
cap-250/cap-1000 corrected-distance, aggregate, program-formula, D(w)
sensitivity, manifest input/output, and count drift.
The WRR D(w) formula sensitivity doc is now CSV/manifest-guarded against
sensitivity summary, changed-pair, manifest input/output, and count drift.
The WRR source-policy scenario doc is now CSV/manifest-guarded against
scenario, term-impact, scenario-pair, manifest input/output, and count drift.
The WRR source-review queue doc is now CSV/manifest-guarded against queue row,
summary-bucket, source-flag, visual-triage, manifest input/output, and count
drift.
The WRR source-recovery probe doc is now CSV/manifest-guarded against
live-probe row, summary, source-manifest, and report-manifest drift.
The WRR Wayback source-recovery probe doc is now CSV/manifest-guarded
against archived probe row, summary, and report-manifest drift.
The WRR source visual-review notes doc is now CSV/manifest-guarded against the
source-review queue visual rows, non-exclusion actions, source queue manifest
input/output, and count locks.
The WRR source-row crop contact sheet doc is now CSV/manifest-guarded
against crop-packet row order, summary, manifest, and contact-sheet dimensions.
The WRR source audit doc is now CSV/manifest-guarded against locked-method,
method-status, manual-decision summary, manifest input/output, and count drift.
The Cities PDF recovery probe doc is now CSV/manifest-guarded against recovery
rows, summary counts, usable/unrecovered labels, manifest tool/source/output
metadata, and recovery boundary drift.
The research missing model pages audit doc is now CSV/manifest-guarded against
unusable level-2/3 model-page rows, summary counts, anchor counts, and the
source-status-only claim boundary.
The centered occurrence index doc is now CSV/manifest-guarded against generated
occurrence rows, presence-summary rows, source/type counts, and path metadata.
The final-report highlights doc is now CSV/manifest-guarded against generated
highlight rows, claim-catalog row counts, and report path metadata.
The claim catalog summary doc is now CSV-guarded against catalog fieldnames,
Current Entries group/status/count rows, and blank Current read cells.
The hypothesis-testing source audit doc is now CSV/manifest-guarded against
page rows, summary counts, protocol anchors, report-manifest boundaries, and
source-download metadata.
The critical-omission follow-up docs are now CSV/manifest-guarded against
aggregate break totals, null distribution shape, cross-tradition class/status
counts, length-stratified rows, disputed-passage passage/cohort counts, and
Pericope inverse-check rows.
The Israeli prime-ministers detail recovery probe doc is now CSV/manifest-guarded
against detail-page rows, summary counts, snapshot bytes/checksums, and the
live-source-recovery-only boundary.
Real-report preflight now runs the Israeli prime-ministers detail recovery
probe doc checker, so the redirected-root/no-result boundary is gated before
formal report assembly.
The public-release hygiene CLI now has direct unit coverage for clean/dirty
tree handling, expected GitHub owner/repo checks, and JSON failure payloads.
The CRD relevance-dictionary CLI now has direct unit coverage for reviewed
dictionary acceptance and expected-hash mismatch failures.
The strongest-candidate deep-dive doc is now CSV/manifest-guarded against
candidate row order, candidate ids, source inputs, and report path metadata.
The prospective lane-status doc is now JSON-guarded against tracked lane ids,
statuses, term/protocol/report paths, and status-count drift.
The prospective study-readiness doc is now JSON-guarded against tracked profile
count/status drift in `configs/prospective_study_lanes.json`.
The prospective next-lock, consolidated-findings, and Greek second-cohort
readiness docs now share the same profile count/status snapshot guard.
The source-row review bundle, source-transcription evidence packet,
source-transcription row-review checklist, and remaining-lane review checklist
are now CSV-guarded as well, and the source-transcription evidence packet
rows, row summaries, CSV schemas, and manifest input/output metadata are now
CSV/manifest-guarded. The source-policy review checklist is also
CSV-guarded, and the source-policy evidence packet/context/summary rows,
CSV schemas, and manifest input/output metadata are CSV/manifest-guarded. The
manual decision register/summary/manifest, manual decision-record worksheet,
and exact reproduction gap dashboard are CSV/manifest-guarded too. The
locked-method report is CSV/manifest-guarded too.
WRR claim readiness is CSV/manifest-guarded as well.
WRR lock options are CSV/manifest-guarded as well.
WRR claim blocker packet readiness, source-queue, residual-summary,
remaining-lane inputs, and manifest row-count/input/output metadata are
CSV/manifest-guarded as well.
WRR method status is CSV/manifest-guarded as well.
WRR residual term reconciliation queue rows, summary rows, CSV schemas, and
manifest input/output metadata are CSV/manifest-guarded as well.
WRR residual reconciliation action plan rows, summary rows, CSV schemas, and
manifest input/output metadata are CSV/manifest-guarded as well.
WRR method/pair-universe evidence packet rows, summary metrics, CSV schemas,
and manifest input/output metadata are CSV/manifest-guarded as well.
WRR remaining-lane evidence packet rows, lane summaries, CSV schemas, and
manifest input/output metadata are CSV/manifest-guarded as well.
WRR source-row coverage packet rows, summary metrics, CSV schemas, and
manifest input/output metadata are CSV/manifest-guarded as well.
Cities source-row lock queueing, worksheet generation, evidence-packet
assembly, decision-record preflight guarding, and transcription-review
worksheet generation now keep Cities source-row candidate pages out of
result-bearing work until readable transcription/import records exist.
Cities source-row lock handoff: 14 source-row lock candidate pages, 14 populated
lock rows, and 14 pending transcription-review rows; no source rows imported,
and no city-name normalization, ELS searches, compactness runs, or p-levels.
The Cities source-transcription decision-record file is now preflight-guarded
as schema-only until readable transcription decisions are deliberately locked.
The Cities PDF recovery probe now checks the 35 linked Cities/Aumann/Simon-McKay
PDF URLs in an isolated ignored bundle and records 17 usable archived PDFs plus
18 unrecovered links; the follow-up recovered-PDF text audit classifies those 17
PDFs into 5 extractable rows, 9 zero-text rows, and 3 garbled/non-Latin rows.
The Cities source-review queue now turns all 35 PDF rows into next-action lanes:
5 extractable-text review rows, 9 OCR/image-only rows, 3 encoding-or-OCR rows,
and 18 missing-PDF recovery rows. The extractable-text role review separates the
five readable PDFs into 1 data-bearing candidate, 1 method-context candidate,
and 3 commentary/critique rows; the data-bearing candidate is already covered
by the Gans communities source-shape audit with 66 source records and 210
community rows, without source-row import or result-bearing work. The
unreadable-PDF review now routes the remaining 12 recovered unreadable PDF rows into
9 OCR/image-only rows and 3 encoding-or-OCR candidates, covering 61 pages
without running OCR; the unreadable-review checker locks those rows, route
metadata, summary metrics, and manifest boundaries back to builder output. The
OCR feasibility probe then attempts those 61 pages with local English OCR and
records text signal in 11 rows and 59 pages, without storing OCR text in
tracked files; the OCR-feasibility checker locks the row schema, OCR parameters,
recomputed summary totals, and manifest metadata. The OCR review packet records
61 page rows with local sidecar paths and counts; the packet checker locks the
schema, sidecar path scope, recomputed summary totals, and manifest metadata.
The OCR review checklist groups the 11 packet PDFs into local contact-sheet review
rows; the checklist checker locks contact-sheet path scope, recomputed summary
totals, and manifest contact-summary metadata. The page-image review now
records 61 packet pages, 41 reviewed packet pages, and 20 unreviewed packet
pages; the public handoff names the same coverage as 61 OCR packet pages, 41
reviewed OCR packet pages, and 20 unreviewed OCR packet pages. The page-review
checker locks builder-derived decision rows, summary rows, manifest inputs,
and no-source-row-use boundaries. The source-row lock
queue isolates 14 candidate pages across three labels, the worksheet assigns 14
lock decision ids, and the evidence packet joins those ids to PDF metadata,
checksums, and page-image paths without OCR body text or source-row import; the
evidence packet checker now locks those rows, summary metrics, and manifest
boundaries back to builder output.
This file tracks work that remains outside the deferred copyrighted/private
English CSVs.

## Deferred Inputs

### BibleGateway English Corpora Without Lawful Local Text

The current BibleGateway refresh has 34 available English versions and skips
30 missing local CSVs. Missing rows are listed in:

```text
reports/biblegateway_english_versions/missing_versions.csv
```

AMPC, NLT, MSG, TPT, and NIV local hooks exist and their private CSVs are
ignored under `data/private/english/`. TPT is wired in the private protocol but
is not part of the BibleGateway manifest.

Current policy: what we have is the working set. Do not treat the 30 missing
BibleGateway rows as an active blocker. Only add a missing version when a
lawful source package or user-supplied text with clear permission is available;
do not scrape BibleGateway text to fill these rows.

Bolls currently adds no further missing BibleGateway labels beyond sources
already mapped separately. The Bolls `NASB` package remains tracked as
`NASB1995`; do not silently use it for the current BibleGateway `NASB` row. The
local NASB EPUB is PDF-derived/two-column and is not safe for verse-level CSV
import without a dedicated parser.

## Completed This Pass

### Cities PDF Recovery Probe

Completed isolated live/archive probe:

```bash
python3 -m scripts.run_protocol protocols/cities_pdf_recovery_probe.toml --resume
```

Current result:

- PDF URLs probed: 35.
- Live PDF rows: 0.
- Usable archived PDF rows: 17.
- Unrecovered PDF rows: 18.
- Boundary: recovered PDF bytes are source-shape inputs only; no OCR,
  city-name normalization, ELS search, compactness calculation, or p-level
  verification is performed.
- Guard: `scripts/check_cities_pdf_recovery_probe_doc.py` now locks the
  manifest tool, source glob, output paths, summary values, and recovery
  boundary in addition to key usable/unrecovered rows.

### Cities Recovered PDF Text Audit

Completed source-shape text classification:

```bash
python3 -m scripts.run_protocol protocols/cities_recovered_pdf_text_audit.toml --resume
```

Current result:

- Recovered PDF rows audited: 17.
- Extractable text rows: 5.
- Zero-text rows: 9.
- Garbled/non-Latin extract rows: 3.
- Protocol anchors found: 5 of 5.
- Boundary: this separates source-review shapes only; no OCR, city-name
  normalization, ELS search, compactness calculation, or p-level verification is
  performed.

### Cities Source Review Queue

Completed source-review queue:

```bash
python3 -m scripts.run_protocol protocols/cities_source_review_queue.toml --resume
```

Current result:

- Rows queued: 35.
- Extractable-text review rows: 5.
- OCR/image-only rows: 9.
- Encoding-or-OCR candidate rows: 3.
- Missing-PDF recovery rows: 18.
- Boundary: this is planning metadata only; it does not decide source
  admissibility, create city-name rows, run ELS searches, compute compactness, or
  verify p-levels.

### Cities Extractable Text Review

Completed extractable-text role review:

```bash
python3 -m scripts.run_protocol protocols/cities_extractable_text_review.toml --resume
```

Current result:

- Extractable rows reviewed: 5.
- Anchors found: 5 of 5.
- Data-bearing candidates: 1.
- Data candidates with existing source-shape audit: 1.
- Gans source-shape records: 66.
- Gans community rows: 210.
- Method-context candidates: 1.
- Commentary/critique rows: 3.
- Boundary: this does not import source rows, decide admissibility, normalize
  city names, run ELS searches, compute compactness, or verify p-levels.

### Cities Unreadable PDF Review

Completed unreadable-PDF review:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_review.toml --resume
```

Current result:

- Unreadable rows reviewed: 12.
- OCR/image-only rows: 9.
- Encoding-or-OCR candidate rows: 3.
- Aumann committee rows: 11.
- Other-family rows: 1.
- Pages needing review: 61.
- Boundary: this does not run OCR, repair text, import source rows, normalize
  city names, run ELS searches, compute compactness, or verify p-levels.
- Guard: `scripts/check_cities_unreadable_pdf_review_doc.py` now compares the
  review CSV, summary CSV, and manifest to builder-derived output and fails on
  source-script text or route/next-action drift.

### Cities Unreadable PDF OCR Feasibility

Completed OCR feasibility probe:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_feasibility.toml --resume
```

Current result:

- Rows reviewed: 12.
- Rows with OCR text: 11.
- Pages attempted: 61.
- Pages with OCR text: 59.
- OCR text signal chars: 70207.
- OCR text detected rows: 11.
- Boundary: this does not store OCR text in tracked files, repair text, import
  source rows, normalize city names, run ELS searches, compute compactness, or
  verify p-levels.
- Guard: `scripts/check_cities_unreadable_pdf_ocr_feasibility_doc.py` now
  compares the feasibility CSV schema, recomputed summary rows, and manifest
  parameters to tracked output and fails on source-script text.

### Cities Unreadable PDF OCR Review Packet

Completed OCR review packet:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_review_packet.toml --resume
```

Current result:

- PDF rows: 11.
- Page rows: 61.
- Pages with OCR text: 59.
- Pages without OCR text: 2.
- OCR text signal chars: 70207.
- OCR words: 19434.
- OCR lines: 2322.
- Boundary: this tracks paths/counts/status only. OCR text sidecars and page
  images are ignored local review aids; this does not repair text, import
  source rows, normalize city names, run ELS searches, compute compactness, or
  verify p-levels.
- Guard: `scripts/check_cities_unreadable_pdf_ocr_review_packet_doc.py` now
  compares the packet CSV schema, sidecar path scope, recomputed summary rows,
  and manifest parameters to tracked output and fails on source-script text.

### Cities Unreadable PDF OCR Review Checklist

Completed OCR review checklist:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_review_checklist.toml --resume
```

Current result:

- Checklist rows: 11.
- PDF rows: 11.
- Pages total: 61.
- Pages with OCR text: 59.
- Pages without OCR text: 2.
- OCR text signal chars: 70207.
- OCR words: 19434.
- OCR lines: 2322.
- Label contact sheets: 11.
- Boundary: this creates ignored local contact sheets and review-order rows
  only. It does not track OCR text, repair text, import source rows, normalize
  city names, run ELS searches, compute compactness, or verify p-levels.
- Guard: `scripts/check_cities_unreadable_pdf_ocr_review_checklist_doc.py`
  now compares the checklist CSV schema, contact-sheet path scope, recomputed
  summary rows, and manifest contact-summary metadata to tracked output and
  fails on source-script text.

### Cities Unreadable PDF OCR Page Review

Completed page-image review:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_page_review.toml --resume
```

Current result:

- Packet pages: 61.
- Reviewed packet pages: 41.
- Unreviewed packet pages: 20.
- Review rows: 41.
- Reviewed pages: 41.
- OCR-empty pages reviewed: 2.
- Low-signal pages reviewed: 3.
- Visual-text-present pages: 40.
- Source-row imports: 0.
- Boundary: this records page-image review labels only; no OCR body text,
  repaired text, source-row import, city-name normalization, ELS search,
  compactness calculation, or p-level verification is performed.
- Guard: `scripts/check_cities_unreadable_pdf_ocr_page_review_doc.py` now
  compares page-review rows, summary rows, and manifest inputs to
  builder-derived output and fails on source-script text or source-row use.

### Cities Source Row Lock Queue

Completed source-row lock queue:

```bash
python3 -m scripts.run_protocol protocols/cities_source_row_lock_queue.toml --resume
```

Current result:

- Queue rows: 14.
- Unique labels: 3.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Source-row imports: 0.
- Boundary: this names page locations only and requires a later citable
  source-row lock before any source data can be used.

### Cities Source Row Lock Worksheet

Completed decision worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_row_lock_worksheet.toml --resume
```

Current result:

- Worksheet rows: 14.
- Recorded decision rows: 14.
- Locked decision rows: 14.
- Unrecorded decision rows: 0.
- Source-row imports: 0.
- Boundary: this assigns decision ids and evidence prompts only; it does not
  transcribe rows, import source rows, normalize city names, run ELS searches,
  compute compactness, or verify p-levels.

### Cities Source Row Lock Evidence Packet

Completed evidence packet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_row_lock_evidence_packet.toml --resume
```

Current result:

- Evidence rows: 14.
- Unique labels: 3.
- Table-bearing candidate pages: 4.
- Source-list candidate pages: 5.
- Exception-note candidate pages: 5.
- Recorded decision rows: 14.
- Source-row imports: 0.
- Boundary: this joins decision ids to recovered PDF metadata, checksums, and
  page-image paths only. It does not copy OCR body text, transcribe source rows,
  import source text, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.
- Guard: `scripts/check_cities_source_row_lock_evidence_packet_doc.py` now
  compares the packet CSV, summary CSV, and manifest to builder-derived output
  and fails on source-script text or source-row imports.

### Cities Source Row Lock Decision Record Guard

Completed decision-record preflight guard:

```bash
python3 -m scripts.check_cities_source_row_lock_decision_records
```

Current result:

- Current records file: `data/study/mappings/cities_source_row_lock_decisions.csv`.
- Populated record rows: 14.
- Guarded evidence rows: 14.
- Boundary: populated lock rows must match the evidence packet, use supported
  status/action values, cite evidence, avoid source-script text, and carry ISO
  lock dates before formal report preflight passes.

### Cities Source Transcription Review Worksheet

Completed no-input transcription-review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_transcription_review_worksheet.toml --resume
```

Current result:

- Rows needing transcription review: 14.
- Locked source pages: 14.
- Transcription decision rows recorded: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this organizes locked source pages for future readable
  transcription and row/column alignment review. It does not copy source-script
  text, import source rows, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.

### Cities Source Page Review Bundle

Completed page-image review bundle:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_review_bundle.toml --resume
```

Current result:

- Bundle rows: 14.
- Page images found: 14.
- Page images missing: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this verifies page-image paths and dimensions for later manual
  transcription review. It does not run OCR, copy source-script text, import
  source rows, normalize city names, run ELS searches, compute compactness, or
  verify p-levels.

### Cities Source Page Contact Sheet

Completed local contact sheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_contact_sheet.toml --resume
```

Current result:

- Contact sheet pages: 14.
- Page images found: 14.
- Page images missing: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this renders local page images as a visual review aid. The contact
  sheet is not transcription verification; tracked files contain no OCR body
  text or source-script body text.

### Cities Source Page OCR Review Packet

Completed local Hebrew OCR review packet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_ocr_review_packet.toml --resume
```

Current result:

- Source-page OCR rows: 14.
- Page images found: 14.
- Page images missing: 0.
- OCR pages attempted: 14.
- Pages with OCR text: 14.
- OCR text sidecars: 14.
- OCR Hebrew letters: 14,408.
- OCR words: 3,939.
- OCR lines: 596.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this writes local ignored OCR sidecars for manual review only.
  Tracked files contain counts, paths, and status, but no OCR body text or
  source-script body text. It does not transcribe verified source rows, import
  source text, normalize city names, run ELS searches, compute compactness, or
  verify p-levels.

### Cities Source Page OCR Review HTML

Completed local image/OCR HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_ocr_review_html.toml --resume
```

Current result:

- HTML rows: 14.
- HTML embedded OCR text rows: 14.
- Page images found: 14.
- OCR text sidecars: 14.
- Pages with OCR text: 14.
- OCR Hebrew letters: 14,408.
- OCR words: 3,939.
- OCR lines: 596.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local HTML file may display OCR text beside page
  images for manual review. Tracked files contain no OCR body text or
  source-script body text and still do not transcribe verified source rows,
  import source text, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.

### Cities Source Page Line Crop Packet

Completed local line-crop review packet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_packet.toml --resume
```

Current result:

- Table candidate pages: 4.
- Line crop rows: 203.
- Line crops available: 203.
- TSV sidecars: 4.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: line crops and TSV sidecars are local ignored review aids only.
  Tracked files contain counts, paths, and status, but no OCR body text or
  source-script body text. This does not verify source-row transcription,
  import source text, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.

### Cities Source Page Line Crop Band Map

Completed coordinate-only line-crop band map:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_map.toml --resume
```

Current result:

- Gap threshold: 40 px.
- Band rows: 16.
- Source line rows: 203.
- Unique table pages: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: band grouping uses local crop coordinates only. It does not read
  Hebrew, transcribe rows, import source rows, normalize city names, run ELS
  searches, compute compactness, or verify p-levels.

### Cities Source Page Line Crop Band Review Worksheet

Completed no-input coordinate-band review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_review_worksheet.toml --resume
```

Current result:

- Band review rows: 16.
- Source line rows represented: 203.
- Unique table pages: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this groups the 203 line crops into 16 coordinate-band review
  rows for later visual checking only. It does not read Hebrew, transcribe
  rows, import source rows, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.

### Cities Source Page Line Crop Band Contact Sheets

Completed local coordinate-band contact sheets:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_contact_sheet.toml --resume
```

Current result:

- Band contact sheets: 16.
- Band contact sheets available: 16.
- Band review rows: 16.
- Line crop rows: 203.
- Line crop images found: 203.
- Unique table pages: 4.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local PNG contact sheets group crop images by coordinate
  band only. They do not read Hebrew, transcribe rows, import source rows,
  normalize city names, run ELS searches, compute compactness, or verify
  p-levels.

### Cities Source Page Line Crop Band Review HTML

Completed local coordinate-band HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_review_html.toml --resume
```

Current result:

- HTML rows: 16.
- HTML embeds source text: `false`.
- HTML band image rows: 16.
- Band contact-sheet rows: 16.
- Band contact sheets available: 16.
- Line crop rows: 203.
- Line crop images found: 203.
- Unique table pages: 4.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local HTML displays band contact-sheet images only. It
  does not embed OCR body text or source-script body text, transcribe rows,
  import source rows, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.

### Cities Source Page Line Crop Contact Sheet

Completed local line-crop contact sheets:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_contact_sheet.toml --resume
```

Current result:

- Table pages: 4.
- Line crop rows: 203.
- Line crop images found: 203.
- Contact sheets: 4.
- Contact sheets available: 4.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: contact sheets are local ignored visual aids only. Tracked files
  contain counts, paths, and status, but no OCR body text or source-script
  body text. They do not verify source-row transcription, import source text,
  normalize city names, run ELS searches, compute compactness, or verify
  p-levels.

### Cities Source Page Line Crop Review HTML

Completed local line-crop HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_review_html.toml --resume
```

Current result:

- HTML rows: 203.
- HTML line-crop image rows: 203.
- HTML pages: 4.
- Line crop packet rows: 203.
- Line crop images found: 203.
- Unique table pages: 4.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local HTML file displays line-crop images only and
  embeds no OCR text or source-script text. Tracked files contain counts,
  paths, and status, but no OCR body text or source-script body text. This
  does not verify source-row transcription, import source text, normalize city
  names, run ELS searches, compute compactness, or verify p-levels.

### Cities Source Page Line Crop Triage

Completed no-input line-crop triage queue:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_triage.toml --resume
```

Current result:

- Line-crop triage rows: 203.
- Unique table pages: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this ranks crop images by layout and OCR-count signal only. It
  does not read Hebrew, transcribe rows, import source rows, normalize city
  names, run ELS searches, compute compactness, or verify p-levels.

### Cities Source Page Line Crop Triage HTML

Completed local line-crop triage HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_triage_html.toml --resume
```

Current result:

- HTML rows: 203.
- HTML line-crop image rows: 203.
- HTML priority sections: 4.
- Line-crop triage rows: 203.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local HTML file displays crop images in triage priority
  order only. It embeds no OCR text or source-script text and does not read
  Hebrew, transcribe rows, import source rows, normalize city names, run ELS
  searches, compute compactness, or verify p-levels.

### Cities Source Page Line Crop Priority Contact Sheets

Completed local priority contact sheets:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_priority_contact_sheet.toml --resume
```

Current result:

- Priority contact sheets: 4.
- Priority contact sheets available: 4.
- Line crop rows: 203.
- Line crop images found: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local PNG contact sheets group crop images by triage
  priority only. They do not read Hebrew, transcribe rows, import source rows,
  normalize city names, run ELS searches, compute compactness, or verify
  p-levels.

### Cities Source Page Line Crop Priority Review HTML

Completed local priority HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_priority_review_html.toml --resume
```

Current result:

- HTML rows: 4.
- HTML priority image rows: 4.
- Priority contact-sheet rows: 4.
- Priority contact sheets available: 4.
- Line crop rows: 203.
- Line crop images found: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: the ignored local HTML file displays priority contact-sheet images
  only and embeds no OCR text or source-script text. Tracked files contain
  counts, paths, and status only. This does not read Hebrew, transcribe rows,
  import source rows, normalize city names, run ELS searches, compute
  compactness, or verify p-levels.

### Cities Source Page Line Crop Priority Review Worksheet

Completed no-input priority review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_priority_review_worksheet.toml --resume
```

Current result:

- Priority review rows: 203.
- Unique table pages: 4.
- Priority contact sheets: 4.
- Priority contact sheets available: 4.
- Crop images available: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Dense-text priority rows: 120.
- Medium-text priority rows: 71.
- Short-text priority rows: 12.
- No-text priority rows: 0.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this joins triage rank, crop image paths, and priority contact
  sheet paths for later visual review only. It does not read Hebrew,
  transcribe rows, import source rows, normalize city names, run ELS searches,
  compute compactness, or verify p-levels.

### Cities Source Page Line Crop Review Worksheet

Completed no-input line-crop review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_review_worksheet.toml --resume
```

Current result:

- Line-crop review rows: 203.
- Unique table pages: 4.
- Table-candidate page rows: 203.
- Crop images available: 203.
- OCR words represented by line boxes: 1,511.
- OCR Hebrew letters represented by line boxes: 4,934.
- Source-row imports: 0.
- City-name normalization: 0.
- ELS runs: 0.
- Compactness runs: 0.
- p-levels: 0.
- Boundary: this worksheet organizes visual review only. Tracked files contain
  counts, paths, and status, but no OCR body text or source-script body text.
  It does not verify source-row transcription, import source text, normalize
  city names, run ELS searches, compute compactness, or verify p-levels.

### Locked Report Rerun And Volatility Cleanup

Completed locked reruns:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_claim_followup.toml --resume
python3 -m scripts.run_protocol protocols/doxa_four_source_confirmatory_followup.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_confirmatory.toml --resume
python3 -m scripts.run_protocol protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml --resume
python3 -m scripts.run_protocol protocols/gog_magog_pair_prospective.toml --resume
python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume
```

Guardrails added:

- Doxa four-source report builder now requires explicit
  `--preregistration-commit`, so locked reports do not drift with current
  `HEAD`.
- README Doxa rerun snippets include pinned preregistration commits.
- Gog/Magog prospective tracked report now records generated time in local
  manifests only, not tracked Markdown.
- Stale completed-follow-up sections in extension, pair-baseline, and public
  baseline docs now point to current follow-up reports instead of old rerun
  instructions.

Current pushed commits for this cleanup:

- `5850141` Require locked doxa prereg commits.
- `201a341` Refresh generated indexes.
- `4aac5c1` Stabilize Gog Magog prospective report.
- `bf48336` Update follow-up status docs.
- `d0ff0fb` Add WRR corrected-distance aggregate diagnostic.
- `c421b5d` Add WRR claim readiness gate.
- `fc07423` Link WRR readiness gate in reports.
- `59cce62` Gate WRR claim catalog on readiness.
- `cb24ceb` Require WRR readiness in report preflight.
- `4b792d4` Surface WRR diagnostic in real report run.
- `d23b87d` Refresh WRR status after cross-pair diagnostics.
- `ac86fb5` Refresh all-codes reports with Hebrew theology DB.
- `883458d` Add WRR readiness evidence context.
- `4abb554` Add WRR single-term evidence to final reports.
- `d97f505` Propagate WRR single-term impacts to support docs.
- `097a5e0` Record adjacent Torah-code model sources.
- `1892dad` Refresh remaining work register.
- `920afcf` Update WRR claim catalog status.
- `5472de0` Refresh Greek prospective follow-up status.
- `9372126` Guard Greek prospective report follow-up text.
- `16ce0b7` Refresh Greek follow-up report statuses.
- `09ee224` Fix prospective preregistration checker command.
- `45c4ff6` Refresh SBLGNT source-only follow-up status.
- `7e4f9d6` Refresh Hebrew MT source candidate status.
- `abb499b` Clarify KJVA bridge lock basis.
- `f49521a` Tighten prospective lane validation.
- `1198262` Guard source audit docs in report preflight.
- `2250b7a` Run prospective lane validation in report preflight.
- `980cfb6` Guard completed source basis audit queue.
- `946e76d` Guard English source basis inputs in preflight.
- `dd777bc` Validate source basis audit queue in preflight.
- `381bcfb` Document source basis queue validation.
- `53c51b8` Document formal preflight metadata checks.
- `34ecc61` Wire study tooling checks into report preflight.
- `5782725` Document study tooling preflight coverage.
- `06e77b4` Guard preregistration placeholders in preflight.
- `3f60f7c` Document preregistration preflight guard.
- `8a6139f` Guard CRD relevance lock in preflight.
- `f70b9c6` Document CRD preflight lock guard.
- `021d7f9` List CRD findings in real report scope.
- `d2b3a4e` Refresh CRD report scope status.
- `c8f69b3` Guard manual review queue in preflight.
- `7709397` Document manual review queue guard.
- `4b5d5d5` Refresh manual queue guard status.
- `cd27c3e` Guard WRR readiness doc in preflight.
- `3a4fecc` Document WRR readiness doc guard.
- `40aeb28` Refresh WRR readiness doc guard status.
- `441d429` Guard WRR blocker packet in preflight.
- `061ba7e` Document WRR blocker packet guard.
- `d1aacc2` Refresh WRR blocker packet guard status.
- `123ca07` Guard WRR lock options in preflight.
- `71c6465` Document WRR lock options guard.
- `9c28769` Refresh WRR lock options guard status.
- `c9b1cf3` Guard WRR method status in preflight.
- `2fa41bd` Document WRR method status guard.
- `81cc9a1` Refresh WRR method status guard.
- `bc3e098` Record WRR source redirect metadata.
- `549faf4` Document WRR source recovery probes.
- `44cb7d9` Refresh WRR source recovery status.
- `87636a5` Add WRR source recovery probe.
- `cc1527c` Guard WRR source recovery probe doc.
- `d8864e8` Probe WRR source shtml alternates.
- `2eea419` Refresh WRR source recovery register.
- `60f6ba1` Audit Torah-code hypothesis source pages.
- `2822abe` Guard hypothesis source audit doc.
- `11d22fc` Guard WRR defined diagnostic docs.
- `34c240d` Guard WRR variant gap docs.
- `cb09f08` Surface WRR variant gap method evidence.
- `c94b991` Guard WRR source review queue doc.
- `2a700c8` Guard WRR D formula sensitivity doc.
- `61b8060` Guard WRR source policy scenario doc.
- `bf099f7` Guard WRR cross pair grid doc.
- `96de90a` Guard WRR direct all-lane diagnostic doc.
- `4914f41` Guard WRR source visual notes doc.
- `fb2b54d` Refine WRR visual source triage.
- `2b7022d` Propagate WRR visual triage to source queue.
- `40f2693` Refresh WRR downstream source actions.
- `db8634d` Add WRR visual triage queue fields.
- `b02bb8e` Guard WRR no-input lock posture.
- `80583a7` Guard WRR visual notes as non exclusions.
- `de37840` Surface WRR visual triage in blockers.
- `c336717` Refresh WRR visual triage run summary.
- `c34290b` Sync final reports with WRR visual triage.
- `b4fe347` Document WRR blocker visual triage protocol.
- `98273a8` Guard WRR support visual non exclusions.
- `0cf7727` Guard WRR catalog visual non exclusions.
- `2e56611` Propagate WRR visual boundary to method status.
- `9f40d0d` Guard WRR source policy visual boundary.
- `0423a7c` Guard WRR defined visual non exclusions.
- `77b1fcb` Promote WRR full corrected distance gate.
- `4ffcf8b` Lock WRR cap1000 permutation gate.
- `5984b9a` Clarify WRR locked-method language.
- `f5229d8` Add WRR variant gap upper bound.
- `b8bb1bc` Add WRR residual variant review packet.
- `e2cdd1a` Surface WRR residual packet in method status.
- `470971e` Surface WRR residual caveat in blocker packet.
- `725e251` Add WRR residual burden summary.
- `48fe253` Refresh WRR residual work register.
- `e0aab3c` Add WRR Wayback source recovery probe.
- `2d1bb1d` Add WRR residual term reconciliation queue.
- `d7023d9` Add WRR method pair universe evidence packet.
- `0e994ff` Surface WRR method pair packet in blockers.
- `221a848` Surface WRR source transcription clusters in blockers.
- `f5e167f` Surface WRR near match lane in blockers.
- `222f231` Sync WRR public handoff docs.
- `90fa1e4` Sync WRR final outline handoff.
- `604b215` Guard WRR public handoff docs.
- `7ffd2fb` Add WRR remaining lane checklist.
- `2e214d0` Add WRR source policy checklist.
- `a085cb9` Add WRR manual decision register.
- `03fa42b` Add WRR decision record template.
- `e8db884` Add WRR manual decision record checker.
- `57488b3` Refresh WRR decision record handoff docs.
- `981e5f6` Guard WRR decision record checklist paths.
- `dbe95db` Add WRR decision record worksheet.
- `1bbd2f0` Enforce real report doc reference preflight.
- `057168a` Check real report preflight input drift.
- `3b80047` Guard centered occurrence index doc.
- `259efa3` Guard strongest candidate deep dive doc.
- `94a7622` Guard claim catalog summary doc.
- `ae73a38` Guard real report run doc.
- `8b8655b` Guard preflight check script inputs.
- `d7fd47e` Guard research missing model audit doc.
- `18a8ee1` Refresh register for missing model guard.
- `205028f` Guard adjacent source audit docs.
- `4637e44` Refresh register for source audit guards.
- `f0dbc31` Refresh validation snapshot count.
- `4d9f2c0` Document source audit preflight guards.
- `64cfdf8` Refresh register after source audit guard docs.
- `f870742` Guard critical omission followup docs.
- `9305d12` Document critical omission doc guard.
- `feb53ee` Refresh register for critical omission guards.
- `11a0938` Refresh WRR support docs for locked local method.
- `cd781fa` Refresh register for WRR support docs.
- `51fcee2` Guard WRR support local lock docs.
- `1791867` Refresh register for WRR support guard.
- `75c1948` Guard WRR source audit local lock boundary.
- `bb2abdf` Refresh register for WRR source audit guard.
- `07a5731` Guard protocol README WRR handoff status.
- `83414a0` Add WRR exact gap priority packet.
- `293c3c6` Refresh register for exact gap priority packet.
- `2993acc` Add WRR source row coverage packet.
- `931af3b` Add WRR source row crop packet.
- `76edd71` Add WRR source row crop contact sheet.
- `44fd9af` Add WRR source row OCR word packet.
- `c9bf709` Add WRR source row review bundle.
- `1ed9651` Surface WRR row review bundle in report summary.
- `2dc325c` Sync WRR row review bundle docs.
- `253b104` Clarify WRR gap packet row rank.

### Formal Real Report Rerun

Command completed successfully from the clean committed tree at `253b104`:

```bash
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

Current summary:

- `reports/real_report_run/summary.md`
- summary commit: `253b104`
- preflight status: passed; support-doc reference failures: 0; protocol input
  drift failures: 0.
- local generated report files under `reports/real_report_run/` are ignored by
  Git and record the commit active when the protocol last ran.
- the committed-tree resume reused cached upstream reports and regenerated the
  final summary; slowest top-level steps were preflight, `wrr_audit_counts`,
  `real_report_summary`, and `wrr_cross_pair_grid`, all under 4 seconds.
- after tracked planning-doc commits, rerun
  `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume`
  if exact local manifest-to-HEAD alignment matters.

### Process-Pool Fallback Hardening

Codex sandbox runs exposed macOS/Python process-pool initialization failures on
`os.sysconf("SC_SEM_NSEMS_MAX")`. The affected scripts now fall back to the
same sequential code path when `ProcessPoolExecutor` cannot initialize:

- `scripts/analyze_hebrew_hit_version_presence.py`
- `scripts/analyze_extension_paired_controls.py`
- `scripts/analyze_gog_magog_pairs.py`
- `scripts/analyze_pair_baselines.py`
- `scripts/analyze_apocrypha_bridge_term_shuffled_controls.py`

Current pushed commits for the hardening:

- `f9a0e8d` Fallback when process pool is unavailable.
- `87f8a28` Fallback extension controls without process pool.
- `a1e7d56` Fallback remaining process pools sequentially.
- `ef1db58` Refresh Gog Magog prospective report.

Historical validation after the fallback work, superseded by the latest
validation snapshot under `Validation Commands`:

- `python3 -m pytest -q` passed: 1407 tests, 2 skipped, and 14117 subtests.
- `python3 -m scripts.check_public_release_hygiene --allow-dirty` passed.
- `python3 -m scripts.run_protocol protocols/gog_magog_pair_prospective.toml --resume` passed.
- `python3 -m scripts.run_protocol protocols/kjv_apocrypha_bridge_term_shuffled_controls_1000.toml --resume` passed.
- `python3 -m scripts.preflight_real_report_run` passed at commit `ef1db58`.

### Reader Report Refresh

Current tracked files:

- `docs/FINAL_REPORT.md`
- `docs/CONSOLIDATED_FINDINGS.md`
- `docs/FINAL_REPORT_OUTLINE.md`

Completed in this pass: refreshed stale centered-occurrence counts to the
current `docs/CENTERED_OCCURRENCE_INDEX.md` snapshot:

- 812 presence rows.
- 809 Bible presence rows.
- 3 control presence rows.
- 923 raw occurrence rows.
- 526 centered-self exact-word presence rows.

Also replaced stronger conclusion-language wording in these reader-facing docs.

### Claim-Language Hygiene

Goal: keep every public-facing file aligned with current status:

- occurrence finding
- review candidate
- post-screen confirmatory review candidate
- controlled review candidate
- under-specified
- not claim

Hygiene command:

```bash
python3 -m scripts.check_public_claim_language
```

Expected result: no unsupported public-facing reader-doc hits. Fenced code
examples are ignored by the checker.

### Doc Command Reference Hygiene

Goal: keep documented commands and source-path references executable from the
public checkout.

Hygiene command:

```bash
python3 -m scripts.check_doc_command_references
```

Expected result: no missing documented script modules, protocol/config/term
files, mapping CSVs, or unmarked report references. This check now runs inside
the formal real-report preflight.

### WRR Method-Lane Wide-Skip Probe

Current tracked files:

- `scripts/analyze_wrr_method_lane_wide_skip.py`
- `scripts/check_wrr_method_lane_wide_skip_probe_doc.py`
- `protocols/wrr_method_lane_wide_skip_probe.toml`
- `docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md`
- `reports/wrr_1994/wrr_method_lane_wide_skip_probe.csv`
- `reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv`

Completed in this pass: probed the 11 OCR-matched WRR method/pair-universe
terms through skip 5000 in ordinary Koren Genesis ELS search. The result is 0
total hits through skip 5000; all 11 terms remain zero-hit. This is now carried
into the claim-blocker packet, exact-gap priority packet, consolidated
findings, claim catalog, final report, start-here doc, real-report run doc,
public reader package, real-report protocol, and real-report preflight.

Boundary: the wide-skip probe is diagnostic only. It does not choose source
corrections, method changes, replacement spellings, or pair exclusions. Exact
published WRR reproduction remains caveated by the 163-distance gap.

## Highest-Value Non-Blocked Work

### 1. WRR Reproduction Upgrade

Current status: source/import work, corrected-distance diagnostics, a
pair eligibility table, source-policy scenario diagnostics, populated manual
decision records, a claim-readiness gate, and a locked local reporting path.
The selected repo-defined path keeps all imported same-record pairs, uses the
printed WRR `D(w)` formula as the main rule, carries the reported-program
formula as sensitivity output, treats undefined corrected-distance rows as
ordinary-not-valid, and locks the cap-1000 999,999 date-label permutation.

Remaining exact-published-reproduction pieces:

- source-defined 163-distance reconciliation remains caveated; the repo treats
  `163` as a cited corrected-distance output count rather than a raw pair
  table;
- current manual records selected 26 `no_source_change` rows and 11
  `method_lock` rows, so source edits are not pending under current evidence;
- single-term Zacut diagnostics show `ZKWTA`, `ZKWTW`, `M$HZKWTA`, and
  `M$HZKWTW` each individually leave 163 >=5 pairs with gap 0 if excluded, but
  that remains diagnostic count evidence only;
- exact published `Q`, corrected-distance, and permutation procedure matching
  remains separate from the repo-defined locked local run;
- study-level report language must keep exact-WRR reproduction caveats attached
  to fixed terms and sources.

Current guard: `scripts/check_public_claim_language.py` now rejects public
exact-published WRR overclaim phrases that assert reproduction or closure,
while allowing caveated gap language and forbidden-wording lists.

Tracked references:

- `docs/WRR_REPLICATION_PLAN.md`
- `docs/WRR_METHODOLOGY_GAPS.md`
- `docs/WRR_CORRECTED_DISTANCE_NOTES.md`
- `docs/WRR_CLAIM_READINESS.md`
- `docs/WRR_CLAIM_BLOCKER_PACKET.md`
- `docs/WRR_LOCKED_METHOD_REPORT.md`
- `docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md`
- `docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md`
- `docs/WRR_LOCK_OPTIONS.md`
- `reports/wrr_1994/wrr2_pair_eligibility_table.csv`
- `reports/wrr_1994/wrr_source_policy_term_impacts.csv`
- `tests/test_wrr_stats.py`

Recent source-audit follow-up added a Torah-code.org geometric level-1
simulation harness and an ELS/cylinder level-1 analogue:

- `scripts/simulate_torah_code_research_model.py`
- `scripts/simulate_torah_code_research_els_model.py`
- `protocols/torah_code_research_geometric_model.toml`
- `docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md`
- `docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md`

The Gans/Inbal/Bombach communities data source now has a source-shape audit:

- `scripts/analyze_gans_communities_source.py`
- `protocols/gans_communities_source_audit.toml`
- `docs/GANS_COMMUNITIES_SOURCE_AUDIT.md`

The American presidents data/rule source also has a source-shape audit:

- `scripts/analyze_american_presidents_source.py`
- `protocols/american_presidents_source_audit.toml`
- `docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md`

The Witztum Genesis birth-date source has a source-shape audit:

- `scripts/analyze_witztum_birth_dates_source.py`
- `protocols/witztum_birth_dates_source_audit.toml`
- `docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md`

The Israeli prime-ministers source has a source-shape audit:

- `scripts/analyze_israeli_prime_ministers_source.py`
- `protocols/israeli_prime_ministers_source_audit.toml`
- `docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md`

The Cities/Aumann/Simon-McKay source chain has a source-shape audit:

- `scripts/analyze_cities_source_chain.py`
- `protocols/cities_source_chain_audit.toml`
- `docs/CITIES_SOURCE_CHAIN_AUDIT.md`

The Sons of Haman, Pumbedita, Auschwitz, and Ark source pages have a
source-shape audit:

- `scripts/analyze_event_object_experiments_source.py`
- `protocols/event_object_experiments_source_audit.toml`
- `docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md`

The Chumash, Twin Towers, Tsunami, Katrina, Great Rabbis, and Son Rabbis
placeholder pages have a source-status audit:

- `scripts/analyze_under_construction_experiments_source.py`
- `protocols/under_construction_experiments_source_audit.toml`
- `docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md`

The Torah-code.org hypothesis-testing overview and linked subpages have a
source-status audit:

- `scripts/analyze_hypothesis_testing_source.py`
- `protocols/hypothesis_testing_source_audit.toml`
- `docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md`

The Bombach/Gans co-linear ELS/verse paper and attachment files have a
source-shape audit:

- `scripts/analyze_colinear_els_source.py`
- `protocols/colinear_els_source_audit.toml`
- `docs/COLINEAR_ELS_SOURCE_AUDIT.md`

The co-linear ELS source audit confirms the paper PDF, 8 linked attachment
PDFs, 515 attachment pages, 6 attachments with explicit row-count expectations,
8,260 expected and observed source rows, 6,060 raw PLS pair rows extracted from
the PLS PDF, 12,830 raw roots rows extracted from the roots PDF, 1,698 raw
all_1698 phrase/verse rows extracted from the all_1698 PDF, 502 raw reviewed
subset rows extracted from the four reviewed subset PDFs, 7 Hebrew-method
appendix anchors, and 21/21 protocol anchors. The
communities audit confirms 66 data records and 210 machine-readable pre-filter
community rows. The presidents audit confirms 42 data records and 279
machine-readable spelling rows. The birth-date audit confirms two S1/S2
tables, 14 rows per table, and 51 date forms per table. The Israeli
prime-ministers audit confirms 12 PDF rows, 43 machine-readable PDF keyword
rows, and 8 downloaded detail-page rows, leaving a 4-page detail-source coverage
gap. The isolated Israeli prime-ministers detail-page recovery probe checks the
current live `_9` through `_12` URLs and confirms 0 usable recovered detail
pages because all four redirect to the Torah-code root with spam-root markers.
The Cities audit confirms 13 source-chain files,
6 `.pdf`-named HTML wrappers, 5 Wayback job-failed wrappers, 1 parse-error PDF,
1 no-text PDF, and 7/7 source anchors. The event/object audit confirms 8 source
files, 20 Pumbedita rows, 32 Auschwitz rows, 12 Sons-of-Haman keyword rows, 1
Auschwitz topic row, 65 machine-readable source rows, a 57-page Ark tutorial
PDF, one reported significant follow-up page, two reported non-significant
pages, and one under-construction page.
The under-construction audit confirms six placeholder pages, no PDF data links,
four copied-title mismatches, and the Katrina page mislabeled as Tsunami.
The hypothesis-testing source audit confirms four hypothesis-testing URLs now
redirect to the Torah-code root, share the same spam-root hash prefix
`d60a59519b55bcff`, contain no expected labels, and provide zero usable method
source pages in the current live crawl.
The missing-model-pages audit confirms that four linked Torah-code.org
level-2/3 geometric and ELS model pages currently download as root-canonical
pages with unrelated slot/gambling content, no expected model labels, and zero
usable model pages. The adjacent level-1 geometric and ELS model pages are
usable source context, but they do not supply the missing level-2/3 rules.
The WRR source downloader now supports targeted `--label` refreshes and records
requested URL, final URL, redirect status, HTTP status, bytes, and hash in the
source manifest. A local targeted refresh can check source recovery without
overwriting the whole ignored source bundle.
The isolated WRR source recovery probe now refreshes selected Torah-code
research labels into `reports/wrr_source_recovery_probe/` and writes
`docs/WRR_SOURCE_RECOVERY_PROBE.md`, so live recovery checks no longer risk
overwriting cached `reports/wrr_1994/` source files. The current live probe
checks the same 18 research URL variants used by the Wayback probe, including
stale-indexed `.shtml` alternates, and finds 18/18 selected research URLs
redirecting to the Torah-code root, 18/18 root canonical rows, 18/18 unrelated
slot/gambling-marker rows, and zero usable current source rows.
The WRR Wayback source recovery probe now checks archived Torah-code research
snapshots in `reports/wrr_wayback_source_recovery_probe/` and writes
`docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md`. The current archive probe checks
18 URL variants across 9 research concepts, checks 13 rows with an exact-URL
CDX fallback when the closest-snapshot endpoint has no row, finds zero CDX
candidate rows, recovers no sources through that fallback, recovers 5 usable
archived concepts total (`research_program_1`, `research_program_2`,
`model_overview`, `geometric_model_level_1`, and `els_model_level_1`), and
leaves 4 concepts missing (`geometric_model_level_2`,
`geometric_model_level_3`, `els_model_level_2`, and `els_model_level_3`).
These lanes stay non-result-bearing. The
research-program ELS harness now includes a split-fit Fisher order-statistic
row plus two transparent row-width modes: strict shared-intersection
candidates and broader combined WRR-series candidates. Next research-program
upgrade: recover a citable fuller source-method reconstruction and
source-published Fisher weights if available; only then consider real
Torah-code source data, communities compactness runs, American-presidents
transliteration experiments, or Witztum birth-date ELS/SL-proximity tests. Do
not run an Israeli prime-ministers result protocol until the missing
detail-page coverage is resolved from usable source pages or explicitly scoped
out in a new preregistration. Do not import Cities city-name rows until the wrapped or
missing PDF sources are recovered, or the usable HTML-only source boundary is
explicitly locked. Do not promote the event/object pages beyond source-shape
status until each lane has its own preregistered term normalization and
control design. Do not use under-construction placeholder pages as data-bearing
protocols unless future source recovery finds real data pages. Do not use the
four level-2/3 research model downloads as method sources unless clean
Torah-code pages are recovered and checksummed. Do not promote the co-linear
ELS/verse source lane until Hebrew term/root normalization, verse-link scoring,
and controls are preregistered separately.

WRR aggregate work now has a diagnostic P1..P4 bridge:

- `scripts/analyze_wrr_corrected_distance_aggregate.py`
- `reports/wrr_1994/wrr2_corrected_distance_aggregate.csv`
- `scripts/check_wrr_claim_readiness.py`
- `docs/WRR_CLAIM_READINESS.md`

Current read: the length-5..8 direct-search corrected-distance smoke output has
28 defined `c(w,w')` values at cap 250 and 46 defined values in the cap-1000
split diagnostic, so P1..P4 diagnostic rows now populate. The cross-pair matrix
now has legacy cap-250 diagnostics plus a locked local cap-1000 keep-all
999,999-permutation run. The locked local run has 182 observed rows, 72 defined
`c(w,w')` values, and Bonferroni rho0 `0.000404`. The readiness gate now allows
repo-defined locked-method language while exact published WRR reproduction
remains caveated by the source-defined 163-distance gap with current manual
source records locked unchanged.

All-lane diagnostic follow-up now exists:
`protocols/wrr_corrected_distance_direct_all_lanes.toml` and
`docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md`. It defines 50 values at cap 250 and
72 at cap 1000 over all 182 imported same-record pairs, still far below the
source-cited 163 defined second-list distances. The tracked protocol now also
runs the cap-1000 reported-program `D(w)` formula sensitivity check; it changes
0 pair rows versus the printed-formula diagnostic.
`docs/WRR_DEFINED_PAIR_SET_AUDIT.md` now joins those outputs back to
candidate-lane, review-status, and WNP-Zacut labels: best current direct run
defines 72 of 163, leaving a 91-distance gap, with ordinary-not-valid rows as
the dominant missing mass.
`docs/WRR_DEFINED_GAP_REASON_AUDIT.md` now classifies that missing mass: in the
best cap-1000 run, 83 rows lack appellation ordinary hits, 12 lack date
ordinary hits, 15 lack both, and 0 are under-minimum perturbation cases. The
method-status matrix now also surfaces the variant-gap impact over those
blocked pairs: in the best cap-1000 run, 51 blocked pairs have all blocking
terms with simple variant leads, 9 have partial variant leads, and 50 have no
simple variant lead. `docs/WRR_VARIANT_GAP_UPPER_BOUND.md` now records the
simple-variant upper bound: even if every fully covered simple variant lead
were valid source evidence, the best current run would rise only from 72 to
123 defined distances, leaving a residual gap of 40 to the source-cited 163.
`docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md` and
`docs/WRR_CLAIM_BLOCKER_PACKET.md` now keep that residual caveat visible: the
residual pool has 59 candidate pairs, the deterministic minimum frontier has
40 rows, and the frontier breaks down to 31 no-simple-variant rows plus 9
partial-simple-variant rows. The residual unresolved-term burden is entirely
on appellation terms in this pass: 45 not-matched/no-variant-lead rows, 11
matched/no-variant-lead rows, 3 near-match/no-variant-lead rows, and one
`wnp_chelm_spelling_context` flag. The blocker packet now also embeds the
residual unique-term queue summary, top term targets, source-transcription row
cluster summary, page-image near-match lane, and method/pair-universe summary,
so the no-input handoff carries the pair-level residual caveat, term-level
review frontier, row-level review order, and page-image review boundary. Its
checker now also locks manifest counts, inputs, and outputs.
`docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md` now collapses that pair-level
packet into 58 unique unresolved appellation terms, preserving 59 residual pair
links and 40 minimum-frontier links. The unique-term reconciliation queue
classifies 43 terms as source-transcription/row-alignment review, 11 as
method-or-pair-universe review, 3 as page-image near-match review, and 1 as
source-policy/pair-rule review (`wrr2_32_app_05`, `$LMHMX@LMA`,
`wnp_chelm_spelling_context`).
`docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md` now converts those classes
into no-input evidence lanes: 1 source-policy/pair-rule target, 43
source-transcription/row-alignment targets, 3 page-image near-match targets,
and 11 method/pair-universe targets. It keeps all terms in the working source
until citable row, policy, or method evidence is locked.
`docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md` now handles the source-policy lane
for Chełm: 1 priority term, 2 related source-review rows, 4 scenario-pair rows,
and 3 WNP context blocks, with no automatic correction or exclusion.
`docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md` keeps that Chełm
source-policy/pair-rule target as a review lane, preserving required
decision-record fields without selecting source edits, method changes, or pair
exclusions. Its checker now also locks CSV fieldnames plus manifest counts,
inputs, and outputs.
`docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md` now handles the main
source-transcription lane: 43 action terms, 44 residual pair links, 35
minimum-frontier links, and 22 row clusters, with row 06 first at 4 frontier
terms.
`docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` keeps those 22 row
clusters in review order, preserving required decision-record fields without
selecting row transcriptions, corrections, exclusions, or method changes. Its
checker now also locks CSV fieldnames plus manifest counts, inputs, and
outputs.
`docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md` now joins that row checklist to
current source-queue visual notes: the current source-transcription action
terms have 0 direct visual-note coverage, 4 rows have related row-level visual
triage only, and 18 rows have no related visual triage. It keeps the boundary
that related visual notes cannot be transferred to action terms and no source
change is selected.
`docs/WRR_SOURCE_ROW_CROP_PACKET.md` now generates ignored local review crops
for all 22 source-transcription rows from the Table 2 page render: 22 auto row
crops are available, 4 checklist rows also had existing manual crop files, and
the packet keeps crop availability separate from transcription verification or
source decisions.
`docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md` now generates one ignored local
contact-sheet image with all 22 source-row crops in review order, so manual
inspection can use one file while the repo still records that the sheet is only
a visual aid and not transcription verification.
`docs/WRR_SOURCE_ROW_CROP_REVIEW_HTML.md` now writes an ignored local HTML page
for those 22 generated source-row crops. It displays crop images only and
tracks 22 HTML rows, 22 image rows, 4 existing manual-crop rows, 43 action
terms, and 35 frontier-pair links without embedding OCR body text or
source-script text, and without selecting row transcriptions, source
corrections, pair exclusions, or method changes.
`docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md` lists current Table 2 OCR words by
source-row crop band and expected name/date column: 22 rows have OCR words,
19 rows touch minimum-frontier pairs, and 76 words fall below the local
confidence threshold. It keeps OCR words as review aids only, not source
transcriptions or source decisions.
`docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md` now handles the two remaining
residual lanes: 3 page-image near-match terms and 11 method/pair-universe
terms, preserving the no-correction boundary until page-image, method, or
pair-universe evidence is locked.
`docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` keeps those 14 remaining-lane
terms in page-image and method/pair-universe review lanes, preserving required
decision-record fields without selecting source edits, method changes, or pair
exclusions. Its checker now also locks CSV fieldnames plus manifest counts,
inputs, and outputs.
`docs/WRR_MANUAL_DECISION_REGISTER.md` consolidates all 37 manual-decision
inventory rows: 1 source-policy/pair-rule row, 22 source-transcription row
clusters, 3 page-image near-match rows, and 11 method/pair-universe rows. It
represents 58 action terms, 59 residual pair links, and 40 minimum-frontier
pair links without selecting source edits, row transcriptions, method changes,
or pair exclusions. Its checker now locks register/summary schemas plus
manifest inputs, outputs, and aggregate counts.
`data/study/mappings/wrr_manual_decision_records.csv` now records all 37
current locks: 26 `no_source_change` rows and 11 `method_lock` rows.
`scripts/check_wrr_manual_decision_records.py` keeps each populated row aligned
to the current manual decision register by rank, lane, state, target, and
checklist, and requires non-placeholder evidence plus an ISO lock date.
`docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md` now gives the exact `decision_id`,
rank, lane, state, target, checklist, current record status, selected action,
and evidence prompt for all 37 lock rows.
The locked record status still means no source correction, row transcription,
replacement lock, or pair exclusion has been selected.
`docs/WRR_LOCKED_METHOD_REPORT.md` is now the compact local locked-method
summary: keep_all_working_source, printed `D(w)` main, reported-program
`D(w)` sensitivity, 182 observed rows, 72 defined `c(w,w')` values, and
`rho0 = 0.000404`, with exact published reproduction caveats attached. Its
checker now locks report CSV schema plus manifest inputs, outputs, and counts.
`docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md` now maps the exact-published
gap: 163 source-cited defined distances vs 72 current defined distances, simple
variant residual gap 40, and post-lock reporting boundary without selecting
source changes.
`docs/WRR_EXACT_GAP_PRIORITY_PACKET.md` now ranks the current no-input
evidence lanes for that 91-distance gap: 1 source-policy/pair-rule term, 43
source-transcription/row-alignment terms across 22 row clusters, 3 page-image
near-match terms, and 11 method/pair-universe terms. It is guarded in
real-report preflight and does not select source corrections, pair exclusions,
replacement spellings, or method changes.
`docs/WRR_POST_LOCK_REPORTING_BOUNDARY.md` now records the post-lock language
boundary: local locked-method wording is allowed with caveats, exact published
WRR reproduction wording remains forbidden, all 37 current manual records are
locked, no source changes are selected, and the 91-distance gap remains
exact-reproduction work rather than pending source-edit work.
`docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md` now splits out the 11
method-lane terms: all are OCR-matched, all have zero skip-250 appellation
counts, all have zero high-cap appellation ordinary hits, and 2 pairs have zero
ordinary hits on both sides.
`docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md` now extends those 11 OCR-matched
method-lane terms through skip 5000 and finds 0 ordinary Genesis hits, so the
method lane is not explained by a small skip-cap extension.
The exact-gap priority-packet checker now validates CSV fieldnames, summary
metrics, review lane rows, and manifest inputs/outputs in addition to doc
prose. The method/pair-universe checker now validates CSV fieldnames, summary
metrics, expected term sets, zero variant leads, no-input boundaries, and
manifest inputs/outputs. The remaining-lane evidence checker now validates CSV
fieldnames, lane summaries, expected term sets, zero variant leads,
no-input boundaries, and manifest inputs/outputs before real-report preflight
can pass.
The source-row coverage checker now validates CSV fieldnames, summary metrics,
22-row rank sequence, 43 action-term total, 35 frontier-pair total, 0 direct
visual-action terms, 4 related-only rows, 18 no-related rows, no-input
boundary, and manifest inputs/outputs before real-report preflight can pass.
The source-row crop checker now validates its CSV summary, 22 available auto
crops, contact-sheet availability, 4 manual-crop rows, 43 action terms, 35
frontier pairs, CSV fieldnames, crop-status rows, crop dimensions, crop path
scope, no-input boundary, and manifest inputs/outputs plus contact-sheet
dimensions before real-report preflight can pass.
The source-row crop contact-sheet checker now validates the tracked doc plus
the local PNG header/dimensions (`1930 x 1742`) so stale or missing visual aids
fail preflight instead of only prose drift.
The source-row OCR word checker now validates its CSV summary and packet rows:
22 rows with tokens, 19 frontier rows, 337 OCR words, 972 normalized Hebrew OCR
letters, 78 low-confidence words, CSV fieldnames, crop path scope, no-input
boundary, and manifest inputs/outputs before real-report preflight can pass.
The residual reconciliation action-plan checker now validates CSV fieldnames,
rank sequence, lane totals, zero variant leads, no-input boundaries, and
manifest inputs/outputs before real-report preflight can pass.
The residual term reconciliation queue checker now validates CSV fieldnames,
priority sequence, summary key totals, reconciliation-need totals, priority-one
source-policy row fields, zero variant leads, and manifest inputs/outputs
before real-report preflight can pass.
The source-policy evidence packet checker now validates packet, context, and
summary CSV fieldnames and rows, WNP context refs, scenario-pair counts,
decision boundaries, and manifest inputs/outputs before real-report preflight
can pass.
The source-row review-bundle checker now validates CSV fieldnames, summary
metrics, and packet rows: 22 review clusters, 19 frontier rows, 43 action
terms, 44 residual links, 35 frontier links, 22 generated crops, 22 OCR-word
rows, 337 OCR words, 78
low-confidence OCR words, review-state locks, allowed no-input action, term
counts, crop path scope, no-input boundary, and manifest inputs/outputs before
real-report preflight can pass.
The source-transcription evidence checker now validates packet and row-summary
CSV fieldnames, rank sequences, 43 action terms, 44 residual links, 35
frontier links, 22 row clusters, row-OCR nonmatches, zero variant leads,
evidence/no-input boundaries, and manifest inputs/outputs before real-report
preflight can pass.
`scripts/check_wrr_public_handoff_docs.py` now guards the README, report-run
doc, final report files, consolidated findings, claim catalog, start-here doc,
outline, remaining-work register, and protocol README against stale WRR blocker
or method-lane wide-skip wording. It is wired into report preflight and treats
public handoff drift as a formal preflight failure.
`docs/WRR_NO_INPUT_HANDOFF_STATUS.md` now consolidates that WRR state into 9
handoff rows, 8 manual-input-needed rows, the 163 vs 72 defined-distance gap,
37 manual-decision rows, and a no-new-result boundary. The next WRR work is
therefore source/term/pair-rule reconciliation plus method and pair-universe
decisions before any exact published reproduction language.

### 2. Source-Basis Audit Queue

The English manifests already track broad source-basis metadata:

- `ot_basis`
- `nt_basis`
- `source_family`
- `basis_status`

Rows with `basis_status=needs_audit` should stay coarse until publisher
introductions or official source notes are checked. Do not upgrade them to
edition-level textual-critical claims from memory.

Current queue after the BibleGateway/eBible audit pass:

- BibleGateway English versions: 0 `needs_audit`, 64 `broad_tradition`.
- eBible English controls: 0 `needs_audit`, 44 `broad_tradition`.
- Door43 English controls: 0 `needs_audit`, 2 `broad_tradition`.
- OET English controls: 0 `needs_audit`, 2 `broad_tradition`.
- OTB English controls: 0 `needs_audit`, 1 `broad_tradition`.
- Open.Bible English controls: 0 `needs_audit`, 4 `broad_tradition`.
- Original Douay-Rheims English controls: 0 `needs_audit`, 1
  `broad_tradition`.
- Supplemental open English controls: 0 `needs_audit`, 20 `broad_tradition`.
- eBible rows moved to broad grouping: `ASVBT`, `BSB`, `E2T`, `FBV`, `F35`,
  `LSV`, `MSB`, `OURB`, `OEBCW`, `OEB`, `BBE`, `NOY`, `PEV`, `T4T`, `ULB`,
  and `OJB`.
- BibleGateway rows moved to broad grouping in the second audit pass include
  `AMP`, `AMPC`, `CJB`, `CEV`, `DLNT`, `ERV`, `EASY`, `EXB`, `GW`, `ICB`,
  `ISV`, `JUB`, `PHILLIPS`, `MSG`, `MOUNCE`, `NOG`, `NCB`, `NCV`, `NLV`,
  `NTFE`, `VOICE`, and `WE`.
- `PEV` license metadata corrected to CC BY-SA 4.0; local source package says
  the translation used Hebrew and Greek language study aids but not exact
  editions. `E2T`, `FBV`, `F35`, `LSV`, `OURB`, `T4T`, and `ULB` were added
  as CC BY-SA 4.0 eBible controls; keep exact source-edition claims coarse
  unless publisher notes state more. `FBV` now imports as a 66-book local USFM
  package, so it is tracked as a full English control rather than NT/Psalms
  partial.
- Remaining downloadable English-ish eBible rows checked in this pass were not
  added as open controls when their eBible details page used NC/ND, ND-only, a
  custom non-open permission statement, non-redistributable status, or a
  non-English language code. Examples include `engaoi`, `engbarkly`,
  `engbarkley`, `engemtv`, `eng-glw`, `engnna`, `engwyc2017`, `engwyc2018`,
  `engerv`, `enggw`, `engnet`, and `ubu-nopenge`.
- OET-LV and OET-RV are tracked as separate CC BY-SA 4.0 open controls using
  the OET cleaned USFM repository files. Keep both as broad controls, not
  edition-level manuscript witnesses.
- OTB English UK is tracked as a CC BY-SA 4.0 open control using the
  repository `lang/en-GB` JSON files. Upstream does not state the
  manuscript/source-text basis, so use it as an English surface control only.
- Open.Bible AFINT English NT controls are tracked as CC BY-SA open controls
  using product-page USFM downloads. Upstream does not state the Greek
  manuscript/source-text basis, so use them as English surface controls only.
- Original Douay-Rheims 1609/1582 is tracked as a CC0 English control using
  the GitHub repository's USFM files. Use it as a historical Latin Vulgate-line
  English control, not as a Greek/Hebrew manuscript witness.
- Supplemental open controls track AKJV from the official public-domain text
  ZIP, CPDV from CrossWire's public-domain source archive, Anderson 1864 from
  BibleCorps public-domain source text, AV1611, AV1811, and DRC1750 from BibleCorps
  public-domain source archives, and DEB/PET from BibleCorps CC BY-SA source
  archives. They also track OpenEnglishBible base-text USFM rows for Kent
  Hosea, McFadyen Psalms/Proverbs, Moffatt OT portions, and TCNT 1904. The OEB
  repository marks these files freely distributable; keep them as broad surface
  controls, not edition-level manuscript witnesses.
- Zefania/CrossWire public-domain supplemental controls now add ACV, NHEB,
  Rotherham, Montgomery, Etheridge, Weymouth, Tyndale, and RWebster. CrossWire
  module pages identify these modules as public-domain English texts; keep them
  as broad English surface controls unless exact source-edition details are
  stated by the module page. Etheridge is a Syriac/Peshitta-line English NT
  control, Tyndale is a partial historical English control, and RWebster is a
  KJV/Webster-line revision control. The NHEB Zefania source tags 1 Kings with
  a bad `bnumber`; the importer uses `bsname=1Ki` to recover the canonical book
  code. The Montgomery source uses `Phi` for Philemon, so the importer prefers
  numeric book codes when source short/name metadata agrees with the numeric
  code.
- Additional BibleCorps sources checked but left out for now: GTP front matter
  identifies CC BY-ND 4.0 despite the repository name, LEB has custom
  distribution/reporting restrictions, and AV2023 is a duplicate Gutenberg KJV
  package with non-biblical trailing text in the final imported verse.
- Open.Bible English API search was rechecked after AFINT import. The remaining
  text rows are either already represented by eBible controls, marked NC/ND or
  ND, a non-meaningful DBL test version, or mixed-license enough to leave out
  for now.
- `BBE` and `NOY` moved to broad grouping only. `BBE` has broad Hebrew/Greek
  source evidence; `NOY` NT title metadata identifies Tischendorf's Greek text.
- No English source-basis rows remain in `needs_audit`.

Suggested local queue command:

```bash
awk -F, 'NR == 1 || /needs_audit/' configs/biblegateway_english_versions.csv configs/ebible_english_controls.csv configs/door43_english_controls.csv configs/oet_english_controls.csv configs/otb_english_controls.csv configs/openbible_english_controls.csv configs/odr_english_controls.csv configs/supplemental_english_controls.csv
```

### 3. English Seed Survivor Gate

Current status: no English seed rows survive the 100-sample corpus-letter
shuffle gate after the 34-version BibleGateway refresh.

Current gate files:

- `reports/english_seed_shuffle_followup_100/summary.csv`
- `terms/english_seed_followup_survivors.csv`
- `docs/ENGLISH_SEED_SHUFFLE_FOLLOWUP_REPORT.md`

Leave these downstream survivor protocols idle unless
`terms/english_seed_followup_survivors.csv` has data rows:

```bash
python3 -m scripts.run_protocol protocols/english_seed_term_shuffle_1000.toml --resume
python3 -m scripts.run_protocol protocols/english_seed_survivor_audit.toml --resume
python3 -m scripts.run_protocol protocols/english_seed_paired_controls_1000.toml --resume
```

Current guard: `scripts/check_english_seed_survivor_gate.py` now validates the
empty survivor CSV, the non-surviving 100-sample follow-up p-value, and the
idle downstream term-shuffle, survivor-audit, target-summary, and paired-control
outputs before real-report preflight can pass.

### 4. Apocrypha/Deuterocanon Prospective Study

KJVA bridge results are strong post-screen review material, not claims.
The KJVA prospective lane used a preregistration/protocol/term-file lock before
producing result-bearing outputs:

- `terms/kjv_apocrypha_bridge_prospective_terms.csv`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md`
- `protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md`
- `protocols/kjv_apocrypha_bridge_prospective_nonbible_controls.toml`

Boundary note: this older lane does not have a
`reports/study_locks/*.manifest.json` or preflight sidecar. Its negative result
can be rerun for reproducibility, but any future KJVA bridge follow-up should
use the current full study-lock-manifest and preflight workflow before
producing new result-bearing output.

Candidate inputs:

- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`
- `terms/kjv_apocrypha_bridge_confirmatory_terms.csv`

Prospective result: 7 registered terms, 1 observed bridge row (`tobit`), 0
terms with Benjamini-Hochberg `q_ge <= 0.05`, and 0 terms above every shuffled
sample. This is negative under the registered shuffled-insertion control rule.
The secondary non-Bible insertion control is also cautionary: 1 of 3 non-Bible
controls is at or above the observed total because the Moby Dick replacement
block also produced 1 `tobit` bridge row.
The lane is now recorded in `configs/prospective_study_lanes.json` and
`docs/PROSPECTIVE_LANE_STATUS.md` as a completed negative controlled result.
The real-report preflight now runs
`scripts/check_kjva_apocrypha_bridge_prospective_boundary.py`, which locks this
boundary directly: 7 registered terms, the single `tobit` candidate row, no
term with BH `q_ge <= 0.05`, no term above every shuffled sample, 1 of 3
non-Bible controls at or above the observed total, and no remaining
`ready_for_preflight` lane.
`docs/KJVA_APOCRYPHA_BRIDGE_NEXT_REPLICATION_DESIGN.md` records the no-input
next-replication design boundary: planning only, fresh term/source target set,
study-lock manifest and preflight sidecar before any new result-bearing output,
and no claim wording from the existing `tobit` row. It is guarded by
`scripts/check_kjva_apocrypha_bridge_next_replication_doc.py`.

Current next step: look for independent replication designs or define a new
locked prospective lane. No KJVA prospective bridge claim language is supported
by the current controls, and there is no remaining `ready_for_preflight` lane in
`configs/prospective_study_lanes.json`.
The CrossWire GitLab KJV/KJVA metadata audit now records one possible
independent KJVA metadata candidate because `kjva.osis.xml` and `kjvdc.xml`
path names are present. Its config metadata also records KJVA GPL distribution
license wording, DC-only general-public-distribution wording, and Crown-rights
language. It is still not source-use or source-lock ready: no local text import,
verse mapping, book-order lock, collation, checksum lock, source-use decision,
term lock, or study-lock sidecar exists.

Covered by the prospective lock:

- fixed prospective term list;
- fixed insertion/control design;
- fixed skip range;
- fixed correction rule.

Still needed before claim language:

- independent replication or a new locked prospective design that survives
  shuffled and non-Bible insertion controls.

### 5. Manual Review Queue

Carry these with controls attached:

- Greek `δοξα` / `δοξανωσ` four-source row.
- Hebrew `יום יהוה` / `היומיהוה` compound extension.
- Greek `γωγ` at Rev 20:8.
- LXX `ιησουσ` rows with Joshua/Jesus referent discipline.
- Hebrew `ישוע` and `משיח` centered rows with background-pressure cautions.

Navigation aid:

- `docs/MANUAL_REVIEW_QUEUE.md`
- `docs/PROSPECTIVE_LANE_STATUS.md`

## Validation Commands

Current fast validation:

```bash
make release-ready
```

Run `make release-ready` from a committed tree; the final public-release gate is
supposed to fail if tracked files are dirty.

Latest validation snapshot after the release-ready make target, refreshed after
the public-reader package protocol guard and real-report protocol duplicate-step
guard:

- Current `make release-ready` passed, including `python3 -m pytest -q`: 2534
  tests, 2 skipped, and 29325 subtests.
- `make public-release-check` passed after the public-reader package protocol
  guard.
- Locked post-discovery reruns for
  `protocols/doxa_four_source_confirmatory_followup.toml`,
  `protocols/all_codes_compound_extension_confirmatory.toml`, and
  `protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml` were
  cache-clean. They remain review/cautionary lanes, not new result-producing
  work.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume`
  passed clean from the committed tree after the all-script exact-test guard.
- `cities_source_row_lock_001` through `cities_source_row_lock_014` are now
  locked as `source_row_lock_ready` for later source-row extraction review only;
  source-row imports, city-name normalization, ELS runs, compactness runs, and
  p-levels remain zero.
- `make public-reader-package` passed after adding the package-time
  general-reader overview guard and package README/manifest guard record.
- `python3 -m scripts.run_protocol protocols/cities_source_row_lock_worksheet.toml --resume`
  and `python3 -m scripts.run_protocol protocols/cities_source_row_lock_evidence_packet.toml --resume`
  passed after adding plain decision meanings and local PDF/page-image path
  checks.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_cities_decision_id_preflight.json`
  passed after requiring populated Cities lock evidence to name its exact
  decision id.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume`
  passed clean from the committed tree after the preregistration
  stale-template guard sync.
- `python3 -m scripts.check_prospective_lane_status_doc` passed with JSON-backed
  lane id/status/path and status-count locks.
- `python3 -m scripts.check_real_report_run_doc` passed with TOML-backed
  protocol step/output locks plus Make target and generated-output path locks.
- `python3 -m scripts.check_strongest_candidate_deep_dive_doc` passed with
  CSV-backed candidate-row locks plus manifest candidate-id/input/path metadata
  locks.
- `python3 -m scripts.check_israeli_prime_ministers_detail_recovery_probe_doc`
  passed with CSV-backed detail-row and summary locks plus snapshot checksum and
  report-manifest boundary locks.
- `python3 -m scripts.check_hypothesis_testing_source_audit_doc` passed with
  CSV-backed page, summary, and anchor locks plus report/source-manifest
  boundary locks.
- `python3 -m scripts.check_final_report_highlights_doc` passed with
  CSV-backed highlight-row locks plus manifest claim-catalog count and path
  metadata locks.
- `python3 -m scripts.check_centered_occurrence_index_doc` passed with
  CSV-backed occurrence-row and presence-summary locks plus manifest
  source/type/path metadata locks.
- `python3 -m scripts.check_research_missing_model_pages_audit_doc` passed with
  CSV-backed unusable level-2/3 model-page rows, source-status summary counts,
  anchor counts, and report-manifest boundary locks.
- `python3 -m scripts.check_cities_pdf_recovery_probe_doc` passed with
  CSV-backed PDF recovery row/summary locks plus manifest boundary locks.
- `python3 -m scripts.check_cities_recovered_pdf_text_audit_doc` passed with
  CSV-backed recovered-PDF text row, summary, and anchor locks plus manifest
  boundary locks.
- `python3 -m scripts.check_cities_extractable_text_review_doc` passed with
  CSV-backed source-role row and summary locks plus manifest boundary locks.
- `python3 -m scripts.check_cities_source_review_queue_doc` passed with
  builder-derived queue and summary locks plus manifest lane-count locks.
- `python3 -m scripts.check_cities_source_row_lock_queue_doc` passed with
  builder-derived source-row lock queue and summary locks plus manifest
  no-import boundary locks.
- `python3 -m scripts.check_cities_source_row_lock_worksheet_doc` passed with
  builder-derived worksheet row locks plus manifest decision-status and
  no-import boundary locks.
- `python3 -m scripts.check_wrr_source_audit_doc` passed with CSV-backed
  locked-method, method-status, and manual-decision summary locks plus
  manifest input/output and count locks.
- `python3 -m scripts.check_wrr_source_row_crop_contact_sheet_doc` passed
  with CSV-backed crop-row, summary, manifest, and PNG dimension locks.
- `python3 -m scripts.check_wrr_source_visual_review_notes_doc` passed with
  CSV-backed source-review queue visual-row and non-exclusion action locks plus
  source queue manifest input/output and count locks.
- `python3 -m scripts.check_wrr_wayback_source_recovery_probe_doc` passed with
  CSV-backed archived row/summary locks plus report-manifest locks.
- `python3 -m scripts.check_wrr_source_recovery_probe_doc` passed with
  CSV-backed row/summary locks plus source-manifest and report-manifest locks.
- `python3 -m scripts.check_wrr_source_review_queue_doc` passed with
  CSV-backed queue, summary-bucket, source-flag, and visual-triage locks plus
  manifest input/output and count locks.
- `python3 -m scripts.check_wrr_source_policy_scenarios_doc` passed with
  CSV-backed scenario, term-impact, and scenario-pair locks plus manifest
  input/output and count locks.
- `python3 -m scripts.check_wrr_dw_formula_sensitivity_doc` passed with
  CSV-backed sensitivity summary and changed-pair locks.
- `python3 -m scripts.check_wrr_direct_all_lanes_doc` passed with CSV-backed
  corrected-distance, aggregate, program-formula, and D(w) sensitivity locks.
- `python3 -m scripts.check_wrr_cross_pair_grid_doc` passed with CSV-backed
  grid-shape, corrected-distance, aggregate, and permutation-summary locks.
- `python3 -m scripts.check_wrr_claim_blocker_packet_doc` passed with
  CSV-backed readiness, source-queue, residual-summary, row-summary, and
  remaining-lane locks.
- `python3 -m scripts.check_wrr_method_pair_universe_evidence_packet_doc`
  passed with CSV fieldname, summary metric, term-set, zero-hit, boundary, and
  manifest input/output locks.
- `python3 -m scripts.check_wrr_remaining_lane_evidence_packets_doc` passed
  with CSV fieldname, lane-summary, term-set, zero-hit, boundary, and manifest
  input/output locks.
- `python3 -m scripts.check_wrr_residual_term_reconciliation_queue_doc` passed
  with CSV fieldname, priority-sequence, summary-key, reconciliation-need,
  priority-one, zero-variant, and manifest input/output locks.
- `python3 -m scripts.check_wrr_residual_reconciliation_action_plan_doc`
  passed with CSV fieldname, rank-sequence, lane-total, zero-variant,
  boundary, and manifest input/output locks.
- `python3 -m scripts.check_wrr_source_policy_evidence_packet_doc` passed with
  packet/context/summary CSV fieldname, row, WNP-context, scenario-count,
  boundary, and manifest input/output locks.
- `python3 -m scripts.check_wrr_source_row_coverage_packet_doc` passed with
  CSV fieldname, summary, rank-sequence, visual-coverage, boundary, and
  manifest input/output locks.
- `python3 -m scripts.check_wrr_source_row_crop_packet_doc` passed with CSV
  fieldname, summary, crop-path, contact-sheet, boundary, and manifest
  input/output locks.
- `python3 -m scripts.check_wrr_source_row_ocr_word_packet_doc` passed with
  CSV fieldname, summary, token-count, low-confidence, crop-path, boundary, and
  manifest input/output locks.
- `python3 -m scripts.check_wrr_source_row_review_bundle_doc` passed with CSV
  fieldname, summary, review-state, OCR/crop, boundary, and manifest
  input/output locks.
- `python3 -m scripts.check_wrr_source_transcription_evidence_packet_doc`
  passed with packet/row-summary CSV fieldname, rank, row-OCR, zero-variant,
  boundary, and manifest input/output locks.
- Cities public handoff docs checker passed and is wired into real-report
  preflight.
- Focused Cities decision-record/preflight pytest passed:
  `tests/test_real_report_run.py`,
  `tests/test_check_cities_source_row_lock_decision_records.py`, and
  `tests/test_check_real_report_run_doc.py`: 111 tests.
- `python3 -m scripts.check_cities_source_row_lock_decision_records` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty` passed.
- `python3 -m scripts.check_doc_command_references --check-local-data` passed.
- Previous `make release-ready` passed from the committed tree, including
  `python3 -m pytest -q`: 1577 tests, 2 skipped, and 29195 subtests.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume`
  passed after the latest pushed guard updates.
- `python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume`
  passed after adding the exact-gap priority-packet step.
- `python3 -m scripts.run_protocol protocols/wrr_cross_pair_grid.toml --resume`
  passed after adding the exact-gap priority-packet refresh step.
- `python3 -m scripts.check_wrr_exact_gap_priority_packet_doc` passed.
- `python3 -m pytest tests/test_real_report_run.py
  tests/test_build_wrr_exact_gap_priority_packet.py
  tests/test_check_wrr_exact_gap_priority_packet_doc.py -q` passed: 87 tests.
- `python3 -m scripts.check_expanded_strata_tooling` passed inside
  `make fast-validate`.
- `make fast-validate` passed after the method/pair-universe evidence packet
  checker manifest lock update: 1907 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the remaining-lane evidence packet checker
  manifest lock update: 1908 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the residual reconciliation action-plan
  checker manifest lock update: 1909 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the residual term reconciliation queue
  checker manifest lock update: 1910 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-policy evidence packet checker
  manifest lock update: 1911 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-row coverage checker manifest
  lock update: 1912 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-row crop checker manifest lock
  update: 1913 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-row OCR word checker manifest
  lock update: 1914 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-row review-bundle checker
  manifest lock update: 1915 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-transcription evidence packet
  checker manifest lock update: 1916 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-transcription row-review
  checklist checker manifest lock update: 1917 tests, 2 skipped, and 29196
  subtests.
- `make fast-validate` passed after the remaining-lane review checklist
  checker manifest lock update: 1918 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-policy review checklist checker
  manifest lock update: 1919 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-policy scenarios checker
  manifest lock update: 1920 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-review queue checker manifest
  lock update: 1921 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source visual-review notes checker
  source-queue manifest lock update: 1922 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the source-audit checker manifest lock
  update: 1923 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the locked-method report checker manifest
  lock update: 1924 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the method-status checker manifest lock
  update: 1925 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the claim-readiness checker manifest lock
  update: 1926 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the lock-options checker manifest lock
  update: 1927 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the exact-gap dashboard checker manifest
  lock update: 1928 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the manual decision-record worksheet
  checker manifest lock update: 1929 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the D(w) formula-sensitivity checker
  manifest lock update: 1930 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the cross-pair grid checker manifest lock
  update: 1931 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the direct all-lane checker manifest lock
  update: 1932 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the claim-catalog field/table lock update:
  1934 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the critical-omission follow-up artifact
  lock update: 1935 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after the prospective readiness profile-status
  snapshot lock update: 1936 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after extending the profile-status snapshot lock
  to next-lock, consolidated-findings, and Greek second-cohort docs: 1936 tests,
  2 skipped, and 29196 subtests.
- `make fast-validate` passed after wiring the Israeli prime-ministers detail
  recovery probe doc into real-report preflight: 1937 tests, 2 skipped, and
  29196 subtests.
- `make fast-validate` passed after adding public-release hygiene CLI tests:
  1940 tests, 2 skipped, and 29196 subtests.
- `make fast-validate` passed after adding CRD relevance-dictionary CLI tests:
  1942 tests, 2 skipped, and 29196 subtests.
- `python3 -m scripts.check_public_claim_language` passed inside
  `make fast-validate`, `make public-release-check`, and the real-report
  preflight.
- `python3 -m scripts.check_doc_command_references` passed inside
  `make public-release-check` and the real-report preflight.
- `make local-data-doc-check` passed on the current local ignored `data/raw/`
  and `data/processed/` caches.
- `make public-release-check` passed from the committed tree.
- `python3 -m scripts.check_wrr_public_handoff_docs` passed after the
  protocol README handoff-status guard.
- Focused pytest for the public-handoff checker and real-report preflight
  wiring passed: 9 tests.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out
  /tmp/edls_preflight_protocols_readme_wrr_lock.json` passed.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume`
  passed from the committed tree at `83414a0`.

Earlier WRR/source-recovery validation snapshot after the WRR gap-reason audit,
readiness gate,
single-term source-policy propagation, missing-model adjacent-source audit,
preflight guard pass, Greek follow-up status refresh, Hebrew MT/STEP_TAHOT
status refresh, KJVA bridge lock-basis clarification, prospective-lane
validator tightening, source-audit preflight guard coverage, prospective-lane
validation in report preflight, source-basis audit queue guarding, and English
source-basis preflight inputs, formal source-basis queue validation,
source-basis validation documentation, and English corpus deferred-policy
guarding, plus formal preflight metadata-check documentation, study-tooling
preflight coverage, and preregistration
placeholder guarding, CRD relevance-lock guarding, manual-review queue
preflight guarding, WRR readiness-doc guarding, WRR blocker-packet preflight
guarding, WRR lock-options preflight guarding, and WRR method-status preflight
guarding, WRR source-recovery probing, WRR source-recovery probe guarding, and
`.shtml` research-source alternate probing, hypothesis-testing source-status
guarding, WRR defined-distance diagnostic doc guarding, and WRR variant-gap
doc guarding, WRR variant-gap method-status evidence propagation, and WRR
residual burden summary/blocker propagation, and WRR Wayback source-recovery
probing/guarding, residual unique-term reconciliation queue guarding, and
residual term blocker-packet propagation, and residual reconciliation action
plan guarding, WRR public handoff doc guarding, and WRR manual decision-record
worksheet guarding, critical-omission follow-up implementation, real-report
reruns, empty-report header preservation, process-pool fallback hardening, WRR
Wayback CDX fallback probing, and live WRR source-recovery parity with the
18-URL Wayback set:

- `python3 -m pytest -q` passed: 1409 tests, 2 skipped, and 14120 subtests after live WRR source-recovery parity with the 18-URL Wayback set.
- `python3 -m pytest tests/test_build_wrr_manual_decision_record_worksheet.py tests/test_check_wrr_manual_decision_record_worksheet_doc.py tests/test_check_wrr_public_handoff_docs.py tests/test_real_report_run.py tests/test_clean_lock_protocols.py -q` passed: 85 tests.
- `python3 -m pytest tests/test_check_wrr_public_handoff_docs.py tests/test_real_report_run.py -q` passed: 57 tests.
- `python3 -m pytest tests/test_build_wrr_residual_reconciliation_action_plan.py tests/test_check_wrr_residual_reconciliation_action_plan_doc.py -q` passed: 6 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_clean_lock_protocols.py tests/test_build_wrr_residual_reconciliation_action_plan.py tests/test_check_wrr_residual_reconciliation_action_plan_doc.py -q` passed: 69 tests.
- `python3 -m pytest tests/test_build_wrr_claim_blocker_packet.py tests/test_check_wrr_claim_blocker_packet_doc.py tests/test_clean_lock_protocols.py tests/test_build_wrr_cross_pair_grid.py tests/test_real_report_run.py -q` passed: 71 tests.
- `python3 -m pytest tests/test_build_wrr_residual_term_reconciliation_queue.py tests/test_check_wrr_residual_term_reconciliation_queue_doc.py tests/test_real_report_run.py -q` passed: 51 tests.
- `python3 -m pytest tests/test_build_wrr_wayback_source_recovery_probe.py tests/test_check_wrr_wayback_source_recovery_probe_doc.py tests/test_real_report_run.py -q` passed: 66 tests.
- `python3 -m pytest tests/test_download_wrr_sources.py tests/test_build_wrr_source_recovery_probe.py tests/test_check_wrr_source_recovery_probe_doc.py tests/test_real_report_run.py -q` passed: 73 tests and 49 subtests.
- `python3 -m pytest tests/test_analyze_hypothesis_testing_source.py tests/test_download_wrr_sources.py -q` passed: 9 tests and 46 subtests.
- `python3 -m pytest tests/test_check_hypothesis_testing_source_audit_doc.py tests/test_real_report_run.py -q` passed: 42 tests.
- `python3 -m pytest tests/test_check_wrr_defined_diagnostic_docs.py tests/test_real_report_run.py -q` passed: 45 tests.
- `python3 -m pytest tests/test_check_wrr_variant_gap_docs.py tests/test_real_report_run.py -q` passed: 46 tests.
- `python3 -m pytest tests/test_build_wrr_variant_residual_review_packet.py tests/test_check_wrr_variant_gap_docs.py tests/test_build_wrr_claim_blocker_packet.py tests/test_check_wrr_claim_blocker_packet_doc.py tests/test_build_wrr_method_status.py tests/test_real_report_run.py -q` passed: 70 tests.
- `python3 -m pytest tests/test_build_wrr_method_status.py tests/test_build_wrr_cross_pair_grid.py tests/test_check_wrr_method_status_doc.py tests/test_check_wrr_claim_readiness_doc.py -q` passed: 15 tests.
- `python3 -m pytest tests/test_check_wrr_claim_readiness_doc.py tests/test_real_report_run.py -q` passed: 38 tests.
- `python3 -m pytest tests/test_check_wrr_claim_blocker_packet_doc.py tests/test_real_report_run.py -q` passed: 39 tests.
- `python3 -m pytest tests/test_check_wrr_lock_options_doc.py tests/test_real_report_run.py -q` passed: 40 tests.
- `python3 -m pytest tests/test_check_wrr_method_status_doc.py tests/test_real_report_run.py -q` passed: 41 tests.
- `python3 -m pytest tests/test_check_manual_review_queue.py tests/test_real_report_run.py -q` passed: 37 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_crd_dictionary_tools.py -q` passed: 40 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_check_preregistration_placeholders.py -q` passed: 36 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_check_expanded_strata_tooling.py tests/test_validate_study_mapping_schemas.py -q` passed: 38 tests.
- `python3 -m pytest tests/test_import_bolls_translation.py tests/test_english_version_manifests.py -q` passed: 12 tests and 117 subtests.
- `python3 -m pytest tests/test_english_version_manifests.py -q` passed: 8 tests and 117 subtests.
- `python3 -m pytest tests/test_english_version_manifests.py tests/test_check_source_basis_audit_queue.py -q` passed: 12 tests and 124 subtests after adding the new CC BY-SA eBible controls.
- `python3 -m pytest tests/test_door43_english_controls.py tests/test_english_version_manifests.py tests/test_check_source_basis_audit_queue.py -q` passed: 13 tests and 126 subtests.
- `python3 -m pytest tests/test_check_source_basis_audit_queue.py tests/test_english_version_manifests.py tests/test_real_report_run.py -q` passed: 39 tests and 117 subtests.
- `python3 -m scripts.check_source_basis_audit_queue` passed.
- `python3 -m scripts.check_english_corpus_policy_docs` passed.
- `python3 -m scripts.run_protocol protocols/ebible_english_controls.toml --resume` passed with 44 included controls, zero missing controls, and 57,333 count rows.
- Door43 ULT/UST open English controls are now tracked separately from eBible
  in `configs/door43_english_controls.csv`; run
  `python3 -m scripts.download_door43_english_controls --skip-existing` and
  `python3 -m scripts.run_protocol protocols/door43_english_controls.toml --resume`
  to refresh their local ignored corpus outputs. Current run passed with 2
  included controls, zero missing controls, and 2,607 count rows.
- OET-LV/OET-RV open English controls are tracked in
  `configs/oet_english_controls.csv`; current run passed with 2 included
  controls, zero missing controls, and 2,606 count rows.
- OTB English UK is tracked in `configs/otb_english_controls.csv`; current
  import wrote 66 books, 31,101 verses, and 3,045,463 letters from 1,189
  chapter JSON files. `python3 -m scripts.run_protocol
  protocols/otb_english_controls.toml --resume` passed with 1 included
  control, zero missing controls, and 1,303 count rows.
- Open.Bible AFINT English NT controls are tracked in
  `configs/openbible_english_controls.csv`; current import wrote 4 controls
  with 7,938-7,940 verses each. `python3 -m scripts.run_protocol
  protocols/openbible_english_controls.toml --resume` passed with 4 included
  controls, zero missing controls, and 5,212 count rows.
- Original Douay-Rheims 1609/1582 is tracked in
  `configs/odr_english_controls.csv`; current import wrote 76 book IDs and
  37,131 rows after merging/skipping 16 duplicate refs from the upstream USFM.
  `python3 -m scripts.run_protocol protocols/odr_english_controls.toml --resume`
  passed with 1 included control, zero missing controls, and 1,303 count rows.
- Supplemental open controls are tracked in
  `configs/supplemental_english_controls.csv` for AKJV, ANDERSON, AV1611,
  AV1811, CPDV, DEB, DRC1750, PET, ACV, NHEB, ROTHERHAM, MONTGOMERY,
  ETHERIDGE, WEYMOUTH, TYNDALE, RWEBSTER, KENT, MCFADYEN, MOFFATT, and TCNT.
  Raw and processed
  source files stay under ignored `data/raw/supplemental/` and
  `data/processed/supplemental/`; current import wrote 31,102 AKJV verses,
  7,946 ANDERSON verses, 36,680 AV1611 verses, 31,102 AV1811 verses, 35,809
  CPDV verses, 30,794 DEB verses, 35,813 DRC1750 verses, 7,753 PET verses, 197
  KENT verses, 3,183 MCFADYEN verses, 2,575 MOFFATT verses, 7,940 TCNT verses,
  31,102 ACV verses, 30,974 NHEB verses, 31,090 ROTHERHAM verses, 7,935
  MONTGOMERY verses, 7,940 ETHERIDGE verses, 7,958 WEYMOUTH verses, and 13,844
  TYNDALE verses, and 31,102 RWEBSTER verses. `python3 -m
  scripts.run_protocol protocols/supplemental_english_controls.toml --resume`
  passed with 20 included controls, zero missing controls, and 26,060 count
  rows.
- `python3 -m scripts.run_protocol protocols/english_version_control_triage.toml --resume`
  now compares BibleGateway-overlap English rows against 74 merged open
  controls from eBible, Door43, OET, OTB, Open.Bible, ODR, and supplemental
  sources; context review
  promoted no seed terms.
- `python3 -m pytest tests/test_download_otb_english_controls.py tests/test_english_version_manifests.py tests/test_check_source_basis_audit_queue.py tests/test_real_report_run.py -q` passed: 75 tests and 124 subtests.
- `python3 -m pytest tests/test_download_openbible_english_controls.py tests/test_english_version_manifests.py tests/test_check_source_basis_audit_queue.py tests/test_real_report_run.py -q` passed: 73 tests and 128 subtests.
- `python3 -m pytest tests/test_download_supplemental_english_controls.py tests/test_check_source_basis_audit_queue.py tests/test_english_version_manifests.py tests/test_real_report_run.py -q` passed: 75 tests and 124 subtests.
- `python3 -m pytest tests/test_download_supplemental_english_controls.py tests/test_check_source_basis_audit_queue.py tests/test_english_version_manifests.py tests/test_real_report_run.py -q` passed: 76 tests and 124 subtests after adding AV1811.
- `python3 -m pytest tests/test_download_supplemental_english_controls.py tests/test_check_source_basis_audit_queue.py tests/test_english_version_manifests.py tests/test_real_report_run.py -q` passed: 77 tests and 124 subtests after adding Zefania/CrossWire supplemental controls.
- `python3 -m pytest tests/test_download_ebible_usfm.py tests/test_download_supplemental_english_controls.py tests/test_check_source_basis_audit_queue.py tests/test_english_version_manifests.py -q` passed: 27 tests and 124 subtests after adding OpenEnglishBible base controls.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_supplemental_controls.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_oeb_supplemental_controls.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_av1811_controls.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_zefania_controls.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_otb_controls.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_openbible_controls.json` passed.
- `python3 -m scripts.check_public_release_hygiene --allow-dirty` passed.
- `python3 -m pytest -q` passed: 1369 tests and 13976 subtests after adding Zefania/CrossWire supplemental controls.
- `python3 -m pytest -q` passed: 1368 tests and 13976 subtests.
- `python3 -m pytest -q` passed: 1359 tests and 13976 subtests after adding Open.Bible AFINT controls.
- `python3 -m scripts.check_expanded_strata_tooling --report /tmp/edls_expanded_tooling_after_patch.json` passed.
- `python3 -m scripts.validate_study_mapping_schemas` passed.
- `python3 -m scripts.check_crd_relevance_dictionary --dictionary terms/relevance_dictionary.toml --term-file terms/gog_magog_pair_prospective_terms.csv --expected-sha256 a6406048b9953ca50715d99100994b9065394d9db31b35867666d365a3bd0f99 --require-reviewed` passed.
- `python3 -m scripts.check_manual_review_queue` passed.
- `python3 -m scripts.check_wrr_claim_readiness_doc` passed.
- `python3 -m scripts.check_wrr_claim_blocker_packet_doc` passed.
- `python3 -m scripts.check_wrr_lock_options_doc` passed.
- `python3 -m scripts.check_wrr_method_status_doc` passed.
- `python3 -m scripts.check_wrr_defined_diagnostic_docs` passed.
- `python3 -m scripts.check_wrr_variant_gap_docs` passed.
- `python3 -m scripts.run_protocol protocols/wrr_source_recovery_probe.toml --resume` passed.
- `python3 -m scripts.run_protocol protocols/wrr_wayback_source_recovery_probe.toml --resume` passed.
- `python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume` passed.
- `python3 -m scripts.run_protocol protocols/wrr_cross_pair_grid.toml --resume` passed.
- `python3 -m scripts.run_protocol protocols/hypothesis_testing_source_audit.toml --resume` passed.
- `python3 -m scripts.check_wrr_source_recovery_probe_doc` passed.
- `python3 -m scripts.check_wrr_wayback_source_recovery_probe_doc` passed.
- `python3 -m scripts.check_wrr_residual_term_reconciliation_queue_doc` passed.
- `python3 -m scripts.check_wrr_residual_reconciliation_action_plan_doc` passed.
- `python3 -m scripts.check_wrr_manual_decision_record_worksheet_doc` passed.
- `python3 -m scripts.check_hypothesis_testing_source_audit_doc` passed.
- `python3 -m pytest tests/test_build_doxa_four_source_claim_followup_report.py tests/test_build_gog_magog_pair_prospective_report.py tests/test_build_wrr_method_status.py -q` passed: 13 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_claim_catalog.py tests/test_wrr_claim_readiness.py -q` passed: 32 tests and 60 subtests.
- `python3 -m pytest tests/test_real_report_run.py -q` passed: 25 tests.
- `python3 -m pytest tests/test_check_prospective_study_lanes.py tests/test_build_prospective_lane_status.py -q` passed: 10 tests.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_check.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_source_audit_guard.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_english_source_basis.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_english_corpus_policy_guard.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_source_basis_docs.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_run_docs_source_basis.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_expanded_mapping_fullgate.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_prereg_placeholders.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_crd_lock.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_manual_queue.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_readiness_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_blocker_packet_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_lock_options_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_method_status_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_hypothesis_source_guard.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_defined_diag_docs.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_variant_gap_docs.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_variant_gap_method_status.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_variant_gap_method_status_cross_pair.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_residual_burden.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wayback_source_probe.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_residual_term_queue.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_residual_term_blocker.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_residual_action_plan.json` passed.
- `python3 -m scripts.check_wrr_public_handoff_docs` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_public_handoff_guard.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_manual_decision_record_worksheet.json` passed.
- `597b1a0` Reflect WRR manual decision locks in worksheet.
- `af38937` Align WRR handoff docs with decision locks.
- `c35f6e6` Update WRR checklist lock boundary wording.
- Historical `python3 -m pytest -q` result after the lock-status documentation updates:
  1409 passed, 2 skipped, 14120 subtests passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_public_locks.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_checklist_locks.json` passed.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume` passed clean from committed state after each pushed update.
- `python3 -m scripts.check_prospective_study_lanes` passed.
- `git diff --check` passed.
- `python3 -m scripts.check_public_release_hygiene --allow-dirty` passed.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume` passed clean after each tracked WRR/report update.

## KJVA Wikisource Candidate Source Audit

- Added `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md` as a metadata-only
  source-status audit for the Wikisource 1911 Ballantyne KJV + Apocrypha
  candidate. It records source markers and fetch metadata only; it does not
  import Bible text, create a corpus, run ELS searches, or change KJVA bridge
  result status.
- Added `protocols/kjva_wikisource_candidate_source_audit.toml` and wired the
  audit into `protocols/real_report_run.toml` plus
  `scripts/preflight_real_report_run.py`.
- The audit keeps the next-replication decision unchanged: the page can be a
  future source candidate, but it still needs lawful text import, verse
  mapping, book-order lock, collation, checksums, term lock, and study-lock
  sidecar before any result-bearing KJVA replication.
- `make fast-validate` passed after wiring: 2162 passed, 2 skipped, and 29325
  subtests passed.

## KJVA Open-Bibles Candidate Source Audit

- Added `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md` as a metadata-only
  source-status audit for `seven1m/open-bibles`. It records GitHub repository
  metadata, tree path counts, and README markers only.
- Current metadata found one KJV OSIS path marker (`eng-kjv.osis.xml`) and zero
  apocrypha/deuterocanon path markers, so this source is KJV-only for current
  KJVA/apocrypha bridge purposes.
- Added `protocols/kjva_open_bibles_candidate_source_audit.toml` and wired the
  audit into `protocols/real_report_run.toml` plus
  `scripts/preflight_real_report_run.py`.
- `make fast-validate` passed after wiring: 2170 passed, 2 skipped, and 29325
  subtests passed.

## KJVA Source Candidate Status Rollup

- Added `docs/KJVA_SOURCE_CANDIDATE_STATUS.md` as a single rollup for the
  current KJVA/apocrypha source-candidate state.
- Current rollup status: 0 ready independent KJVA replication sources, 2
  possible independent KJVA metadata candidates, 1 public-domain split
  KJV+Apocrypha coverage candidate needing collation, 0 result-ready sources,
  and 0 source-lock ready sources.
- It keeps the source boundary explicit: current eBible KJV + Apocrypha remains
  the rerun source family with 14 apocrypha/deuterocanon books, 5720 verses,
  and 593090 normalized letters; CrossWire is a metadata-level future source
  candidate with KJVA/KJVDC paths present; Project Gutenberg eBook 30 plus
  eBook 124 is a public-domain-USA split KJV+Apocrypha coverage candidate
  needing collation and a Baruch/Epistle handling decision; Wikisource remains
  a metadata-level future source candidate; and `seven1m/open-bibles` remains
  KJV-only for current KJVA/apocrypha bridge purposes.
- Added `scripts/check_kjva_source_candidate_status_doc.py` and wired it into
  `scripts/preflight_real_report_run.py` plus `protocols/real_report_run.toml`.

## KJVA Wikisource Book Coverage Probe

- Added `docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md` as a metadata-only
  book-link coverage probe for the Wikisource Ballantyne KJV + Apocrypha
  candidate.
- Current parsed main-page book-link status: 66 expected KJV books, 36 existing
  KJV book links, 30 KJV redlinks, 0 missing KJV rows, 14 expected
  apocrypha/deuterocanon books, and 0 visible apocrypha/deuterocanon book links.
- This keeps Wikisource at coverage-probe status only: no child book text is
  fetched, no Bible text is retained, no verse mapping exists, no book-order
  lock is ready, and no KJVA result status changes.
- Added `protocols/kjva_wikisource_book_coverage_probe.toml`,
  `scripts/analyze_kjva_wikisource_book_coverage_probe.py`, and
  `scripts/check_kjva_wikisource_book_coverage_probe_doc.py`, and wired the
  probe into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA CrossWire Candidate Source Audit

- Added `docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md` as a metadata-only
  source-status audit for the CrossWire Bible Society GitLab KJV repository.
- Current metadata found 9 tree paths, including `kjva.osis.xml`, `kjvdc.xml`,
  `kjva.conf`, `kjvdc.conf`, and `kjvfull2kjva.sh`, and records config
  license/rights markers without importing Bible text.
- The audit records one possible independent KJVA metadata candidate, but 0
  source-use ready pages, 0 source-lock ready pages, 0 verse-import ready pages,
  and 0 result-ready pages.
- No Bible text is downloaded, retained, normalized, or committed by this
  audit; it does not change KJVA bridge result status.
- Added `protocols/kjva_crosswire_candidate_source_audit.toml`,
  `scripts/analyze_kjva_crosswire_candidate_source.py`, and
  `scripts/check_kjva_crosswire_candidate_source_audit_doc.py`, and wired the
  audit into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Candidate Source Audit

- Added `docs/KJVA_GUTENBERG_CANDIDATE_SOURCE_AUDIT.md` as a metadata-only
  source-status audit for Project Gutenberg eBook 30 plus eBook 124.
- Current RDF metadata records `The Bible, King James Version, Complete` for
  eBook 30 and `Deuterocanonical Books of the Bible Apocrypha` for eBook 124,
  with `Public domain in the USA.` rights and plain-text UTF-8 format URLs for
  both source components.
- The audit records one public-domain-USA KJV-complete metadata component, one
  public-domain-USA Apocrypha/deuterocanon metadata component, and one split
  KJV+Apocrypha metadata candidate, but 0 source-use ready pages, 0 source-lock
  ready pages, 0 verse-import ready pages, and 0 result-ready pages.
- No Bible text is downloaded, retained, normalized, or committed by this
  audit; it does not change KJVA bridge result status.
- Added `protocols/kjva_gutenberg_candidate_source_audit.toml`,
  `scripts/analyze_kjva_gutenberg_candidate_source.py`, and
  `scripts/check_kjva_gutenberg_candidate_source_audit_doc.py`, and wired the
  audit into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Book Coverage Probe

- Added `docs/KJVA_GUTENBERG_BOOK_COVERAGE_PROBE.md` as a heading-level
  source-coverage probe for Project Gutenberg eBook 30 plus eBook 124.
- Current plain-text heading marker status: 66 expected KJV books, 66 found KJV
  book headings, 0 missing KJV headings, 14 expected Apocrypha/deuterocanon
  books, 14 found Apocrypha/deuterocanon book headings, 0 missing
  Apocrypha/deuterocanon headings, and one extra Epistle of Jeremiah source
  heading. Verse-shape status: 31102 KJV book:chapter:verse markers and 5704
  Apocrypha/deuterocanon verse-like markers split between chapter:verse and
  number-only marker shapes.
- This changes the Gutenberg read from KJV-only control candidate to possible
  public-domain split KJV+Apocrypha coverage candidate needing collation,
  source-use policy lock, and Baruch/Epistle handling decision before any
  result-bearing KJVA bridge use.
- No Bible text is committed, normalized, or imported by this probe; it does
  not change KJVA bridge result status.
- Added `protocols/kjva_gutenberg_book_coverage_probe.toml`,
  `scripts/analyze_kjva_gutenberg_book_coverage_probe.py`, and
  `scripts/check_kjva_gutenberg_book_coverage_probe_doc.py`, and wired the
  probe into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Source-Lock Prep

- Added `docs/KJVA_GUTENBERG_SOURCE_LOCK_PREP.md` as a count-only source-lock
  prep comparison for Project Gutenberg eBook 30 plus eBook 124 against the
  current local KJVA corpus.
- Current count status: all 66 KJV books match the local KJVA counts exactly;
  12 of 14 tracked Apocrypha/deuterocanon books match after rolling the
  separate Epistle of Jeremiah source section into Baruch; Sirach is one source
  marker short and Prayer of Manasseh has no body verse markers in eBook 124.
- The prep records one extra Epistle of Jeremiah source section, 31102
  Gutenberg KJV verse markers, and 5704 Gutenberg Apocrypha/deuterocanon
  verse-like markers, but it still leaves source-use policy, verse mapping,
  collation, checksum lock, and study-lock sidecar work open.
- No Bible text is committed, normalized, or imported by this prep; it does
  not change KJVA bridge result status.
- Added `protocols/kjva_gutenberg_source_lock_prep.toml`,
  `scripts/analyze_kjva_gutenberg_source_lock_prep.py`, and
  `scripts/check_kjva_gutenberg_source_lock_prep_doc.py`, and wired the prep
  into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Source-Lock Decision Packet

- Added `docs/KJVA_GUTENBERG_SOURCE_LOCK_DECISION_PACKET.md` as a decision
  packet built from the Gutenberg source-lock prep outputs.
- Current packet status: 10 decision rows, 2 policy-ready rows, 3
  recommended-but-not-locked rows, 4 blocked rows, and 1 candidate-not-locked
  row. It recommends using Gutenberg source order for a future independent
  Project Gutenberg replication stream, rolling Epistle of Jeremiah into BAR
  for KJVA book-code compatibility, and keeping raw Gutenberg text ignored or
  in memory only.
- The packet explicitly blocks source lock on Sirach and Prayer of Manasseh:
  Sirach is one source marker short and Prayer of Manasseh has no body verse
  markers in eBook 124. Both need citable non-text collation decisions before
  any source-lock sidecar can be written.
- No Bible text is committed, normalized, or imported by this packet; it does
  not change KJVA bridge result status.
- Added `protocols/kjva_gutenberg_source_lock_decision_packet.toml`,
  `scripts/build_kjva_gutenberg_source_lock_decision_packet.py`, and
  `scripts/check_kjva_gutenberg_source_lock_decision_packet_doc.py`, and wired
  the packet into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Source-Lock Blocker Packet

- Added `docs/KJVA_GUTENBERG_SOURCE_LOCK_BLOCKER_PACKET.md` as a marker-only
  blocker packet for the two remaining Gutenberg KJVA source-lock blockers.
- Current packet status: Sirach source markers 1392 vs local markers 1393,
  with the marker-only gap narrowed to `SIR 44:23`; Prayer of Manasseh source
  section detected with 0 body markers vs 15 local markers.
- Recommended next boundary: do not auto-insert the Sirach marker, and do not
  manually split Prayer of Manasseh before a citable marked source, exclusion
  policy, or boundary rule is locked.
- No Bible text is committed, normalized, split, or imported by this packet;
  it does not change KJVA bridge result status.
- Added `protocols/kjva_gutenberg_source_lock_blocker_packet.toml`,
  `scripts/build_kjva_gutenberg_source_lock_blocker_packet.py`, and
  `scripts/check_kjva_gutenberg_source_lock_blocker_packet_doc.py`, and wired
  the packet into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Hakkaac Boundary Candidate

- Added `docs/KJVA_HAKKAAC_APOCRYPHA_BOUNDARY_CANDIDATE.md` as a marker-only
  candidate audit for the two remaining Gutenberg KJVA source-lock blockers.
- Current audit status: Hakkaac Sirach 44 exposes markers `1..23`, including
  the missing `SIR 44:23` marker; Hakkaac Prayer of Manasseh exposes markers
  `1..15`; both pages include a public-domain note.
- This is candidate evidence only. It does not source-lock Hakkaac, import
  Bible text, collate wording, choose source order, or authorize a
  result-bearing run.
- Added `protocols/kjva_hakkaac_apocrypha_boundary_candidate.toml`,
  `scripts/analyze_kjva_hakkaac_apocrypha_boundary_candidate.py`, and
  `scripts/check_kjva_hakkaac_apocrypha_boundary_candidate_doc.py`.

## KJVA Hakkaac Apocrypha Marker Coverage

- Added `docs/KJVA_HAKKAAC_APOCRYPHA_MARKER_COVERAGE.md` as a full
  marker-only coverage audit for all 14 Hakkaac KJV Apocrypha pages.
- Current audit status: Hakkaac exposes exact marker-count agreement for all
  14 tracked Apocrypha/deuterocanon books, with 5720 source markers, 5720
  local markers, 173 chapter rows, and 0 chapter drift rows.
- This is marker-coverage evidence only. It does not source-lock Hakkaac,
  import Bible text, collate wording, choose source order, or authorize a
  result-bearing run.
- Added `protocols/kjva_hakkaac_apocrypha_marker_coverage.toml`,
  `scripts/analyze_kjva_hakkaac_apocrypha_marker_coverage.py`, and
  `scripts/check_kjva_hakkaac_apocrypha_marker_coverage_doc.py`.

## KJVA Hakkaac Apocrypha Collation Audit

- Added `docs/KJVA_HAKKAAC_APOCRYPHA_COLLATION_AUDIT.md` as an ignored-local
  collation audit for Hakkaac KJV Apocrypha against the current local KJVA
  Apocrypha source.
- Current audit status: raw Hakkaac verse text stays under ignored
  `data/private/` output only; tracked outputs contain hashes, lengths, refs,
  and status rows only.
- Current collation result: 5719 of 5720 exact normalized verse matches, one
  `SIR 19:1` one-letter normalized length drift, 13 of 14 exact book-stream
  matches, exact `SIR 44:23` and `MAN 1:1..15` blocker rows, and 0 missing
  refs.
- This is collation evidence only. It does not source-lock Hakkaac, choose a
  source-order rule, run ELS searches, or authorize a result-bearing run.
- Added `protocols/kjva_hakkaac_apocrypha_collation.toml`,
  `scripts/analyze_kjva_hakkaac_apocrypha_collation.py`, and
  `scripts/check_kjva_hakkaac_apocrypha_collation_doc.py`.

## KJVA Hakkaac Source-Lock Decision Packet

- Added `docs/KJVA_HAKKAAC_SOURCE_LOCK_DECISION_PACKET.md` as a non-text
  decision packet over the Hakkaac marker-coverage and ignored-local collation
  evidence.
- Current packet status: 9 decision rows, 3 policy-ready rows, 2
  recommended-but-not-locked rows, 3 blocked rows, and 1 candidate-not-locked
  row.
- Current recommendation: keep Hakkaac as candidate evidence only, keep
  current eBible KJVA as the rerun baseline, do not patch either source
  automatically for `SIR 19:1`, and do not combine Project Gutenberg plus
  Hakkaac into a result-bearing split-source stream without a source-order and
  source-role sidecar.
- Current blockers: `SIR 19:1` remains a named normalized-letter drift, and
  split-source use remains blocked until source roles and order are written
  into a study-lock sidecar.
- No Bible text is committed, normalized into a tracked corpus, or imported by
  this packet; it does not change KJVA bridge result status.
- Added `protocols/kjva_hakkaac_source_lock_decision_packet.toml`,
  `scripts/build_kjva_hakkaac_source_lock_decision_packet.py`, and
  `scripts/check_kjva_hakkaac_source_lock_decision_packet_doc.py`, and wired
  the packet into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Current Source Lock Sidecar

- Added `docs/KJVA_CURRENT_SOURCE_LOCK_SIDECAR.md` as a non-text checksum,
  book-order, and count-shape sidecar for the current eBible KJV + Apocrypha
  rerun baseline.
- Current sidecar status: source id `eng-kjv`, CSV SHA-256
  `f4f4549c7323de20a6cdd7aa74aeae32d184b2b6a1a51cd41390540efd710360`,
  ZIP SHA-256
  `0ec30ed796dbc1aea401c497359a9e115077c7d72bf19d3dbf93f20acd784f8b`,
  80 books, 36822 verses, 14 apocrypha/deuterocanon books, 5720
  apocrypha/deuterocanon verses, and 593090 apocrypha/deuterocanon normalized
  letters.
- This locks the current rerun baseline only. It does not make eBible an
  independent replication source, does not choose Hakkaac or Project Gutenberg,
  and does not authorize a result-bearing KJVA bridge run.
- Added `protocols/kjva_current_source_lock_sidecar.toml`,
  `scripts/build_kjva_current_source_lock_sidecar.py`, and
  `scripts/check_kjva_current_source_lock_sidecar_doc.py`, and wired the
  sidecar into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Hakkaac Split-Source Role Sidecar

- Added `docs/KJVA_GUTENBERG_HAKKAAC_SPLIT_SOURCE_ROLE_SIDECAR.md` as a
  non-text source-role/order sidecar for the Project Gutenberg plus Hakkaac
  candidate path.
- Current sidecar status: 7 role rows, 6 unresolved blocker rows, 2
  policy-ready role rows, 2 recommended-but-not-locked role rows, 2 blocked
  role rows, and 1 candidate-not-locked role row.
- Current role boundary: Project Gutenberg remains the future primary
  candidate stream, Hakkaac remains marker/collation witness-only, and current
  eBible KJVA remains the rerun-only baseline.
- Current unresolved blockers: `SIR 44:23` Gutenberg marker gap, Prayer of
  Manasseh unmarked Gutenberg section, `SIR 19:1` Hakkaac/local length drift,
  Hakkaac source-use boundary, split-source result boundary, and Gutenberg
  source-stream boundary.
- This closes only the missing written role/order boundary. It does not close
  source-use, drift, term/control, or study-lock blockers and does not change
  KJVA bridge result status.
- Added `protocols/kjva_gutenberg_hakkaac_split_source_role_sidecar.toml`,
  `scripts/build_kjva_gutenberg_hakkaac_split_source_role_sidecar.py`, and
  `scripts/check_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc.py`, and
  wired the sidecar into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Gutenberg Candidate Checksum Sidecar

- Added `docs/KJVA_GUTENBERG_CANDIDATE_CHECKSUM_SIDECAR.md` as a non-text
  checksum sidecar for Project Gutenberg eBook 30 and eBook 124 candidate
  identifiers.
- Current sidecar status: 2 source rows, 2 metadata fetches OK, 2
  public-domain-USA rows, 2 plain-text checksum rows, and 2 checksum records
  ready.
- Current checksum boundary: eBook 30 and eBook 124 RDF SHA-256 values plus
  plain-text SHA-256 values are recorded as candidate identifiers only.
- This closes only the candidate checksum-record step. It does not close
  source-use, verse mapping, collation, `SIR 44:23`, Prayer of Manasseh,
  `SIR 19:1`, term/control, or study-lock blockers and does not change KJVA
  bridge result status.
- Added `protocols/kjva_gutenberg_candidate_checksum_sidecar.toml`,
  `scripts/build_kjva_gutenberg_candidate_checksum_sidecar.py`, and
  `scripts/check_kjva_gutenberg_candidate_checksum_sidecar_doc.py`, and wired
  the sidecar into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Source Policy Blocker Packet

- Added `docs/KJVA_SOURCE_POLICY_BLOCKER_PACKET.md` as a non-text rollup of
  current KJVA source-policy choices and blockers.
- Current packet status: 5 policy option rows, 7 blocker rows, 2 policy-ready
  options, 3 blocked options, 2 checksum records ready, 0 source-use ready
  pages, `SIR 44:23` Gutenberg Sirach gap, 0/15 Gutenberg Prayer of Manasseh
  body markers, and 1 Hakkaac length-drift verse.
- Current policy-ready options: current eBible rerun only, and deferral of new
  KJVA result-bearing work.
- Current blocked options: Project Gutenberg-only candidate, Project Gutenberg
  plus Hakkaac split candidate, and Hakkaac primary stream.
- This packet does not add Bible text, approve source use, lock a source,
  create an ELS result, or change KJVA bridge result status.
- Added `protocols/kjva_source_policy_blocker_packet.toml`,
  `scripts/build_kjva_source_policy_blocker_packet.py`, and
  `scripts/check_kjva_source_policy_blocker_packet_doc.py`, and wired the
  packet into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA Next Result Gate

- Added `docs/KJVA_NEXT_RESULT_GATE.md` as a non-text gate for future KJVA
  result-bearing work.
- Current gate status: 11 gate rows, 1 rerun-only ready row, 10 blocked rows,
  7 source-policy blocker rows, 7 completed-lane terms, 1 completed-lane
  observed bridge row, 0 completed-lane significant terms, and 1 non-Bible
  control at or above the observed total.
- Current ready scope: current eBible KJVA rerun reproducibility only.
- Current blocked scope: completed-lane claim use, source policy, source text,
  verse map/collation, drift/boundary, fresh terms, leakage audit, fixed
  controls, study-lock manifest, and final result permission.
- This gate does not add Bible text, approve source use, lock terms, lock a
  study, create an ELS result, or change KJVA bridge result status.
- Added `protocols/kjva_next_result_gate.toml`,
  `scripts/build_kjva_next_result_gate.py`, and
  `scripts/check_kjva_next_result_gate_doc.py`, and wired the gate into
  `scripts/preflight_real_report_run.py` plus `protocols/real_report_run.toml`.

## WRR No-Input Handoff Status

- Added `docs/WRR_NO_INPUT_HANDOFF_STATUS.md` as a consolidated non-result
  handoff for current WRR no-input work.
- Current status: 9 handoff rows, 9 handoff-ready rows, 8
  manual-input-needed rows, 4/4 local claim-readiness rows ready, 0
  claim-blocker rows, 163 source-cited defined distances, 72 current defined
  distances, and 91 remaining gap.
- Current review load: 4 residual lanes, 58 action terms, 59 residual pairs,
  40 frontier pairs, 37 manual-decision rows, 22 source-transcription row
  clusters, 3 page-image near-match terms, and 11 method/pair-universe terms.
- Current result boundary: new WRR result allowed 0, exact published
  reproduction ready 0, and claim boundary
  `local_locked_method_ready_exact_published_open`.
- This handoff does not create a new WRR result, reproduce published WRR,
  select source corrections, select pair exclusions, lock replacement
  spellings, or change method rules.
- Added `protocols/wrr_no_input_handoff_status.toml`,
  `scripts/build_wrr_no_input_handoff_status.py`, and
  `scripts/check_wrr_no_input_handoff_status_doc.py`, and wired the handoff
  into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## KJVA No-Input Handoff Status

- Added `docs/KJVA_NO_INPUT_HANDOFF_STATUS.md` as a consolidated non-result
  handoff for current KJVA/apocrypha source-readiness work.
- Current status: 9 handoff rows, 9 handoff-ready rows, 8
  manual-input-needed rows, 11 next-result gates, 1 rerun-only ready row, 10
  blocked gate rows, 7 source-policy blocker rows, and result allowed 0.
- Current source boundary: current eBible KJVA remains rerun-only; no
  independent KJVA source is source-locked for result-bearing use.
- Current blockers: 0 source-use ready pages, `SIR 44:23` Gutenberg Sirach
  marker gap, 0/15 Gutenberg Prayer of Manasseh markers, 5719/5720 Hakkaac
  exact normalized verse matches, 1 Hakkaac length-drift verse, 7 split-source
  role rows, 6 split-source blocker rows, fresh terms ready 0, leakage audit
  ready 0, fixed controls ready 0, and study-lock ready 0.
- This handoff does not approve source use, import Bible text, source-lock a
  candidate, choose corrections, create terms, lock controls, write a study
  lock, or create a KJVA result.
- Added `protocols/kjva_no_input_handoff_status.toml`,
  `scripts/build_kjva_no_input_handoff_status.py`, and
  `scripts/check_kjva_no_input_handoff_status_doc.py`, and wired the handoff
  into `scripts/preflight_real_report_run.py` plus
  `protocols/real_report_run.toml`.

## Generated Real-Report Handoff Guarding

- The generated real-report summary now surfaces both consolidated no-input
  packets from their CSV/manifest outputs: WRR from
  `reports/wrr_1994/wrr_no_input_handoff_status_summary.csv` and
  `reports/wrr_1994/wrr_no_input_handoff_status.manifest.json`, and KJVA from
  `reports/kjva_no_input_handoff_status/summary.csv` and
  `reports/kjva_no_input_handoff_status/manifest.json`.
- Current generated WRR handoff read: 9 handoff rows, 8
  manual-input-needed rows, 163 source-cited defined distances, 72 current
  defined distances, 91 remaining gap, new WRR result allowed 0, and exact
  reproduction ready 0.
- Current generated KJVA handoff read: 9 handoff rows, 8
  manual-input-needed rows, 11 next-result gates, 10 blocked gate rows, 7
  source-policy blocker rows, source-lock ready 0, and result allowed 0.
- Public handoff drift guards now also check `reports/real_report_run/summary.md`
  for WRR, KJVA, and Cities boundary language: no new WRR result, no exact
  published WRR reproduction, no new KJVA result, no KJVA source lock, no
  Cities source-row imports, no Cities ELS run, and no Cities compactness run.
- Added or updated `scripts/check_real_report_run_doc.py`,
  `scripts/check_wrr_public_handoff_docs.py`,
  `scripts/check_kjva_public_handoff_docs.py`, and
  `scripts/check_cities_public_handoff_docs.py`, plus their focused tests.
- Commits: `82a6f78`, `c6d4809`, `7a9da6e`, `a061abd`, `45d4eba`, and
  `16f020c`.

## KJVA Candidate-Source Handoff Metrics

- Extended the KJVA no-input handoff summary to read the current metadata-only
  candidate-source audits directly: CrossWire, Project Gutenberg, Wikisource,
  and `seven1m/open-bibles`.
- Current generated handoff read: 4 candidate-source audit rows, 0
  verse-import-ready candidate pages, 0 result-ready candidate pages, 1
  CrossWire possible independent KJVA metadata candidate, 1 Project Gutenberg
  split KJV plus Apocrypha metadata candidate, 1 Wikisource source-candidate
  page, and Open-Bibles at 1 KJV path but 0 Apocrypha/deuterocanon paths.
- This closes only a summary/guarding gap. It does not approve source use,
  import Bible text, source-lock a candidate, change KJVA result status, or
  authorize a new KJVA run.
- Added these candidate-source metrics to
  `docs/KJVA_NO_INPUT_HANDOFF_STATUS.md` and to the generated
  `reports/real_report_run/summary.md` KJVA handoff table, with guard checks in
  `scripts/check_kjva_no_input_handoff_status_doc.py` and
  `scripts/check_kjva_public_handoff_docs.py`.

## KJVA Candidate-Source Public Handoff Sync

- Surfaced the same KJVA candidate-source handoff counts in the public-facing
  reader path: `README.md`, `docs/FINAL_REPORT.md`, `docs/REAL_REPORT_RUN.md`,
  and `protocols/README.md`.
- Current public wording now keeps this boundary visible outside the generated
  handoff report: 4 candidate-source audit rows, 0 verse-import-ready
  candidate pages, 0 result-ready candidate pages, and no new KJVA result
  allowed.
- Extended `scripts/check_kjva_public_handoff_docs.py` and
  `scripts/check_real_report_run_doc.py` so the reader-facing docs cannot drop
  those candidate-source counts while still claiming the handoff is current.

## KJVA Candidate-Source Findings Overview Sync

- Added the same source-readiness boundary to the general-reader findings
  overview and consolidated findings: the KJVA bridge rows remain interesting
  review material, but no new KJVA result run is ready.
- Current reader-facing summary now says the handoff has 4 candidate-source
  audit rows, 0 candidate verse-import-ready pages, 0 candidate result-ready
  pages, and result allowed 0.
- Extended `scripts/check_project_findings_overview_doc.py` and
  `scripts/check_consolidated_findings_doc.py` so those broader summary docs
  cannot describe the KJVA bridge lane without the current source-readiness
  blocker.

## Cities No-Input Handoff Status

- Added `docs/CITIES_NO_INPUT_HANDOFF_STATUS.md` as the consolidated no-input
  packet for the Cities/Aumann/Simon-McKay source-row lane.
- Current Cities no-input handoff summary: 8 handoff rows, 6
  manual-input-needed rows, 14 transcription review rows, 61 OCR packet pages,
  41 reviewed OCR packet pages, 20 unreviewed OCR packet pages, 203 priority
  line-crop review rows, and no Cities result allowed.
- The packet keeps the existing source-row lock handoff boundary visible: 14
  source-row lock candidate pages, 14 populated lock rows, 14 pending
  transcription-review rows, no source rows imported, and no city-name
  normalization, ELS searches, compactness runs, or p-levels.
- Added `scripts/build_cities_no_input_handoff_status.py`,
  `scripts/check_cities_no_input_handoff_status_doc.py`, and
  `protocols/cities_no_input_handoff_status.toml`; wired the checker into
  preflight and the protocol into `protocols/real_report_run.toml`.

## Cities Findings Overview Sync

- Surfaced the Cities/Aumann/Simon-McKay source-row boundary in the
  general-reader findings overview so the whole-project summary no longer
  makes readers discover the Cities blocker only through the handoff packet.
- Current overview wording now keeps the same no-result boundary visible: 14
  source-row lock candidate pages, 14 populated source-row lock rows, 8
  handoff rows, 6 manual-input-needed rows, 14 transcription review rows, 61
  OCR packet pages, 41 reviewed OCR packet pages, 20 unreviewed OCR packet
  pages, 203 priority line-crop review rows, and no Cities result allowed.
- The overview also states that the Cities lane has not produced source rows,
  city-name normalization, ELS searches, compactness runs, or p-levels.
- Extended `scripts/check_project_findings_overview_doc.py` so the
  general-reader overview cannot keep a Cities section while dropping the
  current source-row blocker counts, plain-language page-vs-list explanation,
  and no-result boundary.
- Commit: `a25e313`.

## Cities OCR Packet Coverage Public Sync

- Extended the consolidated Cities no-input handoff to read
  `reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_page_review_summary.csv`,
  so the handoff summary now carries 61 OCR packet pages, 41 reviewed OCR
  packet pages, and 20 unreviewed OCR packet pages alongside the existing
  source-row and line-crop blockers.
- Synced that count into the public reader path: `README.md`,
  `docs/PROJECT_FINDINGS_OVERVIEW.md`, `docs/CLAIM_CATALOG.md`,
  `docs/CONSOLIDATED_FINDINGS.md`, `docs/FINAL_REPORT.md`,
  `docs/FINAL_REPORT_DRAFT.md`, `docs/FINAL_REPORT_OUTLINE.md`,
  `docs/REAL_REPORT_RUN.md`, and `protocols/README.md`.
- Hardened `scripts/check_cities_public_handoff_docs.py` so public docs fail if
  the older transcription-review-plus-priority-summary wording returns without
  the OCR packet coverage counts.
- Commits: `0128758`, `3f063fb`, `63ab308`, `feaad6f`.

## Public Reader Package Cities Handoff Sync

- Added `docs/CITIES_NO_INPUT_HANDOFF_STATUS.md` to the public-reader package
  whitelist because `docs/PROJECT_FINDINGS_OVERVIEW.md` now sends readers
  there for the Cities source-row boundary.
- Updated the package README ordering so the generated package points readers
  to the Cities no-input handoff before the formal real-report summary.
- Extended `tests/test_build_public_reader_package.py` so package tests fail
  if the exported reader package drops the Cities handoff file or any required
  project-findings overview reference.
- This is a reader-export fix only. It does not import source rows, normalize
  city names, run ELS searches, compute compactness, or report p-levels.

## Public Reader Package Release-Gate Check

- Added `public-reader-package-check` to the Makefile and wired it into
  `make fast-validate` and `make public-release-check` so handoff and clean
  release gates now check that the whitelisted reader package can build to
  `/tmp/edls_public_reader_package_check`.
- Updated `README.md` and `tests/test_clean_lock_protocols.py` so the release
  gate and fast-validation documentation and test coverage mention the
  temporary public-reader package build.
- This is a packaging guard only. It does not change the public package
  contents beyond the already-committed Cities handoff inclusion.

## Public Reader Package WRR/KJVA Handoff Sync

- Added `docs/WRR_NO_INPUT_HANDOFF_STATUS.md` and
  `docs/KJVA_NO_INPUT_HANDOFF_STATUS.md` to the public-reader package
  whitelist because the packaged README sends readers to both consolidated
  handoff files.
- Added both files to the general-reader findings overview "Where To Read
  More" list and guarded those references in
  `scripts/check_project_findings_overview_doc.py`.
- Extended `tests/test_build_public_reader_package.py` so package tests fail
  if either consolidated handoff drops out of the exported reader package or
  the package README start list.
- This is a reader-export fix only. It does not change WRR, KJVA, or Cities
  result status.
- Added a broader package guard so no-input handoff links in README,
  project-findings overview, final report, or real-report docs must be present
  in the public-reader package whitelist.

## Public Reader Package Reader-Link Guard

- Added a package-input guard for `docs/START_HERE.md` so every backticked
  `docs/*.md` or `reports/*.md` reader-path link in that guide must be present
  in the public-reader package whitelist before packaging.
- Added the same package-input guard to the README's top `Reader path:` section
  without requiring every support-link elsewhere in the README to be packaged.
- Added focused package tests for the current `START_HERE` reader links and
  README reader-path links, plus failure cases where either points to an
  unpackaged document.
- Aligned the generated package README start list with the `START_HERE` reader
  order by including consolidated findings, real-report run, and remaining
  work before the handoff/status packet links.
- Moved the generated package README start list into a single
  `PACKAGE_START_PATHS` constant and added a guard that every start-list entry
  is in the package whitelist, so numbering and package inclusion cannot drift
  separately.
- Tightened the package-input guard so `START_HERE` must contain packaged
  reader links and the README must retain a non-empty `Reader path:` section.
- Extended the same packaged-reader-link guard to the final report's `Reader
  Path` section and the real-report run's `Reader role` paragraph, while still
  leaving their long support-doc inventories outside the public package.
- Added public-reader package manifest metadata for package start paths and
  reader-link source sections, so the generated package records what link
  guard surface was checked.
- Updated the manifest's reader-path guard description to match the current
  configured reader-link source set.
- Updated README/package README wording so the release and package docs now
  refer to configured reader-link sources rather than only README/Start Here.
- Added source-path guards to the public-reader package copier so package
  sources must be relative `.md`/`.json` paths without `..` segments; absolute
  and parent-traversal extra-doc inputs cannot escape the package tree.
- Added duplicate-source guarding so `--extra-doc` cannot repeat an already
  whitelisted package source and produce duplicated manifest/reader-package
  entries.
- Tightened `--extra-doc` validation so extra document inputs must be Markdown
  docs; JSON remains limited to the formal report outputs.
- Tightened the package start-list guard so every generated start-list path
  must be present in the actual package input set after optional report files
  are filtered, preventing a package README from pointing at a missing formal
  report summary.
- Added Git tracking validation for public-reader doc inputs, so `--extra-doc`
  cannot package an untracked local Markdown file from the working tree.
- Added reader-doc location validation for public-reader doc inputs, so
  `--extra-doc` is limited to `README.md` or tracked `docs/*.md` reader
  documents instead of arbitrary tracked Markdown support files.
- Added symlink rejection for public-reader package sources, so a tracked or
  extra Markdown path cannot package bytes from an out-of-tree target through a
  symbolic link.
- Added regular-file and destination-symlink guards for public-reader package
  copying, so package inputs cannot be directories and `--no-clean` output
  trees cannot write through an existing symbolic-link destination, output
  root, or package subdirectory.
- Added an independent public-reader package manifest verifier and wired it
  into `make public-reader-package-check`, so the temporary release package
  must have its generated files, file count, source paths, package paths, byte
  counts, and SHA-256 hashes match `package_manifest.json`.
- The new verifier exposed and fixed the package-root README collision: the
  repository `README.md` now lands at `docs/REPOSITORY_README.md`, leaving the
  generated package `README.md` intact and hash-verifiable.
- Tightened the verifier so stale unmanifested files left in a package output
  directory are rejected instead of being silently shipped alongside the
  manifest-covered reader files.
- Tightened the verifier so manifest `source` paths must also stay relative,
  supported, and outside raw/source-data locations.
- Tightened the verifier so generated package `README.md` and
  `reader_package.md` must be reproducible from the manifest and packaged
  files, preventing stale or hand-edited package docs from passing hash checks.
- Tightened the verifier so required default package sources must remain in the
  manifest, preventing a package from omitting a whitelisted reader document
  while otherwise keeping generated docs internally consistent.
- Tightened the verifier so manifest package paths must match the package
  builder's source-to-output mapping, including the repository README override
  to `docs/REPOSITORY_README.md`.
- Tightened the verifier so package `git_head` must match the current repo
  HEAD, catching a stale ignored reader package after a new commit.
- Tightened the verifier so the packaged real-report summary's visible
  `Commit:` line must match the package manifest HEAD, catching a package built
  around a stale formal summary.
- Tightened the verifier so the packaged real-report JSON manifest's `commit`
  field must match the package manifest HEAD, catching stale machine-readable
  formal-run metadata too.
- This is a reader-export guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## Real-Report Doc Direct Gate

- Wired `scripts/check_real_report_run_doc.py` directly into `make
  fast-validate` and `make public-release-check`, instead of relying only on
  the formal real-report preflight path to catch real-report documentation
  drift.
- Updated README validation descriptions and Makefile guard tests so the
  direct real-report documentation gate remains visible in both dirty-safe and
  clean release checks.
- Tightened the direct real-report documentation gate so duplicate
  `real_report_run` protocol step ids fail explicitly, instead of allowing a
  repeated TOML step block to collapse inside the structural lookup.
- Added a direct protocol-runner regression test for duplicate step ids, so the
  shared protocol loader guard remains covered outside the real-report wrapper.
- Added a protocol-file checker regression test so duplicate step-id loader
  errors stay surfaced through the release-gate protocol-file check.
- Added term metadata guard tests for required constant values, duplicate
  constant values, required gematria schemes, and bad gematria scheme metadata.
- Tightened the term-file checker so invalid `gematria_schemes.toml` reports a
  structured failure instead of escaping as a raw TOML parser exception.
- Tightened the term-file checker so malformed `schemes` metadata reports
  structured failures instead of escaping as type errors.
- Added corpus-config edge-case tests for invalid TOML, missing source blocks,
  and non-table source entries.
- Tightened the CRD relevance-dictionary checker so invalid TOML reports a
  structured configuration failure through the CLI.
- Tightened the shared CRD relevance loader so invalid dictionary TOML reports
  the same structured configuration failure for classifier callers.
- Tightened CRD relevance dictionary entry-shape validation so malformed
  `entries` metadata fails before parser internals see it.
- This is a documentation guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## Final-Report Assembly Direct Gate

- Wired `scripts/check_final_report_assembly_docs.py` directly into `make
  fast-validate` and `make public-release-check`, instead of relying only on
  formal real-report preflight to catch final-report boundary drift.
- Updated README validation descriptions and Makefile guard tests so the
  final-report assembly docs remain visible in both dirty-safe and clean
  release checks.
- This is a documentation guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## Top-Reader Summary Doc Direct Gate

- Wired `scripts/check_consolidated_findings_doc.py`,
  `scripts/check_claim_catalog_doc.py`,
  `scripts/check_final_report_highlights_doc.py`, and
  `scripts/check_strongest_candidate_deep_dive_doc.py` directly into `make
  fast-validate` and `make public-release-check`.
- Updated README validation descriptions and Makefile guard tests so the
  reader-facing summary packet is checked in both dirty-safe and clean release
  paths, not only during formal real-report preflight.
- This is a documentation guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## Prospective Workflow Doc Direct Gate

- Wired `scripts/check_prospective_lane_status_doc.py`,
  `scripts/check_study_lock_manifests_doc.py`,
  `scripts/check_prospective_study_readiness_doc.py`, and
  `scripts/check_prospective_study_next_lock_doc.py` directly into `make
  fast-validate` and `make public-release-check`.
- Updated README validation descriptions and Makefile guard tests so the
  prospective workflow docs are checked in both dirty-safe and clean release
  paths, not only during formal real-report preflight.
- This is a documentation guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## Public Handoff Doc Direct Gate

- Wired `scripts/check_wrr_public_handoff_docs.py`,
  `scripts/check_cities_public_handoff_docs.py`,
  `scripts/check_kjva_public_handoff_docs.py`,
  `scripts/check_wrr_no_input_handoff_status_doc.py`,
  `scripts/check_cities_no_input_handoff_status_doc.py`, and
  `scripts/check_kjva_no_input_handoff_status_doc.py` directly into `make
  fast-validate` and `make public-release-check`.
- Updated README validation descriptions and Makefile guard tests so public
  handoff/no-input docs are checked in both dirty-safe and clean release paths,
  not only during formal real-report preflight.
- This is a documentation guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## Reader-Doc Check Target Consolidation

- Added `make reader-doc-checks` as the shared Make target for the
  reader-facing documentation guard list.
- Updated `make fast-validate` and `make public-release-check` to call the
  shared target, so the long reader-doc checker list is maintained in one
  place.
- Updated README validation guidance and Makefile guard tests to keep the
  shared target visible.
- This is a Makefile/validation maintenance change only. It does not change
  report conclusions, source policy, imported texts, ELS searches, or result
  status.

## Study-Support Direct Gate

- Added `make study-support-checks` for centered-occurrence, critical-omission
  follow-up, English corpus policy, English seed-survivor, Greek second-cohort,
  hypothesis/source audit, Israeli Prime Ministers detail recovery, KJVA
  prospective boundary, manual-review, preregistration placeholder,
  prospective-lane, research missing-model, source-basis, and study-lock
  manifest drift guards.
- Wired the shared target into `make fast-validate` and
  `make public-release-check`, so non-lane support docs and planning guards are
  checked before both dirty-safe handoffs and clean releases.
- Updated README validation guidance and Makefile guard tests to keep the
  shared target visible.
- This is a documentation/validation guard only. It does not change report
  conclusions, source policy, imported texts, ELS searches, or result status.

## Default Check Coverage Guard

- Added a Makefile coverage test requiring every default-safe
  `scripts/check_*.py` module to be reachable through a Make validation target.
- The preregistration placeholder checker is now called through
  `make study-support-checks` against all concrete preregistration docs.
- Historical study-lock manifest drift is now summarized in
  `docs/STUDY_LOCK_MANIFEST_DRIFT_AUDIT.md`, regenerated locally during
  `make study-support-checks`, and checked without tracking ignored
  `reports/` artifacts.
- The only current exception is `check_study_lock_manifest`, because historical
  lock manifests require explicit manifest paths/settings and many old
  fingerprints intentionally fail after later documentation/tooling edits.
- This is a validation guard only. It does not change report conclusions,
  source policy, imported texts, ELS searches, or result status.

## KJVA Source-Doc Direct Gate

- Added `make kjva-source-doc-checks` for the KJVA source-candidate,
  source-lock, source-policy, Hakkaac/Gutenberg/Wikisource/Open-Bibles, and
  next-replication documentation guards.
- Wired the shared target into `make fast-validate` and
  `make public-release-check`, so KJVA source-policy support docs are checked
  before both dirty-safe handoffs and clean releases.
- Updated README validation guidance and Makefile guard tests to keep the
  shared target visible.
- This is a documentation/validation guard only. It does not change report
  conclusions, source policy, imported texts, ELS searches, or result status.

## WRR Doc Direct Gate

- Added `make wrr-doc-checks` for the WRR method, source-policy,
  source-recovery, source-row, manual-decision, variant-gap, and local-lock
  support documentation guards.
- Wired the shared target into `make fast-validate` and
  `make public-release-check`, so WRR support docs are checked before both
  dirty-safe handoffs and clean releases.
- Updated README validation guidance and Makefile guard tests to keep the
  shared target visible.
- This is a documentation/validation guard only. It does not change report
  conclusions, source policy, imported texts, ELS searches, or result status.

## Cities Doc Direct Gate

- Added `make cities-doc-checks` for the Cities claim-boundary, PDF recovery,
  source-review, source-row, source-page OCR, line-crop, unreadable-PDF,
  decision-record, and no-input handoff documentation guards.
- Wired the shared target into `make fast-validate` and
  `make public-release-check`, so Cities source/recovery support docs are
  checked before both dirty-safe handoffs and clean releases.
- Updated README validation guidance and Makefile guard tests to keep the
  shared target visible.
- This is a documentation/validation guard only. It does not change report
  conclusions, source policy, imported texts, ELS searches, or result status.

## Clean-Lock Results Summary Guard

- Added a dedicated guard for `docs/CLEAN_LOCK_RESULTS_SUMMARY.md` so the
  summary must retain its no-claim status, KJVA legacy-lock caveat, lane counts,
  strict-gate reads, required report links, and local reference existence.
- Wired the guard into real-report preflight, `make fast-validate`, and
  `make public-release-check`, with unit tests covering the current document,
  required phrase drift, required reference drift, and forbidden positive claim
  language.
- This is a documentation guard only. It does not change source policy,
  imported texts, ELS searches, report conclusions, or result status.

## Public-Reader Package Protocol Guard

- Added public-reader package guards for the real-report manifest metrics,
  including Greek surface, length-4, WRR, matrix/strata, centered-occurrence,
  KJVA bridge, and `step_tahot` summary fields.
- The package checker now rejects new unguarded real-report manifest keys,
  missing real-report protocol steps, duplicate real-report protocol step ids,
  and stale protocol step ids no longer present in
  `protocols/real_report_run.toml`.
- The generated public-reader package is now checked against the current
  real-report protocol step list before release or handoff.
- This is a packaging/validation guard only. It does not change source policy,
  imported texts, ELS searches, report conclusions, or result status.
