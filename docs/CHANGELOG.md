# Changelog

## 2026-03-15
- Initialized GCAM Skill scaffold.
- Added project and development documentation.
- Added GCAM reference notes and tooling script.
- Drafted full GCAM skill SOP in `skills/gacm/SKILL.md`.
- Corrected version handling: root `gcam-doc` is now treated as the full `v8.2` doc tree.
- Added version catalog, generated per-version routing docs, and release-note-only routing for non-tree versions.
- Rebuilt the skill to remove machine-specific absolute paths and runtime dependence on sibling source repositories.
- Standardized wording so `v8.2` is explicitly the bundled current full-topic baseline derived from the root `gcam-doc` tree.
- Expanded the bundled reference layer with dedicated topic docs for assumptions, choice/marketplace, energy, land, water, economy, emissions/climate, developer workflows, and coverage mapping.
- Added page-level bundled version trees for all full-tree versions and delta-specific page bundles for release-only versions.
- Added `generate_bundled_pages.py` and page-bundle-aware search paths in `doc_search.py`.
- Reworked page-bundle generation so historical wiki links, `.html` links, cross-version TOC links, and old anchor patterns are normalized into portable bundled markdown links.
- Added automatic inherited page bundles for version-linked pages missing from a version's authoring snapshot, with explicit provenance notes instead of silent omission.
- Added automatic CMP trace pages so local CMP PDF references remain traceable without pretending the binary assets are bundled.
- Added `validate_bundled_pages.py` and brought bundled page markdown link validation to a clean pass.
- Rewrote the runtime skill and top-level reference docs to be CLI-first, text-only, and agent-oriented rather than GUI-first.
- Added explicit headless query guidance for ModelInterface batch mode, `gcamreader`, `rgcam`, and `gcamextractor`.

## 2026-03-16
- Added dedicated shared reference docs for configuration workflows, query automation, workspace layout recognition, and version-specific operational differences.
- Wired those docs into `SKILL.md`, navigation, coverage mapping, and bundled topic listings for better progressive disclosure.
- Fixed `doc_search.py` so historical-page searches no longer fail on the current Windows console encoding.
- Added `validate_shared_references.py` to verify shared-doc topic coverage, navigation references, and real local bundled references without misflagging `<version>` templates or upstream source-topic examples.
- Tightened shared operational docs so the agent-facing layer stays headless/CLI-first while historical UI wording remains confined to page-bundle evidence.
- Added `validate_version_routes.py` to verify that `version_catalog.py`, `version_inventory.md`, `versions/*.md`, `version_pages/<version>/`, and key `v8.2` baseline route docs do not drift apart.
- Added `validate_authoring_sources.py` and fail-fast preflight checks in `generate_bundled_pages.py` so missing `gcam-doc` inputs or catalog drift do not silently generate incomplete bundles.
- Removed an invalid `v8.2` entry from the delta-only CMP source map in the page-bundle generator.
- Strengthened `validate_version_routes.py` to compare route docs against `generate_version_references.py` output and regenerated all `reference/versions/*.md` files so they include the current shared topic set.
