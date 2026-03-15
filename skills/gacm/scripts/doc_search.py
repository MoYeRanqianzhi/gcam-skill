#!/usr/bin/env python3
"""
Search bundled `gacm` reference docs.

Examples:
  python scripts/doc_search.py --pattern "target finder"
  python scripts/doc_search.py --version v7.1 --pattern "hydrogen"
  python scripts/doc_search.py --version v8.2 --scope pages --pattern "GCAM-macro"
  python scripts/doc_search.py --list-versions
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

from version_catalog import REFERENCE_ROOT, VERSION_PAGES_ROOT, get_version_info, ordered_versions


def iter_files(root: Path, exts: Tuple[str, ...]) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in exts:
            yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in exts:
            yield path


def collect_search_paths(version: str | None, scope: str) -> List[Path]:
    paths: List[Path] = []
    if scope in {"all", "topics"}:
        paths.extend(path for path in REFERENCE_ROOT.glob("*.md"))
    if scope in {"all", "pages"} and version:
        bundle_root = VERSION_PAGES_ROOT / get_version_info(version).version
        if bundle_root.exists():
            paths.extend(iter_files(bundle_root, (".md",)))
    if scope == "pages" and not version:
        paths.extend(sorted((VERSION_PAGES_ROOT).rglob("*.md")))
    if scope in {"all", "versions"} and version:
        info = get_version_info(version)
        paths.append(REFERENCE_ROOT / "versions" / f"{info.version}.md")
    if scope in {"all", "versions"} and not version:
        paths.append(REFERENCE_ROOT / "version_inventory.md")
        paths.extend(sorted((REFERENCE_ROOT / "versions").glob("*.md")))
    return paths


def search_file(path: Path, pattern: re.Pattern, max_per_file: int) -> List[Tuple[int, str]]:
    matches: List[Tuple[int, str]] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for idx, line in enumerate(handle, start=1):
                if pattern.search(line):
                    matches.append((idx, line.rstrip()))
                    if len(matches) >= max_per_file:
                        break
    except OSError:
        return []
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Search bundled GCAM skill references.")
    parser.add_argument("--pattern", help="Regex or plain text to search for.")
    parser.add_argument("--version", help="Optional GCAM version filter.")
    parser.add_argument(
        "--scope",
        choices=("all", "topics", "versions", "pages"),
        default="all",
        help="Search topic docs, version route docs, bundled page docs, or any combination through 'all'.",
    )
    parser.add_argument(
        "--root",
        help="Optional custom file or directory under the bundled reference tree.",
    )
    parser.add_argument("--list-versions", action="store_true", help="Print bundled versions and exit.")
    parser.add_argument("--ext", default=".md", help="Comma-separated extensions to search.")
    parser.add_argument("--case-sensitive", action="store_true", help="Enable case-sensitive matching.")
    parser.add_argument("--max-matches", type=int, default=50, help="Maximum total matches to print.")
    parser.add_argument("--max-per-file", type=int, default=5, help="Maximum matches per file.")
    args = parser.parse_args()

    if args.list_versions:
        for info in ordered_versions():
            print(f"{info.version}\t{info.family}\t{info.coverage_mode}")
        return 0

    if not args.pattern:
        print("--pattern is required unless --list-versions is used.", file=sys.stderr)
        return 2

    exts = tuple(part.strip().lower() for part in args.ext.split(",") if part.strip())
    if not exts:
        print("No file extensions provided.", file=sys.stderr)
        return 2

    flags = 0 if args.case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(args.pattern, flags=flags)
    except re.error as exc:
        print(f"Invalid regex: {exc}", file=sys.stderr)
        return 2

    if args.root:
        root = Path(args.root)
        if not root.is_absolute():
            root = REFERENCE_ROOT / root
        if not root.exists():
            print(f"Custom root does not exist: {root}", file=sys.stderr)
            return 2
        search_paths = list(iter_files(root, exts))
    else:
        search_paths = []
        seen = set()
        for path in collect_search_paths(args.version, args.scope):
            if path.exists() and path not in seen:
                search_paths.append(path)
                seen.add(path)

    total = 0
    for path in search_paths:
        matches = search_file(path, pattern, args.max_per_file)
        if not matches:
            continue
        for line_no, text in matches:
            print(f"{path.relative_to(REFERENCE_ROOT.parent)}:{line_no}: {text}")
            total += 1
            if total >= args.max_matches:
                return 0

    if total == 0:
        print("No matches found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
