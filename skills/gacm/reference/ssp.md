# Shared Socioeconomic Pathways (SSPs)

Agent reference for SSP scenarios in GCAM. Use this file after version routing. For full version-specific tables and input-file links, load `version_pages/<ver>/ssp.md`.

## Framework

SSPs are reference scenarios (no explicit GHG policy) defined on two axes: **challenges to mitigation** and **challenges to adaptation** (Riahi et al., 2017). Each can be paired with a radiative forcing target (2.6/4.5/6.0 W/m^2) plus Shared Policy Assumptions (SPAs) for use with CMIP6 climate experiments.

## SSP Narratives & Marker Models

| ID | Name | Narrative (one-liner) | Marker Model | Mitigation | Adaptation |
|----|------|-----------------------|--------------|------------|------------|
| SSP1 | Sustainability | Green growth, low inequality, rapid tech | IMAGE (PBL) | Low | Low |
| SSP2 | Middle of the Road | Historical trends continue | MESSAGE-GLOBIOM (IIASA) | Medium | Medium |
| SSP3 | Regional Rivalry | Fragmented world, slow tech, high pop | AIM/CGE (NIES) | High | High |
| SSP4 | Inequality | Highly unequal across/within countries | **GCAM (PNNL)** | Low | High |
| SSP5 | Fossil-fueled Dev. | Rapid growth via fossil energy | REMIND-MAgPIE (PIK) | High | Low |

> GCAM is the **marker model for SSP4**. GCAM also computed SSP1-3 and SSP5 as non-marker runs.

## Key Quantitative Assumptions (2100)

| Parameter | SSP1 | SSP2 | SSP3 | SSP4 (H/M/L income) | SSP5 |
|-----------|------|------|------|----------------------|------|
| Population | 6.9 B | 9.0 B | 12.7 B | 0.9/2.0/6.4 B | 7.4 B |
| GDP/cap (2005 USD) | $46,306 | $33,307 | $12,092 | $123k/$31k/$7.4k | $83,496 |
| Ag productivity | +50% vs default | Default | -50% vs default | +50/def/-50 | +50% |
| Renewables cost | ADV (low cost) | CORE | LOW (high cost) | ADV | CORE |
| Nuclear cost | LOW (high cost) | CORE | LOW (high cost) | ADV (low cost) | CORE |
| Fossil tech change | Med | Med | Med-High | Med-High | High |
| Trad. biomass phaseout | Fast (-2.5) | Med (-2.0) | Slow (-1.0) | Slowest (-0.75) | Fast (-2.5) |
| Pollutant EF | Low | Med | High | High | Low |

(ADV = advanced/cheaper; LOW = pessimistic/costlier; CORE = default)

## GCAM Implementation Details

SSP assumptions are injected via the **gcamdata R package** and XML add-on files. Modified input categories:

| Category | What changes | Key input files/chunks |
|----------|-------------|----------------------|
| Socioeconomics | Population, GDP per region | `SSP_database_v9.csv` (v7.2+: v3.0.1) |
| Electricity | Capital costs per plant type | `A23.globaltech_capital_adv.csv`, `A23.globaltech_capital_low.csv` |
| Fossil supply | Extraction tech-change rate + enviro cost adder | `A10.TechChange_SSPs.csv`, `A10.EnvironCost_SSPs.csv` |
| Buildings | Fuel preference elasticity for trad. bioenergy | `A44.fuelprefElasticity_SSP15.csv`, `_SSP3.csv`, `_SSP4.csv` |
| Transport | Mode costs, VOTT | `UCD_trn_data_SSP{1,2,3,5}.csv` |
| Agriculture | Productivity multiplier, meat preference | `zchunk_L2052.ag_prodchange_cost_irr_mgmt.R` |
| Land policy | Afforestation / carbon-price-on-land | See SPA table below |
| Emissions | Non-CO2 emission factors | `zchunk_L251.en_ssp_nonco2.R` |
| CCS | Storage cost curves | `zchunk_L261.Cstorage.R` |
| Renewables share | Share-weight overrides | `renewable_shareweights_ssp1_32.xml` (SSP1) |

### Fossil Fuel Cost Adders (2100, $/GJ)

| Fuel | SSP1 | SSP2 | SSP3 | SSP4 | SSP5 |
|------|------|------|------|------|------|
| Coal | 1.37 | 0.27 | 0.00 | 0.27 | 0.00 |
| Gas | 0.14 | 0.14 | 0.14 | 0.71 | 0.00 |
| Conv. Oil | 0.20 | 0.20 | 0.20 | 0.98 | 0.00 |
| Unconv. Oil | 0.21 | 0.21 | 0.21 | 1.06 | 0.00 |

Adders are linearly interpolated from $0 in the final historical year to the 2100 value above.

## Shared Policy Assumptions (SPAs)

When pairing an SSP baseline with a forcing target, SPAs specify:

**Global cooperation start year (harmonized carbon price)**

| Income group | SSP1 | SSP2 | SSP3 | SSP4 | SSP5 |
|-------------|------|------|------|------|------|
| High | 2025 | 2040 | 2040 | 2025 | 2040 |
| Medium | 2025 | 2040 | 2040 | 2025 | 2040 |
| Low | 2025 | 2040 | 2050 | 2025 | 2040 |

**Land carbon pricing policy**

| Income group | SSP1 | SSP2 | SSP3 | SSP4 | SSP5 |
|-------------|------|------|------|------|------|
| High | UCT (100%) | 50% | None (FFICT) | UCT (100%) | UCT (100%) |
| Medium | UCT (100%) | 50% | None (FFICT) | 50% | UCT (100%) |
| Low | UCT (100%) | 50% | None (FFICT) | None (FFICT) | UCT (100%) |

UCT = Universal Carbon Tax (land price = energy price). FFICT = Fossil Fuel & Industrial Carbon Tax only. A 50% transaction-cost discount is further applied to land carbon prices.

Pre-cooperation carbon prices are set to the level required to meet each region's Copenhagen pledge under SSP2 conditions, held constant across SSPs.

## Version Differences

Official SSPs were published from GCAM 4.0 (Calvin et al., 2017). Later versions diverge:

| Version | Change |
|---------|--------|
| v4.2 | Updated power-plant capital costs; established ADV/LOW cost tiers |
| v4.4 | Added net-negative-emissions constraint (affects 2.6 W/m^2 scenarios) |
| v5.1 | New land regions + multiple land technologies |
| v7.2 | SSP socioeconomic database updated to v3.0.1 (2024 revision) |

If the user asks about an older release, route to that version's page before applying modern assumptions.

## Data Access

- Official SSP database (CMIP6): <https://secure.iiasa.ac.at/web-apps/ene/SspDb/>
- GCAM SSP4 marker data: Calvin et al. (2017), Global Environmental Change 42:284-296
- SSP overview: Riahi et al. (2017), Global Environmental Change 42:153-168

---

### Authoring Basis

- Primary source: `gcam-doc/ssp.md` (v8.2 frontmatter)
- Version page: `version_pages/v8.2/ssp.md`
- Condensed for agent reference; load version page for full HTML tables and per-technology breakdowns
