#!/usr/bin/env python3
"""
Generate page-level bundled GCAM references for all versions.

This turns the authoring sources in `gcam-doc/` into self-contained,
versioned page bundles under `skills/gacm/reference/version_pages/`.
"""

from __future__ import annotations

import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from version_catalog import VERSION_PAGES_ROOT, get_version_info, ordered_versions


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
AUTHORING_ROOT = REPO_ROOT / "gcam-doc"
UPDATES_SOURCE = AUTHORING_ROOT / "updates.md"

FULL_TREE_VERSIONS = (
    "v3.2",
    "v4.2",
    "v4.3",
    "v4.4",
    "v5.1",
    "v5.2",
    "v5.3",
    "v5.4",
    "v6.0",
    "v7.0",
    "v7.1",
    "v8.2",
)

DELTA_SOURCE_MAP = {
    "v7.2": (("cmp/399-SSP_Database2024.pdf", "direct"),),
    "v7.3": (("cmp/394-Intermittent_electricity_integration.pdf", "direct"),),
    "v7.4": (),
    "v8.0": (("cmp/404-Base_Year_Update_Move_Model_Base_Year_to_2021.pdf", "direct"),),
    "v8.1": (("cmp/401-Ukraine_as_an_independent_region.pdf", "direct"),),
    "v8.2": (("cmp/403-Misc_Bugfix_2025.pdf", "direct"),),
    "v8.3": (("cmp/405-Gcamstr_A_String_Interning_in-GCAM.pdf", "direct"),),
    "v8.4": (("cmp/410-Socioeconomic_Macro_Data_compressed.pdf", "direct"),),
    "v8.5": (
        ("cmp/422-GCAM_Bugfix_Fall_2025.pdf", "direct"),
        ("cmp/403-Misc_Bugfix_2025.pdf", "related"),
    ),
    "v8.6": (("cmp/400-Electricity_Generation_CCS_Emission_Factors.pdf", "direct"),),
    "v8.7": (("cmp/408-Cement_Data_Updates.pdf", "direct"),),
}

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n*", re.DOTALL)
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"<img\b[^>]*src=\"([^\"]+)\"[^>]*\/?>", re.IGNORECASE)
MARKDOWN_HTML_LINK_RE = re.compile(r"\((?!https?://|mailto:|#)([^)]+?)\.html(#[^)]+)?\)")
HTML_HREF_RE = re.compile(r'(?P<prefix>href=")(?!https?://|mailto:|#)(?P<path>[^"]+?)\.html(?P<frag>#[^"]+)?(?P<suffix>")')
HEADING_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)


def strip_front_matter(text: str) -> tuple[str, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def parse_title(front_matter: str, body: str, fallback: str) -> str:
    for line in front_matter.splitlines():
        if line.lower().startswith("title:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            if value:
                return value
    match = HEADING_RE.search(body)
    if match:
        return match.group(1).strip()
    return fallback.replace("_", " ")


def strip_duplicate_heading(body: str, title: str) -> str:
    lines = body.splitlines()
    if not lines:
        return body
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        return body
    line = lines[idx].strip()
    if line.startswith("# "):
        candidate = line[2:].strip()
        if candidate == title:
            return "\n".join(lines[:idx] + lines[idx + 1 :]).lstrip("\n")
    return body


def rewrite_images(text: str) -> str:
    text = MD_IMAGE_RE.sub(lambda m: f"Image reference: {m.group(1) or 'untitled image'} ({m.group(2)})", text)
    text = HTML_IMG_RE.sub(lambda m: f"Image reference: html-image ({m.group(1)})", text)
    return text


def rewrite_internal_html_links(text: str) -> str:
    text = MARKDOWN_HTML_LINK_RE.sub(lambda m: f"({m.group(1)}.md{m.group(2) or ''})", text)
    text = HTML_HREF_RE.sub(
        lambda m: f'{m.group("prefix")}{m.group("path")}.md{m.group("frag") or ""}{m.group("suffix")}',
        text,
    )
    return text


def sanitize_body(text: str) -> str:
    text = rewrite_images(text)
    text = rewrite_internal_html_links(text)
    return text.strip() + "\n"


def iter_v82_source_files() -> Iterable[Path]:
    for path in sorted(AUTHORING_ROOT.glob("*.md")):
        if path.is_file():
            yield path
    dev_guide_root = AUTHORING_ROOT / "dev-guide"
    if dev_guide_root.exists():
        for path in sorted(dev_guide_root.rglob("*.md")):
            if path.is_file():
                yield path


def iter_full_tree_source_files(version: str) -> Iterable[Path]:
    if version == "v8.2":
        yield from iter_v82_source_files()
        return
    source_root = AUTHORING_ROOT / version
    for path in sorted(source_root.rglob("*.md")):
        if path.is_file():
            yield path


def relative_source_path(version: str, path: Path) -> Path:
    if version == "v8.2":
        return path.relative_to(AUTHORING_ROOT)
    return path.relative_to(AUTHORING_ROOT / version)


def source_root_label(version: str) -> str:
    if version == "v8.2":
        return "gcam-doc root tree"
    return f"gcam-doc/{version}"


def render_full_tree_page(version: str, source_path: Path) -> str:
    raw = source_path.read_text(encoding="utf-8", errors="ignore")
    front_matter, body = strip_front_matter(raw)
    rel_source = relative_source_path(version, source_path)
    title = parse_title(front_matter, body, source_path.stem)
    body = strip_duplicate_heading(body, title)
    body = sanitize_body(body)
    lines = [
        f"# {title}",
        "",
        f"Bundled adapted source page for GCAM `{version}`.",
        "",
        f"- Source root: `{source_root_label(version)}`",
        f"- Source path: `{rel_source.as_posix()}`",
        "- Coverage mode: `full-tree page bundle`",
        "",
        "Load this page when the user needs version-specific detail from this exact page family.",
        "",
        "---",
        "",
        body.rstrip(),
        "",
    ]
    return "\n".join(lines)


def group_page_paths(paths: list[Path]) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in paths:
        parts = path.parts
        group = parts[0] if len(parts) > 1 else "root"
        grouped[group].append(path)
    return dict(sorted(grouped.items()))


def render_full_tree_index(version: str, page_paths: list[Path]) -> str:
    info = get_version_info(version)
    grouped = group_page_paths(page_paths)
    lines = [
        f"# {version} Detailed Page Bundle",
        "",
        f"This directory is the page-level bundled reference set for GCAM `{version}`.",
        "",
        f"- Family: `{info.family}`",
        f"- Coverage mode: `{info.coverage_mode}`",
        f"- Source root: `{source_root_label(version)}`",
        f"- Page count: `{len(page_paths)}`",
        "",
        "Progressive-disclosure rule:",
        "- Start from the version route file.",
        "- Open this index only when the user needs page-level detail for this version.",
        "- Then open only the specific page file relevant to the task.",
        "",
        "## Bundled Pages",
    ]
    for group, items in grouped.items():
        lines.append("")
        lines.append(f"### {group}")
        for item in items:
            lines.append(f"- `{item.as_posix()}`")
    lines.append("")
    return "\n".join(lines)


def render_delta_release_note(version: str) -> str:
    info = get_version_info(version)
    lines = [
        f"# {version} Release Note",
        "",
        f"Bundled release-note page for GCAM `{version}`.",
        "",
        "- Coverage mode: `delta-only`",
        "- Source root: `gcam-doc root updates stream`",
        "- Source path: `updates.md`",
    ]
    lines.extend(
        [
            "",
            "## Release Summary",
        ]
    )
    for bullet in info.deltas or ("No delta summary recorded.",):
        lines.append(f"- {bullet}")
    if info.notes:
        lines.extend(["", "## Notes"])
        for bullet in info.notes:
            lines.append(f"- {bullet}")
    lines.extend(
        [
            "",
            "## Source Trace",
            "- `gcam-doc/updates.md`",
        ]
    )
    lines.append("")
    return "\n".join(lines)


def render_delta_cmp_index(version: str) -> str:
    cmp_refs = DELTA_SOURCE_MAP.get(version, ())
    lines = [
        f"# {version} CMP Index",
        "",
        f"Bundled CMP trace page for GCAM `{version}`.",
        "",
        "Confidence labels:",
        "- `direct`: filename maps directly to the release note title",
        "- `related`: filename appears related, but the mapping is not uniquely guaranteed by the visible filenames alone",
        "",
        "## CMP References",
    ]
    if not cmp_refs:
        lines.extend(
            [
                "- No uniquely identified CMP PDF is recorded for this version from the visible release-note and filename evidence alone.",
                "",
            ]
        )
        return "\n".join(lines)
    for ref, confidence in cmp_refs:
        lines.append(f"- `{ref}` ({confidence})")
    lines.append("")
    return "\n".join(lines)


def render_delta_index(version: str) -> str:
    info = get_version_info(version)
    cmp_refs = DELTA_SOURCE_MAP.get(version, ())
    lines = [
        f"# {version} Detailed Page Bundle",
        "",
        f"This directory is the bundled page-level delta set for GCAM `{version}`.",
        "",
        f"- Family: `{info.family}`",
        f"- Coverage mode: `{info.coverage_mode}`",
        "- Source root: `gcam-doc root updates stream`",
        f"- CMP reference count: `{len(cmp_refs)}`",
        "",
        "Progressive-disclosure rule:",
        "- Open `release_note.md` first.",
        "- Then inspect `cmp_index.md` if method provenance or release-document traceability matters.",
        "- Then combine those with the minimum bundled baseline topic docs needed for the task.",
        "",
        "## Bundled Files",
        "- `release_note.md`",
        "- `cmp_index.md`",
        "",
    ]
    return "\n".join(lines)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_full_tree_version(version: str) -> None:
    version_root = VERSION_PAGES_ROOT / version
    if version_root.exists():
        shutil.rmtree(version_root)
    written_paths: list[Path] = []
    for source_path in iter_full_tree_source_files(version):
        rel = relative_source_path(version, source_path)
        target = version_root / rel
        write_file(target, render_full_tree_page(version, source_path))
        written_paths.append(rel)
    write_file(version_root / "INDEX.md", render_full_tree_index(version, written_paths))


def build_delta_version(version: str) -> None:
    version_root = VERSION_PAGES_ROOT / version
    if version_root.exists():
        shutil.rmtree(version_root)
    write_file(version_root / "release_note.md", render_delta_release_note(version))
    write_file(version_root / "cmp_index.md", render_delta_cmp_index(version))
    write_file(version_root / "INDEX.md", render_delta_index(version))


def write_root_readme() -> None:
    lines = [
        "# Version Page Bundles",
        "",
        "This directory contains the page-level bundled reference trees for all GCAM versions represented by the `gacm` skill.",
        "",
        "Rules:",
        "- Open the exact version route file first.",
        "- Then open `version_pages/<version>/INDEX.md` only when page-level detail is needed.",
        "- For full-tree versions, page files are adapted from the authoring markdown sources.",
        "- For `delta-only` versions, page files capture the release delta and source trace rather than pretending a full standalone tree exists.",
        "",
    ]
    write_file(VERSION_PAGES_ROOT / "README.md", "\n".join(lines))


def main() -> int:
    VERSION_PAGES_ROOT.mkdir(parents=True, exist_ok=True)
    write_root_readme()
    for info in ordered_versions():
        if info.version in FULL_TREE_VERSIONS:
            build_full_tree_version(info.version)
        else:
            build_delta_version(info.version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
