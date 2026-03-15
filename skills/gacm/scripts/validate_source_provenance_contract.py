#!/usr/bin/env python3
"""
Validate bundled GCAM source-provenance contract invariants.

Checks:
- `reference/source_provenance.md` keeps the required provenance sections
- provenance language continues to state the open-source, portable, bundled nature of the skill
- runtime-vs-authoring boundaries remain explicit
- the `v8.2` root `gcam-doc` baseline and non-pretend rules remain explicit
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SOURCE_PROVENANCE = REPO_ROOT / "skills" / "gacm" / "reference" / "source_provenance.md"

HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

REQUIRED_SECTION_SNIPPETS = {
    "Upstream Materials Used During Skill Authoring": (
        "GCAM documentation across historical versioned doc trees from `v3.2` through `v7.1`",
        "The root `gcam-doc` documentation tree corresponding to `v8.2`",
        "Release updates through `v8.7`",
        "`gcamreader` README and CLI usage used during authoring",
        "`gcamextractor` README and vignette usage used during authoring",
    ),
    "What This Means": (
        "The skill is designed to be portable and open-source.",
        "It does not require those upstream repositories to exist beside the skill at runtime.",
        "It also bundles page-level adapted version trees under `reference/version_pages/` so the skill can progressively disclose exact version pages without external repo dependence.",
        "The page-level bundles are adapted into text-only form; images and screenshots are omitted rather than bundled as binary assets.",
        "Shared topic docs deliberately translate human-facing UI guidance into agent-facing CLI, config-editing, and headless extraction workflows.",
        "`coverage_map.md` documents how the bundled `v8.2` topic docs map back to the root source topics.",
    ),
    "What This Skill Does Not Pretend": (
        "It does not claim to contain every line of every upstream documentation page.",
        "It does not claim access to the user's local GCAM checkout unless the user provides one.",
        "It does not silently substitute one version for another.",
    ),
    "When To Inspect a Real Checkout": (
        "the user provides one",
        "the user asks for exact file edits, exact XML snippets from their project, or exact current repository state",
        "the bundled conceptual references are insufficient for the requested implementation task",
    ),
}

REQUIRED_TOP_LEVEL_SNIPPET = "This skill is a bundled synthesis, not a verbatim vendor drop."


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
    text = SOURCE_PROVENANCE.read_text(encoding="utf-8")
    errors: list[str] = []

    if REQUIRED_TOP_LEVEL_SNIPPET not in text:
        errors.append(
            "source_provenance.md drifted; missing required top-level provenance statement"
        )

    for heading, snippets in REQUIRED_SECTION_SNIPPETS.items():
        try:
            section = extract_section(text, heading)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for snippet in snippets:
            if snippet not in section:
                errors.append(
                    f"source_provenance.md section `{heading}` drifted; missing snippet: {snippet}"
                )

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Source provenance contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
