#!/usr/bin/env python3
"""
Validate bundled GCAM page-bundle contract invariants.

Checks:
- `reference/version_pages/README.md` keeps the progressive-disclosure and non-pretend rules
- full-tree bundle indexes keep family/coverage/source/page-count metadata
- delta-only bundle indexes keep release-note/CMP-first routing semantics
- delta-only release-note and CMP index pages keep their required structure
"""

from __future__ import annotations

import re
from pathlib import Path

from generate_bundled_pages import DELTA_SOURCE_MAP
from version_catalog import VERSION_PAGES_ROOT, ordered_versions


README = VERSION_PAGES_ROOT / "README.md"
PAGE_COUNT_RE = re.compile(r"^- Page count: `(\d+)`$", re.MULTILINE)
CMP_COUNT_RE = re.compile(r"^- CMP reference count: `(\d+)`$", re.MULTILINE)


def expected_source_root(version: str, coverage_mode: str) -> str:
    if coverage_mode == "delta-only":
        return "gcam-doc root updates stream"
    if version == "v8.2":
        return "gcam-doc root tree"
    return f"gcam-doc/{version}"


def validate_root_readme(errors: list[str]) -> None:
    text = README.read_text(encoding="utf-8")
    required = (
        "# Version Page Bundles",
        "This directory contains the page-level bundled reference trees for all GCAM versions represented by the `gacm` skill.",
        "- Open the exact version route file first.",
        "- Then open `version_pages/<version>/INDEX.md` only when page-level detail is needed.",
        "- For full-tree versions, page files are adapted from the authoring markdown sources.",
        "- For `delta-only` versions, page files capture the release delta and source trace rather than pretending a full standalone tree exists.",
        "- When a version links to a page that is absent from its own authoring tree, the bundle may include a clearly labeled inherited or trace page instead of silently dropping the route.",
    )
    for snippet in required:
        if snippet not in text:
            errors.append(f"version_pages/README.md drifted; missing snippet: {snippet}")


def validate_full_tree_index(version: str, path: Path, family: str, coverage_mode: str, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    required = (
        f"# {version} Detailed Page Bundle",
        f"This directory is the page-level bundled reference set for GCAM `{version}`.",
        f"- Family: `{family}`",
        f"- Coverage mode: `{coverage_mode}`",
        f"- Source root: `{expected_source_root(version, coverage_mode)}`",
        "Progressive-disclosure rule:",
        "- Start from the version route file.",
        "- Open this index only when the user needs page-level detail for this version.",
        "- Then open only the specific page file relevant to the task.",
        "## Bundled Pages",
    )
    for snippet in required:
        if snippet not in text:
            errors.append(f"version_pages/{version}/INDEX.md drifted; missing snippet: {snippet}")

    match = PAGE_COUNT_RE.search(text)
    if not match:
        errors.append(f"version_pages/{version}/INDEX.md drifted; missing page-count metadata")
    elif int(match.group(1)) <= 0:
        errors.append(f"version_pages/{version}/INDEX.md has non-positive page count")


def validate_delta_index(version: str, path: Path, family: str, coverage_mode: str, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    required = (
        f"# {version} Detailed Page Bundle",
        f"This directory is the bundled page-level delta set for GCAM `{version}`.",
        f"- Family: `{family}`",
        f"- Coverage mode: `{coverage_mode}`",
        "- Source root: `gcam-doc root updates stream`",
        "Progressive-disclosure rule:",
        "- Open `release_note.md` first.",
        "- Then inspect `cmp_index.md` if method provenance or release-document traceability matters.",
        "- Then combine those with the minimum bundled baseline topic docs needed for the task.",
        "## Bundled Files",
        "- `release_note.md`",
        "- `cmp_index.md`",
    )
    for snippet in required:
        if snippet not in text:
            errors.append(f"version_pages/{version}/INDEX.md drifted; missing snippet: {snippet}")

    match = CMP_COUNT_RE.search(text)
    expected_count = len(DELTA_SOURCE_MAP.get(version, ()))
    if not match:
        errors.append(f"version_pages/{version}/INDEX.md drifted; missing CMP-count metadata")
    elif int(match.group(1)) != expected_count:
        errors.append(
            f"version_pages/{version}/INDEX.md CMP reference count drifted; expected {expected_count}"
        )


def validate_delta_release_note(version: str, errors: list[str]) -> None:
    path = VERSION_PAGES_ROOT / version / "release_note.md"
    text = path.read_text(encoding="utf-8")
    required = (
        f"# {version} Release Note",
        f"Bundled release-note page for GCAM `{version}`.",
        "- Coverage mode: `delta-only`",
        "- Source root: `gcam-doc root updates stream`",
        "- Source path: `updates.md`",
        "## Release Summary",
        "## Source Trace",
        "- `gcam-doc/updates.md`",
    )
    for snippet in required:
        if snippet not in text:
            errors.append(f"version_pages/{version}/release_note.md drifted; missing snippet: {snippet}")


def validate_delta_cmp_index(version: str, errors: list[str]) -> None:
    path = VERSION_PAGES_ROOT / version / "cmp_index.md"
    text = path.read_text(encoding="utf-8")
    required = (
        f"# {version} CMP Index",
        f"Bundled CMP trace page for GCAM `{version}`.",
        "Confidence labels:",
        "- `direct`: filename maps directly to the release note title",
        "- `related`: filename appears related, but the mapping is not uniquely guaranteed by the visible filenames alone",
        "## CMP References",
    )
    for snippet in required:
        if snippet not in text:
            errors.append(f"version_pages/{version}/cmp_index.md drifted; missing snippet: {snippet}")

    cmp_refs = DELTA_SOURCE_MAP.get(version, ())
    if cmp_refs:
        for ref, confidence in cmp_refs:
            snippet = f"- `{ref}` ({confidence})"
            if snippet not in text:
                errors.append(
                    f"version_pages/{version}/cmp_index.md drifted; missing CMP reference: {snippet}"
                )
    else:
        snippet = (
            "- No uniquely identified CMP PDF is recorded for this version from the visible "
            "release-note and filename evidence alone."
        )
        if snippet not in text:
            errors.append(
                f"version_pages/{version}/cmp_index.md drifted; missing no-reference statement"
            )


def main() -> int:
    errors: list[str] = []
    validate_root_readme(errors)

    for info in ordered_versions():
        index_path = VERSION_PAGES_ROOT / info.version / "INDEX.md"
        if info.coverage_mode == "delta-only":
            validate_delta_index(info.version, index_path, info.family, info.coverage_mode, errors)
            validate_delta_release_note(info.version, errors)
            validate_delta_cmp_index(info.version, errors)
        else:
            validate_full_tree_index(
                info.version,
                index_path,
                info.family,
                info.coverage_mode,
                errors,
            )

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Page bundle contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
