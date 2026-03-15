# The Climate Module

Bundled adapted source page for GCAM `v3.2`.

- Source root: `gcam-doc/v3.2`
- Source path: `The_Climate_Module.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v3.2/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

The GCAM employs the MAGICC model version 5. MAGICC is documented in
several papers<sup>[[1]](#ref1)[[2]](#ref2)[[3]](#ref3)</sup>. In the current version of GCAM, the MAGICC
code has been re-implemented in C++. MAGICC consists of a coupled set
of simple models for the entire chain from emissions to concentrations
to global radiative forcing to global changes in temperature and
sea-level. Only a brief overview is given here. For a more
complete description see referenced publications.

Emissions of greenhouse gases, aerosols, and short-lived species are
determined endogenously in GCAM (see summary table below). That is,
emissions are linked to underlying human activities. Emissions
mitigation for CO2 is treated explicitly and endogenously for fossil
fuel, industrial and land-use emissions in the GCAM.  While
emissions of non-CO2 greenhouse gases, aerosols and short-lived
species are endogenously determined, emissions mitigation is modeled
as a marginal abatement cost schedule (MAC).  Montreal gases are
treated exogenously with emissions set at levels secified by the
relevant international agreements. Terrestrial carbon emissions
in GCAM are derived from the detailed land-use-land-cover model
described [elsewhere](Agriculture_Land-Use_and_Bioenergy.md).

The first set of models within MAGICC convert emissions to
concentrations, and covers a suite of greenhouse and
pollutant gases. The carbon-cycle model in MAGICC incorporates an
impulse response formulation for the ocean carbon component and a
global-terrestrial model that self- consistently includes the impact
of land-use changes over time on terrestrial carbon stocks and
feedbacks. Changing oxidation capacity of the atmosphere due to
changes in methane and pollutant emissions is accounted for in
computing methane and HFC concentrations. Concentrations of N2O and
other fluorinated gases are computed using constant atmospheric
lifetimes.

Global radiative forcing from well-mixed greenhouse gases is
determined from concentration values using simple relationships drawn
from the literature. Forcing from carbon dioxide is proportional to
the natural logarithm of carbon dioxide concentrations, forcing from
methane and nitrous oxide is proportional to the square root of
concentrations (with an interaction term). Forcing from fluorinated
gases is linear in concentration.  Forcing from tropospheric
ozone is estimated using non-linear relationships between emissions of
methane and reactive gases NOx, CO, and VOCs.

Direct and indirect forcing from aerosols is included. Direct forcing
from sulfur dioxide, black carbon, and organic carbon are taken to be
proportional to SO2, BC, and OC emissions, respectively. The GCAM
version of MAGICC has been updated to include a direct representation
of BC and OC emissions provided by GCAM.<sup>[[4]](#ref4)</sup>
In the distribution version of MAGICC, BC
and OC forcing is, in contrast, inferred from proxy measures such as
land-use change and SO2 or CO emissions. Indirect cloud forcing in
MAGICC is taken to be proportional to the natural logarithm of sulfur
dioxide emissions.

Given total radiative forcing, global mean temperature change is
calculated using an upwelling-diffusion model of ocean thermal
response (with 40 ocean layers), together with a differential
land/ocean forcing response. Climate calculations are performed with
four boxes: two hemispheres plus land/ocean for each. Aerosol forcing
is split into these four boxes as well. MAGICC uses its calculation of
heat diffusion into the ocean to estimate sea-level rise due to
thermal expansion. Sea-level rise (SLR) components due to melting of
land glaciers and (optionally) large arctic and antarctic ice sheets
are also included.

MAGICC has been shown to be able to emulate the global-mean results
from most complex general circulation models<sup>[[5]](#ref5)</sup>. A range of
user-specified parameters, including climate sensitivity,
carbon-cycle<sup>[[6]](#ref6)</sup>, and aerosol forcing strength, are available that
enable a GCAM user to produce a wide range of climate
scenarios.

|   | GCAM |
| --- | --- |
| CO<sub>2</sub> fuel combustion | Endogenous by technology and fuel |
| CO<sub>2</sub> from other industry | Endogenous by technology and fuel |
| CO<sub>2</sub> from land use change | Endogenous by technology and land use |
| CH<sub>4</sub> | Endogenous, mitigation with MAC |
| N<sub>2</sub>O | Endogenous, mitigation with MAC |
| CFCs | Exogenous |
| HFCs | Endogenous, mitigation with MAC |
| PFCs | Endogenous, mitigation with MAC |
| SF<sub>y</sub> | Endogenous, mitigation with MAC |
| Other Montreal gases | Exogenous |
| CO | Endogenous |
| NO<sub>x</sub> | Endogenous |
| VOC | Endogenous |
| SO<sub>2</sub> | Endogenous |
| BC from fossil fuel burning | Endogenous |
| OC from fossil fuel burning | Endogenous |
| BC from biomass burning | Endogenous |
| OC from biomass burning | Endogenous |
| Nitrate | Exogenous |
| Mineral dust | Exogenous |
| Albedo | Exogenous |

References
---------

<a name="ref1"></a>[1] Wigley, T.M.L. and Raper, S.C.B. 1992. Implications for Climate
And Sea-Level of Revised IPCC Emissions Scenarios, _Nature_ 357,
293–300.

<a name="ref2"></a>[2] Wigley, T.M.L. and Raper, S.C.B. 2002. Reasons
for larger warming projections in the IPCC Third Assessment Report, _J. Climate_ 15, 2945–2952.

<a name="ref3"></a>[3] Raper, S.C.B., Wigley T.M.L. and Warrick
R.A. 1996. in _Sea-Level Rise and Coastal Subsidence: Causes, Consequences and Strategies_ J.D. Milliman, B.U. Haq, Eds., Kluwer
Academic Publishers, Dordrecht, The Netherlands,
pp. 11–45.

<!-- This is the closest match I could find to the SJ Smith, et. al, -->
<!-- in preparation, paper cited in the original text.  -rpl -->
<a name="ref4"></a>[4] SJ Smith, A Mizrahi, "Near-term climate mitigation by short-lived forcers"
    _Proceedings of the National Academy of Sciences_, 2013

<a name="ref5"></a>[5] Raper, S. C. B. and U. Cubasch
(1996) Emulation of the results from a coupled general circulation
model using a simple climate model, _GEOPHYSICAL RESEARCH LETTERS_,
VOL. 23, NO. 10, PP. 1107-1110fckLRdoi:10.1029/96GL01065

<a name="ref6"></a>[6] Smith, Steven J. and J.A. Edmonds (2006) The
Economic Implications of Carbon Cycle Uncertainty, _Tellus B_ 58 (5),
pp. 586–590.
