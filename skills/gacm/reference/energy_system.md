# Energy System

Topic reference for GCAM energy resources, transformation, demand sectors, technology competition, and trade. Load this file when the user asks about electricity, fuels, hydrogen, renewables, CCS, resource curves, energy demand, or energy trade.

---

## 1 Primary Resources

### 1.1 Depletable (Fossil & Uranium)
- **Commodities:** oil, unconventional oil, natural gas, coal, uranium.
- Graded supply curves + Resource/Reserve extraction model; technical change reduces cost over time.
- Unconventional oil is a distinct sub-resource within crude oil, sharing one price but carrying extra cost/energy inputs.

### 1.2 Renewable
- **Wind** (onshore & offshore): regional supply curves (EJ elec/yr vs 1975$/GJ); not traded inter-regionally.
- **Solar:** "global solar resource" (unlimited) + "distributed_PV" (upward-sloping, scaled by floorspace). CSP depends on DNI.
- **Geothermal:** graded annual-flow curves; ~10 % thermo-electric efficiency. EGS available as optional XML.
- **Hydropower:** exogenous fixedOutput; does not affect modeled electricity price.
- **Biomass:** waste/residue curve grows with GDP (`gdpSupplyElast`). `v7.1` updates residual biomass (Hanssen et al. 2020).
- **Traditional biomass:** residential only in selected regions; not linked to land-use module.

Renewable curve: `Q = maxSubResource * P^curveExp / (midPrice^curveExp + P^curveExp)`

---

## 2 Energy Transformation

### 2.1 Electricity
Technologies compete via logit on levelized cost = non-energy cost + fuel cost + emissions value.

| Category | Technologies |
|---|---|
| Coal | conv. pulverized, IGCC, each +/- CCS |
| Gas | combined cycle, combustion turbine, each +/- CCS |
| Oil | steam, combustion turbine, +/- CCS |
| Bioenergy | dedicated, IGCC, each +/- CCS |
| Nuclear | Gen III/III+ |
| Wind | onshore, offshore |
| Solar | central PV, distributed PV, CSP |
| Geothermal | hydrothermal (EGS optional) |
| Hydro | fixedOutput |

- **Capacity factor** & **variable O&M** read per tech; capital amortized via fixed-charge-rate.
- **Load segments** (`v5.4+`): demand split into segments for dispatch-order and value differences.
- **Intermittent integration** (`v7.3+`): backup requirement rises with intermittent share via sigmoidal `capacity-limit` curve. Params: `backup-capacity-factor`, `backup-capital-cost`, `capacity-limit`.
- Cooling-system nest (up to 5 types) determines water withdrawal/consumption.

### 2.2 Refining (Liquid Fuels)
Single "refined liquids" product. Four subsectors, capital stocks tracked:

| Subsector | CCS | Notes |
|---|---|---|
| Oil refining | none | inputs: crude oil, gas, electricity |
| Biomass liquids | 2 levels (2nd-gen) | 11 global techs (1st-gen crops + cellulosic ethanol + FT biofuels) |
| Coal to liquids | 2 levels | ~130 kg CO2/GJ vs ~5.5 for oil refining |
| Gas to liquids | none | ~60 % efficiency, ~20 kg CO2/GJ |

### 2.3 Gas Processing
- **Natural gas**, **coal gasification**, **biomass gasification** compete upstream of pipeline.
- Downstream: pipeline -> delivered gas (buildings, transport) / wholesale gas (industry, energy).
- `v7.3+`: pipeline (6 regional networks) vs LNG (global) trade differentiation.

### 2.4 District Services
Modeled only where purchased heat is significant. Four techs (coal, gas, oil, biomass heat); CHP in industry sector.

### 2.5 Hydrogen (`v6.0+`)
10 central + 2 forecourt production technologies; distribution via pipeline or liquefied-truck.

| Pathway | CCS | Pathway | CCS |
|---|---|---|---|
| Coal gasification | yes | Nuclear thermochemical | no |
| Gas steam reforming | yes | Wind electrolysis (direct) | n/a |
| Oil gasification | yes | Solar electrolysis (direct) | n/a |
| Biomass gasification | yes | Grid electrolysis | n/a |

- Direct wind/solar electrolysis avoids grid backup costs and T&D markups.
- Distribution differentiates pressure/temperature states: dispensing (vehicles) vs delivery (stationary).
- `v7.1`: ammonia-trade linkages. `v8.0+`: refined H2A/HDSAM cost assumptions.

---

## 3 Energy Demand Sectors

### 3.1 Buildings
- **Residential:** income-decile disaggregation (`v8.0+`); floorspace via Gompertz function of income, density, region. Services: heating, cooling, other. Traditional fuels phase out with rising income.
- **Commercial:** satiation-demand floorspace (Eom et al. 2013); same three services.
- Thermal load: HDD/CDD, shell conductivity, internal gains from appliances.

### 3.2 Transportation
Four final demands: passenger air, other passenger, intl freight shipping, other freight. Nested by mode / sub-mode / size-class / drivetrain. Time-value-of-travel affects modal competition (passenger). Walking/cycling as non-motorized share.

### 3.3 Industry (9 sectors, `v7.0+`)

| Manufacturing | Non-manufacturing |
|---|---|
| Iron & Steel (BOF, EAF-scrap, EAF-DRI) | Construction (mobile + stationary) |
| Chemicals (energy + feedstocks) | Mining (mobile + stationary) |
| Aluminum (alumina refining + smelting) | Agricultural energy use |
| Cement (fuel + limestone CO2) | |
| N Fertilizer / Ammonia | |
| Food Processing | |

Remainder: "Other Industry" with generic energy-service competition and cogeneration.

---

## 4 CCS (Carbon Capture & Storage)
- Sectors: electricity, refining (biomass liquids, coal-to-liquids), gas processing, hydrogen, cement, iron & steel, chemicals, ammonia.
- Two levels: L1 captures high-purity streams (lower cost); L2 adds post-combustion (higher cost, higher removal). BECCS enables net-negative emissions. Captured CO2 tracked via `storage-market` per region.

## 5 Technology Competition (Logit Choice)
- **Relative-cost logit:** `s_i = alpha_i * c_i^gamma / sum(alpha_j * c_j^gamma)`
- **Absolute-cost logit:** `s_i = alpha_i * exp(beta*c_i) / sum(alpha_j * exp(beta*c_j))`
- Key levers: **share-weight** (0 = unavailable), **logit exponent**, **fuel-preference elasticity**. Profit-shutdown and s-curve-shutdown deciders govern vintage retirement.

## 6 Energy Trade
Armington approach for coal, oil, gas, bioenergy: domestic vs global product, region-specific prices. Gas: pipeline (6 regional networks) + LNG (global) (`v7.3+`). Renewables, electricity, hydrogen, refined liquids **not** traded inter-regionally.

---

## 7 Version Differences

| Feature | Since | Notes |
|---|---|---|
| Hydrogen as energy carrier | `v4.x` | Basic central production |
| Hydrogen expansion (10+2 techs, distribution states) | `v6.0+` | H2A/HDSAM cost basis |
| Load segments / dispatch | `v5.4+` | Value-differentiated electricity demand |
| Intermittent backup curve | `v7.3+` | Sigmoidal capacity-limit function |
| Residual biomass update | `v7.1` | Hanssen et al. 2020 |
| Ammonia trade | `v7.1` | Linked to N fertilizer & agriculture |
| Pipeline vs LNG gas trade | `v7.3+` | 6 regional pipeline networks |
| Detailed industry (9 sectors) | `v7.0+` | BOF/EAF, aluminum, cement, chemicals, food proc. |
| Income-decile residential | `v8.0+` | Gompertz floorspace, inequality capture |

---

## Authoring Basis
- Sources: `gcam-doc/supply_energy.md`, `demand_energy.md`, `details_energy.md`, `en_technologies.md` (v8.2).
- Cross-checked: `version_pages/v8.2/supply_energy.md`.
- Condensed for progressive-disclosure Level 3 reference.
