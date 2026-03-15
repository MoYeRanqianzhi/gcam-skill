#!/usr/bin/env python3
"""
Validate generated page-bundle README and INDEX files.
"""

from __future__ import annotations

from generate_bundled_pages import (
    FULL_TREE_VERSIONS,
    render_delta_index,
    render_full_tree_index,
    render_root_readme,
    version_page_root,
)
from version_catalog import VERSION_PAGES_ROOT, ordered_versions


def main() -> int:
    errors: list[str] = []

    readme_path = VERSION_PAGES_ROOT / "README.md"
    actual_readme = readme_path.read_text(encoding="utf-8")
    expected_readme = render_root_readme()
    if actual_readme != expected_readme:
        errors.append("version_pages/README.md drifted from generate_bundled_pages.py")

    for info in ordered_versions():
        root = version_page_root(info.version)
        index_path = root / "INDEX.md"
        actual = index_path.read_text(encoding="utf-8")
        if info.version in FULL_TREE_VERSIONS:
            page_paths = sorted(
                path.relative_to(root)
                for path in root.rglob("*.md")
                if path.name != "INDEX.md"
            )
            expected = render_full_tree_index(info.version, page_paths)
        else:
            expected = render_delta_index(info.version)
        if actual != expected:
            errors.append(
                f"version_pages/{info.version}/INDEX.md drifted from generate_bundled_pages.py"
            )

    if errors:
        for item in errors:
            print(item)
        return 1

    print("Page bundle indexes validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
