# GCAM Skill Project

## Project Intro
GCAM Skill provides a portable, self-contained workflow for working with the GCAM model and its ecosystem. The skill name is `gacm` and the main entrypoint is `skills/gacm/SKILL.md`.

## Scope
This skill is intended to help an agent:
1. Understand GCAM model structure, assumptions, and outputs.
2. Run or configure GCAM scenarios (reference, policy, batch, target finder).
3. Interpret results through headless query files, BaseX outputs, and command-line extraction workflows.
4. Use companion tools (`gcamreader`, `rgcam`, `gcamextractor`, and related automation tooling) for Python/R post-processing.
5. Maintain traceability: every answer should cite the local source file(s) used.
6. Route correctly across historical families and the `v8.2` root-doc baseline without inventing missing source trees.
7. Open exact bundled version pages when the user needs page-level detail from a specific release.
8. Prefer pure text, CLI, and configuration editing over GUI walkthroughs.
9. Recognize workspace layout, configuration editing, and headless query workflows without relying on UI-oriented upstream prose.

## Primary Sources (Local, Traceable)
The runtime skill uses only bundled references under `skills/gacm/reference/`.

The source material used to author the skill is documented in `skills/gacm/reference/source_provenance.md`.

## Usage Summary
1. Use the `gacm` skill when the user asks about GCAM concepts, scenarios, policies, outputs, or post-processing.
2. Route to the correct version before answering. Default to bundled `v8.2` only when the user does not specify a version.
3. For conceptual questions, use shared bundled topic docs.
4. For exact version-page detail, open `reference/version_pages/<version>/BUNDLE_INDEX.md` and then the minimum necessary page files.
5. Use `scripts/doc_search.py --version <version>` or `--scope pages` to find authoritative bundled references quickly.
6. For `v8.2`, treat the root `gcam-doc` tree as the bundled current full-topic baseline.
7. For `delta-only` releases, answer using the exact release delta plus the minimum necessary bundled baseline topic docs.
8. When a historical version links to a page absent from its own authoring subtree, use the bundled inherited page if present and cite its provenance note.
9. When a page routes to a CMP PDF, use the bundled CMP trace page for provenance unless the user provides the original binary asset separately.

## Open Tasks
- Keep the bundled version catalog aligned with upstream GCAM releases.
- Continue expanding bundled topic coverage where the skill still compresses very specialized upstream material.
- Add more deterministic helper scripts if repeated manual authoring or validation steps appear.

## Decision Log
- 2026-03-15: Rebuilt the skill to remove machine-specific absolute paths.
- 2026-03-15: Switched the runtime design to bundled references plus optional user-provided repository inspection.
- 2026-03-15: Explicitly standardized `v8.2 = root gcam-doc full documentation tree` across routing, navigation, and family docs.
- 2026-03-15: Expanded the reference layer into topic-specific bundled docs to improve progressive disclosure.
- 2026-03-15: Added page-level bundled version trees under `reference/version_pages/` for full-tree versions and delta-specific page bundles for release-only versions.
- 2026-03-15: Added inherited page bundles and CMP trace pages so all known version-linked routes remain portable and locally traceable without hardcoded external paths.
- 2026-03-15: Reoriented the skill around agent-facing CLI, XML/configuration editing, and headless extraction instead of GUI-first workflows.
- 2026-03-16: Added dedicated references for configuration workflows, query automation, workspace layout recognition, and version-specific operational differences.
- 2026-03-16: Fixed bundled document search output so historical-version searches do not crash on the current Windows console encoding.
- 2026-03-16: Added a shared-reference validator so `SKILL.md`, shared topic docs, and version routing docs can be checked without false positives from `<version>` templates or upstream source-topic examples.
- 2026-03-16: Further tightened the shared reference layer so agent-facing guidance stays explicitly headless, CLI-first, and configuration-driven.
- 2026-03-16: Added a version-route validator so the version catalog, route docs, page directories, and `v8.2` root-baseline declarations can be checked together.
- 2026-03-16: Added authoring-source preflight validation so bundled page regeneration fails fast when the `gcam-doc` authoring tree or version maps drift.
- 2026-03-16: Strengthened version-route validation so generated version route docs cannot silently drift behind the current shared topic inventory.
- 2026-03-16: Added conceptual-doc and solver-doc contracts so shorter shared summaries remain version-aware, headless, and agent-usable.
- 2026-03-16: Added maintenance-memory and semantic-coverage validators so top-level docs cannot exist without an explicit behavior-level contract owner.
- 2026-03-16: Added a page-bundle contract validator so generated `version_pages` navigation and delta trace docs remain semantically correct even if the generator changes.
- 2026-03-16: Renamed generated page-bundle directory indexes to `BUNDLE_INDEX.md` so Windows case-insensitive filesystems do not clobber bundled upstream source pages such as `index.md`.
- 2026-03-16: Added Git-index casing validation after finding a Windows-hidden case-only rename residue in `reference/version_pages/v3.2/index.md`.
