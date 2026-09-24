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
# protocol / meta files that are not neurons — must not require ID/Type
PROTOCOL_EXEMPT = {
    "BRAIN.md", "NEURAL_ROUTING.md", "EVIDENCE_PROTOCOL.md", "DECISION_ENGINE.md",
    "SECURITY_GUARDIAN.md", "SIMPLICITY_GOVERNOR.md", "PERFORMANCE_ENGINE.md",
    "RELIABILITY_ENGINE.md", "ARCHITECTURE_LINTER.md", "NEURON_PROTOCOL.md",
    "CODE_TIERS.md", "ARCHITECTURE_GENOME.md", "LEARNING_SYSTEM.md",
    "MEMORY_PROTOCOL.md", "RESEARCH_PROTOCOL.md", "VALIDATION_PROTOCOL.md",
    "adr.md",
}
# directories whose markdown is vendor or non-skill content
SKIP_DIRS = {".mimocode", ".git", "node_modules", ".opencode"}


def _is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def main() -> int:
    mds = sorted(p for p in ROOT.rglob("*.md") if not _is_skipped(p))
    if not mds:
        print("FAIL: zero markdown files scanned — validator is a no-op.")
        return 2

    warnings = 0
    no_id = no_type = no_h1 = no_h2 = 0
    no_contract = set()
    for f in mds:
        if f.name in EXEMPT or f.name in PROTOCOL_EXEMPT:
            continue
        rel = f.relative_to(ROOT)
        # brain/*.md are meta — not neurons
        if rel.parts and rel.parts[0] == "brain":
            continue
        # checklists / playbooks / benchmarks / adr / research index are procedural, not neurons
        if rel.parts and rel.parts[0] in {"checklists", "playbooks", "benchmarks", "adr", "agents", "examples", ".github"}:
            continue
        if rel.parts and rel.parts[0] == "research" and f.name in {"index.md", "sources.md"}:
            continue
        # raport is report output, not neuron
        if rel.parts and rel.parts[0] == "raport":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if text.startswith("---"):
            text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
        is_root_md = f.name.upper() == "ROOT.MD" or f.name.upper() == "SKILL.MD"
        missing = []
        # flexible ID/Type detection: "- ID:" or "ID:" or "**ID:**" (case-insensitive)
        has_id = bool(re.search(r"ID\s*:\s*\S+", text, flags=re.IGNORECASE))
        has_type = bool(re.search(r"Type\s*:\s*\S+", text, flags=re.IGNORECASE))
        if not is_root_md and not has_id:
            missing.append("ID")
            no_id += 1
        if not is_root_md and not has_type:
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