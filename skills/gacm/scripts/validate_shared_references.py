#!/usr/bin/env python3
"""
Validate shared GCAM skill references.

Checks:
- all shared topic docs listed in version_catalog exist
- version_inventory shared topic bullets match version_catalog COMMON_TOPICS
- navigation covers the shared topic docs
- real local `.md` / `.py` references in SKILL.md and shared docs resolve

Notes:
- ignore template placeholders such as `<version>`
- ignore wildcard examples such as `versions/*.md`
- ignore descriptive upstream source-topic names that are not local skill files
"""

from __future__ import annotations

import re
from pathlib import Path

from version_catalog import REFERENCE_ROOT, bundled_topic_docs


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SKILL_FILE = REPO_ROOT / "skills" / "gacm" / "SKILL.md"
VERSION_INVENTORY = REFERENCE_ROOT / "version_inventory.md"
NAVIGATION = REFERENCE_ROOT / "navigation.md"
SHARED_DOCS = {path.name for path in REFERENCE_ROOT.glob("*.md")}
SCRIPT_DOCS = {path.name for path in (REPO_ROOT / "skills" / "gacm" / "scripts").glob("*.py")}

HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
BULLET_CODE_RE = re.compile(r"^\s*-\s+`([^`]+)`", re.MULTILINE)
CODE_FILE_RE = re.compile(
    r"`((?:reference/|version_pages/|versions/|scripts/|docs/)?[^`\n]*\.(?:md|py)(?:[#?][^`\n]+)?)`"
)


def extract_section(text: str, heading: str) -> str:
    matches = list(HEADER_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip() != heading:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[start:end]
    raise ValueError(f"Missing section: {heading}")


def resolve_doc_reference(base: Path, ref: str) -> Path | None:
    normalized = ref.split("#", 1)[0].split("?", 1)[0]
    if any(token in normalized for token in ("<", ">", "*", "{", "}")):
        return None
    if normalized.startswith(("http://", "https://")):
        return None
    candidate = Path(normalized)
    if candidate.suffix not in {".md", ".py"}:
        return None
    if normalized.startswith("reference/"):
        return REFERENCE_ROOT / normalized[len("reference/") :]
    if normalized.startswith("version_pages/"):
        return REFERENCE_ROOT / normalized
    if normalized.startswith("versions/"):
        return REFERENCE_ROOT / normalized
    if normalized.startswith("scripts/"):
        return REPO_ROOT / "skills" / "gacm" / normalized
    if normalized.startswith("docs/"):
        return REPO_ROOT / normalized
    if candidate.name == normalized:
        if base.parent == REFERENCE_ROOT and normalized in SHARED_DOCS:
            return REFERENCE_ROOT / normalized
        if base.parent == (REPO_ROOT / "skills" / "gacm" / "scripts") and normalized in SCRIPT_DOCS:
            return REPO_ROOT / "skills" / "gacm" / "scripts" / normalized
        return None
    resolved = (base.parent / candidate).resolve()
    if resolved.exists():
        return resolved
    return None


def validate_topic_files(errors: list[str]) -> None:
    for topic in bundled_topic_docs():
        path = REFERENCE_ROOT / topic
        if not path.exists():
            errors.append(f"Missing bundled topic doc: {topic}")


def validate_version_inventory(errors: list[str]) -> None:
    text = VERSION_INVENTORY.read_text(encoding="utf-8")
    section = extract_section(text, "Shared Topic Docs")
    listed = BULLET_CODE_RE.findall(section)
    expected = list(bundled_topic_docs())
    if listed != expected:
        errors.append(
            "version_inventory shared topic list drifted from version_catalog COMMON_TOPICS"
        )


def validate_navigation(errors: list[str]) -> None:
    text = NAVIGATION.read_text(encoding="utf-8")
    referenced = set(CODE_FILE_RE.findall(text))
    expected = set(bundled_topic_docs()) - {"navigation.md"}
    missing = sorted(item for item in expected if item not in referenced)
    if missing:
        errors.append(
            "navigation is missing shared topic references: " + ", ".join(missing)
        )


def validate_local_refs(errors: list[str]) -> None:
    docs = [SKILL_FILE, *sorted(REFERENCE_ROOT.glob("*.md"))]
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for ref in CODE_FILE_RE.findall(text):
            resolved = resolve_doc_reference(doc, ref)
            if resolved is None:
                continue
            if not resolved.exists():
                errors.append(f"{doc.relative_to(REPO_ROOT)} -> missing local reference: {ref}")


def main() -> int:
    errors: list[str] = []
    validate_topic_files(errors)
    validate_version_inventory(errors)
    validate_navigation(errors)
    validate_local_refs(errors)

    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1

    print("Shared references validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
