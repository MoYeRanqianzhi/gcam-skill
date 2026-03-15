# Energy System

Skill-bundled topic reference for GCAM energy resources, transformation sectors, technology competition, and trade.

Use this file after version routing when the user asks about electricity, liquids, gas, hydrogen, renewables, CCS, resource supply curves, or interregional energy trade.

## Primary Resource Classes
GCAM distinguishes two broad primary-resource families:
- depletable resources such as oil, unconventional oil, natural gas, coal, and uranium
- renewable resources such as wind, solar, geothermal, hydropower, biomass, and traditional biomass

Depletable resources are represented with graded supply curves and reserve-like dynamics.
Renewables are generally represented as annual flow resources with technology and integration costs layered on top.

## Transformation Sectors
The bundled current baseline organizes energy transformation around several major sectors:
- electricity
- refining and liquids production
- gas processing
- district services in regions where purchased heat matters
- hydrogen production and delivery

These sectors transform primary resources into final energy carriers consumed by buildings, transport, industry, water systems, and other activities.

## Electricity
Electricity is one of the most policy-sensitive and water-sensitive parts of GCAM.

Key features:
- multiple competing technologies by fuel and design
- explicit CCS options for several technologies
- technology cost combines non-energy cost, input fuel cost, and emissions value
- cooling-system choices can matter materially for water use and cost
- intermittent integration assumptions become especially important in later modern releases

## Liquids, Gas, and Hydrogen
- refining combines crude and other feedstocks into a single refined-liquids commodity family for downstream use
- gas processing differentiates natural gas, coal gasification, and biomass gasification pathways
- hydrogen has central and forecourt production variants plus distribution-state distinctions in the modern line

Version cues:
- `v6.0+` expands hydrogen and direct-air-capture-related context substantially
- `v7.1` adds hydrogen and ammonia-trade-related updates in the bundled historical cues
- `v7.3` specifically updates intermittent electricity integration in the delta stream

## Energy Trade
GCAM uses an Armington-style structure for several traded primary commodities, especially coal, oil, gas, and bioenergy.

Important limits:
- most renewables are not traded inter-regionally
- electricity and hydrogen are generally not modeled as globally traded secondary commodities in the standard global setup
- domestic and imported variants can coexist in the same regional consumption decision

## Technology Competition and Costs
Technology share depends on:
- technology-specific non-energy cost
- input prices and efficiencies
- emissions prices or values
- share weights and logit settings

Open `choice_marketplace.md` for the logit interpretation and `emissions_climate.md` for how policy prices feed into these costs.

## Policy Levers
Typical energy-side levers include:
- carbon pricing
- emissions constraints
- energy quantity or share standards
- bioenergy constraints
- CCS deployment assumptions

## Historical Notes
- `v3.2` and early `v4.x` describe many of the same systems with different page organization and older examples.
- `v5.4+` is the closest historical family to this bundled modern energy-system summary.
