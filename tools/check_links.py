#!/usr/bin/env python3
"""Link integrity checker for the skill repository.

Only real references are checked, not prose:
  - markdown link destinations   `[label](target)`
  - inline/code-span tokens      `` `path.md` ``
Tokens ending in `.md` (optionally with `#anchor`) inside those contexts
are resolved in order:
  1. relative to the source file's directory
  2. relative to the skill root (domain-anchored)
  3. by basename anywhere in the tree (wiki-style, last resort)

Ambiguity: a basename-only reference matching >1 file (e.g. `ROOT.md`
matching 28 files) is reported as AMBIGUOUS and is an error — fix the
reference to a qualified path. Prose mentions match nothing and are fine.

Usage: python tools/check_links.py [--strict] [root_dir]
Check: --strict additionally verifies `file.md#anchor` header anchors.
Exit: 0 clean, 1 broken or ambiguous (or stale anchor with --strict).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

argv = sys.argv
ROOT = Path(argv[1]).resolve() if len(argv) > 1 and Path(argv[1]).is_dir() else \
    Path(__file__).resolve().parent.parent
if "--strict" in argv:
    argv.remove("--strict")

TOKEN_RE = re.compile(r"([\w.\-/]+\.md(?:#[A-Za-z0-9\-_]+)?)")
LINK_RE = re.compile(r"\]\(\s*([^)#\s]+(?:#[A-Za-z0-9\-_]+)?)\s*\)")
BACKTICK_RE = re.compile(r"`([^`]+)`")
HEADER_RE = re.compile(r"^#{1,3}\s+(.+?)\s*$", re.M)
IGNORED = {"README.md", "LICENSE"}
SKIP_DIRS = {".mimocode", ".git", "node_modules", ".opencode"}


def scan_tokens(text: str) -> list[str]:
    toks = LINK_RE.findall(text)
    for chunk in BACKTICK_RE.findall(text):
        if re.fullmatch(r"[\w.\-/]+\.md(?:#[A-Za-z0-9\-_]+)?", chunk):
            toks.append(chunk)
    return toks


def _is_skipped(p: Path) -> bool:
    return any(part in SKIP_DIRS for part in p.parts)


def all_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if not _is_skipped(p))


def basename_index(files: list[Path]) -> dict[str, list[Path]]:
    idx: dict[str, list[Path]] = {}
    for f in files:
        idx.setdefault(f.name.lower(), []).append(f)
    return idx


def headers_of(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return [re.sub(r"[^A-Za-z0-9\-_ ]", " ", h.group(1)).strip().lower()
            for h in HEADER_RE.finditer(text)]


def main() -> int:
    files = all_files()
    idx = basename_index(files)
    cache: dict[Path, list[str]] = {}
    broken, ambiguous, bad_anchor = [], [], []
    resolved = {"relative": 0, "root": 0, "basename": 0}

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        for tok in scan_tokens(text):
            target, _, anchor = tok.partition("#")
            if target in IGNORED:
                continue
            # only validate markdown references
            if not target.lower().endswith(".md"):
                continue
            if "/" in target or "\\" in target:
                good = None
                if (f.parent / target).resolve().exists():
                    good = (f.parent / target).resolve()
                    resolved["relative"] += 1
                elif (ROOT / target).resolve().exists():
                    good = (ROOT / target).resolve()
                    resolved["root"] += 1
                if good is None:
                    broken.append(f"{f.relative_to(ROOT)} -> {tok}")
                    continue
            else:
                matches = idx.get(target.lower(), [])
                if not matches:
                    broken.append(f"{f.relative_to(ROOT)} -> {tok}")
                    continue
                if len(matches) > 1:
                    ambiguous.append(f"{f.relative_to(ROOT)} -> {tok} "
                                     f"(matches {len(matches)} files)")
                    continue
                resolved["basename"] += 1
                good = matches[0]
            if anchor and "--strict" in sys.argv:
                if good not in cache:
                    cache[good] = headers_of(good)
                if anchor.lower() not in cache[good]:
                    bad_anchor.append(f"{f.relative_to(ROOT)} -> {tok} "
                                      f"(no header #{anchor} in {good.name})")

    problems = broken + ambiguous + bad_anchor
    stats = (f"relative={resolved['relative']} root={resolved['root']} "
             f"basename={resolved['basename']}")
    if problems:
        print(f"RESOLVED: {stats}")
        if broken:
            print(f"{len(broken)} broken reference(s):")
            for b in sorted(set(broken)):
                print("  " + b)
        if ambiguous:
            print(f"{len(ambiguous)} ambiguous reference(s) — qualify the path:")
            for b in sorted(set(ambiguous)):
                print("  " + b)
        if bad_anchor:
            print(f"{len(bad_anchor)} stale anchor(s) (--strict):")
            for b in sorted(set(bad_anchor)):
                print("  " + b)
        return 1
    print(f"All references resolve ({stats}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())