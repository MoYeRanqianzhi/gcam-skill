# GCAM Skill Project

## Project Intro
GCAM Skill provides a portable, self-contained workflow for working with the GCAM model and its ecosystem. The skill name is `gacm` and the main entrypoint is `skills/gacm/SKILL.md`.

## Scope
This skill is intended to help an agent:
1. Understand GCAM model structure, assumptions, and outputs.
2. Run or configure GCAM scenarios, including reference, policy, batch, and target-finder workflows.
3. Acquire runnable release workspaces or source checkouts without inventing missing files or paths.
4. Interpret results through headless query files, BaseX outputs, and command-line extraction workflows.
5. Use companion tools such as `gcamreader`, `rgcam`, and `gcamextractor` for Python and R post-processing.
6. Route correctly across historical families and the `v8.2` root-doc baseline without inventing missing source trees.
7. Open exact bundled version pages when the user needs page-level detail from a specific release.
8. Prefer pure text, CLI, and configuration editing over GUI walkthroughs.
9. Recognize workspace layout, configuration editing, and headless query workflows without relying on UI-oriented upstream prose.

## Primary Sources (Local, Traceable)
The runtime skill uses only bundled references under `skills/gacm/reference/`.

The source material used to author the skill is documented in `skills/gacm/reference/source_provenance.md`.

## Usage Summary
1. Use the `gacm` skill when the user asks about GCAM concepts, scenarios, policies, outputs, builds, release setup, or post-processing.
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
- Continue auditing long-tail historical prose and adaptation residue in generated page bundles.
- Decide whether to split `generate_bundled_pages.py` once the current validation surface stabilizes enough to make a low-risk refactor worthwhile.
- Validate expanded docs against upstream source for accuracy (especially new gcamextractor params list).
- Consider adding rgcam API reference if source code becomes available.
- Resolve Agents.md duplication with CLAUDE.md (delete or repurpose).

## Decision Log
- 2026-03-15: Rebuilt the skill to remove machine-specific absolute paths.
- 2026-03-15: Switched the runtime design to bundled references plus optional user-provided repository inspection.
- 2026-03-15: Explicitly standardized `v8.2 = root gcam-doc full documentation tree` across routing, navigation, and family docs.
- 2026-03-15: Added page-level bundled version trees under `reference/version_pages/` for full-tree versions and delta-specific page bundles for release-only versions.
- 2026-03-15: Reoriented the skill around agent-facing CLI, XML/configuration editing, and headless extraction instead of GUI-first workflows.
- 2026-03-16: Added dedicated operational docs for release acquisition, workspace classification, query automation, and companion-tool APIs.
- 2026-03-16: Renamed generated page-bundle directory indexes to `BUNDLE_INDEX.md` so Windows case-insensitive filesystems do not clobber bundled upstream source pages such as `index.md`.
- 2026-03-16: Preserved the rule that generated page bundles must be fixed through generator changes and regeneration, not hand-edited patching.
- 2026-03-16: Added explicit official `gcam-core` repository and releases URLs to the release workflow so direct download guidance no longer relies on placeholders.
- 2026-03-16: Added `reference/release_assets/direct_download_links.md` with exact user-supplied package URLs for known GCAM versions and platforms.
- 2026-03-17: Comprehensive doc expansion addressing all P0/P1 audit findings: expanded 9 topic docs, completed gcamextractor API (83+ params), added trade.md and scenario_analysis.md, fixed trigger surface with 13 missing domain terms, added script taxonomy, fixed .gitignore.
