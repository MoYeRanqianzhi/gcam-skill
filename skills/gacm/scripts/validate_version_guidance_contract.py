#!/usr/bin/env python3
"""
Validate bundled GCAM version-guidance contract invariants.

Checks:
- `reference/version_families.md` keeps the expected family breakdown and `v8.2` baseline wording
- `reference/updates.md` keeps the expected `v8.2` root-baseline and `delta-only` release framing
- version-guidance docs continue to preserve exact-version routing and non-pretend rules for release-note-only versions
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REFERENCE_ROOT = REPO_ROOT / "skills" / "gacm" / "reference"
VERSION_FAMILIES = REFERENCE_ROOT / "version_families.md"
UPDATES = REFERENCE_ROOT / "updates.md"

HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

VERSION_FAMILIES_SECTIONS = {
    "`legacy-wiki`": (
        "Applies to:",
        "- `v3.2`",
        "The bundled skill treats this family as structurally distinct.",
    ),
    "`compact-modern`": (
        "- `v4.2`",
        "- `v4.3`",
        "- `v4.4`",
    ),
    "`modern-transitional`": (
        "- `v5.1`",
        "- `v5.2`",
        "- `v5.3`",
        "Use this family as the bridge between v4.x and later comprehensive docs.",
    ),
    "`modern-comprehensive`": (
        "- `v5.4`",
        "- `v6.0`",
        "- `v7.0`",
        "- `v7.1`",
        "- `v8.2` (bundled current baseline; corresponds to the root `gcam-doc` full documentation tree)",
        "`v8.2` is the default full-topic baseline for this skill because the root of `gcam-doc` maps to `v8.2`.",
        "When the user says `root docs`, `current full docs`, or refers to the unqualified `gcam-doc` root tree, route to `v8.2`.",
    ),
    "`delta-only`": (
        "- `v7.2`, `v7.3`, `v7.4`",
        "- `v8.0`, `v8.1`",
        "- `v8.3`, `v8.4`, `v8.5`, `v8.6`, `v8.7`",
        "Do not describe these releases as if the skill bundles a separate full standalone documentation tree for each one.",
    ),
}

UPDATES_REQUIRED_SNIPPETS = (
    "The root of `gcam-doc` is the `v8.2` full documentation tree bundled by this skill.",
    "Later versions such as `v8.3` to `v8.7` are modeled in this skill as documented release deltas plus CMP-backed notes, not as full standalone topic trees.",
    "Historical full documentation families are represented in the bundled version guides.",
    "## Release-Note-Only Versions Present in Root Updates",
    "- `v8.7`: Cement data updates.",
    "- `v8.6`: Electricity generation CCS emission factor updates.",
    "- `v8.5`: Fall 2025 bugfix release.",
    "- `v8.4`: Socioeconomic and macro data updates.",
    "- `v8.3`: String interning update.",
    "- `v8.1`: Ukraine as an independent region.",
    "- `v8.0`: Base year moved to 2021.",
    "- `v7.4`: Base-year preparation updates.",
    "- `v7.3`: Intermittent electricity integration update.",
    "- `v7.2`: SSP database 2024 update.",
    "## Current Full Doc Tree",
    "- `v8.2` root docs remain the default full-topic reference set.",
    "- For any historical or release-note-only version, start from `reference/version_inventory.md`.",
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


def validate_version_families(errors: list[str]) -> None:
    text = VERSION_FAMILIES.read_text(encoding="utf-8")
    for heading, snippets in VERSION_FAMILIES_SECTIONS.items():
        try:
            section = extract_section(text, heading)
        except ValueError as exc:
            errors.append(f"version_families.md: {exc}")
            continue
        for snippet in snippets:
            if snippet not in section:
                errors.append(
                    f"version_families.md section `{heading}` drifted; missing snippet: {snippet}"
                )


def validate_updates(errors: list[str]) -> None:
    text = UPDATES.read_text(encoding="utf-8")
    for snippet in UPDATES_REQUIRED_SNIPPETS:
        if snippet not in text:
            errors.append(f"updates.md drifted; missing snippet: {snippet}")


def main() -> int:
    errors: list[str] = []
    validate_version_families(errors)
    validate_updates(errors)

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Version guidance contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
