# Changelog

High-signal milestone log for the `gacm` skill. Fine-grained edits belong in Git history and commit messages, not here.

## 2026-03-15
- Initialized GCAM Skill scaffold.
- Added project and development documentation.
- Drafted the first runtime SOP in `skills/gacm/SKILL.md`.
- Corrected version handling: root `gcam-doc` is now treated as the full `v8.2` doc tree.
- Rebuilt the skill to remove machine-specific absolute paths and runtime dependence on sibling source repositories.
- Standardized `v8.2` as the bundled current full-topic baseline derived from the root `gcam-doc` tree.
- Added page-level bundled version trees for all full-tree versions and delta-specific page bundles for release-only versions.
- Rewrote the runtime skill and top-level reference docs to be CLI-first, text-only, and agent-oriented rather than GUI-first.
- Added bundled topic docs for model structure, running, configuration, querying, tools, provenance, and version routing.

## 2026-03-16
- Added `validate_all.py` as a one-shot entry point for the bundled validation suite.
- Added `validate_conceptual_docs_contract.py` and wired it into `validate_all.py` to keep shared conceptual docs version-aware and baseline-aware.
- Added `validate_solver_contract.py` and wired it into `validate_all.py` to keep solver guidance log-first, CLI-first, and historically scoped.
- Added `validate_page_bundle_contract.py` and wired it into `validate_all.py` so page-bundle navigation cannot drift semantically even when generation still succeeds.
- Renamed generated page-bundle directory indexes from `INDEX.md` to `BUNDLE_INDEX.md` so Windows case-insensitive filesystems do not clobber bundled upstream source pages such as `index.md`.
- Hardened page-bundle generation and validation to strip GUI residue, web-shell markup, Office export debris, broken citation syntax, figure-number leftovers, invisible Unicode artifacts, and other non-agent-facing noise.
- Tightened portability and filesystem validation so runtime docs and bundled pages fail fast on machine-specific paths, file URIs, case-only collisions, and path hygiene regressions.
- Added contract validators for navigation, version guidance, coverage mapping, provenance, project memory, maintenance memory, shared references, and semantic contract coverage.
- Added dedicated operational docs for configuration workflows, query automation, workspace detection, version-specific operational differences, and release acquisition.
- Added dedicated API references for `gcamreader` and `gcamextractor`, including object-level usage, argument surfaces, caching rules, and failure patterns.
- Added `scripts/generate_modelinterface_batch.py` so agents can deterministically emit minimal headless ModelInterface batch-command XML instead of hand-typing boilerplate.
- Reworked progressive disclosure so `SKILL.md` now uses the standard 3-level model with explicit stop-loading guidance.
- Removed the parity validator's global monkeypatch dependency by letting `generate_bundled_pages.py` render into an explicit output root during validation.
