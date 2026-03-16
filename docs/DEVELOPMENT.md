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
- Re-run `validate_filesystem_hygiene.py` when adding files, renaming bundled pages, or importing upstream trees so Windows device names, invalid filename characters, case-insensitive collisions, and portability-risk path lengths fail fast before release.
- `validate_filesystem_hygiene.py` also compares `git ls-files` path casing against real filesystem casing, because Windows `core.ignorecase=true` can hide case-only renames that would break on case-sensitive clones.
- Validate workflows by running `scripts/doc_search.py --list-versions`.
- Validate versioned lookups by running `scripts/doc_search.py --version <version> --pattern <term>`.
- Validate page-bundle lookups by running `scripts/doc_search.py --version <version> --scope pages --pattern <term>`.
- `doc_search.py` should keep progressive-disclosure priority in its output order: version route docs first, then page-entry docs such as `BUNDLE_INDEX.md` or `release_note.md`, then broader shared topics, then deep bundled pages.
- Re-run `validate_doc_search.py` when changing `doc_search.py` or version-routing behavior so CLI semantics, invalid-version handling, and root-path restrictions stay stable.
- Re-run `validate_page_bundle_content_parity.py` when changing `generate_bundled_pages.py` or bundled page content so the full `reference/version_pages/**/*.md` tree stays byte-for-byte aligned with generator output.
- Re-run `validate_page_bundle_contract.py` after changing `generate_bundled_pages.py` or the generated page-bundle layer so `reference/version_pages/README.md`, per-version `BUNDLE_INDEX.md`, and delta `release_note.md` / `cmp_index.md` files cannot silently drift away from progressive-disclosure and non-pretend rules.
- Re-run `validate_page_bundle_agent_adaptation.py` after regenerating bundled pages so repeated interactive ModelInterface walkthroughs in `user-guide.md` stay rewritten into headless-agent guidance and old wiki `Click here` navigation residue does not re-enter the published skill.
- Treat `validate_page_bundle_agent_adaptation.py` as the guardrail for bundled page CLI-first adaptation, not just `user-guide.md`: it now also rejects website download-chrome phrasing, desktop-launch wording, Xcode/Visual Studio click paths in `gcam-build.md`, and legacy IDE-integration choreography in old `hector.md` pages.
- `validate_page_bundle_agent_adaptation.py` also rejects repeated human-UI phrasing that is still easy to rewrite into headless wording, currently including `section of the GUI` in `user-guide.md` batch-query setup text and `point and click` phrasing in `dev-guide/git.md`.
- `validate_page_bundle_agent_adaptation.py` also guards the adapted historical developer workflow pages (`dev-guide/test_framework.md`, `dev-guide/git.md`, `dev-guide/getting_started.md`, and `dev-guide/analysis.md`) so host-agnostic review-request wording, CI metadata explanations, and automation-oriented tool descriptions do not silently regress to browser-button or GUI-centric phrasing.
- `validate_page_bundle_agent_adaptation.py` also guards a growing set of repeated figure-dependent residue in text-only bundles, including `see Figure below`, `shown in the following figure`, fossil-trade/floorspace XML figure callouts, and omitted-schematic fertilizer references; when these regress, adapt the generator instead of hand-editing published pages.
- `validate_page_bundle_agent_adaptation.py` now also guards the newer land/economy/emissions adaptation layer, including repeated `Figure 1` land-nesting summaries, `details_emissions.md` comparison-figure summaries, `economy.md` macro-structure figure phrasing, and the `inputs_supply.md` FAO commodity-mapping figure callout.
- `validate_page_bundle_agent_adaptation.py` now also guards a first historical `v3.2` adaptation layer, including transportation/industry/refining/resource-curve wording that previously pointed at omitted figures without carrying the same information into text.
- `validate_page_bundle_agent_adaptation.py` now also rejects raw `Figure N:` caption lines, direct `Figure N` prose references, `Figure source:` labels, and `Fig. 2a`-style panel residue; the generator should rewrite these into text-only omitted-figure wording instead of preserving raw figure numbering.
- `validate_page_bundle_agent_adaptation.py` also rejects older historical figure residue that does not look like modern captions, including bold wiki headings such as `**Figure 1: ...**`, malformed inline tails such as `..., Figure 3.`, and phrasing like `depicted Figure 11`; fix these in `generate_bundled_pages.py`, not in generated pages.
- Treat the `data-system.md` `Beyond 2020 Browser` adaptation as version-specific legacy coverage, not a universal requirement. The generic page-header note applies to every bundled `data-system.md`, but the explicit browser-neutral export note is only expected in the versions whose upstream page actually described that GUI workflow (`v4.3` and `v4.4`).
- Re-run generation after changing `version_catalog.py` so `version_inventory.md` and `versions/*.md` stay in sync with the topic set.
- Re-run `validate_authoring_sources.py` before `generate_bundled_pages.py` so missing `gcam-doc` inputs or version-map drift fail fast instead of silently producing incomplete bundles.
- Re-run `generate_bundled_pages.py` after changing bundling rules so `reference/version_pages/` stays in sync with the authoring sources.
- Run `generate_bundled_pages.py` to completion before `validate_bundled_pages.py` or `validate_all.py`; the page bundle tree is regenerated in place, so validating in parallel with generation can produce false negatives from transient missing files.
- Re-run `validate_bundled_pages.py` after regenerating so local markdown links stay fully resolvable and image markup stays stripped.
- `validate_bundled_pages.py` also enforces portability inside `reference/version_pages/**/*.md`: real machine-specific absolute paths and file URIs must be sanitized out of bundled page content, while generic placeholders such as `/path/to`, `<GCAM Workspace>`, `<JAVA_HOME>`, and `<USER_HOME>` remain allowed.
- `validate_bundled_pages.py` also enforces case-insensitive filesystem safety inside `reference/version_pages/`: no lowercased path collisions and no legacy generated `INDEX.md` directory indexes may remain.
- `validate_bundled_pages.py` now also rejects raw bundled web-shell residue such as `<button>`, `onclick=`, `<font>`, `<br>`, `<style>...</style>`, raw HTML `class=` attributes, raw HTML href anchors, raw HTML table markup, raw HTML list/definition-list markup such as `<dl>/<dt>/<dd>/<ul>/<li>`, standalone markdown attribute-list residue such as `{: .tbl}` / `{:toc}`, raw inline HTML formatting tags such as `<cite>` / `<i>` / `<em>`, and the known residual GUI/menu-path phrases (`File -> Manage DB`, `File -> Export`, `Click on each box for a more detailed description`). When these regressions appear, fix `generate_bundled_pages.py` and regenerate instead of hand-editing generated pages.
- `validate_bundled_pages.py` also rejects markdown code fences that remain attached to surrounding prose on the same line, for example `For example:```cpp` or `shown below:````. Use generator fixes, not hand edits, when this formatting residue appears.
- `validate_bundled_pages.py` also rejects the historical `/Applications/Xcode.app/Contents/Developer/usr/bin/make` path if it reappears in bundled pages; rewrite it to a portable `make` invocation during generation instead of preserving machine-local tool-install paths from upstream examples.
- `validate_bundled_pages.py` also rejects malformed citation markdown that the generator is expected to normalize, including wrapped citation labels such as `[(Author 2020)](...)` and broken same-page anchor labels such as `[Author (2020](#anchor))`.
- `validate_bundled_pages.py` also rejects raw or escaped `<sub>/<sup>` residue, broken double-bracket reference links such as `[[1]](#ref1)` / `[[1](#ref1)]`, and prose-side HTML entity residue such as `&amp;` outside inline code.
- `validate_bundled_pages.py` also rejects literal Unicode non-breaking spaces and zero-width characters anywhere in bundled pages, including code examples, because these copy/paste artifacts break command-line and config editing workflows even when the text looks visually correct.
- `validate_bundled_pages.py` also rejects typographic Unicode punctuation residue that is presentation-only rather than semantic: smart quotes/apostrophes, Unicode dash variants, thin spaces, invisible function-application separators, the ring-above temperature mark `˚`, and the multiplication sign `×`.
- Historical developer pages may use raw backticked language-scope markers such as `` `(C++)` `` or `` `(Java)` ``. Normalize those into explicit prose labels like `C++:` / `Java:` during generation instead of preserving the raw marker syntax in published bundles.
- Do not add a broad global inline-code spacing normalizer across bundled prose. If inline-code boundary glue reappears, fix the exact upstream pattern narrowly; generic spacing rewrites are now a documented regression source because they can alter literal CLI snippets, config identifiers, and validator-required adaptation sentences.
- Some upstream source lines are malformed before bundling, not just UI-oriented. When adapting them, prefer regexes that tolerate the source defect and normalize the published output, rather than assuming the authoring text is already syntactically clean.
- Re-run `validate_conceptual_docs_contract.py` after editing conceptual shared docs such as `overview.md`, `common_assumptions.md`, `choice_marketplace.md`, `energy_system.md`, `land_system.md`, `water_system.md`, `economy.md`, `emissions_climate.md`, `policies_scenarios.md`, `inputs_outputs.md`, `developer_workflows.md`, `data_system.md`, `ssp.md`, or `gcam_usa.md` so they cannot silently drift away from version-routing-aware bundled-baseline guidance.
- Re-run `validate_maintenance_memory_contract.py` after editing `docs/DEVELOPMENT.md` or `docs/CHANGELOG.md` so the shared maintainer workflow and hardening history do not silently drift out of long-term memory.
- Re-run `validate_semantic_contract_coverage.py` after adding or removing any root shared doc, persistent memory doc, or dedicated validator so every top-level skill doc remains owned by an explicit behavior-level contract.
- Re-run `validate_solver_contract.py` after editing `reference/solver.md` so solver guidance cannot silently drift away from version-routing-aware, CLI/config/log-first behavior or lose its modern-vs-historical solver caveats.
- Treat `reference/version_pages/README.md` and `reference/version_pages/*/BUNDLE_INDEX.md` as generated artifacts from `generate_bundled_pages.py`; do not hand-edit them unless you also intend to update the generator.
- Treat `reference/version_pages/**/*.md` as generated artifacts from `generate_bundled_pages.py`; if a page bundle must change, prefer changing the generator or authoring source and then regenerating.
- `validate_page_bundle_contract.py` is the semantic guardrail for generated page-bundle navigation and delta trace docs; parity alone is not enough if generator behavior drifts in the wrong direction.
- Keep the generated directory index name as `BUNDLE_INDEX.md`; on Windows, `INDEX.md` would collide with bundled upstream source pages named `index.md`.
- Keep authoring trees free of case-insensitive relative-path collisions; the generator now treats those as portability failures before regeneration.
- Re-run `validate_coverage_map_contract.py` after editing `reference/coverage_map.md` or expanding `gcam-doc` root coverage so the v8.2 root source pages remain fully accounted for and the source-to-bundled-doc traceability map does not silently drift.
- Re-run `validate_operational_docs_contract.py` after editing high-impact shared operational docs such as `running_gcam.md`, `configuration_workflows.md`, `query_automation.md`, `workspace_layouts.md`, `version_operation_notes.md`, `building_gcam.md`, or `tools.md` so the agent-facing layer cannot silently drift away from CLI/headless/config-first guidance.
- Re-run `validate_project_memory_contract.py` after editing `docs/PROJECT.md` or `docs/KNOWN_ISSUES.md` so the shared long-term memory docs cannot silently drift away from the canonical `gacm` identity, `v8.2` root-baseline framing, runtime honesty boundaries, and current coverage caveats.
- Re-run `validate_shared_references.py` after editing shared docs, routing docs, or `SKILL.md` so template placeholders, real local references, and topic listings stay consistent.
- `validate_shared_references.py` also enforces root shared-doc inventory parity: every `skills/gacm/reference/*.md` runtime doc must either be declared in `version_catalog.COMMON_TOPICS` or be the generated `version_inventory.md`.
- `validate_shared_references.py` also fails if `SKILL.md`, root shared docs, or `docs/*.md` embed markdown/HTML image markup; the agent-facing layer must stay pure text.
- `validate_shared_references.py` also covers `docs/*.md`; treat broken local references in project-memory docs as regressions, not just shared runtime-doc drift.
- `validate_semantic_contract_coverage.py` is the meta-guardrail for the top-level doc layer: inventory/link checks are not enough, and every root doc should belong to a dedicated semantic contract owner.
- Re-run `validate_navigation_contract.py` after editing `reference/navigation.md` so the main routing map cannot silently drift away from version-first routing, CLI/headless default behavior, progressive-disclosure sequencing, and the self-contained runtime rule.
- Re-run `validate_skill_contract.py` after editing `skills/gacm/SKILL.md` so the canonical `gacm` name, `v8.2` default-baseline wording, version-routing instructions, and progressive-disclosure contract do not drift.
- Re-run `validate_source_provenance_contract.py` after editing `reference/source_provenance.md` so the skill cannot silently drift away from its open-source portability claims, runtime-vs-authoring boundary, `v8.2` root-baseline provenance statement, and non-pretend rules about external checkouts.
- Re-run `validate_version_catalog.py` after editing `version_catalog.py` so version ordering, alias uniqueness, baseline semantics, family/coverage alignment, and shared-topic inventory invariants do not silently drift while generated docs still appear superficially consistent.
- Re-run `validate_version_guidance_contract.py` after editing `reference/version_families.md` or `reference/updates.md` so family semantics, `delta-only` framing, and the `v8.2 = root gcam-doc full-doc baseline` rule cannot silently drift.
- Re-run `validate_version_routes.py` after changing `version_catalog.py`, regenerating `versions/*.md`, or modifying key route docs so version inventory, route docs, page directories, and `v8.2` baseline declarations stay aligned.
- Treat `version_inventory.md` and `reference/versions/*.md` as generated artifacts from `generate_version_references.py`; do not hand-edit them unless you also intend to update the generator.
- Re-run representative `doc_search.py --version ... --scope pages --pattern ...` commands on Windows after search-tool changes to catch console encoding regressions.
- `doc_search.py` should fail cleanly for unknown versions and should keep `--root` constrained to `skills/gacm/reference/`; treat silent version fallback or root-path escape as regressions.

## Page Bundle Rules
- Treat the root `gcam-doc` tree as bundled `v8.2`.
- Preserve progressive disclosure: route through `versions/<version>.md`, then `version_pages/<version>/BUNDLE_INDEX.md`, then exact page files.
- When a version tree links to a page that is missing from that version's authoring snapshot, generate a clearly labeled `inherited page bundle` from the nearest traceable source rather than dropping the route.
- When a page links to a non-bundled local CMP PDF, generate a clearly labeled `cmp trace page` instead of pretending the binary asset is bundled.
- Historical site-root links such as `../toc.html` must route to bundled `v8.2/toc.md`, not to a non-existent synthetic root file.
- Bundled pages must stay text-only: strip raw image markup and avoid bundling binary figure assets.
- Bundled pages should strip both raw HTML presentation residue and escaped legacy web markup when it is clearly web-shell noise rather than model content.
- Bundled pages should normalize malformed citation markdown instead of preserving broken upstream syntax literally when the intended same-page anchor or external citation target is still unambiguous.
- Bundled pages should also normalize semantic HTML that only carries typographic meaning in prose: convert subscript chemistry notation such as `CO<sub>2</sub>` to plain text, convert non-footnote superscripts such as `m<sup>3</sup>` to caret notation like `m^3`, and convert superscript footnotes into normal inline markdown links.
- Do not apply that semantic normalization inside fenced code blocks or inline code spans; literal XML and escaped entity syntax there may be the exact text an agent must preserve when editing configs.
- Bundled pages should normalize actual Unicode whitespace artifacts globally, especially `NBSP` and zero-width characters copied from HTML/wiki exports. Unlike semantic HTML cleanup, this whitespace cleanup should apply even inside code examples because invisible spacing characters make pasted commands and XML invalid or misleading.
- Bundled pages should also normalize presentation-only Unicode punctuation globally when it improves command-line and search reliability: use ASCII quotes/apostrophes for prose and examples, normalize dash variants to ASCII hyphen usage, replace `×` with `x`, and strip invisible math-layout helpers such as `exp⁡(...)`. Keep semantically meaningful non-ASCII such as Greek equation symbols, author-name diacritics, and the standard degree symbol `°` unless there is a stronger reason to transliterate them.
- When upstream HTML uses empty `span id/name` wrappers as local citation or note anchors, preserve them semantically by converting them into named anchors during generation; do not drop the target and do not leave raw span markup in the published bundle.
- Bundled pages must also stay machine-agnostic: sanitize concrete user-home and installed-tool absolute paths into generic placeholders during generation instead of preserving upstream machine-local examples verbatim.
- Bundled pages must also preserve markdown structure that an agent can copy reliably. In particular, fenced code blocks should start on their own lines after all sanitization/adaptation passes; do not leave opening fences glued to preceding prose.
- Shared topic docs should translate upstream GUI instructions into agent-usable CLI and configuration workflows whenever possible.
- Shared topic docs are the authoritative agent layer; keep them phrased in terms of headless execution, XML/config editing, and batch extraction, while leaving historical UI prose inside `reference/version_pages/` only as traceable evidence.
- Generated page bundles should still be agent-usable evidence, not raw human-web prose dumps: rewrite repeated site chrome, desktop-launch wording, menu/button click paths, and IDE pane choreography into concise CLI/configuration notes whenever the upstream instruction is templatic and repeated across versions.
- Generated page bundles should also rewrite repeated omitted-figure navigation phrases into text-first summaries when the figure asset itself is intentionally omitted; preserve equation lead-ins when the equation still follows directly in text.
- After the latest modern-version adaptation pass, a broad figure-residue scan should mostly return either preserved equation/example lead-ins or older `v3.2` figure-heavy prose; treat new modern-version hits as regressions unless there is a strong reason to preserve them verbatim.
- After the current `v3.2` historical pass, a broad figure-residue scan should now be dominated by preserved equation/example lead-ins such as `The equation is shown below`, `shown below:` before math/code blocks, or explicit example-introduction lines. Treat any new non-equation figure-navigation prose in modern versions or in already-adapted `v3.2` pages as a regression.
- Generated page bundles should not retain raw `[omitted image: ...]` text. If omitted-image residue reappears, fix the generator so descriptive alt text becomes a short prose note and placeholder-only image lines disappear from the published bundle.
- Current broad residue scans should no longer return raw `Figure N:` caption lines or direct `Figure N` prose references. The remaining intentional residue should be text-only `Omitted figure summary:` notes plus legitimate equation/example lead-ins where the referenced math, XML, or example block still immediately follows.
- Current broad residue scans should also stay clean for old bold/heading caption forms and malformed inline `, Figure N.` sentence tails. If those return, treat them as generator regressions, not as acceptable historical residue.
- Generated page bundles should not retain raw Office/Word export scaffolding such as `mso` conditional comments, `WordDocument` XML, or `StartFragment` residue. If those reappear, strip them in the generator rather than treating them as historical content.
- Raw `<!-- ... -->` XML comments inside fenced config snippets are acceptable when they are part of the upstream example syntax; raw HTML/XML comment markers in normal prose are not.
- Generated page bundles should also normalize structural HTML presentation when it carries routing or tabular meaning but no agent-only value in raw form; prefer markdown links and markdown tables over preserved `<a href>` / `<table>` shells in the published bundle.
- When adding or editing adaptation replacement text after `rewrite_markdown_links(...)` has already run, write bundled-local links directly as `.md` targets; do not reintroduce hand-authored `.html` links inside replacement strings.
- Generated page bundles should rewrite historical backticked language-scope tags such as `` `(C++)` `` / `` `(Java)` `` into plain prose labels. Agents should read those pages as text-first guidance, not as malformed inline-markup puzzles.
- Generated page bundles should not apply blanket inline-code spacing cleanup. Preserve literal inline code exactly unless a narrowly-scoped transform is needed for a specific upstream defect and has been validated against required snippet checks.
- Generated page bundles should also eliminate residual figure references that survive after a main caption rewrite, including tails such as `in Figure 1`, mixed table/figure lead-ins like `(**Table 1** and **Figure 1**)`, and figure-introduction verbs other than `shown`, such as `presented in the following figure`.
- If you add a new root shared runtime doc under `skills/gacm/reference/`, also add it to `version_catalog.COMMON_TOPICS` and regenerate the version references, or the inventory-parity validator will fail.
- Authoring-time generation scripts may depend on the bundled `gcam-doc/` authoring tree; runtime skill use must not depend on that tree being present.
- Runtime docs and scripts must stay portable: never hardcode local machine paths such as `E:\...`, `C:\...`, `/Users/...`, `/home/...`, `file://`, or `vscode://`.
- Re-run `validate_portability.py` when editing runtime docs, scripts, or shared references so machine-specific absolute paths and file-URI references do not re-enter the open-source skill.
- Keep repo paths cross-platform safe: avoid Windows reserved filenames, case-only path distinctions, trailing dots/spaces, and path inflation that would make downstream checkouts fragile.
- When correcting a case-only path rename on Windows, use an explicit temporary rename so Git's index casing actually changes; otherwise the repository can silently keep the old tracked path even when the working tree looks correct.
