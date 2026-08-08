#!/usr/bin/env python3
"""Neuron schema validator — scans the WHOLE markdown tree.

Roots: validates every *.md under the skill root (NOT a nonexistent
`domains/` dir). Reports the real scanned count and the share of files
carrying the light contract (Identity), so the checker cannot be "green"
by scanning zero files.

Exit codes:
  2  = zero markdown files found (no-op) — hard fail
  1  = warnings >= --max-warnings (default: always 0-exit for warnings;
       pass --max-warnings 0 to turn advisory output into a gate)
  0  = ok

Usage: python tools/validate_neurons.py [--path DIR] [--max-warnings N]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if "--path" in sys.argv:
    ROOT = Path(sys.argv[sys.argv.index("--path") + 1])

try:
    MAX_WARN = int(sys.argv[sys.argv.index("--max-warnings") + 1])
except (ValueError, IndexError):
    MAX_WARN = int(1e9)

EXEMPT = {"README.md", "LICENSE"}


def main() -> int:
    mds = sorted(p for p in ROOT.rglob("*.md"))
    if not mds:
        print("FAIL: zero markdown files scanned — validator is a no-op.")
        return 2

    warnings = 0
    no_id = no_type = no_h1 = no_h2 = 0
    no_contract = set()
    for f in mds:
        if f.name in EXEMPT:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if text.startswith("---"):
            text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
        is_root_md = f.name.upper() == "ROOT.MD" or f.name.upper() == "SKILL.MD"
        missing = []
        if not is_root_md and "- ID:" not in text:
            missing.append("ID")
            no_id += 1
        if not is_root_md and "- Type:" not in text:
            missing.append("Type")
            no_type += 1
        if missing:
            no_contract.add(f.relative_to(ROOT))
        if not text.lstrip().startswith("# "):
            missing.append("H1")
            no_h1 += 1
        if "## " not in text:
            missing.append("##SECTIONS")
            no_h2 += 1
        if missing:
            warnings += 1
            for m in missing:
                print(f"WARN {f.relative_to(ROOT)}: missing {m}")

    print(f"Validated files: {len(mds)}")
    print(f"With light contract (ID+Type): {len(mds) - len(no_contract)} / {len(mds)}")
    if warnings:
        print("Run with --max-warnings 0 in CI to fail on any violation.")
        return 1 if warnings > MAX_WARN else 0
    print("All neurons carry the light contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())