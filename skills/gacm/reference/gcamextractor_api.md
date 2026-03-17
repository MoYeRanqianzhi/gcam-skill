# gcamextractor API (R)

Agent-oriented reference for the upstream `gcamextractor` R package.

Use this file after version routing when the user needs the `readgcam` argument surface, standardized table outputs, `.Proj` reuse, or the authoritative mapping between params and underlying queries.

## Package Role
`gcamextractor` sits on top of GCAM query output workflows and standardizes the extracted tables for downstream analysis.

Use it when the user wants:
- R-native post-processing
- parameter- or class-level aggregations
- unit conversions already handled for them
- reusable `.Proj` snapshots instead of re-querying every time

## Install
```r
install.packages("devtools")
devtools::install_github("JGCRI/gcamextractor")
```

## Exported Functions

The NAMESPACE exports exactly three functions:
- `readgcam` -- main extraction entry point
- `get_example_data` -- download example data from Zenodo
- `gdp_deflator` -- GDP implicit price deflator calculation

---

## Main Entry Point: `readgcam`

### Full Source Signature (16 parameters)

```r
readgcam(
  gcamdatabase      = NULL,
  gcamdata_folder   = NULL,
  queryFile         = NULL,
  dataProjFile      = "dataProj.proj",
  maxMemory         = "4g",
  scenOrigNames     = "All",
  scenNewNames      = NULL,
  reReadData        = T,
  regionsSelect     = NULL,
  regionsAggregate  = NULL,
  regionsAggregateNames = NULL,
  paramsSelect      = "diagnostic",
  folder            = getwd(),
  nameAppend        = "",
  saveData          = T,
  removeVintages    = F
)
```

### Parameter Descriptions

| # | Parameter | Default | Description |
|---|-----------|---------|-------------|
| 1 | `gcamdatabase` | `NULL` | Full path to the GCAM database directory. Source stops if the path does not exist. |
| 2 | `gcamdata_folder` | `NULL` | Full path to the `gcamdata` folder. Required only for params that need gcamdata files (e.g. `elec_lifetime_scurve_yr`, `elec_fuel_co2_content_tonsperMBTU`). Source warns and skips those params if the folder is missing. |
| 3 | `queryFile` | `NULL` | Path to an XML query file. When `NULL`, the package materializes the bundled `queries_xml` to `folder/queries.xml` automatically. |
| 4 | `dataProjFile` | `"dataProj.proj"` | Cached `.Proj` file path. When `reReadData=TRUE` this is the output name; when `FALSE` this file is loaded directly. |
| 5 | `maxMemory` | `"4g"` | Java / rgcam memory budget string (e.g. `"4g"`, `"8g"`). Increase for very large databases. |
| 6 | `scenOrigNames` | `"All"` | Original scenario names in the GCAM database as a character vector, e.g. `c("scenario1","scenario2")`. `"All"` reads every available scenario. |
| 7 | `scenNewNames` | `NULL` | Replacement scenario labels for output tables and figures. Must match the length of `scenOrigNames`. When `NULL`, original names are kept. |
| 8 | `reReadData` | `TRUE` | `TRUE` to query the GCAM database and create/update the `.Proj`; `FALSE` to reuse an existing `.Proj` file. |
| 9 | `regionsSelect` | `NULL` | Character vector of regions to keep, e.g. `c("Colombia","Argentina")`. `NULL` keeps all regions. `"United States"` is auto-normalized to `"USA"`. |
| 10 | `regionsAggregate` | `NULL` | Vector or list of vectors defining regions to aggregate. Single vector adds one aggregate; list of vectors adds multiple. Example: `list(c("South America_Northern","South America_Southern"), c("USA","Canada","Mexico"))`. |
| 11 | `regionsAggregateNames` | `NULL` | Character vector of names for aggregate regions. Length must match `regionsAggregate`. Example: `c("South America","North America")`. |
| 12 | `paramsSelect` | `"diagnostic"` | Parameter group name, individual parameter names, or `"All"`. See Parameter Selection Model below. |
| 13 | `folder` | `getwd()` | Output directory for saved CSV files and the `.Proj`. |
| 14 | `nameAppend` | `""` | Suffix appended to all saved file names. |
| 15 | `saveData` | `TRUE` | Whether to write CSV output files to disk. |
| 16 | `removeVintages` | `FALSE` | When `TRUE`, vintage columns are dropped from aggregation outputs. |

### Return Value

A named list with seven elements:

| Element | Description |
|---------|-------------|
| `dataAll` | Full tibble with all columns including `origQuery`, `origValue`, `origUnits`, `origScen`, `origX` |
| `data` | Cleaned tibble: `scenario`, `region`, `subRegion`, `param`, `classLabel1`, `class1`, `classLabel2`, `class2`, `xLabel`, `x`, `vintage`, `aggregate`, `units`, `value` |
| `dataAggClass1` | Aggregated across class 2 (summed or averaged by `aggregate` flag) |
| `dataAggClass2` | Aggregated across class 1 |
| `dataAggParam` | Aggregated across both class dimensions to the param level |
| `scenarios` | Character vector of scenario names in the database |
| `queries` | Character vector of queries from the query XML |

When `saveData=TRUE`, the following CSVs are written:
- `gcamDataTable_Extended{nameAppend}.csv` (dataAll)
- `gcamDataTable{nameAppend}.csv` (data)
- `gcamDataTable_aggClass1{nameAppend}.csv`
- `gcamDataTable_aggClass2{nameAppend}.csv`
- `gcamDataTable_aggParam{nameAppend}.csv`

---

## Parameter Selection Model

`paramsSelect` can be:
- `"All"` -- all params in `map_param_query`
- A group name (e.g. `"energy"`, `"diagnostic"`)
- A character vector of individual param names

### Group Families

There are 14 distinct groups defined in `map_param_query`:

| Group | Description |
|-------|-------------|
| `summary` | Key overview indicators (GDP, population, emissions, energy, electricity) |
| `diagnostic` | Balanced cross-domain snapshot for quick diagnostics |
| `energy` | Primary and final energy by fuel, sector, subsector (EJ, MTOE, TWh) |
| `electricity` | Generation by tech, capacity, demand-sector consumption, load segments |
| `transport` | Passenger/freight VMT by mode, fuel, tech; transport GHG by mode |
| `buildings` | Service output by technology; building floorspace |
| `water` | Consumption, withdrawals, irrigation, runoff by sector/crop/basin |
| `socioecon` | GDP, GDP per capita, GDP growth rate, population |
| `ag` | Agricultural production by irrigation/rainfed, biomass, forest, crop |
| `fertilizer` | Fertilizer consumption by agricultural technology |
| `livestock` | Meat and dairy production by mixed/pastoral/import tech and subsector |
| `land` | Land allocation irrigated/rainfed, by crop, aggregated, detailed |
| `emissions` | GHG by sector/gas (GWP AR5), CO2 by sector, LUC, methane, cumulative |
| `hydrogen` | Production, utilization, prices, costs, inputs, outputs by tech |
| `general` | Generic inputs/outputs by technology |
| `cerf` | Capacity Expansion Regional Feasibility parameters (heat rates, lifetimes, costs, capture rates) |
| `go` | Grid Operations parameters (heat rate, fuel prices) |
| `demeter` | Demeter land model parameters (detailed land allocation, crops, fertilizer) |

### Complete Parameter List by Group

#### summary (10 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `emissGHGBySectorGWPAR5` | nonCO2 emissions by sector + CO2 emissions by sector + LUC + sequestration | GHG emissions by sector using GWP AR5 100-yr potentials |
| `emissGHGByGasGWPAR5` | (same queries as above) | GHG emissions by individual gas using GWP AR5 |
| `emissCO2BySector` | CO2 emissions by sector + no bio + sequestration + LUC | CO2 emissions by sector including bioenergy and LUC |
| `energyFinalConsumBySecEJ` | total final energy by aggregate sector | Final energy consumption by aggregate end-use sector (EJ) |
| `energyFinalByFuelEJ` | Final energy by detailed end-use sector and fuel | Final energy by fuel type across sectors (EJ) |
| `elecConsumByDemandSectorTWh` | elec consumption by demand sector | Electricity consumption disaggregated by demand sector (TWh) |
| `elecByTechTWh` | elec gen by gen tech (cogen/USA/cooling) | Electricity generation by generation technology (TWh) |
| `gdpPerCapita` | GDP per capita MER by region | GDP per capita at market exchange rates |
| `gdp` | GDP MER by region | Total GDP at market exchange rates |
| `pop` | Population by region | Population by region |

#### diagnostic (22 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `energyPrimaryByFuelMTOE` | primary energy consumption by region (direct equivalent) | Primary energy by fuel (Mtoe) |
| `energyPrimaryRefLiqProdMTOE` | refined liquids production by subsector | Refined liquid fuel production (Mtoe) |
| `energyFinalConsumBySecMTOE` | total final energy by aggregate sector | Final energy consumption by sector (Mtoe) |
| `energyFinalByFuelBySectorMTOE` | Final energy by detailed end-use sector and fuel | Final energy by fuel and sector (Mtoe) |
| `elecByTechTWh` | elec gen by gen tech (cogen/USA/cooling) | Electricity generation by technology (TWh) |
| `elecCapByFuel` | elec gen by gen tech (cogen/USA/cooling) | Electricity capacity by fuel type (GW) |
| `elecFinalBySecTWh` | inputs by tech | Electricity delivered to final sectors (TWh) |
| `elecFinalByFuelTWh` | Final energy by detailed end-use sector and fuel | Final electricity consumption by fuel (TWh) |
| `transportPassengerVMTByMode` | transport service output by mode | Passenger transport VMT by travel mode |
| `transportFreightVMTByMode` | transport service output by mode | Freight transport VMT by mode |
| `transportPassengerVMTByFuel` | transport service output by tech | Passenger transport VMT by fuel type |
| `transportFreightVMTByFuel` | transport service output by tech | Freight transport VMT by fuel type |
| `watConsumBySec` | water consumption by state, sector, basin (includes desal) | Water consumption by sector |
| `watWithdrawBySec` | water withdrawals by state, sector, basin (includes desal) | Water withdrawals by sector |
| `watWithdrawByCrop` | water withdrawals by crop | Water withdrawals by crop type |
| `watSupRunoffBasin` | Basin level available runoff | Available surface runoff by basin |
| `gdpPerCapita` | GDP per capita MER by region | GDP per capita at market exchange rates |
| `gdp` | GDP MER by region | Total GDP |
| `gdpGrowthRate` | GDP Growth Rate (Percent) | GDP growth rate as percentage |
| `pop` | Population by region | Population by region |
| `agProdByCrop` | ag production by tech | Agricultural production by crop |
| `landAlloc` | aggregated land allocation | Aggregated land allocation |
| `landAllocByCrop` | land allocation by crop | Land allocation broken down by crop |
| `emissLUC` | Land Use Change Emission (future) | Land-use change CO2 emissions |
| `emissCO2BySector` | CO2 emissions by sector | CO2 emissions by sector |

#### energy (33 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `energyPrimaryByFuelEJ` | primary energy consumption by region (direct equivalent) | Primary energy by fuel (EJ) |
| `energyPrimaryRefLiqProdEJ` | refined liquids production by subsector | Refined liquid fuel production (EJ) |
| `energyFinalConsumBySecEJ` | total final energy by aggregate sector | Final energy consumption by sector (EJ) |
| `energyFinalByFuelBySectorEJ` | Final energy by detailed end-use sector and fuel | Final energy by fuel and sector (EJ) |
| `energyFinalSubsecByFuelTranspEJ` | transport final energy by fuel | Final energy in transport by fuel (EJ) |
| `energyFinalSubsecByFuelBuildEJ` | building final energy by fuel | Final energy in buildings by fuel (EJ) |
| `energyFinalSubsecByFuelIndusEJ` | industry final energy by fuel | Final energy in industry by fuel (EJ) |
| `energyFinalSubsecBySectorBuildEJ` | building final energy by subsector | Final energy in buildings by subsector (EJ) |
| `energyFinalConsumByIntlShpAvEJ` | transport final energy by mode and fuel | International shipping and aviation energy (EJ) |
| `energyFinalConsumBySecEJNoFeedstock` | total final energy by sector | Final energy by sector excluding feedstock (EJ) |
| `energyFinalByFuelEJNoFeedstock` | Final energy by detailed end-use sector and fuel | Final energy by fuel excluding feedstock (EJ) |
| `energyPrimaryByFuelMTOE` | primary energy consumption by region (direct equivalent) | Primary energy by fuel (Mtoe) |
| `energyPrimaryRefLiqProdMTOE` | refined liquids production by subsector | Refined liquid fuel production (Mtoe) |
| `energyFinalConsumBySecMTOE` | total final energy by aggregate sector | Final energy consumption by sector (Mtoe) |
| `energyFinalByFuelBySectorMTOE` | Final energy by detailed end-use sector and fuel | Final energy by fuel and sector (Mtoe) |
| `energyFinalbyFuelMTOE` | Final energy by detailed end-use sector and fuel | Final energy by fuel (Mtoe) |
| `energyFinalSubsecByFuelTranspMTOE` | transport final energy by fuel | Final energy in transport by fuel (Mtoe) |
| `energyFinalSubsecByFuelBuildMTOE` | building final energy by fuel | Final energy in buildings by fuel (Mtoe) |
| `energyFinalSubsecByFuelIndusMTOE` | industry final energy by fuel | Final energy in industry by fuel (Mtoe) |
| `energyFinalSubsecBySectorBuildMTOE` | building final energy by subsector | Final energy in buildings by subsector (Mtoe) |
| `energyFinalConsumByIntlShpAvMTOE` | transport final energy by mode and fuel | International shipping and aviation energy (Mtoe) |
| `energyPrimaryByFuelTWh` | primary energy consumption by region (direct equivalent) | Primary energy by fuel (TWh) |
| `energyPrimaryRefLiqProdTWh` | refined liquids production by subsector | Refined liquid fuel production (TWh) |
| `energyFinalConsumBySecTWh` | total final energy by aggregate sector | Final energy consumption by sector (TWh) |
| `energyFinalbyFuelTWh` | Final energy by detailed end-use sector and fuel | Final energy by fuel (TWh) |
| `energyFinalSubsecByFuelTranspTWh` | transport final energy by fuel | Final energy in transport by fuel (TWh) |
| `energyFinalSubsecByFuelBuildTWh` | building final energy by fuel | Final energy in buildings by fuel (TWh) |
| `energyFinalSubsecByFuelIndusTWh` | industry final energy by fuel | Final energy in industry by fuel (TWh) |
| `energyFinalSubsecBySectorBuildTWh` | building final energy by subsector | Final energy in buildings by subsector (TWh) |
| `energyFinalConsumByIntlShpAvTWh` | transport final energy by mode and fuel | International shipping and aviation energy (TWh) |
| `energyFinalByFuelBySectorTWh` | Final energy by detailed end-use sector and fuel | Final energy by fuel and sector (TWh) |

Note: MTOE and TWh variants are registered in `map_param_query` but the EJ-to-MTOE/TWh conversion code in `readgcam.R` is currently commented out (lines ~6709-6719). The EJ params are fully implemented; MTOE/TWh may not produce output in the current source.

#### electricity (6 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `elecByTechTWh` | elec gen by gen tech (cogen USA / USA / cooling tech) | Electricity generation by generation technology (TWh) |
| `elecCapByFuel` | elec gen by gen tech (cogen USA / USA / cooling tech) | Installed electricity capacity by fuel type (GW) |
| `elecFinalBySecTWh` | inputs by tech | Electricity delivered to final demand sectors (TWh) |
| `elecFinalByFuelTWh` | Final energy by detailed end-use sector and fuel | Final electricity by fuel (TWh) |
| `elecConsumByDemandSectorTWh` | elec consumption by demand sector | Electricity consumption by demand sector (TWh) |
| `elecLoadBySegmentGW` | elec gen by segment (grid level) | Electricity generation by load segment (GW). Requires gcamdata file `L102.load_segments_gcamusa`. |

#### transport (8 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `transportPassengerVMTByMode` | transport service output by mode | Passenger vehicle-miles traveled by mode (bus, rail, air, LDV, etc.) |
| `transportFreightVMTByMode` | transport service output by mode | Freight ton-miles by mode |
| `transportPassengerVMTByFuel` | transport service output by tech | Passenger VMT broken down by fuel type |
| `transportFreightVMTByFuel` | transport service output by tech | Freight VMT broken down by fuel type |
| `transportPassengerVMTByTech` | transport service output by tech | Passenger VMT by specific vehicle technology |
| `transportFreightVMTByTech` | transport service output by tech | Freight VMT by specific vehicle technology |
| `transportPassengerGHGByMode` | nonCO2 emissions by subsector | Passenger transport GHG emissions by mode (GWP AR5, Mt CO2-eq) |
| `transportFreightGHGByMode` | nonCO2 emissions by subsector | Freight transport GHG emissions by mode (GWP AR5, Mt CO2-eq) |

Also registered in `map_param_query` but not confirmed with `paramx` in source:
- `transportPassengerVMTByFuelNew` (query: transport service output by tech (new))
- `transportFreightVMTByFuelNew` (query: transport service output by tech (new))

#### buildings (2 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `serviceOutputByTechBuildings` | building service output by tech | Building service output disaggregated by technology |
| `buildingFloorspace` | building floorspace | Total building floorspace by region |

#### water (8 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `watConsumBySec` | water consumption by state, sector, basin (includes desal) | Water consumption by sector |
| `watWithdrawBySec` | water withdrawals by state, sector, basin (includes desal) | Water withdrawals by sector |
| `watWithdrawByCrop` | water withdrawals by crop | Water withdrawals disaggregated by crop type |
| `watBioPhysCons` | biophysical water demand by crop type and land region | Biophysical water consumption by crop and land region |
| `watIrrWithdrawBasin` | water withdrawals by water mapping source | Irrigation water withdrawals by basin |
| `watIrrConsBasin` | water consumption by water mapping source | Irrigation water consumption by basin |
| `watSupRunoffBasin` | Basin level available runoff | Available surface runoff at basin level |
| `waterWithdrawROGW` | Water withdrawals by water source (runoff vs. groundwater) | Water withdrawals split between runoff and groundwater sources |

#### socioecon (4 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `gdpPerCapita` | GDP per capita MER by region | GDP per capita at market exchange rates |
| `gdp` | GDP MER by region | Total GDP at market exchange rates |
| `gdpGrowthRate` | GDP Growth Rate (Percent) | GDP growth rate as percentage |
| `pop` | Population by region | Population by region |

#### ag (4 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `agProdbyIrrRfd` | ag production by tech | Agricultural production split by irrigated vs. rainfed |
| `agProdBiomass` | ag production by tech | Biomass production from agriculture |
| `agProdForest` | ag production by tech | Forest product production |
| `agProdByCrop` | ag production by tech | Agricultural production by individual crop |

#### fertilizer (1 param)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `fertConsByAgTech` | fertilizer consumption by ag tech | Fertilizer consumption by agricultural technology |

Note: the group name in `map_param_query` is spelled `"fertilzier"` (typo in source).

#### livestock (4 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `livestock_MeatDairybyTechMixed` | meat and dairy production by tech | Meat and dairy production from mixed farming systems |
| `livestock_MeatDairybyTechPastoral` | meat and dairy production by tech | Meat and dairy production from pastoral systems |
| `livestock_MeatDairybyTechImports` | meat and dairy production by tech | Meat and dairy production from import-based systems |
| `livestock_MeatDairybySubsector` | meat and dairy production by tech | Meat and dairy production by subsector aggregation |

#### land (6 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `landIrrRfd` | land allocation by crop and water source | Land allocation split irrigated vs. rainfed |
| `landIrrCrop` | land allocation by crop and water source | Irrigated land allocation by crop |
| `landRfdCrop` | land allocation by crop and water source | Rainfed land allocation by crop |
| `landAlloc` | aggregated land allocation | Aggregated land allocation across categories |
| `landAllocByCrop` | land allocation by crop | Land allocation broken down by individual crop |
| `landAllocDetail` | detailed land allocation | Detailed land allocation (all leaf nodes) |

#### emissions (18 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `emissGHGBySectorGWPAR5` | nonCO2 by sector + CO2 by sector + LUC + sequestration | Total GHG emissions by sector using 100-yr GWP AR5 (Mt CO2-eq) |
| `emissGHGBySectorNoBioGWPAR5` | nonCO2 by sector + CO2 no bio + LUC + sequestration | GHG by sector excluding bioenergy CO2 (GWP AR5) |
| `emissGHGByGasGWPAR5` | nonCO2 by sector + CO2 by sector + LUC + sequestration | GHG emissions by individual gas (GWP AR5) |
| `emissGHGByGasNoBioGWPAR5` | nonCO2 by sector + CO2 no bio + LUC + sequestration | GHG by gas excluding bioenergy CO2 (GWP AR5) |
| `emissGHGByResProdGWPAR5` | nonCO2 emissions by resource production | GHG from resource production (GWP AR5) |
| `emissLUC` | Land Use Change Emission (future) | Land-use change CO2 emissions |
| `emissCO2BySector` | CO2 emissions by sector + sequestration + LUC | CO2 emissions by sector (including bioenergy and LUC) |
| `emissCO2BySectorNoBio` | CO2 emissions by sector (no bio) + sequestration + LUC | CO2 emissions by sector excluding bioenergy |
| `emissCO2CumGlobal2010to2100` | CO2 emissions by sector | Cumulative global CO2 emissions 2010-2100 |
| `emissCO2CumGlobal2010to2100RCP` | CO2 emissions by sector | Cumulative global CO2 vs. RCP benchmarks |
| `emissMethaneBySourceGWPAR5` | nonCO2 emissions by sector | Methane emissions by source (GWP AR5) |
| `emissGHGBySectorPowerGWPAR5` | CO2 emissions by sector + nonCO2 by sector | Power-sector GHG emissions (GWP AR5) |
| `emissGHGBySectorBuildingsGWPAR5` | nonCO2 by sector + CO2 no bio | Buildings-sector GHG emissions (GWP AR5) |
| `emissGHGBySectorTransportGWPAR5` | nonCO2 by subsector + CO2 by subsector | Transport-sector GHG emissions (GWP AR5) |
| `emissGHGBySectorIndustryGWPAR5` | nonCO2 by subsector + CO2 by subsector | Industry-sector GHG emissions (GWP AR5) |
| `co2SequestrationBySector` | CO2 sequestration by sector | CO2 captured and sequestered by sector |

Commented-out / documented but not active in current source (GTP variants):
- `emissGHGBySectorGTPAR5`, `emissNonCO2ByResProdGWPAR5`, `emissBySectorGWPAR5FFI`, `emissByGasGWPAR5FFI`, `emissByGasGWPAR5LUC`, `emissBySectorGWPAR5LUC`, `emissNonCO2ByResProdGTPAR5`, `emissMethaneBySourceGTPAR5`, `emissByGasGTPAR5FFI`, `emissByGasGTPAR5LUC`, `emissBySectorGTPAR5FFI`, `emissBySectorGTPAR5LUC`

These are listed in the roxygen `@param paramsSelect` documentation but their `map_param_query` entries are commented out and no `paramx` implementation exists in the current source.

#### hydrogen (6 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `hydrogenProdByTech` | hydrogen production by tech | Hydrogen production by technology (e.g. electrolysis, SMR) |
| `hydrogenUtilizationByTech` | hydrogen utilization by technology | Hydrogen consumption/utilization by end-use technology |
| `hydrogenPricesBySector` | hydrogen prices by sector | Hydrogen prices disaggregated by demand sector |
| `hydrogenCostsByTech` | hydrogen costs by tech | Hydrogen production costs by technology |
| `hydrogenInputsByTech` | hydrogen inputs by tech | Input fuels/feedstocks for hydrogen production by technology |
| `hydrogenOutputsByTech` | hydrogen outputs by technology | Outputs from hydrogen production by technology |

#### general (2 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `inputs` | inputs by tech | Generic technology inputs across all sectors |
| `outputs` | outputs by tech | Generic technology outputs across all sectors |

#### cerf (11 params -- Capacity Expansion Regional Feasibility)

| Param | Underlying Query | gcamdata Required | Description |
|-------|-----------------|-------------------|-------------|
| `elec_heat_rate_BTUperkWh` | elec coeff | no | Electricity heat rate by tech and vintage (BTU/kWh) |
| `elec_heat_rate_MBTUperMWh` | elec coeff | no | Heat rate converted to MBTU/MWh |
| `elec_cap_usa_GW` | elec capacity by tech and vintage | no | US electricity capacity by tech and vintage (GW) |
| `elec_variable_om_2015USDperMWh` | elec operating costs by tech and vintage | no | Variable O&M costs (2015 USD/MWh) |
| `elec_variable_om_escl_rate_fraction` | elec operating costs by tech and vintage | no | Variable O&M escalation rate (fraction) |
| `elec_fuel_price_2015USDperMBTU` | prices by sector | no | Fuel prices for power generation (2015 USD/MBTU) |
| `elec_fuel_price_escl_rate_fraction` | prices by sector | no | Fuel price escalation rate (fraction) |
| `elec_capacity_factor_usa_in` | elec investment capacity factor | no | Capacity factors for US electricity generation |
| `elec_lifetime_scurve_yr` | NA | yes (L2244, L223, L2241, L2233 outputs) | S-curve retirement parameters (half-life, steepness) by tech |
| `elec_lifetime_yr` | NA | yes (L223, L2242, L2233 outputs) | Straight lifetime in years by tech |
| `elec_fuel_co2_content_tonsperMBTU` | NA | yes (L2261, L202, L222 outputs) | Fuel CO2 content (tons/MBTU) by technology |
| `elec_carbon_capture_rate_fraction` | NA | yes (L223, L2233 outputs) | Carbon capture rate as fraction by technology |
| `elec_carbon_capture_escl_rate_fraction` | NA | yes (L223, L2233 outputs) | Carbon capture escalation rate fraction |

Note: params requiring gcamdata automatically prepend `"pop"` to `paramsSelect` internally. These params are expanded across all scenarios and US states after extraction.

#### go (2 params -- Grid Operations)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `elec_heat_rate_BTUperkWh` | elec coeff | Heat rate (shared with cerf group) |
| `elec_fuel_price_2015USDperMBTU` | prices by sector | Fuel prices (shared with cerf group) |

#### demeter (3 params)

| Param | Underlying Query | Description |
|-------|-----------------|-------------|
| `landAllocDetail` | detailed land allocation | Detailed land allocation for Demeter coupling |
| `agProdByCrop` | ag production by tech | Agricultural production by crop |
| `fertConsByAgTech` | fertilizer consumption by ag tech | Fertilizer consumption by ag technology |

---

## `get_example_data`

```r
get_example_data(
  write_dir = getwd(),
  dir_name  = "gcamextractor_example_data",
  data_link = NULL
)
```

Downloads test data files from Zenodo needed for example runs.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `write_dir` | `getwd()` | Directory to write the downloaded zip and extracted files |
| `dir_name` | `"gcamextractor_example_data"` | Name of the subdirectory for extracted files |
| `data_link` | `NULL` | URL to the Zenodo zip file. When `NULL`, the function skips download and prints a message |

Returns the path to the extracted data directory: `paste0(write_dir, "/", dir_name)`.

Behavior:
- If the zip file already exists at `write_dir/dir_name.zip`, download is skipped
- Download timeout is set to `max(3600, getOption("timeout"))` for large files
- Zip is extracted then deleted automatically

---

## `gdp_deflator`

```r
gdp_deflator(year, base_year)
```

Calculate a GDP implicit price deflator between two years. From the BEA "A191RD3A086NBEA" series (downloaded April 13, 2017 from FRED).

| Parameter | Description |
|-----------|-------------|
| `year` | Year to convert TO |
| `base_year` | Year to convert FROM |

Returns a numeric deflator. Multiply prices in `base_year` dollars by the result to get `year` dollars.

Coverage: 1929-2019.

Source: U.S. Bureau of Economic Analysis via FRED (Federal Reserve Bank of St. Louis).

---

## Exported Datasets

### Parameter and Query Mapping

| Dataset | Format | Description |
|---------|--------|-------------|
| `params` | character vector | Sorted unique parameter names from `map_param_query$param` |
| `queries` | character vector | Sorted unique query names from `map_param_query$query` |
| `map_param_query` | tibble (columns: `group`, `param`, `query`, `mapPalette`, `gcamdata`) | Authoritative mapping between params, their GCAM queries, group membership, palette, and gcamdata dependency. This is the most important helper table for agents. Use it to answer: which query underlies a param, which group a param belongs to, whether a param needs gcamdata. |

### Region and Mapping Helpers

| Dataset | Format | Description |
|---------|--------|-------------|
| `regions_gcam32` | tibble | The 32 standard GCAM world regions |
| `regions_gcam_basins` | tibble | GCAM water basin regions |
| `regions_US52` | tibble | 52 US regions (50 states + DC + Puerto Rico) |
| `regions_US49` | tibble | 49 GCAM-USA regions (excludes Alaska, Hawaii, Puerto Rico; includes DC) |
| `map_country_to_gcam_region` | tibble (columns: `gcam_region_code`, `country_code`, `gcam_region`, `country`) | Mapping of individual countries to GCAM 32 regions |
| `map_state_to_gridregion` | tibble (columns: `state`, `grid_region`, `country`) | Mapping of US states to GCAM grid regions |

### Conversion and Economics Helpers

| Dataset | Format | Description |
|---------|--------|-------------|
| `convert` | named list | Unit conversion factors. Access as e.g. `convert$conv_EJ_to_MTOE`, `convert$conv_EJ_to_TWh`, `convert$conv_BTU_per_kWh`. |
| `GWP` | tibble (columns: `ghg`, `GWPAR5`, plus others) | Global Warming Potentials for GHG-to-CO2eq conversion. Uses 100-yr GWP from IPCC AR4 and AR5. Also includes GTP AR5 values. |
| `conv_GgTg_to_MTC` | tibble (columns: `Units`, `Convert`) | Conversion factors from Gg/Tg to Megatonnes of Carbon (MTC). 1 Tg = 1 Megatonne = 10^6 tonnes. |
| `capfactors` | data.table | Capacity factors by electricity generation subsector. Source: `capacity_factor_by_elec_gen_subsector.csv`. |

### XML and Example Data

| Dataset | Format | Description |
|---------|--------|-------------|
| `queries_xml` | XML node | Bundled XML query definition file. When `queryFile=NULL` in `readgcam()`, this is written to `folder/queries.xml`. Can be saved with `XML::saveXML(gcamextractor::queries_xml, file="queries.xml")`. |
| `example_gcamv54_argentina_colombia_2025_proj` | .Proj file | Pre-extracted example project data for GCAM v5.4, Argentina + Colombia, year 2025. For use with `readgcam(dataProjFile=..., reReadData=FALSE)`. |
| `gcamextractor_test_data` | tibble | Internal test data for package testing |

---

## `.Proj` Workflow
Use `.Proj` files when extraction is expensive and the user will iterate on analysis.

Rules:
- `reReadData=TRUE`: query GCAM again and create or update the `.Proj`
- `reReadData=FALSE`: reuse an existing `.Proj`
- `dataProjFile` can point to an existing file or define where a new cached project should be written

This is the preferred path when:
- the same scenario set is reused repeatedly
- the user wants to share extracted data without sharing the whole GCAM DB

---

## Minimal Workflows

### Extract directly from a GCAM database
```r
library(gcamextractor)

dataGCAM <- gcamextractor::readgcam(
  gcamdatabase = "/path/to/gcam/output/database_ref",
  regionsSelect = c("Colombia"),
  paramsSelect = "pop",
  folder = "my_output_folder"
)
```

### Reuse a cached `.Proj`
```r
library(gcamextractor)

dataGCAM <- gcamextractor::readgcam(
  dataProjFile = "/path/to/dataProj.proj",
  reReadData = FALSE,
  folder = "my_output_folder"
)
```

### Inspect the param-query mapping first
```r
library(gcamextractor)

gcamextractor::params
gcamextractor::queries
gcamextractor::map_param_query
```

### Download example data and run
```r
library(gcamextractor)

path <- gcamextractor::get_example_data(
  data_link = "https://zenodo.org/record/XXXX/files/example.zip"
)
```

### Use GDP deflator for price conversion
```r
library(gcamextractor)

# Convert 1990 dollars to 2015 dollars
deflator <- gcamextractor::gdp_deflator(year = 2015, base_year = 1990)
price_2015 <- price_1990 * deflator
```

---

## Failure and Edge Cases
- **invalid `paramsSelect`**: source prints available params via `map_param_query` then stops with `"None of the parameters in paramsSelect ... are available."`
- **missing `gcamdatabase` path**: source stops if the provided database directory does not exist
- **missing `gcamdata_folder`**: source warns `"gcamdata_folder provided: ... does not exist."` and skips params that require gcamdata
- **`queryFile=NULL`**: If `queryFile=NULL`, the package writes bundled `queries_xml` to `folder/queries.xml`
- **region naming**: the source normalizes `"United States"` to `"USA"`; US state abbreviations are mapped to `"USA"` region in aggregation
- **no data returned**: if the selected regions/params/queries produce zero rows, returns a warning `"No data extracted for chosen arguments."` instead of a list
- **cerf/go params auto-add pop**: when any of `elec_lifetime_scurve_yr`, `elec_lifetime_yr`, `elec_fuel_co2_content_tonsperMBTU`, `elec_carbon_capture_rate_fraction`, `elec_carbon_capture_escl_rate_fraction` is selected, `"pop"` is automatically prepended to `paramsSelect`

---

## Practical Agent Rules
- Start with `map_param_query` when the user asks what a parameter really means.
- Prefer `.Proj` reuse for repeated analytic work.
- Treat the current source signature as authoritative when the vignette, README, and generated `man/*.Rd` pages disagree. Note that source and generated docs are slightly out of sync: the current R source includes `removeVintages=F` in `readgcam` but the generated Rd files omit it.
- The `diagnostic` group is a good starting point for users who want a quick cross-domain overview.
- Energy params exist in three unit variants (EJ, MTOE, TWh) but only EJ is fully implemented in current source; MTOE/TWh conversion code is commented out.
- If the user needs raw GCAM-native query parity rather than standardized tables, fall back to `query_automation.md` or `tools.md`.

---

## Authoring Basis
- `gcamextractor/R/readgcam.R` -- main function, all paramx implementations, full signature
- `gcamextractor/R/data.R` -- all exported dataset documentation
- `gcamextractor/R/get_example_data.R` -- get_example_data function
- `gcamextractor/R/gdp_deflator.R` -- gdp_deflator function
- `gcamextractor/NAMESPACE` -- export list (readgcam, get_example_data, gdp_deflator)
- `gcamextractor/inst/extdata/saveDataFiles.R` -- map_param_query definition, all group/param/query/gcamdata mappings
- `gcamextractor/man/readgcam.Rd`
- `gcamextractor/man/queries_xml.Rd`
- `gcamextractor/man/params.Rd`
- `gcamextractor/man/queries.Rd`
- `gcamextractor/man/map_param_query.Rd`
- `gcamextractor/vignettes/vignette_readgcam.Rmd`
- `gcamextractor/vignettes/vignette_parameters.Rmd`
