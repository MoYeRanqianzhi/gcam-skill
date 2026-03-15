# Development Guide

## Workflow Requirements
- Use `skill-creator` skill guidance when modifying or extending the skill.
- Maintain traceability: use bundled references and cite them in outputs.
- Commit after each meaningful part; tag at key milestones.
- Keep the runtime skill portable and free of hardcoded local paths.

## Traceability Checklist
- Identify the target GCAM version before anything else.
- Identify the question domain (model structure, scenario config, policies, outputs, tools).
- Open the relevant bundled doc(s) before drafting conclusions.
- Provide bundled doc references in responses.
- Avoid speculation; if unsure, search locally first.

## Suggested Process for Updates
1. Review changes in upstream GCAM sources and ecosystem tools.
2. Update version metadata and regenerate `skills/gacm/reference/version_inventory.md` plus `skills/gacm/reference/versions/`.
3. Update bundled topic docs in `skills/gacm/reference/`, keeping `v8.2` root coverage explicit and traceable.
4. Update SOP steps in `skills/gacm/SKILL.md` as needed.
5. Update `docs/CHANGELOG.md`, `docs/KNOWN_ISSUES.md`, and any coverage or provenance notes.
6. Commit and tag.

## Testing Notes
- No automated tests included yet.
- Validate workflows by running `scripts/doc_search.py --list-versions`.
- Validate versioned lookups by running `scripts/doc_search.py --version <version> --pattern <term>`.
- Re-run generation after changing `version_catalog.py` so `version_inventory.md` and `versions/*.md` stay in sync with the topic set.
