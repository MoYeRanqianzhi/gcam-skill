---
name: gacm
description: Portable GCAM expertise as a self-contained open-source skill. Use this skill whenever the user mentions GCAM, GCAM-USA, BaseX/XML DB, GCAM scenarios, policies, solver behavior, inputs, outputs, SSPs, build/compile tasks, version differences, ModelInterface, gcamreader, gcamextractor, rgcam, pygcam, or companion projects such as gcam-doc and gcam-core. Those names are trigger terms, not runtime dependencies. If the user names a GCAM version such as v3.2, v5.4, v7.1, or v8.2, route to that exact bundled version guide. If no version is named, default to the bundled current baseline v8.2.
---

# GCAM Skill (gacm)

## Mission
Provide accurate, traceable, verifiable, and explainable GCAM guidance without relying on machine-specific filesystem layouts or undisclosed external repositories.

## Agent Operating Rules
- Keep the skill portable. Do not hardcode absolute local paths.
- Default to pure text, command-line, and configuration-file workflows.
- Prefer editing XML/configuration files and running headless tools over GUI instructions.
- Treat ModelInterface as historical context or a headless batch-query engine, not as the default interactive path.
- Do not claim access to `gcam-doc`, `gcam-core`, `gcamreader`, or `gcamextractor` checkouts unless the user actually provides them.
- Use bundled references first. Treat any real checkout as optional external context.

## Version Routing
Version routing is always the first decision.

1. If the user explicitly names a version, use that version exactly.
2. If the user gives a versioned path, trust the path over any default.
3. If the user asks for a comparison, load only the specific versions being compared.
4. If the user does not name a version, default to the bundled current baseline `v8.2`.
5. Treat `delta-only` releases as release-specific deltas layered onto the broader bundled baseline. State that explicitly.

## Non-Negotiables
- Search bundled references first. Use `scripts/doc_search.py`.
- Cite the bundled reference files you relied on.
- Use the exact version route requested by the user.
- If a source is missing, ask for it rather than speculating.
- When page-level upstream material is GUI-oriented, translate it into the closest CLI/config workflow instead of repeating click paths.

## Progressive Disclosure
Keep context tight and load only what is needed.

### Level 1: Routing
Open `reference/version_inventory.md` first to identify the correct documentation tree or release-note route.

### Level 2: Version Entry
- For `v8.2` / `root` / `current`, open the relevant current-version summary in `reference/`.
- For any historical version or release-note-only version, open `reference/versions/<version>.md`.

### Level 3: Version Page Index
- For page-level version detail, open `reference/version_pages/<version>/INDEX.md`.
- For `delta-only` versions, start with `reference/version_pages/<version>/release_note.md`.

### Level 4: Exact Sources
Open only the specific bundled docs needed for the user's question.
- Use `scripts/doc_search.py --version <version> --pattern "term"` for targeted lookups.
- For exact version pages, use `scripts/doc_search.py --version <version> --scope pages --pattern "term"`.
- For `delta-only` versions, combine the release note and CMP trace page with the minimum necessary bundled topic docs.
- Use `reference/navigation.md` to choose the smallest topic set that answers the request.

## Default Response Structure
Keep answers traceable:
1. **Version**: state which GCAM version or release route you used.
2. **Answer**: concise response or steps, favoring CLI/config actions.
3. **Evidence**: list of bundled reference files you used.
4. **Next step**: any required user action or the next bundled doc to open.

## Task Triage
Always do version routing first:
- **All requests**: `reference/version_inventory.md`
- **Historical version or release-note-only version**: `reference/versions/<version>.md`

Then load the bundled topic docs from `reference/navigation.md`.

## Common Workflows

### Run a Reference Scenario
1. Ensure a valid configuration file exists in the GCAM executable workspace.
2. Start from `configuration_ref.xml` or pass it directly with `gcam.exe -C configuration_ref.xml` when the executable supports `-C`.
3. If using a release package wrapper, run `run-gcam`, `run-gcam.bat`, or `run-gcam.command` from the command line.
4. Monitor `exe/logs/main_log.txt`.
5. Treat the run as successful only when the log reaches `Starting output to XML Database.` and `Model run completed.`

### Add a Policy Scenario
1. Start from `configuration_policy.xml`.
2. Append policy XML files late in `ScenarioComponents`.
3. If targeting a climate outcome, configure target-finder mode and provide the target file.

### Batch Mode
1. Set `BatchMode=1` in the configuration.
2. Point the batch-file setting at a batch XML.
3. Keep scenario names explicit so database contents remain traceable.

### Query Results Without GUI
1. Prefer `gcamreader`, `rgcam`, or `gcamextractor` when those tools fit the task.
2. For exact GCAM query XML execution, use headless ModelInterface batch mode via `ModelInterface/InterfaceMain -b <batch.xml>`.
3. For post-run automatic extraction, configure `XMLDBDriver.properties` and the `batch-queries` option.
4. Use interactive ModelInterface steps only when the user explicitly asks about that historical workflow.

### Build GCAM
1. Prefer command-line builds.
2. On POSIX systems, use the GCAM Makefile flow in `cvs/objects/build/linux`.
3. On Windows, prefer CLI invocation of the project file over manually driving the Visual Studio UI.
4. Treat Xcode and Visual Studio screenshots in bundled page docs as legacy evidence, not as the default skill workflow.

## Local Reference Index
Start with `reference/version_inventory.md`.
