# Configuration Workflows

Agent-first guide to editing GCAM runtime configuration files and related XML control files.

Open this file when the task is about:
- modifying `configuration_ref.xml` or `configuration_policy.xml`
- changing scenario composition
- enabling batch mode or target finder
- changing output database paths, debug files, or early-stop behavior
- diagnosing configuration-driven run failures

## Safe Edit Cycle
1. Start from the closest stock configuration file instead of editing ad hoc.
2. Rename or clone files for the scenario you are creating.
3. Change `scenarioName` early so outputs remain traceable.
4. Add override XML files late in `ScenarioComponents`.
5. Run the smallest useful test first:
   - set `stop-period` if you only need an early-period smoke test
   - keep one change per run when debugging
6. Read `exe/logs/main_log.txt` before changing solver settings.

## Core Files To Recognize
- `configuration_ref.xml`: reference scenario baseline
- `configuration_policy.xml`: policy and target-finder baseline
- `policy-target-file`: separate target-finder control file
- solver configuration file referenced from the main configuration

Open `solver.md` for solver-specific tuning and `policies_scenarios.md` for policy semantics.

## Main Configuration Sections

### `<Files>`
Most common operational edits:
- `xmldb-location`: move or rename the output XML database
- `BatchFileName`: point to a GCAM batch file
- `policy-target-file`: enable target finder with a policy target file
- `batchCSVOutputFile`: write minimal CSV output for large batch runs
- `xmlDebugFileName`: enable region-specific debug output

Operational rule:
- Path mistakes in `XMLInputFileName` or `BatchFileName` are a common cause of immediate startup failures.

### `<ScenarioComponents>`
This is the ordered scenario definition.

Rules:
- Do not edit canonical stock components in place if you want reproducible comparisons.
- Add project-specific XML files at the end so later values override earlier values.
- The `name` attribute is for human readability only; the file path drives behavior.
- If parsing fails while reading a scenario component, suspect file-not-found or malformed XML first.

Typical use:
- append a climate policy XML from `input/policy`
- append a project-specific override XML
- selectively include optional XMLs such as extra technology assumptions that are not in the default configuration

### `<Strings>`
Most common edits:
- `scenarioName`
- `debug-region`

Use short, stable names. Batch mode appends `FileSet` suffixes to `scenarioName`, so keep the prefix concise.

### `<Bools>`
High-value switches:
- `CalibrationActive`
- `FixedGDP-Path`
- `BatchMode`
- `find-path`
- `createCostCurve`
- `QuitFirstFailure`

Operational cautions:
- `BatchMode=1` is inert unless `BatchFileName` is valid.
- `find-path=1` is inert unless `policy-target-file` is valid.
- Target finder should start from `configuration_policy.xml`, not the reference configuration.

### `<Ints>`
Most useful runtime controls:
- `stop-period`
- `restart-period`
- `carbon-output-start-year`
- `climateOutputInterval`
- `parallel-grain-size`

Practical uses:
- `stop-period` for smoke tests or fast failure reproduction
- `restart-period` for checkpoint-style reruns and target-finder acceleration

## Common Edit Patterns

### Add a Policy Scenario
1. Clone `configuration_policy.xml`.
2. Set `scenarioName`.
3. Append the policy XML late in `ScenarioComponents`.
4. Keep the base reference components unchanged.

### Run Multiple Scenario Variants
1. Keep shared components in the main configuration.
2. Put scenario-specific permutations in a GCAM batch file.
3. Turn on `BatchMode`.

### Run Target Finder
1. Start from `configuration_policy.xml`.
2. Set `find-path=1`.
3. Provide `policy-target-file`.
4. If convergence is slow, improve the target file's `initial-tax-guess` before touching solver complexity.

### Reduce Cost During Debugging
1. Set `stop-period` to the earliest period that reproduces the problem.
2. Use `batchCSVOutputFile` or filtered XML DB output if full database output is not needed.
3. Set `QuitFirstFailure=1` when target finder is not in use.

## Failure Signatures To Recognize
- Immediate crash after `Parsing input files...`:
  likely path or missing-input issue
- Crash while reading a specific scenario component:
  likely malformed XML or bad file path
- Post-parse failure before period 1:
  likely missing technology, bad naming, or inconsistent object references
- Target-finder warning about explicitly creating a CO2 market:
  read in a zero-tax or equivalent policy file so dependencies exist

## Version Notes

### `v5.4` through `v8.2`
- This is the closest family to the shared bundled workflow in this file.
- Use `<GCAM Workspace>` style paths.
- Expect `configuration_ref.xml`, `configuration_policy.xml`, BaseX output, and modern batch/query examples.

### `v4.2` through `v5.3`
- The same major sections and workflows exist, but docs are more ModelInterface-centric.
- BaseX and query automation are still documented, but Java and path details are older.

### `v3.2`
- Treat as a legacy family with older packaging and more inherited pages in the bundle.
- Source/build docs explicitly document direct execution such as `./gcam.exe -C<alternative configuration file>`.
- If the user provides a real legacy workspace, inspect it before assuming modern path conventions.
