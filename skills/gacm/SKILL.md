---
name: gacm
description: Portable GCAM expertise as a self-contained open-source skill. Use this skill whenever the user mentions GCAM, GCAM-USA, ModelInterface, BaseX/XML DB, GCAM scenarios, policies, solver behavior, inputs, outputs, SSPs, build/compile tasks, version differences, or companion projects such as gcam-doc, gcam-core, gcamreader, or gcamextractor. Those project names are trigger terms, not runtime dependencies. If the user names a GCAM version such as v3.2, v5.4, v7.1, or v8.2, route to that exact bundled version guide. If no version is named, default to the bundled current baseline v8.2.
---

# GCAM Skill (gacm)

## Mission
Provide accurate, traceable, verifiable, and explainable guidance on GCAM without relying on machine-specific filesystem layouts or undisclosed external repositories.

## Hard Rule
This skill must remain portable.
- Do not hardcode machine-specific absolute paths.
- Do not assume an external checkout of `gcam-doc`, `gcam-core`, `gcamreader`, or `gcamextractor`.
- Do not claim access to a user repository unless the user actually provides it.
- Use the bundled references first. Treat any real checkout as optional external context.
- The companion project names in the description are trigger keywords only; they are never prerequisites for using this skill.

## Version Routing
Version routing is the first decision, before topic routing.

1. If the user explicitly names a version, use that version exactly.
2. If the user gives a versioned path, trust the path over any default.
3. If the user asks for a comparison, load only the specific versions being compared.
4. If the user does not name a version, default to the bundled current baseline `v8.2`.
5. Treat `delta-only` releases as release-specific deltas layered onto the broader bundled knowledge base. Be explicit about that mode.

## Non-Negotiables
- If unsure, **search bundled references first** (use `scripts/doc_search.py`).
- Cite the bundled skill references you relied on.
- Use the exact version route requested by the user.
- If a source is missing, ask for it rather than speculating.

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
- For exact version pages, search `scripts/doc_search.py --version <version> --scope pages --pattern "term"`.
- For `delta-only` versions, combine the release note and CMP trace page with the minimum necessary bundled topic docs.
- Use `reference/navigation.md` to choose the smallest topic set that answers the request.

## Default Response Structure
Use a short structure to keep answers traceable:
1. **Version**: state which GCAM version or release route you used.
2. **Answer**: concise response or steps.
3. **Evidence**: list of bundled reference files you used.
4. **Next step**: any required user action or additional bundled doc to open next.

## Task Triage
Always do version routing first:
- **All requests**: `reference/version_inventory.md`
- **Historical version or release-note-only version**: `reference/versions/<version>.md`

Then load the bundled topic docs from `reference/navigation.md`.

## Common Workflows (Use as Templates)

These workflows are conceptual templates. When the user provides a real GCAM checkout, inspect that checkout before giving repository-specific file advice.

### Run a Reference Scenario
1. Ensure a valid `configuration.xml` exists in the GCAM executable workspace.
2. Copy `configuration_ref.xml` to `configuration.xml`.
3. Run GCAM and monitor `exe/logs/main_log.txt`.
4. Open `output/database_basexdb` in ModelInterface to query results.

### Add a Policy Scenario
1. Start from `configuration_policy.xml`.
2. Append a policy XML to `ScenarioComponents`.
3. If targeting a climate outcome, configure target finder and policy target file.

### Batch Mode
1. Set `BatchMode=1` in config.
2. Provide a batch file with `FileSet` permutations.
3. Run GCAM; outputs will be per-scenario.

### Use gcamreader
1. Locate the BaseX database directory.
2. Provide query XML (e.g., `Main_queries.xml`).
3. Run gcamreader CLI to produce CSV outputs.

### Use gcamextractor
1. Install in R via `devtools`.
2. Call `readgcam` with database path and params.
3. Use aggregated outputs for plotting/analysis.

## Local Reference Index
Start with `reference/version_inventory.md`.
