# Solver (Configuration and Diagnostics)

Use this file after version routing.

`v8.2` root docs are the bundled current baseline for solver guidance in this skill. If the user asks about historical solver component names, deprecated algorithms, or release-specific solver behavior, route to the exact version before reusing this summary.

This shared doc is intentionally CLI-first and configuration-first. Use it to edit solver XML, interpret solver failures, and decide what to inspect next. Do not default to GUI tooling.

## Purpose
GCAM solves for a vector of prices that clears markets and satisfies consistency conditions. In practice, agent work usually means:

1. Find the active scenario configuration.
2. Resolve which solver XML that scenario actually points to.
3. Inspect logs for calibration or solve failures.
4. Edit the active solver configuration conservatively.
5. Re-run and compare the failure mode.

Inspect `exe/logs/main_log.txt` or the console output before editing solver settings. Many apparent solver failures are actually caused by configuration, data, or calibration problems upstream.

## Agent Workflow
### 1. Find the active solver file
Start from the scenario configuration that is actually being run, then locate the `solver_config` entry:

```xml
<Value name="solver_config">../input/solution/cal_solver_config.xml</Value>
```

Edit the active solver configuration referenced by the scenario, not a random example file and not the reference configuration unless it is the one actually in use.

### 2. Classify the failure before changing anything
- Parse failure: XML or path problem before the model really starts.
- Calibration failure: supply and demand do not balance in calibration periods.
- Solver failure: GCAM reaches runtime solving but cannot converge within the configured limits.

If the log says `Model did not calibrate successfully in period...`, treat it as a calibration/data issue first, not a pure solver-tuning problem.

If the log says `Model did not solve within set iteration...`, continue with the solver checks below.

### 3. Change one thing at a time
Make one solver change at a time. GCAM solver behavior is path-dependent enough that changing tolerances, filters, and algorithm order all at once makes diagnosis worse.

### 4. Prefer XML edits and reruns
The default agent path is:
- inspect config XML
- inspect solver XML
- inspect logs
- rerun headlessly
- compare the new failure mode

Cross-reference `configuration_workflows.md` for safe XML editing and `running_gcam.md` for headless rerun patterns.

## Core Algorithms
### Bisection
Use bisection to move the model toward a solvable region when initial guesses are poor or the Jacobian is effectively singular. It is useful for bracketing behavior and for pushing difficult markets away from extreme-price regimes.

Important parameters:
- `bracket-interval`
- `max-bracket-iterations`
- `max-iterations`
- `solution-info-filter`

### Broyden
Broyden is the main modern solver. In modern families, Broyden should always remain in the configured solver sequence because it is the component that actually drives the system to a solution.

Important parameters:
- `ftol`
- `max-iterations`
- `solution-info-filter`

Operational meaning:
- If convergence stalls, the issue may be bad filters, extreme prices, or invalid local derivatives.
- Increasing iteration counts may help, but it is usually not the first thing to change if the problem is structural.

### Preconditioner
Use the preconditioner to move bad initial guesses back into a numerically safer region before Broyden runs. This is especially relevant when prices are far outside normal operating ranges.

Important parameters:
- `max-iterations`
- `ftol`
- `solution-info-filter`

### Newton-Raphson
Newton-Raphson is historical in GCAM. Modern guidance treats it as deprecated in favor of Broyden, but older releases use Newton-Raphson-centered terminology and filters.

Do not assume a Newton-Raphson-specific block from `v3.2` maps one-to-one onto a modern `v8.2` solver configuration. Route the exact version first when the user asks about historical solver XML.

## Common Solver XML Structure
Solver XML is organized by `user-configurable-solver` blocks, usually keyed by year:

```xml
<user-configurable-solver year="2025" fillout="1">
    <solution-tolerance>0.001</solution-tolerance>
    <solution-floor>0.0001</solution-floor>
    <calibration-tolerance>0.01</calibration-tolerance>
    <max-model-calcs>2500</max-model-calcs>
</user-configurable-solver>
```

Typical general controls:
- `solution-tolerance`: relative excess-demand threshold
- `solution-floor`: absolute excess-demand floor for tiny markets
- `calibration-tolerance`: allowed mismatch during calibration
- `max-model-calcs`: total model evaluations allowed
- `fillout="1"`: continue this block forward to later years until another block overrides it

The solver components inside a block run in sequence. Order matters.

## Market Filters
Solver blocks and components often target only part of the market set.

Common predicates:
- `solvable`
- `solvable-nr`
- `unsolved`
- `market-type="Tax"`
- `market-name="..."`

Predicates can be combined with logical operators such as `&&`, `||`, and `!`.

Use filters to keep numerically problematic markets away from the wrong algorithm rather than trying to solve everything with one aggressive component.

## Practical Troubleshooting
### When GCAM does not solve
- Double-check that the intended scenario configuration and solver XML are actually the files being used.
- Verify the problem is not a parse or calibration failure first.
- Use `input/extra/supply_demand_curves.xml` when available to inspect problematic markets; discontinuities and near-vertical curves are hard to solve.
- Increase iteration limits only after confirming the issue is not caused by impossible configuration or bad data.
- Check whether a market filter is excluding the wrong markets or sending unstable markets into the wrong component.
- Keep Broyden in the modern solver sequence.

### When target finder or policy runs behave badly
Some failures that look like generic solver problems are actually scenario-setup problems. For example, target-finder workflows can degrade if the required policy market was never created. Diagnose the policy/configuration path before over-tuning the solver.

### When extreme prices appear
Extreme prices often imply near-zero derivatives or saturated supply/demand responses. That usually means:
- preconditioning may help
- bisection may help bring the system back toward a better region
- blindly tightening tolerances usually will not help

## Version Notes
- `v8.2` root docs are the bundled current baseline for solver interpretation in this skill.
- `v5.4` through `v8.2` are the closest historical families to this modern Broyden-centered summary.
- `v3.2` uses Newton-Raphson-centered terminology such as `solvable-nr`, and the surrounding solver guidance is historically different.
- If the user asks for exact solver component names, XML block names, or historical filter semantics, route to the exact version page bundle before answering.

## Escalation Rule
If conservative solver edits do not change the failure mode, stop assuming it is a tuning issue. Inspect scenario configuration, policy inputs, calibration data, and any recent XML edits before continuing to tune the solver.
