#!/usr/bin/env python3
"""Evidence freshness reporter.

Finds `Last Verified:` / `Evidence` lines and inspects nearby dates.
  - future-dated claims (vs today)                  -> ERROR, exit 1
  - claims older than N days (default 400)        -> STALE,  exit 1
  - `yyyy-mm` short dates are accepted (day = 1)  -> treated like full
  - zero dated markers anywhere                   -> gate failure, exit 3

Usage: python tools/freshness.py [--path DIR] [--days N]
Exit codes: 0 ok, 1 stale/future, 2 bad arg, 3 no evidence markers at all.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if "--path" in sys.argv:
    ROOT = Path(sys.argv[sys.argv.index("--path") + 1])

try:
    DAYS = int(sys.argv[sys.argv.index("--days") + 1])
except (ValueError, IndexError):
    DAYS = 400

DATE_RE = re.compile(r"(\d{4})-(\d{2})(?:-(\d{2}))?")
MARKER = re.compile(r"\b(verified|evidence|last accessed|last verified|refresh)\b", re.I)
TODAY = date.today()
SKIP_DIRS = {"tools"}


def parse_date(y: int, mo: int, d: str | None) -> date | None:
    try:
        return date(y, mo, int(d) if d else 1)
    except ValueError:
        return None


def main() -> int:
    errors = 0
    markers = 0
    files_seen = 0
    for f in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in f.parts[:-1]):
            continue
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        found = False
        for i, line in enumerate(lines):
            if not MARKER.search(line):
                continue
            if re.search(r"\b(refresh|re-check|due|next check|review)\b", line, re.I):
                continue
            found = True
            markers += 1
            near = " ".join(lines[max(0, i - 1): i + 2])
            dates = [parse_date(int(y), int(mo), d) for y, mo, d in DATE_RE.findall(near)]
            dates = [dt for dt in dates if dt]
            if not dates:
                continue
            # ranges like `2025-03 -> 2026-06` mean "verified in 2026-06"
            if "→" in near or "->" in near:
                dt = max(dates)
            else:
                dt = min(dates)  # the oldest stamp in the window
            age = (TODAY - dt).days
            rel = f.relative_to(ROOT)
            if age < 0:
                print(f"FUTURE {rel}: {dt.isoformat()} ({-age}d in future) -- impossible stamp")
                errors += 1
            elif age > DAYS:
                print(f"STALE  {rel}: {dt.isoformat()} ({age}d)")
                errors += 1
        if found:
            files_seen += 1

    print(f"Evidence markers: {markers} lines in {files_seen} file(s).")
    if not markers:
        print("NO-EVIDENCE: zero dated evidence markers in the tree — gate fails.")
        return 3
    if errors:
        print(f"{errors} date violation(s); exit 1")
        return 1
    print("No stale or future-dated evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())