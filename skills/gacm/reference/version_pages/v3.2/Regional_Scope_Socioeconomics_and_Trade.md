# Regional Scope, Socioeconomics, and Trade

Bundled adapted source page for GCAM `v3.2`.

- Source root: `gcam-doc/v3.2`
- Source path: `Regional_Scope_Socioeconomics_and_Trade.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v3.2/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

GCAM is a multi‐regional dynamic-recursive model which couples a simple economic growth model with detailed energy system, agriculture system-land-use-terrestrial-carbon-cycle model and a simple atmosphere-ocean-climate model, MAGICC.

Geographic Coverage and Regions

-----------------------------------------

GCAM is a global model.  The economy and energy system are disaggregated into 14 geopolitical regions (**Table 1** and **Figure 1**):

|                |                     |                |
|----------------|---------------------|----------------|
| Africa

 Australia\_NZ

 Canada

 China

 Eastern Europe  | Former Soviet Union

                  India

                  Japan

                  Korea

                  Latin America        | Middle East

                                        Southeast Asia

                                        USA

                                        Western Europe

      |

###### Table 1: GCAM Regions

###### Figure 1: GCAM Region Definitions

The agriculture and land-use system are divided into 151 subregions based on the GTAP-AEZs. [Source: Monfreda, Chad, Navin Ramankutty and Thomas Hertel (2007). "Global Agricultural Land Use Data for Climate Change Analysis" in Economic Analysis of Land Use in Global Climate Change Policy (eds: Tom Hertel, Steven Rose, Richard Tol).]  These regions are discussed further in the [Agriculture, Land-Use, and Bioenergy](Agriculture_Land-Use_and_Bioenergy.md) documentation.

Socioeconomics

------------------------

GCAM computes the potential GDP of each region using exogenous assumptions about population, labor participation, and labor productivity growth.  In some formulations of the model, GDP is adjusted to reflect the effect of changing energy prices on economic growth.  However, the default assumption does not include this feedback. Population and GDP in the current baseline scenario are shown in Figures 2 and 3.

###### Figure 2: Population

###### Figure 3: GDP

Trade

---------------

In principle international trade is possible for any commodity in the GCAM. As a practical matter, however, products such as electricity or CO&lt;sub&gt;2&lt;/sub&gt; storage services are assumed to be produced and consumed within a given region. Many products are traded globally, including fossil fuels (coal, gas, oil), bioenergy, and all agricultural products.  We assume that these products are supplied to a global pool and any region can consume from this pool.

Climate Policy Analysis
-----------------------

The GCAM can be run with any combination of climate and non-climate policies. Policies can take a variety of forms including taxes or subsidies applied to energy markets, activity permits, e.g. cap-and-trade emissions permits, and/or technology standards, e.g. CAFE or new source performance standards. Costs are computed as the integral of marginal abatement cost curve.

References
----------
