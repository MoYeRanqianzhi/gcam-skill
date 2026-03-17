# Economy

Skill-bundled topic reference for socioeconomic drivers, GDP formation, GCAM-macro, and economic interpretation.

Use this file after version routing when the user asks about GDP assumptions, macro coupling, savings, SAM consistency, income elasticity, or how economic activity feeds other GCAM modules. For version-specific equations and tables, load the appropriate `version_pages/<ver>/economy.md`.

If the user asks about endogenous GDP or macro feedbacks, version routing is mandatory. `v7+` is the key modern macro era in the bundled references.

## Core Role

The economy block sets the scale of demand throughout GCAM. Population and GDP together drive energy, agriculture, and land-use demands across 32 geo-political regions.

**Required exogenous inputs (per region and year):**

| Input | Unit | Source |
|:------|:-----|:-------|
| Population | thousands | Maddison (1700-1900), UN (1950-2015), SSP database (2015-2100) |
| Labor productivity growth rate | unitless | Exogenous assumption |
| Labor force participation rate | unitless | Exogenous assumption |
| Base-year GDP | million 1990$ | USDA (MER), FAOSTAT, SSP database (PPP) |
| Base-year national accounts | million 1990$ | Penn World Table v9.1, GTAP v10 |

## GDP Formation: Exogenous vs Endogenous

**Exogenous GDP (legacy, pre-v7).** GDP is prescribed externally from SSP or other scenario pathways. A simple scalar feedback elasticity optionally adjusted GDP for energy-cost changes, but the coupling was one-way: energy prices did not structurally alter GDP.

**Endogenous GDP via GCAM-macro (v7+).** GCAM incorporates a macroeconomic module creating two-way coupling between economic output and the energy system. Energy-system costs feed back into GDP, consumption, and investment. This is the default mode from v7 onward ("open GDP mode").

## KLEM Production Function

GCAM-macro represents GDP production through a nested CES (Constant Elasticity of Substitution) structure over four factors -- Capital (K), Labor (L), Energy (E), and Materials (M):

```
Materials output X_M = F_M(X_K, X_L, X_E)

Nested CES:
  X_M = [ a * (b * X_L^eta + X_K^eta)^(rho/eta) + c * X_E^rho ]^(1/rho)
```

- The inner nest combines Labor and Capital with elasticity parameter eta.
- The outer nest combines the KL composite with Energy using elasticity parameter rho.
- The Materials sector (M) is the sole retailer of final goods and services to the economy and the sole consumer of final energy output.

**GDP for a region:**
```
GDP = P_M * F_M(X_K, X_L, X_E) + NX_E + X_I,M
```
where NX_E is net energy exports and X_I,M is the net balance of trade.

## Population and Labor Productivity

Population is exogenous (Maddison pre-1900, UN 1950-2015, SSP database 2015-2100), aggregated to 32 regions. Effective labor input: `X_L,M = L_M * h_L(t)` where h_L(t) is an exogenous labor productivity scalar. All labor is assumed employed by the Materials sector. For any target GDP pathway, total factor productivity values can be back-calculated to reproduce it (SSP calibration).

## Capital Accumulation and Savings

Capital stock evolves via: `X_K,M(t) = (1 - lambda) * X_K,M(t-1) + X_I,M`. Savings is a function of GDP distributed across materials investment, energy investment, and net international capital flows: `S = X_I,M + X_I,E + NX_K`. Future savings rates are projected via regression on historical per-capita GDP. Depreciation rates are held at historical values. Energy capital uses a putty-clay representation (irreversible once deployed, retired only if operating costs exceed revenue).

## SAM (Social Accounting Matrix) Calibration

The SAM is a double-entry bookkeeping framework ensuring macroeconomic consistency. Key properties:

- Every row sum must equal its corresponding column sum; violation indicates a failed solve.
- GDP can be computed as final expenditure (C + I + G + net exports) or as factor payments (K + L).
- Savings-investment identity: S + NX = I.
- Net exports across all regions sum to zero for energy, capital, and materials.
- Energy-consuming consumer durables (cars, appliances) are included in the capital account.
- Net international financial transfers are inherited from historical data and configured to phase out by 2035.

Historical calibration uses Penn World Tables (national accounts) and GTAP v10 (sectoral value-added and I-O tables), aggregated to GCAM's 32 regions. Energy-service expenditures are derived from calibrated GCAM energy quantities and endogenous service prices.

## Income Elasticity and Demand Linkages

GDP per capita and population jointly drive demand for energy services, food, and other goods through income-elastic demand functions in downstream modules. Changes in GDP under GCAM-macro propagate to all demand sectors, creating general-equilibrium-like feedback even though GCAM is a partial-equilibrium model at its core.

## Regional Economic Structure

GCAM partitions the world into 32 geo-political regions. Each region has its own:
- Population and labor force trajectory
- National accounts and SAM
- Savings and depreciation parameters
- Trade linkages (net exports of energy, capital, materials must sum to zero globally)

## Carbon Price Feedback on the Economy

With GCAM-macro enabled, a carbon price directly affects energy costs, which feed back into Materials-sector production and thus GDP. The model can report:
- **GDP change** -- macroeconomic measure of overall activity impact
- **Consumption change** -- welfare-relevant measure
- **Deadweight loss** -- bottom-up, technology-switch cost (legacy method, still available)

These are distinct metrics and should not be conflated. The macro module also captures non-carbon perturbations (regulatory, water, climate shocks) without ad-hoc post-processing.

## Price Index and GDP Deflator

All monetary values in the economic module are expressed in constant 1990 US dollars. The Materials-sector price P_M is normalized to 1. Factor prices (P_K, P_L, P_E) are derived as marginal products of the CES function. Cross-scenario comparisons should use the same deflator base year to avoid spurious differences.

## Version Differences

| Version | GDP Mode | Macro Coupling |
|:--------|:---------|:---------------|
| v5 and earlier | Exogenous only | One-way (GDP drives energy demand) |
| v5.x-v6.x | Exogenous with optional scalar feedback | One-way with simple elasticity adjustment |
| **v7** | Endogenous (open GDP mode, default) | Two-way via GCAM-macro KLEM module |
| **v7.1-v8.2** | Endogenous (refined) | Two-way; improved SAM calibration; SSP 2024 database |

Key code: [`national_account.cpp`](https://github.com/JGCRI/gcam-core/blob/master/cvs/objects/containers/source/national_account.cpp)

## Authoring Basis

- Primary source: `gcam-doc/economy.md` (v8.2 tagged), `gcam-doc/inputs_economy.md`
- Version page: `version_pages/v8.2/economy.md`, `version_pages/v8.2/inputs_economy.md`
- Key references: Edmonds & Reilly 1983/1985; Hogan & Manne 1978; Feenstra et al. 2015 (PWT); Aguiar et al. 2019 (GTAP v10); IEA Energy Balances 2023; SSP Database (IIASA)
- Bundled: 2026-03-17
