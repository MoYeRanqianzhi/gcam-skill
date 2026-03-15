#!/usr/bin/env python3
"""
Validate bundled GCAM coverage-map invariants.

Checks:
- `coverage_map.md` keeps the required coverage sections
- all top-level `gcam-doc/*.md` source pages are explicitly accounted for
- key shared topic docs remain referenced from the coverage map
- the `v8.2` root baseline and page-bundle coverage statements remain explicit
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
AUTHORING_ROOT = REPO_ROOT / "gcam-doc"
COVERAGE_MAP = REPO_ROOT / "skills" / "gacm" / "reference" / "coverage_map.md"

HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CODE_MD_RE = re.compile(r"`([^`]+\.md)`")

REQUIRED_SECTION_SNIPPETS = {
    "Root `v8.2` Topic Coverage": (
        "`index.md`, `overview.md` -> `overview.md`",
        "`community-guide.md`, `fusion.md`, `dev-guide.md`, `dev-guide/*` -> `developer_workflows.md`",
        "`toc.md` -> `navigation.md`",
    ),
    "Root `v8.2` Bundle-Only / Meta Pages": (
        "`references.md` -> page-bundle-only trace; no dedicated synthesized shared topic doc",
        "`LICENSE.md` -> page-bundle-only legal/reference artifact; no dedicated synthesized shared topic doc",
    ),
    "Page-Level Version Bundles": (
        "`reference/version_pages/v8.2/*` contains adapted page-level bundled copies of the `gcam-doc` root and `dev-guide` markdown sources.",
    ),
    "Version Routing Coverage": (
        "`v8.2` is the bundled current full-topic baseline because it maps to the root `gcam-doc` tree.",
    ),
    "Tooling Coverage": (
        "`gcamreader` authoring references -> `tools.md`",
        "`gcamextractor` authoring references -> `tools.md`",
    ),
}

REQUIRED_SHARED_DOC_REFS = (
    "overview.md",
    "configuration_workflows.md",
    "query_automation.md",
    "workspace_layouts.md",
    "developer_workflows.md",
    "version_operation_notes.md",
    "navigation.md",
    "tools.md",
)


def extract_section(text: str, heading: str) -> str:
    matches = list(HEADER_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() != heading:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[start:end]
    raise ValueError(f"Missing section: {heading}")


def validate_sections(text: str, errors: list[str]) -> None:
    for heading, snippets in REQUIRED_SECTION_SNIPPETS.items():
        try:
            section = extract_section(text, heading)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for snippet in snippets:
            if snippet not in section:
                errors.append(
                    f"coverage_map.md section `{heading}` drifted; missing snippet: {snippet}"
                )


def validate_root_source_coverage(text: str, errors: list[str]) -> None:
    if not AUTHORING_ROOT.exists():
        errors.append(f"Missing authoring root required for coverage-map validation: {AUTHORING_ROOT}")
        return

    referenced = set(CODE_MD_RE.findall(text))
    actual_root_files = {path.name for path in AUTHORING_ROOT.glob("*.md")}
    missing = sorted(name for name in actual_root_files if name not in referenced)
    if missing:
        errors.append(
            "coverage_map.md does not account for all top-level gcam-doc root pages: "
            + ", ".join(missing)
        )


def validate_shared_doc_refs(text: str, errors: list[str]) -> None:
    for name in REQUIRED_SHARED_DOC_REFS:
        if f"`{name}`" not in text:
            errors.append(f"coverage_map.md is missing required shared-doc reference: {name}")


def main() -> int:
    text = COVERAGE_MAP.read_text(encoding="utf-8")
    errors: list[str] = []
    validate_sections(text, errors)
    validate_root_source_coverage(text, errors)
    validate_shared_doc_refs(text, errors)

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Coverage map contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
