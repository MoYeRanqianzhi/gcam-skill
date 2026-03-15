# Running GCAM (Quickstart + Advanced)

Skill-bundled baseline operational summary for running GCAM scenarios.

Use this file after version routing. `v8.2` is the bundled full-topic baseline. Older versions may use different workspace layouts, different packaging, or earlier database workflows.

## Quickstart (Reference Scenario)
1. Ensure the GCAM executable workspace contains a valid `configuration.xml`.
2. Start from `configuration_ref.xml` for a reference run or `configuration_policy.xml` for a policy run.
3. Launch the platform run script or the executable directly.
4. Inspect `exe/logs/main_log.txt` while the run proceeds.
5. Treat the run as successful only when you see both of these terminal states:
   - `Starting output to XML Database.`
   - `Model run completed.`

Resource note:
- Reference scenarios can require many GB of RAM and multi-GB output storage.
- Target-finder and large batch workflows increase both wall-clock time and output volume materially.

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
- When debugging scenario behavior, inspect component order first. Many apparent model issues are actually override-order mistakes.

## Batch Mode
Batch mode runs multiple file combinations from one configuration.

Typical pattern:
- Set `BatchMode=1`.
- Point `<BatchFileName>` to a batch XML.
- Define `FileSet` permutations that append or swap XML components per scenario.
- Keep scenario names explicit so output DB contents remain traceable.

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

## ModelInterface and Querying
ModelInterface remains the standard interactive query tool for BaseX outputs.

Typical flow:
1. Open the BaseX database directory in `output/`.
2. Select scenario and query XML.
3. Run interactive or batch queries.

Useful modes:
- interactive browsing of scenario/query combinations
- batch query execution to files
- Java command-line automation for headless extraction
- exporting data for R or Python workflows

## Controlling XML DB Output
GCAM can reduce or reshape XML DB output volume.

Typical controls include:
- in-memory DB mode for speed
- output filters to limit stored results
- post-run batch queries
- exported XML plus later import through XMLDBDriver

If the user complains about output size or I/O time, inspect XML DB output settings before changing the model itself.

## Common Failure Modes
- Immediate startup failure usually indicates missing files, bad paths, or invalid XML.
- Failure while reading `ScenarioComponents` usually indicates malformed XML or incorrect object ordering.
- Failure after parsing but before solution usually indicates configuration inconsistency or missing linked inputs.
- Solver failure during periods points to market or calibration issues; inspect `solver.md`.
- Java/BaseX output errors often come from runtime Java configuration rather than core model logic.

## Historical Caution
- `v3.2` and early `v4.x` use older run packaging and different documentation terminology.
- `v5.4+` aligns more closely with the skill-bundled baseline operating pattern.
- When the user asks about an exact historical release package, trust the version route file first and use this page only as a modernized operational scaffold.
