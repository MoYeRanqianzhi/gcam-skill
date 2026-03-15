#!/usr/bin/env python3
"""
Validate bundled GCAM version-catalog invariants.

Checks:
- version identifiers are unique and remain in descending semantic order
- families and coverage modes stay within the supported taxonomy
- alias mappings stay unique and canonicalize as expected
- exactly one bundled baseline exists and it is `v8.2`
- `delta-only` metadata stays aligned with `family` / `coverage_mode`
- shared topic inventory stays unique and retains the required routing docs
"""

from __future__ import annotations

import re

from version_catalog import (
    COMMON_TOPICS,
    FAMILY_DESCRIPTIONS,
    VERSION_CATALOG,
    canonicalize_version,
    family_notes,
    get_version_info,
)


VERSION_RE = re.compile(r"^v(\d+)\.(\d+)$")
ALLOWED_COVERAGE_MODES = {"delta-only", "version-summary", "bundled-baseline"}
REQUIRED_BASELINE_ALIASES = {"root", "current", "baseline", "full-docs", "8.2"}
REQUIRED_TOPIC_DOCS = {"navigation.md", "version_families.md", "version_inventory.md"}


def version_key(raw: str) -> tuple[int, int]:
    match = VERSION_RE.fullmatch(raw)
    if not match:
        raise ValueError(raw)
    return int(match.group(1)), int(match.group(2))


def validate_versions(errors: list[str]) -> None:
    seen: set[str] = set()
    listed = [info.version for info in VERSION_CATALOG]
    for version in listed:
        if version in seen:
            errors.append(f"Duplicate version in VERSION_CATALOG: {version}")
        seen.add(version)
        if not VERSION_RE.fullmatch(version):
            errors.append(f"Invalid version identifier format: {version}")

    if listed != sorted(listed, key=version_key, reverse=True):
        errors.append("VERSION_CATALOG must remain sorted from newest to oldest")


def validate_families_and_coverage(errors: list[str]) -> None:
    bundled_baselines = []
    for info in VERSION_CATALOG:
        if info.family not in FAMILY_DESCRIPTIONS:
            errors.append(f"{info.version} -> unknown family: {info.family}")
        if info.coverage_mode not in ALLOWED_COVERAGE_MODES:
            errors.append(f"{info.version} -> unknown coverage mode: {info.coverage_mode}")
        if family_notes(info.family) != FAMILY_DESCRIPTIONS[info.family]:
            errors.append(f"{info.version} -> family_notes mismatch for family `{info.family}`")

        if info.coverage_mode == "delta-only":
            if info.family != "delta-only":
                errors.append(f"{info.version} -> delta-only coverage must use family `delta-only`")
        elif info.family == "delta-only":
            errors.append(f"{info.version} -> family `delta-only` requires coverage mode `delta-only`")

        if info.coverage_mode == "bundled-baseline":
            bundled_baselines.append(info)

    if len(bundled_baselines) != 1:
        errors.append("Exactly one bundled-baseline version must exist in VERSION_CATALOG")
        return

    baseline = bundled_baselines[0]
    if baseline.version != "v8.2":
        errors.append("The bundled baseline version must remain `v8.2`")
    if baseline.family != "modern-comprehensive":
        errors.append("`v8.2` bundled baseline must remain in family `modern-comprehensive`")
    if not REQUIRED_BASELINE_ALIASES.issubset(set(baseline.aliases)):
        missing = sorted(REQUIRED_BASELINE_ALIASES - set(baseline.aliases))
        errors.append("`v8.2` bundled baseline is missing required aliases: " + ", ".join(missing))


def validate_aliases(errors: list[str]) -> None:
    seen: dict[str, str] = {}
    for info in VERSION_CATALOG:
        canonical = info.version.lower()
        if canonical in seen:
            errors.append(f"Duplicate canonical version key: {info.version}")
        seen[canonical] = info.version

        for alias in info.aliases:
            normalized = alias.lower()
            previous = seen.get(normalized)
            if previous is not None:
                errors.append(f"Alias collision: `{alias}` maps to both {previous} and {info.version}")
            else:
                seen[normalized] = info.version

            try:
                resolved = canonicalize_version(alias)
            except KeyError:
                errors.append(f"{info.version} -> alias does not canonicalize: {alias}")
                continue
            if resolved != info.version:
                errors.append(f"{info.version} -> alias canonicalizes to wrong version: {alias} -> {resolved}")
            if get_version_info(alias).version != info.version:
                errors.append(f"{info.version} -> get_version_info returned wrong version for alias: {alias}")

        if canonicalize_version(info.version) != info.version:
            errors.append(f"{info.version} -> canonicalize_version drifted for canonical version key")
        if get_version_info(info.version).version != info.version:
            errors.append(f"{info.version} -> get_version_info drifted for canonical version key")
        if canonicalize_version(info.version[1:]) != info.version:
            errors.append(f"{info.version} -> numeric version lookup without `v` prefix failed")

    if canonicalize_version(None) != "v8.2":
        errors.append("canonicalize_version(None) must default to `v8.2`")


def validate_common_topics(errors: list[str]) -> None:
    if len(COMMON_TOPICS) != len(set(COMMON_TOPICS)):
        errors.append("COMMON_TOPICS contains duplicate entries")

    missing = sorted(topic for topic in REQUIRED_TOPIC_DOCS if topic not in set(COMMON_TOPICS) | {"version_inventory.md"})
    if missing:
        errors.append("COMMON_TOPICS / generated inventory are missing required routing docs: " + ", ".join(missing))


def main() -> int:
    errors: list[str] = []
    validate_versions(errors)
    validate_families_and_coverage(errors)
    validate_aliases(errors)
    validate_common_topics(errors)

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Version catalog validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
