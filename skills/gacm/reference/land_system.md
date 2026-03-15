# Land System

Skill-bundled topic reference for land allocation, agricultural land competition, terrestrial carbon, and land-side policy mechanisms.

Use this file after version routing when the user asks about GLUs, crop competition, land carbon, afforestation, bioenergy land pressure, or land-use change emissions.

## Allocation Logic
GCAM land allocation is profit-driven and nested.

Key concepts:
- land uses compete through relative profitability
- the land tree defines which uses are close substitutes
- logit exponents control how strongly land shifts among competing uses
- calibration aligns base-year shares with observed land use

## GLUs, Nests, and Intensification
Modern GCAM land structure is tied to GLUs and nested crop or land categories.

Important consequences:
- crop, pasture, forest, and unmanaged land compete within structured nests
- irrigation and management levels allow price-induced intensification
- average yields can rise or fall depending on profitability, water cost, and fertilizer cost

## Carbon Accounting
GCAM tracks land-use change carbon through separate vegetation and soil logic.

Important distinctions:
- vegetation carbon releases on contraction are effectively immediate
- vegetation uptake on expansion is spread over time using maturity assumptions
- soil carbon changes evolve over longer, region-specific timescales
- land carbon policies therefore affect both land shares and multi-period emissions behavior

## Data and Calibration
Land inputs combine historical land cover, harvested area, productivity assumptions, and carbon-density information.

Modern cues:
- Moirai-generated land inputs play a central role in current lines
- users can alter carbon-state assumptions and some protection parameters through the data system
- GLU geography and carbon-density choices materially affect land outcomes

## Policy Levers
Common land-side levers include:
- land protection or availability constraints
- pricing land-use change carbon
- bioenergy quantity constraints
- land expansion costs or hard limits
- explicit carbon-park or afforestation-style interventions in customized setups

## Version Notes
- `v3.2` and early `v4.x` predate the fully modern GLU-oriented land framing.
- `v5+` is the important transition to the modern land-data architecture.
- `v7.1` adds notable AgLU parameter and forestry-detail updates in the bundled historical cues.
