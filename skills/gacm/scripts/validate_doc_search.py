#!/usr/bin/env python3
"""
Validate representative `doc_search.py` behavior.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DOC_SEARCH = SCRIPT_DIR / "doc_search.py"
REPO_ROOT = SCRIPT_DIR.parent.parent.parent


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DOC_SEARCH), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def assert_ok(args: list[str], required: tuple[str, ...], errors: list[str]) -> None:
    completed = run(args)
    if completed.returncode != 0:
        errors.append(
            f"{' '.join(args)} -> expected success, got exit {completed.returncode}: {completed.stderr.strip()}"
        )
        return
    combined = completed.stdout + completed.stderr
    for token in required:
        if token not in combined:
            errors.append(f"{' '.join(args)} -> missing expected output token: {token}")


def assert_fail(args: list[str], required: tuple[str, ...], errors: list[str]) -> None:
    completed = run(args)
    if completed.returncode == 0:
        errors.append(f"{' '.join(args)} -> expected failure, got success")
        return
    combined = completed.stdout + completed.stderr
    for token in required:
        if token not in combined:
            errors.append(f"{' '.join(args)} -> missing expected failure token: {token}")


def main() -> int:
    errors: list[str] = []

    assert_ok(
        ["--list-versions"],
        ("v8.2\tmodern-comprehensive\tbundled-baseline", "v3.2\tlegacy-wiki\tversion-summary"),
        errors,
    )
    assert_ok(
        ["--version", "v3.2", "--scope", "pages", "--pattern", "Main_User_Workspace|ModelInterface.jar|gcam.exe -C"],
        ("reference\\version_pages\\v3.2\\",),
        errors,
    )
    assert_ok(
        ["--version", "v8.2", "--scope", "versions", "--pattern", "configuration_workflows|query_automation|workspace_layouts|version_operation_notes"],
        ("reference\\versions\\v8.2.md",),
        errors,
    )
    assert_ok(
        ["--root", "version_pages/v8.2", "--pattern", "run-gcam|ModelInterface.jar"],
        ("reference\\version_pages\\v8.2\\",),
        errors,
    )

    assert_fail(
        ["--version", "v9.9", "--scope", "topics", "--pattern", "baseline"],
        ("Unknown GCAM version: v9.9",),
        errors,
    )
    assert_fail(
        ["--root", "..", "--pattern", "baseline"],
        ("Custom root must stay under bundled reference directory",),
        errors,
    )

    if errors:
        for item in errors:
            print(item)
        return 1

    print("doc_search behavior validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
