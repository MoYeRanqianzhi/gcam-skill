#!/usr/bin/env python3
"""
Validate bundled GCAM navigation contract invariants.

Checks:
- `reference/navigation.md` keeps the expected routing sections
- navigation remains version-first, CLI-first, and progressive-disclosure oriented
- runtime rules continue to state that the skill is self-contained unless the user supplies external context
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
NAVIGATION = REPO_ROOT / "skills" / "gacm" / "reference" / "navigation.md"

HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

REQUIRED_SECTION_SNIPPETS = {
    "Agent Mode": (
        "This skill is optimized for agent use and headless CLI/config workflows.",
        "Default to command-line execution, XML/configuration editing, and headless extraction.",
        "Use page-level historical UI material only when the user explicitly asks for ModelInterface or IDE behavior from a specific release.",
        "Prefer shared topic docs for operational guidance and page bundles for traceable evidence.",
    ),
    "First Decision: Version": (
        "Always determine version before topic.",
        "If the user specifies a version, open `version_inventory.md` and then `versions/<version>.md`.",
        "If the user does not specify a version, default to the bundled baseline `v8.2`.",
        "If the user asks for comparison, open only the involved version route files plus the minimum topic docs needed.",
    ),
    "Second Decision: Detail Level": (
        "For cross-version conceptual answers, use the shared topic docs below.",
        "For exact version page detail, open `version_pages/<version>/BUNDLE_INDEX.md` and then only the needed page file.",
        "For `delta-only` versions, open `version_pages/<version>/release_note.md` first and `cmp_index.md` when provenance matters.",
    ),
    "Third Decision: Topic": (
        "After version routing, open only the topic docs needed for the task:",
        "`configuration_workflows.md`",
        "`query_automation.md`",
        "`workspace_layouts.md`",
        "`version_operation_notes.md`",
    ),
    "Version Families": (
        "Open `version_families.md` when the user asks about structural differences across eras.",
    ),
    "Version Page Bundles": (
        "Open `version_pages/README.md` if you need the rules for the page-level bundled reference trees.",
    ),
    "Runtime Rule": (
        "This skill is self-contained.",
        "Do not assume the user has a local `gcam-doc`, `gcam-core`, `gcamreader`, or `gcamextractor` checkout unless they explicitly provide one.",
    ),
    "Optional External Context": (
        "If the user explicitly provides a checkout, workspace, or file paths, you may inspect them as additional project context.",
        "That external context is never required. The bundled references remain the default conceptual baseline.",
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


def main() -> int:
    text = NAVIGATION.read_text(encoding="utf-8")
    errors: list[str] = []

    for heading, snippets in REQUIRED_SECTION_SNIPPETS.items():
        try:
            section = extract_section(text, heading)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for snippet in snippets:
            if snippet not in section:
                errors.append(
                    f"navigation.md section `{heading}` drifted; missing snippet: {snippet}"
                )

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Navigation contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
