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
- no git-index path casing drift relative to actual filesystem entries
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import subprocess


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


def in_checked_tree(rel: str) -> bool:
    for root in CHECK_ROOTS:
        root_rel = root.relative_to(REPO_ROOT).as_posix()
        if rel == root_rel or rel.startswith(root_rel + "/"):
            return True
    return False


def actual_repo_relative_case(rel: str) -> str | None:
    current = REPO_ROOT
    actual_parts: list[str] = []

    for part in Path(rel).parts:
        try:
            children = {child.name.lower(): child.name for child in current.iterdir()}
        except FileNotFoundError:
            return None
        actual = children.get(part.lower())
        if actual is None:
            return None
        actual_parts.append(actual)
        current = current / actual

    return Path(*actual_parts).as_posix()


def validate_git_index_casing(errors: list[str]) -> None:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        errors.append(f"Unable to inspect git index paths for filesystem hygiene validation: {exc}")
        return

    lowered_tracked: dict[str, list[str]] = defaultdict(list)
    tracked_paths: list[str] = []

    for raw in result.stdout.splitlines():
        rel = raw.strip().replace("\\", "/")
        if not rel or not in_checked_tree(rel):
            continue
        tracked_paths.append(rel)
        lowered_tracked[rel.lower()].append(rel)

    for lowered, items in sorted(lowered_tracked.items()):
        unique_items = sorted(set(items))
        if len(unique_items) > 1:
            errors.append("Case-insensitive git index path collision detected: " + " | ".join(unique_items))

    for rel in tracked_paths:
        actual_rel = actual_repo_relative_case(rel)
        if actual_rel is None:
            continue
        if actual_rel != rel:
            errors.append(
                "Git index path casing diverges from filesystem path casing: "
                f"{rel} | actual: {actual_rel}"
            )


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

    validate_git_index_casing(errors)

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
