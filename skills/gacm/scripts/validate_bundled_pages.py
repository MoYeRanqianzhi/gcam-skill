#!/usr/bin/env python3
"""
Validate bundled page-level GCAM references.

Checks local markdown links inside `reference/version_pages/` and reports any
targets that do not resolve to a bundled file.
"""

from __future__ import annotations

import re
from pathlib import Path

from version_catalog import VERSION_PAGES_ROOT


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"(^```.*?^```[ \t]*\n?)", re.MULTILINE | re.DOTALL)
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
RAW_MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
RAW_HTML_IMG_RE = re.compile(r"<img\b", re.IGNORECASE)
LEGACY_IMAGE_RE = re.compile(r"Image reference:")
PLACEHOLDER_IMAGE_RE = re.compile(r"\[\[IMAGE_OMITTED:")


def strip_code_fences(text: str) -> str:
    return CODE_FENCE_RE.sub("", text)


def split_target(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    parts = value.rsplit(" ", 1)
    if len(parts) == 2:
        title = parts[1].strip()
        if len(title) >= 2 and title[0] == title[-1] and title[0] in {'"', "'"}:
            return parts[0].strip()
    return value


def should_ignore(target: str) -> bool:
    return not target or target.startswith("#") or bool(SCHEME_RE.match(target))


def normalize_target(base: Path, target: str) -> Path:
    target_path = target.split("#", 1)[0]
    return (base.parent / target_path).resolve()


def main() -> int:
    errors: list[str] = []
    roots = sorted(VERSION_PAGES_ROOT.rglob("*.md"))
    for page in roots:
        text = strip_code_fences(page.read_text(encoding="utf-8", errors="ignore"))
        for match in LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            target = split_target(raw_target)
            if should_ignore(target):
                continue
            resolved = normalize_target(page, target)
            if not resolved.exists():
                errors.append(
                    f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> missing target: {target}"
                )
        if RAW_MD_IMAGE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw markdown image syntax remains")
        if RAW_HTML_IMG_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html image tag remains")
        if LEGACY_IMAGE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> legacy image reference marker remains")
        if PLACEHOLDER_IMAGE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> unresolved image placeholder remains")
    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1
    print("All bundled page markdown links resolved and text-only checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
