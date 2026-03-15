# Trade Outputs

Bundled adapted source page for GCAM `v7.1`.

- Source root: `gcam-doc/v7.1`
- Source path: `outputs_trade.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v7.1/INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Description of Outputs

There is no specific `XML tag` or query for trade in GCAM. For commodities that are traded via the [Armington Style Approach](details_trade.md#armington-style-trade), there are specific technologies for imports and domestic consumption (e.g., the "regional corn" sector has a "domestic corn" and "imported corn" technology) and exports are tracked in a traded sector (e.g., the "traded corn" sector has technologies for each region that exports into the global market). For all commodities, trade information can be derived by taking the difference between production and consumption of a particular commodity in a particular region. See [quantities](outputs_quantity.md) for information on how to get production and consumption.
