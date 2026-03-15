#!/usr/bin/env python3
"""
Validate semantic-contract coverage for root skill docs.

Checks:
- every root shared runtime doc is assigned to a dedicated semantic contract owner
- every persistent memory doc in `docs/` is assigned to a dedicated semantic contract owner
- `SKILL.md` is explicitly covered

This prevents future docs from existing with only inventory/link validation and no
behavior-level contract.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REFERENCE_ROOT = REPO_ROOT / "skills" / "gacm" / "reference"
DOCS_ROOT = REPO_ROOT / "docs"
SKILL_FILE = REPO_ROOT / "skills" / "gacm" / "SKILL.md"
SCRIPTS_ROOT = REPO_ROOT / "skills" / "gacm" / "scripts"

CONTRACT_OWNERS: dict[str, set[str]] = {
    "validate_conceptual_docs_contract.py": {
        "reference/overview.md",
        "reference/common_assumptions.md",
        "reference/choice_marketplace.md",
        "reference/energy_system.md",
        "reference/land_system.md",
        "reference/water_system.md",
        "reference/economy.md",
        "reference/emissions_climate.md",
        "reference/policies_scenarios.md",
        "reference/inputs_outputs.md",
        "reference/developer_workflows.md",
        "reference/data_system.md",
        "reference/ssp.md",
        "reference/gcam_usa.md",
    },
    "validate_operational_docs_contract.py": {
        "reference/running_gcam.md",
        "reference/configuration_workflows.md",
        "reference/query_automation.md",
        "reference/workspace_layouts.md",
        "reference/version_operation_notes.md",
        "reference/building_gcam.md",
        "reference/tools.md",
    },
    "validate_solver_contract.py": {
        "reference/solver.md",
    },
    "validate_navigation_contract.py": {
        "reference/navigation.md",
    },
    "validate_version_guidance_contract.py": {
        "reference/version_families.md",
        "reference/updates.md",
    },
    "validate_coverage_map_contract.py": {
        "reference/coverage_map.md",
    },
    "validate_source_provenance_contract.py": {
        "reference/source_provenance.md",
    },
    "validate_version_routes.py": {
        "reference/version_inventory.md",
    },
    "validate_project_memory_contract.py": {
        "docs/PROJECT.md",
        "docs/KNOWN_ISSUES.md",
    },
    "validate_maintenance_memory_contract.py": {
        "docs/DEVELOPMENT.md",
        "docs/CHANGELOG.md",
    },
    "validate_skill_contract.py": {
        "skills/gacm/SKILL.md",
    },
}


def main() -> int:
    errors: list[str] = []

    for validator_name in CONTRACT_OWNERS:
        if not (SCRIPTS_ROOT / validator_name).exists():
            errors.append(f"Semantic coverage references missing validator script: {validator_name}")

    actual_targets = {
        f"reference/{path.name}" for path in sorted(REFERENCE_ROOT.glob("*.md"))
    }
    actual_targets.update(
        f"docs/{path.name}" for path in sorted(DOCS_ROOT.glob("*.md"))
    )
    actual_targets.add("skills/gacm/SKILL.md")

    covered_targets = set().union(*CONTRACT_OWNERS.values())

    missing = sorted(actual_targets - covered_targets)
    unexpected = sorted(covered_targets - actual_targets)

    if missing:
        errors.append(
            "Root skill docs exist without semantic contract ownership: " + ", ".join(missing)
        )
    if unexpected:
        errors.append(
            "Semantic contract ownership references missing docs: " + ", ".join(unexpected)
        )

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Semantic contract coverage validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
