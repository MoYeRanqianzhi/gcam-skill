# Known Issues

## Data and Tooling
- Status: open. `gcamreader` and `gcamextractor` are not installed by default; users must install them in their Python or R environments before running those examples.
- Status: open. If a user wants repository-specific edits, they must provide an actual checkout or files; the bundled skill does not invent repository state.
- Status: open. Authoring-time regeneration scripts depend on the bundled `gcam-doc/` source tree; this is a maintainer requirement, not a runtime dependency of the published skill.
- Status: deferred. Operational helper scripts are still limited; most runtime guidance remains doc-driven rather than template-generator-driven. `generate_modelinterface_batch.py` added for batch XML generation.

## Runtime Constraints
- Status: open. GCAM runs are resource intensive; large scenarios still require significant RAM, disk, and wall-clock time.
- Status: open. ModelInterface and XML database output require Java and BaseX; if Java is misconfigured, GCAM runs may fail to write the database.
- Status: open. Release packages and source checkouts are not interchangeable; users can still pick the wrong asset type and end up without a runnable workspace.

## Coverage
- Status: open. Some specialized topics still require a real GCAM repository checkout beyond the bundled conceptual docs, especially when the user wants exact source edits or project-local XML changes.
- Status: open. `delta-only` releases in the bundled skill summarize release deltas rather than restating a full standalone doc set.
- Status: open. The skill is substantially more explicit for `v8.2` root coverage now, but it still synthesizes topic docs rather than mirroring every upstream page one-to-one.
- Status: open. Inherited page bundles are explicitly labeled, but they still reflect the nearest traceable source file rather than a guaranteed version-local restatement when the upstream version tree omitted that page.
- Status: open. Some exact page bundles still preserve historical GUI prose for traceability; shared topic docs are the authoritative agent-first headless CLI/config guidance.
- Status: open. Some exact page bundles still contain text-only `Omitted figure summary:` notes and preserved equation or example lead-ins where the upstream source depended on omitted diagrams.

## Maintainer Debt
- Status: deferred. `skills/gacm/scripts/generate_bundled_pages.py` remains a large monolithic generator; the current priority is validation integrity rather than risky structural refactoring.
- Status: deferred. Some companion-tool upstream docs are internally inconsistent, so the skill must continue preferring source code over generated package docs when they disagree.
- Status: open. `Agents.md` duplicates `CLAUDE.md` at 97% overlap; should be deleted or given a distinct sub-agent-specific purpose.
- Status: open. Git tags are 1:1 with commits (60 tags for 60 commits); should introduce semver milestones and prune noise tags.
