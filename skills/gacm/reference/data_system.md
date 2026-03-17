# GCAM Data System

Comprehensive reference for the `gcamdata` R package and related preprocessing that builds GCAM's XML input files.

## Role and Architecture
The GCAM data system (the `gcamdata` R package, [github.com/JGCRI/gcamdata](https://github.com/JGCRI/gcamdata)) is the pipeline that transforms raw socioeconomic, energy, land, water, and emissions source data into the XML files GCAM reads at runtime. It is developed as a standalone R package since GCAM 5.1.

Key components:
- **Driver** (`driver.R`): orchestrates the full build. Discovers chunks, resolves dependency order, runs each chunk, writes XML. Also provides `driver_drake()` for incremental/cached builds.
- **Chunks**: R functions (one per file in `R/`) that declare inputs, produce outputs. Naming convention: `z<module>_L<level>_<topic>.R` for data processing, `z<module>_xml_<topic>.R` for XML generation.
- **Constants** (`constants.R`): shared parameters (region mappings, year vectors, elasticity defaults, `energy.NEG_EMISS_GDP_BUDGET_PCT`, etc.). Changing constants invalidates the entire cache.
- **Extdata** (`inst/extdata/`): raw CSV inputs organized by module -- `aglu/`, `energy/`, `emissions/`, `water/`, `common/`, `socioeconomics/`.

## Data Pipeline: Raw Data to XML Inputs
```
inst/extdata/ CSVs          (raw statistics: FAO, IEA, LDS/Moirai, CEDS, ...)
       |
   L1xx chunks              (country-level processing, reconciliation)
       |
   L2xx chunks              (GCAM-region aggregation, technology parameterization)
       |
   xml_* chunks             (XML batch generation via CSVToXML / mi-headers)
       |
   output/gcamdata/xml/     (XML files consumed by GCAM configuration)
```

Intermediate tibbles (e.g. `L102.pcgdp_thous90USD_Scen_R_Y`) flow between chunks; final XML outputs land in `xml/`.

## How Chunks Work
Every chunk is an R function responding to three commands:
1. `driver.DECLARE_INPUTS` -- returns character vector of required data names (prefix `FILE =` for CSV, otherwise another chunk's output).
2. `driver.DECLARE_OUTPUTS` -- returns names of tibbles or XML objects the chunk produces.
3. `driver.MAKE` -- receives `all_data` list, processes, returns outputs via `return_data()`.

Each output tibble must carry metadata: `add_title()`, `add_units()`, `add_precursors()`, `add_comments()`. The driver validates these before accepting the data.

## Adding New Data or Modifying Assumptions
1. **Edit existing extdata CSVs** in `inst/extdata/<module>/` to change source numbers.
2. **Create a new chunk** by copying `sample-chunk.R`, declaring new inputs/outputs, placing the file in `R/`.
3. **User modifications** (`user_modifications` arg to `driver()`): write a function using `driver.DECLARE_MODIFY` to intercept and alter an existing data object without editing the core chunk. Outputs get a `_usermod` suffix; downstream chunks consume the modified version automatically. Use `xml_suffix` to distinguish generated XML.
4. Re-run: `gcamdata::driver()` (full) or `gcamdata::driver_drake()` (incremental).

## Moirai / LDS Land Data Preprocessing
Moirai (Land Data System) produces gridded land-type areas, crop harvested area, production, and carbon densities at the country-by-GLU level. Its outputs live in `inst/extdata/aglu/LDS/`:
- `Land_type_area_ha.csv`, `LDS_ag_HA_ha.csv`, `LDS_ag_prod_t.csv`, `LDS_value_milUSD.csv`
- `MIRCA_irrHA_ha.csv` / `MIRCA_rfdHA_ha.csv` (irrigated vs rainfed)
- `Ref_veg_carbon_Mg_per_ha.csv`

These are consumed by `zaglu_L100.0_LDS_preprocessing.R` and subsequent aglu chunks. To use custom Moirai outputs, replace the LDS CSVs and rebuild.

## Custom Scenario Data Modification
For scenario experiments that change assumptions (e.g. different SSP agricultural productivity):
- Swap `ag_prodchange_ref_IRR_MGMT.xml` for an SSP-specific variant (produced by `zaglu_xml_ag_prodchange_ssp*.R` chunks).
- Or use the `user_modifications` mechanism to alter intermediate tibbles programmatically.
- Policy and socioeconomic add-on XMLs are loaded as `ScenarioComponents` in the configuration file and override base data; no data system rebuild is needed for these.

## Version Notes
| Era | Notes |
|-----|-------|
| Pre-5.1 | Perl/Makefiles-based data system; not the `gcamdata` R package |
| 5.1-5.4 | `gcamdata` R package introduced; drake support added |
| 6.0+ | GCAMFAOSTAT replaces older FAO preprocessing; chunk naming updated |
| 7.0-8.2 | Expanded modules (food processing, iron & steel, aluminum); Moirai v4 LDS inputs; prebuilt data caching |

Running GCAM for ordinary scenario experiments does **not** require rebuilding the data system. Rebuild only when changing baseline assumptions, adding new sectors/commodities, or updating historical calibration data.

## Related References
- `common_assumptions.md` -- shared structural assumptions (regions, years, GLUs)
- `inputs_outputs.md` -- catalog of XML files the data system produces
- `developer_workflows.md` -- where `gcamdata` and Moirai fit in the broader toolchain

---

### Authoring Basis
- Primary source: `gcam-doc/data-system.md` (v8.2 root tree)
- Supplementary: `gcam-core/input/gcamdata/R/driver.R`, `sample-chunk.R`, `constants.R`, `inst/extdata/` directory structure
- Bundled version page: `version_pages/v8.2/data-system.md`
