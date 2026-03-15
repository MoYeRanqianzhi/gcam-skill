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

ROOT_REQUIRED_FILES = (
    "index.md",
    "overview.md",
    "user-guide.md",
    "gcam-build.md",
    "updates.md",
)
ROOT_REQUIRED_DIRS = ("dev-guide",)

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
LINKED_IMAGE_RE = re.compile(r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)")
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"<img\b[^>]*\/?>", re.IGNORECASE)
HTML_IMG_SRC_RE = re.compile(r'src="([^"]+)"', re.IGNORECASE)
HTML_IMG_ALT_RE = re.compile(r'alt="([^"]+)"', re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r'(?P<prefix>href=")(?P<target>[^"]+)(?P<suffix>")', re.IGNORECASE)
HEADING_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"(^```.*?^```[ \t]*\n?)", re.MULTILINE | re.DOTALL)
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
CROSS_VERSION_TOC_RE = re.compile(r"^v\d+\.\d+/")
IMAGE_PLACEHOLDER_RE = re.compile(r"\[\[IMAGE_OMITTED:([^\]]+)\]\]")
FIGURE_ARTIFACT_RE = re.compile(r"(?i)(?:<br\s*/?>|&lt;br&gt;|&nbsp;|\{:\s*\.fig\s*\})")
WINDOWS_JAVA_INCLUDE_RE = re.compile(
    r"(?i)\b[A-Za-z]:[\\/](?:Program Files|Program Files \(x86\))[\\/]Java[\\/][^\\/\s`]+[\\/]include\b"
)
WINDOWS_JAVA_LIB_RE = re.compile(
    r"(?i)\b[A-Za-z]:[\\/](?:Program Files|Program Files \(x86\))[\\/]Java[\\/][^\\/\s`]+[\\/]lib\b"
)
WINDOWS_JAVA_HOME_RE = re.compile(
    r"(?i)\b[A-Za-z]:[\\/](?:Program Files|Program Files \(x86\))[\\/]Java[\\/][^\\/\s`]+\b"
)
POSIX_USER_HOME_RE = re.compile(r"(?<![A-Za-z])/(?:Users|home)/[A-Za-z0-9_.-]+")

WIKILINK_ALIAS_MAP = {
    "v3.2": {
        "Main_Page": "toc.md",
    },
}

ALT_SOURCE_RELATIONS = {
    "Agriculture,_Land-Use,_and_Bioenergy.md": ("Agriculture_Land-Use_and_Bioenergy.md",),
    "Cycle-breaking-in-GCAM.md": ("Cycle-breaking_in_GCAM.md",),
}

VERSION_INDEX = {version: index for index, version in enumerate(FULL_TREE_VERSIONS)}


def validate_authoring_sources() -> list[str]:
    errors: list[str] = []
    if not AUTHORING_ROOT.exists():
        return [f"Missing authoring root: {AUTHORING_ROOT}"]

    expected_full_tree = tuple(
        info.version for info in ordered_versions() if info.coverage_mode != "delta-only"
    )
    if FULL_TREE_VERSIONS != expected_full_tree[::-1]:
        errors.append(
            "FULL_TREE_VERSIONS drifted from version_catalog non-delta-only versions"
        )

    expected_delta_versions = {
        info.version for info in ordered_versions() if info.coverage_mode == "delta-only"
    }
    if set(DELTA_SOURCE_MAP) != expected_delta_versions:
        missing = sorted(expected_delta_versions - set(DELTA_SOURCE_MAP))
        extra = sorted(set(DELTA_SOURCE_MAP) - expected_delta_versions)
        if missing:
            errors.append("DELTA_SOURCE_MAP missing versions: " + ", ".join(missing))
        if extra:
            errors.append("DELTA_SOURCE_MAP has unexpected versions: " + ", ".join(extra))

    for name in ROOT_REQUIRED_FILES:
        if not (AUTHORING_ROOT / name).exists():
            errors.append(f"Missing v8.2/root source file: gcam-doc/{name}")
    for name in ROOT_REQUIRED_DIRS:
        if not (AUTHORING_ROOT / name).exists():
            errors.append(f"Missing v8.2/root source directory: gcam-doc/{name}")

    if not list(iter_v82_source_files()):
        errors.append("No markdown source files found in the v8.2/root authoring tree")

    for version in FULL_TREE_VERSIONS:
        if version == "v8.2":
            continue
        source_root = AUTHORING_ROOT / version
        if not source_root.exists():
            errors.append(f"Missing full-tree version source directory: gcam-doc/{version}")
            continue
        if not any(source_root.rglob("*.md")):
            errors.append(f"No markdown source files found in: gcam-doc/{version}")

    for version, refs in DELTA_SOURCE_MAP.items():
        for rel_path, _confidence in refs:
            candidate = AUTHORING_ROOT / rel_path
            if not candidate.exists():
                errors.append(f"{version} -> missing CMP source file: gcam-doc/{rel_path}")

    return errors


def strip_front_matter(text: str) -> tuple[str, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


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


def normalize_image_label(label: str) -> str:
    cleaned = label.strip().strip('"').strip("'")
    cleaned = cleaned.replace("fig:", "").replace("html-image", "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def image_label_from_alt_or_path(alt: str, path: str) -> str:
    label = normalize_image_label(alt)
    if label and label.lower() != "untitled image":
        return label
    stem = Path(path.split("#", 1)[0].split("?", 1)[0]).stem
    stem = normalize_image_label(stem.replace("_", " ").replace("-", " "))
    return stem or "figure"


def html_image_label(tag: str) -> str:
    alt_match = HTML_IMG_ALT_RE.search(tag)
    src_match = HTML_IMG_SRC_RE.search(tag)
    alt = alt_match.group(1) if alt_match else ""
    src = src_match.group(1) if src_match else ""
    return image_label_from_alt_or_path(alt, src)


def rewrite_images(text: str) -> str:
    text = LINKED_IMAGE_RE.sub(
        lambda m: f"[{image_label_from_alt_or_path(m.group(1), m.group(2))}]({m.group(3)})",
        text,
    )
    text = MD_IMAGE_RE.sub(
        lambda m: f"[[IMAGE_OMITTED:{image_label_from_alt_or_path(m.group(1), m.group(2))}]]",
        text,
    )
    text = HTML_IMG_RE.sub(lambda m: f"[[IMAGE_OMITTED:{html_image_label(m.group(0))}]]", text)
    return text


def is_standalone_image_placeholder(line: str) -> bool:
    normalized = FIGURE_ARTIFACT_RE.sub(" ", line.strip())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return bool(IMAGE_PLACEHOLDER_RE.fullmatch(normalized))


def strip_image_artifacts(text: str) -> str:
    lines: list[str] = []
    for raw_line in text.splitlines():
        if raw_line.strip() == "{: .fig}":
            continue
        if is_standalone_image_placeholder(raw_line):
            continue
        line = IMAGE_PLACEHOLDER_RE.sub(lambda m: f"[omitted image: {m.group(1)}]", raw_line)
        lines.append(line.rstrip())
    return "\n".join(lines)


def sanitize_absolute_paths(text: str) -> str:
    text = WINDOWS_JAVA_INCLUDE_RE.sub(r"<JAVA_HOME>\\include", text)
    text = WINDOWS_JAVA_LIB_RE.sub(r"<JAVA_HOME>\\lib", text)
    text = WINDOWS_JAVA_HOME_RE.sub("<JAVA_HOME>", text)
    text = POSIX_USER_HOME_RE.sub("<USER_HOME>", text)
    return text


def split_target_and_title(raw: str) -> tuple[str, str]:
    value = raw.strip()
    if not value:
        return "", ""
    parts = value.rsplit(" ", 1)
    if len(parts) == 2:
        title = parts[1].strip()
        if len(title) >= 2 and title[0] == title[-1] and title[0] in {'"', "'"}:
            return parts[0].strip(), title[1:-1]
    return value, ""


def split_fragment(target: str) -> tuple[str, str]:
    if ".html$" in target:
        path, fragment = target.split(".html$", 1)
        return f"{path}.html", f"#{fragment}"
    if "#" in target:
        path, fragment = target.split("#", 1)
        return path, f"#{fragment}"
    return target, ""


def normalize_wikilink_path(version: str, target: str) -> str:
    alias_map = WIKILINK_ALIAS_MAP.get(version, {})
    if target in alias_map:
        return alias_map[target]
    cleaned = target.replace(",_", "_").replace(",", "_").replace(" ", "_")
    cleaned = re.sub(r"_+", "_", cleaned)
    if "." not in Path(cleaned).name:
        cleaned = f"{cleaned}.md"
    return cleaned


def normalize_path_target(version: str, target: str, title: str) -> str:
    cleaned = target.strip()
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1]
    if not cleaned or cleaned.startswith("#") or SCHEME_RE.match(cleaned):
        return cleaned

    path_part, fragment = split_fragment(cleaned)
    if title == "wikilink":
        path_part = normalize_wikilink_path(version, path_part)
    elif path_part.endswith(".html"):
        path_part = f"{path_part[:-5]}.md"
    elif path_part.endswith(".pdf"):
        path_part = f"{path_part[:-4]}.md"
    elif "." not in Path(path_part).name and not path_part.endswith("/"):
        path_part = f"{path_part}.md"

    if path_part == "../toc.md" and version != "v8.2":
        path_part = "../v8.2/toc.md"
    if CROSS_VERSION_TOC_RE.match(path_part):
        path_part = f"../{path_part}"
    return f"{path_part}{fragment}"


def rewrite_markdown_links(segment: str, version: str) -> str:
    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        target_raw = match.group(2)
        target, title = split_target_and_title(target_raw)
        normalized = normalize_path_target(version, target, title)
        return f"[{label}]({normalized})"

    return MARKDOWN_LINK_RE.sub(repl, segment)


def rewrite_html_hrefs(segment: str, version: str) -> str:
    def repl(match: re.Match[str]) -> str:
        normalized = normalize_path_target(version, match.group("target"), "")
        return f'{match.group("prefix")}{normalized}{match.group("suffix")}'

    return HTML_HREF_RE.sub(repl, segment)


def apply_outside_code_fences(text: str, transform) -> str:
    parts: list[str] = []
    last = 0
    for match in CODE_FENCE_RE.finditer(text):
        parts.append(transform(text[last : match.start()]))
        parts.append(match.group(0))
        last = match.end()
    parts.append(transform(text[last:]))
    return "".join(parts)


def sanitize_body(text: str, version: str) -> str:
    text = rewrite_images(text)
    text = apply_outside_code_fences(text, lambda chunk: rewrite_html_hrefs(rewrite_markdown_links(chunk, version), version))
    text = strip_image_artifacts(text)
    text = sanitize_absolute_paths(text)
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


def authoring_root_for(version: str) -> Path:
    if version == "v8.2":
        return AUTHORING_ROOT
    return AUTHORING_ROOT / version


def relative_source_path(version: str, path: Path) -> Path:
    return path.relative_to(authoring_root_for(version))


def source_root_label(version: str) -> str:
    if version == "v8.2":
        return "gcam-doc root tree"
    return f"gcam-doc/{version}"


def source_path_for(version: str, rel_path: Path) -> Path:
    return authoring_root_for(version) / rel_path


def render_source_page(
    bundle_version: str,
    source_version: str,
    source_path: Path,
    coverage_mode: str,
    note_lines: Iterable[str] = (),
) -> str:
    raw = source_path.read_text(encoding="utf-8", errors="ignore")
    front_matter, body = strip_front_matter(raw)
    rel_source = relative_source_path(source_version, source_path)
    title = parse_title(front_matter, body, source_path.stem)
    body = strip_duplicate_heading(body, title)
    body = sanitize_body(body, bundle_version)
    lines = [
        f"# {title}",
        "",
        f"Bundled adapted source page for GCAM `{bundle_version}`.",
        "",
        f"- Source root: `{source_root_label(source_version)}`",
        f"- Source path: `{rel_source.as_posix()}`",
        f"- Coverage mode: `{coverage_mode}`",
        "- Bundle mode: `text-only page bundle; images omitted`",
        f"- Version page index: `version_pages/{bundle_version}/INDEX.md`",
    ]
    if source_version != bundle_version:
        lines.append(f"- Source provenance: inherited from `{source_version}` because `{bundle_version}` links to this page but its authoring tree does not contain a version-local copy")
    for note in note_lines:
        lines.append(f"- Note: {note}")
    lines.extend(
        [
            "",
            "Load this page when the user needs version-specific detail from this exact page family.",
            "",
            "---",
            "",
            body.rstrip(),
            "",
        ]
    )
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
        "",
        "## Release Summary",
    ]
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
            "",
        ]
    )
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


def render_cmp_trace_page(version: str, rel_path: Path) -> str:
    title = rel_path.stem.replace("_", " ")
    pdf_path = rel_path.with_suffix(".pdf").as_posix()
    lines = [
        f"# {title}",
        "",
        f"Bundled CMP trace page for GCAM `{version}`.",
        "",
        "- Coverage mode: `cmp trace page`",
        f"- Source root: `{source_root_label(version)}`",
        f"- Original linked asset: `{pdf_path}`",
        f"- Version page index: `version_pages/{version}/INDEX.md`",
        "",
        "This bundle stores a trace page instead of the original binary PDF asset.",
        "",
        "## Source Trace",
        f"- `{pdf_path}`",
        "",
    ]
    return "\n".join(lines)


def render_unresolved_trace_page(version: str, rel_path: Path) -> str:
    title = rel_path.stem.replace("_", " ")
    lines = [
        f"# {title}",
        "",
        f"Bundled unresolved trace page for GCAM `{version}`.",
        "",
        "- Coverage mode: `unresolved trace page`",
        f"- Source root: `{source_root_label(version)}`",
        f"- Missing linked page: `{rel_path.as_posix()}`",
        f"- Version page index: `version_pages/{version}/INDEX.md`",
        "",
        "The bundled authoring sources referenced this page, but no version-local or traceable inherited source file was found in the available repository snapshot.",
        "",
    ]
    return "\n".join(lines)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def version_page_root(version: str) -> Path:
    return VERSION_PAGES_ROOT / version


def find_target_source(version: str, rel_path: Path) -> tuple[str, Path] | None:
    candidate_rels = [rel_path]
    candidate_rels.extend(Path(item) for item in ALT_SOURCE_RELATIONS.get(rel_path.as_posix(), ()))

    current_index = VERSION_INDEX[version]
    earlier_versions = [FULL_TREE_VERSIONS[index] for index in range(current_index, -1, -1)]
    later_versions = [FULL_TREE_VERSIONS[index] for index in range(current_index + 1, len(FULL_TREE_VERSIONS))]
    search_versions = earlier_versions + later_versions

    for source_version in search_versions:
        for candidate_rel in candidate_rels:
            candidate_path = source_path_for(source_version, candidate_rel)
            if candidate_path.exists():
                return source_version, candidate_path
    return None


def extract_local_targets(text: str) -> list[str]:
    stripped = CODE_FENCE_RE.sub("", text)
    targets = [match.group(2).strip() for match in MARKDOWN_LINK_RE.finditer(stripped)]
    targets.extend(match.group("target").strip() for match in HTML_HREF_RE.finditer(stripped))
    return targets


def is_local_target(target: str) -> bool:
    return bool(target) and not target.startswith("#") and not SCHEME_RE.match(target)


def collect_missing_local_pages(version: str) -> list[Path]:
    root = version_page_root(version)
    missing: set[Path] = set()
    for page in sorted(root.rglob("*.md")):
        text = page.read_text(encoding="utf-8", errors="ignore")
        for raw_target in extract_local_targets(text):
            target, _title = split_target_and_title(raw_target)
            if not is_local_target(target):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (page.parent / target_path).resolve()
            try:
                rel = resolved.relative_to(root.resolve())
            except ValueError:
                continue
            if rel.suffix == ".md" and not resolved.exists():
                missing.add(rel)
    return sorted(missing)


def materialize_missing_target(version: str, rel_path: Path) -> bool:
    root = version_page_root(version)
    target = root / rel_path
    if target.exists():
        return False

    if "cmp" in rel_path.parts:
        write_file(target, render_cmp_trace_page(version, rel_path))
        return True

    inherited = find_target_source(version, rel_path)
    if inherited:
        source_version, source_path = inherited
        note = f"Referenced from `{version}` as `{rel_path.as_posix()}`."
        write_file(
            target,
            render_source_page(
                bundle_version=version,
                source_version=source_version,
                source_path=source_path,
                coverage_mode="inherited page bundle",
                note_lines=(note,),
            ),
        )
        return True

    write_file(target, render_unresolved_trace_page(version, rel_path))
    return True


def ensure_missing_targets(version: str) -> None:
    while True:
        missing = collect_missing_local_pages(version)
        if not missing:
            return
        wrote_any = False
        for rel_path in missing:
            wrote_any = materialize_missing_target(version, rel_path) or wrote_any
        if not wrote_any:
            return


def build_full_tree_version(version: str) -> None:
    version_root = version_page_root(version)
    if version_root.exists():
        shutil.rmtree(version_root)

    for source_path in iter_full_tree_source_files(version):
        rel = relative_source_path(version, source_path)
        target = version_root / rel
        write_file(
            target,
            render_source_page(
                bundle_version=version,
                source_version=version,
                source_path=source_path,
                coverage_mode="full-tree page bundle",
            ),
        )

    ensure_missing_targets(version)

    page_paths = sorted(
        path.relative_to(version_root)
        for path in version_root.rglob("*.md")
        if path.name != "INDEX.md"
    )
    write_file(version_root / "INDEX.md", render_full_tree_index(version, page_paths))


def build_delta_version(version: str) -> None:
    version_root = version_page_root(version)
    if version_root.exists():
        shutil.rmtree(version_root)
    write_file(version_root / "release_note.md", render_delta_release_note(version))
    write_file(version_root / "cmp_index.md", render_delta_cmp_index(version))
    write_file(version_root / "INDEX.md", render_delta_index(version))


def write_root_readme() -> None:
    write_file(VERSION_PAGES_ROOT / "README.md", render_root_readme())


def render_root_readme() -> str:
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
        "- When a version links to a page that is absent from its own authoring tree, the bundle may include a clearly labeled inherited or trace page instead of silently dropping the route.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    errors = validate_authoring_sources()
    if errors:
        for item in errors[:200]:
            print(item)
        if len(errors) > 200:
            print(f"... truncated {len(errors) - 200} additional errors")
        return 1
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
