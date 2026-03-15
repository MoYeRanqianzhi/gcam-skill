#!/usr/bin/env python3
"""
Generate bundled version-routing reference files for the open-source `gacm` skill.
"""

from __future__ import annotations

from pathlib import Path

from version_catalog import bundled_topic_docs, family_notes, ordered_versions


REFERENCE_DIR = Path(__file__).resolve().parent.parent / "reference"
VERSIONS_DIR = REFERENCE_DIR / "versions"
BUNDLE_INDEX_NAME = "BUNDLE_INDEX.md"


def render_inventory() -> str:
    lines = [
        "# Version Inventory",
        "",
        "This file is the authoritative bundled version-routing table for the `gacm` skill.",
        "",
        "Rules:",
        "- If the user specifies a GCAM version, route to that exact bundled version file first.",
        "- If the user does not specify a version, default to the bundled current baseline: `v8.2`.",
        "- `delta-only` releases bundle only their documented deltas, not a full standalone restatement of every topic.",
        "- Never claim access to a version-specific upstream checkout unless the user actually provides one.",
        "",
        "| Version | Family | Coverage Mode | Route |",
        "| --- | --- | --- | --- |",
    ]
    for info in ordered_versions():
        lines.append(
            f"| `{info.version}` | `{info.family}` | `{info.coverage_mode}` | `versions/{info.version}.md` |"
        )
    lines.extend(
        [
            "",
            "## Detailed Version Page Bundles",
            f"For page-level detail, open `version_pages/<version>/{BUNDLE_INDEX_NAME}` after routing to the exact version.",
            "",
            "## Shared Topic Docs",
            "These bundled topic docs are the main progressive-disclosure entry points after version routing.",
        ]
    )
    for name in bundled_topic_docs():
        lines.append(f"- `{name}`")
    return "\n".join(lines) + "\n"


def render_version_file(info) -> str:
    lines = [
        f"# {info.version}",
        "",
        f"- Family: `{info.family}`",
        f"- Coverage mode: `{info.coverage_mode}`",
    ]
    if info.aliases:
        lines.append(f"- Accepted aliases: `{', '.join(info.aliases)}`")

    lines.extend(["", "## Routing Rule"])
    if info.coverage_mode == "bundled-baseline":
        lines.append(
            "Use the shared bundled topic docs directly. This is the default baseline when the user does not specify a version."
        )
    elif info.coverage_mode == "delta-only":
        lines.append(
            "Use this file for the release-specific delta, then load only the shared topic docs needed for the user task. Do not pretend the skill contains a full standalone restatement of this release."
        )
    else:
        lines.append(
            "Use this file first, then load the shared topic docs relevant to the user task. Apply the version-specific cues below while answering."
        )

    lines.extend(["", "## Family Notes"])
    for note in family_notes(info.family):
        lines.append(f"- {note}")

    if info.summary:
        lines.extend(["", "## Summary"])
        for bullet in info.summary:
            lines.append(f"- {bullet}")

    if info.deltas:
        lines.extend(["", "## Version-Specific Cues"])
        for bullet in info.deltas:
            lines.append(f"- {bullet}")

    if info.notes:
        lines.extend(["", "## Cautions"])
        for bullet in info.notes:
            lines.append(f"- {bullet}")

    lines.extend(
        [
            "",
            "## Detailed Bundled Page Directory",
            f"- `version_pages/{info.version}/{BUNDLE_INDEX_NAME}`",
            "",
            "## Shared Topic Docs To Load On Demand",
        ]
    )
    for name in bundled_topic_docs():
        lines.append(f"- `{name}`")

    return "\n".join(lines) + "\n"


def main() -> int:
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

    (REFERENCE_DIR / "version_inventory.md").write_text(render_inventory(), encoding="utf-8")
    for info in ordered_versions():
        (VERSIONS_DIR / f"{info.version}.md").write_text(render_version_file(info), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
