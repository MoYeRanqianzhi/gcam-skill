# Navigation

This file is the main bundled routing map for the open-source `gacm` skill.

## First Decision: Version
Always determine version before topic.

- If the user specifies a version, open `version_inventory.md` and then `versions/<version>.md`.
- If the user does not specify a version, default to the bundled baseline `v8.2`.
- If the user asks for comparison, open only the involved version route files plus the minimum topic docs needed.

## Second Decision: Topic
After version routing, open only the topic docs needed for the task:

- `overview.md`: high-level model structure and core concepts
- `common_assumptions.md`: regions, basins, GLUs, years, and shared assumptions
- `choice_marketplace.md`: logit choice, share weights, market-clearing logic, marketplace semantics
- `energy_system.md`: resources, electricity, liquids, gas, hydrogen, and trade
- `land_system.md`: land allocation, GLU nesting, terrestrial carbon, and land policy
- `water_system.md`: basin water demand and supply, cooling, scarcity, and water markets
- `economy.md`: GDP, macro module, KLEM, SAM consistency, and economic interpretation
- `emissions_climate.md`: CO2 and non-CO2 emissions, MACs, Hector coupling, and climate constraints
- `running_gcam.md`: reference runs, configuration, batch mode, target finder, ModelInterface
- `building_gcam.md`: compilation and runtime prerequisites
- `solver.md`: solver algorithms and configuration logic
- `policies_scenarios.md`: policy types, scenario components, targeting
- `inputs_outputs.md`: input classes, output classes, query patterns
- `ssp.md`: SSP assumptions and scenario framing
- `gcam_usa.md`: GCAM-USA scope and interpretation
- `tools.md`: gcamreader and gcamextractor usage
- `developer_workflows.md`: Fusion, dev/debug workflows, and broader GCAM ecosystem tools
- `updates.md`: release evolution and delta-only version notes
- `data_system.md`: GCAM data system role
- `coverage_map.md`: map from bundled docs back to the `v8.2` root topic pages
- `source_provenance.md`: what upstream materials were synthesized into this skill

## Version Families
Open `version_families.md` when the user asks about structural differences across eras.

## Runtime Rule
This skill is self-contained. Do not assume the user has a local `gcam-doc`, `gcam-core`, `gcamreader`, or `gcamextractor` checkout unless they explicitly provide one.

## Optional External Context
If the user explicitly provides a checkout, workspace, or file paths, you may inspect them as additional project context.

That external context is never required. The bundled references remain the default conceptual baseline.
