# GCAM Skill Project

## Project Intro
GCAM Skill provides a portable, self-contained workflow for working with the GCAM model and its ecosystem. The skill name is `gacm` and the main entrypoint is `skills/gacm/SKILL.md`.

## Scope
This skill is intended to help an agent:
1. Understand GCAM model structure, assumptions, and outputs.
2. Run or configure GCAM scenarios (reference, policy, batch, target finder).
3. Interpret results using ModelInterface, query files, and database outputs.
4. Use companion tools (`gcamreader`, `gcamextractor`) for Python/R post-processing.
5. Maintain traceability: every answer should cite the local source file(s) used.
6. Route correctly across historical families and the `v8.2` root-doc baseline without inventing missing source trees.

## Primary Sources (Local, Traceable)
The runtime skill uses only bundled references under `skills/gacm/reference/`.

The source material used to author the skill is documented in `skills/gacm/reference/source_provenance.md`.

## Usage Summary
1. Use the `gacm` skill when the user asks about GCAM concepts, scenarios, policies, outputs, or post-processing.
2. Route to the correct version before answering. Default to bundled `v8.2` only when the user does not specify a version.
3. For any factual claim, open the relevant bundled reference doc and cite it.
4. Use `scripts/doc_search.py --version <version>` to find authoritative bundled references quickly.
5. For `v8.2`, treat the root `gcam-doc` tree as the bundled current full-topic baseline.
6. For `delta-only` releases, answer using the exact release delta plus the minimum necessary bundled baseline topic docs.

## Open Tasks
- Keep the bundled version catalog aligned with upstream GCAM releases.
- Continue expanding bundled topic coverage where the skill still compresses very specialized upstream material.
- Add more deterministic helper scripts if repeated manual authoring or validation steps appear.

## Decision Log
- 2026-03-15: Rebuilt the skill to remove machine-specific absolute paths.
- 2026-03-15: Switched the runtime design to bundled references plus optional user-provided repository inspection.
- 2026-03-15: Explicitly standardized `v8.2 = root gcam-doc full documentation tree` across routing, navigation, and family docs.
- 2026-03-15: Expanded the reference layer into topic-specific bundled docs to improve progressive disclosure.
