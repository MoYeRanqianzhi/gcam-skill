# Policies and Scenario Controls

Comprehensive reference for GCAM policy mechanisms: emissions pricing, energy standards, land protection, and climate-target-driven runs. All XML examples use v8.2 conventions.

## Emissions Policies

GCAM supports three primary approaches; all work by placing a price on emissions that propagates through the entire model:

1. **Carbon / GHG price** -- user supplies `<fixedTax>` values; GCAM computes resulting emissions.
2. **Emissions constraint** -- user supplies `<constraint>` quantities; GCAM solves for the price each period.
3. **Climate constraint (target finder)** -- user supplies a climate target; GCAM iterates over price paths to find the least-cost trajectory.

### XML: Carbon Tax / Constraint
```xml
<ghgpolicy name="CO2">
  <market>USA</market>
  <fixedTax year="2025" fillout="1">1</fixedTax>    <!-- $1/tC price path -->
  <!-- OR: <constraint year="2050">5000</constraint>  MtC cap, solver finds price -->
</ghgpolicy>
```
Regions sharing the same `<market>` string share a common price. The string is arbitrary.

## Linked Emission Markets

`<linked-ghg-policy>` connects non-CO2 gases to a parent market:
- `<price-adjust>` -- price multiplier (e.g. GWP-based). Set to 0 to disable economic feedback while MAC curves still respond.
- `<demand-adjust>` -- quantity conversion to common units for shared constraints.
- `<linked-policy>` -- parent market name.

Default `linked_ghg_policy.xml` links all Kyoto gases to a "GHG" market using 100-year GWPs. CH4/N2O get nonzero `price-adjust`; F-gases default to zero.

## Non-CO2 Markets

Standalone markets for any species (SO2, NOx, etc.) via `<ghgpolicy>`. Useful only with MAC curves. Key MAC tags: `market-name` (default CO2), `mac-price-conversion` (default 1; -1 disables), `zero-cost-phase-in-time` (default 25 yr).

## Renewable / Clean Energy Standards (RES)

Implemented via `<policy-portfolio-standard>` with `<policyType>RES</policyType>`:
- **Demand side**: add `<minicam-energy-input name="Credits"><coefficient>0.1</coefficient>` (10% share target) to consuming sector.
- **Supply side**: add `<res-secondary-output name="Credits"><output-ratio>1</output-ratio>` to qualifying technologies.
- **Market**: `<policy-portfolio-standard name="Credits"><market>USA</market><policyType>RES</policyType>`.

If the standard is non-binding, the credit price falls to zero. The same pattern works for clean energy standards by choosing which technologies receive the secondary output.

## Energy Production Constraints

Use `<policy-portfolio-standard>` with `policyType` = `tax` (upper bound) or `subsidy` (lower bound). Link technologies via `<input-tax>` or `<input-subsidy>`:
```xml
<technology name="regional biomass">
  <period year="2025"><input-tax name="bio-constraint"/></period>
</technology>
<policy-portfolio-standard name="bio-constraint">
  <market>USA</market><policyType>tax</policyType>
  <constraint year="2025" fillout="1">10</constraint>
</policy-portfolio-standard>
```
For exact (equality) constraints, add `<min-price year="2025" fillout="1">-100</min-price>`.

## Land-Use Policies

- **Protected lands** -- default protects 90% of non-commercial ecosystems (`protected_land_input_*.xml`).
- **Valuing carbon in land** -- carbon price on LUC CO2 via `global_uct*.xml` policy files.
- **Land constraints** -- use `<land-constraint-policy>` on `UnmanagedLandLeaf` nodes with a `<policy-portfolio-standard>` (`policyType` subsidy = floor, tax = ceiling).
- **Bioenergy constraints** -- default includes negative-emissions GDP budget (`energy.NEG_EMISS_GDP_BUDGET_PCT`) and biomass externality cost curve (`A27.GrdRenewRsrcCurves.csv`).

## Subsidies and Tax Policies

`<fixedTax>` without a `<constraint>` creates an unsolved market -- the value is added (tax) or subtracted (subsidy) from technology costs each period. Simplest way to model technology-specific incentives.

## Multi-Policy Stacking

Multiple policies coexist. Standard `configuration_policy.xml` pattern:
1. Near-term CO2 price (`spa14_tax.xml`) -- fixed regional path.
2. Long-term CO2 (`carbon_tax_0.xml`) -- global `CO2_LTG` market, adjusted by target finder.
3. Target finder link (`2025_target_finder.xml`) -- links regional CO2 to near/long-term markets.
4. LUC carbon pricing (`global_uct_phasein_no_constraint.xml`).
5. GHG linkage (`linked_ghg_policy.xml`) -- ties non-CO2 to GHG basket.

Policy XMLs go in `<ScenarioComponents>` after base data to override defaults.

## Target Finder Mode

Enable: `<find-path>1</find-path>` in `<Bools>`, set `<policy-target-file>` in `<Files>`. The `<policy-target-runner>` controls:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tax-name` | CO2 | Market whose price is adjusted |
| `target-value` | -- | e.g. 4.5 W/m2 |
| `target-type` | concentration | `concentration`, `forcing`, `stabilization`, `kyoto-forcing`, `rcp-forcing`, `temperature`, `cumulative-emissions` |
| `path-discount-rate` | 0.03 | Hotelling rate |
| `first-tax-year` | 2020 | Start year |
| `forward-look` | 0 | Periods to skip |
| `max-tax` | 4999 | Price cap per period |

Use `<stabilization/>` for monotonic paths or `<overshoot year="2100"/>` for overshoot. Pre-built targets: `forcing_target_2p6_overshoot.xml`, `_3p7`, `_4p5`, `_6p0`.

## Policy Cost Calculation

GCAM uses the **deadweight loss** approach: area under the marginal abatement cost curve. Limitations: no macro feedback, no tax-revenue recycling. Currently supports only CO2-pegged policies.

## Version Notes

| Era | Key differences |
|-----|----------------|
| v3.x-v4.x | Fewer pre-built policy files; less modular docs |
| v5.2+ | `configuration_policy.xml`; near/long-term split; target finder formalized |
| v7.0+ | Expanded SPA files; phasein target-finder variants |
| v8.2 | 32-region linked policies; Hector integration; `CO2_LTG` convention |

---

### Authoring Basis
- Primary: `gcam-doc/policies.md`, `gcam-doc/policies_examples.md` (v8.2)
- Supplementary: `gcam-core/exe/configuration_policy.xml`, `gcam-core/input/policy/` (forcing targets, linked_ghg_policy, carbon_tax, target_finder XMLs)
- Bundled: `version_pages/v8.2/policies.md`, `version_pages/v8.2/policies_examples.md`
