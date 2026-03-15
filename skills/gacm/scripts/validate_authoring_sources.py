#!/usr/bin/env python3
"""
Validate the bundled-page authoring sources before regeneration.
"""

from __future__ import annotations

from generate_bundled_pages import validate_authoring_sources


def main() -> int:
    errors = validate_authoring_sources()
    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1
    print("Authoring sources validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
