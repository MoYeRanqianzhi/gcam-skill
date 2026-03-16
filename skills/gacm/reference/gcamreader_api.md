# gcamreader API (Python)

Agent-oriented reference for the upstream `gcamreader` Python package.

Use this file after version routing when the user needs Python extraction details, method names, DataFrame semantics, or failure diagnosis beyond the short tool-selection summary in `tools.md`.

## Reality Check
- The upstream Python API uses `runQuery`, not `run_query`.
- The main public surfaces come from `gcamreader/querymi.py` and are re-exported by `gcamreader/__init__.py`.
- The package supports both CLI use and direct Python use.

## Install
```bash
pip install gcamreader
```

Use the CLI when the user just wants CSV files. Use the Python API when the user needs in-memory Pandas workflows, custom scenario filtering, or programmatic control over local versus remote BaseX access.

## Core Objects and Functions

### `Query(xmlin)`
Purpose: hold one GCAM query definition parsed from XML.

Accepted input:
- a raw XML string
- a parsed XML element

Key attributes:
- `querystr`: serialized XML query text
- `regions`: list of `<region name="...">` filters found in the query, or `None`
- `title`: query title from the XML element

Operational use:
- build this indirectly through `parse_batch_query(...)` unless the user already has a single query element in memory

### `parse_batch_query(filename)`
Purpose: parse a GCAM query XML file into a list of `Query` objects.

Use it when:
- the user has `Main_queries.xml` or another query file
- they want to run one or more existing GCAM queries programmatically

Minimal pattern:
```python
from gcamreader import parse_batch_query

queries = parse_batch_query("Main_queries.xml")
first_query = queries[0]
print(first_query.title)
```

### `LocalDBConn(dbpath, dbfile, suppress_gabble=True, miclasspath=None, validatedb=True, maxMemory='4g')`
Purpose: open a local BaseX-backed GCAM database through the bundled ModelInterface / BaseX Java flow.

Important arguments:
- `dbpath`: parent directory containing the `*.basex` files
- `dbfile`: database directory name
- `suppress_gabble`: whether to suppress ModelInterface chatter
- `miclasspath`: optional Java classpath override; default points to the package-bundled ModelInterface files
- `validatedb`: if `True`, immediately runs a scenario-list query to prove the DB works
- `maxMemory`: Java heap cap passed as `-Xmx...`

Important behavior:
- with `validatedb=True`, construction fails early if the database cannot be queried
- the constructor prints discovered scenario names on success

### `RemoteDBConn(dbfile, username, password, address='localhost', port=8984, validatedb=True)`
Purpose: run the same query flow against a remote BaseX REST endpoint.

Use it when:
- the database is hosted on a server
- the user already has BaseX REST credentials

Important behavior:
- query execution happens through HTTP POST to `/rest/<dbfile>`
- `validatedb=True` performs the same early scenario-list check as the local connection

### `conn.runQuery(query, scenarios=None, regions=None, warn_empty=True)`
Available on both `LocalDBConn` and `RemoteDBConn`.

Purpose: execute one `Query` and return a Pandas DataFrame, or `None` for an empty result.

Filtering rules:
- `scenarios=None`: use the last scenario in the database
- `regions=None`: respect the region filters parsed from the query XML
- `regions=[]`: remove region filtering entirely

Returned DataFrame behavior:
- if the parsed CSV contains a `value` column, `gcamreader` groups by every other column and sums `value`
- if the output is scenario metadata rather than a value table, no grouping is applied
- empty query output returns `None`

### `conn.listScenariosInDB()`
Purpose: inspect available scenarios before querying.

Returned columns:
- `name`
- `date`
- `version`
- `fqName` = `name + " " + date`

Use `fqName` when a short scenario name is ambiguous.

### `importdata(dbspec, queries, scenarios=None, regions=None, warn_empty=False, suppress_gabble=True, miclasspath=None)`
Purpose: run a list of queries and get a Python dictionary keyed by query title.

Convenience behavior:
- `dbspec` can be an existing connection object or a string path to a local GCAM database
- `queries` can be a query filename or the output of `parse_batch_query(...)`

Use it when:
- the user wants multiple query results in one Python call
- CSV files are not required yet

## CLI Surface
`gcamreader` exposes two main commands through `gcamreader/cli.py`.

### Local DB
```bash
gcamreader local \
  --database_path <path/to/database_dir> \
  --query_path <path/to/Main_queries.xml> \
  --output_path <output_dir> \
  --force true
```

### Remote DB
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

CLI output behavior:
- output files are named from `query.title`
- CSV files are written with `|` separators
- the output directory must already exist

## Minimal Python Workflows

### Local database to DataFrame
```python
from gcamreader import LocalDBConn, parse_batch_query

db_parent = r"<GCAM Workspace>/output"
db_name = "database_basexdb"
conn = LocalDBConn(db_parent, db_name)
query = parse_batch_query(r"<GCAM Workspace>/output/queries/Main_queries.xml")[0]
df = conn.runQuery(query, scenarios=["Reference"], regions=["China"])
```

### Multiple queries with one call
```python
from gcamreader import importdata

results = importdata(
    r"<GCAM Workspace>/output/database_basexdb",
    r"<GCAM Workspace>/output/queries/Main_queries.xml",
    scenarios=["Reference"],
    regions=["USA"],
)

for title, df in results.items():
    if df is not None:
        print(title, df.shape)
```

## Failure Patterns
- constructor fails immediately:
  likely bad `dbpath` / `dbfile`, unreadable `*.basex` files, or broken Java / BaseX setup
- `subprocess.CalledProcessError` during local query:
  usually bad Java classpath, insufficient heap, or ModelInterface / BaseX runtime failure
- remote HTTP failure:
  usually wrong credentials, wrong database name, or BaseX REST not exposed on the expected host and port
- empty result:
  `runQuery(...)` returns `None`; check scenario name, region filters, and whether the query matches the selected version
- wrong database path in CLI:
  `database_path` should be the directory that directly contains the `*.basex` files

## Practical Agent Rules
- Start with `listScenariosInDB()` before guessing scenario names.
- Prefer the CLI for bulk export and the Python API for chained analysis.
- Do not promise a `run_query()` helper that upstream does not provide.
- If the user already has GCAM-native query XML and wants exact upstream parity, `query_automation.md` plus headless ModelInterface may still be the safer route.

## Authoring Basis
- `gcamreader/README.md`
- `gcamreader/gcamreader/querymi.py`
- `gcamreader/gcamreader/cli.py`
- `gcamreader/gcamreader/tests/test_querymi.py`
