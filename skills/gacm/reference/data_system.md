# GCAM Data System

Skill-bundled baseline summary of the GCAM data system role.

Use this file after version routing.

## Summary
The GCAM data system is the XML-building layer behind much of the core model input set. In the modern GCAM line it is largely associated with `gcamdata`, which processes raw datasets, reconciles assumptions, and writes the XML files consumed by GCAM.

## What It Does
- harmonizes raw energy, land, water, economic, and policy source data
- generates historical calibration XML and future-assumption XML
- encodes shared assumptions about regions, basins, GLUs, years, and scenario defaults
- materializes many settings that users later perceive as "core GCAM inputs"

## When It Matters
Open this topic when the user asks:
- where an XML input came from
- how to rebuild or modify baseline XML data
- why a region, basin, year, or land structure looks the way it does
- how Moirai, SSP assumptions, or other preprocessing enters GCAM

## Scope Boundary
- Running GCAM does not require rerunning the data system for ordinary scenario experiments.
- Rebuilding foundational XML inputs or changing baseline data assumptions usually does.
- The data system is part of the GCAM ecosystem, not a runtime dependency of the `gacm` skill itself.

## Version Notes
- `v5.x` is the important era where the data system becomes more explicitly separated into the `gcamdata` ecosystem workflow.
- `v8.2` root docs are the bundled current baseline for data-system interpretation in this skill.
- If the user asks about a historical preprocessing structure or exact generated XML lineage, route to the exact version and inspect any provided workspace before assuming the modern `gcamdata` split.

## Related References
- `common_assumptions.md` for shared structural assumptions
- `inputs_outputs.md` for the kinds of files the data system helps produce
- `developer_workflows.md` for where `gcamdata` and `moirai` sit in the broader toolchain
