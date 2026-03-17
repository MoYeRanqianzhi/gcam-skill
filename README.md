# GCAM Skill (`gacm`)

A portable, self-contained AI agent skill for the [Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core). Provides comprehensive, version-aware GCAM expertise without requiring local model installations.

## What It Does

This skill equips AI agents (Claude, etc.) with deep knowledge of the entire GCAM ecosystem:

- **Model structure** -- energy, land, water, economy, emissions, and climate systems
- **22 GCAM versions** (v3.2 through v8.7) with version-specific routing and documentation
- **Scenario configuration** -- XML editing, policy design, target-finder mode, batch runs
- **Data extraction** -- Python (`gcamreader`) and R (`gcamextractor`) API references with 83+ documented extraction parameters
- **Scenario analysis** -- multi-scenario comparison workflows, visualization patterns, common analysis templates
- **Build & install** -- release download, source compilation, workspace management

## Quick Start

### For Agent Frameworks (Claude Code, etc.)

Install the skill in your agent environment, then simply ask GCAM-related questions:

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

The skill automatically activates on GCAM-related queries and routes to the correct version documentation.

### For Developers

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Validate the skill integrity:

```bash
python skills/gacm/scripts/validate_all.py
```

## Architecture

```
skills/gacm/
├── SKILL.md                    # SOP -- agent workflow, version routing, progressive disclosure
├── scripts/                    # 28 Python scripts (2 runtime, 3 generators, 23 validators)
│   ├── doc_search.py           # Runtime: search bundled references by version/pattern
│   ├── version_catalog.py      # Runtime: version registry and family metadata
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # One-shot validation suite
└── reference/                  # 33 topic docs + 22 version bundles
    ├── overview.md             # Model structure and core concepts
    ├── energy_system.md        # Resources, electricity, hydrogen, CCS, demand
    ├── land_system.md          # AgLU, GLU nesting, Moirai, carbon accounting
    ├── water_system.md         # 235 basins, cooling tech, water-energy-food nexus
    ├── economy.md              # GDP, KLEM, GCAM-macro, SAM calibration
    ├── emissions_climate.md    # CO2/non-CO2, MACs, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Carbon tax, RES, target finder, XML examples
    ├── trade.md                # Armington, Heckscher-Ohlin, commodity assignments
    ├── scenario_analysis.md    # Python/R multi-scenario comparison workflows
    ├── gcamreader_api.md       # Python Query/Connection API reference
    ├── gcamextractor_api.md    # R readgcam() with 83+ params, 14 groups
    ├── ssp.md                  # SSP1-5 narratives, quantitative assumptions
    ├── gcam_usa.md             # 51-state sub-national extension
    ├── versions/               # 22 version-specific route files (v3.2--v8.7)
    └── version_pages/          # 614 bundled version-page markdown files
```

### Progressive Disclosure

The skill uses a three-level loading system to minimize context window consumption:

| Level | Content | When Loaded | Token Cost |
|-------|---------|-------------|------------|
| **1** | `name` + `description` | Always | ~130 tokens |
| **2** | SKILL.md workflow | On skill trigger | ~2,800 tokens |
| **3** | Topic docs, scripts, version pages | On demand | Unlimited |

Three explicit **stop-loading gates** prevent unnecessary context accumulation.

## Coverage

### GCAM Systems

| System | Topics Covered |
|--------|---------------|
| Energy | Fossil/renewable resources, electricity (load segments, cooling), hydrogen (12 techs), CCS, refining, intermittent integration |
| Land | AgLU nested logit, GLUs, Moirai preprocessing, carbon accounting, bioenergy, livestock, forest management |
| Water | 6 demand sectors, 235 basins, cooling technology competition, groundwater (Superwell), desalination |
| Economy | Exogenous/endogenous GDP, KLEM CES production, SAM calibration, carbon price feedback |
| Emissions | 30+ species, MAC curves, Hector v3.2.0 (permafrost), GWP AR4/AR5, linked GHG markets |
| Policy | Carbon tax/constraint, RES/CES, target finder (7 target types), land protection, multi-policy stacking |
| Trade | Heckscher-Ohlin, Armington (21 sectors with logit params), Fixed Trade, GCAM-USA interstate |

### Companion Tool APIs

| Tool | Coverage |
|------|----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, CLI modes |
| `gcamextractor` (R) | `readgcam()` 16 params, 83+ `paramsSelect` values across 14 groups, `.Proj` caching, region aggregation |
| `rgcam` (R) | Conceptual summary; no source in project |
| ModelInterface | Headless batch-command XML generation |

### Version Support

22 versions from **v3.2** to **v8.7**, organized by documentation family:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 baseline)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Validation

The skill includes 22 automated validators covering:

- Document contract compliance (required phrases, version awareness)
- Page bundle integrity and content parity
- Filesystem hygiene and cross-platform portability
- Progressive disclosure alignment
- Semantic contract coverage (every doc has a validator)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Project Documentation

Persistent memory for contributors lives in `docs/`:

- `PROJECT.md` -- scope, decisions, open tasks
- `DEVELOPMENT.md` -- workflow guide, script taxonomy, validation gates
- `CHANGELOG.md` -- milestone log
- `KNOWN_ISSUES.md` -- limitations and technical debt

## License

[MIT](LICENSE)

## Acknowledgments

This skill synthesizes content from the open-source GCAM ecosystem:

- [GCAM](https://github.com/JGCRI/gcam-core) -- the Global Change Analysis Model (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- official GCAM documentation
- [gcamreader](https://github.com/JGCRI/gcamreader) -- Python query interface
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- R extraction package
