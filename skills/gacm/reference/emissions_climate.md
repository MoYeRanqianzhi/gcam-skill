# Emissions and Climate

Skill-bundled topic reference for CO2 and non-CO2 emissions, MAC behavior, Hector coupling, and climate-target interpretation.

Use this file after version routing when the user asks about emissions coefficients, linked GHG markets, air pollutants, climate constraints, or Hector outputs.

## Emissions Families
Modern GCAM tracks several emissions classes:
- fossil and industrial CO2
- land-use change CO2
- fugitive CO2 from fossil production
- non-CO2 greenhouse gases such as CH4 and N2O
- fluorinated gases
- air pollutants such as SO2, NOx, BC, OC, CO, VOCs, and NH3

## How Emissions Are Driven
Different emissions respond to different drivers:
- fuel use and technology choice in the energy system
- land allocation and agricultural activity in AgLU
- explicit MAC curves for many non-CO2 gases
- exogenous emissions controls that improve with income for many air pollutants

## MACs and Linked Markets
For many non-CO2 gases, GCAM uses technology-mapped marginal abatement curves.

Important controls:
- emissions price
- technology change in MAC response over time
- phase-in timing
- linked GHG markets through `linked-ghg-policy`

Operational caution:
- species-specific markets only make sense if the model has a mechanism to reduce that species
- `price-adjust` and related linked-market settings strongly affect interpretation

## Hector Coupling
Hector is the reduced-form climate and carbon-cycle model used in the modern GCAM line.

GCAM passes emissions into Hector each period. Hector then provides:
- concentrations
- radiative forcing
- temperature indicators
- land and ocean carbon-cycle variables
- ocean chemistry indicators such as pH-related outputs

## Climate Constraints
GCAM can target climate outcomes such as:
- concentration
- radiative forcing
- temperature
- cumulative emissions style outcomes in the target-finder framework

These runs usually require iterative searching rather than a single forward execution.

## Interpreting Results
When users ask about "emissions" or "climate results," first separate:
- emissions inventories vs scenario outputs
- fossil/industrial CO2 vs land-use change emissions
- direct GCAM outputs vs Hector-derived climate indicators

## Version Notes
- `v3.2` reflects older climate framing and legacy terminology.
- Modern lines use Hector-centered language in the bundled baseline.
- `delta-only` releases can alter emissions or climate-relevant details without providing a full standalone retelling of all baseline material.
