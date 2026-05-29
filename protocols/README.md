# Protocols

Protocol files freeze run settings before analysis:

- input paths
- source configs
- term lists
- skip bounds
- direction
- output paths
- expected follow-up indexes/manifests

Run:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml
```

Dry run:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --dry-run
```

Formal report assembly run:

```bash
make real-report
# equivalent:
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

This runs preflight checks, refreshes locked STEP_TAHOT and Greek exact-center
final gates with resume, refreshes WRR source/import audit state and the
current WRR repo-defined diagnostic status, validates prospective-lane and
English source-basis metadata, validates expanded-strata tooling docs, future
study-mapping CSV schemas, and concrete preregistration placeholder cleanup,
checks the locked CRD relevance dictionary basis, verifies manual-review queue
guardrails, keeps WRR method-status, lock-options, claim-readiness, and
blocker-packet wording visible, builds the generated report index, and writes
`reports/real_report_run/summary.md`.
Tracked plan: `docs/REAL_REPORT_RUN.md`.

Run one step:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --only batch_term_sets
```

Broader screening run:

```bash
python3 -m scripts.run_protocol protocols/broad_search.toml --resume
```

This keeps the fixed public baseline at skip `2..50` while also offering a
separate skip `2..100` sweep over every declared term list. Tracked summary:
`docs/BROAD_SEARCH_FINDINGS.md`.

Focused wide modern/prophetic screening run:

```bash
python3 -m scripts.run_protocol protocols/wide_focus_search.toml --resume
```

This keeps the broader all-list sweep at skip `2..100` while adding a focused
skip `2..250` run for modern/geopolitical/local and prophetic rows. Tracked
summary: `docs/WIDE_FOCUS_SEARCH.md`.

Focused wide exact-hit version-presence follow-up:

```bash
python3 -m scripts.run_protocol protocols/wide_focus_exact_presence.toml --resume
```

This exports capped exact ref-key patterns for length 4+ rows from the same
modern/geopolitical/local and prophetic focus set. Tracked summary:
`docs/WIDE_FOCUS_EXACT_PRESENCE.md`.

Focused wide paired-control follow-up:

```bash
python3 -m scripts.run_protocol protocols/wide_focus_paired_controls.toml --resume
```

This runs representative shuffled-term and same-length random controls for
nonzero wide-focus rows in MT_WLC, UHB, LXX, TR_NT, and SBLGNT. Tracked
summary: `docs/WIDE_FOCUS_PAIRED_CONTROLS.md`.

WRR source audit:

```bash
python3 -m scripts.run_protocol protocols/wrr_source_import.toml --resume
```

This downloads external WRR audit files into ignored reports output and converts
the WRR2 plain-text list into repo term rows without committing third-party
data. It also summarizes the raw ANU famous-rabbis source-list shapes so the
163-distance mismatch stays visible alongside the locked local method reports.
Tracked audit: `docs/WRR_SOURCE_AUDIT.md`; selected local summary:
`docs/WRR_LOCKED_METHOD_REPORT.md`; exact-reproduction gap map:
`docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md`.

Co-linear ELS source audit:

```bash
python3 -m scripts.run_protocol protocols/colinear_els_source_audit.toml --resume
```

This parses the Bombach/Gans co-linear ELS paper, attachment index, and linked
PDF tables into source-shape counts. It records source coverage, row counts,
raw PLS pair rows, raw roots rows, raw all_1698 phrase/verse rows, and raw
reviewed subset rows. It also records Hebrew-method appendix anchors without
normalizing Hebrew terms, computing ELSs, scoring verse links, or evaluating
controls. Tracked audit: `docs/COLINEAR_ELS_SOURCE_AUDIT.md`.

Gans communities source-shape audit:

```bash
python3 -m scripts.run_protocol protocols/gans_communities_source_audit.toml --resume
```

This parses the Gans/Inbal/Bombach communities data PDF into ignored record
and community-row source outputs and writes a tracked source-boundary summary.
It also supplies existing source-shape coverage for the Cities extractable
data-table lane. It does not run ELS hits or compactness statistics. Tracked audit:
`docs/GANS_COMMUNITIES_SOURCE_AUDIT.md`.

American presidents source-shape audit:

```bash
python3 -m scripts.run_protocol protocols/american_presidents_source_audit.toml --resume
```

This parses the Torah-code.org American presidents data PDF and linked
transliteration-rule PDF into ignored source-shape and spelling-row outputs. It
does not choose variants, run ELS hits, or evaluate controls. Tracked audit:
`docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md`.

Witztum birth-date source-shape audit:

```bash
python3 -m scripts.run_protocol protocols/witztum_birth_dates_source_audit.toml --resume
```

This parses the Witztum Genesis birth-date paper and data PDFs into ignored
source-shape outputs for the S1/S2 sample tables. It does not normalize terms,
run ELS/SL proximity, or rerank permutations. Tracked audit:
`docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md`.

Israeli prime-ministers source-shape audit:

```bash
python3 -m scripts.run_protocol protocols/israeli_prime_ministers_source_audit.toml --resume
```

This parses the Torah-code.org Israeli prime-ministers main page, keyword PDF,
and downloaded detail pages into ignored source-shape, PDF keyword-row, and
detail-page outputs. It records the current detail-page coverage gap without
normalizing terms or testing ELS results. Tracked audit:
`docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md`.

Israeli prime-ministers detail-page recovery probe:

```bash
python3 -m scripts.run_protocol protocols/israeli_prime_ministers_detail_recovery_probe.toml --resume
```

This live-checks the missing `_9` through `_12` detail-page URLs in an isolated
ignored directory and writes
`docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md`. It does not infer
missing detail-page data or run result-bearing ELS work.

Cities source-chain audit:

```bash
python3 -m scripts.run_protocol protocols/cities_source_chain_audit.toml --resume
```

This classifies Torah-code.org Cities/Aumann/Simon-McKay HTML pages and
PDF-shaped downloads. It records wrapper downloads, Wayback job-failed wrapper
status, parse status, and source anchors without normalizing city names or
testing ELS results. Tracked audit:
`docs/CITIES_SOURCE_CHAIN_AUDIT.md`.

Cities PDF recovery probe:

```bash
python3 -m scripts.run_protocol protocols/cities_pdf_recovery_probe.toml --resume
```

This live/archive probe checks the 35 PDF links found on the Cities, Aumann,
and Simon-McKay source pages in an isolated ignored output directory. It
currently recovers 12 archived PDFs and leaves 23 links unrecovered. It does
not overwrite the cached `reports/wrr_1994/` bundle, perform OCR, normalize
city names, or run ELS results. Tracked probe:
`docs/CITIES_PDF_RECOVERY_PROBE.md`.

Cities recovered-PDF text audit:

```bash
python3 -m scripts.run_protocol protocols/cities_recovered_pdf_text_audit.toml --resume
```

This classifies the 12 recovered Cities/Aumann/Gans PDFs by extractable text
shape and checks five title/protocol anchors. It does not run OCR, normalize
city names, run ELS results, compute compactness, or verify p-levels. Tracked
audit: `docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md`.

Cities source-review queue:

```bash
python3 -m scripts.run_protocol protocols/cities_source_review_queue.toml --resume
```

This joins the 35-row recovery probe and 12-row recovered-PDF text audit into
next-action lanes: extractable-text review, OCR/image-only review,
encoding-or-OCR candidate, and missing-PDF recovery. It does not decide source
admissibility or run result-bearing work. Tracked queue:
`docs/CITIES_SOURCE_REVIEW_QUEUE.md`.

Cities unreadable-PDF review:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_review.toml --resume
```

This classifies the seven recovered but unreadable Cities PDFs into
OCR/image-only and encoding-or-OCR planning routes. It does not run OCR, repair
text, import source rows, normalize city names, or run result-bearing work.
Tracked review: `docs/CITIES_UNREADABLE_PDF_REVIEW.md`.

Cities unreadable-PDF OCR feasibility:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_feasibility.toml --resume
```

This runs local English OCR against the seven recovered unreadable PDFs and
records counts/status only. It does not track OCR text, repair text, import
source rows, normalize city names, or run result-bearing work. Tracked review:
`docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md`.

Cities unreadable-PDF OCR review packet:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_review_packet.toml --resume
```

This renders ignored local page-image and OCR-text sidecars for the same 41
pages and records paths/counts/status only. It does not track OCR text, repair
text, import source rows, normalize city names, or run result-bearing work.
Tracked review: `docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md`.

Cities unreadable-PDF OCR review checklist:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_review_checklist.toml --resume
```

This groups the ignored local sidecars into review order and contact sheets.
It does not track OCR text, repair text, import source rows, normalize city
names, or run result-bearing work. Tracked review:
`docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md`.

Cities unreadable-PDF OCR page review:

```bash
python3 -m scripts.run_protocol protocols/cities_unreadable_pdf_ocr_page_review.toml --resume
```

This records visual page-role decisions for all 41 OCR packet pages. It does
not track OCR body text, repair text, import source rows, normalize city names,
or run result-bearing work. Tracked review:
`docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md`.

Cities source-row lock queue:

```bash
python3 -m scripts.run_protocol protocols/cities_source_row_lock_queue.toml --resume
```

This filters reviewed OCR page roles into 14 table/list/exception-note
candidate pages that need separate citable source-row locks before any data
use. It does not import source rows, normalize city names, or run
result-bearing work. Tracked queue: `docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md`.

Cities source-row lock worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_row_lock_worksheet.toml --resume
```

This assigns stable decision ids and evidence prompts to the 14 source-row
lock candidates. It does not transcribe rows, import source text, normalize
city names, or run result-bearing work. Tracked worksheet:
`docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md`.

Cities source-row lock evidence packet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_row_lock_evidence_packet.toml --resume
```

This joins the 14 source-row lock worksheet rows to recovered PDF metadata,
checksums, and page-image paths. It does not copy OCR text, transcribe rows,
import source text, normalize city names, or run result-bearing work. Tracked
packet: `docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md`.
Cities source-row lock handoff: 14 source-row lock candidate pages, 14
populated lock rows, and 14 pending transcription-review rows; no source rows
imported, and no city-name normalization, ELS searches, compactness runs, or
p-levels. Current decision-record paths:
`data/study/mappings/cities_source_row_lock_decisions.csv` and
`data/study/mappings/cities_source_transcription_decisions.csv`.

Cities source-transcription review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_transcription_review_worksheet.toml --resume
```

This organizes the 14 locked source pages for later readable transcription and
row/column alignment review. It does not copy source-script text, import source
text, normalize city names, or run result-bearing work. Tracked worksheet:
`docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md`.

Cities source-page review bundle:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_review_bundle.toml --resume
```

This verifies the 14 locked source-page image paths and dimensions for later
manual review. It does not run OCR, transcribe rows, import source text,
normalize city names, or run result-bearing work. Tracked bundle:
`docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md`.

Cities source-page contact sheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_contact_sheet.toml --resume
```

This renders the 14 locked source-page images into a local contact sheet for
manual review. The contact-sheet image stays in ignored reports output; tracked
files contain no source-script body text and still import no source rows.
Tracked doc: `docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md`.

Cities source-page OCR review packet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_ocr_review_packet.toml --resume
```

This runs local Hebrew OCR against the 14 locked source-page images and writes
ignored OCR text sidecars for manual review. Tracked files contain counts,
paths, and status only; they contain no OCR body text, no source-script body
text, no source-row import, no city-name normalization, and no result-bearing
work. Tracked doc: `docs/CITIES_SOURCE_PAGE_OCR_REVIEW_PACKET.md`.

Cities source-page OCR HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_ocr_review_html.toml --resume
```

This writes an ignored local HTML page that places each locked source-page
image beside its OCR sidecar text. The HTML may contain OCR body text for local
review, but tracked files contain only paths/counts/status and still import no
source rows. Tracked doc: `docs/CITIES_SOURCE_PAGE_OCR_REVIEW_HTML.md`.

Cities source-page line crop packet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_packet.toml --resume
```

This runs local Hebrew OCR TSV against the 4 table candidate source pages and
writes ignored crop images for detected text lines. Tracked files contain only
paths/counts/status and still contain no OCR body text, no source-script body
text, no source-row import, no city-name normalization, and no result-bearing
work. Tracked doc: `docs/CITIES_SOURCE_PAGE_LINE_CROP_PACKET.md`.

Cities source-page line crop contact sheets:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_contact_sheet.toml --resume
```

This writes 4 ignored local contact-sheet images for the 203 line crops, one
per table candidate page. The sheets support non-transcription visual review
of crop order and row shape. Tracked files contain only paths/counts/status and
still import no source rows. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_CONTACT_SHEET.md`.

Cities source-page line crop HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_review_html.toml --resume
```

This writes an ignored local HTML gallery of the 203 source-page line-crop
images from the 4 table candidate pages. The HTML displays crop images only
and embeds no OCR text or source-script text. Tracked files contain only
paths/counts/status and still import no source rows. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_HTML.md`.

Cities source-page line crop triage:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_triage.toml --resume
```

This writes a 203-row no-input triage queue for the table-candidate line
crops. It ranks crops by layout and OCR-count signal only; it does not read
Hebrew, transcribe rows, import source rows, normalize city names, or run
result-bearing work. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE.md`.

Cities source-page line crop band map:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_map.toml --resume
```

This writes a coordinate-only map grouping adjacent line crops by vertical
gaps. It contains no OCR body text or source-script text and imports no source
rows. Tracked doc: `docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_MAP.md`.

Cities source-page line crop band review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_review_worksheet.toml --resume
```

This writes a 16-row worksheet for later visual review of the coordinate bands.
It contains no OCR body text or source-script text and imports no source rows.
Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_WORKSHEET.md`.

Cities source-page line crop band contact sheets:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_contact_sheet.toml --resume
```

This writes ignored local PNG contact sheets grouped by the 16 coordinate
bands. The tracked files contain only paths/counts/status and still import no
source rows or source-script text. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_CONTACT_SHEET.md`.

Cities source-page line crop band HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_band_review_html.toml --resume
```

This writes an ignored local HTML gallery of the 16 band contact-sheet images.
The HTML displays images only and embeds no OCR text or source-script text.
Tracked files contain only paths/counts/status and still import no source rows.
Tracked doc: `docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_HTML.md`.

Cities source-page line crop triage HTML:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_triage_html.toml --resume
```

This writes an ignored local HTML gallery of the 203 source-page line-crop
images in triage priority order. The HTML displays crop images only and embeds
no OCR text or source-script text. Tracked files contain only
paths/counts/status and still import no source rows. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE_HTML.md`.

Cities source-page line crop priority contact sheets:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_priority_contact_sheet.toml --resume
```

This writes ignored local PNG contact sheets grouped by triage priority. The
tracked files contain only paths/counts/status and still import no source rows
or source-script text. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_CONTACT_SHEET.md`.

Cities source-page line crop priority HTML review aid:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_priority_review_html.toml --resume
```

This writes an ignored local HTML gallery of the 4 priority contact-sheet
images. The HTML displays images only and embeds no OCR text or source-script
text. Tracked files contain only paths/counts/status and still import no
source rows. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_HTML.md`.

Cities source-page line crop priority review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_priority_review_worksheet.toml --resume
```

This writes a 203-row priority-ordered worksheet joining triage rank, crop
paths, and priority contact-sheet paths. It contains no OCR body text or
source-script text and imports no source rows. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_WORKSHEET.md`.

Cities source-page line crop review worksheet:

```bash
python3 -m scripts.run_protocol protocols/cities_source_page_line_crop_review_worksheet.toml --resume
```

This writes a 203-row worksheet for later human review of the table-candidate
line crops. It records crop paths, dimensions, and review-state fields only;
it does not transcribe rows, embed OCR text, import source rows, normalize city
names, or run result-bearing work. Tracked doc:
`docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_WORKSHEET.md`.

Cities extractable-text role review:

```bash
python3 -m scripts.run_protocol protocols/cities_extractable_text_review.toml --resume
```

This classifies the five extractable Cities PDFs into data-table,
method-context, and commentary/critique source-review roles. The data-table
candidate is linked to the Gans communities source-shape audit with 66 records
and 210 community rows. It does not import source rows, normalize city names,
or run result-bearing work. Tracked review:
`docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md`.

Event/object experiment source audit:

```bash
python3 -m scripts.run_protocol protocols/event_object_experiments_source_audit.toml --resume
```

This parses the Sons of Haman, Pumbedita, Auschwitz, and Ark source pages plus
linked data/tutorial PDFs into ignored source-shape and source-row outputs. It
records declared status and 65 machine-readable source rows without normalizing
spellings or testing ELS results. Tracked audit:
`docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md`.

Under-construction experiment source audit:

```bash
python3 -m scripts.run_protocol protocols/under_construction_experiments_source_audit.toml --resume
```

This records source-status placeholders for Chumash, Twin Towers, Tsunami,
Katrina, Great Rabbis, and Son Rabbis experiment pages. It also records copied
title/heading anomalies so those pages are not treated as data-bearing sources.
Tracked audit: `docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md`.

Research missing model pages audit:

```bash
python3 -m scripts.run_protocol protocols/research_missing_model_pages_audit.toml --resume
```

This records that the linked Torah-code.org level-2/3 geometric and ELS model
pages currently download as root-canonical pages with unrelated slot/gambling
content and no expected model labels. Tracked audit:
`docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md`.
For targeted recovery probes without refreshing the entire source bundle, use
`scripts.download_wrr_sources --refresh --label <source_label>`; the manifest
records both requested URL and final URL so root redirects are visible.

WRR source recovery probe:

```bash
python3 -m scripts.run_protocol protocols/wrr_source_recovery_probe.toml --resume
```

This live-refreshes selected Torah-code research labels into the isolated
ignored `reports/wrr_source_recovery_probe/` directory and writes
`docs/WRR_SOURCE_RECOVERY_PROBE.md`. It does not overwrite cached
`reports/wrr_1994/` source files. It checks the same 18 research URL variants
used by the Wayback probe, including `.html` labels and stale-indexed `.shtml`
alternates.

WRR Wayback source recovery probe:

```bash
python3 -m scripts.run_protocol protocols/wrr_wayback_source_recovery_probe.toml --resume
```

This probes archived Torah-code research snapshots into the isolated ignored
`reports/wrr_wayback_source_recovery_probe/` directory and writes
`docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md`. It currently recovers five usable
archived research/model concepts while leaving level-2/3 geometric and ELS
model pages missing.

WRR imported-term Genesis count and pair smoke:

```bash
python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume
```

This counts the imported WRR2 appellation/date rows in Koren Genesis, emits a
same-record appellation/date pair audit, and control-screens the top raw pair
rows. It also repeats the pair audit/control screen with the WRR
appendix-compatible `5..8` length filter, audits expected-count skip caps, and
now collapses the residual pair packet into
`docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md` for unique unresolved-term
review after the simple-variant upper-bound diagnostic.
It also samples WRR-style perturbation boundary and exact-match validity, then joins
that diagnostic back to the lock-prep pair table. It now also emits a
corrected-distance smoke table from generated perturbed rows for the 5..8
candidate lane, a full selected-universe cap-1000 corrected-distance output,
and a variant comparison for term-printed, term-program, and fixed-250 skip
settings. It also writes `docs/WRR_METHOD_STATUS.md`, a compact matrix of
current locks, exact-published-reproduction caveats, and next actions. It
fingerprints the Koren Genesis source stream, checks primary-PDF method anchors,
source-locks the primary Table 2 row labels and Table 3 published rank rows,
bridges Table 2 row labels to secondary WRR2 record counts, runs a
probe-only Hebrew OCR check against those secondary terms, and emits a pair-table
reconciliation for the current imported-pair count versus the source-cited
163-distance WRR second-list sample. It also reads the current repo-defined
999,999 date-label permutation diagnostic into the WRR method-status matrix,
emits source-policy scenario impact, emits D(w) formula sensitivity, and gathers
lock options plus the claim-blocker packet, including visual triage notes. It
also runs the method-lane wide-skip probe: the 11 OCR-matched method-lane terms
have 0 ordinary Genesis hits through skip 5000, so that lane is not explained
by a small cap extension.
It also writes `docs/WRR_SOURCE_ROW_CROP_REVIEW_HTML.md`, an ignored local
HTML review aid that displays the 22 generated source-row crop images only,
without OCR body text, source-script text, row transcription, source
correction, pair exclusion, or method change.
It is locked local evidence, not an exact WRR reproduction.

Hebrew MT-family version comparison:

```bash
python3 -m scripts.run_protocol protocols/mt_version_comparison.toml --resume
```

This aligns MT_WLC, UXLC, MAM, eBible WLC, and UHB by canonical book/chapter/verse
and reports normalized consonantal verse differences. Tracked summary:
`docs/MT_VERSION_COMPARISON.md`.

Hebrew exact-hit MT-family version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_hit_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_controlled_review.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_screening_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_screening_controlled_review.toml --resume
```

The focused protocol compares selected modern/local Hebrew ELS hit ref-key
patterns across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB. The broader
modern/geopolitical protocol applies the same check to every Hebrew row in
`terms/modern_names_dates.csv`. The controlled-review protocol runs
representative MT_WLC/UHB paired controls for the nonzero rows from that broad
modern/geopolitical matrix. The broader screening protocol applies the same
check to Hebrew rows from theological, modern, Table of Nations, prophetic,
Hebrew claim, tribe, festival, and calendar files. The broader screening
controlled-review protocol runs the same representative MT_WLC/UHB paired
controls over nonzero broader-screening rows. Tracked summaries:
`docs/HEBREW_HIT_VERSION_PRESENCE.md`,
`docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`,
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`,
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md`,
`docs/HEBREW_SCREENING_VERSION_PRESENCE.md`,
`docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md`, and
`docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md`.

Compiled Hebrew claim-term version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_claim_version_presence.toml --resume
```

This compares exact hit ref-key patterns for `terms/hebrew_claim_terms.csv`
across the same Hebrew MT-family source set. Tracked summary:
`docs/HEBREW_CLAIM_VERSION_PRESENCE.md`.

Hebrew null/frequency control version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_control_version_presence.toml --resume
```

This compares exact hit ref-key patterns for `terms/null_controls.csv` and
`terms/frequency_anchors.csv` across the same Hebrew MT-family source set.
Tracked summary: `docs/HEBREW_CONTROL_VERSION_PRESENCE.md`.

STEP_TAHOT null/frequency control version-presence follow-up:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_version_presence.toml --resume
```

This repeats the Hebrew null/frequency control screen with `STEP_TAHOT` added as
a selected sixth stream. Tracked summary:
`docs/STEP_TAHOT_CONTROL_VERSION_PRESENCE.md`.

STEP_TAHOT null/frequency control source-policy follow-up:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_policy_hits.toml --resume
```

This audits the `STEP_TAHOT`-only control rows against TAHOT source-type paths.

STEP_TAHOT final gate:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_final_gate.toml --resume
```

This joins the real-term and control-term source-only rates plus source-policy
audits into one held/review table. Tracked summary:
`docs/STEP_TAHOT_FINAL_GATE.md`.

Comparison across the Hebrew modern, claim, and control version-presence runs:
`docs/HEBREW_VERSION_PRESENCE_COMPARISON.md`.
Source-specific Hebrew distribution:
`docs/HEBREW_VERSION_SPECIFIC_DISTRIBUTION.md`.

Focused deep exact-center extension controls:

```bash
python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume
```

This runs the slower 1000/1000 paired-control follow-up for the `δοξα`
cross-text exact-center extension row. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`.

Locked Greek exact-center theological cohort:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_cohort.toml --resume
```

This derives exact-center, cross-text Greek NT extension candidates from
`terms/greek_exact_center_cohort_terms.csv` and runs 1000/1000 controls.
Preregistration: `docs/GREEK_EXACT_CENTER_COHORT_PREREGISTRATION.md`.
Tracked report: `docs/GREEK_EXACT_CENTER_COHORT_REPORT.md`. It also emits
`reports/greek_exact_center_cohort/pattern_presence.csv` so source-specific
patterns remain visible.

Greek exact-center final gate:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_final_gate.toml --resume
```

This consolidates version presence, row-local controls, context review, and
synthetic baselines into candidate-type labels. Hidden-path-only findings are
candidate types, not failures. Tracked summary:
`docs/GREEK_EXACT_CENTER_FINAL_GATE.md`.

Post-screen expanded Greek surface review:

```bash
python3 -m scripts.run_protocol protocols/greek_expanded_surface_queue.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_triage.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_letter_paths.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_available_control_evaluation.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_followup.toml --resume
```

This keeps exact-center surface rows visible even when no same-skip phrase
extension survives. The letter-path audit reconstructs the selected ELS paths
across TR_NT, BYZ_NT, TCG_NT, and SBLGNT. Tracked summaries:
`docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`,
`docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`, and
`docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`. Compact
selected-row follow-up:
`docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`.

Locked Greek surface prospective cohort:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_prospective.toml --resume
```

This uses `terms/greek_surface_prospective_terms.csv`, which is the expanded
Greek prospective list after removing prior selected surface rows. It writes a
new prospective surface-context screen, queue, triage table, all-available
surface-frequency controls, and letter-path audit under
`reports/greek_surface_prospective/`. Preregistration:
`docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md`. Tracked compact report:
`docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`.

Registered Hebrew theology follow-up cohort:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_prospective.toml --resume
```

This uses `terms/hebrew_theology_prospective_terms.csv` for a fixed 20-row
Hebrew theology cohort across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB. It writes
exact version-presence rows, representative MT_WLC/UHB paired controls, and a
tracked report under `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md`.
Preregistration: `docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md`.
Findings summary: `docs/HEBREW_THEOLOGY_PROSPECTIVE_FINDINGS.md`.

Relaxed all-codes collection for the same Hebrew theology cohort:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_all_codes_collection.toml --resume
```

This writes all hidden-path rows with `--include-all` under
`reports/hebrew_theology_all_codes/` and tracks a compact summary at
`docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md`. The row export now distinguishes
same center-word surface matches from broader center-verse surface matches. It
also tracks a ranked review queue at
`docs/HEBREW_THEOLOGY_ALL_CODES_TRIAGE.md`.

Broader relaxed all-codes collections:

```bash
python3 -m scripts.run_protocol protocols/hebrew_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/english_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_selection.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_letter_paths.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_context.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_extensions.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_controls.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_review.toml --resume
```

These retain every hidden-path row for the broader Hebrew, Greek, and English
KJV screening
cohorts and track compact summaries at
`docs/HEBREW_SCREENING_ALL_CODES_COLLECTION.md` and
`docs/GREEK_SCREENING_ALL_CODES_COLLECTION.md`, and
`docs/ENGLISH_SCREENING_ALL_CODES_COLLECTION.md`. Ranked review queues are
tracked at `docs/HEBREW_SCREENING_ALL_CODES_TRIAGE.md` and
`docs/GREEK_SCREENING_ALL_CODES_TRIAGE.md`, and
`docs/ENGLISH_SCREENING_ALL_CODES_TRIAGE.md`. The follow-up selection protocol
deduplicates those queues into `docs/ALL_CODES_FOLLOWUP_SELECTION.md`; the
letter-path audit protocol reconstructs every selected hidden path at
`docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`; the context protocol exports
center/span excerpts at `docs/ALL_CODES_FOLLOWUP_CONTEXT.md`; the extension
protocol audits same-skip before/after lexicon matches at
`docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`; compound-extension paired controls
are tracked at `docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`; the review
protocol packages the selected rows into `docs/ALL_CODES_FOLLOWUP_REVIEW.md`.

ChurchAges-style expected-count audit:

```bash
python3 -m scripts.run_protocol protocols/churchages_statistics_audit.toml --resume
```

This compares transcribed ChurchAges KJV observed counts against two
independent-letter expected-count baselines: the article's simplified
scatter-plot triangle and this repo's exact legal-window count. Tracked output:
`reports/churchages_statistics/audit.md`.

Post-discovery length-4 Greek surface follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_length4_followup.toml --resume
```

This controls and audits the all-source length-4 bucket exposed by the locked
Greek surface prospective run. It is not prospective discovery. Tracked
summaries: `docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md`,
`docs/GREEK_SURFACE_LENGTH4_CONTROL_POOL.md`,
`docs/GREEK_SURFACE_LENGTH4_CONTROL_EVALUATION.md`, and
`docs/GREEK_SURFACE_LENGTH4_LETTER_PATHS.md`.

Generated vocabulary-control follow-up for those length-4 rows:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_length4_vocabulary_controls.toml --resume
```

This builds a generated length-4 real Greek surface-vocabulary control universe
under ignored `reports/` output, then reruns exact-center surface controls.
Tracked summaries: `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROLS.md`,
`docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_POOL.md`, and
`docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md`.

Post-discovery SBLGNT source-only exact-center follow-up:

```bash
python3 -m scripts.run_protocol protocols/sblgnt_source_only_exact_center.toml --resume
```

This runs 1000/1000 controls for the SBLGNT-only `αιμα` and `υιος` exact-center
rows from the Greek exact-center cohort. Preregistration:
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md`. Tracked report:
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_REPORT.md`.

Post-discovery BYZ_NT source-only exact-center follow-up:

```bash
python3 -m scripts.run_protocol protocols/byz_source_only_exact_center.toml --resume
```

This runs 1000/1000 controls for the BYZ_NT-only `υιος` exact-center row from
the four-source Greek pattern-presence matrix. Preregistration:
`docs/BYZ_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md`. Tracked report:
`docs/BYZ_SOURCE_ONLY_EXACT_CENTER_REPORT.md`.

Locked Greek exact-center independent-source follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_three_source.toml --resume
```

This reruns the locked Greek exact-center cohort across TR_NT, BYZ_NT, and
SBLGNT, then controls only exact-center overlap groups that include the
independent Byzantine NT source. Preregistration:
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_PREREGISTRATION.md`. Tracked report:
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_REPORT.md`. It also emits
`reports/greek_exact_center_three_source/pattern_presence.csv` so
source-specific patterns remain visible.

Locked Greek exact-center added-source follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_four_source.toml --resume
```

This reruns the locked Greek exact-center cohort across TR_NT, BYZ_NT, TCG_NT,
and SBLGNT, then controls only exact-center overlap groups that include the
added eBible Text-Critical Greek NT source. Preregistration:
`docs/GREEK_EXACT_CENTER_FOUR_SOURCE_PREREGISTRATION.md`. Tracked report:
`docs/GREEK_EXACT_CENTER_FOUR_SOURCE_REPORT.md`. It also emits
`reports/greek_exact_center_four_source/pattern_presence.csv` so source-specific
patterns remain visible.

Consolidated Greek pattern/version summary:

```bash
python3 -m scripts.run_protocol protocols/greek_pattern_versions.toml --resume
```

This merges the two-source, three-source, four-source, and source-only control
outputs into one current-status table. Tracked report:
`docs/GREEK_PATTERN_VERSION_SUMMARY.md`.

Version-distribution reporting methodology is tracked in
`docs/VERSION_DISTRIBUTION_METHOD.md`.

Targeted modern/geopolitical/local version-presence join:

```bash
python3 -m scripts.run_protocol protocols/targeted_version_presence.toml --resume
```

This joins the broader Hebrew and Greek exact-version summaries with available
paired controls and bounded version-presence extension summaries, then runs
representative `2..100` paired controls for nonzero target rows and regenerates
a final controlled summary. Tracked summary:
`docs/TARGETED_VERSION_PRESENCE_REVIEW.md`.

Greek NT exact-hit version-presence screens:

```bash
python3 -m scripts.run_protocol protocols/greek_nt_claim_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/greek_control_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_version_presence.toml --resume
```

These compare exact ELS hit ref-key patterns across TR_NT, BYZ_NT, TCG_NT, and
SBLGNT for Greek NT claim terms and Greek null/frequency controls. Tracked
summaries: `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md`,
`docs/GREEK_CONTROL_VERSION_PRESENCE.md`, and
`docs/GREEK_VERSION_PRESENCE_COMPARISON.md`. The broader screening run covers
Greek rows from theological, modern, Table of Nations, prophetic, Greek NT
claim, tribe, and festival files; tracked summary:
`docs/GREEK_SCREENING_VERSION_PRESENCE.md`.
LXX/NT corpus-presence read from the broad search:
`docs/GREEK_LXX_NT_CORPUS_PRESENCE.md`.

Resume completed outputs:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume
```

Resume uses per-step integrity stamps under the manifest directory. Existing files
alone are not enough; input, command, and output fingerprints must match a prior
successful step. This avoids treating partial CSV/JSON output from an interrupted
run as cached and prevents stale resumes after term/config edits.

Set `always_run = true` on cheap summary/report steps whose output includes
volatile run metadata such as the current commit. That keeps expensive upstream
steps cached while refreshing the final local report text.

Long parallel groups print active-step heartbeats. Set
`progress_interval_seconds = 0` in a protocol file to silence them.

Benchmark repeated protocol runs:

```bash
python3 -m scripts.benchmark_protocol protocols/public_baseline.toml --runs 3
```

The benchmark writes ignored local reports under `reports/benchmarks/`:

- `public_baseline_benchmark.json`
- `public_baseline_benchmark.md`
- per-run protocol manifests

The public baseline also includes `els_controls`, which compares observed ELS
counts against shuffled-letter and shuffled-term controls. See
`docs/ELS_CONTROLS.md`.

The broad search protocol also emits `reports/broad_search/broad_version_presence.csv`,
which groups broad count rows by term and records which observed corpora contain
at least one hit.

The modern focus extension protocol runs a capped same-skip extension screen for
modern names, places, and local terms:

```bash
python3 -m scripts.run_protocol protocols/modern_focus_extensions.toml --resume
python3 -m scripts.run_protocol protocols/version_presence_extensions.toml --resume
```

It uses `surface-context --include-all` to collect capped hits, then runs
`els extensions` per corpus and summarizes phrase-extension rows under
`reports/modern_extension_screen/`.

The version-presence extension protocol exports bounded all-source Hebrew and
Greek version-presence rows into ordinary hit rows, then runs the same extension
workflow against MT_WLC, UHB, TR_NT, and SBLGNT. Tracked summary:
`docs/VERSION_PRESENCE_EXTENSION_SCREEN.md`.

The public baseline also derives TR NT and SBLGNT same-skip extension reports
from `surface_context_hits.csv`. Raw extension rows stay separate by corpus, then
`extension-summary` writes grouped counts and strongest compound-extension rows
with short-term noise filters enabled. See `docs/ELS_EXTENSIONS.md`.

See `docs/PUBLIC_BASELINE_FINDINGS.md` for the current plain-English findings
from the public baseline reports.

The `targeted_terms_report` step joins raw counts, controls, NT surface context,
and filtered extension tops for the current focused target set under
`reports/targeted_terms.*`.

Tracked summary: `docs/TARGETED_TERMS_FINDINGS.md`.

The `targeted_paired_controls` step compares each focused target row against
term-shuffle controls and same-length same-corpus random controls. Tracked
summary: `docs/TARGETED_PAIRED_CONTROLS.md`.

The `gog_magog_pairs` step checks Gog/Magog ELS proximity against paired
controls. Tracked summary: `docs/GOG_MAGOG_PAIR_CONTROLS.md`.

The `gog_magog_strict_pairs` step reruns Gog/Magog proximity requiring same
chapter and same signed skip. Tracked summary:
`docs/GOG_MAGOG_STRICT_PAIR_CONTROLS.md`.

The `pair_baselines` step compares strict observed pair counts for Gog/Magog
against unrelated declared prophetic pairs. Tracked summary:
`docs/PAIR_BASELINES.md`.

The `synthetic_pair_baselines` step compares short Hebrew strict pair density
against length-matched synthetic 3+4 letter strings sampled from MT_WLC letter
frequencies. Tracked summary: `docs/SYNTHETIC_PAIR_BASELINES.md`.

The `beast_dragon_strict_controls` step runs full strict paired controls for
the Hebrew baseline pair that exceeded Gog/Magog in observed strict close
pairs. Tracked summary: `docs/BEAST_DRAGON_STRICT_CONTROLS.md`.

The `extension_paired_controls` step checks filtered NT same-skip extension top
rows against shuffled-term and same-length random controls. Tracked summary:
`docs/EXTENSION_PAIRED_CONTROLS.md`.

The `extension_overlap_controls` step narrows that screen to strict TR/SBLGNT
overlap rows and raises the paired-control samples. Tracked summary:
`docs/EXTENSION_OVERLAP_CONTROLS.md`.

The `extension_context_review` step joins those strict overlap rows back to
center, hit-span, and extension-span verse context. Tracked summary:
`docs/EXTENSION_CONTEXT_REVIEW.md`.

The `extension_exact_center_controls` step reruns deeper 200/200 controls for
the exact-center `δοξα` overlap only. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_CONTROLS.md`.

The separate `extension_deep_controls` protocol reruns that same exact-center
`δοξα` overlap with 1000/1000 controls. It stays outside the routine public
baseline because it is a slower focused follow-up.

The `extension_exact_center_cohort_controls` step broadens that follow-up to
all NT extension top rows whose center verse has exact surface context. Tracked
summary: `docs/EXTENSION_EXACT_CENTER_COHORT_CONTROLS.md`.

The `extension_exact_center_cohort_review` step builds the matching context and
letter-path sheets. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`.

The `extension_exact_center_cross_text` step checks exact-center cohort rows
against the opposite Greek NT text by exact extension key. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_CROSS_TEXT.md`.

The `extension_exact_center_final_gate` step combines context, controls, and
cross-text status into one promotion/hold table. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`.

The `synthetic_extension_baselines` step compares exact-center NT extension rows
against same-length synthetic Greek strings. Tracked summary:
`docs/SYNTHETIC_EXTENSION_BASELINES.md`.

The `synthetic_extension_match_review` step reviews the synthetic controls that
match or exceed target any-type extension scores. Tracked summary:
`docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md`.
