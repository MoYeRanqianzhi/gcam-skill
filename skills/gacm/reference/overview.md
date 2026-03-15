# Overview

Skill-bundled baseline summary synthesized from the `v8.2` root documentation tree and cross-checked against older documentation families.

Use this file after version routing. If the user requested an older version, keep `versions/<version>.md` in scope and treat this overview as the closest modern conceptual map rather than a claim of exact page parity.

## What GCAM Is
GCAM is a global, dynamic-recursive, multi-sector integrated assessment model. It links energy, agriculture and land use, water, emissions, macroeconomic activity, and a reduced-form climate system. Each model period is solved sequentially; GCAM does not assume perfect foresight across the full century.

## How GCAM Advances Through Time
- Inputs define historical calibration structure plus future assumptions.
- Within each period, GCAM iterates on market prices until supply and demand clear.
- Solved outcomes for the period become part of the state handed to the next period.
- Climate and policy calculations feed back through prices, technology competition, land allocation, water scarcity, and emissions costs.

## Major System Blocks
- `common_assumptions.md`: shared spatial, temporal, and baseline modeling assumptions
- `choice_marketplace.md`: how GCAM chooses among technologies and clears markets
- `energy_system.md`: primary resources, electricity, liquids, gas, hydrogen, and trade
- `land_system.md`: land allocation, intensification, terrestrial carbon, and land policy
- `water_system.md`: basin-scale water demand, supply, scarcity, and cooling competition
- `economy.md`: exogenous socioeconomic drivers plus the GCAM-macro/KLEM coupling
- `emissions_climate.md`: fossil and non-CO2 emissions, MACs, Hector, and climate targets

## Scenario Interpretation
GCAM outputs are conditional scenarios, not predictions. Population, GDP, technology, land, water, and policy assumptions define a coherent scenario frame. GCAM then computes internally consistent trajectories for markets, quantities, emissions, and climate indicators under those assumptions.

## Version Guidance
- `v3.2` is a structurally different wiki-style family with 14-region framing and older climate terminology.
- `v4.x` introduces modular documentation, but not yet the full modern topic split.
- `v5.4` through `v7.1` are the closest historical relatives to the bundled baseline topic set.
- `v8.2` is the skill-bundled current full-topic baseline because it corresponds to the root `gcam-doc` documentation tree.

## Regional Variant
For U.S.-focused questions, open `gcam_usa.md` after version routing. GCAM-USA increases U.S. spatial detail while preserving global context in the surrounding model.
