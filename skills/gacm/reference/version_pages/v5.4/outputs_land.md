# Outputs from the Land Model

Bundled adapted source page for GCAM `v5.4`.

- Source root: `gcam-doc/v5.4`
- Source path: `outputs_land.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v5.4/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Description of Outputs

| Name | Resolution | Unit | Query | XML Tag |
| :--- | :--- | :--- | :--- | :--- |
| Land use and land cover | By GLU, land leaf, and year | thousand $$km^2$$ | <a name="detailed land allocation"></a>detailed land allocation or <a name="aggregated land allocation"></a>aggregated land allocation [1](#table_footnote)| `land-allocation` |
| Land use change emissions | By GLU and land leaf | MtC / year | <a name="LUC emissions by region"></a>LUC emissions by region | `land-use-change-emission` |
| Change in above ground carbon | By GLU and land leaf | MtC / year |  | `above-land-use-change-emission`|
| Change in below ground carbon | By GLU and land leaf | MtC / year |  | `below-land-use-change-emission`|
| Above ground carbon stock | By GLU and land leaf | MtC | <a name="vegetative carbon stock by region"></a>vegetative carbon stock by region | `above-ground-carbon-stock` |
| Profit rate | By GLU and land leaf | 1975$/thous km^2 | <a name="profit rate"></a>profit rate | `profit-rate` |

Outputs are specified in the `startVisitLandLeaf` and `startVisitCarbonCalc` methods of [xml_db_outputter.cpp](https://github.com/JGCRI/gcam-core/blob/master/cvs/objects/reporting/source/xml_db_outputter.cpp).

<a name="table_footnote"></a>1: There is a long list of standard queries that report land allocation outputs. The "detailed land allocation" query will list land for every single land leaf and region combo (see [land nesting](details_land.md#land-nesting-strategy) for a complete list of land leafs). The "aggregated land allocation" query listed above will aggregate land into 12 categories (e.g., crops, biomass, etc.). There are also queries that will return land allocation for an individual GLU ("land allocation in a specified land use region") or total land by crop ("land allocation by land crop").
