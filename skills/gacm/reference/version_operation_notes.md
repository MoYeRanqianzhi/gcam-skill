# Version Operation Notes

Operational differences across GCAM version families for agent workflows.

Open this file when the user asks:
- whether a command or path differs by version
- how much of a shared workflow can be reused across releases
- whether to treat a release as full-doc or delta-only

## First Rule
Route exact version first with `version_inventory.md`.

This file helps interpret the operational consequences of that route; it does not replace exact version routing.

## `v8.2`
- This is the bundled current baseline and corresponds to the root `gcam-doc` tree.
- Use it when the user says `root docs`, `current full docs`, or does not specify a version.
- Shared topic docs are primarily written to match this operational baseline.

## `v8.3` through `v8.7`
- These are `delta-only` routes in the skill.
- Do not pretend each one has a full standalone topic tree in the bundle.
- Combine the exact release delta with the `v8.2` baseline only as needed.

## `v8.0` and `v8.1`
- Also `delta-only`.
- Important bundled cues:
  - `v8.0`: base year moved to 2021
  - `v8.1`: Ukraine introduced as an independent region

## `v7.0` and `v7.1`
- Full modern-comprehensive families in the bundle.
- Build docs explicitly require C++17 from `v7.0` onward.
- Java/BaseX guidance is already in the modern form used by the shared docs.

## `v5.4` and `v6.0`
- Closest historical relatives to the bundled operational model after `v7.x`.
- Full topic trees are present in the bundle.
- Build docs explicitly reference C++14-era compiler requirements.
- BaseX and headless query workflows are already well documented.

## `v5.1` through `v5.3`
- Transitional modern family.
- Major workflow concepts match the later line, but documentation granularity is smaller.
- Reuse shared topic docs carefully and fall back to exact page bundles sooner.

## `v4.2` through `v4.4`
- Compact-modern family.
- BaseX is present, but Java guidance is older and the docs are more ModelInterface-centric.
- Batch command examples may still reference paths like `../Main_User_Workspace/output/queries/Main_queries.xml`.
- Treat those examples as evidence of older packaging assumptions, not as universal modern paths.

## `v3.2`
- Legacy-wiki family with the biggest operational gap from the `v8.2` baseline.
- The bundle includes inherited pages for some user-guide material because the historical tree omits later-structured copies.
- Legacy compile docs explicitly document direct invocation such as:
  - `./gcam.exe -C<alternative configuration file>`
- Legacy packaging references `Main_User_Workspace` and a separate `ModelInterface` directory.

Operational consequence:
- if the user provides a real `v3.2` workspace, inspect it before translating anything into modern path assumptions

## Cross-Version Build Cues
- `v5.4` and `v6.0`: C++14-era build guidance
- `v7.0+`: C++17-era build guidance
- `v4.3`: BaseX 7.9 and Java 1.6+ are explicitly documented
- `v5.4+`: BaseX 9.5.0 and Java 1.7+ are explicitly documented in the bundled build pages

## Cross-Version Query Cues
- Modern line: BaseX database in `output/database_basexdb`
- Modern line: query XML in `output/queries/Main_queries.xml`
- Early line: exact query and ModelInterface paths may use older nested workspace forms
- `delta-only` releases do not provide a separate full query manual inside the skill

## Decision Rule
If the user needs:
- exact file paths or exact commands for a real checkout:
  inspect that checkout
- conceptual or historical comparison:
  use this file plus the exact routed version docs
- modern default behavior:
  use `v8.2`
