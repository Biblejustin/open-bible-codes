#!/usr/bin/env python3
"""Download external WRR audit/source files into ignored reports output."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import urlopen

from els import __version__


DEFAULT_OUT_DIR = Path("reports/wrr_1994")
DEFAULT_SOURCES = {
    "wrr_1994_paper": "https://academicweb.nd.edu/~rwilliam/ndonly/readings/Methods/06-ContentAnalysis/Equidistant%20Letter%20Sequences%20in%20the%20Book%20of%20Genesis%201994.pdf",
    "wrr1": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/WRR1.txt",
    "wrr2": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/WRR2.txt",
    "se2a": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE2a.txt",
    "se2b": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE2b.txt",
    "se3": "https://users.cecs.anu.edu.au/~bdm/codes/statsci/SE3.txt",
    "mc_key": "https://users.cecs.anu.edu.au/~bdm/codes/MC.html",
    "wrr_nations_mc": "https://www.math.utoronto.ca/drorbn/Codes/Nations/main_mc.html",
    "wrr_nations_gir": "https://www.math.utoronto.ca/drorbn/Codes/Nations/main_gir.html",
    "wnp_mc": "https://users.cecs.anu.edu.au/~bdm/codes/WNP/main_mc.html",
    "wnp_en": "https://users.cecs.anu.edu.au/~bdm/codes/WNP/main_en.html",
}
REQUIRED_MANIFEST_LABELS = tuple(DEFAULT_SOURCES)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    downloads = []
    for label, url in DEFAULT_SOURCES.items():
        target = args.out_dir / source_filename(label, url)
        if target.exists() and not args.refresh:
            status = "cached"
        else:
            data = fetch_url(url)
            target.write_bytes(data)
            status = "downloaded"
        downloads.append(
            {
                "label": label,
                "url": url,
                "path": str(target),
                "status": status,
                "bytes": target.stat().st_size,
                "sha256": sha256_file(target),
            }
        )
        print(target)
    if args.manifest_out:
        write_manifest(args.manifest_out, downloads, started)
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_OUT_DIR / "sources.manifest.json")
    parser.add_argument("--refresh", action="store_true")
    return parser


def source_filename(label: str, url: str) -> str:
    suffix = Path(url).suffix or ".txt"
    canonical_names = {
        "wrr_1994_paper": "wrr_1994_paper.pdf",
        "wrr1": "WRR1.txt",
        "wrr2": "WRR2.txt",
        "se2a": "SE2a.txt",
        "se2b": "SE2b.txt",
        "se3": "SE3.txt",
        "wrr_nations_mc": "wrr_nations_main_mc.html",
        "wrr_nations_gir": "wrr_nations_main_gir.html",
    }
    if label in canonical_names:
        return canonical_names[label]
    return f"{label}{suffix}"


def fetch_url(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:
        return response.read()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(path: Path, downloads: list[dict[str, object]], started: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "downloads": downloads,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
