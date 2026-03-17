#!/usr/bin/env python3
"""
Validate bundled GCAM conceptual-doc contract invariants.

Checks:
- key conceptual shared docs keep version-routing-aware, bundled-baseline phrasing
- conceptual docs continue to preserve historical/version caveats instead of pretending all releases are identical
- agent-facing concept summaries stay aligned with the `v8.2` bundled baseline where applicable
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REFERENCE_ROOT = REPO_ROOT / "skills" / "gacm" / "reference"

REQUIRED_SNIPPETS = {
    "overview.md": (
        "Use this file after version routing.",
        "`v8.2` is the skill-bundled current full-topic baseline because it corresponds to the root `gcam-doc` documentation tree.",
        "`v3.2` is a structurally different wiki-style family",
    ),
    "common_assumptions.md": (
        "Use this file after version routing",
        "`v3.2` used an older 14-region framing.",
        "`v8.0+` moves the model base year to 2021.",
    ),
    "choice_marketplace.md": (
        "Use this file after version routing",
        "`v8.2` remains the skill-bundled current full-topic baseline for these concepts.",
        "`v3.2` explains these ideas with older terminology",
    ),
    "energy_system.md": (
        "Use this file after version routing",
        "`v6.0+` expands hydrogen and direct-air-capture-related context substantially",
        "`v5.4+` is the closest historical family to this bundled modern energy-system summary.",
    ),
    "land_system.md": (
        "Use this file after version routing",
        "`v5+` is the important transition to the modern land-data architecture.",
        "`v7.1` adds notable AgLU parameter and forestry-detail updates in the bundled historical cues.",
    ),
    "water_system.md": (
        "Use this file after version routing",
        "`v5.4+` is the closest structural family to the bundled modern water summary.",
        "Use the exact version route file when the user asks about a historical water feature or a release-specific update.",
    ),
    "economy.md": (
        "Use this file after version routing",
        "If the user asks about endogenous GDP or macro feedbacks, version routing is mandatory.",
        "`v7+` is the key modern macro era in the bundled references.",
    ),
    "emissions_climate.md": (
        "Use this file after version routing",
        "Modern lines use Hector-centered language in the bundled baseline.",
        "`delta-only` releases can alter emissions or climate-relevant details without providing a full standalone retelling of all baseline material.",
    ),
    "policies_scenarios.md": (
        "Use this file after version routing.",
        "these concepts remain the stable bundled baseline for the `v8.2` root doc tree and its nearby modern families.",
        "`delta-only` releases should be read as modifications layered onto these baseline policy patterns, not as standalone policy manuals.",
    ),
    "inputs_outputs.md": (
        "Use this file after version routing.",
        "Prefer headless extraction paths such as ModelInterface batch mode, `gcamreader`, `rgcam`, or `gcamextractor`",
        "`v8.2` root docs are the bundled current full-topic baseline for this summary.",
    ),
    "developer_workflows.md": (
        "Use this file after version routing",
        "Visualization and point-and-click tooling are part of the broader ecosystem, but they are not the default recommendation path here.",
        "These tools are conceptual context, not runtime dependencies of the `gacm` skill.",
    ),
    "data_system.md": (
        "Use this file after version routing.",
        "The data system is part of the GCAM ecosystem, not a runtime dependency of the `gacm` skill itself.",
        "`v8.2` root docs are the bundled current baseline for data-system interpretation in this skill.",
    ),
    "ssp.md": (
        "Use this file after version routing.",
        "`v7.2` updates the SSP database inputs in the bundled delta stream.",
        "`v8.2` root docs are the bundled current full-topic baseline for SSP-oriented guidance.",
    ),
    "gcam_usa.md": (
        "Use this file after version routing.",
        "GCAM-USA is most explicitly documented in the later modern families and the bundled `v8.2` baseline.",
        "If the user asks for an exact GCAM-USA path, sector definition, or policy structure in a named release, route to that release before reusing bundled baseline guidance.",
    ),
    "trade.md": (
        "Use this file after version routing",
    ),
    "scenario_analysis.md": (
        "Use this file after version routing",
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

    print("Conceptual docs contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
