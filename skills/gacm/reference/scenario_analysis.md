# Scenario Analysis and Data Processing

Guide for comparing GCAM scenarios and processing results into actionable outputs.

Open this file when the task involves:
- comparing two or more GCAM scenarios
- building emissions/energy/land analysis from GCAM output
- pivot tables, aggregation, or visualization of scenario results
- exporting processed GCAM data to CSV, Excel, or plots

## Scenario Comparison Workflow (General)

1. Locate the database (`output/database_basexdb` or user-specified path).
2. List scenarios in the database.
3. Extract the same queries across all target scenarios.
4. Align on common dimensions (region, year, sector); compute deltas or ratios.
5. Visualize or export.

## Python Workflow (gcamreader)

```python
from gcamreader.querymi import LocalDBConn, parse_batch_query, importdata

# Connect and list scenarios
conn = LocalDBConn("output", "database_basexdb")   # prints scenarios on connect
scenarios_df = conn.listScenariosInDB()             # columns: name, date, fqName

# Single query
queries = parse_batch_query("output/queries/Main_queries.xml")
q = [q for q in queries if q.title == "CO2 emissions by region"][0]
df = conn.runQuery(q, scenarios=["Reference", "Carbon_Tax_25"])

# Batch query -- returns dict {query_title: DataFrame}
results = importdata("output/database_basexdb",
                     "output/queries/Main_queries.xml",
                     scenarios=["Reference", "Carbon_Tax_25"], warn_empty=False)
```

Use `fqName` (name + date) to disambiguate duplicate scenario names.

**Multi-scenario pivot and common pandas patterns:**

```python
import pandas as pd
pivot = df.pivot_table(index=["region", "Year"], columns="scenario",
                       values="value", aggfunc="sum")
pivot["delta"] = pivot["Carbon_Tax_25"] - pivot["Reference"]
pivot["pct_change"] = pivot["delta"] / pivot["Reference"] * 100

by_sector = df.groupby(["sector", "Year"])["value"].sum().reset_index()
merged = pd.merge(energy_df, emissions_df,
                  on=["scenario", "region", "Year"], suffixes=("_e", "_m"))
```

**CLI batch export** (pipe-separated CSV, one file per query):

```bash
gcamreader local -d output/database_basexdb \
  -q output/queries/Main_queries.xml -o results/ --force true
```

## R Workflow (gcamextractor)

```r
library(gcamextractor)
dataGCAM <- readgcam(
  gcamdatabase  = "output/database_basexdb",
  scenOrigNames = c("Reference", "Carbon_Tax_25"),
  scenNewNames  = c("Ref", "CT25"),           # short labels for plots
  regionsSelect = NULL,                       # NULL = all regions
  paramsSelect  = "emissions",                # group or individual param
  folder        = "analysis_out")
```

**Output tables:** `dataGCAM$data` (detailed), `$dataAggParam`, `$dataAggClass1`, `$dataAggClass2`, `$dataAll` (with original query metadata).

**`.Proj` cache** -- first run writes `dataProj.proj`; reload to skip the database:

```r
dataGCAM <- readgcam(dataProjFile = "analysis_out/dataProj.proj",
                     reReadData = FALSE, paramsSelect = "energy",
                     folder = "analysis_out")
```

**Region aggregation and filtering:**

```r
dataGCAM <- readgcam(
  gcamdatabase = "output/database_basexdb",
  regionsSelect = c("USA", "China", "EU-15"),
  regionsAggregate = list(c("USA", "Canada", "Mexico")),
  regionsAggregateNames = c("North America"),
  paramsSelect = "All", folder = "regional_out")
```

**Multi-scenario visualization:**

```r
library(ggplot2)
ggplot(dataGCAM$data, aes(x = x, y = value, color = scenario)) +
  geom_line() + facet_wrap(~region, scales = "free_y")
```

## Common Analysis Patterns

### Emissions Reduction Pathway
Compare total GHG between reference and mitigation scenarios.
- Python: query `"CO2 emissions by region"`, pivot on scenario, compute `ref - policy`.
- R: `paramsSelect = "emissGHGBySectorGWPAR5"`, overlay scenarios.
- Verify 2015/2020 values align (shared calibration period).

### Energy Transition
Track primary energy mix shift: `paramsSelect = "energyPrimaryByFuelEJ"` (R) or query `"primary energy consumption by region"` (Python). Derived metric: `renewable_share = (solar+wind+hydro+geo+bio) / total`.

### Land Use Change
`paramsSelect = "landAlloc"` gives allocation by type. Compute `value(policy,2050) - value(ref,2050)` per land category.

### Carbon Price Impact
Correlate carbon price trajectory with electricity mix (`elecByTechTWh`), total emissions, and fossil fuel decline.

### Technology Penetration

```python
elec = results["elec gen by gen tech"]
solar = elec[elec["technology"].str.contains("solar", case=False)]
total = elec.groupby(["scenario","Year"])["value"].sum()
share = solar.groupby(["scenario","Year"])["value"].sum() / total
```

### Regional Disparity
- R: `regionsAggregate` for macro-regions, then facet by region.
- Python: groupby `region`, merge with population query for per-capita values.

## Data Export

```python
# CSV
df.to_csv("scenario_comparison.csv", index=False)

# Excel -- multiple sheets
with pd.ExcelWriter("results.xlsx") as w:
    for title, frame in results.items():
        if frame is not None:
            frame.to_excel(w, sheet_name=title[:31], index=False)

# Plot
import matplotlib.pyplot as plt
pivot[["Reference","Carbon_Tax_25"]].plot()
plt.savefig("comparison.png", dpi=150, bbox_inches="tight")
```

```r
ggsave("comparison.png", width = 10, height = 6, dpi = 150)
```

## Authoring Basis

- `gcamreader` source: `gcamreader/querymi.py` -- `LocalDBConn`, `importdata`, `parse_batch_query`
- `gcamreader` CLI: `gcamreader/cli.py` -- `local`/`remote`, batch export via multiprocessing
- `gcamextractor` source: `gcamextractor/R/readgcam.R` -- `readgcam()` full signature and params
- `gcamextractor` vignettes: `vignette_readgcam.Rmd`, `vignette_parameters.Rmd`
- Existing reference docs: `query_automation.md`, `tools.md`
