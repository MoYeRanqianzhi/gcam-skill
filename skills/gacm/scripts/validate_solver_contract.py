#!/usr/bin/env python3
"""
Validate bundled GCAM solver-doc contract invariants.

Checks:
- `reference/solver.md` stays version-routing-aware and `v8.2` baseline-aware
- solver guidance remains CLI/config/log-first instead of GUI-first
- key troubleshooting and historical-solver caveats remain explicit
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SOLVER_DOC = REPO_ROOT / "skills" / "gacm" / "reference" / "solver.md"

REQUIRED_SNIPPETS = (
    "Use this file after version routing.",
    "`v8.2` root docs are the bundled current baseline for solver guidance in this skill.",
    "This shared doc is intentionally CLI-first and configuration-first.",
    "Inspect `exe/logs/main_log.txt` or the console output before editing solver settings.",
    "Edit the active solver configuration referenced by the scenario, not a random example file",
    "Make one solver change at a time.",
    "In modern families, Broyden should always remain in the configured solver sequence",
    "Use `input/extra/supply_demand_curves.xml` when available to inspect problematic markets",
    "`v3.2` uses Newton-Raphson-centered terminology such as `solvable-nr`",
    "If conservative solver edits do not change the failure mode, stop assuming it is a tuning issue.",
)


def main() -> int:
    text = SOLVER_DOC.read_text(encoding="utf-8")
    errors: list[str] = []

    for snippet in REQUIRED_SNIPPETS:
        if snippet not in text:
            errors.append(f"solver.md drifted; missing required snippet: {snippet}")

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Solver contract validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
