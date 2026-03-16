#!/usr/bin/env python3
"""
Validate agent-oriented adaptation rules for bundled page docs.

Checks:
- bundled `user-guide.md` pages replace repeated interactive ModelInterface UI walkthroughs
- screenshot-only user-guide residue is removed from bundled pages
- bundled `gcam-build.md` pages rewrite GUI IDE click paths into agent-readable build requirements
- bundled `hector.md` pages rewrite IDE integration click paths into dependency/build-setting summaries
- legacy v3.2 wiki "click here to view a previous version" boilerplate is removed
- raw figure captions and direct figure-number references are normalized into text-only wording
"""

from __future__ import annotations

import re

from version_catalog import VERSION_PAGES_ROOT, ordered_versions


USER_GUIDE_REQUIRED = (
    "This adapted user-guide page rewrites interactive ModelInterface browsing into headless-agent guidance and omits screenshot-dependent UI steps.",
    "Agent adaptation: result inspection should start from batch or file-based query automation, not interactive ModelInterface browsing.",
    "Agent adaptation: the packaged `ModelInterface.jar` / `ModelInterface.app` is not the default workflow in this bundle. Prefer direct batch execution, query-file editing, and scripted CSV/XLS export.",
    "Agent adaptation: treat the `interactive mode` subsection below as historical context and prefer batch or direct file-based workflows.",
)

USER_GUIDE_FORBIDDEN = (
    "Download GCAM` link in the upper right",
    "double click on the `run-gcam` executable script",
    "double click on the executable",
    "double clicking the `run-gcam` executable script",
    "To view model output open the ModelInterface application.",
    "A tabular data display will appear on the left and a simple graphical output will appear on the right.",
    "*Sorting*: You can sort results in the Model Interface tables by clicking on the table heading.",
    "double clicking the `ModelInterface.jar`",
    "`File -> Save`",
    "`File -> Save As`",
    "`File -> Batch File`",
    "Show Package Contents",
    "Select `Open` from the Model Interface File menu",
    "Screenshot of GCAM ModelInterface",
    'Press this button and model output will appear as shown below',
    "*Copying Data*:",
    "section of the GUI",
    "pressed any button it will attempt to open the DB once more",
)

GCAM_BUILD_REQUIRED = (
    "This adapted build page rewrites GUI IDE click paths into agent-readable configuration targets and prefers Makefile/headless builds when available.",
    "Agent adaptation: the upstream Xcode walkthrough was UI-oriented. For agent workflows, prefer the Makefile build.",
    "Agent adaptation: if this project is used, treat `Release` + `x64` as the effective build configuration instead of relying on IDE menu selection.",
)

GCAM_BUILD_FORBIDDEN = (
    "Product -> Build",
    "Build -> Build Solution",
    "Platform Toolset` under menu `Project -> objects-main Properties..`",
    "Build Settings -> Preprocessor Macros",
    "Project -> objects-main Properties -> C/C++ -> Preprocessor -> Preprocessor Definitions",
    "available from the Apple App Store",
    "Once open you should change the `Scheme` to build the `Release` target.",
    "You can find the scheme settings here:",
    "Then under the `Info` tab change the build configuration to `Release`:",
    "Options` section of the current scheme",
    "Once open you should change the `Solution Configurations` and `Solution Platform`",
)

HECTOR_REQUIRED = (
    "This adapted Hector page rewrites IDE integration click paths into agent-readable dependency and build-setting summaries.",
)

HECTOR_LEGACY_REQUIRED = (
    "Agent adaptation: skip the Xcode click path. Treat the following values as the relevant build facts:",
    "Agent adaptation: skip the Visual Studio click path. Treat the following values as the relevant build facts:",
)

HECTOR_FORBIDDEN = (
    "Project Navigator",
    "Build Settings",
    "Build Phases",
    "Solution Explorer",
    "Add -> Existing project",
    "Open the GCAM project in Xcode.",
    "Open the GCAM project in Visual Studio.",
    "click the +",
    "drop down menu",
)

GLOBAL_FORBIDDEN = (
    "Click here for info on how to view a previous version",
    "point and click",
    "click on the “history” tab at the top of that page",
)

FIGURE_DEPENDENT_FORBIDDEN = (
    "(see Figure below)",
    "land types included in GCAM (see Figure 1).",
    "management practice included in GCAM (see Figure 1).",
    "Figure 1 shows the nesting diagram of land with a subregion.",
    "Figure 1 shows the nesting diagram of land with an AEZ subregion.",
    "Figure 1 shows a simplified nesting diagram of land with a subregion.",
    "A representative, simplified nnesting structure is depicted in Figure 1.",
    "A representative, simplified nesting structure is depicted in Figure 1.",
    "different levels of resolution for each of these different systems (see Figure 2).",
    "the energy system depicted below",
    "The nesting structure of the electric sector is shown in the figure below",
    "shown in the following figure",
    "as indicated in the figure above, this technology does not differentiate between conventional and unconventional oil",
    "Resource curves for fossil fuels are shown below.",
    "depicted graphically below",
    "with four competing technology options, shown below.",
    "see Figure 2 for more details",
    "Figure 2 also indicates the corresponding files in the `gcamdata` system that process the inputs for each land type.",
    "The figure also indicates which file in the `gcamdata` system processes the inputs for each type of land",
    "finite time required for forests to grow, as shown in the figure below.",
    "relative attractiveness to deploy DACCS in a given state within GCAM (see figure below).",
    "and Asia-Pacific (see figures).",
    "Figures 1 and 2 compare historical emissions from CEDS with the emissions from GCAM after initialization .",
    "Figure 1 shows the new elements in relation to existing GCAM elements.",
    "and shown in Figures 1 (crop harvested area) and 2 (food).",
    "with the sector divided into three service demands: passenger, freight, and international shipping (see Figure 1).",
    "as shown in Figure 1. Within energy use there is cost-based competition between fuels",
    "such as steam and machine drive (see Figure 2).",
    "Figure 3 shows the eleven GCAM industries and their energy requirements, by service, in 2005.",
    "Population and GDP in the current baseline scenario are shown in Figures 2 and 3.",
    "Resource supply curves for natural gas, crude oil, unconventional oil, and coal are shown for each of the 14 GCAM regions in Figures 1-4 below.",
    "the supply curves shown below do not include the cost of the energy used in extraction",
    "are shown in the figures as dotted lines.",
    "Supply curves by GCAM region are shown in Figure 5;",
    "Rooftop PV supply curves are shown in Figure 6;",
    "Supply curves for the hydrothermal and EGS resources in all regions are shown in Figure 7.",
    "Figure 8 shows the supply curves used in each region;",
    "For wind power, the supply curve for the U.S. region is based on NREL (2008), and is shown in Figure 2.",
    "The supply curve for rooftop PV in the U.S. is from NREL (P. Denholm and R. Margolis, pers. comm.), and is also shown in Figure 3.",
    "Supply curves assumed for hydrothermal and EGS resources for the U.S. are based on Petty and Porro (2007) and are shown in Figure 3.",
    "These different technology options for refining are shown in Figure 1; the non-energy costs and input/output coefficients are shown in Table 1.",
    "note the electricity and gas inputs to the “unconventional oil production” sector in Figure 1 and Table 1",
    "network shown in the figure above",
    "This is illustrated further in the graphic below.",
    "shown in the figure above, hydrogen can be produced from up to 7 primary energy sources",
    "The figure below depicts the fossil fuel trade structures",
    "The figure below is an example XML of user-specified residential floorspace values for Maine.",
    "The schematic below shows how N fertilizer is situated between the energy and agricultural systems of GCAM.",
    "The schematic below shows how ammonia and N fertilizer commodities are situated between the energy and agricultural systems of GCAM.",
    "In the figure below, the rate of growth as a function of time since planting is shown",
    "For example in the figure below, the cost of moving",
    "shown in red below",
)
FIGURE_DEPENDENT_REGEXES = (
    re.compile(
        r'The structural implementations of a "global-market" versus a "regional-market" representation are shown in Figure \d+(?: with an example of corn trade)?\.'
    ),
    re.compile(
        r"Furthermore, the two market structures are also compared in Figure \d+ with an example of a global wheat market equilibrium with demand and supply flows in 2010\."
    ),
    re.compile(
        r"The structure of refining in the broader energy system is shown in Figure \d+, with example input-output coefficients\."
    ),
    re.compile(
        r"This is depicted in Figure \d+, with typical input-output coefficients shown\."
    ),
    re.compile(
        r"network shown in Figure \d+"
    ),
    re.compile(
        r"with four competing technology options, shown in Figure \d+\."
    ),
    re.compile(
        r'As shown in Figure \d+, all energy losses and cost mark-ups incurred in transforming primary energy into delivered district heat are accounted in the "district heat" technologies'
    ),
    re.compile(
        r"This is illustrated further in Figure \d+\."
    ),
    re.compile(
        r"^The structure of the natural gas supply and distribution in GCAM is shown in Figure \d+:\s*$",
        re.MULTILINE,
    ),
    re.compile(
        r"The structure of the hydrogen production and distribution sectors and technologies in GCAM generally uses the structure of the U\.S\. Department of Energy's Hydrogen Analysis \(H2A\) models \[[^\]]+\]\([^)]+\), and is shown in Figure \d+\."
    ),
    re.compile(
        r"; as shown in Figure \d+, hydrogen can be produced from up to 7 primary energy sources\."
    ),
    re.compile(
        r"Figure 1 below shows a competition between two options with distributions of profits\."
    ),
)
FIGURE_LABEL_TOKEN = r"[A-Za-z]*\d[A-Za-z0-9.\-]*"
RAW_FIGURE_TEXT_REGEXES = (
    re.compile(
        rf"^\s*(?:#+\s*)?(?:\*\*|__)?Figure\s+{FIGURE_LABEL_TOKEN}(?:[:.]|\s+-)",
        re.IGNORECASE | re.MULTILINE,
    ),
    re.compile(rf"\bFrom Figure\s+{FIGURE_LABEL_TOKEN}\b"),
    re.compile(
        rf"\bFigure\s+{FIGURE_LABEL_TOKEN}\s+(illustrates|shows|provides|summarizes|depicts|compares|contrasts|maps|presents|describes)\b",
        re.IGNORECASE,
    ),
    re.compile(rf"\bgiven in Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE),
    re.compile(rf"\bwhat is in Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE),
    re.compile(rf"\bthe omitted Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE),
    re.compile(rf"\bdisplayed in Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE),
    re.compile(rf"\bshown schematically in Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE),
    re.compile(rf",\s*Figure\s+{FIGURE_LABEL_TOKEN}\.(?=\s+[A-Z])", re.IGNORECASE),
    re.compile(rf"\bdepicted(?:\s+in)?\s+Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE),
    re.compile(r"Figure source:", re.IGNORECASE),
    re.compile(r"\bFig\.\s*\d+[A-Za-z]\b"),
)

TEST_FRAMEWORK_REQUIRED = (
    "This adapted testing-framework page preserves historical internal CI topology but rewrites pull-request/button/UI phrasing into repository events, webhook payloads, and status API concepts.",
    "Agent adaptation: this page documents historical internal CI wiring. Treat pull-request pages, buttons, and Jenkins/Bitbucket UI labels as names for repository events, webhook payloads, and status APIs, not mandatory GUI steps.",
)

TEST_FRAMEWORK_FORBIDDEN = (
    "pull request interface",
    "open your pull request",
    "add a new menu option with in the pull request",
    'When the "button" is clicked and a user confirms',
    "watch the progress / look at logs or build artifacts after the fact",
    'Pull Request Notifier "Button" labeled "Launch Validation Runs"',
    "button form was generated manually",
    'Historical UI note: the internal "Launch Validation Runs" button invoked Jenkins',
)

GETTING_STARTED_REQUIRED = (
    "This adapted getting-started page rewrites final submission steps as host-agnostic review-request workflow instead of browser-only pull-request actions.",
    "Agent adaptation: use the forge CLI or API when available instead of assuming a browser-only pull request action.",
)

GETTING_STARTED_FORBIDDEN = (
    "When your development is complete, open a pull request.",
)

ANALYSIS_REQUIRED = (
    "This adapted analysis page prefers automation-oriented descriptions over GUI-centric wording where the original text listed tool categories.",
)

ANALYSIS_FORBIDDEN = (
    "graphical user interfaces for working with GCAM",
)

GIT_REQUIRED = (
    "This adapted git page preserves historical forge examples but rewrites browser-specific actions into CLI/API-friendly repository workflow terms.",
    "Once the review request exists, expect feedback from other developers.",
)

GIT_FORBIDDEN = (
    "server and open a pull request",
    "fork button on GitHub",
    "Open a pull request as soon you have some progress to share.",
    "Once you have opened the pull request,",
    "mark your pull request as",
)

DATA_SYSTEM_REQUIRED = (
    "This adapted data-system page rewrites source-tool GUI export wording into dataset-shape requirements, filesystem targets, and text-first preprocessing steps.",
)

DATA_SYSTEM_LEGACY_IEA_BROWSER_REQUIRED = (
    "Agent adaptation: do not rely on a specific GUI such as `Beyond 2020 Browser`.",
)

DATA_SYSTEM_FORBIDDEN = (
    "open the `Beyond 2020 Browser`",
    "toggle the variables so that the years are columns",
    "displayed, with no variables held fixed",
)


def validate_user_guides(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "user-guide.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in USER_GUIDE_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required agent-adaptation snippet: {snippet}"
                )
        for snippet in USER_GUIDE_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden GUI residue: {snippet}"
                )


def validate_gcam_build_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "gcam-build.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in GCAM_BUILD_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required build adaptation snippet: {snippet}"
                )
        for snippet in GCAM_BUILD_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden IDE residue: {snippet}"
                )


def validate_hector_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "hector.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in HECTOR_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required hector adaptation snippet: {snippet}"
                )
        if info.version in {"v3.2", "v4.2"}:
            for snippet in HECTOR_LEGACY_REQUIRED:
                if snippet not in text:
                    errors.append(
                        f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required hector legacy adaptation snippet: {snippet}"
                    )
        for snippet in HECTOR_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden IDE residue: {snippet}"
                )


def validate_global_residue(errors: list[str]) -> None:
    for path in sorted(VERSION_PAGES_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for snippet in GLOBAL_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden legacy residue: {snippet}"
                )


def validate_figure_dependent_residue(errors: list[str]) -> None:
    for path in sorted(VERSION_PAGES_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for snippet in FIGURE_DEPENDENT_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden figure-dependent residue: {snippet}"
                )
        for pattern in FIGURE_DEPENDENT_REGEXES:
            if pattern.search(text):
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still matches forbidden figure-dependent pattern: {pattern.pattern}"
                )
        for pattern in RAW_FIGURE_TEXT_REGEXES:
            if pattern.search(text):
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains raw figure-text residue: {pattern.pattern}"
                )


def validate_devguide_test_framework_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "dev-guide" / "test_framework.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in TEST_FRAMEWORK_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required test-framework adaptation snippet: {snippet}"
                )
        for snippet in TEST_FRAMEWORK_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden test-framework UI residue: {snippet}"
                )


def validate_devguide_getting_started_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "dev-guide" / "getting_started.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in GETTING_STARTED_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required getting-started adaptation snippet: {snippet}"
                )
        for snippet in GETTING_STARTED_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden getting-started GUI residue: {snippet}"
                )


def validate_devguide_analysis_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "dev-guide" / "analysis.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in ANALYSIS_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required analysis adaptation snippet: {snippet}"
                )
        for snippet in ANALYSIS_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden analysis GUI residue: {snippet}"
                )


def validate_devguide_git_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "dev-guide" / "git.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in GIT_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required git adaptation snippet: {snippet}"
                )
        for snippet in GIT_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden git GUI residue: {snippet}"
                )


def validate_data_system_pages(errors: list[str]) -> None:
    for info in ordered_versions():
        if info.coverage_mode == "delta-only":
            continue
        path = VERSION_PAGES_ROOT / info.version / "data-system.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in DATA_SYSTEM_REQUIRED:
            if snippet not in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required data-system adaptation snippet: {snippet}"
                )
        if info.version in {"v4.3", "v4.4"}:
            for snippet in DATA_SYSTEM_LEGACY_IEA_BROWSER_REQUIRED:
                if snippet not in text:
                    errors.append(
                        f"{path.relative_to(VERSION_PAGES_ROOT.parent)} missing required data-system legacy adaptation snippet: {snippet}"
                    )
        for snippet in DATA_SYSTEM_FORBIDDEN:
            if snippet in text:
                errors.append(
                    f"{path.relative_to(VERSION_PAGES_ROOT.parent)} still contains forbidden data-system GUI residue: {snippet}"
                )


def main() -> int:
    errors: list[str] = []
    validate_user_guides(errors)
    validate_gcam_build_pages(errors)
    validate_hector_pages(errors)
    validate_devguide_test_framework_pages(errors)
    validate_devguide_getting_started_pages(errors)
    validate_devguide_analysis_pages(errors)
    validate_devguide_git_pages(errors)
    validate_data_system_pages(errors)
    validate_global_residue(errors)
    validate_figure_dependent_residue(errors)

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Page bundle agent adaptation validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
