# Outputs from Emissions Modeling

Bundled adapted source page for GCAM `v7.1`.

- Source root: `gcam-doc/v7.1`
- Source path: `outputs_emissions.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v7.1/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Description of Outputs

| Name | Resolution | Unit | Query | XML Tag |
| :--- | :--- | :--- | :--- | :--- |
|Emissions (CO<sub>2</sub>)|Technology, Region<sup>[3](#table_footnote)</sup>, and Year|MtC/year|CO2 emissions by tech (excluding resource production)|`emissions`|
| Emissions (non-CO<sub>2</sub>)<sup>[1,2](#table_footnote)</sup> |  Technology, Region<sup>[3](#table_footnote)</sup>, and Year | Various<sup>[4](#table_footnote)</sup>  | nonCO2 emissions by tech (excluding resource production) | `emissions` |
|Resource production emissions (CO<sub>2</sub>)|Subresource, Region, and Year|MtC/year|CO2 emissions by resource production|`emissions`|
|Resource production emissions (non-CO<sub>2</sub>)|Subresource, Region, and Year|MtC/year|nonCO2 emissions by resource production|`emissions`|
| Land use change emissions | By GLU and land type | MtC / year | LUC emissions by region | `land-use-change-emission` |
| Change in above ground carbon | By GLU and land type | MtC / year |  | `above-land-use-change-emission`|
| Change in below ground carbon | By GLU and land type | MtC / year |  | `below-land-use-change-emission`|
| CO<sub>2</sub> Sequestration<sup>[6](#table_footnote)</sup> |  Technology, Region<sup>[3](#table_footnote)</sup>, and Year | MtC / year  | CO2 sequestration by tech | `emissions-sequestered` |

Outputs are specified in the `startVisitGHG`<sup>[5](#table_footnote)</sup> and `startVisitCarbonCalc` methods of [xml_db_outputter.cpp](https://github.com/JGCRI/gcam-core/blob/master/cvs/objects/reporting/source/xml_db_outputter.cpp).

Note that the query "CO<sub>2</sub> emissions by region" represents gross CO<sub>2</sub> emissions for a region and is equal to the sum of all emissions from "CO<sub>2</sub> emissions by tech (excluding resource production)" and all emissions from "CO<sub>2</sub> emissions by resource production". A region's net CO<sub>2</sub> emissions can be calculated by adding "CO<sub>2</sub> emissions by region" and "LUC emissions by region".

<a name="table_footnote">1</a>: A full list of gases included in GCAM is provided on the <a href="emissions.md#iamc-reference-card">emissions page</a>.

<a name="table_footnote">2</a>: There is a long list of standard queries that report emissions outputs. The "nonCO2 emissions by tech (excluding resource production)"  and "CO2 emissions by tech (excluding resource production)" queries listed above will report all emissions except for land use change CO<sub>2</sub> and emissions from resource production at the technology level. The other queries filter or aggregate those outputs. For example, the "CO2 emissions by region" query aggregates <i>emissions</i> to the region level for fossil fuel and industrial CO<sub>2</sub> only.

<a name="table_footnote">3</a>: Emissions are reported at the regional resolution of the sector. See <a href="common_assumptions.md#regional-resolution">Regional Resolution</a>

<a name="table_footnote">4</a>: Units vary. Fluorinated gas emissions are reported in Gg of the specific gas per year. All other emissions are reported in Tg of the specific gas per year (e.g., CH<sub>4</sub> emissions are reported in TgCH<sub>4</sub> / yr).

<a name="table_footnote">5</a>: While the method is called <i>startVisitGHG</i>, it includes non-GHG emissions. However, land use change CO<sub>2</sub> emissions are not included in this method.

<a name="table_footnote">6</a>: There are two emissions sequestration queries. The "CO2 sequestration by tech" query listed above will return CO<sub>2</sub> sequestration by technology, while "CO2 sequestration by sector" aggregates this to the sector level.
