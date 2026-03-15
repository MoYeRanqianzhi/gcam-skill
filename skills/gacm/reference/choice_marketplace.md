# Choice and Marketplace

Skill-bundled topic reference for GCAM choice functions, market-clearing logic, and marketplace semantics.

Use this file after version routing when the user asks how technologies compete, what share weights do, why prices change, how linked markets work, or what a GCAM market means.

## Choice Indicators
GCAM reduces many discrete technology or land-use choices to a single indicator:
- energy and most technology competition use cost
- land allocation uses profit rate
- some sectors add penalties or adjustments so non-cost preferences can still be represented through the same machinery

## Choice Functions
GCAM primarily uses two discrete-choice formulations:
- `relative-cost-logit` / modified logit
- `absolute-cost-logit` / logit

Key concepts:
- `share weights` calibrate observed historical shares and phase in new technologies
- `logit exponents` or coefficients control how strongly shares respond to cost or profit differences
- land generally uses modified-logit style profit-sharing rather than the more configurable energy-system setup

Interpretation:
- larger absolute sensitivity means stronger switching toward the preferred option
- lower sensitivity preserves more diversity among competing technologies
- modified-logit behavior is ratio-based and is often less aggressive in eliminating expensive technologies

## Market-Clearing Logic
GCAM solves for prices that balance supply and demand in each model period.

Operational meaning:
- a market is the accounting object where supply, demand, and price meet
- the solver iterates on prices until the market residuals are sufficiently small
- carbon and other policy prices propagate through input costs, technology competition, and demand response

Open `solver.md` when the user is asking about the numerical algorithms themselves.

## Marketplace Semantics
The marketplace aggregates:
- energy supplies and demands
- agriculture and land commodities
- water withdrawals and consumption
- policy markets such as carbon or linked GHG prices

Common sources of confusion:
- not every market is globally traded
- some markets are regional, some basin-level, and some global
- shadow prices from constraints are still operationally important even when no explicit commodity is traded in the everyday sense

## Share Weights and Calibration
Share weights do more than fit history:
- they encode region-specific historical structure
- they allow phased market entry for emerging technologies
- they can preserve technologies that would otherwise disappear too abruptly under purely cost-minimizing logic

## Version Notes
- `v3.2` explains these ideas with older terminology and less modular separation.
- `v4.x` introduces more modern structural language but still lacks the full current topic split.
- `v8.2` remains the skill-bundled current full-topic baseline for these concepts.
