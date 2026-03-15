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
from typing import Callable, Iterable

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
HTML_STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.IGNORECASE | re.DOTALL)
HTML_COL_TAG_RE = re.compile(r"</?col(?:group)?\b[^>]*\/?>", re.IGNORECASE)
HTML_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
HTML_BUTTON_RE = re.compile(r"<button\b[^>]*>(?P<label>.*?)</button>", re.IGNORECASE | re.DOTALL)
HTML_SPAN_RE = re.compile(r"<span\b[^>]*>(?P<content>.*?)</span>", re.IGNORECASE | re.DOTALL)
HTML_FONT_RE = re.compile(r"</?font\b[^>]*>", re.IGNORECASE)
HTML_LIST_RE = re.compile(r"<(?P<tag>ul|ol)\b[^>]*>(?P<body>.*?)</(?P=tag)>", re.IGNORECASE | re.DOTALL)
HTML_LIST_ITEM_RE = re.compile(r"<li\b[^>]*>(?P<item>.*?)</li>", re.IGNORECASE | re.DOTALL)
HTML_DL_RE = re.compile(r"<dl\b[^>]*>(?P<body>.*?)</dl>", re.IGNORECASE | re.DOTALL)
HTML_DT_DD_RE = re.compile(
    r"<dt\b[^>]*>(?P<term>.*?)</dt>\s*<dd\b[^>]*>(?P<desc>.*?)</dd>",
    re.IGNORECASE | re.DOTALL,
)
HTML_PRESENTATIONAL_ATTR_RE = re.compile(
    r'(?P<prefix><[A-Za-z][^>]*?)\s(?:class|style|align|valign|rowspan|colspan|width|height)\s*=\s*(?:"[^"]*"|\'[^\']*\')',
    re.IGNORECASE,
)
HTML_BOLD_RE = re.compile(r"<(?P<tag>b|strong)\b[^>]*>(?P<content>.*?)</(?P=tag)>", re.IGNORECASE | re.DOTALL)
HTML_EMPHASIS_RE = re.compile(
    r"<(?P<tag>cite|i|em)\b[^>]*>(?P<content>.*?)</(?P=tag)>",
    re.IGNORECASE | re.DOTALL,
)
HTML_PARAGRAPH_RE = re.compile(r"</?p\b[^>]*>", re.IGNORECASE)
HTML_HREF_ANCHOR_RE = re.compile(
    r'<a\b[^>]*href="(?P<target>[^"]+)"[^>]*>(?P<label>.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
HTML_SELF_CLOSING_NAMED_ANCHOR_RE = re.compile(
    r'<a\b[^>]*name="(?P<name>[^"]+)"[^>]*/>',
    re.IGNORECASE,
)
HTML_NAMED_ANCHOR_RE = re.compile(
    r'<a\b[^>]*name="(?P<name>[^"]+)"[^>]*?(?<!/)>(?P<label>.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
HTML_TABLE_RE = re.compile(r"<table\b[^>]*>(?P<body>.*?)</table>", re.IGNORECASE | re.DOTALL)
HTML_TABLE_ROW_RE = re.compile(r"<tr\b[^>]*>(?P<body>.*?)</tr>", re.IGNORECASE | re.DOTALL)
HTML_TABLE_CELL_RE = re.compile(r"<t[dh]\b[^>]*>(?P<body>.*?)</t[dh]>", re.IGNORECASE | re.DOTALL)
ESCAPED_HTML_STYLE_BLOCK_RE = re.compile(r"&lt;style\b.*?&gt;.*?&lt;/style&gt;", re.IGNORECASE | re.DOTALL)
ESCAPED_HTML_BR_RE = re.compile(r"&lt;br\s*/?&gt;", re.IGNORECASE)
ESCAPED_HTML_BUTTON_RE = re.compile(
    r"&lt;button\b.*?&gt;(?P<label>.*?)&lt;/button&gt;",
    re.IGNORECASE | re.DOTALL,
)
ESCAPED_HTML_SPAN_RE = re.compile(
    r"&lt;span\b.*?&gt;(?P<content>.*?)&lt;/span&gt;",
    re.IGNORECASE | re.DOTALL,
)
ESCAPED_HTML_FONT_RE = re.compile(r"&lt;/?font\b.*?&gt;", re.IGNORECASE)
ESCAPED_HTML_DIV_RE = re.compile(r"&lt;/?div\b.*?&gt;", re.IGNORECASE)
ESCAPED_WIKI_REF_SELF_CLOSING_RE = re.compile(
    r"&lt;ref\b[^&]*?/\s*&gt;",
    re.IGNORECASE,
)
ESCAPED_WIKI_REF_WITH_ENCODED_CLOSE_RE = re.compile(
    r"&lt;ref\b[^&]*?&gt;(?P<content>(?:(?!&lt;/ref&gt;).)*?%3C/ref%3E>)",
    re.IGNORECASE | re.DOTALL,
)
ESCAPED_WIKI_REF_RE = re.compile(
    r"&lt;ref\b[^&]*?&gt;(?P<content>.*?)&lt;/ref&gt;",
    re.IGNORECASE | re.DOTALL,
)
ESCAPED_WIKI_REF_UNCLOSED_RE = re.compile(
    r"&lt;ref\b[^&]*?&gt;(?P<content>.+)\Z",
    re.IGNORECASE | re.DOTALL,
)
ESCAPED_WIKI_REFERENCES_RE = re.compile(r"&lt;references\b[^&]*?/\s*&gt;", re.IGNORECASE)
TABLE_ATTR_ONLY_CELL_RE = re.compile(
    r'^(?:(?:style|align|valign|rowspan|colspan|width|height)\s*=\s*(?:"[^"]*"|\'[^\']*\'))'
    r'(?:\s+(?:(?:style|align|valign|rowspan|colspan|width|height)\s*=\s*(?:"[^"]*"|\'[^\']*\')))*$',
    re.IGNORECASE,
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HTML_HREF_RE = re.compile(r'(?P<prefix>href=")(?P<target>[^"]+)(?P<suffix>")', re.IGNORECASE)
MARKDOWN_ATTR_LINE_RE = re.compile(r"^[ \t]*\{:\s*[^}\n]+\}[ \t]*$", re.MULTILINE)
HEADING_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"(^```.*?^```[ \t]*\n?)", re.MULTILINE | re.DOTALL)
MISATTACHED_CODE_FENCE_RE = re.compile(r"(?<![\r\n])```")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
CROSS_VERSION_TOC_RE = re.compile(r"^v\d+\.\d+/")
IMAGE_PLACEHOLDER_RE = re.compile(r"\[\[IMAGE_OMITTED:([^\]]+)\]\]")
OMITTED_IMAGE_LINK_LABEL_RE = re.compile(r"\[omitted image:\s*(?P<label>.+?)\]", re.IGNORECASE)
LINKED_IMAGE_LABEL_PLACEHOLDER_RE = re.compile(
    r"\[\[(?:IMAGE_OMITTED:|omitted image:\s*)(?P<label>[^\]]+)\]\]\((?P<target>[^)]+)\)",
    re.IGNORECASE,
)
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
LEGACY_PREVIOUS_VERSION_RE = re.compile(
    r"^.*Click here for info on how to view a previous version\..*(?:\n|$)",
    re.MULTILINE,
)
USER_GUIDE_OPEN_DB_RE = re.compile(
    r"^Select `Open` from the Model Interface File menu.*(?:\n|$)",
    re.MULTILINE,
)
USER_GUIDE_DOWNLOAD_SITE_RE = re.compile(
    r"^.*To download GCAM you can follow the `Download GCAM` link in the upper right ha(?:d|nd) corner\..*$",
    re.MULTILINE,
)
USER_GUIDE_RUN_GCAM_RE = re.compile(
    r"^In order to run GCAM double click on (?:the `run-gcam` executable script|the executable) "
    r"or run the executable from the command line\.\s+You should see log messages scroll up the screen as GCAM "
    r"reads in xml files and begins solving each model period\. Log information for each run can be found in "
    r"`exe/logs/main_log\.txt`\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_RUN_GCAM_FAILURE_RE = re.compile(
    r"^The most common failure to run GCAM when double clicking the `run-gcam` executable script typically relate "
    r"to Java\.\s+Dealing with Java differs depending on your system\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_VIEW_OUTPUT_RE = re.compile(
    r"^To view model output open the ModelInterface application\. This multi-platform application is written in "
    r"java and requires that java be installed on your machine\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_RUN_QUERY_RE = re.compile(
    r'^To view data select one or more scenarios.*(?:\n|$)',
    re.MULTILINE,
)
USER_GUIDE_TABLE_VIEW_RE = re.compile(
    r"^A tabular data display will appear on the left and a simple graphical output will appear on the right\. "
    r"If multiple queries were selected, these will open in different tabs\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_SORTING_RE = re.compile(
    r"^\*Sorting\*: You can sort results in the Model Interface tables by clicking on the table heading\. "
    r"You can add secondary sorting by holding ctrl while click another column heading\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_SCREENSHOT_RE = re.compile(
    r"^Figure UG-[12]:\s+Screenshot of GCAM ModelInterface.*(?:\n|$)",
    re.MULTILINE,
)
USER_GUIDE_COPY_DATA_RE = re.compile(
    r"^\*Copying Data\*:.*(?:\n|$)",
    re.MULTILINE,
)
USER_GUIDE_MODELINTERFACE_SECTION_RE = re.compile(
    r"^The model interface is a GCAM tool to view GCAM results from the \[BaseX\]\(http://basex\.org\) XML "
    r"database or convert CSV files to XML\.\s+You may find a copy at the top level of your release package and "
    r"can be run by double clicking the `ModelInterface\.jar` \(on Mac this will be ModelInterface\.app\)\.\s+"
    r"This section will focus mainly on viewing results\.\s+It can be used in an \[interactive mode\]"
    r"\(#interactive-mode\) or users can set up \[batch query\]\(#modelinterface-batch-modes\) files to "
    r"automate dumping results to CSV or XLS\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_MODELINTERFACE_MAC_BUNDLE_RE = re.compile(
    r"^Note as of GCAM 4\.4 the ModelInterface package on the Mac.*?^```.*?^```[ \t]*\n?",
    re.MULTILINE | re.DOTALL,
)
USER_GUIDE_INTERACTIVE_INTRO_RE = re.compile(
    r"^Please see the \[Quick Start\]\([^)]+\) section for the basics on how to open an database and run queries\.\s+"
    r"The `Scenarios` and `Regions` sections get populated automatically from the GCAM results that are stored in "
    r"the database\.\s+The `Queries` are loaded from a query file\.\s+You can check the "
    r"`model_interface\.properties` file which is located in the folder as the `ModelInterface\.jar`(?: or if "
    r"using the `ModelInterface\.app` on the Mac in your home directory)?:\s*$",
    re.MULTILINE,
)
USER_GUIDE_QUERY_FILE_PROMPT_RE = re.compile(
    r"^Note if the query file is not found the ModelInterface will ask you to select a new one\. "
    r"Each query is represented in it'?s own XML syntax such as:\s*$",
    re.MULTILINE,
)
USER_GUIDE_QUERY_XML_SHARE_RE = re.compile(
    r"^This XML can be copied directly out of the ModelInterface by using Ctrl-C \(or CMD-C on Mac\) and pasted "
    r"back into the Model Interface or as text elsewhere such as email\.\s+Similarly the XML text can be copied "
    r"out of an email and pasted back into the Model Interface using Ctrl-V \(or CMD-V on Mac\)\.\s+This is a "
    r"handy short cut for sharing or editing queries\.\s+You will notice when queries are modified a `\*` appears "
    r"at the root of the q(?:eries|ueries)\.\s+You can choose to `File -> Save` to update the underlying query "
    r"file or use `File -> Save As` to save and switch to a new query file\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_QUERY_XML_TRANSFER_RE = re.compile(
    r"^The actual queries are of the same format as described \[above\]\(#interactive-mode\) and can be copied "
    r"out of a query file or pasted from the Model Interface\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_BATCH_FILE_INTERACTIVE_RE = re.compile(
    r'^Users can run this "batch query" file from an interactive Model Interface session by selecting '
    r"`File -> Batch File` and selecting the \"batch query\" file they wish to run\.\s+Users are then asked where "
    r"to save the results \(\.csv saves as CSV and \.xls saves to excel\) and which scenarios to run\.\s*$",
    re.MULTILINE,
)
USER_GUIDE_GUI_REGION_RE = re.compile(
    r"which can be any of the ones listed in the `Regions` section of the GUI",
    re.IGNORECASE,
)

GCAM_BUILD_PARALLEL_XCODE_RE = re.compile(
    r"^\* Xcode edit Build Settings -> Preprocessor Macros -> add `GCAM_PARALLEL_ENABLED=0`\s*$",
    re.MULTILINE,
)
GCAM_BUILD_PARALLEL_VISUAL_RE = re.compile(
    r"^\* Visual edit Project -> objects-main Properties -> C/C\+\+ -> Preprocessor -> Preprocessor Definitions "
    r"-> add `GCAM_PARALLEL_ENABLED=0`\s*$",
    re.MULTILINE,
)
GCAM_BUILD_XCODE_INTRO_RE = re.compile(
    r"^Mac users who would like to use the Xcode integrated development environment.*?Users can find the project "
    r"file under `(?P<project>[^`]+)`\. Once open you should change the `Scheme` to build the `Release` target\.\s+"
    r"You can find the scheme settings here:\s*$",
    re.MULTILINE,
)
GCAM_BUILD_XCODE_FINAL_RE = re.compile(
    r"^Finally sel(?:ect|cet) menu option `Product -> Build` to build GCAM\.\s+Once complete an executable will be "
    r"copied to `(?P<output>[^`]+)` and you can still use `(?P<wrapper>[^`]+)` to run it\.\s+Note that to run "
    r"GCAM from within Xcode, you must set the working directory to the `exe` directory within your workspace\. "
    r"This is done within the `Options` section of the current scheme\.\s*$",
    re.MULTILINE,
)
GCAM_BUILD_XCODE_INFO_TAB_RE = re.compile(
    r"^Then under the `Info` tab change the build configuration to `Release`:\s*$",
    re.MULTILINE,
)
GCAM_BUILD_VS_INTRO_RE = re.compile(
    r"^(?P<preamble>Users will need to have Microsoft Visual Studio C\+\+ compiler installed.*?)(?:Users can find "
    r"the project file under `(?P<project>[^`]+)`\.  Once open you should change the `Solution Configurations` "
    r"and `Solution Platform` to `Release` and `x64`:\s*)$",
    re.MULTILINE,
)
GCAM_BUILD_VS_TOOLSET_RE = re.compile(
    r"^Also you will likely have to change the `Platform Toolset` under menu "
    r"`Project -> objects-main Properties\.\.` to the latest toolset installed with your Visual Studio\.\s+Note "
    r"that to run GCAM from within Visual Studio, you must also set the working directory to the `exe` directory "
    r"within your workspace and update the \[PATH environment variable to find jvm\.dll\]\((?P<java_ref>[^)]+)\)\. "
    r"This is done within the same project properties dialog under the `Debugging` section and properties "
    r"`Working Directory` and `Environment`\.\s*$",
    re.MULTILINE,
)
GCAM_BUILD_VS_FINAL_RE = re.compile(
    r"^Finally select menu option `Build -> Build Solution` to build GCAM\.\s+Once complete an executable will be "
    r"copied to `(?P<output>[^`]+)` and you can still use `(?P<wrapper>[^`]+)` to run it\.\s*$",
    re.MULTILINE,
)
GCAM_BUILD_DEBUG_DB_IMPORT_RE = re.compile(
    r"^Which can subsequently be loaded into an XML database by using the \[Model Interface\]\(user-guide\.md#modelinterface\) "
    r"by opening a database, choosing `File -> Manage DB`, then Click `Add`, finally select the `debug_db\.xml` "
    r"document to add to the database\.\s+Note a _new_ database can be created by simply selecting an empty folder "
    r"to open as a database \(you will see a warning message about potentially deleting files \*\*and you should "
    r"pay attention to it\*\*\)\.\s*$",
    re.MULTILINE,
)
DATA_SYSTEM_IEA_EXPORT_RE = re.compile(
    r"The reason why `FLOW` should be displayed as `ID codes` is that in several cases, different flows with "
    r"different ID codes are assigned the same name \(e\.g\., \"EREFINER\" and \"TREFINER\" are differentiated "
    r"flows, but both are named \"Petroleum Refineries\"\)\. Once the full dataset is displayed, users can "
    r"select `File -> Export`, and select \"CSV\"\. The exported files should be named `(?P<oecd>[^`]+)` for "
    r"the OECD countries' energy balances, and `(?P<non>[^`]+)` for the non-OECD balances, and placed in the "
    r"`(?P<path>[^`]+)` folder\.",
    re.MULTILINE,
)
INDEX_DIAGRAM_CLICK_RE = re.compile(
    r"^\*\*GCAM diagram\. Click on each box for a more detailed description of that element\.\*\*\s*$",
    re.MULTILINE,
)

HECTOR_XCODE_UI_BLOCK_RE = re.compile(
    r"^3\. Open the GCAM project in Xcode\..*?^#### Building GCAM-Hector on Visual Studio\s*$",
    re.MULTILINE | re.DOTALL,
)
HECTOR_VISUAL_UI_BLOCK_RE = re.compile(
    r"^3\. Open the GCAM project in Visual Studio\..*?^## References\s*$",
    re.MULTILINE | re.DOTALL,
)
COMMUNITY_GUIDE_LATEST_DOC_PLACEHOLDER_RE = re.compile(
    r"^\\<cite latest version of model documentation\\>\s*$",
    re.MULTILINE | re.IGNORECASE,
)
DEV_GUIDE_GIT_POINT_AND_CLICK_RE = re.compile(
    r"Git can be used entirely through text commands, but there are also\s+graphical clients available, which "
    r"provide a point and click\s+interface, along with some visualization capabilities to help you\s+understand "
    r"how various branches relate to each other\.\s*",
    re.IGNORECASE | re.DOTALL,
)

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
BUNDLE_INDEX_NAME = "BUNDLE_INDEX.md"


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

    for version in FULL_TREE_VERSIONS:
        rel_buckets: dict[str, list[str]] = defaultdict(list)
        for source_path in iter_full_tree_source_files(version):
            rel = relative_source_path(version, source_path).as_posix()
            rel_buckets[rel.lower()].append(rel)
        for lowered, items in sorted(rel_buckets.items()):
            if len(items) > 1:
                errors.append(
                    f"{version} -> authoring tree has case-insensitive path collision: "
                    + " | ".join(items)
                )
            if lowered == BUNDLE_INDEX_NAME.lower():
                errors.append(
                    f"{version} -> authoring tree uses reserved generated bundle index name: {items[0]}"
                )

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
        line = LINKED_IMAGE_LABEL_PLACEHOLDER_RE.sub(
            lambda m: f"[{m.group('label').strip()}]({m.group('target')})",
            line,
        )
        lines.append(line.rstrip())
    return "\n".join(lines)


def sanitize_absolute_paths(text: str) -> str:
    text = WINDOWS_JAVA_INCLUDE_RE.sub(r"<JAVA_HOME>\\include", text)
    text = WINDOWS_JAVA_LIB_RE.sub(r"<JAVA_HOME>\\lib", text)
    text = WINDOWS_JAVA_HOME_RE.sub("<JAVA_HOME>", text)
    text = POSIX_USER_HOME_RE.sub("<USER_HOME>", text)
    return text


def apply_agent_text_adaptations(text: str, rel_source: Path) -> str:
    changed = False

    def replace(
        pattern: re.Pattern[str], replacement: str | Callable[[re.Match[str]], str]
    ) -> None:
        nonlocal text, changed
        updated = pattern.sub(replacement, text)
        if updated != text:
            text = updated
            changed = True

    updated = LEGACY_PREVIOUS_VERSION_RE.sub("", text)
    if updated != text:
        text = updated
        changed = True

    if rel_source.name == "user-guide.md":
        replace(
            USER_GUIDE_DOWNLOAD_SITE_RE,
            "This document provides information on acquiring and running the GCAM model. "
            "Agent adaptation: the upstream source referenced website navigation for release downloads; "
            "in this skill, resolve the target release from repository contents, version route docs, or release "
            "archives instead of relying on page layout. There will typically be separate platform release "
            "packages plus a source archive for rebuild workflows.\n",
        )
        replace(
            USER_GUIDE_RUN_GCAM_RE,
            "Agent adaptation: invoke GCAM from the shell instead of desktop launch. Expect log messages as GCAM "
            "reads XML inputs and solves each model period; inspect `exe/logs/main_log.txt` for run diagnostics.\n",
        )
        replace(
            USER_GUIDE_RUN_GCAM_FAILURE_RE,
            "The most common wrapper-launch failures when starting GCAM from packaged scripts typically relate to "
            "Java. Dealing with Java differs depending on your system.\n",
        )
        replace(
            USER_GUIDE_VIEW_OUTPUT_RE,
            "Agent adaptation: result inspection should start from batch or file-based query automation, not "
            "interactive ModelInterface browsing. The underlying ModelInterface tooling is still Java-based, so "
            "Java remains required when those query tools are used.\n",
        )
        replace(
            USER_GUIDE_OPEN_DB_RE,
            "Agent adaptation: the upstream source described interactive ModelInterface browsing here. "
            "For agent use, prefer headless query automation via `ModelInterface/InterfaceMain -b <batch.xml>`, "
            "post-run `XMLDBDriver.properties` batch queries, or the shared `reference/query_automation.md` guide.\n",
        )
        replace(
            USER_GUIDE_RUN_QUERY_RE,
            "Agent adaptation: interactive scenario/region/query selection is omitted in this text-only bundle. "
            "Treat scenario, region, and query names as identifiers for headless batch execution instead.\n",
        )
        replace(
            USER_GUIDE_TABLE_VIEW_RE,
            "Agent adaptation: interactive table/chart rendering is omitted in this text-only bundle. Treat query "
            "results as structured outputs to export, diff, sort, and visualize with shell or data-analysis tools.\n",
        )
        replace(
            USER_GUIDE_SORTING_RE,
            "*Agent adaptation*: Sort and reshape exported results with shell, Python, R, SQL, or spreadsheet "
            "automation rather than interactive table widgets.\n",
        )
        replace(USER_GUIDE_SCREENSHOT_RE, "")
        replace(
            USER_GUIDE_COPY_DATA_RE,
            "*Agent adaptation*: Prefer CSV/XLS export through headless batch queries or extraction libraries "
            "instead of manual copy/paste from the ModelInterface UI.\n",
        )
        replace(
            USER_GUIDE_MODELINTERFACE_SECTION_RE,
            "The model interface is the historical GCAM tool for querying [BaseX](http://basex.org) XML "
            "databases and converting CSV files to XML.\n\n"
            "Agent adaptation: the packaged `ModelInterface.jar` / `ModelInterface.app` is not the default "
            "workflow in this bundle. Prefer direct batch execution, query-file editing, and scripted CSV/XLS "
            "export.\n\n"
            "Agent adaptation: treat the `interactive mode` subsection below as historical context and prefer "
            "batch or direct file-based workflows.\n",
        )
        replace(
            USER_GUIDE_MODELINTERFACE_MAC_BUNDLE_RE,
            "Agent adaptation: older macOS packaging notes about `ModelInterface.app` bundle metadata are not the "
            "primary workflow for agents. Prefer invoking the jar from the shell or editing "
            "`model_interface.properties` directly in a text-accessible working directory.\n",
        )
        replace(
            USER_GUIDE_INTERACTIVE_INTRO_RE,
            "Agent adaptation: interactive mode is preserved only as historical context. For agent work, read "
            "scenario names from the database, region names from results or batch query files, and query "
            "definitions from XML files directly. Inspect `model_interface.properties` as plain text to locate "
            "the active query file, for example:\n",
        )
        replace(
            USER_GUIDE_QUERY_FILE_PROMPT_RE,
            "If the query file is not found, update the configured query-file path directly instead of relying on "
            "an interactive chooser. Each query is represented in its own XML syntax such as:\n",
        )
        replace(
            USER_GUIDE_QUERY_XML_SHARE_RE,
            "Agent adaptation: query XML is plain text. Copy it between files, repositories, or messages as "
            "needed, then edit and save the underlying query file directly instead of relying on GUI copy/paste "
            "or interactive save-menu actions.\n",
        )
        replace(
            USER_GUIDE_QUERY_XML_TRANSFER_RE,
            "The actual queries are the same XML definitions described [above](#interactive-mode) and can be "
            "copied between query files, repositories, or batch command files.\n",
        )
        replace(
            USER_GUIDE_BATCH_FILE_INTERACTIVE_RE,
            "Agent adaptation: the interactive batch-file menu path is omitted. The portable workflow is to "
            "reference the batch query file from a ModelInterface batch command file and execute it from the "
            "shell, setting output paths and scenario names in XML rather than interactive dialogs.\n",
        )
        replace(
            USER_GUIDE_GUI_REGION_RE,
            "which can be any of the region names available in the database or query context",
        )

    if rel_source.name == "index.md":
        replace(
            INDEX_DIAGRAM_CLICK_RE,
            "Agent adaptation: the upstream diagram navigation is rewritten below as text links grouped by topic.\n",
        )

    if rel_source.name == "gcam-build.md":
        replace(
            GCAM_BUILD_PARALLEL_XCODE_RE,
            "* Xcode project adaptation: set the preprocessor macro `GCAM_PARALLEL_ENABLED=0` if you must "
            "disable parallel GCAM in the Xcode project.\n",
        )
        replace(
            GCAM_BUILD_PARALLEL_VISUAL_RE,
            "* Visual Studio project adaptation: set the preprocessor definition `GCAM_PARALLEL_ENABLED=0` if "
            "you must disable parallel GCAM in the Visual Studio project.\n",
        )
        replace(
            GCAM_BUILD_XCODE_INTRO_RE,
            lambda match: (
                "Agent adaptation: the upstream Xcode walkthrough was UI-oriented. For agent workflows, prefer "
                "the Makefile build. If you must use the bundled Xcode project, the essential facts are the "
                f"project path `{match.group('project')}`, the compiler baseline noted above, and the need to use "
                "the `Release` configuration.\n"
            ),
        )
        replace(
            GCAM_BUILD_XCODE_FINAL_RE,
            lambda match: (
                "For Xcode-based builds, use the `Release` configuration and ensure the runtime working "
                "directory is the workspace `exe` directory. The resulting executable is copied to "
                f"`{match.group('output')}` and can still be launched with `{match.group('wrapper')}`.\n"
            ),
        )
        replace(GCAM_BUILD_XCODE_INFO_TAB_RE, "")
        replace(
            GCAM_BUILD_VS_INTRO_RE,
            lambda match: (
                f"{match.group('preamble').strip()} "
                f"The bundled project file is `{match.group('project')}`. Agent adaptation: if this project is "
                "used, treat `Release` + `x64` as the effective build configuration instead of relying on IDE "
                "menu selection.\n"
            ),
        )
        replace(
            GCAM_BUILD_VS_TOOLSET_RE,
            lambda match: (
                "If this Visual Studio project is used, update `Platform Toolset` to the newest installed "
                "toolset. For IDE or debugger launches, set the runtime working directory to the workspace `exe` "
                "directory and update the "
                f"[PATH environment variable to find jvm.dll]({match.group('java_ref')}) so the JVM runtime can "
                "be located.\n"
            ),
        )
        replace(
            GCAM_BUILD_VS_FINAL_RE,
            lambda match: (
                "Build the Visual Studio solution in `Release`/`x64`; the resulting executable is copied to "
                f"`{match.group('output')}` and can still be launched with `{match.group('wrapper')}`.\n"
            ),
        )
        replace(
            GCAM_BUILD_DEBUG_DB_IMPORT_RE,
            "Agent adaptation: `debug_db.xml` is a text XML dump of the results that would have been written to "
            "the XML database. Prefer importing it with scripted BaseX/XML tooling or headless ModelInterface "
            "batch workflows rather than interactive `Manage DB` steps. If you create a fresh database directory "
            "for that import, use a dedicated empty folder because initialization may remove existing contents.\n",
        )

    if rel_source.name == "hector.md":
        replace(
            HECTOR_XCODE_UI_BLOCK_RE,
            "3. Agent adaptation: skip the Xcode click path. Treat the following values as the relevant build "
            "facts:\n\n"
            "- Define `USE_HECTOR=1`.\n"
            "- Add linker flags `-lgsl -lgslcblas -lm`.\n"
            "- Add library search path `<path to gsl install>/lib`.\n"
            "- Add user header search path `../../climate/source/hector/headers`.\n"
            "- Set the C++ language dialect to `Compiler Default`.\n"
            "- Set the C++ standard library to `libstdc++`.\n"
            "- Ensure the workspace includes `cvs/objects/climate/source/hector/project_files/Xcode/hector.xcodeproj`.\n"
            "- Ensure the GCAM target links the Hector dependency/library pair `hector-lib` and `libhector-lib.a`.\n"
            "- After those settings are in place, rebuilding GCAM should rebuild and link Hector as needed.\n\n"
            "#### Building GCAM-Hector on Visual Studio\n",
        )
        replace(
            HECTOR_VISUAL_UI_BLOCK_RE,
            "3. Agent adaptation: skip the Visual Studio click path. Treat the following values as the relevant "
            "build facts:\n\n"
            "- Define `USE_HECTOR` in the project preprocessor settings.\n"
            "- Add include directory `..\\\\..\\\\climate\\\\source\\\\hector\\\\headers`.\n"
            "- Add library directory `<path to gsl install>/Release`.\n"
            "- Add link dependency `gsl.lib`.\n"
            "- Ensure the solution includes `cvs/objects/climate/source/hector/project_files/VS/hector-lib.vcxproj`.\n"
            "- Ensure `objects-main` references `hector-lib` so GCAM and Hector rebuild and link together as needed.\n"
            "- After those settings are in place, building the solution should rebuild and link Hector as needed.\n\n"
            "## References\n",
        )

    if rel_source.name == "data-system.md":
        replace(
            DATA_SYSTEM_IEA_EXPORT_RE,
            lambda match: (
                'The reason why `FLOW` should be displayed as `ID codes` is that in several cases, different '
                'flows with different ID codes are assigned the same name (e.g., "EREFINER" and "TREFINER" are '
                'differentiated flows, but both are named "Petroleum Refineries"). Once the full dataset is '
                "displayed, export it as CSV from the source tool. The exported files should be named "
                f"`{match.group('oecd')}` for the OECD countries' energy balances, and `{match.group('non')}` "
                f"for the non-OECD balances, and placed in the `{match.group('path')}` folder."
            ),
        )

    if rel_source.name == "community-guide.md":
        replace(
            COMMUNITY_GUIDE_LATEST_DOC_PLACEHOLDER_RE,
            "Source author note: insert a citation to the then-current GCAM model documentation release when "
            "preparing a paper-specific bibliography.\n",
        )

    if rel_source.parts[-2:] == ("dev-guide", "git.md"):
        replace(
            DEV_GUIDE_GIT_POINT_AND_CLICK_RE,
            "Git can be used entirely through text commands. Agent adaptation: prefer shell-based Git for GCAM "
            "workflows. Historical graphical clients are listed below only as ecosystem context for users who "
            "need them.\n\n",
        )

    if changed:
        text = re.sub(r"\n{3,}", "\n\n", text)
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


def normalize_inline_html(segment: str) -> str:
    def clean_fragment(raw: str) -> str:
        cleaned = HTML_PARAGRAPH_RE.sub(" ", raw)
        cleaned = re.sub(r"</?(?:ul|ol)\b[^>]*>", " ", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def render_html_list(body: str, ordered: bool) -> str:
        items = [clean_fragment(match.group("item")) for match in HTML_LIST_ITEM_RE.finditer(body)]
        items = [item for item in items if item]
        if not items:
            return ""
        if ordered:
            return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))
        return "\n".join(f"- {item}" for item in items)

    def normalize_html_definition_lists(text: str) -> str:
        def repl(match: re.Match[str]) -> str:
            blocks: list[str] = []
            for pair in HTML_DT_DD_RE.finditer(match.group("body")):
                term = clean_fragment(pair.group("term"))
                desc_raw = pair.group("desc")
                rendered_list = render_html_list(desc_raw, ordered=False)
                if rendered_list:
                    if term:
                        blocks.append(f"**{term}**\n\n{rendered_list}")
                    else:
                        blocks.append(rendered_list)
                    continue
                desc = clean_fragment(desc_raw)
                if term and desc:
                    blocks.append(f"- **{term}**: {desc}")
                elif term:
                    blocks.append(f"- **{term}**")
                elif desc:
                    blocks.append(f"- {desc}")
            if not blocks:
                return match.group(0)
            return "\n\n".join(blocks) + "\n"

        return HTML_DL_RE.sub(repl, text)

    def normalize_html_lists(text: str) -> str:
        def repl(match: re.Match[str]) -> str:
            rendered = render_html_list(match.group("body"), ordered=match.group("tag").lower() == "ol")
            if not rendered:
                return match.group(0)
            return rendered + "\n"

        return HTML_LIST_RE.sub(repl, text)

    def unwrap_button(match: re.Match[str]) -> str:
        label = match.group("label")
        label = re.sub(r"\s+", " ", label).strip()
        return label

    def unwrap_span(match: re.Match[str]) -> str:
        content = match.group("content")
        if content.strip():
            return content
        return match.group(0)

    def strip_presentational_attr(match: re.Match[str]) -> str:
        return match.group("prefix")

    def render_bold(match: re.Match[str]) -> str:
        content = re.sub(r"\s+", " ", match.group("content")).strip()
        if not content:
            return ""
        return f"**{content}**"

    def render_emphasis(match: re.Match[str]) -> str:
        content = re.sub(r"\s+", " ", match.group("content")).strip()
        if not content:
            return ""
        return f"*{content}*"

    def normalize_anchor_label(label: str) -> str:
        cleaned = HTML_PARAGRAPH_RE.sub(" ", label)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        placeholder_match = IMAGE_PLACEHOLDER_RE.fullmatch(cleaned)
        if placeholder_match:
            cleaned = placeholder_match.group(1).strip()
        omitted_match = OMITTED_IMAGE_LINK_LABEL_RE.fullmatch(cleaned)
        if omitted_match:
            cleaned = omitted_match.group("label").strip()
        return cleaned

    def render_href_anchor(match: re.Match[str]) -> str:
        label = normalize_anchor_label(match.group("label"))
        if not label:
            return match.group("target").strip()
        return f"[{label}]({match.group('target').strip()})"

    def render_named_anchor(match: re.Match[str]) -> str:
        name = match.group("name").strip()
        label = normalize_anchor_label(match.group("label"))
        anchor = f'<a name="{name}"></a>'
        if not label:
            return anchor
        return f"{anchor}{label}"

    def render_markdown_table(rows: list[list[str]]) -> str:
        def format_row(row: list[str]) -> str:
            escaped = [cell.replace("|", r"\|") for cell in row]
            return "| " + " | ".join(escaped) + " |"

        if not rows:
            return ""
        lines = [
            format_row(rows[0]),
            format_row(["---"] * len(rows[0])),
        ]
        for row in rows[1:]:
            lines.append(format_row(row))
        return "\n".join(lines)

    def normalize_html_tables(text: str) -> str:
        def clean_cell(raw: str) -> str:
            cleaned = HTML_PARAGRAPH_RE.sub(" ", raw)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            return cleaned

        def repl(match: re.Match[str]) -> str:
            rows: list[list[str]] = []
            for row_match in HTML_TABLE_ROW_RE.finditer(match.group("body")):
                cells = [
                    clean_cell(cell_match.group("body"))
                    for cell_match in HTML_TABLE_CELL_RE.finditer(row_match.group("body"))
                ]
                if cells:
                    rows.append(cells)
            if not rows:
                return ""
            width = max(len(row) for row in rows)
            padded = [row + [""] * (width - len(row)) for row in rows]
            keep_indexes = [
                index for index in range(width) if any(row[index].strip() for row in padded)
            ]
            compact = [[row[index] for index in keep_indexes] for row in padded]
            compact = [row for row in compact if any(cell.strip() for cell in row)]
            if not compact:
                return ""
            return render_markdown_table(compact) + "\n"

        return HTML_TABLE_RE.sub(repl, text)

    segment = HTML_STYLE_BLOCK_RE.sub("", segment)
    segment = HTML_COL_TAG_RE.sub("", segment)
    segment = HTML_BR_RE.sub("\n", segment)
    segment = normalize_html_definition_lists(segment)
    segment = normalize_html_lists(segment)
    segment = HTML_BUTTON_RE.sub(unwrap_button, segment)
    for _ in range(8):
        updated = HTML_SPAN_RE.sub(unwrap_span, segment)
        if updated == segment:
            break
        segment = updated
    segment = HTML_FONT_RE.sub("", segment)
    for _ in range(4):
        updated = HTML_PRESENTATIONAL_ATTR_RE.sub(strip_presentational_attr, segment)
        if updated == segment:
            break
        segment = updated
    segment = HTML_BOLD_RE.sub(render_bold, segment)
    for _ in range(4):
        updated = HTML_EMPHASIS_RE.sub(render_emphasis, segment)
        if updated == segment:
            break
        segment = updated
    segment = HTML_HREF_ANCHOR_RE.sub(render_href_anchor, segment)
    segment = HTML_SELF_CLOSING_NAMED_ANCHOR_RE.sub(
        lambda match: f'<a name="{match.group("name").strip()}"></a>',
        segment,
    )
    segment = HTML_NAMED_ANCHOR_RE.sub(render_named_anchor, segment)
    segment = normalize_html_tables(segment)
    segment = segment.replace("&nbsp;", " ")
    return segment


def normalize_escaped_inline_html(segment: str) -> str:
    def unwrap_button(match: re.Match[str]) -> str:
        label = match.group("label")
        label = re.sub(r"\s+", " ", label).strip()
        return label

    def unwrap_span(match: re.Match[str]) -> str:
        return match.group("content")

    segment = ESCAPED_HTML_STYLE_BLOCK_RE.sub("", segment)
    segment = ESCAPED_HTML_BR_RE.sub("\n", segment)
    segment = ESCAPED_HTML_BUTTON_RE.sub(unwrap_button, segment)
    for _ in range(8):
        updated = ESCAPED_HTML_SPAN_RE.sub(unwrap_span, segment)
        if updated == segment:
            break
        segment = updated
    segment = ESCAPED_HTML_FONT_RE.sub("", segment)
    segment = ESCAPED_HTML_DIV_RE.sub("\n", segment)
    return segment


def normalize_escaped_wiki_refs(segment: str) -> str:
    def render_ref(content: str) -> str:
        normalized = content.replace("%3C/ref%3E", "")
        normalized = normalized.replace("%3c/ref%3e", "")
        normalized = normalized.replace("&lt;/ref&gt;", "")
        normalized = re.sub(r"&lt;ref\b[^&]*?&gt;", "", normalized, flags=re.IGNORECASE)
        normalized = normalized.replace("&nbsp;", " ")
        normalized = re.sub(r"\s+", " ", normalized).strip(" ,;:")
        if not normalized:
            return ""
        return f" [Source: {normalized}]"

    def rewrite_block(block: str) -> str:
        block = ESCAPED_WIKI_REF_SELF_CLOSING_RE.sub("", block)
        block = ESCAPED_WIKI_REF_WITH_ENCODED_CLOSE_RE.sub(
            lambda match: render_ref(match.group("content")),
            block,
        )
        block = ESCAPED_WIKI_REF_RE.sub(
            lambda match: render_ref(match.group("content")),
            block,
        )
        block = ESCAPED_WIKI_REF_UNCLOSED_RE.sub(
            lambda match: render_ref(match.group("content")),
            block,
        )
        block = ESCAPED_WIKI_REFERENCES_RE.sub("", block)
        return block

    parts = re.split(r"(\n{2,})", segment)
    return "".join(
        part if index % 2 else rewrite_block(part)
        for index, part in enumerate(parts)
    )


def normalize_markdown_table_residue(segment: str) -> str:
    trailing_newline = segment.endswith("\n")
    normalized_lines: list[str] = []
    for line in segment.splitlines():
        stripped = line.lstrip()
        if not stripped.startswith("|"):
            normalized_lines.append(line)
            continue
        cells = line.split("|")
        if len(cells) < 3:
            normalized_lines.append(line)
            continue
        filtered = [cells[0]]
        removed = False
        for cell in cells[1:-1]:
            if TABLE_ATTR_ONLY_CELL_RE.fullmatch(cell.strip()):
                removed = True
                continue
            filtered.append(cell)
        filtered.append(cells[-1])
        normalized_lines.append("|".join(filtered) if removed else line)
    normalized = "\n".join(normalized_lines)
    if trailing_newline:
        normalized += "\n"
    return normalized


def normalize_markdown_attribute_residue(segment: str) -> str:
    return MARKDOWN_ATTR_LINE_RE.sub("", segment)


def apply_outside_code_fences(text: str, transform) -> str:
    parts: list[str] = []
    last = 0
    for match in CODE_FENCE_RE.finditer(text):
        parts.append(transform(text[last : match.start()]))
        parts.append(match.group(0))
        last = match.end()
    parts.append(transform(text[last:]))
    return "".join(parts)


def sanitize_body(text: str, version: str, rel_source: Path) -> str:
    text = rewrite_images(text)
    text = MISATTACHED_CODE_FENCE_RE.sub("\n```", text)
    text = apply_outside_code_fences(
        text,
        lambda chunk: normalize_escaped_wiki_refs(
            normalize_escaped_inline_html(
                normalize_markdown_attribute_residue(
                    normalize_markdown_table_residue(
                        normalize_inline_html(
                            rewrite_html_hrefs(rewrite_markdown_links(chunk, version), version)
                        )
                    )
                )
            )
        ),
    )
    text = strip_image_artifacts(text)
    text = sanitize_absolute_paths(text)
    text = apply_agent_text_adaptations(text, rel_source)
    text = re.sub(r"\n{3,}", "\n\n", text)
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
    body = sanitize_body(body, bundle_version, rel_source)
    lines = [
        f"# {title}",
        "",
        f"Bundled adapted source page for GCAM `{bundle_version}`.",
        "",
        f"- Source root: `{source_root_label(source_version)}`",
        f"- Source path: `{rel_source.as_posix()}`",
        f"- Coverage mode: `{coverage_mode}`",
        "- Bundle mode: `text-only page bundle; images omitted`",
        f"- Version page index: `version_pages/{bundle_version}/{BUNDLE_INDEX_NAME}`",
    ]
    if rel_source.name == "user-guide.md":
        lines.append(
            "- Note: This adapted user-guide page rewrites interactive ModelInterface browsing into headless-agent guidance and omits screenshot-dependent UI steps."
        )
    if rel_source.name == "gcam-build.md":
        lines.append(
            "- Note: This adapted build page rewrites GUI IDE click paths into agent-readable configuration targets and prefers Makefile/headless builds when available."
        )
    if rel_source.name == "hector.md":
        lines.append(
            "- Note: This adapted Hector page rewrites IDE integration click paths into agent-readable dependency and build-setting summaries."
        )
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
        f"- Version page index: `version_pages/{version}/{BUNDLE_INDEX_NAME}`",
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
        f"- Version page index: `version_pages/{version}/{BUNDLE_INDEX_NAME}`",
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
        if path.name != BUNDLE_INDEX_NAME
    )
    write_file(version_root / BUNDLE_INDEX_NAME, render_full_tree_index(version, page_paths))


def build_delta_version(version: str) -> None:
    version_root = version_page_root(version)
    if version_root.exists():
        shutil.rmtree(version_root)
    write_file(version_root / "release_note.md", render_delta_release_note(version))
    write_file(version_root / "cmp_index.md", render_delta_cmp_index(version))
    write_file(version_root / BUNDLE_INDEX_NAME, render_delta_index(version))


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
        f"- Then open `version_pages/<version>/{BUNDLE_INDEX_NAME}` only when page-level detail is needed.",
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
