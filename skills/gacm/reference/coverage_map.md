# Coverage Map

This file maps the bundled `gacm` references back to the `v8.2` root documentation topics used during authoring.

Purpose:
- make the bundled skill traceable
- show that `v8.2` coverage is rooted in the `gcam-doc` root tree
- clarify which bundled file to open for a given source topic family

## Root `v8.2` Topic Coverage
- `index.md`, `overview.md` -> `overview.md`
- `common_assumptions.md` -> `common_assumptions.md`
- `choice.md`, `marketplace.md` -> `choice_marketplace.md`
- `demand_energy.md`, `supply_energy.md`, `details_energy.md`, `en_technologies.md` -> `energy_system.md`
- `land.md`, `demand_land.md`, `supply_land.md`, `details_land.md` -> `land_system.md`
- `demand_water.md`, `supply_water.md`, `details_water.md` -> `water_system.md`
- `economy.md`, `inputs_economy.md` -> `economy.md`
- `emissions.md`, `details_emissions.md`, `hector.md` -> `emissions_climate.md`
- `user-guide.md` -> `running_gcam.md`
- `gcam-build.md` -> `building_gcam.md`
- `solver.md` -> `solver.md`
- `policies.md`, `policies_examples.md` -> `policies_scenarios.md`
- `inputs_demand.md`, `inputs_supply.md`, `inputs_land.md`, `outputs_quantity.md`, `outputs_prices.md`, `outputs_emissions.md`, `outputs_land.md`, `outputs_trade.md` -> `inputs_outputs.md`
- `ssp.md` -> `ssp.md`
- `gcam-usa.md` -> `gcam_usa.md`
- `fusion.md`, `dev-guide.md`, `dev-guide/*` -> `developer_workflows.md`
- `data-system.md` -> `data_system.md`
- `updates.md`, release-note/CMP material -> `updates.md` plus `versions/*.md`

## Version Routing Coverage
- Historical full-doc families from `v3.2` through `v7.1` are represented in `version_inventory.md`, `version_families.md`, and `versions/*.md`.
- Release-note-oriented versions such as `v7.2`-`v7.4` and `v8.0`-`v8.7` are represented as `delta-only` routes rather than fake full topic trees.
- `v8.2` is the bundled current full-topic baseline because it maps to the root `gcam-doc` tree.

## Tooling Coverage
- `gcamreader` authoring references -> `tools.md`
- `gcamextractor` authoring references -> `tools.md`
- broader GCAM ecosystem references -> `developer_workflows.md`
