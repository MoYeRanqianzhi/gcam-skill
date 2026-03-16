# Query Automation

Agent-first guide to extracting GCAM results through query XML, batch commands, and headless tooling.

Open this file when the task is about:
- running query XML headlessly
- exporting CSV from a GCAM database
- wiring post-run automatic extraction
- choosing between ModelInterface batch mode, `gcamreader`, `rgcam`, and `gcamextractor`

## Core Artifacts
Recognize these paths before choosing a tool:
- output database: `output/database_basexdb`
- main query file: `output/queries/Main_queries.xml`
- example batch query file: `output/gcam_diagnostics/batch_queries/Model_verification_queries.xml`
- example batch command file: `output/gcam_diagnostics/batch_queries/xmldb_batch.xml`
- XML DB driver properties file in `exe/`

Do not hardcode those paths. Detect them from the actual workspace the user provides.

## Preferred Automation Order
1. Use `gcamreader` when Python CSV/DataFrame output is enough.
2. Use `rgcam` when the user is already in R and wants project-data files.
3. Use `gcamextractor` when the user wants standardized extracted tables and aggregations.
4. Use headless ModelInterface batch mode when the user already has GCAM-native query XML and wants exact upstream query behavior.

## Headless ModelInterface Batch Mode
The exact upstream no-UI pattern is:

```bash
java -cp "$CLASSPATH" ModelInterface/InterfaceMain -b batch_queries/xmldb_batch.xml
```

This is the most direct way to reuse GCAM query XML from the command line.

### Minimal Batch Command Structure
The bundled v4.3 and v8.2 user guides document a `ModelInterfaceBatch` file containing:
- `<scenario>`
- `<queryFile>`
- `<outFile>`
- `<xmldbLocation>`

Minimum operational interpretation:
- `scenario`: which scenario to query
- `queryFile`: query definitions
- `outFile`: CSV or XLS destination
- `xmldbLocation`: database to open

Use this when you want deterministic headless export and already know the scenario name.

## Post-Run Automatic Queries
GCAM can run queries automatically after a scenario completes through the XML DB driver properties file.

Important keys documented in the bundled modern user guide:
- `in-memory`
- `open-db-wait`
- `filter-script`
- `batch-queries`
- `batch-logfile`

Practical use cases:
- run queries immediately after each scenario
- avoid keeping the full XML database on disk
- emit only selected CSV outputs in large batch workflows

## Query File Choices

### Reuse Existing Query XML
Use the existing query file when:
- the user already trusts the GCAM-native aggregation
- they want parity with prior GCAM workflows
- they need exact scenario/query reproducibility

### Generate or Edit Batch Query XML
Use a batch query file when:
- you want multiple queries exported in one run
- you want region selection controlled in XML
- you want a stable artifact that can be reused across scenarios

Use `scripts/generate_modelinterface_batch.py` when you need a minimal batch-command XML file quickly and do not want to hand-type the `ModelInterfaceBatch` wrapper.

### Choose Extraction Libraries Instead
Use a higher-level extraction library when:
- the user wants Python or R tables, not GCAM query authoring
- the workflow is analytical rather than GCAM-native
- repeated downstream scripting matters more than preserving ModelInterface XML

## Tool Selection

### `gcamreader`
Use when:
- Python is the target environment
- CSV or DataFrame output is enough
- local or remote BaseX access is needed

Open `gcamreader_api.md` when the user needs the Python object model or method-level behavior.

### `rgcam`
Use when:
- the user works in R
- they want persistent project-data files
- they are comfortable using GCAM query XML through an R wrapper

### `gcamextractor`
Use when:
- the user wants standardized extracted tables
- they want unit conversion and aggregation by parameter/class
- they are already organizing work around `paramsSelect`

Open `gcamextractor_api.md` when the user needs the exact R argument surface or `.Proj` reuse behavior.

Open `tools.md` for install and selection examples.

## Storage and Performance Controls
When result volume is the problem, do not change the model first.
Try:
- `in-memory` DB mode
- `filter-script`
- `batch-queries`
- minimal CSV outputs instead of keeping the whole DB

## Version Notes

### `v5.4` through `v8.2`
- BaseX-based query automation is the stable reference path.
- `output/queries/Main_queries.xml` and `output/gcam_diagnostics/batch_queries/` are explicitly documented.

### `v4.2` through `v4.4`
- Headless ModelInterface batch mode is already documented.
- The docs still reflect older Java and path assumptions, so inspect the actual workspace when provided.

### `v3.2`
- The bundle contains inherited user-guide material plus separate compile/build notes.
- Some query behavior may reflect legacy DBXML-era tooling details, so treat the provided workspace as authoritative if the user has one.
