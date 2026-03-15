#!/usr/bin/env python3
"""
Validate agent-oriented adaptation rules for bundled page docs.

Checks:
- bundled `user-guide.md` pages replace repeated interactive ModelInterface UI walkthroughs
- screenshot-only user-guide residue is removed from bundled pages
- bundled `gcam-build.md` pages rewrite GUI IDE click paths into agent-readable build requirements
- bundled `hector.md` pages rewrite IDE integration click paths into dependency/build-setting summaries
- legacy v3.2 wiki "click here to view a previous version" boilerplate is removed
"""

from __future__ import annotations

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


def main() -> int:
    errors: list[str] = []
    validate_user_guides(errors)
    validate_gcam_build_pages(errors)
    validate_hector_pages(errors)
    validate_global_residue(errors)

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
