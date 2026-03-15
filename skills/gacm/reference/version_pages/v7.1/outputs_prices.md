# Price Outputs

Bundled adapted source page for GCAM `v7.1`.

- Source root: `gcam-doc/v7.1`
- Source path: `outputs_prices.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v7.1/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Description of Outputs

| Name | Resolution | Unit | Query | XML Tag |
| :--- | :--- | :--- | :--- | :--- |
| Price [1](#table_footnote1) | Market [2](#table_footnote2) and Year  | Various [3](#table_footnote3) | <a name="prices of all markets"></a>prices of all markets | `price` |
| Food demand prices | Region, Type and Year  | 2005$/Mcal/day | <a name="food demand prices"></a>food demand prices | `price-paid` |

Outputs are specified in the `startVisitMarket` method of [xml_db_outputter.cpp](https://github.com/JGCRI/gcam-core/blob/master/cvs/objects/reporting/source/xml_db_outputter.cpp).

<a name="table_footnote1"></a>1: There is a long list of standard queries that report price results. The price query above will report prices for all markets, while other queries filter those results. For example, the "ag commodity prices" query reports prices for agriculture and forestry commodities only.

<a name="table_footnote2"></a>2: Prices are reported by market. The market name contains both region and commodity information. For example, *globalcrude oil* is the price of the globally traded crude oil market and *USACorn* is the price of Corn in the USA. Some markets will have both a global and a regional price.

<a name="table_footnote3"></a>3: Units vary by market. In general, energy-related prices are reported in $1975/GJ, agricultural prices are in $1975/kg, forestry prices are in $1975/m^3, and carbon prices are in $1990/tC.
