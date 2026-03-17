# Land System

Reference for GCAM Agriculture and Land Use (AgLU): land allocation, terrestrial carbon, crop/livestock supply, bioenergy, forest management, and land-side policy mechanisms.

Load this file when the user asks about GLUs, crop competition, land nesting, land carbon, afforestation, bioenergy land pressure, Moirai data, or land-use change emissions.

---

## 1 AgLU Framework Overview

GCAM's land module couples economic land competition with terrestrial carbon accounting. Land allocation is profit-driven: each land use (crop, pasture, forest, biomass, unmanaged) competes for area within a hierarchical nesting tree. The resulting area changes feed carbon-stock calculations that produce LUC CO2 emissions over time.

Key inputs per GLU and land type: historical land cover (thous km2), vegetation and soil carbon density (kg/m2), mature age (yr), soil time scale (yr), unmanaged land value, managed land profit (from supply module), and logit exponents.

## 2 Land Allocation -- Nested Logit

### 2.1 Sharing equation

Share of leaf or node i: `s_i = (lambda_i * pi_i)^rho / SUM_j (lambda_j * pi_j)^rho`, where lambda is the calibrated profit scaler, pi is profit, rho is the logit exponent. Node profit aggregates upward with the same CES form.

### 2.2 Nesting structure

The tree descends: **All Land -> Agro-forestry vs Non-agricultural -> Non-pasture vs Pasture -> {Forest, Cropland, Shrub/Grass}**. Under Forest: managed forest, unmanaged forest, woody biomass. Under Cropland: each commodity splits into irrigated/rainfed x high/low fertilizer leaves, plus "other arable land" (fallow). Dedicated herbaceous energy crops enter in 2025. Higher logit exponents within a node mean tighter substitution (e.g., crop-to-crop easier than crop-to-forest). Zero exponents lock land (desert, tundra).

### 2.3 Calibration

The share equation is inverted in the final historical period to solve for lambda_i (profit scalers) that reproduce observed land shares given observed profits and unmanaged land values. These scalers persist into future periods; if profits are unchanged, future shares equal base-year shares.

### 2.4 Intensification

Multiple management types per crop enable price-induced intensification. As high-yield options (more fertilizer, irrigation) become more profitable, their share rises and average yield increases. Yields can also decline if input costs rise or commodity prices fall.

## 3 Geographic Land Units (GLUs)

GLUs are the intersection of geopolitical regions and agro-ecological zones (land-use region x water basin). All land competition, carbon density, and yield data are resolved at the GLU level. The number of GLUs depends on the region/basin mapping used by the data system.

## 4 Moirai Land Data System

`moirai` preprocesses gridded inputs into GLU-level tables consumed by `gcamdata`. Key data flows:

- **Soil carbon**: SoilGrids (top 0-30 cm, Hengl et al. 2017), aggregated to GLU x land-type with 6 statistical states (min, q1, median, weighted_average, q3, max). Default = `q3_value` (best proxy for steady-state density).
- **Vegetation carbon**: above + below ground biomass (Spawn et al. 2020), same 6 states.
- User selects state via `aglu.CARBON_STATE` in `constants.R`; can switch source to Houghton (1999) via `aglu.CARBON_DATA_SOURCE`.
- Land suitability (Zabel et al. 2014) and IUCN protection status determine 7 mutually exclusive land categories; `aglu.NONPROTECT_LAND_STATUS` controls which are available for expansion.

## 5 Carbon Accounting

### 5.1 Cumulative emission identity

`E_t = A_t * D_t - A_{t-1} * D_{t-1}` for both vegetation and soil, where A = area, D = carbon density.

### 5.2 Vegetation (above-ground) carbon

- **Contraction** (E > 0): all carbon emitted instantaneously in the conversion period.
- **Expansion** (E < 0): uptake spread over time via a Bertalanffy-Richards sigmoid parameterized by **mature age** M (1 yr for crops, 30-100 yr for forests). Implementation: `precalc_sigmoid_helper` in `land_carbon_densities.cpp`.

### 5.3 Soil (below-ground) carbon

Both emission and uptake follow an exponential decay: half-life = `soil_time_scale / 10 * ln(2)`. Colder regions have longer half-lives. Implementation: `calcBelowGroundCarbonEmission` in `asimple_carbon_calc.cpp`.

### 5.4 Carbon stock tracking

`C_y = C_{y-1} - (E_veg_{y-1} + E_soil_{y-1})`. Stocks are updated annually by subtracting realized emissions and adding realized uptake.

## 6 Bioenergy

Dedicated biomass (herbaceous and woody) enters the land nest from 2025. A graded renewable-resource cost curve (`A27.GrdRenewRsrcCurves.csv`) adds an externality cost that rises with production scale. Two default constraints limit bioenergy: (1) a negative-emissions GDP budget (`energy.NEG_EMISS_GDP_BUDGET_PCT`) that scales back subsidies, and (2) the biomass externality cost curve. Users may also impose explicit upper/lower bounds; GCAM then solves for the required tax/subsidy.

## 7 Forest Management

The forest node contains **managed forest** (industrial roundwood, residues) and **unmanaged forest**. Woody biomass competes in the same node. Land expansion cost curves can be applied to unmanaged forest to represent planting/fire-management costs and prevent unrealistic afforestation surges under carbon pricing. A "carbon park" technology (dense tree planting purely for carbon storage) exists in the code but is not enabled in the core configuration.

## 8 Agricultural Technology and Yield

Future yield: `yield_t = yield_{t-1} * (1 + APG)^timestep`, where APG is the exogenous agricultural productivity growth rate. Profit rate: `profitRate = 1e9 * (price + subsidy - varCost - inputCosts + secondaryValue) * yield + impliedSubsidy`. Variable costs exclude land rent, value-added, and owner-wages; they create hard price floors. Fertilizer and water costs are modeled explicitly with IO coefficients and market prices.

## 9 Livestock Modeling

Livestock subsectors represent production systems; technologies represent feed sources. Feed shares use either a relative-cost logit (`s_i = alpha_i * c_i^gamma / SUM`) or absolute-cost logit (`s_i = alpha_i * exp(beta*c_i) / SUM`). Feed demand scales with total livestock demand. A nested logit in the demand module separates staples vs non-staples food; income growth shifts diets toward non-staples (meat, dairy). Agricultural storage (from v8.x) models stockholding with a logit between current consumption and carryover stock.

## 10 Land-Use Change Emissions

Total LUC CO2 = vegetation emissions + soil emissions, allocated over time per Sections 5.2-5.3. Valuing carbon in land (subsidy = carbon price x density x discount) shifts allocation toward high-carbon ecosystems. Since v7.1, a minimum soil-carbon-density threshold (`Min_Soil_C_at_Cropland`) prevents crediting low-density conversions.

## 11 Policy Levers

| Lever | Mechanism | Key parameter / file |
|---|---|---|
| Land protection | Fix area, remove from competition | `aglu.PROTECT_DEFAULT`, `aglu.NONPROTECT_LAND_STATUS` |
| Carbon pricing on land | Subsidy for holding C stocks | `global_uct.xml`, region-level multiplier |
| Bioenergy bounds | Tax/subsidy to meet constraint | `A27.GrdRenewRsrcCurves.csv`, `NEG_EMISS_GDP_BUDGET_PCT` |
| Land expansion cost | Renewable-resource cost curve on target type | Per-region XML add-on |
| Carbon parks | Managed dense-planting technology | Input file modification (not core default) |
| Diet / food preference | SSP-specific preference elasticities | Food demand parameters |

## 12 Version Evolution

| Era | Key changes |
|---|---|
| v3.x-v4.3 | Early AgLU; single-level or shallow nesting; Houghton carbon densities; no explicit GLU framing |
| v4.4 | Default bioenergy constraint via negative-emissions budget introduced |
| v5.x | Transition to modern GLU-oriented architecture; Moirai data pipeline; deep nesting with irrigated/rainfed x hi/lo management |
| v7.1 | AgLU parameter update (Zhao et al. 2024); min soil-C threshold for land carbon policy; forestry detail improvements |
| v8.x | Food demand model update (Edmonds et al. 2017 integration); agricultural storage/stockholding; updated suitability-protection land categories; Moirai uses SoilGrids + Spawn vegetation data |

---

### Authoring Basis

- `gcam-doc/land.md` (v8.2) -- allocation logic, equations, policy options, carbon approach
- `gcam-doc/details_land.md` (v8.2) -- nesting strategy, calibration detail, comparative advantage, LUC emissions
- `gcam-doc/supply_land.md` (v8.2) -- profit rate, yield, variable cost, livestock production
- `gcam-doc/demand_land.md` (v8.2) -- food/feed/forest demand, storage
- `skills/gacm/reference/version_pages/v8.2/land.md` -- version-bundled page
- Cross-referenced: Wise et al. 2014, Calvin et al. 2014/2017, Zhao et al. 2020/2024, Snyder et al. 2017, Edmonds et al. 2017
