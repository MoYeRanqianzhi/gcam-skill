# Development Guide

## Workflow Requirements
- Use `skill-creator` skill guidance when modifying or extending the skill.
- Maintain traceability: use bundled references and cite them in outputs.
- Commit after each meaningful part; tag at key milestones.
- Keep the runtime skill portable and free of hardcoded local paths.

## Maintainer Environment
- Bundled maintainer scripts under `skills/gacm/scripts/` target Python 3.10+.
- Runtime use of the published skill does not require the local authoring trees, but regeneration does.
- `gcamreader` and `gcamextractor` are upstream companion tools, not bundled runtime dependencies.

## Traceability Checklist
- Identify the target GCAM version before anything else.
- Identify the question domain before loading topic docs.
- Open the minimum bundled docs needed to answer the question.
- Prefer shared topic docs for agent workflows and exact page bundles for traceable evidence.
- Avoid speculation; if unsure, search locally first.

## Suggested Process for Updates
1. Review upstream changes across `gcam-doc`, `gcam-core`, and companion tools.
2. Update `skills/gacm/scripts/version_catalog.py` if version inventory or shared topic coverage changed.
3. Run `python skills/gacm/scripts/generate_version_references.py` after any shared-topic inventory or version-catalog change.
4. Run `python skills/gacm/scripts/validate_authoring_sources.py` before regenerating bundled pages.
5. Run `python skills/gacm/scripts/generate_bundled_pages.py`.
6. Run `python skills/gacm/scripts/validate_all.py`.
7. Update `docs/CHANGELOG.md`, `docs/PROJECT.md`, and `docs/KNOWN_ISSUES.md`.
8. Commit and tag.

## Runtime Versus Maintenance Boundary
- Validator and generation scripts are maintainer tools only. Do not surface them as required runtime steps for normal GCAM users.
- Shared topic docs are the authoritative agent layer; keep them phrased in terms of headless execution, XML/config editing, and batch extraction.
- Treat `reference/version_pages/**/*.md`, `reference/version_pages/README.md`, and `reference/version_pages/*/BUNDLE_INDEX.md` as generated artifacts. Fix the generator, then regenerate.
- Treat `version_inventory.md` and `reference/versions/*.md` as generated artifacts from `generate_version_references.py`.

## Validation Gates
- Use `python skills/gacm/scripts/validate_all.py` as the default one-shot validation suite before commit.
- Re-run `validate_portability.py` when editing runtime docs, scripts, or shared references.
- Re-run `validate_conceptual_docs_contract.py` after editing conceptual shared docs.
- Re-run `validate_operational_docs_contract.py` after editing operational shared docs such as run, config, query, tool, API, or release-workflow references.
- Re-run `validate_solver_contract.py` after editing `reference/solver.md`.
- Re-run `validate_navigation_contract.py` after editing `reference/navigation.md`.
- Re-run `validate_shared_references.py` after editing `SKILL.md`, shared root docs, or `docs/*.md`.
- Re-run `validate_page_bundle_contract.py` after changing `generate_bundled_pages.py` or the generated page-bundle layer.
- Re-run `validate_page_bundle_content_parity.py` after changing `generate_bundled_pages.py` or generated `reference/version_pages/**/*.md`.
- Re-run `validate_page_bundle_agent_adaptation.py` after changing page-bundle adaptation behavior.
- Re-run `validate_version_routes.py` and `validate_version_guidance_contract.py` after version-routing or family-guidance edits.

## Search and Progressive Disclosure Rules
- Start from `scripts/doc_search.py` for bundled lookups.
- Keep version-route docs and page-entry docs ahead of broad shared topics in search results.
- Stop loading files once the current route doc plus the minimum topic docs already answer the question.
- Use `--scope pages` only when page-level evidence is actually needed.

## Page Bundle Rules
- Treat the root `gcam-doc` tree as bundled `v8.2`.
- Keep the generated directory index name as `BUNDLE_INDEX.md`.
- Preserve the route order: `versions/<version>.md` -> `version_pages/<version>/BUNDLE_INDEX.md` -> exact page file.
- Preserve inherited page bundles and CMP trace pages instead of pretending missing upstream pages or PDFs are locally bundled in full.
- Keep bundled pages text-only, portable, and machine-agnostic.
- Do not validate in parallel with generation; finish `generate_bundled_pages.py` first, then run validators.

## Documentation Rules
- `CHANGELOG.md` is for milestones only, not edit-by-edit transcripts.
- `PROJECT.md` stores stable project identity, scope, and decisions.
- `KNOWN_ISSUES.md` stores live limitations and technical debt with clear status.
- If a decision matters to future contributors, document it here instead of relying on chat context.
