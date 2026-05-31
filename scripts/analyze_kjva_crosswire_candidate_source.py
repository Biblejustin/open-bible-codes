#!/usr/bin/env python3
"""Audit CrossWire KJV/KJVA GitLab metadata without importing Bible text."""

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
from urllib.parse import quote
from urllib.request import Request, urlopen

from els import __version__


PROJECT_API = "https://gitlab.com/api/v4/projects/crosswire-bible-society%2Fkjv"
PROJECT_WEB_URL = "https://gitlab.com/crosswire-bible-society/kjv"
TREE_API_TEMPLATE = PROJECT_API + "/repository/tree?recursive=true&per_page=100&ref={branch}"
README_API_TEMPLATE = PROJECT_API + "/repository/files/{path}?ref={branch}"
DEFAULT_OUT_DIR = Path("reports/kjva_crosswire_candidate_source")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "source_status.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md")
USER_AGENT = "OpenBibleCodes-EDLS source-status audit/1.0"

ROW_FIELDNAMES = [
    "source_id",
    "repo_url",
    "project_fetch_status",
    "tree_fetch_status",
    "readme_fetch_status",
    "kjva_conf_fetch_status",
    "kjvdc_conf_fetch_status",
    "default_branch",
    "tree_path_count",
    "tree_paths",
    "kjv_osis_path_present",
    "kjva_osis_path_present",
    "kjvdc_xml_path_present",
    "kjvdc_conf_path_present",
    "kjva_conf_path_present",
    "builder_script_present",
    "readme_sha",
    "readme_size",
    "readme_public_domain_marker_present",
    "readme_kjvdc_marker_present",
    "readme_kjva_osis_marker_present",
    "kjva_distribution_license",
    "kjvdc_distribution_license",
    "kjva_crown_rights_marker_present",
    "kjvdc_crown_rights_marker_present",
    "source_audit_status",
    "source_use_status",
    "verse_numbered_import_ready",
    "source_lock_ready_status",
    "result_ready_status",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "metadata_fetches_ok",
    "possible_independent_kjva_candidates",
    "kjva_osis_paths",
    "kjvdc_paths",
    "source_use_ready_pages",
    "source_lock_ready_pages",
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
    project = fetch_json(args.project_api, timeout=args.timeout)
    branch = str(project.data.get("default_branch") or args.default_branch)
    tree = fetch_json(args.tree_api_template.format(branch=branch), timeout=args.timeout)
    readme = fetch_json(
        args.readme_api_template.format(path=quote("README.md", safe=""), branch=branch),
        timeout=args.timeout,
    )
    kjva_conf = fetch_json(
        args.readme_api_template.format(path=quote("kjva.conf", safe=""), branch=branch),
        timeout=args.timeout,
    )
    kjvdc_conf = fetch_json(
        args.readme_api_template.format(path=quote("kjvdc.conf", safe=""), branch=branch),
        timeout=args.timeout,
    )
    rows = [analyze_metadata(args, project, tree, readme, kjva_conf, kjvdc_conf, branch)]
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
    parser.add_argument("--project-api", default=PROJECT_API)
    parser.add_argument("--tree-api-template", default=TREE_API_TEMPLATE)
    parser.add_argument("--readme-api-template", default=README_API_TEMPLATE)
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
            if isinstance(data, list):
                return JsonFetch(status="fetched", data={"items": data})
            return JsonFetch(status="unexpected_json_shape", data={}, error="top-level JSON is not object or list")
    except HTTPError as exc:
        return JsonFetch(status=f"http_error_{exc.code}", data={}, error=str(exc))
    except (OSError, URLError, json.JSONDecodeError) as exc:
        return JsonFetch(status="fetch_error", data={}, error=str(exc))


def analyze_metadata(
    args: argparse.Namespace,
    project: JsonFetch,
    tree: JsonFetch,
    readme: JsonFetch,
    kjva_conf: JsonFetch,
    kjvdc_conf: JsonFetch,
    branch: str,
) -> dict[str, object]:
    paths = sorted(
        str(item.get("path", ""))
        for item in tree_items(tree.data)
        if str(item.get("type", "")) == "blob"
    )
    path_set = set(paths)
    readme_text = decode_readme(readme.data)
    readme_lower = readme_text.lower()
    kjva_conf_text = decode_readme(kjva_conf.data)
    kjvdc_conf_text = decode_readme(kjvdc_conf.data)
    kjva_license = conf_value(kjva_conf_text, "DistributionLicense")
    kjvdc_license = conf_value(kjvdc_conf_text, "DistributionLicense")
    metadata_ok = all(
        status == "fetched"
        for status in [project.status, tree.status, readme.status, kjva_conf.status, kjvdc_conf.status]
    )
    has_kjva = "kjva.osis.xml" in path_set
    has_kjvdc = "kjvdc.xml" in path_set
    has_builder = "kjvfull2kjva.sh" in path_set
    possible_candidate = metadata_ok and has_kjva and has_kjvdc
    return {
        "source_id": "crosswire_gitlab_kjva_osis",
        "repo_url": PROJECT_WEB_URL,
        "project_fetch_status": project.status,
        "tree_fetch_status": tree.status,
        "readme_fetch_status": readme.status,
        "kjva_conf_fetch_status": kjva_conf.status,
        "kjvdc_conf_fetch_status": kjvdc_conf.status,
        "default_branch": branch,
        "tree_path_count": len(paths),
        "tree_paths": ";".join(paths),
        "kjv_osis_path_present": "kjv.osis.xml" in path_set,
        "kjva_osis_path_present": has_kjva,
        "kjvdc_xml_path_present": has_kjvdc,
        "kjvdc_conf_path_present": "kjvdc.conf" in path_set,
        "kjva_conf_path_present": "kjva.conf" in path_set,
        "builder_script_present": has_builder,
        "readme_sha": str(readme.data.get("blob_id") or readme.data.get("content_sha256") or ""),
        "readme_size": int(readme.data.get("size") or 0),
        "readme_public_domain_marker_present": "public domain" in readme_lower,
        "readme_kjvdc_marker_present": "kjvdc.xml" in readme_lower,
        "readme_kjva_osis_marker_present": "kjva.osis.xml" in readme_lower,
        "kjva_distribution_license": kjva_license,
        "kjvdc_distribution_license": kjvdc_license,
        "kjva_crown_rights_marker_present": "rights to the base text are held by the crown" in kjva_conf_text.lower(),
        "kjvdc_crown_rights_marker_present": "rights to the base text are held by the crown" in kjvdc_conf_text.lower(),
        "source_audit_status": (
            "possible_independent_kjva_candidate_needs_text_audit"
            if possible_candidate
            else "source_candidate_not_confirmed"
        ),
        "source_use_status": "needs_rights_review",
        "verse_numbered_import_ready": False,
        "source_lock_ready_status": "not_source_lock_ready",
        "result_ready_status": "not_result_ready",
    }


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "source_pages": len(rows),
        "metadata_fetches_ok": sum(
            1
            for row in rows
            if row["project_fetch_status"] == row["tree_fetch_status"] == row["readme_fetch_status"] == "fetched"
            and row["kjva_conf_fetch_status"] == row["kjvdc_conf_fetch_status"] == "fetched"
        ),
        "possible_independent_kjva_candidates": sum(
            1
            for row in rows
            if row["source_audit_status"] == "possible_independent_kjva_candidate_needs_text_audit"
        ),
        "kjva_osis_paths": sum(1 for row in rows if bool(row["kjva_osis_path_present"])),
        "kjvdc_paths": sum(1 for row in rows if bool(row["kjvdc_xml_path_present"])),
        "source_use_ready_pages": sum(
            1 for row in rows if row["source_use_status"] == "source_use_ready"
        ),
        "source_lock_ready_pages": sum(
            1 for row in rows if row["source_lock_ready_status"] != "not_source_lock_ready"
        ),
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
            "crosswire",
            "metadata_fetch_status_recorded",
            bool(row.get("project_fetch_status")) and bool(row.get("tree_fetch_status")),
            "GitLab project and tree fetch status are recorded",
        ),
        (
            "crosswire",
            "kjva_osis_path_recorded",
            int(summary["kjva_osis_paths"]) == 1,
            "kjva.osis.xml path is present in tree metadata",
        ),
        (
            "crosswire",
            "kjvdc_xml_path_recorded",
            int(summary["kjvdc_paths"]) == 1,
            "kjvdc.xml path is present in tree metadata",
        ),
        (
            "crosswire",
            "source_use_not_ready",
            int(summary["source_use_ready_pages"]) == 0,
            "conf metadata requires rights review before local text import",
        ),
        (
            "crosswire",
            "source_lock_not_ready",
            int(summary["source_lock_ready_pages"]) == 0,
            "no source-lock-ready corpus import is declared",
        ),
        (
            "crosswire",
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
        "# KJVA CrossWire Candidate Source Audit",
        "",
        "Status: source-status audit only.",
        "",
        "This is not an ELS result, not a corpus import, and not a source lock.",
        "It records GitLab metadata only and does not download, retain, normalize, or commit Bible text.",
        "",
        "## Summary",
        "",
        f"- Source pages: {summary['source_pages']}.",
        f"- Metadata fetches ok: {summary['metadata_fetches_ok']}.",
        f"- Possible independent KJVA metadata candidates: {summary['possible_independent_kjva_candidates']}.",
        f"- KJVA OSIS paths: {summary['kjva_osis_paths']}.",
        f"- KJVDC XML paths: {summary['kjvdc_paths']}.",
        f"- Source-use ready pages: {summary['source_use_ready_pages']}.",
        f"- Source-lock ready pages: {summary['source_lock_ready_pages']}.",
        f"- Verse-numbered import ready pages: {summary['verse_import_ready_pages']}.",
        f"- Result-ready pages: {summary['result_ready_pages']}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Source Rows",
        "",
        "| Source | Status | Branch | Tree paths | KJVA OSIS | KJVDC XML | Source use | Source lock | Result |",
        "| --- | --- | --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["source_id"]),
                    f"`{row['source_audit_status']}`",
                    f"`{row['default_branch']}`",
                    str(row["tree_path_count"]),
                    str(row["kjva_osis_path_present"]),
                    str(row["kjvdc_xml_path_present"]),
                    f"`{row['source_use_status']}`",
                    f"`{row['source_lock_ready_status']}`",
                    f"`{row['result_ready_status']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Anchors",
            "",
            f"Found anchors: {found}/{len(anchors)}.",
            "",
            "| Source | Anchor | Status | Diagnostic |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in anchors:
        lines.append(
            f"| {row['source']} | `{row['anchor']}` | `{row['status']}` | {row['diagnostic']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "CrossWire metadata is a stronger future source candidate than the KJV-only Open-Bibles repository because it exposes both `kjva.osis.xml` and `kjvdc.xml` path names.",
            "The configuration metadata records `DistributionLicense=GPL` for KJVA and `DistributionLicense=General public license for distribution for any purpose` for the DC-only file, while also noting Crown rights language; source-use review is still required before any local text import.",
            "It is still not source-lock ready: the project has not imported the text, mapped verses, checked book order, compared against current KJVA output, or frozen checksums in a study lock.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    anchors: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_crosswire_candidate_source",
        "project_api": args.project_api,
        "claim_boundary": "source-status audit only; no ELS result",
        "text_retention": "metadata only; no Bible text retained",
        "row_count": len(rows),
        "summary": summary,
        "anchor_count": len(anchors),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tree_items(data: dict[str, object]) -> list[dict[str, object]]:
    items = data.get("items", [])
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]
    return []


def decode_readme(data: dict[str, object]) -> str:
    content = data.get("content", "")
    if not isinstance(content, str) or not content:
        return ""
    try:
        return base64.b64decode(content, validate=False).decode("utf-8", errors="replace")
    except (ValueError, OSError):
        return ""


def conf_value(text: str, key: str) -> str:
    prefix = f"{key}="
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return ""


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
