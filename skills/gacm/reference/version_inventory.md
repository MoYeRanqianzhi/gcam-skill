# Version Inventory

This file is the authoritative bundled version-routing table for the `gacm` skill.

Rules:
- If the user specifies a GCAM version, route to that exact bundled version file first.
- If the user does not specify a version, default to the bundled current baseline: `v8.2`.
- `delta-only` releases bundle only their documented deltas, not a full standalone restatement of every topic.
- Never claim access to a version-specific upstream checkout unless the user actually provides one.

| Version | Family | Coverage Mode | Route |
| --- | --- | --- | --- |
| `v8.7` | `delta-only` | `delta-only` | `versions/v8.7.md` |
| `v8.6` | `delta-only` | `delta-only` | `versions/v8.6.md` |
| `v8.5` | `delta-only` | `delta-only` | `versions/v8.5.md` |
| `v8.4` | `delta-only` | `delta-only` | `versions/v8.4.md` |
| `v8.3` | `delta-only` | `delta-only` | `versions/v8.3.md` |
| `v8.2` | `modern-comprehensive` | `bundled-baseline` | `versions/v8.2.md` |
| `v8.1` | `delta-only` | `delta-only` | `versions/v8.1.md` |
| `v8.0` | `delta-only` | `delta-only` | `versions/v8.0.md` |
| `v7.4` | `delta-only` | `delta-only` | `versions/v7.4.md` |
| `v7.3` | `delta-only` | `delta-only` | `versions/v7.3.md` |
| `v7.2` | `delta-only` | `delta-only` | `versions/v7.2.md` |
| `v7.1` | `modern-comprehensive` | `version-summary` | `versions/v7.1.md` |
| `v7.0` | `modern-comprehensive` | `version-summary` | `versions/v7.0.md` |
| `v6.0` | `modern-comprehensive` | `version-summary` | `versions/v6.0.md` |
| `v5.4` | `modern-comprehensive` | `version-summary` | `versions/v5.4.md` |
| `v5.3` | `modern-transitional` | `version-summary` | `versions/v5.3.md` |
| `v5.2` | `modern-transitional` | `version-summary` | `versions/v5.2.md` |
| `v5.1` | `modern-transitional` | `version-summary` | `versions/v5.1.md` |
| `v4.4` | `compact-modern` | `version-summary` | `versions/v4.4.md` |
| `v4.3` | `compact-modern` | `version-summary` | `versions/v4.3.md` |
| `v4.2` | `compact-modern` | `version-summary` | `versions/v4.2.md` |
| `v3.2` | `legacy-wiki` | `version-summary` | `versions/v3.2.md` |

## Detailed Version Page Bundles
For page-level detail, open `version_pages/<version>/INDEX.md` after routing to the exact version.

## Shared Topic Docs
These bundled topic docs are the main progressive-disclosure entry points after version routing.
- `navigation.md`
- `version_families.md`
- `overview.md`
- `common_assumptions.md`
- `choice_marketplace.md`
- `energy_system.md`
- `land_system.md`
- `water_system.md`
- `economy.md`
- `emissions_climate.md`
- `running_gcam.md`
- `building_gcam.md`
- `solver.md`
- `policies_scenarios.md`
- `inputs_outputs.md`
- `ssp.md`
- `gcam_usa.md`
- `tools.md`
- `developer_workflows.md`
- `updates.md`
- `data_system.md`
- `coverage_map.md`
- `source_provenance.md`
