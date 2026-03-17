# Emissions and Climate

Skill-bundled topic reference for CO2/non-CO2 emissions, MAC curves, Hector coupling, and climate-target interpretation.
Use after version routing when the user asks about emissions coefficients, GWP aggregation, linked GHG markets, air pollutants, climate constraints, or Hector outputs.

---

## 1 Tracked Species

| Category | Species |
|---|---|
| CO2 | Fossil-fuel & industrial CO2, cement CO2, fugitive CO2 (flaring/extraction), land-use change CO2 (CO2_LUC) |
| Non-CO2 GHGs | CH4, N2O |
| Fluorinated gases | CF4, C2F6, SF6, HFC23, HFC32, HFC43-10mee, HFC125, HFC134a, HFC143a, HFC152a, HFC227ea, HFC236fa, HFC245fa, HFC365mfc |
| Air pollutants | SO2 (4 metaregions: SO2_1..SO2_4), NOx, BC, OC, CO, VOCs (NMVOC), NH3 |

Agricultural emissions carry suffixes: base name, `_AGR`, `_AWB`. Sum all three for totals (e.g., CH4 + CH4_AGR + CH4_AWB).

## 2 CO2 Emission Calculation

**Fossil & industrial**: CO2 = fuel_consumption x global_carbon_coefficient_by_fuel (oil, unconventional oil, gas, coal; calibrated to CDIAC). CCS is an explicit technology option; the model endogenously produces a CO2 MAC as carbon prices rise.

**Cement**: one global EF for limestone; regional IO coefficients (limestone/cement) calibrated to CDIAC.

**Fugitive CO2**: flaring/extraction initialized from CEDS, modeled via the non-CO2 approach. Unconventional oil uses IPCC 2019 EFs.

**Land-use change (LULCC)**: tracked separately via land module carbon accounting.

## 3 Non-CO2 GHG Emissions and MAC Curves

For any technology in period t: `E_t = A_t * F_t0 * (1 - MAC(Eprice_t))`

- `A` = activity level; `F` = base-year emission factor; `MAC` = piece-wise linear curve (EPA 2019); `Eprice` = emissions price (default: CO2 price).

| XML Tag | Role | Default |
|---|---|---|
| `tech-change` | Annual rightward shift of MAC | Backward-calc from EPA 2019 (2030-2050); post-2050 = avg pre-2050 |
| `mac-phase-in-time` | Ramp-in years for MAC reductions | 25 |
| `no-zero-cost-reductions` | 1 disables below-zero MAC mitigation | 0 |
| `market-name` | Price source market | "CO2" |
| `mac-price-conversion` | Price unit multiplier; -1 disables MAC | 1 |
| `zero-cost-phase-in-time` | Phase-in years for below-zero reductions | 25 |

Tech-change: `R(t2,p) = R(t1,p) * (1 + TC)^(t2-t1)`. Below-zero MAC applies in reference case, phased in over decades, unaffected by `tech-change`.

**Fluorinated gases**: most scale with industrial output, population, or GDP. SF6 scales with electricity; HFC134a (cooling) with AC electricity. Developing regions get exogenous future EF adjustments (CFC-to-HFC transition). EPA MAC curves provide abatement.

## 4 Air Pollutant Emissions

`E_t = A_t * EF_t0 * (1 - EmCtrl(pcGDP_t))` where `EmCtrl = 1 - 1/(1 + (pcGDP - pcGDP_t0)/steepness)`.

`steepness` is exogenous per technology/species, capturing income-driven control deployment. SSP scenarios used region/sector/fuel-specific EF pathways instead. Outlier EFs (>2 SD above or >3 SD below median) replaced with global median (GCAM) or national median (GCAM-USA).

## 5 GWP and Total GHG Aggregation

Non-CO2 gases convert to CO2-eq via GWP multipliers carried in the `demand-adjust` parameter of `linked-ghg-policy`. AR4 vs AR5 GWP choice affects weighting; users must ensure consistency between GWP set and `price-adjust`/`demand-adjust` values in policy XML.

## 6 Linked Markets and Policy Approaches

**Three policy modes**: (1) Carbon/GHG price -- user specifies price, emissions endogenous. (2) Emissions constraint -- user specifies cap, GCAM solves for price. (3) Climate constraint -- user specifies concentration/forcing/temperature target (overshoot optional), GCAM iterates for least-cost path (much slower).

**Linked GHG policy** (`linked-ghg-policy`): links non-CO2 to CO2 market. `price-adjust` = price conversion (0 = no economic feedback, MAC still uses CO2 price). `demand-adjust` = quantity conversion (GWP-based). Separately configurable for CH4, CH4_AGR, CH4_AWB, CO2_LUC. A `<ghgpolicy>` must load before any linked policy referencing it.

## 7 Hector Climate Module

Hector v3.2.0: default reduced-form C++ climate/carbon-cycle model. Architecture: 1-pool atmosphere, 3-pool land (vegetation/detritus/soil), 4-pool ocean. Solves ocean inorganic carbon for air-sea CO2 flux and pH.

**Coupling**: each period GCAM passes all species (Section 1) to Hector. Hector returns:
- **Atmosphere**: temperature (absolute & relative to 1850-1900), concentrations, total & per-species radiative forcing.
- **Land**: NBP, NPP, RH, carbon pools.
- **Ocean**: uptake, pool stocks, carbonate chemistry (DIC, pCO2, CO3^2-, pH, saturation states), SST, heat flux.

Carbon balance: `dC_atm/dt = F_A(t) + F_LC(t) - F_O(t) - F_L(t)`.

**Constraints**: Hector accepts user-provided CO2 concentrations, total forcing, or temperature (data-mode override), enabling climate-target runs.

**Configuration**: default single land biome; optional multi-biome. Many tunable parameters (see online Hector manual).

## 8 Emissions Control Options

- **NSPS**: drop CSV files into emissions control folder; data system generates XML overriding EFs for new vintages.
- **Retrofits**: linear-control objects ramp down EFs from start to end year for existing vintages.
- **linear-control**: `end-year`, `start-year` (opt, default=final calib year), `final-emissions-coefficient`, `allow-ef-increase` (default false).
- Target by region, meta-region, or all; trigger at year or pcGDP threshold. GDP control auto-removed when NSPS/retrofit specified.

## 9 IAMC Reference Cards

**GHGs**: CO2 (fossil, cement, land use), CH4, N2O (each: energy/land use/other), CFCs, HFCs, SF6, PFCs.
**Pollutants**: CO, NOx, VOC, SO2, BC, OC, NH3 (each: energy/land use/other).
**CDR**: BECCS, reforestation, afforestation, DAC. Not modeled: soil carbon enhancement, enhanced weathering.
**Climate** (Hector): concentrations (CO2, CH4, N2O), forcing (CO2, CH4, N2O, F-gases, Kyoto, aerosols, land albedo, total), temperature, ocean acidification. Not modeled: sea level rise.

## 10 Data Sources

| Source | Coverage |
|---|---|
| CEDS (Hoesly et al. 2018) | Non-CO2 GHGs & air pollutants, 1970-2019 |
| CDIAC (2017) | Global fossil-fuel & cement CO2 |
| GFED LULC (CMIP6) | Grasslands, forest fires, deforestation, AWB |
| GAINS (IIASA) | Road-transport mode-specific EFs |
| EPA 2019 | F-gas projections, non-CO2 MAC curves |
| IPCC 2019 | Unconventional oil fugitive EFs |

## 11 Version Notes

- v7.0 and earlier: MAGICC climate model; v7.1+: Hector default.
- v8.2: Hector v3.2.0 with permafrost module (CO2 + CH4; Woodard et al. 2021).
- Non-CO2 MACs updated to EPA 2019 + backward-calculated `tech-change` (Ou et al. 2021) from v7.0.
- CEDS coverage extended to 2019 in recent builds; earlier versions used shorter windows.
- SSP pollutant pathway approach differs from default GDP-steepness method.
- CEDS-GCAM calibration-year gaps: protected-land deforestation zeroed; 5-year deforestation coefficient averaging.

---

## Authoring Basis

- Primary: `gcam-doc/emissions.md`, `gcam-doc/details_emissions.md`, `gcam-doc/hector.md` (all v8.2).
- Mirrors: `version_pages/v8.2/emissions.md`, `version_pages/v8.2/hector.md`.
- Key refs: Ou et al. 2021, EPA 2019, Hoesly et al. 2018, Hartin et al. 2015, Dorheim et al. (in press), Woodard et al. 2021, CDIAC 2017, IPCC 2019.
