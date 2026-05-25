# WRR Source Row Coverage Packet

Status: no-input visual-triage coverage packet for WRR source-row review.
It does not choose row transcriptions, source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_row_coverage_packet --row-checklist reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --source-queue reports/wrr_1994/wrr_source_review_queue.csv --out reports/wrr_1994/wrr_source_row_coverage_packet.csv --summary-out reports/wrr_1994/wrr_source_row_coverage_packet_summary.csv --markdown-out docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md --manifest-out reports/wrr_1994/wrr_source_row_coverage_packet.manifest.json
```

## Current Read

- Source rows: 22.
- Action terms: 43.
- Frontier pairs: 35.
- Direct action-term visual coverage: 0 terms.
- Related row visual triage only: 4 rows.
- No related visual triage: 18 rows.
- Boundary: No row transcription, source correction, pair exclusion, or method change is selected by this coverage packet.

## Row Coverage

| Rank | Row | Terms | Frontier | Direct visual terms | Related visual terms | Coverage | Next action |
| ---: | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | `06` | 4 | 4 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 2 | `14` | 3 | 3 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 3 | `24` | 3 | 3 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 4 | `01` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 5 | `03` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 6 | `09` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 7 | `10` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 8 | `11` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 9 | `15` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 10 | `22` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 11 | `23` | 2 | 2 |  | `wrr2_23_app_04;wrr2_23_app_05` | `related_row_visual_triage_only` | do not transfer related visual notes to action terms; review row image directly |
| 12 | `25` | 2 | 2 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 13 | `26` | 2 | 1 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 14 | `27` | 1 | 1 |  | `wrr2_27_date_01;wrr2_27_app_06` | `related_row_visual_triage_only` | do not transfer related visual notes to action terms; review row image directly |
| 15 | `02` | 1 | 1 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 16 | `05` | 1 | 1 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 17 | `07` | 1 | 1 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 18 | `16` | 1 | 1 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 19 | `20` | 1 | 1 |  |  | `no_related_visual_triage` | retrieve or review primary row image before any frontier source decision |
| 20 | `30` | 4 | 0 |  | `wrr2_30_app_05` | `related_row_visual_triage_only` | do not transfer related visual notes to action terms; review row image directly |
| 21 | `32` | 2 | 0 |  | `wrr2_32_app_04` | `related_row_visual_triage_only` | do not transfer related visual notes to action terms; review row image directly |
| 22 | `29` | 1 | 0 |  |  | `no_related_visual_triage` | review after frontier rows unless policy scope changes |

## Visual-Triage Rows Outside This Checklist

- Rows with visual notes outside this source-transcription checklist: `19;28;31`.
- These rows can remain useful for page-image, title-prefix, or source-policy review, but they do not cover the current source-transcription action terms directly.

## Visual Note Boundary

- Do not transfer related visual notes to action terms.
- Visual notes can identify rows worth reviewing, but they are not locked primary transcriptions.
- No row here changes the working WRR source or excludes a pair automatically.
- Preserve the working source unless a separate decision record selects a source or method change.

## Source-Queue Visual Notes Used

| Row | Term id | Visual note | Visual action |
| --- | --- | --- | --- |
| 23 | `wrr2_23_app_04` | primary page row visibly contains Yaakov Ha-Levi wording; row OCR missed it | treat as visual OCR miss until a locked transcription says otherwise |
| 30 | `wrr2_30_app_05` | primary Hebrew name cell visibly contains Yosher Levav text without visible B@L prefix | review title-prefix/appellation rule before any source correction |
| 23 | `wrr2_23_app_05` | primary page row visibly contains Maharil Segal wording; row OCR missed it | treat as visual OCR miss until a locked transcription says otherwise |
| 28 | `wrr2_28_app_04` | primary Hebrew name cell visibly contains Pnei Moshe text without visible B@L prefix | review title-prefix/appellation rule before any source correction |
| 32 | `wrr2_32_app_04` | English label says of-Chelm; visible primary Hebrew cell supports Rabbi Shelomo only in this pass | review source/pair rule before using this as a Hebrew-cell match |
| 27 | `wrr2_27_date_01` | primary page row visibly contains 16 Tishri date forms; row OCR has near match | check page image before treating as source difference |
| 27 | `wrr2_27_app_06` | primary page row visibly contains Moshe/Zacut forms; row OCR has near match | check WNP Zacut dispute and page image before treating as source difference |
| 19 | `wrr2_19_app_11` | primary page row visibly contains Maharit/Trani forms including Yosef Trani; row OCR has one-edit near match | keep as page-image near-match until a locked transcription resolves the aleph spelling |
| 19 | `wrr2_19_app_12` | primary page row visibly contains Maharit/Trani forms including Matrani/Mitrani variants; row OCR has one-edit near match | keep as page-image near-match until a locked transcription resolves the aleph spelling |
| 31 | `wrr2_31_app_07` | primary page row visibly contains Rabbi Shalom Sharabi forms including Sar Shalom and MaharaSHaSH; exact SMSh form is not settled by this crop | keep as page-image or pair-rule review before any source correction |
