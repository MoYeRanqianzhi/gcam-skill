# Shared Socioeconomic Pathways (SSPs)

Bundled summary of SSP handling in GCAM.

Use this file after version routing. SSP interpretation changed across data vintages and model generations, so keep the exact version route in scope when the user asks for a historical release.

## SSP Overview
SSPs are reference scenarios describing societal challenges to mitigation and adaptation. GCAM was a marker model for SSP4. Each SSP can be paired with emissions mitigation assumptions (e.g., 2.6, 4.5, 6.0).

## GCAM Implementation
GCAM maps SSP narratives into quantitative assumptions:
- Socioeconomics (population, GDP)
- Energy supply costs and technical change
- Energy demand preferences
- Agriculture productivity and food preferences
- Policy timing and land policy

## Key Notes
- In practice, SSP assumptions are implemented through GCAM data inputs and data-system processing scripts.
- Official SSPs were based on GCAM4.0; differences exist in newer GCAM versions.

## Version Notes
- `v7.2` updates the SSP database inputs in the bundled delta stream.
- `v8.2` root docs are the bundled current full-topic baseline for SSP-oriented guidance.
- If the user asks for an exact SSP implementation in an older release, route to that version first rather than assuming modern data-system structure.
