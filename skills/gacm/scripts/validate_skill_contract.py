#!/usr/bin/env python3
"""
Validate bundled GCAM SKILL.md contract invariants.

Checks:
- SKILL frontmatter exists and keeps the canonical skill name `gacm`
- description continues to advertise GCAM trigger context and the default `v8.2` baseline
- core SKILL sections preserve version-routing, CLI-first, and progressive-disclosure instructions
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SKILL_FILE = REPO_ROOT / "skills" / "gacm" / "SKILL.md"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^(name|description):\s*(.+?)\s*$", re.MULTILINE)

REQUIRED_DESCRIPTION_SNIPPETS = (
    "Portable GCAM expertise as a self-contained open-source skill.",
    "If the user names a GCAM version",
    "default to the bundled current baseline v8.2.",
)

REQUIRED_SECTION_SNIPPETS = {
    "Agent Operating Rules": (
        "Default to pure text, command-line, and configuration-file workflows.",
        "Prefer editing XML/configuration files and running headless tools over GUI instructions.",
        "Do not claim access to `gcam-doc`, `gcam-core`, `gcamreader`, or `gcamextractor` checkouts unless the user actually provides them.",
    ),
    "Version Routing": (
        "If the user explicitly names a version, use that version exactly.",
        "If the user does not name a version, default to the bundled current baseline `v8.2`.",
        "Treat `delta-only` releases as release-specific deltas layered onto the broader bundled baseline. State that explicitly.",
    ),
    "Non-Negotiables": (
        "Search bundled references first. Use `scripts/doc_search.py`.",
        "Cite the bundled reference files you relied on.",
        "Use the exact version route requested by the user.",
    ),
    "Progressive Disclosure": (
        "Open `reference/version_inventory.md` first",
        "open `reference/versions/<version>.md`.",
        "open `reference/version_pages/<version>/BUNDLE_INDEX.md`.",
        "Use `reference/navigation.md` to choose the smallest topic set that answers the request.",
    ),
    "Task Triage": (
        "**All requests**: `reference/version_inventory.md`",
        "**Historical version or release-note-only version**: `reference/versions/<version>.md`",
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


def validate_frontmatter(text: str, errors: list[str]) -> None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append("SKILL.md is missing YAML frontmatter")
        return

    fields = dict(FIELD_RE.findall(match.group(1)))
    if fields.get("name") != "gacm":
        errors.append("SKILL.md frontmatter name must stay `gacm`")

    description = fields.get("description")
    if not description:
        errors.append("SKILL.md frontmatter is missing description")
        return

    for snippet in REQUIRED_DESCRIPTION_SNIPPETS:
        if snippet not in description:
            errors.append(f"SKILL.md description drifted; missing snippet: {snippet}")


def validate_sections(text: str, errors: list[str]) -> None:
    for heading, snippets in REQUIRED_SECTION_SNIPPETS.items():
        try:
            section = extract_section(text, heading)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for snippet in snippets:
            if snippet not in section:
                errors.append(f"SKILL.md section `{heading}` drifted; missing snippet: {snippet}")


def main() -> int:
    text = SKILL_FILE.read_text(encoding="utf-8")
    errors: list[str] = []
    validate_frontmatter(text, errors)
    validate_sections(text, errors)

    if errors:
        for item in errors:
            print(item)
        return 1

    print("Skill contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
