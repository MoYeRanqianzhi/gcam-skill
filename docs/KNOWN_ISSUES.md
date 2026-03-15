# Known Issues

## Data and Tooling
- `gcamreader` and `gcamextractor` are not installed by default; users must install them in their Python/R environments to run examples.
- If a user wants repository-specific edits, they must provide an actual checkout or files; the bundled skill does not invent repository state.

## Runtime Constraints
- GCAM runs are resource intensive; typical memory and disk needs are high (see GCAM user guide for exact guidance).
- ModelInterface and XML database output require Java and BaseX; if Java is misconfigured, GCAM runs may fail to write the database.

## Coverage
- Some specialized topics (e.g., deep module internals, custom code changes) require a real GCAM repository checkout beyond the bundled conceptual docs.
- `delta-only` releases in the bundled skill summarize release deltas rather than restating a full standalone doc set.
- The skill is substantially more explicit for `v8.2` root coverage now, but it still synthesizes topic docs rather than mirroring every upstream page one-to-one.
- Page-level bundles now normalize local markdown links and materialize inherited or CMP trace pages where needed, but figures are still represented as text references rather than bundled binary image assets.
- Inherited page bundles are explicitly labeled, but they still reflect the nearest traceable source file rather than a guaranteed version-local restatement when the upstream version tree omitted that page.
