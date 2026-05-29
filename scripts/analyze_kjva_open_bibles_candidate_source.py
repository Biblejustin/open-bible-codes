#!/usr/bin/env python3
"""Audit seven1m/open-bibles metadata without importing Bible text."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from els import __version__


REPO_API = "https://api.github.com/repos/seven1m/open-bibles"
REPO_WEB_URL = "https://github.com/seven1m/open-bibles"
TREE_API_TEMPLATE = REPO_API + "/git/trees/{branch}?recursive=1"
README_API = REPO_API + "/readme"
DEFAULT_OUT_DIR = Path("reports/kjva_open_bibles_candidate_source")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "source_status.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md")
USER_AGENT = "OpenBibleCodes-EDLS source-status audit/1.0"

ROW_FIELDNAMES = [
    "source_id",
    "repo_url",
    "repo_fetch_status",
    "tree_fetch_status",
    "readme_fetch_status",
    "default_branch",
    "github_license_key",
    "tree_path_count",
    "tree_truncated",
    "osis_path_count",
    "kjv_path_count",
    "kjv_paths",
    "apocrypha_path_count",
    "deuterocanon_path_count",
    "readme_sha",
    "readme_public_domain_marker_present",
    "readme_kjv_row_present",
    "readme_apocrypha_marker_present",
    "source_audit_status",
    "verse_numbered_import_ready",
    "result_ready_status",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "metadata_fetches_ok",
    "kjv_paths",
    "apocrypha_paths",
    "deuterocanon_paths",
    "verse_import_ready_pages",
    "result_ready_pages",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class JsonFetch:
    status: str
    data: dict[str, object]
    error: str = ""


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    repo = fetch_json(args.repo_api, timeout=args.timeout)
    branch = str(repo.data.get("default_branch") or args.default_branch)
    tree = fetch_json(args.tree_api_template.format(branch=branch), timeout=args.timeout)
    readme = fetch_json(args.readme_api, timeout=args.timeout)
    rows = [analyze_metadata(args, repo, tree, readme, branch)]
    summary = build_summary(rows)
    anchors = build_anchors(rows, summary)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors)
    write_manifest(args.manifest_out, args, rows, summary, anchors, started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-api", default=REPO_API)
    parser.add_argument("--tree-api-template", default=TREE_API_TEMPLATE)
    parser.add_argument("--readme-api", default=README_API)
    parser.add_argument("--default-branch", default="master")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    return parser


def fetch_json(url: str, *, timeout: float) -> JsonFetch:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
            if isinstance(data, dict):
                return JsonFetch(status="fetched", data=data)
            return JsonFetch(status="unexpected_json_shape", data={}, error="top-level JSON is not object")
    except HTTPError as exc:
        return JsonFetch(status=f"http_error_{exc.code}", data={}, error=str(exc))
    except (OSError, URLError, json.JSONDecodeError) as exc:
        return JsonFetch(status="fetch_error", data={}, error=str(exc))


def analyze_metadata(
    args: argparse.Namespace,
    repo: JsonFetch,
    tree: JsonFetch,
    readme: JsonFetch,
    branch: str,
) -> dict[str, object]:
    paths = [
        str(item.get("path", ""))
        for item in tree_items(tree.data)
        if str(item.get("type", "")) == "blob"
    ]
    lower_paths = [path.lower() for path in paths]
    kjv_paths = [path for path in paths if "kjv" in path.lower()]
    readme_text = decode_readme(readme.data)
    readme_lower = readme_text.lower()
    license_data = repo.data.get("license")
    license_key = ""
    if isinstance(license_data, dict):
        license_key = str(license_data.get("key") or "")
    apocrypha_count = sum("apoc" in path for path in lower_paths)
    deuterocanon_count = sum("deutero" in path or "deuterocanon" in path for path in lower_paths)
    metadata_ok = all(
        status == "fetched"
        for status in [repo.status, tree.status, readme.status]
    )
    has_kjv = bool(kjv_paths) or "eng-kjv.osis.xml" in readme_lower
    has_apocrypha = apocrypha_count > 0 or "apocrypha" in readme_lower
    if metadata_ok and has_kjv and not has_apocrypha and deuterocanon_count == 0:
        source_status = "kjv_only_not_kjva_source_candidate"
    elif metadata_ok and has_kjv and has_apocrypha:
        source_status = "possible_kjva_candidate_needs_text_audit"
    elif metadata_ok:
        source_status = "source_candidate_not_confirmed"
    else:
        source_status = "metadata_fetch_incomplete"
    return {
        "source_id": "seven1m_open_bibles_kjv_osis",
        "repo_url": REPO_WEB_URL,
        "repo_fetch_status": repo.status,
        "tree_fetch_status": tree.status,
        "readme_fetch_status": readme.status,
        "default_branch": branch,
        "github_license_key": license_key,
        "tree_path_count": len(paths),
        "tree_truncated": bool(tree.data.get("truncated", False)),
        "osis_path_count": sum(path.endswith(".osis.xml") for path in lower_paths),
        "kjv_path_count": len(kjv_paths),
        "kjv_paths": ";".join(kjv_paths),
        "apocrypha_path_count": apocrypha_count,
        "deuterocanon_path_count": deuterocanon_count,
        "readme_sha": str(readme.data.get("sha") or ""),
        "readme_public_domain_marker_present": "public domain" in readme_lower,
        "readme_kjv_row_present": "eng-kjv.osis.xml" in readme_lower,
        "readme_apocrypha_marker_present": "apocrypha" in readme_lower,
        "source_audit_status": source_status,
        "verse_numbered_import_ready": False,
        "result_ready_status": "not_result_ready",
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "source_pages": len(rows),
        "metadata_fetches_ok": sum(
            1
            for row in rows
            if row["repo_fetch_status"] == row["tree_fetch_status"] == row["readme_fetch_status"] == "fetched"
        ),
        "kjv_paths": sum(int(row["kjv_path_count"]) for row in rows),
        "apocrypha_paths": sum(int(row["apocrypha_path_count"]) for row in rows),
        "deuterocanon_paths": sum(int(row["deuterocanon_path_count"]) for row in rows),
        "verse_import_ready_pages": sum(
            1 for row in rows if bool(row["verse_numbered_import_ready"])
        ),
        "result_ready_pages": sum(
            1 for row in rows if row["result_ready_status"] != "not_result_ready"
        ),
        "claim_status": "source_status_only_not_result_bearing",
    }


def build_anchors(
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> list[dict[str, str]]:
    row = rows[0] if rows else {}
    checks = [
        (
            "open_bibles",
            "metadata_fetch_status_recorded",
            bool(row.get("repo_fetch_status")) and bool(row.get("tree_fetch_status")),
            "repository and tree fetch status are recorded",
        ),
        (
            "open_bibles",
            "kjv_path_recorded",
            int(summary["kjv_paths"]) >= 1,
            "KJV OSIS path is recorded from tree metadata",
        ),
        (
            "open_bibles",
            "apocrypha_absence_recorded",
            int(summary["apocrypha_paths"]) == 0 and int(summary["deuterocanon_paths"]) == 0,
            "no apocrypha/deuterocanon path marker is present in tree metadata",
        ),
        (
            "open_bibles",
            "result_not_ready",
            int(summary["result_ready_pages"]) == 0,
            "no result-bearing replication is declared ready",
        ),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if ok else "missing",
            "diagnostic": diagnostic,
        }
        for source, anchor, ok, diagnostic in checks
    ]


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
) -> None:
    found = sum(1 for row in anchors if row["status"] == "found")
    lines = [
        "# KJVA Open-Bibles Candidate Source Audit",
        "",
        "Status: source-status audit only. This is not an ELS result, not a",
        "corpus import, and not a claim-ready replication.",
        "",
        "## Setup",
        "",
        "This audit checks GitHub repository metadata for the seven1m/open-bibles",
        "candidate. It records repository JSON, tree path counts, and README",
        "markers only. It does not download, retain, normalize, or commit Bible",
        "text.",
        "",
        "Primary candidate:",
        "",
        "- https://github.com/seven1m/open-bibles",
        "",
        "## Findings",
        "",
        f"- Metadata rows checked: {summary['source_pages']}.",
        f"- Metadata fetches complete: {summary['metadata_fetches_ok']}.",
        f"- KJV path markers: {summary['kjv_paths']}.",
        f"- Apocrypha path markers: {summary['apocrypha_paths']}.",
        f"- Deuterocanon path markers: {summary['deuterocanon_paths']}.",
        "- Verse-numbered import ready pages: 0.",
        "- Result-ready pages: 0.",
        "",
        "Current read: this repository is useful as a KJV-only OSIS metadata",
        "candidate, but current tree metadata does not show apocrypha or",
        "deuterocanon coverage. It is not a KJVA/apocrypha source candidate until",
        "a separate source audit finds lawful apocrypha coverage.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| source pages | {summary['source_pages']} |",
        f"| metadata fetches ok | {summary['metadata_fetches_ok']} |",
        f"| KJV paths | {summary['kjv_paths']} |",
        f"| Apocrypha paths | {summary['apocrypha_paths']} |",
        f"| Deuterocanon paths | {summary['deuterocanon_paths']} |",
        f"| verse import ready pages | {summary['verse_import_ready_pages']} |",
        f"| result ready pages | {summary['result_ready_pages']} |",
        "",
        "## Page Status",
        "",
        "| Source | Repo | Tree | README | Branch | KJV Paths | Apocrypha Paths | Deuterocanon Paths | Status |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["source_id"]),
                    markdown_cell(row["repo_fetch_status"]),
                    markdown_cell(row["tree_fetch_status"]),
                    markdown_cell(row["readme_fetch_status"]),
                    markdown_cell(row["default_branch"]),
                    markdown_cell(row["kjv_path_count"]),
                    markdown_cell(row["apocrypha_path_count"]),
                    markdown_cell(row["deuterocanon_path_count"]),
                    markdown_cell(row["source_audit_status"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Protocol Anchors",
            "",
            f"Found anchors: {found} of {len(anchors)}.",
            "",
            "| Source | Anchor | Status | Diagnostic |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in anchors:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["source"]),
                    f"`{markdown_cell(row['anchor'])}`",
                    markdown_cell(row["status"]),
                    markdown_cell(row["diagnostic"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This audit does not import Bible text, normalize verses, run ELS",
            "searches, evaluate controls, or upgrade the completed KJVA bridge",
            "lane. It only records that current seven1m/open-bibles metadata has",
            "KJV OSIS coverage without visible apocrypha/deuterocanon path coverage.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    anchors: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "sources": [args.repo_api, args.tree_api_template, args.readme_api],
        "rows": len(rows),
        "summary": summary,
        "anchors": anchors,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-status audit only; no ELS result",
        "text_retention": "metadata only; no Bible text retained",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def tree_items(data: dict[str, object]) -> list[dict[str, object]]:
    tree = data.get("tree", [])
    if isinstance(tree, list):
        return [item for item in tree if isinstance(item, dict)]
    return []


def decode_readme(data: dict[str, object]) -> str:
    content = data.get("content", "")
    if not isinstance(content, str):
        return ""
    try:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    except ValueError:
        return ""


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
