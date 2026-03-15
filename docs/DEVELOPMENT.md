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
- Use `python skills/gacm/scripts/validate_all.py` as the default one-shot validation suite before commit; run individual validators when narrowing down a failure.
- `validate_all.py` also self-checks its own `VALIDATION_STEPS` inventory against the actual `skills/gacm/scripts/validate_*.py` files, so new validators cannot be added without being wired into the main suite.
- Validate workflows by running `scripts/doc_search.py --list-versions`.
- Validate versioned lookups by running `scripts/doc_search.py --version <version> --pattern <term>`.
- Validate page-bundle lookups by running `scripts/doc_search.py --version <version> --scope pages --pattern <term>`.
- Re-run `validate_doc_search.py` when changing `doc_search.py` or version-routing behavior so CLI semantics, invalid-version handling, and root-path restrictions stay stable.
- Re-run `validate_page_bundle_content_parity.py` when changing `generate_bundled_pages.py` or bundled page content so the full `reference/version_pages/**/*.md` tree stays byte-for-byte aligned with generator output.
- Re-run generation after changing `version_catalog.py` so `version_inventory.md` and `versions/*.md` stay in sync with the topic set.
- Re-run `validate_authoring_sources.py` before `generate_bundled_pages.py` so missing `gcam-doc` inputs or version-map drift fail fast instead of silently producing incomplete bundles.
- Re-run `generate_bundled_pages.py` after changing bundling rules so `reference/version_pages/` stays in sync with the authoring sources.
- Re-run `validate_bundled_pages.py` after regenerating so local markdown links stay fully resolvable and image markup stays stripped.
- `validate_bundled_pages.py` also enforces portability inside `reference/version_pages/**/*.md`: real machine-specific absolute paths and file URIs must be sanitized out of bundled page content, while generic placeholders such as `/path/to`, `<GCAM Workspace>`, `<JAVA_HOME>`, and `<USER_HOME>` remain allowed.
- Treat `reference/version_pages/README.md` and `reference/version_pages/*/INDEX.md` as generated artifacts from `generate_bundled_pages.py`; do not hand-edit them unless you also intend to update the generator.
- Treat `reference/version_pages/**/*.md` as generated artifacts from `generate_bundled_pages.py`; if a page bundle must change, prefer changing the generator or authoring source and then regenerating.
- Re-run `validate_coverage_map_contract.py` after editing `reference/coverage_map.md` or expanding `gcam-doc` root coverage so the v8.2 root source pages remain fully accounted for and the source-to-bundled-doc traceability map does not silently drift.
- Re-run `validate_shared_references.py` after editing shared docs, routing docs, or `SKILL.md` so template placeholders, real local references, and topic listings stay consistent.
- `validate_shared_references.py` also enforces root shared-doc inventory parity: every `skills/gacm/reference/*.md` runtime doc must either be declared in `version_catalog.COMMON_TOPICS` or be the generated `version_inventory.md`.
- `validate_shared_references.py` also fails if `SKILL.md`, root shared docs, or `docs/*.md` embed markdown/HTML image markup; the agent-facing layer must stay pure text.
- `validate_shared_references.py` also covers `docs/*.md`; treat broken local references in project-memory docs as regressions, not just shared runtime-doc drift.
- Re-run `validate_navigation_contract.py` after editing `reference/navigation.md` so the main routing map cannot silently drift away from version-first routing, CLI/headless default behavior, progressive-disclosure sequencing, and the self-contained runtime rule.
- Re-run `validate_skill_contract.py` after editing `skills/gacm/SKILL.md` so the canonical `gacm` name, `v8.2` default-baseline wording, version-routing instructions, and progressive-disclosure contract do not drift.
- Re-run `validate_source_provenance_contract.py` after editing `reference/source_provenance.md` so the skill cannot silently drift away from its open-source portability claims, runtime-vs-authoring boundary, `v8.2` root-baseline provenance statement, and non-pretend rules about external checkouts.
- Re-run `validate_version_catalog.py` after editing `version_catalog.py` so version ordering, alias uniqueness, baseline semantics, family/coverage alignment, and shared-topic inventory invariants do not silently drift while generated docs still appear superficially consistent.
- Re-run `validate_version_routes.py` after changing `version_catalog.py`, regenerating `versions/*.md`, or modifying key route docs so version inventory, route docs, page directories, and `v8.2` baseline declarations stay aligned.
- Treat `version_inventory.md` and `reference/versions/*.md` as generated artifacts from `generate_version_references.py`; do not hand-edit them unless you also intend to update the generator.
- Re-run representative `doc_search.py --version ... --scope pages --pattern ...` commands on Windows after search-tool changes to catch console encoding regressions.
- `doc_search.py` should fail cleanly for unknown versions and should keep `--root` constrained to `skills/gacm/reference/`; treat silent version fallback or root-path escape as regressions.

## Page Bundle Rules
- Treat the root `gcam-doc` tree as bundled `v8.2`.
- Preserve progressive disclosure: route through `versions/<version>.md`, then `version_pages/<version>/INDEX.md`, then exact page files.
- When a version tree links to a page that is missing from that version's authoring snapshot, generate a clearly labeled `inherited page bundle` from the nearest traceable source rather than dropping the route.
- When a page links to a non-bundled local CMP PDF, generate a clearly labeled `cmp trace page` instead of pretending the binary asset is bundled.
- Historical site-root links such as `../toc.html` must route to bundled `v8.2/toc.md`, not to a non-existent synthetic root file.
- Bundled pages must stay text-only: strip raw image markup and avoid bundling binary figure assets.
- Bundled pages must also stay machine-agnostic: sanitize concrete user-home and installed-tool absolute paths into generic placeholders during generation instead of preserving upstream machine-local examples verbatim.
- Shared topic docs should translate upstream GUI instructions into agent-usable CLI and configuration workflows whenever possible.
- Shared topic docs are the authoritative agent layer; keep them phrased in terms of headless execution, XML/config editing, and batch extraction, while leaving historical UI prose inside `reference/version_pages/` only as traceable evidence.
- If you add a new root shared runtime doc under `skills/gacm/reference/`, also add it to `version_catalog.COMMON_TOPICS` and regenerate the version references, or the inventory-parity validator will fail.
- Authoring-time generation scripts may depend on the bundled `gcam-doc/` authoring tree; runtime skill use must not depend on that tree being present.
- Runtime docs and scripts must stay portable: never hardcode local machine paths such as `E:\...`, `C:\...`, `/Users/...`, `/home/...`, `file://`, or `vscode://`.
- Re-run `validate_portability.py` when editing runtime docs, scripts, or shared references so machine-specific absolute paths and file-URI references do not re-enter the open-source skill.
