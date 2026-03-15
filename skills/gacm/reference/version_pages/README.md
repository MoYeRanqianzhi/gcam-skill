# Version Page Bundles

This directory contains the page-level bundled reference trees for all GCAM versions represented by the `gacm` skill.

Rules:
- Open the exact version route file first.
- Then open `version_pages/<version>/BUNDLE_INDEX.md` only when page-level detail is needed.
- For full-tree versions, page files are adapted from the authoring markdown sources.
- For `delta-only` versions, page files capture the release delta and source trace rather than pretending a full standalone tree exists.
- When a version links to a page that is absent from its own authoring tree, the bundle may include a clearly labeled inherited or trace page instead of silently dropping the route.
