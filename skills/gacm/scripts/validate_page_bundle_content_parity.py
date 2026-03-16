#!/usr/bin/env python3
"""
Validate that generated page-bundle markdown files match generator output.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import generate_bundled_pages as gbp


ACTUAL_ROOT = gbp.VERSION_PAGES_ROOT


def normalize_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")


def main() -> int:
    errors: list[str] = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir) / "version_pages"
        exit_code = gbp.main(output_root=temp_root)
        if exit_code != 0:
            print(f"generate_bundled_pages.py failed during parity validation with exit {exit_code}")
            return exit_code

        actual_files = sorted(path.relative_to(ACTUAL_ROOT) for path in ACTUAL_ROOT.rglob("*.md"))
        expected_files = sorted(path.relative_to(temp_root) for path in temp_root.rglob("*.md"))
        if actual_files != expected_files:
            missing = [item.as_posix() for item in expected_files if item not in actual_files]
            extra = [item.as_posix() for item in actual_files if item not in expected_files]
            if missing:
                errors.append("Missing generated page bundle files: " + ", ".join(missing[:20]))
            if extra:
                errors.append("Unexpected generated page bundle files: " + ", ".join(extra[:20]))
        for rel_path in actual_files:
            if rel_path not in expected_files:
                continue
            actual_text = normalize_text(ACTUAL_ROOT / rel_path)
            expected_text = normalize_text(temp_root / rel_path)
            if actual_text != expected_text:
                errors.append(
                    f"Generated page bundle drifted from generator output: {rel_path.as_posix()}"
                )
                if len(errors) >= 50:
                    break

    if errors:
        for item in errors:
            print(item)
        return 1

    print("Page bundle content parity validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
