# Water System

Skill-bundled topic reference for water demand, supply, basin mapping, scarcity, and cooling-system competition.

Use this file after version routing when the user asks about river basins, water withdrawals vs consumption, cooling technologies, groundwater, desalination, or water markets.

## Water Demand Sectors
Modern GCAM represents water demand across several major uses:
- agriculture
- electricity generation
- industrial manufacturing
- livestock
- primary energy production
- municipal use

These sectors use different coefficients, drivers, and spatial resolutions.

## Water Types
The bundled baseline distinguishes several water concepts:
- withdrawals
- consumption
- biophysical water consumption
- seawater use where relevant

Do not treat these as interchangeable. Many GCAM questions become ambiguous when the user says only "water use."

## Basin Mapping
- Agricultural water demand is naturally basin-linked.
- Several non-agricultural demands are computed at regional scale and then mapped to basins.
- Water scarcity and supply therefore depend on both region-to-basin mapping and sector structure.

## Supply Side
Water supply in the modern line includes:
- renewable water
- non-renewable groundwater
- desalinated water
- distribution and transport
- market mechanisms in some settings

## Electricity Cooling
Water and electricity are tightly coupled through cooling-system competition.

Important consequences:
- cooling choices can shift under water scarcity or higher water prices
- once-through, recirculating, pond, dry, and seawater-based systems have different withdrawal and consumption profiles
- electricity-sector water behavior is therefore both a power-system and water-system question

## Municipal and Industrial Demand
- municipal demand grows with income and population, moderated by price and technical change assumptions
- industrial demand excludes some energy-sector uses that are counted elsewhere
- interpretation often depends on whether the user wants delivered municipal water, self-supplied industrial water, or both

## Version Notes
- `v5.4+` is the closest structural family to the bundled modern water summary.
- Water-market and energy-for-water features become more explicit in later modern releases.
- Use the exact version route file when the user asks about a historical water feature or a release-specific update.
