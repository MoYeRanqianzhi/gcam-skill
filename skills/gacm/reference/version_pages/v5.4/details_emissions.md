# Details about emissions in GCAM

Bundled adapted source page for GCAM `v5.4`.

- Source root: `gcam-doc/v5.4`
- Source path: `details_emissions.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v5.4/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

## Calibration year differences between CEDS and GCAM

Two omitted figures compare historical emissions from CEDS with GCAM emissions after initialization: one at the global-by-species level and one as a region-by-species-by-year scatter comparison. Those comparisons indicate that emissions translate mostly correctly for all species of gases.

However, there are reasons for the differences. One reason is that deforestation emissions from protected land are zeroed out in GCAM in the historical period since protected land is held constant in the calibration years. Also deforestation emissions in the final base year are initialized using deforestation coefficients calculated on the basis of deforestation over a 5 year period (2000 and 2005). This leads to a difference in the total deforestation emissions from the CEDS inventory when compared to the numbers initialized in  GCAM.
