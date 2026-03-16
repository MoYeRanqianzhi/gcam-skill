# gcamextractor API (R)

Agent-oriented reference for the upstream `gcamextractor` R package.

Use this file after version routing when the user needs the `readgcam` argument surface, standardized table outputs, `.Proj` reuse, or the authoritative mapping between params and underlying queries.

## Package Role
`gcamextractor` sits on top of GCAM query output workflows and standardizes the extracted tables for downstream analysis.

Use it when the user wants:
- R-native post-processing
- parameter- or class-level aggregations
- unit conversions already handled for them
- reusable `.Proj` snapshots instead of re-querying every time

## Install
```r
install.packages("devtools")
devtools::install_github("JGCRI/gcamextractor")
```

## Main Entry Point: `readgcam`

### Current source signature
The current R source defines:

```r
readgcam(
  gcamdatabase = NULL,
  gcamdata_folder = NULL,
  queryFile = NULL,
  dataProjFile = "dataProj.proj",
  maxMemory = "4g",
  scenOrigNames = "All",
  scenNewNames = NULL,
  reReadData = T,
  regionsSelect = NULL,
  regionsAggregate = NULL,
  regionsAggregateNames = NULL,
  paramsSelect = "diagnostic",
  folder = getwd(),
  nameAppend = "",
  saveData = T,
  removeVintages = F
)
```

Important note:
- source and generated docs are slightly out of sync: the current R source includes `removeVintages=F` in `readgcam`, so prefer the source signature when they disagree

### High-value arguments
- `gcamdatabase`: full path to the GCAM database directory
- `gcamdata_folder`: optional path to `gcamdata`; only required for some params
- `queryFile`: optional XML query file; if `NULL`, the package writes bundled `queries_xml` to `folder/queries.xml`
- `dataProjFile`: cached project file path or output name for `.Proj` reuse
- `maxMemory`: Java / query memory budget such as `"4g"`
- `scenOrigNames`: scenario names to read; `"All"` means all available scenarios
- `scenNewNames`: replacement scenario labels for downstream outputs
- `reReadData`: `TRUE` to re-query GCAM, `FALSE` to reuse an existing `.Proj`
- `regionsSelect`: subset of regions to keep
- `regionsAggregate`: vector or list of vectors defining aggregate regions
- `regionsAggregateNames`: names for those aggregate regions
- `paramsSelect`: parameter group, individual parameter names, or `All`
- `folder`: output directory
- `nameAppend`: suffix for saved files
- `saveData`: whether to write files to disk
- `removeVintages`: source-only flag in the current R code

If `queryFile=NULL`, the package writes bundled `queries_xml` to `folder/queries.xml` before extraction.

## Parameter Selection Model
`paramsSelect` can be:
- `All`
- a group name
- one or more individual parameter names

Documented group families include:
- `energy`
- `electricity`
- `transport`
- `water`
- `socioecon`
- `ag`
- `livestock`
- `land`
- `emissions`

The package default is `diagnostic`, which is handled in source even though it is not emphasized in every generated doc artifact.

## Authoritative Helper Datasets

### `params`
List of available parameter names.

### `queries`
List of upstream query names used by the package.

### `map_param_query`
The most important helper table for agents.

Use it to answer:
- which GCAM query underlies a parameter
- which group a parameter belongs to
- whether a parameter requires `gcamdata`

### `queries_xml`
Bundled XML query definition used when `queryFile=NULL`.

### Region and mapping helpers
- `regions_gcam32`
- `regions_gcam_basins`
- `regions_US49`
- `regions_US52`
- `map_country_to_gcam_region`
- `map_state_to_gridregion`

### Conversion and economics helpers
- `convert`
- `GWP`
- `conv_GgTg_to_MTC`
- `gdp_deflator(year, base_year)`

## Output Structure
`readgcam(...)` returns a list that commonly includes:
- `data`: cleaned data table
- `dataAggParam`: aggregated by parameter
- `dataAggClass1`: aggregated by class 1
- `dataAggClass2`: aggregated by class 2
- `dataAll`: full table with original query metadata
- `scenarios`: scenario metadata
- `queries`: query metadata

The package vignettes also describe these as the main saved CSV and in-memory table outputs.

## `.Proj` Workflow
Use `.Proj` files when extraction is expensive and the user will iterate on analysis.

Rules:
- `reReadData=TRUE`: query GCAM again and create or update the `.Proj`
- `reReadData=FALSE`: reuse an existing `.Proj`
- `dataProjFile` can point to an existing file or define where a new cached project should be written

This is the preferred path when:
- the same scenario set is reused repeatedly
- the user wants to share extracted data without sharing the whole GCAM DB

## Minimal Workflows

### Extract directly from a GCAM database
```r
library(gcamextractor)

dataGCAM <- gcamextractor::readgcam(
  gcamdatabase = "/path/to/gcam/output/database_ref",
  regionsSelect = c("Colombia"),
  paramsSelect = "pop",
  folder = "my_output_folder"
)
```

### Reuse a cached `.Proj`
```r
library(gcamextractor)

dataGCAM <- gcamextractor::readgcam(
  dataProjFile = "/path/to/dataProj.proj",
  reReadData = FALSE,
  folder = "my_output_folder"
)
```

### Inspect the param-query mapping first
```r
library(gcamextractor)

gcamextractor::params
gcamextractor::queries
gcamextractor::map_param_query
```

## Failure and Edge Cases
- invalid `paramsSelect`:
  source prints the available params and then stops with `None of the params chosen are available.`
- missing `gcamdatabase` path:
  source stops if the provided database directory does not exist
- missing `gcamdata_folder`:
  source warns and skips params that require `gcamdata`
- `queryFile=NULL`:
  the package materializes `queries_xml` into `folder/queries.xml` automatically
- region naming:
  the source normalizes `United States` to `USA`

## Practical Agent Rules
- Start with `map_param_query` when the user asks what a parameter really means.
- Prefer `.Proj` reuse for repeated analytic work.
- Treat the current source signature as authoritative when the vignette, README, and generated `man/*.Rd` pages disagree.
- If the user needs raw GCAM-native query parity rather than standardized tables, fall back to `query_automation.md` or `tools.md`.

## Authoring Basis
- `gcamextractor/README.md`
- `gcamextractor/R/readgcam.R`
- `gcamextractor/R/data.R`
- `gcamextractor/man/readgcam.Rd`
- `gcamextractor/man/queries_xml.Rd`
- `gcamextractor/man/params.Rd`
- `gcamextractor/man/queries.Rd`
- `gcamextractor/man/map_param_query.Rd`
- `gcamextractor/vignettes/vignette_readgcam.Rmd`
- `gcamextractor/vignettes/vignette_parameters.Rmd`
