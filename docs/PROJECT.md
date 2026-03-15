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
- Continue auditing lower-frequency human-oriented residue in inherited historical page bundles so CLI-first adaptation remains comprehensive beyond the already-normalized `user-guide.md`, `gcam-build.md`, `hector.md`, `index.md`, and repeated data-system passages.
- Continue auditing historical developer-workflow pages beyond the newly adapted `dev-guide/test_framework.md`, `dev-guide/git.md`, `dev-guide/getting_started.md`, and `dev-guide/analysis.md` so internal-platform context is preserved without drifting back into browser-only instructions.
- Continue reducing the remaining lower-frequency historical figure residue, which is now mostly limited to figure-caption lines plus preserved equation/example lead-ins rather than raw omitted-image markers or repeated `shown in Figure N` prose.
- Preserve equation/example lead-ins such as `The equation is shown below` or `An example setup is shown below` when the equation or example still immediately follows in text, even if broad residue scans still report them.
- Continue auditing long-tail historical prose for editor-export or workflow-UI residue, but treat fenced XML comment lines in configuration examples as intentional documentation rather than as web-shell noise.

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
- 2026-03-16: Reordered `doc_search.py` to prioritize version-route and page-entry docs so progressive-disclosure search results stay agent-safe under `--max-matches`.
- 2026-03-16: Rewrote repeated bundled `user-guide.md` GUI walkthrough blocks into headless-agent notes and stripped obsolete v3.2 previous-version click-through boilerplate from page bundles.
- 2026-03-16: Extended page-bundle adaptation to also rewrite download-site chrome, desktop-launch/menu residue, `gcam-build.md` IDE click paths, and legacy `hector.md` integration choreography into CLI-first or configuration-oriented agent notes, with validator coverage expanded to reject those regressions.
- 2026-03-16: Normalized malformed citation markdown during page-bundle generation so wrapped citation labels and broken historical same-page citation anchors are repaired consistently across all bundled versions instead of surfacing raw upstream syntax defects.
- 2026-03-16: Reworked another broad pass of omitted-figure prose into text-first wording across `energy.md`, `details_energy.md`, `demand_energy.md`, `policies.md`, `details_land.md`, `ssp.md`, and related pages, and expanded validator coverage so those high-frequency figure-dependent phrases now fail fast if they reappear.
- 2026-03-16: Added a follow-up modern-version figure-adaptation pass across `aglu.md`, `overview.md`, `energy.md`, `details_land.md`, `gcam-usa.md`, `details_energy.md`, `land.md`, `economy.md`, `details_emissions.md`, and `inputs_supply.md`, including inherited `v8.2` pages.
- 2026-03-16: Reduced the remaining broad-scan figure residue mostly to preserved equation/example lead-ins and older `v3.2` figure-heavy pages, and documented that distinction so future maintainers do not over-normalize equations while continuing the text-only adaptation work.
- 2026-03-16: Added a first dedicated `v3.2` historical adaptation pass so major omitted-figure explanations in transportation, industry, socioeconomics/trade, resource supply curves, electricity, refining, and early AgLU overview pages are now carried forward as text summaries.
- 2026-03-16: Hardened bundled-page sanitization to strip raw/escaped web presentation residue such as style blocks, button wrappers, line-break tags, font wrappers, span wrappers, and presentation-only HTML `class=` attributes while keeping semantic anchors and links intact.
- 2026-03-16: Further normalized bundled page output so HTML navigation tables, raw href anchors, and presentational bold wrappers are rewritten into markdown text structures, especially for image-driven `index.md` landing pages.
- 2026-03-16: Rewrote repeated interactive `File -> Manage DB` and `File -> Export` wording into headless or source-tool-neutral guidance and tightened the bundled-page validator to reject those phrases if they reappear.
- 2026-03-16: Removed standalone Kramdown/Jekyll attribute-list residue such as `{: .tbl}` and `{:toc}` from generated page bundles and tightened validation so those presentation-only markers cannot silently re-enter any version, including the `v8.2` root baseline.
- 2026-03-16: Normalized residual inline HTML formatting tags such as `<cite>` and `<i>` into markdown emphasis across historical exact-page bundles, preserving text meaning while reducing agent-irrelevant HTML noise.
- 2026-03-16: Rewrote the historical `community-guide.md` placeholder `\<cite latest version of model documentation\>` into an explicit source-author note so exact bundles preserve provenance without surfacing raw editorial placeholders.
- 2026-03-16: Normalized raw HTML definition-list/list structures such as `<dl>/<dt>/<dd>/<ul>/<li>` into markdown in historical exact-page bundles, including inherited `aglu.md` pages that remain part of the `v8.2` route graph.
- 2026-03-16: Rewrote repeated human-UI phrasing in bundled historical pages where the source text still depended on GUI framing, including the `Regions` GUI-pane reference in ModelInterface batch-query setup and the `point and click` sentence in `dev-guide/git.md`.
- 2026-03-16: Preserved semantic same-page anchors by converting upstream `span id/name` wrappers into named anchors during bundle generation, fixing historical `gcam-usa.md` citation and figure-note fragments without leaving raw span markup in the published text layer.
- 2026-03-16: Expanded historical developer-workflow adaptation so `dev-guide/test_framework.md`, `dev-guide/git.md`, `dev-guide/getting_started.md`, and `dev-guide/analysis.md` now explain internal CI/review concepts in CLI/API and metadata terms rather than browser-button or GUI-first terms.
- 2026-03-16: Confirmed again in the durable reference layer that `v8.2` is the bundled current full baseline and maps to the root `gcam-doc` tree, with that rule explicitly present in `reference/version_families.md`.
- 2026-03-16: Removed the last raw `[omitted image: ...]` residue from generated page bundles, turning descriptive inline alt text into prose notes and dropping placeholder-only image lines where captions or surrounding text already carry the meaning.
- 2026-03-16: Added another text-only adaptation pass for repeated `Figure N` prose in `trade.md`, `details_trade.md`, `aglu.md`, older `v4.x energy.md`, and `v3.2/Economic_land_sharing.md`, so those pages no longer depend on missing figures for their main explanatory sentences.
- 2026-03-16: Confirmed with a fresh residue scan that the remaining high-frequency `shown below` hits are primarily equation/example lead-ins and figure-caption text rather than dead figure-navigation prose.
- 2026-03-16: Added generator cleanup for escaped Office/Word export blocks and removed the historical `mso` / `WordDocument` paste artifact from `v3.2/GCAM_Revision_History.md`.
- 2026-03-16: Further rewrote historical button/click phrasing in `user-guide.md`, `GCAM_Revision_History.md`, and `dev-guide/test_framework.md` into action-oriented workflow language while keeping the underlying historical CI/process facts traceable.
- 2026-03-16: Added generator-side semantic normalization for code-fence-external HTML sub/sup and broken superscript references, turning chemical formulas, unit exponents, and malformed historical footnote residue into plain-text agent-readable forms across all bundled versions including the `v8.2` root baseline.
- 2026-03-16: Explicitly kept literal XML/entity syntax intact inside inline code and fenced code examples while tightening bundled-page validation to reject prose-side sub/sup and entity residue.
- 2026-03-16: Added global cleanup for literal Unicode `NBSP` and zero-width characters in bundled pages so invisible copy/paste whitespace no longer contaminates commands, XML examples, or prose in any version family.
