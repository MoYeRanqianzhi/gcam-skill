# GCAM Revision History

Bundled adapted source page for GCAM `v3.2`.

- Source root: `gcam-doc/v3.2`
- Source path: `GCAM_Revision_History.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v3.2/BUNDLE_INDEX.md`

Load this page when the user needs version-specific detail from this exact page family.

---

Version History
---------------

GCAM developers use a version control system to manage revisions to the model. Since the transition from MiniCAM to [GCAM](toc.md), there have been three major releases of the model, as well as hundreds of minor revisions.

### GCAM 1.0

GCAM 1.0 was the initial release version of the GCAM model. This version ran with 15-year time steps and 14 global energy and agricultural regions. Intermediate GCAM 1.0 revisions included a more detailed representation of the electricity system in the US (r.3725), improved technology retirements and shutdown behavior (r.3897), and an improved representation of internal gains in the buildings sector (r.4010).

### GCAM 2.0

GCAM 2.0 introduced variable timesteps to the model, with the default model timestep moving from 15 years to 5 years. Subsequent GCAM 2.0 revisions included the introduction of the C++ version of the climate module (r.4090). With the additional of 5 year time steps, it became important to accurately reflect historical observations in 2010. Model results were revised to reflect this in r.4137.

### GCAM 3.0

The latest major revision to the model began with the introduction of an extensive update to the the agriculture and land use portion of GCAM. This expanded the number of regions in this portion of the model from 14 to 151 regions based on agro-ecological zones (the energy system continues to use 14 aggregate regions). This introduced substantial complexities to the model and increased the total solution time. Model run time was substantially reduced with the release of an improved solver in r.4371. This is the version that was distributed at the 2011 Community Modeling Meeting held in December at JGCRI's College Park, MD office.

### GCAM 3.1

The latest model release (r.4517), now distributed under the ECL open source license, contains a mechanistic building model which simulates explicit energy services for a representative commercial and residential building in each region. The climate model was revised with an explicit representation of historical emissions (used to calibrate concentration and forcing calculations), along with several smaller fixes to non-CO2 emissions. Other changes include explicit trading of unconventional oil and regional CO2 storage supply curves for CCS. GCAM 3.1 was made available through a new web interface in June 2012.

Viewing Wiki Documentation For Previous Versions
------------------------------------------------

At the top of each page you may notice some text indicating which version of GCAM the documentation on that page is valid for. GCAM is a research tool that is constantly evolving and we hope to always keep the wiki up to date with the latest revision of GCAM. Users however may not always be able to use the latest version of GCAM therefore may want to view documentation for earlier versions. In order to accommodate these users we will adhere to the following scheme to make it straightforward to retrieve the documentation valid for the revision you are using.

If the version note on a page indicates that it was revised for a later GCAM version than the one you need, inspect that page's revision history and select the last revision that predates the later-version update:

On this page you will find a list of edits to the wiki page of interest. For each edit there may be a comment giving some insight about what changed in that edit. In these comments we will indicate when an edit was made for upgrades made in GCAM. Here you will want to select the last version of the wiki page before it was updated to a later GCAM revision than what you are looking for.

Note that this strategy was adopted May 1, 2012 and all edits prior to this date should be assumed to be valid for GCAM 3.0 r4371.
