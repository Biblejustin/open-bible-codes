#!/usr/bin/env python3
"""Download eBible 66-book English KJV USFM and convert it to CSV."""

from __future__ import annotations

import sys

from scripts.download_ebible_usfm import main


if __name__ == "__main__":
    sys.argv.insert(1, "--source")
    sys.argv.insert(2, "eng-kjv2006")
    raise SystemExit(main())
