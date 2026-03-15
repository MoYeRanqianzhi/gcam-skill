#!/usr/bin/env python3
"""
Validate agent-oriented adaptation rules for bundled page docs.

Checks:
- bundled `user-guide.md` pages replace repeated interactive ModelInterface UI walkthroughs
- screenshot-only user-guide residue is removed from bundled pages
- legacy v3.2 wiki "click here to view a previous version" boilerplate is removed
"""

from __future__ import annotations

from version_catalog import VERSION_PAGES_ROOT, ordered_versions


USER_GUIDE_REQUIRED = (
    "This adapted user-guide page rewrites interactive ModelInterface browsing into headless-agent guidance and omits screenshot-dependent UI steps.",
    "Agent adaptation: the upstream source described interactive ModelInterface browsing here.",
    "Agent adaptation: interactive scenario/region/query selection is omitted in this text-only bundle.",
    "*Agent adaptation*: Prefer CSV/XLS export through headless batch queries or extraction libraries instead of manual copy/paste from the ModelInterface UI.",
)

USER_GUIDE_FORBIDDEN = (
    "Select `Open` from the Model Interface File menu",
    "Screenshot of GCAM ModelInterface",
    'Press this button and model output will appear as shown below',
    "*Copying Data*:",
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
