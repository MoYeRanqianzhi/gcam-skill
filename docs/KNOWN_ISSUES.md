# Known Issues

## Data and Tooling
- `gcamreader` and `gcamextractor` are not installed by default; users must install them in their Python/R environments to run examples.
- If a user wants repository-specific edits, they must provide an actual checkout or files; the bundled skill does not invent repository state.
- Authoring-time regeneration scripts depend on the bundled `gcam-doc/` source tree; this is a maintainer requirement, not a runtime dependency of the published skill.

## Runtime Constraints
- GCAM runs are resource intensive; typical memory and disk needs are high (see GCAM user guide for exact guidance).
- ModelInterface and XML database output require Java and BaseX; if Java is misconfigured, GCAM runs may fail to write the database.

## Coverage
- Some specialized topics (e.g., deep module internals, custom code changes) require a real GCAM repository checkout beyond the bundled conceptual docs.
- `delta-only` releases in the bundled skill summarize release deltas rather than restating a full standalone doc set.
- The skill is substantially more explicit for `v8.2` root coverage now, but it still synthesizes topic docs rather than mirroring every upstream page one-to-one.
- Page-level bundles normalize local markdown links and materialize inherited or CMP trace pages where needed, but some exact source pages still refer to omitted figures in prose because the upstream documentation depended on diagrams.
- Inherited page bundles are explicitly labeled, but they still reflect the nearest traceable source file rather than a guaranteed version-local restatement when the upstream version tree omitted that page.
- Some exact page bundles still preserve historical GUI prose for traceability; shared topic docs are the authoritative agent-first headless CLI/config guidance.
- Some exact page bundles still retain text-only `Omitted figure summary:` notes and equation/example lead-ins where the upstream source depended on diagrams or inline equation images; raw figure numbering is removed, but factual diagram content may still remain as prose when it adds model context.
- Some exact page bundles still contain XML comments inside fenced configuration examples. These are retained intentionally because they document config parameters; they are not treated as stray webpage markup.
- Some exact page bundles still contain escaped XML entities inside inline code or fenced examples when that escaping is the literal syntax an agent must preserve, for example XML logical operators in solver filters. Prose outside code is normalized more aggressively than these literal examples.
- The bundled pages now strip presentation-only Unicode punctuation aggressively, but semantically meaningful non-ASCII still remains in some places by design, especially Greek equation symbols, author-name diacritics, and the standard degree symbol `°`.
- Semantic HTML anchors such as `<a name="..."></a>` may still appear where same-page citation targets must remain stable across historical pages; these are retained deliberately as link targets rather than as UI residue.
