# Policies and Scenario Controls

Skill-bundled baseline summary of GCAM policy and scenario control patterns.

Use this file after version routing. Policy expression and support evolved, but these concepts remain the stable bundled baseline for the `v8.2` root doc tree and its nearby modern families.

## Emissions Policies
GCAM supports three primary policy types:
1. Carbon or GHG price paths.
2. Emissions constraints (GCAM solves for the price).
3. Climate constraints (concentration, forcing, temperature, or cumulative emissions).

All policies are implemented by placing a price on emissions, which propagates through the model.

Scenario interpretation:
- Fixed price path: user supplies the price and GCAM computes the resulting emissions.
- Quantity constraint: user supplies the emissions quantity and GCAM solves for the price.
- Climate target: user supplies the climate outcome and GCAM repeatedly searches for a compliant price path.

## Linked Emission Markets
Linked GHG policies connect multiple gas markets (e.g., CH4, N2O) to a CO2 market via `linked-ghg-policy`.
Key parameters:
- `price-adjust` (price conversion)
- `demand-adjust` (unit conversion)

Operational caution:
- Do not create a linked policy before the parent market exists.
- `price-adjust=0` disables economic feedback for that gas while still allowing MAC-style responses if configured.

## Land Use Policies
- Protected lands: remove land from competition.
- Valuing carbon in land: apply carbon price to land-use change CO2.
- Land or bioenergy constraints: set min/max quantity or share and solve for tax/subsidy.

## Energy Production Policies
Quantity or share constraints (e.g., renewable portfolio standards, biofuels mandates) are implemented as constraints that solve for a tax or subsidy.

Common examples:
- renewable generation or fuel-share standards
- bioenergy quantity floors or caps
- land protection percentages
- linked non-CO2 market designs

## Policy Costs
GCAM reports policy costs using a deadweight loss framework tied to CO2 prices. Other cost concepts (GDP loss, EV) are not fully implemented.

## Configuration Tips
- Use `configuration_policy.xml` as the baseline for policy runs.
- For target finder, enable `find-path` and set `policy-target-file`.
- Add policy XMLs as late `ScenarioComponents` to override base data.

## Version Notes
- `v3.2` and early `v4.x` describe similar ideas with different organization and less modular documentation.
- `v5.4+` is the closest structural family to the bundled baseline policy workflow.
- `delta-only` releases should be read as modifications layered onto these baseline policy patterns, not as standalone policy manuals.
