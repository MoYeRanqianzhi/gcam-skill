# Water System

Skill-bundled topic reference for water demand, supply, basin mapping, scarcity, and cooling-system competition in GCAM.

Use this file after version routing when the user asks about river basins, water withdrawals vs consumption, cooling technologies, groundwater, desalination, water markets, or the water-energy-food nexus. `v5.4+` is the closest structural family to the bundled modern water summary. Use the exact version route file when the user asks about a historical water feature or a release-specific update.

---

## Water Types (clarify first)

| Type | Definition | Applies to |
|------|-----------|------------|
| **Withdrawals** | Water diverted from a surface or groundwater source | All six demand sectors |
| **Consumption** | Withdrawn water that is not returned (evaporated, transpired, incorporated) | All six demand sectors |
| **Biophysical consumption** | Total crop ET (blue + green water); excludes conveyance/field losses | Agriculture only |
| **Seawater** | Ocean/brackish water used for power-plant cooling or primary energy | Electricity, primary energy |

Never treat these as interchangeable. Many GCAM questions become ambiguous when the user says only "water use" -- always confirm which type is intended.

## Water Demand Sectors

Six sectors drive freshwater demand. Each uses sector-specific coefficients, drivers, and spatial resolution.

| Sector | Key driver | Spatial resolution | Notes |
|--------|-----------|-------------------|-------|
| **Irrigation (agriculture)** | Crop production x water coeff (km3/Mt) | Basin-level (GLU) | Blue-water only for withdrawals/consumption; conveyance losses handled in distribution sector |
| **Electricity cooling** | Generation x cooling-tech coeff (km3/EJ) | Region, mapped to basin | See cooling technology detail below |
| **Industrial manufacturing** | Industrial output x coeff (km3/EJ) | Region, mapped to basin | Self-supplied only; excludes mining, on-site power cooling, and municipal piped water |
| **Livestock** | Animal production x coeff (m3/kg) | Region, mapped to basin | All withdrawals assumed consumed; coefficients constant over time |
| **Primary energy (mining)** | Fuel production x coeff (km3/EJ) | Region, mapped to basin | Coal, oil (conv + unconv), gas, uranium; seawater fraction deducted |
| **Municipal** | Population, GDP per capita, price, tech change | Region, mapped to basin | Grows via per-capita demand equation with income elasticity 0.37, price elasticity -0.33 |

Municipal per-capita demand equation: `pcW_t = pcW_{t-1} * (pcGDP_t/pcGDP_{t-1})^0.37 * (P_t/P_{t-1})^{-0.33} * (1 - Tech_t)`.

## Electricity Cooling Technologies

Up to five cooling options compete per thermo-electric generation technology via a calibrated logit nest:

| Cooling system | Withdrawal intensity | Consumption intensity | Availability |
|---------------|---------------------|----------------------|-------------|
| **Once-through (freshwater)** | Very high | Low | Most regions; dominant historically |
| **Recirculating (tower)** | Low | Moderate-high | Universal; gains share under scarcity |
| **Cooling pond** | Moderate | Moderate | Excluded in some regions/technologies due to data gaps |
| **Dry cooling** | Near zero | Near zero | Not available for current nuclear; efficiency penalty applies |
| **Once-through (seawater)** | Very high (seawater) | Low (seawater) | Coastal regions only; share assumed persistent |

Under rising water prices, regions shift from once-through to recirculating; dry cooling enters where freshwater cost exceeds its efficiency penalty. Capital costs from NETL 2008; water coefficients from Macknick et al. 2011. The cooling-system nesting uses pass-through sectors internally, but standard electricity queries aggregate them back.

## Basin Mapping

GCAM operates on **235 water basins** derived from global hydrographic data.

- **Irrigated agriculture**: demand computed directly at basin level (GLU); no additional mapping needed.
- **All other sectors**: demand computed at GCAM-region level, then allocated to basins via fixed mapping shares based on gridded population (municipal, industrial, livestock, primary energy) or power-plant locations (electricity).
- **Shared basins**: basins may span multiple GCAM regions (e.g., Great Lakes shared by US and Canada); all mapped regions can access the full basin supply. No upstream/downstream priority is modeled.
- **Limitation**: mappings are currently fixed over time -- no inter-basin transfers and no capture of intra-regional population or industry migration. Sub-national modules (GCAM-USA, GCAM-China) can improve this.

## Water Supply

### Renewable water
Surface runoff + groundwater recharge estimated by the Xanthos hydrological model at 0.5-degree resolution, aggregated per basin. Accessible volume accounts for environmental flow requirements, baseflow, and reservoir storage (~6,100 km3 globally from GRanD). Available at low cost up to the accessible fraction; sharply higher cost beyond that to protect ecosystems and reflect reservoir expansion costs. Climate-driven precipitation changes can shift accessible volume over time.

### Non-renewable groundwater
Modeled as a graded depletable resource per basin. Supply curves built from physics-based extraction cost models (well depth, geology, pumping energy). Recharge timescale >100 years. Detailed aquifer data (extent, thickness, porosity, depth-to-water) from global hydrogeological datasets. Groundwater depletion is tracked cumulatively. See Niazi et al. 2024/2025 (Superwell v1.1).

### Desalinated water
Available from brackish groundwater and seawater purification. High cost means it enters supply only when renewable + non-renewable sources are scarce. In core simulations, limited to municipal and industrial end-uses (configurable via input data). Competes within the water distribution sector alongside basin freshwater.

### Combined supply curve
Renewable and non-renewable sub-resource curves are overlaid into a single continuous supply curve per basin (235 markets total), ensuring smooth solution behavior. The overlapping design prevents discontinuities from depletion or climate shifts.

## Water Pricing and Scarcity

- Basin-level shadow prices are solved simultaneously with all other GCAM markets.
- When renewable supply is abundant, prices stay near zero and groundwater/desalination are unused.
- As demand approaches accessible renewable limits, prices rise, triggering: demand reduction, technology switching (e.g., dry cooling), crop trade shifts, and activation of non-renewable groundwater and desalination.
- **Agricultural water subsidy**: irrigation water priced at 5% of the general water price (`water.IRR_PRICE_SUBSIDY_MULT` in constants.R), reflecting OECD findings that agriculture pays >100x less than industrial/household users. Without this, historical calibration fails in water-scarce regions.
- Market clearing currently uses withdrawal volumes (not consumption); consumptive-volume pricing is possible but found to be under-responsive to scarcity.

## Water-Energy-Food Nexus

GCAM is one of the few IAMs that endogenously couples all three nexus dimensions:

- **Water for energy**: cooling water for electricity; water for fuel extraction; energy-for-water (pumping, desalination, treatment).
- **Water for food**: irrigation withdrawals; livestock water; virtual water embedded in agricultural trade.
- **Energy for water**: electricity/fuel consumed by water pumping, conveyance, treatment, and desalination -- modeled via energy inputs in the water distribution sectors (explicit from v5.4+; see Kyle et al. 2021).
- **Feedback loops**: water scarcity raises water prices, which raises electricity costs (via cooling), which raises irrigation pumping costs, which shifts crop production and trade patterns.

## Version Differences

| Feature | v5.4 | v6.0 | v7.0+ | v8.2 |
|---------|------|------|-------|------|
| Basin count | 235 | 235 | 235 | 235 |
| Renewable water equation (QA) | Simplified accessible fraction | Same | Explicit QA formula with EFR, baseflow, reservoir | Same as v7.0 with Zhao et al. 2024 reservoir update |
| Groundwater supply curves | Graded depletable | Same | Physics-based cost model (Superwell) | Superwell v1.1 (Niazi et al. 2025) |
| Desalination scope | Municipal + industrial | Same | Same | Same (configurable) |
| Energy-for-water | Basic | More explicit | Expanded | Full representation |
| Cooling technology data | Macknick 2011, NETL 2008 | Same | Same | Same |
| Water subsidy | 5% multiplier | Same | Same | Same |

Use the exact version-route page (e.g., `version_pages/v7.0/supply_water.md`) when the user needs release-specific detail.

---

### Authoring Basis

- Primary sources: `gcam-doc/demand_water.md` (v8.2), `gcam-doc/supply_water.md` (v8.2), `gcam-doc/details_water.md` (v8.2)
- Cross-checked against: `gcam-doc/v5.4/supply_water.md`, `gcam-doc/v7.0/supply_water.md`
- Key references: Kim et al. 2016, Hejazi et al. 2014, Davies et al. 2013, Macknick et al. 2011, Niazi et al. 2024/2025, Zhao et al. 2024, Kyle et al. 2021, Turner et al. 2019a/b, Graham et al. 2018
- Last updated: 2026-03-17
