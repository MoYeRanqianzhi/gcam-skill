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
