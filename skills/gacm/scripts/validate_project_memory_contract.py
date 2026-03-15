#!/usr/bin/env python3
"""
Validate bundled GCAM project-memory contract invariants.

Checks:
- `docs/PROJECT.md` keeps the required persistent project-memory sections
- `docs/KNOWN_ISSUES.md` keeps the required runtime/tooling/coverage caveats
- long-term memory docs continue to preserve key project identity, scope, and honesty boundaries
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_DOC = REPO_ROOT / "docs" / "PROJECT.md"
KNOWN_ISSUES_DOC = REPO_ROOT / "docs" / "KNOWN_ISSUES.md"

HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

PROJECT_REQUIRED_TOP_LEVEL = (
    "# GCAM Skill Project",
)

PROJECT_SECTION_SNIPPETS = {
    "Project Intro": (
        "portable, self-contained workflow",
        "The skill name is `gacm`",
        "The skill name is `gacm` and the main entrypoint is `skills/gacm/SKILL.md`.",
    ),
    "Scope": (
        "Route correctly across historical families and the `v8.2` root-doc baseline without inventing missing source trees.",
        "Prefer pure text, CLI, and configuration editing over GUI walkthroughs.",
        "Recognize workspace layout, configuration editing, and headless query workflows without relying on UI-oriented upstream prose.",
    ),
    "Primary Sources (Local, Traceable)": (
        "The runtime skill uses only bundled references under `skills/gacm/reference/`.",
        "The source material used to author the skill is documented in `skills/gacm/reference/source_provenance.md`.",
    ),
    "Usage Summary": (
        "Route to the correct version before answering. Default to bundled `v8.2` only when the user does not specify a version.",
        "For exact version-page detail, open `reference/version_pages/<version>/BUNDLE_INDEX.md` and then the minimum necessary page files.",
        "For `v8.2`, treat the root `gcam-doc` tree as the bundled current full-topic baseline.",
        "For `delta-only` releases, answer using the exact release delta plus the minimum necessary bundled baseline topic docs.",
        "When a page routes to a CMP PDF, use the bundled CMP trace page for provenance unless the user provides the original binary asset separately.",
    ),
    "Open Tasks": (
        "Keep the bundled version catalog aligned with upstream GCAM releases.",
        "Continue expanding bundled topic coverage where the skill still compresses very specialized upstream material.",
        "Add more deterministic helper scripts if repeated manual authoring or validation steps appear.",
    ),
    "Decision Log": (
        "Explicitly standardized `v8.2 = root gcam-doc full documentation tree` across routing, navigation, and family docs.",
        "Added page-level bundled version trees under `reference/version_pages/` for full-tree versions and delta-specific page bundles for release-only versions.",
        "Reoriented the skill around agent-facing CLI, XML/configuration editing, and headless extraction instead of GUI-first workflows.",
        "Renamed generated page-bundle directory indexes to `BUNDLE_INDEX.md` so Windows case-insensitive filesystems do not clobber bundled upstream source pages such as `index.md`.",
    ),
}

KNOWN_ISSUES_REQUIRED_TOP_LEVEL = (
    "# Known Issues",
)

KNOWN_ISSUES_SECTION_SNIPPETS = {
    "Data and Tooling": (
        "`gcamreader` and `gcamextractor` are not installed by default",
        "the bundled skill does not invent repository state",
        "maintainer requirement, not a runtime dependency of the published skill",
    ),
    "Runtime Constraints": (
        "GCAM runs are resource intensive",
        "ModelInterface and XML database output require Java and BaseX",
    ),
    "Coverage": (
        "require a real GCAM repository checkout beyond the bundled conceptual docs",
        "`delta-only` releases in the bundled skill summarize release deltas rather than restating a full standalone doc set.",
        "The skill is substantially more explicit for `v8.2` root coverage now, but it still synthesizes topic docs rather than mirroring every upstream page one-to-one.",
        "Inherited page bundles are explicitly labeled",
        "shared topic docs are the authoritative agent-first headless CLI/config guidance.",
    ),
}


def extract_section(text: str, heading: str) -> str:
    matches = list(HEADER_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() != heading:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[start:end]
    raise ValueError(f"Missing section: {heading}")


def validate_doc(
    path: Path,
    top_level_snippets: tuple[str, ...],
    section_snippets: dict[str, tuple[str, ...]],
    errors: list[str],
) -> None:
    text = path.read_text(encoding="utf-8")

    for snippet in top_level_snippets:
        if snippet not in text:
            errors.append(f"{path.name} drifted; missing required top-level snippet: {snippet}")

    for heading, snippets in section_snippets.items():
        try:
            section = extract_section(text, heading)
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        for snippet in snippets:
            if snippet not in section:
                errors.append(
                    f"{path.name} section `{heading}` drifted; missing snippet: {snippet}"
                )


def main() -> int:
    errors: list[str] = []
    validate_doc(PROJECT_DOC, PROJECT_REQUIRED_TOP_LEVEL, PROJECT_SECTION_SNIPPETS, errors)
    validate_doc(
        KNOWN_ISSUES_DOC,
        KNOWN_ISSUES_REQUIRED_TOP_LEVEL,
        KNOWN_ISSUES_SECTION_SNIPPETS,
        errors,
    )

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Project memory contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
