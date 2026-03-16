# GCAM Tooling (Headless Extraction)

Bundled summary of GCAM ecosystem tools that fit agent-oriented text and command-line workflows.

Open `query_automation.md` when the task is about end-to-end query/export wiring rather than tool selection alone.

## Selection Rule
Choose the smallest tool that matches the task:
- raw query XML to CSV or DataFrame: `gcamreader`
- R-native extraction project workflow: `rgcam`
- standardized parameter/class extraction tables: `gcamextractor`
- multi-run orchestration and automation around GCAM: see `developer_workflows.md` for `pygcam`

Prefer dedicated headless tools over interactive ModelInterface workflows when they solve the task.

## gcamreader (Python)
Purpose: run GCAM query XML against a BaseX database and return Pandas DataFrames or CSV output.

Open `gcamreader_api.md` when the user needs object-level Python usage, method names, return semantics, or failure handling.

### Install
```bash
pip install gcamreader
```

### CLI (Local DB)
```bash
gcamreader local \
  --database_path <path/to/database_parent> \
  --query_path <path/to/Main_queries.xml> \
  --output_path <output_dir> \
  --force true
```

Notes:
- `database_path` is the directory that contains the `*.basex` files.
- Outputs are written as `*.csv` with `|` separators.

### CLI (Remote DB)
```bash
gcamreader remote \
  --username <user> \
  --password <pass> \
  --hostname <host> \
  --port 8984 \
  --database_name <db_name> \
  --query_path <path/to/queries.xml> \
  --output_path <output_dir> \
  --force true
```

## rgcam (R)
Purpose: extract data from GCAM output databases into an R-native project data file.

Use when:
- the user already works in R
- they want repeatable query extraction across scenarios
- they want a persistent project-data representation rather than ad hoc CSV files

Bundled role summary:
- runs the same query families used for ModelInterface batch extraction
- stores imported results in an R-friendly project data file
- supports repeated analysis without manually re-querying the XML DB every time

## gcamextractor (R)
Purpose: extract GCAM data to standardized tables, convert units, and aggregate by parameter/class.

Open `gcamextractor_api.md` when the user needs `readgcam` argument behavior, `.Proj` caching rules, or parameter/query mapping details.

### Install
```r
install.packages("devtools")
devtools::install_github("JGCRI/gcamextractor")
```

### Basic Usage
```r
library(gcamextractor)
path_to_gcam_database <- "/path/to/gcam/output/database_ref"
gcamextractor::params
dataGCAM <- gcamextractor::readgcam(
  gcamdatabase = path_to_gcam_database,
  regionsSelect = c("Colombia"),
  paramsSelect = "pop",
  folder = "my_output_folder"
)
```

### Output Structure
- `data`: raw table
- `dataAggParam`: aggregated by parameter
- `dataAggClass1`: aggregated by class 1
- `dataAggClass2`: aggregated by class 2
- `dataAll`: full table with original query metadata
- `scenarios`, `queries`: metadata

### Cached Project Files
`gcamextractor` can read or write `.Proj` files for cached extraction workflows.

## Headless Query Engine Fallback
If the user already has GCAM query XML and wants exact upstream query behavior, use ModelInterface batch mode from the command line:

```bash
java -cp "$CLASSPATH" ModelInterface/InterfaceMain -b batch_queries/xmldb_batch.xml
```

Treat this as a headless query engine, not as the preferred human-facing interface.
