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
2. Update version metadata and regenerate `skills/gacm/reference/version_inventory.md` plus `skills/gacm/reference/versions/` with `skills/gacm/scripts/generate_version_references.py`.
3. Validate authoring inputs with `skills/gacm/scripts/validate_authoring_sources.py` before regenerating bundled pages.
4. Regenerate page-level bundled version trees with `skills/gacm/scripts/generate_bundled_pages.py`.
5. Validate bundled page links and text-only adaptation rules with `skills/gacm/scripts/validate_bundled_pages.py`.
6. Validate shared topic-doc references, version routing references, and navigation coverage with `skills/gacm/scripts/validate_shared_references.py`.
7. Validate version routing completeness with `skills/gacm/scripts/validate_version_routes.py`.
8. Update bundled topic docs in `skills/gacm/reference/`, keeping `v8.2` root coverage explicit, traceable, and CLI-first.
9. Update SOP steps in `skills/gacm/SKILL.md` as needed.
10. Update `docs/CHANGELOG.md`, `docs/KNOWN_ISSUES.md`, and any coverage or provenance notes.
11. Commit and tag.

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
- Re-run `validate_authoring_sources.py` before `generate_bundled_pages.py` so missing `gcam-doc` inputs or version-map drift fail fast instead of silently producing incomplete bundles.
- Re-run `generate_bundled_pages.py` after changing bundling rules so `reference/version_pages/` stays in sync with the authoring sources.
- Re-run `validate_bundled_pages.py` after regenerating so local markdown links stay fully resolvable and image markup stays stripped.
- Re-run `validate_shared_references.py` after editing shared docs, routing docs, or `SKILL.md` so template placeholders, real local references, and topic listings stay consistent.
- Re-run `validate_version_routes.py` after changing `version_catalog.py`, regenerating `versions/*.md`, or modifying key route docs so version inventory, route docs, page directories, and `v8.2` baseline declarations stay aligned.
- Re-run representative `doc_search.py --version ... --scope pages --pattern ...` commands on Windows after search-tool changes to catch console encoding regressions.

## Page Bundle Rules
- Treat the root `gcam-doc` tree as bundled `v8.2`.
- Preserve progressive disclosure: route through `versions/<version>.md`, then `version_pages/<version>/INDEX.md`, then exact page files.
- When a version tree links to a page that is missing from that version's authoring snapshot, generate a clearly labeled `inherited page bundle` from the nearest traceable source rather than dropping the route.
- When a page links to a non-bundled local CMP PDF, generate a clearly labeled `cmp trace page` instead of pretending the binary asset is bundled.
- Historical site-root links such as `../toc.html` must route to bundled `v8.2/toc.md`, not to a non-existent synthetic root file.
- Bundled pages must stay text-only: strip raw image markup and avoid bundling binary figure assets.
- Shared topic docs should translate upstream GUI instructions into agent-usable CLI and configuration workflows whenever possible.
- Shared topic docs are the authoritative agent layer; keep them phrased in terms of headless execution, XML/config editing, and batch extraction, while leaving historical UI prose inside `reference/version_pages/` only as traceable evidence.
- Authoring-time generation scripts may depend on the bundled `gcam-doc/` authoring tree; runtime skill use must not depend on that tree being present.
