# Marketplace

Bundled adapted source page for GCAM `v7.1`.

- Source root: `gcam-doc/v7.1`
- Source path: `marketplace.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v7.1/INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

# Table of Contents

- [Inputs to the Module](#inputs-to-the-module)
- [Description](#description)
- [Policy options](#policy-options)
- [Insights and intuition](#insights-and-intuition)

## Inputs to the Module
**Table 1: Inputs required by the marketplace module**

| Name | Resolution | Unit | Source |
| :--- | :--- | :--- | :--- |
| Supply of all energy commodities | Region and year  | EJ/yr | [Energy Supply Module](supply_energy.md) |
| Demand for all energy commodities | Region and year  | EJ/yr | [Energy Demand Module](demand_energy.md) |
| Supply of all agriculture and land-based commodities | Region and year  | Various (e.g., Mt/yr, billion m<sup>3</sup>/yr) | [Land Supply Module](supply_land.md) |
| Demand for all agriculture and land-based commodities | Region and year  | Various (e.g., Mt/yr, billion m<sup>3</sup>/yr) | [Land Demand Module](demand_land.md) |
| Supply of all water types | Basin and year  | km<sup>3</sup> | [Water Supply Module](supply_water.md) |
| Demand for water withdrawals and consumption | Basin and year  | km<sup>3</sup> | [Water Demand Module](demand_water.md) |

<br/>

## Description

GCAM operates by determining a set of prices that ensure supply is equal to demand for all time steps. The marketplace collects the supplies and demands and uses [solver algorithms](solver.md) to determine those prices.

## Policy options

This section summarizes some of the marketplace policy options available in GCAM.

### Carbon or GHG prices

GCAM users can directly specify the price of carbon or GHGs. Given a carbon price, the resulting emissions will vary depending on other scenario drivers, such as population, GDP, resources, and technology. See [example](policies_examples.md#carbon-price).

## Insights and intuition
