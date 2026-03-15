#!/usr/bin/env python3
"""
Run the full bundled GCAM skill validation suite.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

VALIDATION_STEPS = (
    "validate_authoring_sources.py",
    "validate_bundled_pages.py",
    "validate_shared_references.py",
    "validate_version_routes.py",
)


def run_step(step: str) -> int:
    command = [sys.executable, str(SCRIPT_DIR / step)]
    print(f">>> {step}", flush=True)
    completed = subprocess.run(command, cwd=SCRIPT_DIR.parent.parent.parent)
    return completed.returncode


def main() -> int:
    failures: list[str] = []
    for step in VALIDATION_STEPS:
        code = run_step(step)
        if code != 0:
            failures.append(f"{step} (exit {code})")

    if failures:
        print("")
        print("Validation suite failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("")
    print("All GCAM skill validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
