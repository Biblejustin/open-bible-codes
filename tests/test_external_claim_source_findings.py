import json
from pathlib import Path

from scripts import build_external_claim_source_findings as findings


def test_build_findings_splits_bible_and_control_rows() -> None:
    payload = findings.build_findings(
        [
            {
                "term_set": "source_terms",
                "corpus": "MT_WLC",
                "total_hits": "10",
            }
        ],
        [
            {
                "corpus": "MT_WLC",
                "term_id": "yhwh_h",
                "concept": "YHWH",
                "normalized_term": "יהוה",
                "hit_count": "10",
                "context_hit_count": "8",
                "exact_center_word_hits": "3",
            },
            {
                "corpus": "HEB_BIALIK",
                "term_id": "yhwh_h",
                "concept": "YHWH",
                "normalized_term": "יהוה",
                "hit_count": "20",
                "context_hit_count": "19",
                "exact_center_word_hits": "2",
            },
        ],
        [
            {
                "overall_rank": "1",
                "bucket_rank": "1",
                "bucket": "center_word_exact",
                "presence_scope": "multi_source",
                "present_corpora": "MT_WLC",
                "term_id": "yhwh_h",
                "concept": "YHWH",
                "normalized_term": "יהוה",
                "center_ref": "1Kgs 10:5",
                "center_normalized_word": "יהוה",
            },
            {
                "overall_rank": "2",
                "bucket_rank": "1",
                "bucket": "center_word_exact",
                "presence_scope": "source_specific",
                "present_corpora": "HEB_BIALIK",
                "term_id": "yhwh_h",
                "concept": "YHWH",
                "normalized_term": "יהוה",
                "center_ref": "PBY Bialik",
                "center_normalized_word": "יהוה",
            },
        ],
    )

    assert payload["corpus_summary"]["bible"]["hit_count"] == 10
    assert payload["corpus_summary"]["control"]["hit_count"] == 20
    assert payload["top_bible_queue_rows"][0]["center_ref"] == "1Kgs 10:5"
    assert payload["top_control_queue_rows"][0]["center_ref"] == "PBY Bialik"


def test_main_writes_markdown_and_manifest(tmp_path: Path) -> None:
    counts = tmp_path / "counts.csv"
    summary = tmp_path / "summary.csv"
    queue = tmp_path / "queue.csv"
    markdown = tmp_path / "findings.md"
    manifest = tmp_path / "manifest.json"
    counts.write_text(
        "term_set,corpus,total_hits\nsource_terms,MT_WLC,10\n",
        encoding="utf-8",
    )
    summary.write_text(
        "corpus,term_id,concept,category,normalized_term,hit_count,context_hit_count,"
        "exact_center_word_hits,same_concept_center_word_hits,same_category_center_word_hits,"
        "exact_center_hits,same_concept_center_hits,same_category_center_hits,"
        "exact_span_hits,same_concept_span_hits,same_category_span_hits\n"
        "MT_WLC,yhwh_h,YHWH,theology,יהוה,10,8,3,0,0,2,0,0,1,0,0\n",
        encoding="utf-8",
    )
    queue.write_text(
        "overall_rank,bucket_rank,bucket,presence_scope,present_corpora,term_id,concept,"
        "normalized_term,center_ref,center_normalized_word\n"
        "1,1,center_word_exact,multi_source,MT_WLC,yhwh_h,YHWH,יהוה,1Kgs 10:5,יהוה\n",
        encoding="utf-8",
    )

    code = findings.main(
        [
            "--counts-summary",
            str(counts),
            "--all-codes-summary",
            str(summary),
            "--triage-queue",
            str(queue),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    text = markdown.read_text(encoding="utf-8")
    assert "External Claim Source Findings" in text
    assert "`יהוה` (YHWH; English: YHWH)" in text
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["count_rows"] == 1
    assert data["triage_rows"] == 1
