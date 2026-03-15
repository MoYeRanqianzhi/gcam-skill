# Economy

Skill-bundled topic reference for socioeconomic drivers, GDP formation, GCAM-macro, and economic interpretation.

Use this file after version routing when the user asks about GDP assumptions, macro coupling, savings, SAM consistency, or how economic activity feeds other GCAM modules.

## Core Role
The economy block sets the scale of demand throughout GCAM through population, productivity, income, and GDP.

At minimum, GCAM uses:
- population
- labor productivity and labor-force assumptions
- base-year GDP and national accounts
- savings and depreciation assumptions

## Older vs Newer Behavior
- Older GCAM generations treated GDP largely as exogenous with limited feedback.
- Modern GCAM includes GCAM-macro, a two-way coupling between the macroeconomy and the energy system.

That distinction matters for cross-version comparisons. If the user asks about endogenous GDP or macro feedbacks, version routing is mandatory.

## GCAM-Macro / KLEM Frame
The modern macro module represents production through a nested structure linking:
- capital
- labor
- energy services
- a materials sector

Key implications:
- energy-system costs can feed back into economic output
- GDP, consumption, and other macro indicators can change directly under scenario perturbations
- macro consistency checks become more important than in the older one-way structure

## Social Accounting Matrix (SAM)
The SAM is a bookkeeping and consistency device.

What it is used for:
- checking row and column consistency
- verifying savings-investment balance
- interpreting factor payments, trade, and macro closure

If the user reports inconsistent macro results, ask whether the issue is conceptual, data-system-related, or a failed solve reflected in the SAM balances.

## Calibration and Inputs
Modern economic calibration typically combines:
- population and national accounts inputs
- historical GDP and savings data
- energy-service expenditures derived from calibrated GCAM energy outputs
- SSP or other future socioeconomic pathways

## Interpreting Economic Costs
GCAM can support several economic interpretations depending on configuration:
- carbon price
- deadweight loss style interpretation
- GDP change
- consumption change

These are not interchangeable. Ask which concept the user needs before comparing scenarios.

## Version Notes
- `v7+` is the key modern macro era in the bundled references.
- Earlier versions should not be described as if they fully share the later two-way macro coupling.
