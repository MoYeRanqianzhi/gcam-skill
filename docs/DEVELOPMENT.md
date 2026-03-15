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
3. Regenerate page-level bundled version trees with `skills/gacm/scripts/generate_bundled_pages.py`.
4. Validate bundled page links and text-only adaptation rules with `skills/gacm/scripts/validate_bundled_pages.py`.
5. Update bundled topic docs in `skills/gacm/reference/`, keeping `v8.2` root coverage explicit, traceable, and CLI-first.
6. Update SOP steps in `skills/gacm/SKILL.md` as needed.
7. Update `docs/CHANGELOG.md`, `docs/KNOWN_ISSUES.md`, and any coverage or provenance notes.
8. Commit and tag.

High-value shared docs to maintain:
- `configuration_workflows.md`
- `query_automation.md`
- `workspace_layouts.md`
- `version_operation_notes.md`

## Testing Notes
- No automated tests included yet.
- Validate workflows by running `scripts/doc_search.py --list-versions`.
- Validate versioned lookups by running `scripts/doc_search.py --version <version> --pattern <term>`.
- Validate page-bundle lookups by running `scripts/doc_search.py --version <version> --scope pages --pattern <term>`.
- Re-run generation after changing `version_catalog.py` so `version_inventory.md` and `versions/*.md` stay in sync with the topic set.
- Re-run `generate_bundled_pages.py` after changing bundling rules so `reference/version_pages/` stays in sync with the authoring sources.
- Re-run `validate_bundled_pages.py` after regenerating so local markdown links stay fully resolvable and image markup stays stripped.
- Re-run representative `doc_search.py --version ... --scope pages --pattern ...` commands on Windows after search-tool changes to catch console encoding regressions.

## Page Bundle Rules
- Treat the root `gcam-doc` tree as bundled `v8.2`.
- Preserve progressive disclosure: route through `versions/<version>.md`, then `version_pages/<version>/INDEX.md`, then exact page files.
- When a version tree links to a page that is missing from that version's authoring snapshot, generate a clearly labeled `inherited page bundle` from the nearest traceable source rather than dropping the route.
- When a page links to a non-bundled local CMP PDF, generate a clearly labeled `cmp trace page` instead of pretending the binary asset is bundled.
- Historical site-root links such as `../toc.html` must route to bundled `v8.2/toc.md`, not to a non-existent synthetic root file.
- Bundled pages must stay text-only: strip raw image markup and avoid bundling binary figure assets.
- Shared topic docs should translate upstream GUI instructions into agent-usable CLI and configuration workflows whenever possible.
