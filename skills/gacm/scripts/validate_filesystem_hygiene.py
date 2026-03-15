#!/usr/bin/env python3
"""
Validate repository filesystem hygiene for cross-platform portability.

Checks:
- no Windows reserved device names in relevant repo paths
- no trailing spaces or dots in path segments
- no Windows-invalid filename characters in path segments
- no control characters in path segments
- no case-insensitive duplicate repo-relative paths in the checked trees
- no excessively long repo-relative paths in the checked trees
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CHECK_ROOTS = (
    REPO_ROOT / "docs",
    REPO_ROOT / "skills" / "gacm",
    REPO_ROOT / "gcam-doc",
    REPO_ROOT / "gcam-core",
)
WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{i}" for i in range(1, 10)),
    *(f"lpt{i}" for i in range(1, 10)),
}
WINDOWS_INVALID_CHARS = set('<>:"|?*')
MAX_REL_PATH_LEN = 220


def validate_segment(path: Path, segment: str, errors: list[str]) -> None:
    rel = path.relative_to(REPO_ROOT).as_posix()
    stem = Path(segment).stem.lower()
    if stem in WINDOWS_RESERVED:
        errors.append(f"Reserved Windows device name in path segment: {rel}")
    if segment.endswith(" ") or segment.endswith("."):
        errors.append(f"Trailing space or dot in path segment: {rel}")
    if any(ch in WINDOWS_INVALID_CHARS for ch in segment):
        errors.append(f"Windows-invalid filename character in path segment: {rel}")
    if any(ord(ch) < 32 for ch in segment):
        errors.append(f"Control character in path segment: {rel}")


def main() -> int:
    errors: list[str] = []
    lowered_paths: dict[str, list[str]] = defaultdict(list)

    for root in CHECK_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            rel = path.relative_to(REPO_ROOT).as_posix()
            lowered_paths[rel.lower()].append(rel)

            if len(rel) > MAX_REL_PATH_LEN:
                errors.append(
                    f"Repo-relative path too long for portability budget ({len(rel)} > {MAX_REL_PATH_LEN}): {rel}"
                )

            for segment in path.relative_to(REPO_ROOT).parts:
                validate_segment(path, segment, errors)

    for lowered, items in sorted(lowered_paths.items()):
        unique_items = sorted(set(items))
        if len(unique_items) > 1:
            errors.append(
                "Case-insensitive repo path collision detected: " + " | ".join(unique_items)
            )

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Filesystem hygiene validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
