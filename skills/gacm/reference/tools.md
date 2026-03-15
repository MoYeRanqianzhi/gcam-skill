# GCAM Tooling (gcamreader + gcamextractor)

Bundled summary of common GCAM ecosystem tools outside the core model runtime.

## gcamreader (Python)
Purpose: run GCAM query XML against a BaseX database and return Pandas DataFrames or CSV output.

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
- Outputs are written as `*.csv` with `|` separator.

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

## gcamextractor (R)
Purpose: extract GCAM data to standardized tables, convert units, and aggregate by parameter/class.

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

### Output Structure (readgcam)
- `data`: raw table
- `dataAggParam`: aggregated by parameter
- `dataAggClass1`: aggregated by class 1
- `dataAggClass2`: aggregated by class 2
- `dataAll`: full table with original query metadata
- `scenarios`, `queries`: metadata

### .Proj Files
gcamextractor can read or write `.Proj` files for cached extraction.
