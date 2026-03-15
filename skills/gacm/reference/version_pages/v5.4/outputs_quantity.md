# Quantity Outputs

Bundled adapted source page for GCAM `v5.4`.

- Source root: `gcam-doc/v5.4`
- Source path: `outputs_quantity.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v5.4/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Description of Outputs

| Name | Resolution | Unit | Query | XML Tag |
| :--- | :--- | :--- | :--- | :--- |
| Physical Output [1](#table_footnote) | Technology, Region [2](#table_footnote), Vintage, and Year  | Various [3](#table_footnote) | <a name="outputs by tech"></a>outputs by tech | `physical-output` |
| Resource Production | Region, Resource and Year   | Various [3](#table_footnote) | <a name="resource production"></a>resource production | `output` |
| Inputs [1](#table_footnote) | Technology, Input, Region [2](#table_footnote), Vintage, and Year    | Various [3](#table_footnote) | <a name="inputs by tech"></a>inputs by tech | `demand-physical` |
| Supply | Market [4](#table_footnote) and Year   | Various [3](#table_footnote) | <a name="supply of all markets"></a>supply of all markets | `supply` |
| Demand | Market [4](#table_footnote) and Year   | Various [3](#table_footnote) | <a name="demand of all markets"></a>demand of all markets | `demand` |

Outputs are specified in the `startVisitOutput`, `startVisitResource`, `startVisitInput`, and `startVisitMarket` methods of [xml_db_outputter.cpp](https://github.com/JGCRI/gcam-core/blob/master/cvs/objects/reporting/source/xml_db_outputter.cpp).

<a name="table_footnote"></a>1: There is a long list of standard queries that report quantity outputs. The "physical output" query listed above will report all outputs at the technology level. The "inputs" query listed above will report all inputs to each technology. The other queries filter or aggregate those outputs. For example, the "outputs by sector" query aggregates *physical-output* to the sector level; the "elec gen by gen tech" query filters the *physical-output* for electricity generating technologies. The "primary energy consumption by region (direct equivalent)" aggregates all energy-related inputs, providing a total energy consumption by fuel, region, and year.

<a name="table_footnote"></a>2: Outputs are reported at the regional resolution of the sector. See [Regional Resolution](common_assumptions.md#regional-resolution)

<a name="table_footnote"></a>3: Units vary. In general, energy-related outputs are reported in EJ/yr, agricultural outputs are in Mt/yr, forestry outputs are in million m^3/yr, and water outputs are in km^3/yr.

<a name="table_footnote"></a>4: Supply and demand can be reported by market. The market name contains both region and commodity information. For example, *globalcrude oil* is the globally traded crude oil market and *USACorn* is Corn market in the USA. Some markets will have both a global and a regional supply or demand.
