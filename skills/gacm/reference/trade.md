# Trade

Skill-bundled topic reference for international and interstate trade modeling in GCAM.

Use this file after version routing when the user asks about trade modes, Armington parameters, commodity trade assumptions, or GCAM-USA interstate electricity/refining trade.

## Three Trade Modes

| Mode | Market clearing | Price visibility | Used for |
|---|---|---|---|
| **Heckscher-Ohlin (H-O)** | Single global market | One world price, all regions | Coal, oil, gas, uranium, bioenergy, FodderHerb |
| **Armington** | Segmented regional markets | Region-specific prices; gross trade tracked | Most crops, livestock, forest, ammonia (v7.1+) |
| **Fixed Trade** | Historical volumes held constant | N/A | Legacy livestock trade (pre-v5.4); FodderGrass is not traded |

Secondary energy goods (electricity, refined liquids, hydrogen) are **not traded** between GCAM geopolitical regions.

## Heckscher-Ohlin
Products are homogeneous; markets clear at the world level; every region faces the same price and independently decides supply and demand. Net trade is endogenous (economics, technology, resources, demand). No bilateral preference.

## Armington Style Trade
Products are differentiated by origin; domestic and imported goods are imperfect substitutes (Armington 1969). Two nested logit layers:
1. **Global "traded commodity"** pool -- supplied by gross exports from every region, logit over exporter shares.
2. **"Regional commodity"** sector -- allocates share between domestic production and imports, logit over domestic vs. import.

This creates segmented regional markets with region-specific prices and gross trade tracking.

### Armington Logit Parameters
The "rule of two" (Liu et al. 2004): the international logit exponent equals exactly twice the regional exponent, reflecting that cross-border substitution is harder than domestic-vs-import switching.

| Sector | Regional | International |
|---|---|---|
| Corn | -1.3 | -2.6 |
| Fibercrop | -2.5 | -5.0 |
| Fruits | -2.41 | -4.82 |
| Legumes | -2.41 | -4.82 |
| Misccrop | -2.41 | -4.82 |
| NutsSeeds | -2.41 | -4.82 |
| OilCrop | -2.99 | -5.98 |
| OilPalm | -2.99 | -5.98 |
| Othergrain | -1.3 | -2.6 |
| Rice | -2.9 | -5.8 |
| Roottuber | -2.41 | -4.82 |
| Soybean | -2.99 | -5.98 |
| Sugarcrop | -2.7 | -5.4 |
| Vegetables | -2.41 | -4.82 |
| Wheat | -4.45 | -8.9 |
| Beef | -3.9 | -7.7 |
| Dairy | -3.7 | -7.3 |
| Pork | -4.4 | -8.8 |
| Poultry | -4.4 | -8.8 |
| Sheep & Goat | -3.9 | -7.7 |
| Forest | -2.5 | -5.0 |

Livestock products have generally higher (more negative) exponents than crops (Hertel et al. 2007).

## Commodity Coverage
- **Energy (H-O global market)**: coal, oil, gas, uranium, bioenergy. See `energy_system.md`.
- **Agriculture & forestry (Armington, v5.4+)**: all crops/livestock/forest in the table above. Exceptions: FodderHerb (H-O), FodderGrass (not traded), Fish & Other Meats (excluded).
- **Ammonia (v7.1+)**: Armington-like, calibrated on **net** trade flows (gross data unavailable). Bridges energy and agriculture -- feedstocks become NH3, then N fertilizer for crop production. CCS-equipped production technologies available.
- Trade outputs are inferred from production vs. consumption via domestic/import splits and traded-sector queries.

## Interstate Trade -- GCAM-USA
- **Electricity**: states within the same NERC-based grid region (~15 regions) trade freely; inter-grid-region trade is driven by economic competition, calibrated from EIA net-trade data disaggregated to gross flows via PCA-level data.
- **Refined liquids**: state-level refining sectors compete via a logit at the USA-region level.
- Infrastructure is assumed available, which can produce faster trade shifts than historically observed. Results are most reliable at grid-region or national aggregation.

## Version Evolution

| Version | Trade change |
|---|---|
| v4.x | Agriculture mostly H-O; livestock fixed trade |
| v5.2 | Armington introduced for primary crops; livestock still fixed |
| v5.4 | Armington extended to livestock and forestry with full parameter table |
| v7.1 | Ammonia trade added (Armington, net-flow calibration) |
| v8.2 | Current baseline; same structure as v5.4+ with continued refinement |

## IAMC Reference Card
Traded: Coal, Oil, Gas, Uranium, Bioenergy crops, Food crops, Emissions permits. Not traded: Electricity, Capital, Non-energy goods.

## Authoring Basis
- Primary: `gcam-doc/details_trade.md` (v8.2 root), `version_pages/v8.2/details_trade.md`
- Ammonia: `gcam-doc/demand_energy.md` L160-174; GCAM-USA: `gcam-doc/gcam-usa.md` L136-155
- Cross-refs: `energy_system.md`, `inputs_outputs.md`, `choice_marketplace.md`
- v5.2 baseline comparison: `gcam-doc/v5.2/trade.md`
- Zhao et al. (2022) for Armington derivation and validation
