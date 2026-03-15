# Inputs and Outputs

Skill-bundled baseline summary of the main GCAM input and output classes.

Use this file after version routing. Fine-grained page structure and exact taxonomy changed over time, but these groupings are the stable starting point.

## Inputs Overview
GCAM inputs are organized by module and by historical vs. future assumptions. Supply and demand inputs must be globally consistent in historical periods.

### Energy Inputs (Examples)
- Historical supply and demand from IEA balances.
- Technology costs, efficiencies, and retirement rules.
- Logit exponents and share-weight interpolation rules.
- Emissions factors and historical emissions (CO2 and non-CO2).

### Economy Inputs
- Population, labor productivity, labor force participation, and base-year GDP.
- Historical national accounts and savings behavior.
- SSP-aligned or other user-defined socioeconomic pathways.

### Water Inputs (Examples)
- Surface and groundwater supply curves.
- Desalination costs.
- Water coefficients for agriculture, manufacturing, power cooling, and municipal use.

### Agriculture and Land Inputs (Examples)
- FAO production, harvested area, and livestock data.
- Moirai land data for basin-scale calibration.
- Productivity growth and food demand parameters.

### Shared Structure Inputs
- Region, basin, and GLU mappings.
- Scenario component ordering.
- Policy XML files and linked market definitions.
- Data-system outputs that materialize raw source data into GCAM-ready XML.

## Outputs Overview
GCAM outputs are stored in the BaseX XML database and exposed via queries.

### Quantity Outputs
- `physical-output` (technology-level outputs)
- `demand-physical` (technology inputs)
- `supply` and `demand` by market
- Activity, service, and transformation outputs by sector and technology

### Price Outputs
- `price` for all markets
- `price-paid` for food demand
- Policy shadow prices and linked market prices where applicable

### Emissions Outputs
- `emissions` for CO2 and non-CO2 by technology
- `land-use-change-emission` for LUC
- `emissions-sequestered` for CO2 sequestration
- Climate and radiative forcing outputs via Hector-linked queries

### Land Outputs
- `land-allocation` (GLU and land leaf)
- Carbon stock and carbon change
- `profit-rate` by land leaf

### Trade Outputs
Trade is inferred from production vs. consumption. GCAM uses Armington-style trade with separate domestic/import technologies and traded sectors.

## Practical Notes
- Query XML files define the exact aggregation and filtering logic; output interpretation depends heavily on query choice.
- Prefer headless extraction paths such as ModelInterface batch mode, `gcamreader`, `rgcam`, or `gcamextractor` when querying the BaseX database.
- When the user asks for a specific variable, identify the query family first before explaining the number.

## Historical Notes
- Earlier releases expose many of the same concepts with different query names or page organization.
- `v8.2` root docs are the bundled current full-topic baseline for this summary.
