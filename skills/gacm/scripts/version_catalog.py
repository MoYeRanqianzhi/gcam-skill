#!/usr/bin/env python3
"""
Bundled GCAM version catalog for the open-source `gacm` skill.

This module is intentionally self-contained:
- no absolute paths
- no dependency on a local GCAM checkout
- version routing is expressed only in terms of bundled skill references
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Tuple


REFERENCE_ROOT = Path(__file__).resolve().parent.parent / "reference"
VERSIONS_ROOT = REFERENCE_ROOT / "versions"


@dataclass(frozen=True)
class VersionInfo:
    version: str
    family: str
    coverage_mode: str
    aliases: Tuple[str, ...] = field(default_factory=tuple)
    summary: Tuple[str, ...] = field(default_factory=tuple)
    deltas: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


COMMON_TOPICS: Tuple[str, ...] = (
    "navigation.md",
    "version_families.md",
    "overview.md",
    "common_assumptions.md",
    "choice_marketplace.md",
    "energy_system.md",
    "land_system.md",
    "water_system.md",
    "economy.md",
    "emissions_climate.md",
    "running_gcam.md",
    "building_gcam.md",
    "solver.md",
    "policies_scenarios.md",
    "inputs_outputs.md",
    "ssp.md",
    "gcam_usa.md",
    "tools.md",
    "developer_workflows.md",
    "updates.md",
    "data_system.md",
    "coverage_map.md",
    "source_provenance.md",
)


FAMILY_DESCRIPTIONS: Dict[str, Tuple[str, ...]] = {
    "legacy-wiki": (
        "Wiki-style documentation and older model framing.",
        "Expect different naming, fewer dedicated module pages, and older structural assumptions.",
        "Start from the exact version file, then load only the bundled topic docs needed for the question.",
    ),
    "compact-modern": (
        "Compact modular docs with fewer specialized pages than modern releases.",
        "Good for v4.x questions, but avoid assuming current page granularity.",
        "Start from the exact version file, then load only the bundled topic docs needed for the question.",
    ),
    "modern-transitional": (
        "Modernized doc layout, but less granular than v5.4+ and v6+ trees.",
        "Useful bridge between v4.x and later comprehensive doc sets.",
        "Start from the exact version file, then load only the bundled topic docs needed for the question.",
    ),
    "modern-comprehensive": (
        "Broad modular doc layout with dedicated overview, running, build, solver, policy, and IO pages.",
        "Use as the main routing family for v5.4, v6.0, v7.0, v7.1, and current v8.2.",
        "Start from the exact version file, then load only the bundled topic docs needed for the question.",
    ),
    "delta-only": (
        "The bundled skill only includes release deltas for this version, not a full standalone restatement.",
        "Route through the delta notes plus shared topic docs; do not pretend to have a complete dedicated doc tree.",
        "Start from the exact version file, then layer only the needed bundled baseline topic docs on top of the delta.",
    ),
}


VERSION_CATALOG: Tuple[VersionInfo, ...] = (
    VersionInfo(
        version="v8.7",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Cement data updates.",),
        notes=("Treat as an incremental release layered on the v8.x line.",),
    ),
    VersionInfo(
        version="v8.6",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Electricity generation CCS emission factor update.",),
    ),
    VersionInfo(
        version="v8.5",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Bugfix release in Fall 2025.",),
    ),
    VersionInfo(
        version="v8.4",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Socioeconomic and macro data updates.",),
    ),
    VersionInfo(
        version="v8.3",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("String interning implementation update in GCAM core.",),
    ),
    VersionInfo(
        version="v8.2",
        family="modern-comprehensive",
        coverage_mode="bundled-baseline",
        aliases=("root", "current", "baseline", "full-docs", "8.2"),
        summary=(
            "Current bundled baseline for this skill.",
            "Represents the root `gcam-doc` documentation tree bundled as the default full-topic baseline when no version is specified.",
        ),
        deltas=(
            "Base year moved to 2021 in the v8.x line.",
            "Future years start at 2025 in the current baseline.",
            "Ukraine appears as an independent GCAM region in the v8.x line.",
        ),
    ),
    VersionInfo(
        version="v8.1",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Ukraine introduced as an independent region.",),
    ),
    VersionInfo(
        version="v8.0",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Model base year moved to 2021.",),
    ),
    VersionInfo(
        version="v7.4",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Initial base-year update work preparing the new base year.",),
    ),
    VersionInfo(
        version="v7.3",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("Updated intermittent electricity integration approach.",),
    ),
    VersionInfo(
        version="v7.2",
        family="delta-only",
        coverage_mode="delta-only",
        deltas=("SSP database updated to v3.0 / 2024 inputs.",),
    ),
    VersionInfo(
        version="v7.1",
        family="modern-comprehensive",
        coverage_mode="version-summary",
        aliases=("7.1",),
        summary=("Fully documented modern GCAM release with broad topical coverage.",),
        deltas=(
            "Forestry detail and pulp-and-paper updates.",
            "Hydrogen and ammonia trade updates.",
            "Food storage and AgLU parameter updates.",
        ),
    ),
    VersionInfo(
        version="v7.0",
        family="modern-comprehensive",
        coverage_mode="version-summary",
        aliases=("7.0",),
        summary=("Major release preceding v7.1 with macro and trade updates.",),
        deltas=(
            "Base-year preparation had not yet moved to 2021.",
            "Macro-economic module and natural gas trade changes were introduced in this line.",
            "AgLU method update linked hectares to food calories.",
        ),
    ),
    VersionInfo(
        version="v6.0",
        family="modern-comprehensive",
        coverage_mode="version-summary",
        aliases=("6.0",),
        summary=("Modern comprehensive line with strong sector expansion.",),
        deltas=(
            "Detailed industrial sectors expanded.",
            "Hydrogen and direct air capture capabilities expanded.",
            "Additional limits to bioenergy and more crop detail added.",
        ),
    ),
    VersionInfo(
        version="v5.4",
        family="modern-comprehensive",
        coverage_mode="version-summary",
        aliases=("5.4",),
        summary=("Late v5 release with broader modern page structure.",),
        deltas=(
            "Trade improvements for fossil fuels, forestry, and agriculture.",
            "Water markets in GCAM-USA and energy-for-water additions.",
            "Solver improvements and source-data updates.",
        ),
    ),
    VersionInfo(
        version="v5.3",
        family="modern-transitional",
        coverage_mode="version-summary",
        aliases=("5.3",),
        summary=("Transitional modern release family; less granular than v5.4+.",),
    ),
    VersionInfo(
        version="v5.2",
        family="modern-transitional",
        coverage_mode="version-summary",
        aliases=("5.2",),
        summary=("Transitional modern release with SSP, policy, and core topical docs.",),
    ),
    VersionInfo(
        version="v5.1",
        family="modern-transitional",
        coverage_mode="version-summary",
        aliases=("5.1",),
        summary=("Early v5 modernized doc set.",),
        deltas=("GCAM data system separated into its own package in the v5 era.",),
    ),
    VersionInfo(
        version="v4.4",
        family="compact-modern",
        coverage_mode="version-summary",
        aliases=("4.4",),
        summary=("Compact modular documentation, pre-v5 expansion.",),
    ),
    VersionInfo(
        version="v4.3",
        family="compact-modern",
        coverage_mode="version-summary",
        aliases=("4.3",),
        summary=("Compact modular documentation, pre-v5 expansion.",),
    ),
    VersionInfo(
        version="v4.2",
        family="compact-modern",
        coverage_mode="version-summary",
        aliases=("4.2",),
        summary=("Compact modular documentation, pre-v5 expansion.",),
    ),
    VersionInfo(
        version="v3.2",
        family="legacy-wiki",
        coverage_mode="version-summary",
        aliases=("3.2",),
        summary=(
            "Legacy wiki-style release with older model architecture framing.",
            "Do not assume naming or structure parity with later releases.",
        ),
        deltas=(
            "14 geopolitical regions instead of the later 32-region framing.",
            "MAGICC-based climate framing in the bundled source material for that era.",
            "Pages are organized around large narrative topics rather than later modular doc trees.",
        ),
    ),
)


_LOOKUP: Dict[str, VersionInfo] = {}
for entry in VERSION_CATALOG:
    _LOOKUP[entry.version.lower()] = entry
    for alias in entry.aliases:
        _LOOKUP[alias.lower()] = entry


def canonicalize_version(raw: str | None) -> str:
    if not raw:
        return "v8.2"
    key = raw.strip().lower()
    if key in ("root", "current", "baseline", "full-docs"):
        return "v8.2"
    if key and not key.startswith("v") and key[0].isdigit():
        key = f"v{key}"
    info = _LOOKUP.get(key)
    if info is None:
        raise KeyError(f"Unknown GCAM version: {raw}")
    return info.version


def get_version_info(raw: str | None) -> VersionInfo:
    return _LOOKUP[canonicalize_version(raw).lower()]


def ordered_versions() -> Iterable[VersionInfo]:
    return VERSION_CATALOG


def bundled_topic_docs() -> Tuple[str, ...]:
    return COMMON_TOPICS


def family_notes(family: str) -> Tuple[str, ...]:
    return FAMILY_DESCRIPTIONS[family]
