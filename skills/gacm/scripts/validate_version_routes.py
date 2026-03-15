#!/usr/bin/env python3
"""
Validate bundled GCAM version routing integrity.

Checks:
- `version_inventory.md` table order matches `version_catalog.py`
- every catalog version has a route doc in `reference/versions/`
- every catalog version has a page bundle directory in `reference/version_pages/`
- every page bundle directory has `INDEX.md`
- every `delta-only` bundle also has `release_note.md` and `cmp_index.md`
- key route docs continue to state the `v8.2` bundled baseline explicitly
"""

from __future__ import annotations

import re
from pathlib import Path

from version_catalog import REFERENCE_ROOT, VERSION_PAGES_ROOT, ordered_versions


VERSIONS_DIR = REFERENCE_ROOT / "versions"
VERSION_INVENTORY = REFERENCE_ROOT / "version_inventory.md"
VERSION_FAMILIES = REFERENCE_ROOT / "version_families.md"
VERSION_OPERATION_NOTES = REFERENCE_ROOT / "version_operation_notes.md"
NAVIGATION = REFERENCE_ROOT / "navigation.md"
COVERAGE_MAP = REFERENCE_ROOT / "coverage_map.md"

INVENTORY_ROW_RE = re.compile(r"^\|\s*`(v\d+\.\d+)`\s*\|", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(v\d+\.\d+)\s*$", re.MULTILINE)

V82_ROUTE_SNIPPETS = {
    VERSION_INVENTORY: "| `v8.2` | `modern-comprehensive` | `bundled-baseline` | `versions/v8.2.md` |",
    VERSION_FAMILIES: "- `v8.2` (bundled current baseline; corresponds to the root `gcam-doc` full documentation tree)",
    VERSION_OPERATION_NOTES: "## `v8.2`",
    NAVIGATION: "- If the user does not specify a version, default to the bundled baseline `v8.2`.",
    COVERAGE_MAP: "## Root `v8.2` Topic Coverage",
}


def validate_inventory(errors: list[str]) -> None:
    text = VERSION_INVENTORY.read_text(encoding="utf-8")
    listed_versions = INVENTORY_ROW_RE.findall(text)
    expected_versions = [info.version for info in ordered_versions()]
    if listed_versions != expected_versions:
        errors.append("version_inventory.md table order/content drifted from version_catalog.py")


def validate_route_docs(errors: list[str]) -> None:
    expected_versions = [info.version for info in ordered_versions()]
    actual_versions = sorted(path.stem for path in VERSIONS_DIR.glob("*.md"))

    missing = [version for version in expected_versions if version not in actual_versions]
    extra = [version for version in actual_versions if version not in expected_versions]
    if missing:
        errors.append("Missing version route docs: " + ", ".join(missing))
    if extra:
        errors.append("Unexpected version route docs: " + ", ".join(extra))

    for info in ordered_versions():
        path = VERSIONS_DIR / f"{info.version}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        heading_match = HEADING_RE.search(text)
        if not heading_match or heading_match.group(1) != info.version:
            errors.append(f"{path.relative_to(REFERENCE_ROOT)} -> missing or incorrect heading")
        index_ref = f"`version_pages/{info.version}/INDEX.md`"
        if index_ref not in text:
            errors.append(f"{path.relative_to(REFERENCE_ROOT)} -> missing page bundle index reference")


def validate_page_bundle_dirs(errors: list[str]) -> None:
    expected_versions = [info.version for info in ordered_versions()]
    actual_versions = sorted(
        path.name for path in VERSION_PAGES_ROOT.iterdir() if path.is_dir()
    )

    missing = [version for version in expected_versions if version not in actual_versions]
    extra = [version for version in actual_versions if version not in expected_versions]
    if missing:
        errors.append("Missing version page directories: " + ", ".join(missing))
    if extra:
        errors.append("Unexpected version page directories: " + ", ".join(extra))

    for info in ordered_versions():
        bundle_dir = VERSION_PAGES_ROOT / info.version
        if not bundle_dir.exists():
            continue
        if not (bundle_dir / "INDEX.md").exists():
            errors.append(f"version_pages/{info.version} -> missing INDEX.md")
        if info.coverage_mode == "delta-only":
            if not (bundle_dir / "release_note.md").exists():
                errors.append(f"version_pages/{info.version} -> missing release_note.md")
            if not (bundle_dir / "cmp_index.md").exists():
                errors.append(f"version_pages/{info.version} -> missing cmp_index.md")


def validate_v82_route_snippets(errors: list[str]) -> None:
    for path, snippet in V82_ROUTE_SNIPPETS.items():
        text = path.read_text(encoding="utf-8")
        if snippet not in text:
            errors.append(f"{path.relative_to(REFERENCE_ROOT)} -> missing required v8.2 route snippet")


def main() -> int:
    errors: list[str] = []
    validate_inventory(errors)
    validate_route_docs(errors)
    validate_page_bundle_dirs(errors)
    validate_v82_route_snippets(errors)

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Version routing validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
