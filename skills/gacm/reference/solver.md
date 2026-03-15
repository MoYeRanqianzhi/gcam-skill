# Solver Summary

Bundled summary of GCAM solver behavior.

Use this file after version routing.

## Purpose
GCAM solves for a price vector that clears markets by finding the root of the excess demand function.

## Solver Components
- **Bisection**: robust for initial bracketing; helps move toward solution.
- **Broyden**: primary solver that can converge to a solution; should always be included.
- **Preconditioner**: adjusts initial guesses to avoid singular regions.
- **Newton-Raphson**: deprecated.

## Solver Configuration
Solver settings are defined in a solver configuration file referenced from the main configuration:
`<Value name="solver_config">../input/solution/cal_solver_config.xml</Value>`

Each `user-configurable-solver` block defines:
- General parameters (tolerances, max evaluations).
- Ordered solver components with their own parameters.
- Solution-info filters to select markets.

## Market Filters (Examples)
Predicates like `solvable`, `solvable-nr`, `market-type="Tax"` can be combined with logical operators.
