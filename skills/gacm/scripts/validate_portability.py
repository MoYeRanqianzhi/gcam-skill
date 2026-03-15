#!/usr/bin/env python3
"""
Validate that the runtime skill stays free of machine-specific absolute paths.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SCAN_ROOTS = (
    REPO_ROOT / "docs",
    REPO_ROOT / "skills" / "gacm" / "SKILL.md",
    REPO_ROOT / "skills" / "gacm" / "scripts",
    REPO_ROOT / "skills" / "gacm" / "reference",
)
SKIP_DIRS = {
    REPO_ROOT / "skills" / "gacm" / "reference" / "version_pages",
    REPO_ROOT / "skills" / "gacm" / "scripts" / "__pycache__",
}
WINDOWS_ABS_RE = re.compile(r"\b[A-Za-z]:[\\/]")
POSIX_HOME_RE = re.compile(r"(?<![A-Za-z])/(?:Users|home)/")
URI_RE = re.compile(r"\b(?:file|vscode)://", re.IGNORECASE)


def should_scan(path: Path) -> bool:
    if any(parent in SKIP_DIRS for parent in path.parents):
        return False
    return path.is_file() and path.suffix.lower() in {".md", ".py"}


def iter_scan_files():
    for root in SCAN_ROOTS:
        if root.is_file():
            if should_scan(root):
                yield root
            continue
        for path in sorted(root.rglob("*")):
            if should_scan(path):
                yield path


def main() -> int:
    errors: list[str] = []
    for path in iter_scan_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if WINDOWS_ABS_RE.search(line) or POSIX_HOME_RE.search(line) or URI_RE.search(line):
                rel_path = path.relative_to(REPO_ROOT)
                snippet = line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:157] + "..."
                errors.append(f"{rel_path}:{line_no}: {snippet}")
                if len(errors) >= 100:
                    break
        if len(errors) >= 100:
            break

    if errors:
        print("Found non-portable absolute-path or file-URI references:")
        for item in errors:
            print(item)
        return 1

    print("Portability checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
