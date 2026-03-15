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


def normalize_output(text: str) -> str:
    return text.replace("\\", "/").replace("\r\n", "\n")


def output_lines(completed: subprocess.CompletedProcess[str]) -> list[str]:
    combined = normalize_output(completed.stdout + completed.stderr)
    return [line for line in combined.splitlines() if line.strip()]


def assert_ok(args: list[str], required: tuple[str, ...], errors: list[str]) -> None:
    completed = run(args)
    if completed.returncode != 0:
        errors.append(
            f"{' '.join(args)} -> expected success, got exit {completed.returncode}: {completed.stderr.strip()}"
        )
        return
    combined = normalize_output(completed.stdout + completed.stderr)
    for token in required:
        if token not in combined:
            errors.append(f"{' '.join(args)} -> missing expected output token: {token}")


def assert_order(args: list[str], prefixes: tuple[str, ...], errors: list[str]) -> None:
    completed = run(args)
    if completed.returncode != 0:
        errors.append(
            f"{' '.join(args)} -> expected success, got exit {completed.returncode}: {completed.stderr.strip()}"
        )
        return

    lines = output_lines(completed)
    cursor = -1
    for prefix in prefixes:
        found = None
        for idx in range(cursor + 1, len(lines)):
            if lines[idx].startswith(prefix):
                found = idx
                break
        if found is None:
            errors.append(f"{' '.join(args)} -> missing ordered output prefix: {prefix}")
            return
        cursor = found


def assert_fail(args: list[str], required: tuple[str, ...], errors: list[str]) -> None:
    completed = run(args)
    if completed.returncode == 0:
        errors.append(f"{' '.join(args)} -> expected failure, got success")
        return
    combined = normalize_output(completed.stdout + completed.stderr)
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
        ("reference/version_pages/v3.2/",),
        errors,
    )
    assert_ok(
        ["--version", "v8.2", "--scope", "versions", "--pattern", "configuration_workflows|query_automation|workspace_layouts|version_operation_notes"],
        ("reference/versions/v8.2.md",),
        errors,
    )
    assert_ok(
        ["--version", "root", "--scope", "versions", "--pattern", "Current bundled baseline for this skill|root `gcam-doc` documentation tree"],
        ("reference/versions/v8.2.md",),
        errors,
    )
    assert_ok(
        ["--root", "version_pages/v8.2", "--pattern", "run-gcam|ModelInterface.jar"],
        ("reference/version_pages/v8.2/",),
        errors,
    )
    assert_ok(
        ["--version", "v7.2", "--scope", "pages", "--pattern", "SSP database updated to v3.0 / 2024 inputs|gcam-doc/updates.md"],
        ("reference/version_pages/v7.2/release_note.md",),
        errors,
    )
    assert_ok(
        ["--root", "version_pages/v8.2/BUNDLE_INDEX.md", "--pattern", "Page count|Bundled Pages"],
        ("reference/version_pages/v8.2/BUNDLE_INDEX.md",),
        errors,
    )
    assert_order(
        ["--pattern", "bundled current baseline", "--max-matches", "5"],
        ("reference/version_inventory.md:",),
        errors,
    )
    assert_order(
        ["--version", "v8.2", "--scope", "all", "--pattern", "v8.2", "--max-matches", "5"],
        (
            "reference/versions/v8.2.md:",
            "reference/version_pages/v8.2/BUNDLE_INDEX.md:",
        ),
        errors,
    )
    assert_order(
        ["--version", "v7.2", "--scope", "pages", "--pattern", "Release Note|Release Summary", "--max-matches", "5"],
        ("reference/version_pages/v7.2/release_note.md:",),
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
