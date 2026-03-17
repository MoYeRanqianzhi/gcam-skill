# GCAM-USA Reference

Bundled summary of GCAM-USA -- the 51-state (50 states + D.C.) sub-national extension of GCAM.

Use this file after version routing. GCAM-USA is most explicitly documented in the later modern families and the bundled `v8.2` baseline. If the user asks for an exact GCAM-USA path, sector definition, or policy structure in a named release, route to that release before reusing bundled baseline guidance.

## What GCAM-USA Adds

- 50 states + D.C. modeled as explicit regions inside the global GCAM.
- State-level energy transformation: electricity generation, refined-liquids production.
- State-level end-use demands: buildings, transportation, industry (including cement and N-fertilizer).
- Inter-state trade of energy goods with state-specific consumer price mark-ups (coal, natural gas, refined liquids).
- National-scale items retained: primary fossil resource production (oil, gas, coal) and biomass supply (modeled at U.S. water basins).

## State-Level Energy System Architecture

### Electricity
- Sub-annual load duration curves (LDCs) divided into four segments (baseload, intermediate, sub-peak, peak) at 15 grid-region level.
- State-specific coal and nuclear retirement schedules derived from EIA Form 860/923 and NRC data.
- Renewable resources (wind, solar PV, CSP, geothermal) use state-specific cost curves and capacity factors.
- Hydropower is exogenous, calibrated to state-level historical generation and AEO projections.
- Technology cost assumptions follow the global GCAM except capital costs for coal, gas, nuclear, wind, PV, and CSP which use U.S.-specific trajectories; ITC/PTC credits are included.

### Buildings
- Up to 10 energy services per state (space heating/cooling, water heating, etc.) with state-specific climate (HDD/CDD) inputs.
- Service demand driven by state population and GDP; envelope efficiency improves over the century.

### Transportation
- Three final demands: passenger, domestic freight, international shipping.
- State allocation based on EIA SEDS fuel-by-mode mapping (e.g., motor gasoline for LDV, jet fuel for air).
- Vehicle technology options include liquid fuels, hybrids, BEVs, hydrogen, consistent with global GCAM.

### Industry
- "Other industrial energy use" captures fuel-level competition; cement and N-fertilizer modeled separately by state.
- Industrial cogeneration allocated to states proportionally from national IEA autoproducer CHP data.
- Industry vintaging (`industry_vintage_USA.xml`) tracks capital stock turnover.

## Inter-State Electricity Trade
- States grouped into 15 grid regions consistent with NERC reliability regions.
- Free trade within a grid region; a region's net-importer/exporter status is fixed over time.
- Magnitude of inter-regional trade can change as relative prices shift, but the elasticity of expanding imports tightens as the import share exceeds historical levels.

## Refining Assumptions
- Each state has separate oil refining, BTL, CTL, and GTL sectors with logit competition.
- Oil refining expansion confined to current refining states; BTL distributed by current feedstock geography.
- CTL/GTL assumed to locate near coal/gas production states; no discovery of new resource basins assumed.

## Water Resources System
- Water supply: 23 U.S. basins from the global GCAM basin structure; three sources -- renewable surface/groundwater, non-renewable groundwater, desalination.
- State-level water demands for electricity, manufacturing, and municipal sectors.
- National-level demands (irrigation, livestock, mining) downscaled to state-basin intersections using gridded historical data (Huang et al. 2018); state-basin shares held constant at 2010 values.
- Electricity cooling: endogenous competition among cooling technologies; no new freshwater once-through systems allowed in future periods.
- Municipal water driven by state population and GDP; manufacturing water by state industrial activity with USGS-calibrated intensities.

## Socioeconomic Inputs
- Historical state population from U.S. Census through 2018; future from downscaled SSP2 (Jiang et al. 2018).
- Labor productivity growth from AEO per-capita GDP by Census Division through 2050; all states converge to a common rate by 2100.
- USA-region totals re-calibrated to match sum-of-states when GCAM-USA is active (differs from 32-region core).

## Reference Scenario Storyline Summary
The reference scenario assumes: (i) growing economy and peaking population; (ii) growing electricity demand with modest electrification; (iii) increasing gas and renewables in electricity, declining coal and limited nuclear; (iv) fixed net-importer/exporter status for grid regions; (v) conservative refining geography; (vi) modest declines in water withdrawals through mid-century driven by power-sector cooling reductions.

## Interpretation Cautions
- GCAM's logit-share and smooth retirement functions applied at state resolution can produce **non-monotonic** results in electricity and refining sectors. Discrete, lumpy real-world investments are smoothed.
- End-use sector projections (buildings, transportation) are generally **monotonic** because service demands are continuous functions of population and GDP.
- The model does not account for land-use restrictions, transmission infrastructure constraints, or other site-specific factors at the state level.
- Inter-state trade assumes free trade within a grid region with buildable infrastructure, potentially overstating the pace of trade shifts.
- Results are most reliable at the grid-region or national level; individual state results require careful interpretation.

## How to Enable GCAM-USA
Use the dedicated configuration file `exe/configuration_usa.xml`. Key USA-specific XML add-ons loaded on top of the global core include:
- `socioeconomics_USA.xml` -- state-level population and GDP
- `elec_segments_water_USA.xml` -- state electricity with endogenous cooling (preferred over `elec_segments_USA.xml`)
- `building_USA.xml`, `transportation_USA_CORE.xml`, `industry_USA.xml` -- state end-use sectors
- `en_transformation_USA.xml`, `en_prices_USA.xml` -- state energy transformation and prices
- `Cstorage_USA.xml`, `resources_USA.xml` -- state CCS and resources
- `water_td_USA.xml`, `water_demand_municipal_USA.xml`, `water_demand_industry_USA.xml` -- state water
- `ghg_emissions_USA.xml`, `bld_emissions_USA.xml`, etc. -- state non-CO2 and air pollutant emissions
- Scenario name is typically set to `GCAM-USA_Reference`; debug region defaults to `CA`.

## Version Differences

| Aspect | v5.x | v7.x | v8.x |
|--------|-------|-------|-------|
| Biomass supply geography | 10 agro-ecological zones (AEZs) | 22 U.S. water basins | 22 U.S. water basins |
| Reference storyline elements | 5 (no water) | 6 (adds water) | 6 (adds water) |
| Water demand modeling | National-only or early state pilots | State-level with endogenous cooling | State-level; enhanced water market balancing |
| Non-CO2 GHG at state level | Limited | CH4/N2O in energy + industrial process sectors | CH4/N2O + HFC + SF6; state air pollutants with CLE controls |
| Air pollutant emissions | Not included | Added (v7.0+) | Full NEI-calibrated CLE with CEDS scaling |
| Direct Air Capture | Not available | Not available | State-level DAC correlated with CO2 storage potential |
| Historical calibration final year | 2015 or earlier | 2015 | 2021 |
| Industrial detail | Aggregate + cement/fertilizer | Aggregate + cement/fertilizer + vintaging | Expanded sub-sectors (iron/steel, chemical, aluminum, paper, food processing) + vintaging |

## Authoring Basis
- Primary source: `gcam-doc/gcam-usa.md` (v8.2 baseline).
- Cross-checked against version-specific pages: v5.1, v7.0, v7.1, v8.2.
- Configuration details verified from `gcam-core/exe/configuration_usa.xml`.
