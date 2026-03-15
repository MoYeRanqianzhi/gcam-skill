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

## Primary Sources (Local, Traceable)
The runtime skill uses only bundled references under `skills/gacm/reference/`.

The source material used to author the skill is documented in `skills/gacm/reference/source_provenance.md`.

## Usage Summary
1. Use the `gacm` skill when the user asks about GCAM concepts, scenarios, policies, outputs, or post-processing.
2. Route to the correct version before answering. Default to bundled `v8.2` only when the user does not specify a version.
3. For conceptual questions, use shared bundled topic docs.
4. For exact version-page detail, open `reference/version_pages/<version>/INDEX.md` and then the minimum necessary page files.
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
