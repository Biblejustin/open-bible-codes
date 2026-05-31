# KJVA Gutenberg Source-Lock Prep

Status: source-lock prep only.

This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.
It scans Project Gutenberg eBook 30 and eBook 124 plain text only to compare verse-marker counts against the current local KJVA corpus.
It does not commit Bible text, normalize Bible text, create a local corpus, or declare a source-lock-ready stream.

## Summary

- Source pages: 2.
- Plain-text pages scanned: 2.
- Raw text retained: 0.
- KJV plain-text bytes scanned: 4644740.
- Apocrypha plain-text bytes scanned: 835074.
- Local KJVA books counted: 80.
- Local KJVA verses counted: 36822.
- Local KJV verses counted: 31102.
- Local Apocrypha/deuterocanon verses counted: 5720.
- Book-shape rows written: 81.
- Local book rows compared: 80.
- KJV books compared: 66.
- KJV exact count matches: 66.
- KJV count drifts: 0.
- Apocrypha/deuterocanon books compared: 14.
- Apocrypha/deuterocanon exact count matches: 12.
- Apocrypha/deuterocanon count drifts: 2.
- Extra source sections: 1.
- Gutenberg KJV verse markers: 31102.
- Gutenberg Apocrypha/deuterocanon chapter:verse markers: 5636.
- Gutenberg Apocrypha/deuterocanon number-only markers: 68.
- Gutenberg Apocrypha/deuterocanon total verse-like markers: 5704.
- Baruch/Epistle split detected: 1.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `source_lock_prep_only_not_result_bearing`.

## Shape Read

Project Gutenberg eBook 30 has exact verse-count agreement with the current local KJVA corpus for all 66 KJV books.
Project Gutenberg eBook 124 has exact count agreement for 12 of 14 tracked Apocrypha/deuterocanon books after Baruch is read together with the separate Epistle of Jeremiah source section.
The remaining count drifts are Sirach at one fewer source marker and Prayer of Manasseh with no verse markers in the Project Gutenberg body text.
That means Project Gutenberg is stronger than metadata-only evidence, but it still needs a real collation and source-use lock before any replication run.

## Apocrypha Drift Rows

| Book | Source marker count | Local KJVA count | Delta | Status | Notes |
| --- | ---: | ---: | ---: | --- | --- |
| SIR | 1392 | 1393 | -1 | `count_drift` |  |
| MAN | 0 | 15 | -15 | `source_markers_missing` | Project Gutenberg body text has no verse markers for this section. |

## Extra Source Sections

| Source section | Marker count | Status | Notes |
| --- | ---: | --- | --- |
| LJE_SOURCE | 73 | `extra_source_component_rolls_into_BAR` | Project Gutenberg exposes this as a separate section; local KJVA counts it inside BAR. |

## Anchors

Found anchors: 6/6.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| gutenberg | `plain_text_pages_scanned` | `found` | Project Gutenberg KJV and Apocrypha plain text were scanned for counts |
| gutenberg | `kjv_counts_exact` | `found` | all 66 KJV book counts match the current local KJVA corpus |
| gutenberg | `apocrypha_count_drift_recorded` | `found` | two Apocrypha/deuterocanon book-count drifts are recorded |
| gutenberg | `baruch_epistle_split_detected` | `found` | eBook 124 separates Epistle of Jeremiah from Baruch |
| gutenberg | `source_lock_not_ready` | `found` | no source-lock-ready corpus import is declared |
| gutenberg | `result_not_ready` | `found` | no result-bearing replication is declared ready |

## Boundary

KJV source scanned: `https://www.gutenberg.org/cache/epub/30/pg30.txt`.
Apocrypha source scanned: `https://www.gutenberg.org/cache/epub/124/pg124.txt`.
Raw source text is scanned in memory or from an ignored local path and is not written to tracked files.
This prep does not choose a source stream, does not make a verse map, does not perform text collation, does not set a term lock, and does not create a study-lock sidecar.
It does not change any KJVA bridge result status.
