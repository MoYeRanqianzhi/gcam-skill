#!/usr/bin/env python3
"""
Validate bundled page-level GCAM references.

Checks local markdown links inside `reference/version_pages/` and reports any
targets that do not resolve to a bundled file.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from version_catalog import VERSION_PAGES_ROOT


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"(^```.*?^```[ \t]*\n?)", re.MULTILINE | re.DOTALL)
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
RAW_MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
RAW_HTML_IMG_RE = re.compile(r"<img\b", re.IGNORECASE)
RAW_HTML_BUTTON_RE = re.compile(r"<button\b|onclick\s*=", re.IGNORECASE)
RAW_HTML_FONT_RE = re.compile(r"</?font\b", re.IGNORECASE)
RAW_HTML_STYLE_TAG_RE = re.compile(r"<style\b|</style>", re.IGNORECASE)
RAW_HTML_CLASS_ATTR_RE = re.compile(
    r"<[A-Za-z][^>]*\sclass\s*=\s*(?:\"[^\"]*\"|'[^']*')",
    re.IGNORECASE,
)
RAW_HTML_HREF_RE = re.compile(r"<a\b[^>]*href\s*=", re.IGNORECASE)
RAW_HTML_TABLE_RE = re.compile(r"</?(?:table|tr|td|th)\b", re.IGNORECASE)
RAW_HTML_STYLED_SPAN_RE = re.compile(r"<span\b[^>]*style=", re.IGNORECASE)
RAW_HTML_BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
RAW_HTML_INLINE_FORMATTING_RE = re.compile(r"</?(?:cite|i|em)\b", re.IGNORECASE)
RAW_PRESENTATIONAL_ATTR_RE = re.compile(
    r"(?:\bstyle\s*=|\balign\s*=|\bvalign\s*=|\browspan\s*=|\bcolspan\s*=|\bwidth\s*=|\bheight\s*=)",
    re.IGNORECASE,
)
RAW_MD_ATTR_LINE_RE = re.compile(r"(?m)^[ \t]*\{:\s*[^}\n]+\}[ \t]*$")
ESCAPED_WIKI_REF_RE = re.compile(r"&lt;ref\b|&lt;/ref&gt;|%3C/ref%3E", re.IGNORECASE)
ESCAPED_WIKI_REFERENCES_RE = re.compile(r"&lt;references\b", re.IGNORECASE)
LEGACY_IMAGE_RE = re.compile(r"Image reference:")
PLACEHOLDER_IMAGE_RE = re.compile(r"\[\[IMAGE_OMITTED:")
WINDOWS_ABS_RE = re.compile(r"\b[A-Za-z]:[\\/]")
POSIX_USER_HOME_RE = re.compile(r"(?<![A-Za-z])/(?:Users|home)/[A-Za-z0-9_.-]+/")
URI_RE = re.compile(r"\b(?:file|vscode)://", re.IGNORECASE)
GENERIC_WINDOWS_PLACEHOLDER_RE = re.compile(r"(?i)\b[A-Za-z]:[\\/]path(?:[\\/]|$)")
RAW_GUI_PATH_RE = re.compile(r"`File -> (?:Manage DB|Export)`|Click on each box for a more detailed description", re.IGNORECASE)


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


def normalize_portability_line(line: str) -> str:
    normalized = GENERIC_WINDOWS_PLACEHOLDER_RE.sub("", line)
    normalized = normalized.replace("<JAVA_HOME>", "")
    normalized = normalized.replace("<USER_HOME>", "")
    return normalized


def main() -> int:
    errors: list[str] = []
    roots = sorted(VERSION_PAGES_ROOT.rglob("*.md"))
    lowered_paths: dict[str, list[str]] = defaultdict(list)
    for page in roots:
        rel = page.relative_to(VERSION_PAGES_ROOT).as_posix()
        lowered_paths[rel.lower()].append(rel)
        if page.name == "INDEX.md":
            errors.append(
                f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> legacy INDEX.md remains; use BUNDLE_INDEX.md for generated directory indexes"
            )
    for lowered, items in sorted(lowered_paths.items()):
        if len(items) > 1:
            errors.append(
                "Case-insensitive bundled page path collision remains: " + " | ".join(items)
            )
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
        if RAW_HTML_BUTTON_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html widget/button markup remains")
        if RAW_HTML_FONT_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html font tag remains")
        if RAW_HTML_STYLE_TAG_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html style block remains")
        if RAW_HTML_CLASS_ATTR_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html class attribute remains")
        if RAW_HTML_HREF_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html href anchor remains")
        if RAW_HTML_TABLE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html table markup remains")
        if RAW_HTML_STYLED_SPAN_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw styled span markup remains")
        if RAW_HTML_BREAK_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw html line-break tag remains")
        if RAW_HTML_INLINE_FORMATTING_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> raw inline html formatting tag remains")
        if RAW_PRESENTATIONAL_ATTR_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> presentational table/html attributes remain")
        if RAW_MD_ATTR_LINE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> markdown attribute-list residue remains")
        if ESCAPED_WIKI_REF_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> escaped legacy wiki ref markup remains")
        if ESCAPED_WIKI_REFERENCES_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> escaped legacy wiki references marker remains")
        if LEGACY_IMAGE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> legacy image reference marker remains")
        if PLACEHOLDER_IMAGE_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> unresolved image placeholder remains")
        if RAW_GUI_PATH_RE.search(text):
            errors.append(f"{page.relative_to(VERSION_PAGES_ROOT.parent)} -> residual GUI/menu-path phrasing remains")
        for line_no, line in enumerate(text.splitlines(), start=1):
            normalized_line = normalize_portability_line(line)
            if (
                WINDOWS_ABS_RE.search(normalized_line)
                or POSIX_USER_HOME_RE.search(normalized_line)
                or URI_RE.search(normalized_line)
            ):
                snippet = line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:157] + "..."
                errors.append(
                    f"{page.relative_to(VERSION_PAGES_ROOT.parent)}:{line_no} -> non-portable absolute path or file URI remains: {snippet}"
                )
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
