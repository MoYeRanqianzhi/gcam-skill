# Getting Started

Bundled adapted source page for GCAM `v6.0`.

- Source root: `gcam-doc/v5.3`
- Source path: `dev-guide/getting_started.md`
- Coverage mode: `inherited page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v6.0/BUNDLE_INDEX.md`
- Note: This adapted getting-started page rewrites final submission steps as host-agnostic review-request workflow instead of browser-only pull-request actions.
- Source provenance: inherited from `v5.3` because `v6.0` links to this page but its authoring tree does not contain a version-local copy
- Note: Referenced from `v6.0` as `dev-guide/getting_started.md`.

Load this page when the user needs version-specific detail from this exact page family.

---

## Getting Started

This guide provides information on how to develop GCAM, including the process for adding to the GCAM repository and requirements (e.g., naming convention for branches).

### Step-by-step guide

1. Clone the GCAM repository (internal developers should clone from stash.pnnl.gov, external developers should clone from github.com/jgcri/gcam-core)
2. Create a new branch (see the guide below for how to name your branch)
3. Make your changes
4. Commit your changes (see the advice below for commits)
5. Push your changes (see the advice below for how often to push)
6. When your development is complete, submit the host platform's review request for the branch. Agent adaptation: use the forge CLI or API when available instead of assuming a browser-only pull request action.

### Branch naming guide

Branches should be named as follows \[your initials\]/\[type of branch\]/\[meaningful name\]

The possible options for \[type of branch\] include:

1. "feature" if you are adding a new major feature to GCAM
2. "bugfix" if you are making a minor change to GCAM
3. "paper" if you are documenting a paper – note these changes may or may not go into the core

### General Advice

* Smaller changes are easier to review. Consider breaking a very large development into several smaller incremental pull requests.
* Pushing your changes is a way of backing up your work. More frequent pushing is recommended.
