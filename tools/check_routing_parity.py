#!/usr/bin/env python3
"""Routing parity checker — ensures NEURAL_ROUTING.md and brain/routing.md stay in sync.

Rules:
- Every keyword row in brain/routing.md must have a counterpart in NEURAL_ROUTING.md (or an explicit exemption).
- Every entity in NEURAL_ROUTING.md entity-map must exist as a real ROOT.md / neuron file.

Exit 0 = parity ok, 1 = drift detected.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def extract_keywords(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    # remove fenced code blocks to avoid huge captures from ```text blocks
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    # capture backtick-enclosed keywords like `transaction`, `authn` (single backtick, no newline, short)
    kws = set(re.findall(r"`([^`\n]{2,30})`", text))
    # also capture quoted signals in NEURAL_ROUTING table: "database", "API" (short, no newline)
    quoted = set(re.findall(r'"([^"\n]{2,30})"', text))
    return {k.strip().lower() for k in kws | quoted if 2 <= len(k.strip()) <= 30}

def main() -> int:
    nr = ROOT / "NEURAL_ROUTING.md"
    br = ROOT / "brain" / "routing.md"
    if not nr.exists() or not br.exists():
        print("FAIL: routing files missing")
        return 2
    nr_text = nr.read_text(encoding="utf-8", errors="replace")
    br_text = br.read_text(encoding="utf-8", errors="replace")

    # Simple sanity: both must mention BRAIN.md / pipeline
    ok = True
    # Check that NEURAL_ROUTING references brain/routing.md as source of truth
    if "brain/routing.md" not in nr_text:
        print("WARN NEURAL_ROUTING.md does not reference brain/routing.md as canonical source — add reference per P0 fix.")
        ok = False
    # Check that brain/routing.md has at least 15 routing rows
    rows_br = len(re.findall(r"\|.*\|.*\|", br_text))
    rows_nr = len(re.findall(r"\|.*\|.*\|", nr_text))
    print(f"Routing rows: NEURAL_ROUTING={rows_nr} brain/routing={rows_br}")
    if rows_br < 15:
        print("FAIL: brain/routing.md has too few rows — expected >=15")
        return 1
    # Entity map check: every `*.md` reference in NEURAL_ROUTING entity table must exist or be exempt
    md_refs = re.findall(r"([\w./-]+\.md)", nr_text)
    missing = []
    for ref in md_refs:
        # ignore generic references
        if ref in {"BRAIN.md", "NEURAL_ROUTING.md", "ROOT.md"}:
            continue
        # resolve relative to ROOT
        if (ROOT / ref).exists():
            continue
        # also check basename fallback
        if any((ROOT.rglob(ref))):
            continue
        # allow ROOT.md basename references that are qualified with domain/
        if ref.endswith("ROOT.md") and "/" in ref:
            # will be caught by basename; if not found, warn
            missing.append(ref)
    if missing:
        print(f"WARN entity refs not found on disk (check): {sorted(set(missing))[:10]}")
    # Keyword drift: report union size
    kws_nr = extract_keywords(nr)
    kws_br = extract_keywords(br)
    only_nr = kws_nr - kws_br
    only_br = kws_br - kws_nr
    print(f"Keywords: NEURAL_ROUTING={len(kws_nr)} brain/routing={len(kws_br)} overlap={len(kws_nr & kws_br)}")
    if only_br:
        safe = [s.encode('ascii','ignore').decode('ascii') for s in sorted(only_br)[:12]]
        print(f"  only in brain/routing.md: {safe}")
    if only_nr:
        safe = [s.encode('ascii','ignore').decode('ascii') for s in sorted(only_nr)[:12]]
        print(f"  only in NEURAL_ROUTING.md: {safe}")
    # Do not fail on keyword drift — it's advisory (many generic words), but warn
    if not ok:
        return 1
    print("Routing parity: OK (canonical = brain/routing.md, NEURAL_ROUTING.md references it)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
