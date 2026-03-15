# Version Families

GCAM documentation evolves in families rather than as perfectly uniform version-to-version clones. Use these family notes to avoid overgeneralizing across releases.

## `legacy-wiki`
Applies to:
- `v3.2`

Characteristics:
- Wiki-style page naming and topic organization.
- Older model framing and terminology.
- Broader narrative pages rather than later modular doc trees.

Important cues:
- Expect large topic pages such as climate module, transportation, buildings, and industry.
- Do not assume later naming like `overview.md`, `user-guide.md`, or `inputs_outputs` style pages.
- The bundled skill treats this family as structurally distinct.
- Start from the exact version file, then load only the bundled topic docs needed for the user's question.

## `compact-modern`
Applies to:
- `v4.2`
- `v4.3`
- `v4.4`

Characteristics:
- Early modular documentation with a smaller page set.
- More standardized than `v3.2`, but still less granular than v5.4+.

Important cues:
- `v4.2` is the main structural transition toward the modern organization.
- `v4.3` strengthens data-system and references documentation.
- `v4.4` adds `Fusion` as an explicit documented capability.
- Start from the exact version file, then load only the bundled topic docs needed for the user's question.

## `modern-transitional`
Applies to:
- `v5.1`
- `v5.2`
- `v5.3`

Characteristics:
- Modern page naming is established.
- Topic coverage broadens, but not yet at the same granularity as later releases.

Important cues:
- Use this family as the bridge between v4.x and later comprehensive docs.
- Avoid assuming every later dedicated topic page exists in the same form.
- Start from the exact version file, then load only the bundled topic docs needed for the user's question.

## `modern-comprehensive`
Applies to:
- `v5.4`
- `v6.0`
- `v7.0`
- `v7.1`
- `v8.2` (bundled current baseline; corresponds to the root `gcam-doc` full documentation tree)

Characteristics:
- Broad modular coverage across overview, running, building, solver, policies, and inputs/outputs.
- Best family for reusable topic routing.

Important cues:
- This family is the main backbone for the bundled topic docs.
- `v8.2` is the default full-topic baseline for this skill because the root of `gcam-doc` maps to `v8.2`.
- When the user says `root docs`, `current full docs`, or refers to the unqualified `gcam-doc` root tree, route to `v8.2`.
- Even within this family, version-specific deltas still matter.
- Start from the exact version file, then load only the bundled topic docs needed for the user's question.

## `delta-only`
Applies to:
- `v7.2`, `v7.3`, `v7.4`
- `v8.0`, `v8.1`
- `v8.3`, `v8.4`, `v8.5`, `v8.6`, `v8.7`

Characteristics:
- The skill bundles release deltas rather than a full independent topical restatement.

Important cues:
- Route through the relevant version file first.
- Load only the topic docs needed for the question.
- Be explicit that you are combining family/baseline understanding with documented release deltas.
- Do not describe these releases as if the skill bundles a separate full standalone documentation tree for each one.
