# Outputs from Emissions Modeling

Bundled adapted source page for GCAM `v7.0`.

- Source root: `gcam-doc/v7.0`
- Source path: `outputs_emissions.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v7.0/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Description of Outputs

| Name | Resolution | Unit | Query | XML Tag |
| :--- | :--- | :--- | :--- | :--- |
|Emissions (CO2)|Technology, Region [3](#table_footnote), and Year|MtC/year|<a name="CO2 emissions by tech (excluding resource production)"></a>CO2 emissions by tech (excluding resource production)|`emissions`|
| Emissions (non-CO2) [1,2](#table_footnote) |  Technology, Region [3](#table_footnote), and Year | Various [4](#table_footnote)  | <a name="nonCO2 emissions by tech (excluding resource production)"></a>nonCO2 emissions by tech (excluding resource production) | `emissions` |
|Resource production emissions (CO2)|Subresource, Region, and Year|MtC/year|<a name="CO2 emissions by resource production"></a>CO2 emissions by resource production|`emissions`|
|Resource production emissions (non-CO2)|Subresource, Region, and Year|MtC/year|<a name="CO2 emissions by resource production"></a>nonCO2 emissions by resource production|`emissions`|
| Land use change emissions | By GLU and land type | MtC / year | <a name="LUC emissions by region"></a>LUC emissions by region | `land-use-change-emission` |
| Change in above ground carbon | By GLU and land type | MtC / year |  | `above-land-use-change-emission`|
| Change in below ground carbon | By GLU and land type | MtC / year |  | `below-land-use-change-emission`|
| CO2 Sequestration [6](#table_footnote) |  Technology, Region [3](#table_footnote), and Year | MtC / year  | <a name="CO2 sequestration by tech"></a>CO2 sequestration by tech | `emissions-sequestered` |

Outputs are specified in the `startVisitGHG` [5](#table_footnote) and `startVisitCarbonCalc` methods of [xml_db_outputter.cpp](https://github.com/JGCRI/gcam-core/blob/master/cvs/objects/reporting/source/xml_db_outputter.cpp).

Note that the query "CO2 emissions by region" represents gross CO2 emissions for a region and is equal to the sum of all emissions from "CO2 emissions by tech (excluding resource production)" and all emissions from "CO2 emissions by resource production". A region's net CO2 emissions can be calculated by adding "CO2 emissions by region" and "LUC emissions by region".

<a name="table_footnote"></a>1: A full list of gases included in GCAM is provided on the [emissions page](emissions.md#iamc-reference-card).

<a name="table_footnote"></a>2: There is a long list of standard queries that report emissions outputs. The "nonCO2 emissions by tech (excluding resource production)"  and "CO2 emissions by tech (excluding resource production)" queries listed above will report all emissions except for land use change CO2 and emissions from resource production at the technology level. The other queries filter or aggregate those outputs. For example, the "CO2 emissions by region" query aggregates *emissions* to the region level for fossil fuel and industrial CO2 only.

<a name="table_footnote"></a>3: Emissions are reported at the regional resolution of the sector. See [Regional Resolution](common_assumptions.md#regional-resolution)

<a name="table_footnote"></a>4: Units vary. Fluorinated gas emissions are reported in Gg of the specific gas per year. All other emissions are reported in Tg of the specific gas per year (e.g., CH4 emissions are reported in TgCH4 / yr).

<a name="table_footnote"></a>5: While the method is called *startVisitGHG*, it includes non-GHG emissions. However, land use change CO2 emissions are not included in this method.

<a name="table_footnote"></a>6: There are two emissions sequestration queries. The "CO2 sequestration by tech" query listed above will return CO2 sequestration by technology, while "CO2 sequestration by sector" aggregates this to the sector level.
