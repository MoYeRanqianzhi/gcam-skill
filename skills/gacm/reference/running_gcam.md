# Running GCAM (CLI First)

Skill-bundled operational summary for running GCAM scenarios without relying on GUI steps.

Use this file after version routing. `v8.2` is the bundled full-topic baseline. Older versions may use different workspace layouts, packaging, or database conventions, so keep the exact version route in scope.

Open `configuration_workflows.md` for deeper configuration editing patterns, `query_automation.md` for headless extraction details, and `workspace_layouts.md` when the user provides real paths.

## Default Execution Pattern
For agent use, prefer one of these command-line paths:

1. Direct executable invocation for scripted runs:
   - `gcam.exe -C configuration_ref.xml`
   - or the equivalent platform executable with `-C <config>`
2. Release-package wrapper scripts from a shell:
   - `run-gcam`
   - `run-gcam.bat`
   - `run-gcam.command`

Treat double-click instructions in upstream user guides as historical packaging notes, not as the recommended workflow.

## Quickstart (Reference Scenario)
1. Ensure the executable workspace contains the required support files such as `log_conf.xml`.
2. Pick the correct configuration file:
   - `configuration_ref.xml` for a reference run
   - `configuration_policy.xml` for policy or target-finder workflows
3. Run GCAM from the command line.
4. Inspect `exe/logs/main_log.txt` while the run proceeds.
5. Treat the run as successful only when the log reaches both:
   - `Starting output to XML Database.`
   - `Model run completed.`

Resource note:
- Reference scenarios can require many GB of RAM and multi-GB output storage.
- Target-finder and large batch workflows materially increase wall-clock time and output volume.

## Configuration File Structure
The configuration file is the operational control surface for a run.

Key sections:
- `<Files>`: input XML locations, XML DB path, batch file, target file, query support files
- `<ScenarioComponents>`: ordered XML include list; later components override earlier inputs
- `<Strings>`: scenario names, diagnostics strings, climate-related file strings
- `<Bools>`: batch mode, target-finder mode, XML DB options, output controls
- `<Ints>`: model period controls, restart behavior, and related integer options

## ScenarioComponents Rules
- Do not edit canonical reference XML files in place if you want reproducible comparisons.
- Create add-on XML files and append them late in `ScenarioComponents` so they override base assumptions.
- When debugging scenario behavior, inspect component order first. Many apparent model issues are override-order mistakes.

## Batch Mode
Batch mode runs multiple file combinations from one configuration.

Typical pattern:
- Set `BatchMode=1`.
- Point the batch-file setting at a batch XML.
- Define `FileSet` permutations that append or swap XML components per scenario.
- Keep scenario names explicit so output database contents remain traceable.

## Target Finder
Target finder solves for a price path that reaches a climate target.

Operational cues:
- Start from `configuration_policy.xml`.
- Enable `find-path`.
- Provide a `policy-target-file`.
- Expect multiple reruns while GCAM searches for a price path.

Common target styles:
- concentration
- radiative forcing
- temperature
- cumulative emissions

## Query Results Without GUI
For agent workflows, prefer headless extraction.

### Path 1: Post-run automatic batch queries
Use the `XMLDBDriver` properties file in `exe/` to run queries immediately after a scenario completes.

Relevant keys from the bundled v8.2 user guide:
- `in-memory`
- `open-db-wait`
- `filter-script`
- `batch-queries`
- `batch-logfile`

This path is useful when you want CSV outputs and do not want to keep the full XML database permanently.

### Path 2: Headless ModelInterface batch mode
When the query XML already exists, invoke ModelInterface without a UI:

```bash
java -cp "$CLASSPATH" ModelInterface/InterfaceMain -b batch_queries/xmldb_batch.xml
```

Use this as a batch-query engine, not as an interactive GUI walkthrough.

### Path 3: Extraction libraries
If the task is post-processing rather than raw query authoring, prefer:
- `gcamreader` for Python-first CSV/DataFrame workflows
- `rgcam` for R project-data extraction
- `gcamextractor` for standardized extracted tables and aggregations

Open `tools.md` for tool selection and examples.

## Controlling XML DB Output
GCAM can reduce or reshape XML DB output volume.

Typical controls include:
- in-memory DB mode for speed
- output filters to limit stored results
- post-run batch queries
- writing `debug_db.xml` or other intermediate artifacts for later processing

If the user complains about output size or I/O time, inspect XML DB output settings before changing the model itself.

## Common Failure Modes
- Immediate startup failure usually indicates missing files, bad paths, or invalid XML.
- Failure while reading `ScenarioComponents` usually indicates malformed XML or incorrect object ordering.
- Failure after parsing but before solution usually indicates configuration inconsistency or missing linked inputs.
- Solver failure during periods points to market or calibration issues; inspect `solver.md`.
- Java/BaseX output errors often come from runtime Java configuration rather than core model logic.
- On Windows, `run-gcam.bat` issues often reduce to incorrect `JAVA_HOME`, missing `jvm.dll`, or wrong Java bitness.

## Historical Caution
- `v3.2` and early `v4.x` use older run packaging and different documentation terminology.
- `v5.4+` aligns more closely with the skill-bundled baseline operating pattern.
- Exact historical page bundles may still describe ModelInterface GUI usage. Translate those into CLI/config equivalents unless the user explicitly asks for the historical UI path.
