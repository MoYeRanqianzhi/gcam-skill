# Source Provenance

This skill is a bundled synthesis, not a verbatim vendor drop.

## Upstream Materials Used During Skill Authoring
- GCAM documentation across historical versioned doc trees from `v3.2` through `v7.1`
- The root `gcam-doc` documentation tree corresponding to `v8.2`
- Release updates through `v8.7`
- GCAM core project overview material used during authoring
- `gcamreader` README and CLI usage used during authoring
- `gcamextractor` README and vignette usage used during authoring

## What This Means
- The skill is designed to be portable and open-source.
- It does not require those upstream repositories to exist beside the skill at runtime.
- It bundles summarized operational knowledge, routing logic, and version cues derived from those materials.
- It also bundles page-level adapted version trees under `reference/version_pages/` so the skill can progressively disclose exact version pages without external repo dependence.
- The page-level bundles are adapted into text-only form; images and screenshots are omitted rather than bundled as binary assets.
- Shared topic docs deliberately translate human-facing UI guidance into agent-facing CLI, config-editing, and headless extraction workflows.
- `coverage_map.md` documents how the bundled `v8.2` topic docs map back to the root source topics.

## What This Skill Does Not Pretend
- It does not claim to contain every line of every upstream documentation page.
- It does not claim access to the user's local GCAM checkout unless the user provides one.
- It does not silently substitute one version for another.

## When To Inspect a Real Checkout
Inspect a real repository or workspace only when:
- the user provides one
- the user asks for exact file edits, exact XML snippets from their project, or exact current repository state
- the bundled conceptual references are insufficient for the requested implementation task
