#!/usr/bin/env python3
"""
Validate bundled GCAM maintenance-memory contract invariants.

Checks:
- `docs/DEVELOPMENT.md` keeps the required maintainer workflow and validation rules
- `docs/CHANGELOG.md` preserves the major repository-hardening milestones
- shared maintenance memory remains explicit instead of depending on chat context
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEVELOPMENT_DOC = REPO_ROOT / "docs" / "DEVELOPMENT.md"
CHANGELOG_DOC = REPO_ROOT / "docs" / "CHANGELOG.md"

DEVELOPMENT_REQUIRED_SNIPPETS = (
    "Use `skill-creator` skill guidance when modifying or extending the skill.",
    "Commit after each meaningful part; tag at key milestones.",
    "Use `python skills/gacm/scripts/validate_all.py` as the default one-shot validation suite before commit",
    "Re-run `validate_conceptual_docs_contract.py` after editing conceptual shared docs",
    "Re-run `validate_solver_contract.py` after editing `reference/solver.md`",
    "Treat `version_inventory.md` and `reference/versions/*.md` as generated artifacts from `generate_version_references.py`",
    "Shared topic docs are the authoritative agent layer; keep them phrased in terms of headless execution, XML/config editing, and batch extraction",
    "Re-run `validate_portability.py` when editing runtime docs, scripts, or shared references",
)

CHANGELOG_REQUIRED_SNIPPETS = (
    "Initialized GCAM Skill scaffold.",
    "Corrected version handling: root `gcam-doc` is now treated as the full `v8.2` doc tree.",
    "Rebuilt the skill to remove machine-specific absolute paths and runtime dependence on sibling source repositories.",
    "Added page-level bundled version trees for all full-tree versions and delta-specific page bundles for release-only versions.",
    "Rewrote the runtime skill and top-level reference docs to be CLI-first, text-only, and agent-oriented rather than GUI-first.",
    "Added `validate_all.py` as a one-shot entry point for the bundled validation suite.",
    "Added `validate_conceptual_docs_contract.py` and wired it into `validate_all.py`",
    "Added `validate_solver_contract.py` and wired it into `validate_all.py`",
)


def main() -> int:
    errors: list[str] = []

    development_text = DEVELOPMENT_DOC.read_text(encoding="utf-8")
    changelog_text = CHANGELOG_DOC.read_text(encoding="utf-8")

    for snippet in DEVELOPMENT_REQUIRED_SNIPPETS:
        if snippet not in development_text:
            errors.append(f"DEVELOPMENT.md drifted; missing required snippet: {snippet}")

    for snippet in CHANGELOG_REQUIRED_SNIPPETS:
        if snippet not in changelog_text:
            errors.append(f"CHANGELOG.md drifted; missing required snippet: {snippet}")

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Maintenance memory contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
