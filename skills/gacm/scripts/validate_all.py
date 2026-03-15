#!/usr/bin/env python3
"""
Run the full bundled GCAM skill validation suite.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SELF_NAME = Path(__file__).name

VALIDATION_STEPS = (
    "validate_portability.py",
    "validate_authoring_sources.py",
    "validate_doc_search.py",
    "validate_page_bundle_content_parity.py",
    "validate_bundled_pages.py",
    "validate_filesystem_hygiene.py",
    "validate_page_bundle_contract.py",
    "validate_conceptual_docs_contract.py",
    "validate_maintenance_memory_contract.py",
    "validate_semantic_contract_coverage.py",
    "validate_solver_contract.py",
    "validate_coverage_map_contract.py",
    "validate_operational_docs_contract.py",
    "validate_project_memory_contract.py",
    "validate_shared_references.py",
    "validate_navigation_contract.py",
    "validate_skill_contract.py",
    "validate_source_provenance_contract.py",
    "validate_version_catalog.py",
    "validate_version_guidance_contract.py",
    "validate_version_routes.py",
)


def validate_step_inventory() -> list[str]:
    errors: list[str] = []
    discovered = {
        path.name
        for path in SCRIPT_DIR.glob("validate_*.py")
        if path.name != SELF_NAME
    }
    configured = set(VALIDATION_STEPS)

    duplicates = sorted(
        step
        for index, step in enumerate(VALIDATION_STEPS)
        if step in VALIDATION_STEPS[:index]
    )
    missing = sorted(discovered - configured)
    unexpected = sorted(configured - discovered)

    if duplicates:
        errors.append(
            "Duplicate validation steps configured in validate_all.py: "
            + ", ".join(duplicates)
        )
    if missing:
        errors.append(
            "Validation scripts exist but are not included in VALIDATION_STEPS: "
            + ", ".join(missing)
        )
    if unexpected:
        errors.append(
            "VALIDATION_STEPS references missing validation scripts: "
            + ", ".join(unexpected)
        )

    return errors


def run_step(step: str) -> int:
    command = [sys.executable, str(SCRIPT_DIR / step)]
    print(f">>> {step}", flush=True)
    completed = subprocess.run(command, cwd=SCRIPT_DIR.parent.parent.parent)
    return completed.returncode


def main() -> int:
    inventory_errors = validate_step_inventory()
    if inventory_errors:
        print("Validation suite configuration failed:")
        for item in inventory_errors:
            print(f"- {item}")
        return 1

    failures: list[str] = []
    for step in VALIDATION_STEPS:
        code = run_step(step)
        if code != 0:
            failures.append(f"{step} (exit {code})")

    if failures:
        print("")
        print("Validation suite failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("")
    print("All GCAM skill validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
