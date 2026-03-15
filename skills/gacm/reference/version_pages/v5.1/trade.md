# Trade in GCAM

Bundled adapted source page for GCAM `v5.1`.

- Source root: `gcam-doc/v5.1`
- Source path: `trade.md`
- Coverage mode: `full-tree page bundle`

Load this page when the user needs version-specific detail from this exact page family.

---

Commodities in GCAM are either traded globally (Heckscher-Ohlin) or fixed interregional trade.  Altough alternative approaches for trade can readily be implemented in the GCAM framework they are not currently implmented (with the exception of [GCAM USA](gcam-usa.md) where logit based decisions are made to facilitating trade between the 50-states).

## Heckscher-Ohlin
Commodities such as coal, gas, oil, bio-energy, Corn, Rice, etc are each traded in a single global market.  Each region will see the same global price and independently decide how much each will supply and demand of each commodity given that price.  A region's net trade position is dynamic depending on economics, technical change, demand, growth, resources, etc.  Under this method for trading goods there is no modeled preference for a given region to demand a commodity from any other specific region.

## Fixed Interregion Trade
Some commodities such as meat and dairy and trade volumes are simply held fixed at their historical value for the rest of the simulation. Our basic economic modeling approach makes dynamic trade complicated, and the fixed trade assumption based on historical data is a conservative approach.

## No Trade of Secondary energy goods
Note that secondary energy products such as [Electricity](energy.md#electricity) or [Refined Liquids](energy.md#refining) are assumed to not be traded at all between the GCAM geo-political regions.
