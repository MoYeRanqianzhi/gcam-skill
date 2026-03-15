#!/usr/bin/env python3
"""
Validate bundled GCAM operational-doc contract invariants.

Checks:
- key agent-facing operational docs keep their CLI/headless/config-first posture
- high-impact run/query/build/workspace/version/tool rules remain explicit
- historical UI wording continues to be framed as evidence rather than default workflow
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REFERENCE_ROOT = REPO_ROOT / "skills" / "gacm" / "reference"

REQUIRED_SNIPPETS = {
    "running_gcam.md": (
        "# Running GCAM (Headless CLI First)",
        "`v8.2` is the bundled full-topic baseline.",
        "Treat double-click instructions in upstream user guides as historical packaging notes, not as the default workflow.",
        "`Model run completed.`",
        "### Path 2: Headless ModelInterface batch mode",
        "Translate those into CLI/config equivalents unless the user explicitly asks for the historical UI path.",
    ),
    "configuration_workflows.md": (
        "Agent-first guide to editing GCAM runtime configuration files and related XML control files.",
        "Read `exe/logs/main_log.txt` before changing solver settings.",
        "Target finder should start from `configuration_policy.xml`, not the reference configuration.",
        "### `v5.4` through `v8.2`",
        "### `v3.2`",
    ),
    "query_automation.md": (
        "Agent-first guide to extracting GCAM results through query XML, batch commands, and headless tooling.",
        "Do not hardcode those paths. Detect them from the actual workspace the user provides.",
        "## Preferred Automation Order",
        "This is the most direct way to reuse GCAM query XML from the command line.",
        "Use a higher-level extraction library when:",
    ),
    "workspace_layouts.md": (
        "Guide to recognizing GCAM workspace structure from paths and files instead of guessing.",
        "Never assume a machine-specific absolute path.",
        "If none of the above are clear, ask for a directory listing rather than guessing.",
        "keep the nested root exactly as documented",
    ),
    "version_operation_notes.md": (
        "Route exact version first with `version_inventory.md`.",
        "This is the bundled current baseline and corresponds to the root `gcam-doc` tree.",
        "These are `delta-only` routes in the skill.",
        "Do not pretend each one has a full standalone topic tree in the bundle.",
        "## Decision Rule",
    ),
    "building_gcam.md": (
        "# Building GCAM (Command Line First)",
        "Prefer command-line builds.",
        "Compile only when:",
        "msbuild cvs/objects/build/vc10/objects.vcxproj /p:Configuration=Release /p:Platform=x64",
        "summarize those pages into CLI build actions instead of reproducing IDE click paths unless the user explicitly requests them.",
    ),
    "tools.md": (
        "# GCAM Tooling (Headless Extraction)",
        "Prefer dedicated headless tools over interactive ModelInterface workflows when they solve the task.",
        "## gcamreader (Python)",
        "## gcamextractor (R)",
        "Treat this as a headless query engine, not as the preferred human-facing interface.",
    ),
}


def main() -> int:
    errors: list[str] = []
    for name, snippets in REQUIRED_SNIPPETS.items():
        path = REFERENCE_ROOT / name
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{name} drifted; missing required snippet: {snippet}")

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Operational docs contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
