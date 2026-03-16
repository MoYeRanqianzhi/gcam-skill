#!/usr/bin/env python3
"""
Generate page-level bundled GCAM references for all versions.

This turns the authoring sources in `gcam-doc/` into self-contained,
versioned page bundles under `skills/gacm/reference/version_pages/`.
"""

from __future__ import annotations

import html
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
HTML_SPAN_RE = re.compile(
    r"<span\b(?P<attrs>[^>]*)>(?P<content>.*?)</span>",
    re.IGNORECASE | re.DOTALL,
)
HTML_ID_OR_NAME_ATTR_RE = re.compile(
    r"""\b(?:id|name)\s*=\s*(?:"(?P<double>[^"]+)"|'(?P<single>[^']+)')""",
    re.IGNORECASE,
)
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
HTML_COMMENT_RE = re.compile(r"<!--(?P<content>.*?)-->", re.DOTALL)
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
ESCAPED_HTML_COMMENT_RE = re.compile(r"&lt;!--(?P<content>.*?)--&gt;", re.IGNORECASE | re.DOTALL)
ESCAPED_MSO_EXPORT_BLOCK_RE = re.compile(
    r"&lt;!--\[if gte mso \d+\]&gt;&lt;xml&gt;.*?&lt;!--StartFragment--&gt;\s*",
    re.IGNORECASE | re.DOTALL,
)
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
PAREN_WRAPPED_CITATION_LINK_RE = re.compile(
    r"\[\((?P<label>[^][]*[A-Za-z][^][]*?\d{4}[^][]*)\)\]\((?P<target>[^)]+)\)"
)
BROKEN_ANCHOR_CITATION_LINK_RE = re.compile(
    r"\[(?P<label>[^][]*?\(\d{4})\]\((?P<target>#[^)]+)\)\)"
)
BROKEN_DOUBLE_BRACKET_LINK_RE = re.compile(
    r"\[\[(?P<label>[^\]]+)\]\((?P<target>[^)]+)\)\]"
)
BROKEN_DOUBLE_BRACKET_LABEL_LINK_RE = re.compile(
    r"\[\[(?P<label>[^\]]+)\]\]\((?P<target>[^)]+)\)"
)
HTML_HREF_RE = re.compile(r'(?P<prefix>href=")(?P<target>[^"]+)(?P<suffix>")', re.IGNORECASE)
MARKDOWN_ATTR_LINE_RE = re.compile(r"^[ \t]*\{:\s*[^}\n]+\}[ \t]*$", re.MULTILINE)
HEADING_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"(^```.*?^```[ \t]*\n?)", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"(`+)([^`\n]*?)\1")
MISATTACHED_CODE_FENCE_RE = re.compile(r"(?<![\r\n])```")
ZERO_WIDTH_CHAR_RE = re.compile(r"[\u200b\u200c\u200d\ufeff]")
UNICODE_DASH_RE = re.compile(r"[\u2010\u2013\u2014]")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
CROSS_VERSION_TOC_RE = re.compile(r"^v\d+\.\d+/")
IMAGE_PLACEHOLDER_RE = re.compile(r"\[\[IMAGE_OMITTED:([^\]]+)\]\]")
OMITTED_IMAGE_LINK_LABEL_RE = re.compile(r"\[omitted image:\s*(?P<label>.+?)\]", re.IGNORECASE)
OMITTED_IMAGE_RE = re.compile(r"\[omitted image:\s*(?P<label>[^\]]+)\]", re.IGNORECASE)
OMITTED_IMAGE_LINE_RE = re.compile(
    r"^\s*(?P<images>(?:\[omitted image:\s*[^\]]+\]\s*)+)(?P<rest>\S.*)?$",
    re.IGNORECASE,
)
LINKED_IMAGE_LABEL_PLACEHOLDER_RE = re.compile(
    r"\[\[(?:IMAGE_OMITTED:|omitted image:\s*)(?P<label>[^\]]+)\]\]\((?P<target>[^)]+)\)",
    re.IGNORECASE,
)
FIGURE_ARTIFACT_RE = re.compile(r"(?i)(?:<br\s*/?>|&lt;br&gt;|&nbsp;|\{:\s*\.fig\s*\})")
FIGURE_CAPTION_LINE_RE = re.compile(
    r"^\s*(?:#+\s*)?(?:\*\*|__)?Figure\s+\d+(?:[:.]|\b)",
    re.IGNORECASE,
)
FIGURE_LABEL_TOKEN = r"[A-Za-z]*\d[A-Za-z0-9.\-]*"
FIGURE_CAPTION_ONLY_RE = re.compile(
    rf"^\s*(?:#+\s*)?(?:\*\*|__)?Figure\s+(?P<number>{FIGURE_LABEL_TOKEN})(?:[:.]|\s+-)\s*(?P<caption>.*?)(?:\*\*|__)?\s*$",
    re.IGNORECASE,
)
FIGURE_SENTENCE_VERB_RE = re.compile(
    rf"\bFigure\s+{FIGURE_LABEL_TOKEN}\s+(?P<verb>illustrates|shows|provides|summarizes|depicts|compares|contrasts|maps|presents|describes)\b",
    re.IGNORECASE,
)
FROM_FIGURE_RE = re.compile(rf"\bFrom Figure\s+{FIGURE_LABEL_TOKEN}\b")
GIVEN_IN_FIGURE_RE = re.compile(rf"\bgiven in Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE)
WHAT_IS_IN_FIGURE_RE = re.compile(rf"\bwhat is in Figure\s+{FIGURE_LABEL_TOKEN}\b", re.IGNORECASE)
IN_FIGURE_AND_TABLE_RE = re.compile(
    rf"\bin Figure\s+{FIGURE_LABEL_TOKEN}\s+and\s+(?P<table>Table\s+\d+)\b",
    re.IGNORECASE,
)
THIS_FIGURE_RE = re.compile(r"\bthis figure\b", re.IGNORECASE)
OMITTED_FIGURE_NUMBER_RE = re.compile(
    rf"\b(?P<prefix>(?:[Tt]he|[Aa]n?)\s+omitted)\s+Figure\s+{FIGURE_LABEL_TOKEN}\b"
)
FIGURE_SOURCE_RE = re.compile(r"Figure source:", re.IGNORECASE)
FIG_PANEL_REF_RE = re.compile(r"\bFig\.\s*\d+(?P<panel>[A-Za-z])\b")
DISPLAYED_IN_FIGURE_INLINE_RE = re.compile(
    rf",\s*displayed in Figure\s+{FIGURE_LABEL_TOKEN},\s*",
    re.IGNORECASE,
)
SHOWN_SCHEMATICALLY_IN_FIGURE_INLINE_RE = re.compile(
    rf",\s*shown schematically in Figure\s+{FIGURE_LABEL_TOKEN}\s+and\s+detailed in\s+",
    re.IGNORECASE,
)
INLINE_TRAILING_FIGURE_SENTENCE_RE = re.compile(
    rf",\s*Figure\s+{FIGURE_LABEL_TOKEN}\.(?=\s+[A-Z])",
    re.IGNORECASE,
)
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
DATA_SYSTEM_IEA_BROWSER_RE = re.compile(
    r"Users who have access the the \[IEA energy balances\]\((?P<link>[^)]+)\) will need to export the data from "
    r"the Beyond 2020 browser\.\s+The GCAM data system is configured for the 2012 edition of the IEA energy "
    r"balances, which goes through 2010 for all countries and sectors, and provides 2011 estimates for a small "
    r"selection of variables\. While more recent versions with more recent years will ostensibly work with the "
    r"existing R code, any changes to the names or available categories of any variables \(COUNTRY, PRODUCT, "
    r"FLOW\) in the source data will require updates to the mappings and/or code\. To export the data in the "
    r"format used by the data system, users should open the `Beyond 2020 Browser`, and toggle the variables so "
    r"that the years are columns, and the following ID variables are all displayed, with no variables held "
    r"fixed:\s*$",
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
DEV_GUIDE_TEST_FRAMEWORK_INTRO_RE = re.compile(
    r"^Most users will interact with the testing framework only through the pull request interface and will not "
    r"need to worry about updating the testing framework\.\s+Some instances of when they would need to update "
    r"include:\s*$",
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_OPEN_PR_RE = re.compile(
    r"^At this point you can open your pull request and the automated tests will use your updated testing "
    r"framework automatically\.\s+In addition no other pull requests will yet be affected!\s+At this point you "
    r"should also open a pull request in the \[gcam-testing-framework repository\]\((?P<repo>[^)]+)\) and link "
    r"to it from your GCAM pull request so all changes can be considered together\.\s*$",
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_PR_NOTIFIER_RE = re.compile(
    r"^This is a plugin to Bitbucket which allows us to signal Jenkins when to kick off tests\.\s+This plug can "
    r"trigger on any Bitbucket action, such as pull request opened or updated\.\s+It makes available a number "
    r"of useful meta data about what happened and will send it off to some arbitrary URL\.\s+In addition it "
    r"allows us to add a new menu option with in the pull request and even configure arbitrary forms to collect "
    r"user input to send along too\.\s+The full documentation of what is possible is on it'?s Github page:\s*"
    r"(?P<url>https://github\.com/tomasbjerre/pull-request-notifier-for-bitbucket)\s*$",
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_NOTIFY_STATUS_RE = re.compile(
    r"^A plugin to update the build status \(In Progress, Failure, Success\) in Bitbucket\.\s+The Jenkins "
    r"plugin takes care of all of the details for us automatically filling in the name of the test, build "
    r"number, and link back to Jenkins so a user can watch the progress / look at logs or build artifacts after "
    r"the fact\.\s*$",
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_BUTTON_RE = re.compile(
    r'^When the "button" is clicked and a user confirms,\s+It will notify Jenkins with the '
    r'"JGCRI-gcam-pic" tag with the meta data:\s*$',
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_LAUNCH_BUTTON_RE = re.compile(
    r'^We have configured a Pull Request Notifier "Button" labeled "Launch Validation Runs" and contains the check box form options:\s*$',
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_BUTTON_FORM_RE = re.compile(
    r"^This defaults to the set of scenario we currently require users to run: Ref, Ref \+ 2\.6; SSPs,\s+SSPs \+ SPA 2\.6\.  "
    r"However all of the SPA climate target levels in the committed `batch_SSP_SPA\*\.xml` are available\.  "
    r"Note this button form was generated manually but the actual scenarios available are generated from the batch files committed in the gcam-core repo\.\s*$",
    re.MULTILINE,
)
DEV_GUIDE_TEST_FRAMEWORK_HISTORICAL_BUTTON_RE = re.compile(
    r'^Historical UI note: the internal "Launch Validation Runs" button invoked Jenkins with the "JGCRI-gcam-pic" tag and the following metadata payload:\s*$',
    re.MULTILINE,
)
DEV_GUIDE_GETTING_STARTED_PR_STEP_RE = re.compile(
    r"^6\.\s+When your development is complete, open a pull request\.\s*$",
    re.MULTILINE,
)
DEV_GUIDE_ANALYSIS_GUI_RE = re.compile(
    r"software developers wanting to write new tools like graphical user interfaces for working with GCAM",
    re.IGNORECASE,
)
SEE_FIGURE_BELOW_PAREN_RE = re.compile(r"\s*\(see Figure below\)")
AGLU_LAND_OUTPUTS_FIGURE_RE = re.compile(
    r"Outputs include land use and land cover for each of the land types included in GCAM \(see Figure 1\)\."
)
AGLU_FERTILIZER_OUTPUTS_FIGURE_RE = re.compile(
    r"Outputs include fertilizer use for each crop and management practice included in GCAM \(see Figure 1\)\."
)
LAND_NESTING_DIAGRAM_RE = re.compile(
    r"Figure 1 shows the nesting diagram of land with (?:an AEZ|a) subregion\."
)
LAND_SIMPLIFIED_NESTING_RE = re.compile(
    r"Figure 1 shows a simplified nesting diagram of land with a subregion\. Note that crops are further divided beyond what is in Figure 1, nesting irrigated/rainfed and hi/lo fertilizer\."
)
HISTORICAL_AGLU_SIMPLIFIED_STRUCTURE_RE = re.compile(
    r"A\s+representative, simplified n?nesting structure is depicted in Figure 1\."
)
OVERVIEW_RESOLUTION_FIGURE_RE = re.compile(
    r"it is constructed with different levels of resolution for each of these different systems \(see Figure 2\)\."
)
OVERVIEW_HUMAN_EARTH_SYSTEMS_FIGURE_RE = re.compile(
    rf"IA models include both human and physical Earth systems,\s*Figure\s+{FIGURE_LABEL_TOKEN}\."
)
OVERVIEW_FIVE_SYSTEMS_FIGURE_RE = re.compile(
    rf"The interactions between these different systems all take place within the GCAM core; that is, they are not modeled as independent modules, but as one integrated whole,\s*Figure\s+{FIGURE_LABEL_TOKEN}\."
)
ENERGY_SYSTEM_SCHEMATIC_RE = re.compile(
    r"^In the schematic of the energy system depicted below, the energy transformation and distribution sectors include all sectors except for the resources \(colored red\) and the final demands \(colored light blue\)\.\s*$",
    re.MULTILINE,
)
ELECTRIC_NESTING_FIGURE_RE = re.compile(
    r"The nesting structure of the electric sector is shown in the figure below, with a focus on one repesentative technology\."
)
ELECTRIC_THIRD_NEST_FIGURE_RE = re.compile(
    r", in a third nest, as shown in the figure above\. That is, within any thermo-electric generation technology, there is modeled competition between up to five different cooling system types;",
    re.MULTILINE,
)
REFINING_STRUCTURE_FIGURE_RE = re.compile(
    r"The structure of refining in the broader energy system is shown in (?:the following figure|Figure \d+), with example input-output coefficients\."
)
OIL_REFINING_GRAPHIC_RE = re.compile(
    r"In a typical region, the oil refining technology consumes three energy inputs: crude oil, natural gas, and electricity\. This is depicted (?:graphically below|in Figure \d+), with typical input-output coefficients shown\."
)
OIL_REFINING_COMPETITION_FIGURE_RE = re.compile(
    r"as indicated in (?:the figure above|Figure \d+), this technology does not differentiate between conventional and unconventional oil, whose competition is explicitly modeled upstream of the refining sector\."
)
FOSSIL_RESOURCE_CURVES_RE = re.compile(r"Resource curves for fossil fuels are shown below\.")
GAS_STRUCTURE_FIGURE_RE = re.compile(
    r"^The structure of the natural gas supply and distribution in GCAM is shown (?:below|in Figure \d+):\s*$",
    re.MULTILINE,
)
UPSTREAM_GAS_NETWORK_FIGURE_RE = re.compile(r"network shown in (?:the figure above|Figure \d+)", re.MULTILINE)
DISTRICT_HEAT_OPTIONS_RE = re.compile(
    r"(?:However, in several regions|In regions) where purchased heat accounts for a large share of the final energy use, GCAM does include a representation of district heat production, with four competing technology options, shown (?:below|in Figure \d+)\."
)
DISTRICT_HEAT_AS_SHOWN_RE = re.compile(
    r'As shown(?: in Figure \d+)?, all energy losses and cost mark-ups incurred in transforming primary energy into delivered district heat are accounted in the "district heat" technologies; there are no explicit cost adders and efficiency losses for heat distribution, or different prices for the heat consumed by buildings and industry sectors\.'
)
DISTRICT_HEAT_GRAPHIC_RE = re.compile(
    r"This is illustrated further in (?:the graphic below|Figure \d+)\."
)
HYDROGEN_TRANSPORT_STRUCTURE_RE = re.compile(
    r"^Structure of hydrogen transmission, distribution and end use, with illustrative input-output coefficients \(GJ of energy input per GJ of hydrogen\) showing the approximate energy requirements of each stage of hydrogen compression, refrigeration, transportation, and storage, is shown in the figure below\.?\s*$",
    re.MULTILINE,
)
HYDROGEN_H2A_STRUCTURE_RE = re.compile(
    r"The structure of the hydrogen production and distribution sectors and technologies in GCAM generally uses the structure of the U\.S\. Department of Energy's Hydrogen Analysis \(H2A\) models (?P<cite>\[[^\]]+\]\([^)]+\)), and is shown in (?:the figure below|Figure \d+)\."
)
HYDROGEN_PRIMARY_SOURCES_RE = re.compile(
    r"; as shown in (?:the figure above|Figure \d+), hydrogen can be produced from up to 7 primary energy sources\.",
    re.MULTILINE,
)
FOSSIL_FUEL_TRADE_FIGURE_RE = re.compile(
    r"^\s*The figure below depicts the fossil fuel trade structures \(using coal as an example\)\.\s*",
    re.MULTILINE,
)
FLOORSPACE_XML_FIGURE_RE = re.compile(
    r"^\s*The figure below is an example XML of user-specified residential floorspace values for Maine\.\s*$",
    re.MULTILINE,
)
CEMENT_SCHEMATIC_RE = re.compile(
    r'A simple schematic with example input-outout coefficients is shown below; note that in the structure, "process heat cement" is treated as a specific energy commodity, so as to avoid allowing electricity to compete for market share of this input to the cement production process\.',
    re.MULTILINE,
)
AMMONIA_N_FERTILIZER_SCHEMATIC_RE = re.compile(
    r"^Fuel and feedstock sources and input-output coefficients are calibrated based on Table 4\.15 of \[IEA 2007\]\((?P<target>[^)]+)\)\. The schematic below shows how ammonia and N fertilizer commodities are situated between the energy and agricultural systems of GCAM\.\s*$",
    re.MULTILINE,
)
N_FERTILIZER_SCHEMATIC_RE = re.compile(
    r"^Fuel and feedstock sources and input-output coefficients are calibrated based on Table 4\.15 of \[IEA 2007\]\((?P<target>[^)]+)\)\. The schematic below shows how N fertilizer is situated between the energy and agricultural systems of GCAM\.\s*$",
    re.MULTILINE,
)
PASSENGER_TYPICAL_REGION_RE = re.compile(
    rf"^The structure of the passenger sector differs by region, but a typical region is depicted(?: below| in Figure\s+{FIGURE_LABEL_TOKEN}| Figure\s+{FIGURE_LABEL_TOKEN})\.\s*$",
    re.MULTILINE,
)
PASSENGER_AS_SHOWN_RE = re.compile(
    r"^As shown, the passenger sector consists of up to five nesting levels,",
    re.MULTILINE,
)
LAND_GROWTH_FIGURE_RE = re.compile(
    r"^When land is converted to forests, the vegetation carbon content of that new forest land gradually approaches an exogenously-specified, region- and land-type-dependent value\. The rate at which this value is reached depends on the mature age of forests\. Mature age is specified by region, GLU, and land type\. In the figure below, the rate of growth as a function of time since planting is shown for four different mature ages\. In this figure, the y-axis indicates the percentage of the exogenously-specified, region- and land-type-dependent value accumulated\.\s*$",
    re.MULTILINE,
)
HISTORICAL_FOREST_REGROWTH_FIGURE_RE = re.compile(
    r"When land is converted to forests, the vegetation carbon content of that new forest land exponentially approaches an exogenously-specified, region-dependent value in order to represent the finite time required for forests to grow, as shown in the figure below\."
)
DETAILS_LAND_CROP_SUBDIVISION_FIGURE_RE = re.compile(
    r"Crop areas are further subdivided into irrigated/rainfed and high/low management categories \(see Figure 2 for more details\)\. This specification allows for adjusting the level of substitution across categories by varying the logit parameters\. Figure 2 also indicates the corresponding files in the `gcamdata` system that process the inputs for each land type\."
)
DETAILS_LAND_FILE_MAP_FIGURE_RE = re.compile(
    r"The figure also indicates which file in the `gcamdata` system processes the inputs for each type of land"
)
DACCS_ATTRACTIVENESS_FIGURE_RE = re.compile(
    r"The existing assumptions for energy and geologic carbon storage supply in each state and grid region further determine the relative attractiveness to deploy DACCS in a given state within GCAM \(see figure below\)\."
)
LNG_TRADE_NETWORK_FIGURES_RE = re.compile(
    r"\s*Natural gas has been further disaggregated into traded pipeline gas and traded liquefied natural gas \(LNG\)\. LNG is traded at the global market level, while pipeline gas is traded in 6 regional markets: North America, Latin America, Europe, Russia\+, Africa and Middle East, and Asia-Pacific \(see figures\)\."
)
DETAILS_EMISSIONS_COMPARISON_FIGURES_RE = re.compile(
    r"Figures 1 and 2 compare historical emissions from CEDS with the emissions from GCAM after initialization \. Figure 1 compares global emissions by species and Figure 2 presents a scatter plot comparing emissions by species and year for each region\.  As seen in the figures, emissions translate mostly correctly for all species of gases\."
)
ECONOMY_MACRO_FIGURE_RE = re.compile(
    r"Figure 1 shows the new elements in relation to existing GCAM elements\."
)
INPUTS_SUPPLY_FAO_MAPPING_FIGURES_RE = re.compile(
    r"The commodity mapping is provided in \[(?P<label>Mapping_SUA_PrimaryEquivalent\.csv)\]\((?P<target>[^)]+)\) and shown in Figures 1 \(crop harvested area\) and 2 \(food\)\."
)
TRADE_MARKET_STRUCTURE_FIGURE_RE = re.compile(
    r'The structural implementations of a "global-market" versus a "regional-market" representation are shown in Figure \d+(?: with an example of corn trade)?\.'
)
TRADE_MARKET_COMPARISON_FIGURE_RE = re.compile(
    r"Furthermore, the two market structures are also compared in Figure \d+ with an example of a global wheat market equilibrium with demand and supply flows in 2010\."
)
V32_TRANSPORTATION_STRUCTURE_RE = re.compile(
    r"GCAM contains a detailed representation of transportation energy use and service demands, with the sector divided into three service demands: passenger, freight, and international shipping \(see Figure 1\)\."
)
V32_TOC_END_USE_SECTORS_FIGURE_RE = re.compile(
    rf"end-use sectors: buildings, industry and transport,\s*Figure\s+{FIGURE_LABEL_TOKEN}\."
)
V32_INDUSTRY_AGGREGATE_FIGURE_RE = re.compile(
    r"In all non-US regions, the industrial sector is represented as a consumer of generic energy services and feedstocks, as shown in Figure 1\."
)
V32_INDUSTRY_US_FIGURES_RE = re.compile(
    r"Each manufacturing industry group consumes energy to produce a range of intermediate industrial services, such as steam and machine drive \(see Figure 2\)\."
)
V32_INDUSTRY_US_ENERGY_REQUIREMENTS_RE = re.compile(
    r"Figure 3 shows the eleven GCAM industries and their energy requirements, by service, in 2005\."
)
V32_SOCIOECONOMIC_FIGURES_RE = re.compile(
    r"Population and GDP in the current baseline scenario are shown in Figures 2 and 3\."
)
V32_DEPLETABLE_RESOURCE_FIGURES_RE = re.compile(
    r"Resource supply curves for natural gas, crude oil, unconventional oil, and coal are shown for each of the 14 GCAM regions in Figures 1-4 below\."
)
V32_UNCONVENTIONAL_OIL_SHOWN_BELOW_RE = re.compile(
    r"note that for unconventional oil, the supply curves shown below do not include the cost of the energy used in extraction, and as such the actual supply curves in each region will have higher costs at all quantities\."
)
V32_GLOBAL_RESOURCE_DOTTED_LINES_RE = re.compile(
    r"These global resource supply curves, derived by adding up each region's available resource at each price point, are shown in the figures as dotted lines\."
)
V32_WIND_REGION_ORDER_FIGURE_RE = re.compile(
    r"Supply curves by GCAM region are shown in Figure 5; the region order from greatest to least is as follows:"
)
V32_ROOFTOP_PV_FIGURE_RE = re.compile(
    r"Rooftop PV supply curves are shown in Figure 6; note that as with wind, this supply curve only accounts for the portion of the costs that increase with deployment\."
)
V32_GEOTHERMAL_SUPPLY_FIGURE_RE = re.compile(
    r"Supply curves for the hydrothermal and EGS resources in all regions are shown in Figure 7\."
)
V32_WASTE_BIOMASS_FIGURE_RE = re.compile(
    r"Figure 8 shows the supply curves used in each region; supplies are generally based on the amount and composition of municipal waste produced in each GCAM region\."
)
V32_ELECTRICITY_WIND_PV_FIGURES_RE = re.compile(
    r"For wind power, the supply curve for the U\.S\. region is based on NREL \(2008\), and is shown in Figure 2\. The supply curve shown also includes technology non-energy costs, but not ancillary costs\. The same supply curve is assumed for non-U\.S\. regions, but with maximum resource amounts scaled to estimates from GIS-based analysis, also informed by IEAGHG \(2000\)\. Assumed maximum resources for all GCAM regions are shown in Table 7\. The supply curve for rooftop PV in the U\.S\. is from NREL \(P\. Denholm and R\. Margolis, pers\. comm\.\), and is also shown in Figure 3\. The assumed limit in non-U\.S\. regions, shown in Table 7, is based on a GIS analysis of solar irradiance by region\."
)
V32_ELECTRICITY_GEOTHERMAL_FIGURE_RE = re.compile(
    r"Geothermal costs in GCAM are input as exogenous supply curves\. Supply curves assumed for hydrothermal and EGS resources for the U\.S\. are based on Petty and Porro \(2007\) and are shown in Figure 3\."
)
V32_REFINING_FIGURE_RE = re.compile(
    r"These different technology options for refining are shown in Figure 1; the non-energy costs and input/output coefficients are shown in Table 1\."
)
V32_UNCONVENTIONAL_REFINING_FIGURE_RE = re.compile(
    r"note the electricity and gas inputs to the “unconventional oil production” sector in Figure 1 and Table 1"
)
V32_ECONOMIC_LAND_COMPETITION_FIGURE_RE = re.compile(
    r"Figure 1 below shows a competition between two options with distributions of profits\. In this example, option 2 will get a higher share than 1 due to its higher potential average profit\. Sharing will be done between option 1 and option 2 in order to allocate all land to one of the two options so that the marginal profit rates of option 1 and option 2 are equal to each other\. At this point, there are no potential gains from changing the shares\. Also from Figure 1, this point at which marginal profits are equal must also be equal to the marginal value or price of land\. Only those instances of option 1 and option 2 which have profit rates higher than or equal to the land price at the margin will be implemented\."
)
V32_ECONOMIC_LAND_SHARE_EQUATION_RE = re.compile(
    r"The logit sharing equation for land uses across an assumed level of competition, whether leaves in a node or among nodes in a nest, is shown here\.\s+\[omitted image:[^\]]+\]",
    re.IGNORECASE,
)
V32_ECONOMIC_LAND_PROFIT_SYMBOL_RE = re.compile(
    r"where\s+\[omitted image:[^\]]+\]\s+is the profit rate of option i and p is the logit exponent\.",
    re.IGNORECASE,
)
V32_ECONOMIC_LAND_AVG_PROFIT_EQUATION_RE = re.compile(
    r"The average profit rate for a node resulting from the share competition in each nest is given by\s+\[omitted image:[^\]]+\]",
    re.IGNORECASE,
)
POLICIES_FIGURE_EXAMPLE_RE = re.compile(
    r"For example in the figure below, the cost of moving from a reference path without a carbon tax \(blue\) to the emissions path with a carbon tax \(green\) in period T can be calculated simply\.",
    re.MULTILINE,
)
POLICIES_TAX_REVENUE_RE = re.compile(
    r"The tax revenue can be calculated as the tax rate times the remaining emissions, shown in red below\.",
    re.MULTILINE,
)
USER_GUIDE_OPEN_DB_WAIT_BUTTON_RE = re.compile(
    r"a user has pressed any button it will attempt to open the DB once more and if that\s+fails again then the results will be lost\.",
    re.IGNORECASE,
)
GCAM_REV_HISTORY_CLICK_RE = re.compile(
    r"Should the note on the page your are viewing indicate that it was revised for a version of GCAM later than what you are interested in click on the [“\"]history[”\"] tab at the top of that page:",
    re.IGNORECASE,
)
DEV_GUIDE_GIT_INTERNAL_SERVER_RE = re.compile(
    r"PNNL staff should use the internal server\.\s+Your project lead will be\s+able to get you write access "
    r"to the repository, and after that you can\s+push your branch \(q\.v\. \[creating branches\]\(#Creating-"
    r"branches\)\) to the\s+server and open a pull request\s+\(q\.v\. \[opening pull requests\]\(#Opening-pull-"
    r"requests\)\)\.\s*",
    re.DOTALL,
)
DEV_GUIDE_GIT_OUTSIDE_USERS_RE = re.compile(
    r"Outside users should use the GitHub repository\.\s+You will have read\s+access to this repository, but "
    r"you won't be able to write to it\.\s+Instead, if you want to do development, use the\s+\[fork\]\([^)]+\)"
    r"\s+button on GitHub to create your own copy of the repository\.\s+You will\s+be able to create branches "
    r"in your copy, and you will be able to open\s+pull requests from your copy back to the main repository\.\s*",
    re.DOTALL,
)
DEV_GUIDE_GIT_OPEN_PR_RE = re.compile(
    r"Once you've made some progress on your development, you will want to\s+open a\s+\[pull request\]\([^)]+\)"
    r"\.\s+Notionally, a pull request is a proposal to merge changes from your\s+branch into another branch "
    r"\(usually the `master` branch\)\.\s+However,\s+opening a pull request also provides other developers with "
    r"an\s+opportunity to review your code and give feedback, so you don't have\s+to wait until your code is "
    r"ready to go before you open one\.\s+Open a\s+pull request as soon you have some progress to share\.\s+On "
    r"GitHub, pull\s+requests can be marked as drafts, indicating that they are not yet\s+ready to merge\.\s+"
    r"Bitbucket doesn't have an equivalent feature, so if a\s+pull request is not ready to merge, it's a good "
    r"idea to add the tag\s+WIP \(\"work in progress\"\) to the description when you create it\.\s+Otherwise "
    r"the process is similar between the two platforms\.\s*",
    re.DOTALL,
)
DEV_GUIDE_GIT_PR_FOLLOWUP_RE = re.compile(
    r"Once you have opened the pull request, you will probably get some\s+feedback from other developers\.\s+"
    r"Push additional commits to your\s+branch addressing the feedback or continuing the development, and they\s+"
    r"will automatically be added to the pull request\.\s+Eventually, when\s+your development is complete, you "
    r"should mark your pull request as\s+ready to merge\.\s+Before the branch can be merged, you will have to\s+"
    r"write a change proposal \(q\.v\. \[GCAM Review Process\]\(review\.md\)\)\.\s*",
    re.DOTALL,
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


def normalize_heading_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = ZERO_WIDTH_CHAR_RE.sub("", text)
    text = text.replace("\u2009", " ")
    text = text.replace("\u2061", "")
    text = text.translate(
        str.maketrans(
            {
                "\u201c": '"',
                "\u201d": '"',
                "\u2018": "'",
                "\u2019": "'",
                "\u00d7": "x",
                "\u02da": "\u00b0",
            }
        )
    )
    text = re.sub(r"(?<=\d)\s*[\u2010\u2013\u2014]\s*(?=\d)", "-", text)
    text = re.sub(r"(?<=\w)[\u2010\u2013\u2014](?=\w)", "-", text)
    text = UNICODE_DASH_RE.sub(" - ", text)
    text = re.sub(r"\s+-\s+", " - ", text)
    return text.strip()


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
        if normalize_heading_text(candidate) == normalize_heading_text(title):
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


def normalize_omitted_image_label(label: str) -> str:
    raw = label.strip()
    quoted_parts = [part.strip() for part in raw.split('"') if part.strip()]
    if len(quoted_parts) >= 2:
        raw = quoted_parts[-1]
    else:
        raw = quoted_parts[0] if quoted_parts else raw
    raw = raw.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    raw = re.sub(r"\.(?:png|gif|jpe?g|svg|webp)\b", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", raw)
    cleaned = normalize_image_label(raw.replace("_", " ").replace("-", " "))
    return cleaned or "figure"


def parse_omitted_image_labels(images: str) -> list[str]:
    labels: list[str] = []
    for match in OMITTED_IMAGE_RE.finditer(images):
        labels.append(normalize_omitted_image_label(match.group("label")))
    return labels


def format_omitted_image_labels(labels: list[str]) -> str:
    if not labels:
        return "omitted figure"
    if len(labels) == 1:
        return labels[0].rstrip(".")
    return "; ".join(label.rstrip(".") for label in labels)


def is_descriptive_omitted_image_label(label: str) -> bool:
    return len(label) >= 30 or any(char in label for char in ".,:;()")


def normalize_omitted_image_lines(text: str) -> str:
    source_lines = text.splitlines()
    lines: list[str] = []
    for index, raw_line in enumerate(source_lines):
        match = OMITTED_IMAGE_LINE_RE.match(raw_line)
        if not match:
            lines.append(raw_line)
            continue
        labels = parse_omitted_image_labels(match.group("images"))
        rest = (match.group("rest") or "").strip()
        next_nonempty = ""
        for future in source_lines[index + 1 :]:
            if future.strip():
                next_nonempty = future.strip()
                break
        if rest:
            if any(is_descriptive_omitted_image_label(label) for label in labels):
                lines.append(f"Omitted figure summary: {format_omitted_image_labels(labels)}.")
            lines.append(rest)
            continue
        if any(is_descriptive_omitted_image_label(label) for label in labels) and not FIGURE_CAPTION_LINE_RE.match(
            next_nonempty
        ):
            lines.append(f"Omitted figure summary: {format_omitted_image_labels(labels)}.")
    return "\n".join(lines)


def is_figure_caption_continuation(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(("```", "#", "- ", "* ", "| ")):
        return False
    if re.match(r"^\d+\.\s", stripped):
        return False
    if FIGURE_CAPTION_ONLY_RE.match(stripped):
        return False
    return True


def normalize_figure_text_residue(text: str) -> str:
    lines = text.splitlines()
    normalized_lines: list[str] = []
    index = 0
    while index < len(lines):
        match = FIGURE_CAPTION_ONLY_RE.match(lines[index])
        if not match:
            normalized_lines.append(lines[index])
            index += 1
            continue

        caption_parts: list[str] = []
        if match.group("caption"):
            caption_parts.append(match.group("caption").strip())
        index += 1
        while index < len(lines) and is_figure_caption_continuation(lines[index]):
            caption_parts.append(lines[index].strip())
            index += 1

        caption = re.sub(r"\s+", " ", " ".join(caption_parts)).strip()
        if caption:
            normalized_lines.append(f"Omitted figure summary: {caption}")
        else:
            normalized_lines.append("Omitted figure summary.")

    text = "\n".join(normalized_lines)
    text = OMITTED_FIGURE_NUMBER_RE.sub(lambda match: f"{match.group('prefix')} figure", text)
    text = FIGURE_SENTENCE_VERB_RE.sub(
        lambda match: f"The omitted figure {match.group('verb').lower()}",
        text,
    )
    text = FROM_FIGURE_RE.sub("From the omitted figure", text)
    text = GIVEN_IN_FIGURE_RE.sub("given in the omitted figure", text)
    text = WHAT_IS_IN_FIGURE_RE.sub("what is shown in the omitted figure", text)
    text = IN_FIGURE_AND_TABLE_RE.sub(
        lambda match: f"in the omitted figure and {match.group('table')}",
        text,
    )
    text = DISPLAYED_IN_FIGURE_INLINE_RE.sub(" ", text)
    text = SHOWN_SCHEMATICALLY_IN_FIGURE_INLINE_RE.sub(
        ", summarized in the omitted figure and detailed in ",
        text,
    )
    text = INLINE_TRAILING_FIGURE_SENTENCE_RE.sub(
        ". The omitted figure summarized the referenced structure.",
        text,
    )
    text = THIS_FIGURE_RE.sub("the omitted figure", text)
    text = FIGURE_SOURCE_RE.sub("Source:", text)
    text = FIG_PANEL_REF_RE.sub(
        lambda match: f"panel {match.group('panel').lower()}",
        text,
    )
    text = text.replace(
        "simply a convenience for the omitted figure",
        "simply a convenience in the omitted figure summary",
    )
    text = text.replace(
        "beyond what is shown in the omitted figure",
        "beyond what is summarized in the omitted figure",
    )
    text = text.replace(
        "shown in the omitted figure",
        "summarized in the omitted figure",
    )
    return text


def sanitize_absolute_paths(text: str) -> str:
    text = WINDOWS_JAVA_INCLUDE_RE.sub(r"<JAVA_HOME>\\include", text)
    text = WINDOWS_JAVA_LIB_RE.sub(r"<JAVA_HOME>\\lib", text)
    text = WINDOWS_JAVA_HOME_RE.sub("<JAVA_HOME>", text)
    text = POSIX_USER_HOME_RE.sub("<USER_HOME>", text)
    return text


def normalize_problem_unicode_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = ZERO_WIDTH_CHAR_RE.sub("", text)
    text = text.replace("\u2009", " ")
    text = text.replace("\u2061", "")
    return text


def normalize_problem_unicode_punctuation(text: str) -> str:
    text = text.translate(
        str.maketrans(
            {
                "\u201c": '"',
                "\u201d": '"',
                "\u2018": "'",
                "\u2019": "'",
                "\u00d7": "x",
                "\u02da": "\u00b0",
            }
        )
    )
    text = re.sub(r"(?<=\d)\s*[\u2010\u2013\u2014]\s*(?=\d)", "-", text)
    text = re.sub(r"(?<=\w)[\u2010\u2013\u2014](?=\w)", "-", text)
    text = UNICODE_DASH_RE.sub(" - ", text)
    text = re.sub(r"\s+-\s+", " - ", text)
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

    replace(SEE_FIGURE_BELOW_PAREN_RE, "")
    replace(
        AGLU_LAND_OUTPUTS_FIGURE_RE,
        "Outputs include land use and land cover for each of the land types included in GCAM. The omitted figure summarized the relevant land-type hierarchy.",
    )
    replace(
        AGLU_FERTILIZER_OUTPUTS_FIGURE_RE,
        "Outputs include fertilizer use for each crop and management practice included in GCAM. The omitted figure summarized the crop and management hierarchy used for these outputs.",
    )
    replace(
        LAND_NESTING_DIAGRAM_RE,
        "The omitted figure summarized the land nesting diagram within a subregion.",
    )
    replace(
        LAND_SIMPLIFIED_NESTING_RE,
        "The omitted figure summarized a simplified land nesting diagram for a subregion. Crops are further divided beyond that simplified sketch, including irrigated/rainfed and hi/lo fertilizer branches.",
    )
    replace(
        HISTORICAL_AGLU_SIMPLIFIED_STRUCTURE_RE,
        "The omitted figure summarized one representative simplified land-nesting structure.",
    )
    replace(
        OVERVIEW_RESOLUTION_FIGURE_RE,
        "it is constructed with different levels of resolution for each of these different systems.",
    )
    replace(
        OVERVIEW_HUMAN_EARTH_SYSTEMS_FIGURE_RE,
        "IA models include both human and physical Earth systems. The omitted figure summarized one illustrative mapping of those human and Earth systems.",
    )
    replace(
        OVERVIEW_FIVE_SYSTEMS_FIGURE_RE,
        "The interactions between these different systems all take place within the GCAM core; that is, they are not modeled as independent modules, but as one integrated whole. The omitted figure summarized those five interacting systems.",
    )
    replace(
        ENERGY_SYSTEM_SCHEMATIC_RE,
        "In GCAM's energy-system structure, the energy transformation and distribution sectors include all sectors except the resources and the final demands.\n",
    )
    replace(
        ELECTRIC_NESTING_FIGURE_RE,
        "The electric sector uses a nested structure, described here with one representative technology as the reference pattern.\n",
    )
    replace(
        ELECTRIC_THIRD_NEST_FIGURE_RE,
        " in a third nest. Within any thermo-electric generation technology, there is modeled competition between up to five different cooling system types;",
    )
    replace(
        REFINING_STRUCTURE_FIGURE_RE,
        "The structure of refining in the broader energy system is summarized here with example input-output coefficients.\n",
    )
    replace(
        OIL_REFINING_COMPETITION_FIGURE_RE,
        "this technology does not differentiate between conventional and unconventional oil; that competition is explicitly modeled upstream of the refining sector.",
    )
    replace(
        OIL_REFINING_GRAPHIC_RE,
        "In a typical region, the oil refining technology consumes three energy inputs: crude oil, natural gas, and electricity. The omitted schematic and caption summarize typical input-output coefficients.\n",
    )
    replace(
        FOSSIL_RESOURCE_CURVES_RE,
        "The omitted figures provided representative fossil-fuel resource-curve examples.",
    )
    replace(
        GAS_STRUCTURE_FIGURE_RE,
        "The natural gas supply and distribution structure in GCAM is summarized below:\n",
    )
    replace(UPSTREAM_GAS_NETWORK_FIGURE_RE, "network described above")
    replace(
        DISTRICT_HEAT_OPTIONS_RE,
        "In regions where purchased heat accounts for a large share of final energy use, GCAM includes a representation of district heat production with four competing technology options.",
    )
    replace(
        DISTRICT_HEAT_AS_SHOWN_RE,
        'In this representation, all energy losses and cost mark-ups incurred in transforming primary energy into delivered district heat are accounted in the "district heat" technologies; there are no explicit cost adders and efficiency losses for heat distribution, or different prices for the heat consumed by buildings and industry sectors.\n',
    )
    replace(
        DISTRICT_HEAT_GRAPHIC_RE,
        "The omitted pulp-and-paper example caption below provides additional context for this accounting boundary.\n",
    )
    replace(
        HYDROGEN_TRANSPORT_STRUCTURE_RE,
        "The hydrogen transmission, distribution, and end-use structure is summarized here with illustrative input-output coefficients (GJ of energy input per GJ of hydrogen) for the approximate energy requirements of compression, refrigeration, transportation, and storage.\n",
    )
    replace(
        HYDROGEN_H2A_STRUCTURE_RE,
        lambda match: (
            "The structure of the hydrogen production and distribution sectors and technologies in GCAM generally follows the U.S. Department of Energy's Hydrogen Analysis (H2A) models "
            f"{match.group('cite')}.\n"
        ),
    )
    replace(HYDROGEN_PRIMARY_SOURCES_RE, "; in this structure, hydrogen can be produced from up to 7 primary energy sources.")
    replace(
        FOSSIL_FUEL_TRADE_FIGURE_RE,
        "The fossil fuel trade structures in GCAM, using coal as an example, are summarized as follows. ",
    )
    replace(
        FLOORSPACE_XML_FIGURE_RE,
        "The following XML is an example of user-specified residential floorspace values for Maine.\n",
    )
    replace(
        CEMENT_SCHEMATIC_RE,
        'The example structure uses illustrative input-output coefficients; note that in this structure, "process heat cement" is treated as a specific energy commodity, so as to avoid allowing electricity to compete for market share of this input to the cement production process.',
    )
    replace(
        AMMONIA_N_FERTILIZER_SCHEMATIC_RE,
        lambda match: (
            "Fuel and feedstock sources and input-output coefficients are calibrated based on Table 4.15 of "
            f"[IEA 2007]({match.group('target')}). Ammonia and N fertilizer commodities sit between the energy and agricultural systems of GCAM.\n"
        ),
    )
    replace(
        N_FERTILIZER_SCHEMATIC_RE,
        lambda match: (
            "Fuel and feedstock sources and input-output coefficients are calibrated based on Table 4.15 of "
            f"[IEA 2007]({match.group('target')}). N fertilizer sits between the energy and agricultural systems of GCAM.\n"
        ),
    )
    replace(
        PASSENGER_TYPICAL_REGION_RE,
        "The structure of the passenger sector differs by region; the omitted schematic summarized one typical regional structure.\n",
    )
    replace(
        PASSENGER_AS_SHOWN_RE,
        "In a typical regional structure, the passenger sector consists of up to five nesting levels,",
    )
    replace(
        LAND_GROWTH_FIGURE_RE,
        "When land is converted to forests, the vegetation carbon content of that new forest land gradually approaches an exogenously-specified, region- and land-type-dependent value. The rate at which this value is reached depends on the mature age of forests. Mature age is specified by region, GLU, and land type. Growth trajectories as a function of time since planting differ across four representative mature ages, and the omitted figure's y-axis represented the percentage of the exogenously-specified, region- and land-type-dependent value accumulated.\n",
    )
    replace(
        HISTORICAL_FOREST_REGROWTH_FIGURE_RE,
        "When land is converted to forests, the vegetation carbon content of that new forest land exponentially approaches an exogenously-specified, region-dependent value in order to represent the finite time required for forests to grow. The omitted figure illustrated the implied regrowth timescales.",
    )
    replace(
        DETAILS_LAND_CROP_SUBDIVISION_FIGURE_RE,
        "Crop areas are further subdivided into irrigated/rainfed and high/low management categories. This specification allows for adjusting the level of substitution across categories by varying the logit parameters. The omitted figure also mapped those categories to the corresponding `gcamdata` processing files for each land type.",
    )
    replace(
        DETAILS_LAND_FILE_MAP_FIGURE_RE,
        "The omitted figure also indicated which `gcamdata` file processes the inputs for each type of land",
    )
    replace(
        DACCS_ATTRACTIVENESS_FIGURE_RE,
        "The existing assumptions for energy and geologic carbon storage supply in each state and grid region further determine the relative attractiveness of DACCS deployment in each state within GCAM.",
    )
    replace(
        LNG_TRADE_NETWORK_FIGURES_RE,
        "Natural gas has been further disaggregated into traded pipeline gas and traded liquefied natural gas (LNG). LNG is traded at the global market level, while pipeline gas is traded in 6 regional markets: North America, Latin America, Europe, Russia+, Africa and Middle East, and Asia-Pacific.",
    )
    replace(
        DETAILS_EMISSIONS_COMPARISON_FIGURES_RE,
        "Two omitted figures compare historical emissions from CEDS with GCAM emissions after initialization: one at the global-by-species level and one as a region-by-species-by-year scatter comparison. Those comparisons indicate that emissions translate mostly correctly for all species of gases.",
    )
    replace(
        ECONOMY_MACRO_FIGURE_RE,
        "The omitted figure summarized the new macroeconomic elements in relation to the existing GCAM elements.",
    )
    replace(
        INPUTS_SUPPLY_FAO_MAPPING_FIGURES_RE,
        lambda match: (
            f"The commodity mapping is provided in [{match.group('label')}]({match.group('target')}). "
            "The omitted figures illustrated representative harvested-area and food mappings."
        ),
    )
    replace(
        TRADE_MARKET_STRUCTURE_FIGURE_RE,
        'The omitted figure summarized the structural implementations of a "global-market" versus a "regional-market" representation using a representative crop-trade example.',
    )
    replace(
        TRADE_MARKET_COMPARISON_FIGURE_RE,
        "An omitted comparison figure also contrasted the two market structures using a 2010 global wheat market-equilibrium example with demand and supply flows.",
    )
    replace(
        V32_TRANSPORTATION_STRUCTURE_RE,
        "GCAM contains a detailed representation of transportation energy use and service demands, with the sector divided into three service demands: passenger, freight, and international shipping. The omitted figure summarized that top-level transportation structure.",
    )
    replace(
        V32_TOC_END_USE_SECTORS_FIGURE_RE,
        "end-use sectors: buildings, industry and transport. The omitted figure summarized that transformation-to-end-use linkage.",
    )
    replace(
        V32_INDUSTRY_AGGREGATE_FIGURE_RE,
        "In all non-US regions, the industrial sector is represented as a consumer of generic energy services and feedstocks. The omitted figure summarized that aggregate-sector structure.",
    )
    replace(
        V32_INDUSTRY_US_FIGURES_RE,
        "Each manufacturing industry group consumes energy to produce a range of intermediate industrial services, such as steam and machine drive. The omitted figure summarized one representative U.S. industry structure.",
    )
    replace(
        V32_INDUSTRY_US_ENERGY_REQUIREMENTS_RE,
        "The omitted figure summarized the eleven GCAM industries and their 2005 energy requirements by service.",
    )
    replace(
        V32_SOCIOECONOMIC_FIGURES_RE,
        "The omitted figures summarized population and GDP in the current baseline scenario.",
    )
    replace(
        V32_DEPLETABLE_RESOURCE_FIGURES_RE,
        "The omitted regional resource-curve examples covered natural gas, crude oil, unconventional oil, and coal.",
    )
    replace(
        V32_UNCONVENTIONAL_OIL_SHOWN_BELOW_RE,
        "note that for unconventional oil, the omitted plotted supply curves did not include the cost of the energy used in extraction, and as such the actual supply curves in each region would have higher costs at all quantities.",
    )
    replace(
        V32_GLOBAL_RESOURCE_DOTTED_LINES_RE,
        "The omitted figures also overlaid dotted global resource supply curves derived by summing each region's available resource at each price point.",
    )
    replace(
        V32_WIND_REGION_ORDER_FIGURE_RE,
        "The omitted Figure 5 ranked GCAM regions by wind resource magnitude in the following order:",
    )
    replace(
        V32_ROOFTOP_PV_FIGURE_RE,
        "The omitted Figure 6 provided representative rooftop PV supply curves; as with wind, this supply curve only accounts for the portion of the costs that increase with deployment.",
    )
    replace(
        V32_GEOTHERMAL_SUPPLY_FIGURE_RE,
        "The omitted Figure 7 summarized the hydrothermal and EGS resource supply curves across regions.",
    )
    replace(
        V32_WASTE_BIOMASS_FIGURE_RE,
        "The omitted Figure 8 summarized regional waste-biomass supply curves; supplies are generally based on the amount and composition of municipal waste produced in each GCAM region.",
    )
    replace(
        V32_ELECTRICITY_WIND_PV_FIGURES_RE,
        "For wind power, the U.S. supply curve is based on NREL (2008), and the omitted figure used it as the reference shape. The plotted supply curve also included technology non-energy costs, but not ancillary costs. The same supply-curve shape is assumed for non-U.S. regions, but with maximum resource amounts scaled to estimates from GIS-based analysis, also informed by IEAGHG (2000). Assumed maximum resources for all GCAM regions are shown in Table 7. The rooftop PV supply curve for the U.S. is from NREL (P. Denholm and R. Margolis, pers. comm.), and the omitted figure used it as the corresponding reference for rooftop solar. The assumed limit in non-U.S. regions, shown in Table 7, is based on a GIS analysis of solar irradiance by region.",
    )
    replace(
        V32_ELECTRICITY_GEOTHERMAL_FIGURE_RE,
        "Geothermal costs in GCAM are input as exogenous supply curves. Supply curves assumed for hydrothermal and EGS resources for the U.S. are based on Petty and Porro (2007), and the omitted figure summarized those reference curves.",
    )
    replace(
        V32_REFINING_FIGURE_RE,
        "The omitted Figure 1 summarized the refining technology options, while Table 1 reports the non-energy costs and input/output coefficients.",
    )
    replace(
        V32_UNCONVENTIONAL_REFINING_FIGURE_RE,
        "note the electricity and gas inputs to the “unconventional oil production” sector in the omitted schematic and Table 1",
    )
    replace(
        V32_ECONOMIC_LAND_COMPETITION_FIGURE_RE,
        "An omitted figure illustrated two competing land-use options with profit distributions. In that example, the option with the higher potential average profit receives the larger share, while land is allocated until the marginal profit rates of the competing options and the land price at the margin are equal.",
    )
    replace(
        V32_ECONOMIC_LAND_SHARE_EQUATION_RE,
        "The logit sharing equation for land uses across an assumed level of competition, whether leaves in a node or among nodes in a nest, was embedded as an inline source image and is omitted in this text bundle. It defines each option's land share from relative profitability at that nest level.",
    )
    replace(
        V32_ECONOMIC_LAND_PROFIT_SYMBOL_RE,
        "In that omitted equation, the corresponding symbol denotes the profit rate of option i and `p` is the logit exponent.",
    )
    replace(
        V32_ECONOMIC_LAND_AVG_PROFIT_EQUATION_RE,
        "The average profit rate for a node resulting from the share competition in each nest was also given by an inline equation image in the upstream source; the surrounding text below explains how to interpret that average-profit term.",
    )
    replace(
        POLICIES_FIGURE_EXAMPLE_RE,
        "For example, in period T, compare a reference path without a carbon tax to the emissions path with a carbon tax; the cost of moving between them can be calculated directly.",
    )
    replace(
        POLICIES_TAX_REVENUE_RE,
        "The tax revenue can be calculated as the tax rate times the remaining emissions.",
    )
    replace(
        re.compile(
            r"The depiction of the grid-region-specific graded CO<sub>2</sub> transport storage cost curves reflect"
        ),
        "The grid-region-specific graded CO<sub>2</sub> transport storage cost curves reflect",
    )
    replace(re.compile(r"The costs shown in the figure include"), "The reported costs include")

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
            USER_GUIDE_OPEN_DB_WAIT_BUTTON_RE,
            "once the wait condition ends it will attempt to open the DB once more, and if that second attempt still fails then the results will be lost.",
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
            DATA_SYSTEM_IEA_BROWSER_RE,
            lambda match: (
                "Users who have access to the [IEA energy balances]"
                f"({match.group('link')}) must obtain a CSV export from the licensed source dataset. "
                "The GCAM data system is configured for the 2012 edition of the IEA energy balances, which goes "
                "through 2010 for all countries and sectors and provides 2011 estimates for a small selection of "
                "variables. More recent editions may still work with the existing R code, but any changes to the "
                "names or available categories of `COUNTRY`, `PRODUCT`, or `FLOW` will require mapping and/or "
                "code updates. Agent adaptation: do not rely on a specific GUI such as `Beyond 2020 Browser`. "
                "Instead, ensure the export uses years as columns and keeps the following ID fields present with "
                "no dimensions fixed:\n"
            ),
        )
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
    if rel_source.name == "GCAM_Revision_History.md":
        replace(
            GCAM_REV_HISTORY_CLICK_RE,
            "If the version note on a page indicates that it was revised for a later GCAM version than the one you need, inspect that page's revision history and select the last revision that predates the later-version update:",
        )

    if rel_source.parts[-2:] == ("dev-guide", "git.md"):
        replace(
            DEV_GUIDE_GIT_POINT_AND_CLICK_RE,
            "Git can be used entirely through text commands. Agent adaptation: prefer shell-based Git for GCAM "
            "workflows. Historical graphical clients are listed below only as ecosystem context for users who "
            "need them.\n\n",
        )
        replace(
            DEV_GUIDE_GIT_INTERNAL_SERVER_RE,
            "PNNL staff should use the internal server when it is available. Agent adaptation: treat the "
            "historical Bitbucket host as one forge endpoint among many; the essential workflow is to push your "
            "branch (q.v. [creating branches](#Creating-branches)) to a writable remote and create the "
            "corresponding review request through the forge's CLI or API.\n\n",
        )
        replace(
            DEV_GUIDE_GIT_OUTSIDE_USERS_RE,
            "Outside users should use the GitHub repository. You will normally have read access to this "
            "repository but not direct write access. If you want to do development, create your own fork or "
            "other writable mirror, create branches there, and submit a pull request or equivalent review "
            "request back to the main repository.\n\n",
        )
        replace(
            DEV_GUIDE_GIT_OPEN_PR_RE,
            "Once you've made some progress on your development, you will want to open a "
            "[pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/"
            "about-pull-requests) or the equivalent review request on your forge. Notionally, this is a "
            "proposal to merge changes from your branch into another branch (usually the `master` branch), but "
            "it also creates the review thread where other developers can examine the code and give feedback. "
            "Open that review request as soon as you have progress worth sharing. If your forge supports draft "
            "or work-in-progress review states, use them; otherwise mark unfinished work clearly in the title or "
            "description.\n\n",
        )
        replace(
            DEV_GUIDE_GIT_PR_FOLLOWUP_RE,
            "Once the review request exists, expect feedback from other developers. Push additional commits to "
            "your branch to address that feedback or continue development; those commits should remain attached "
            "to the same review record automatically. When development is complete, update the review state to "
            "ready for merge. Before the branch can be merged, you will have to write a change proposal (q.v. "
            "[GCAM Review Process](review.md)).\n\n",
        )

    if rel_source.parts[-2:] == ("dev-guide", "test_framework.md"):
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_INTRO_RE,
            "Agent adaptation: this page documents historical internal CI wiring. Treat pull-request pages, "
            "buttons, and Jenkins/Bitbucket UI labels as names for repository events, webhook payloads, and "
            "status APIs, not mandatory GUI steps.\n\n"
            "Most users will interact with the testing framework through repository review events or CI-trigger "
            "metadata and will not need to worry about updating the testing framework. Some instances of when "
            "they would need to update include:\n",
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_LAUNCH_BUTTON_RE,
            "Historical workflow note: the internal validation system exposed a `Launch Validation Runs` action that collected the following user-selectable options:\n",
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_BUTTON_FORM_RE,
            "By default this validation action ran the scenario set currently required by the team: Ref, Ref + 2.6, SSPs, and SSPs + SPA 2.6. All of the SPA climate target levels in the committed `batch_SSP_SPA*.xml` files were also available. The UI form definition was maintained manually, but the actual runnable scenarios were generated from the batch files committed in the `gcam-core` repository.",
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_OPEN_PR_RE,
            lambda match: (
                "After pushing the testing-framework branch and the updated submodule pointer, submit the "
                "repository review request that should trigger CI for your host platform. Historical upstream "
                "docs described this as opening a pull request. If both GCAM core and the testing-framework "
                "repository changed, keep the two linked review records together. Historical testing-framework "
                f"repository URL: {match.group('repo')}.\n"
            ),
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_PR_NOTIFIER_RE,
            lambda match: (
                "This historical Bitbucket plugin acted as the event-to-webhook adapter for CI. For agent use, "
                "treat it as the component that maps repository review events, updates, and optional form "
                "payloads into structured metadata sent to Jenkins. Full upstream plugin documentation: "
                f"{match.group('url')}\n"
            ),
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_NOTIFY_STATUS_RE,
            "This historical Jenkins plugin reported build state back to Bitbucket. For agent use, treat it as "
            "a commit-status API updater that publishes `IN_PROGRESS`, `FAILURE`, or `SUCCESS` plus a build URL "
            "for logs and artifacts.\n",
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_BUTTON_RE,
            'Historical UI note: the internal "Launch Validation Runs" button invoked Jenkins with the '
            '"JGCRI-gcam-pic" tag and the following metadata payload:\n',
        )
        replace(
            DEV_GUIDE_TEST_FRAMEWORK_HISTORICAL_BUTTON_RE,
            "Historical workflow note: invoking that validation action called Jenkins with the `JGCRI-gcam-pic` tag and the following metadata payload:\n",
        )

    if rel_source.parts[-2:] == ("dev-guide", "getting_started.md"):
        replace(
            DEV_GUIDE_GETTING_STARTED_PR_STEP_RE,
            "6. When your development is complete, submit the host platform's review request for the branch. "
            "Agent adaptation: use the forge CLI or API when available instead of assuming a browser-only pull "
            "request action.\n",
        )

    if rel_source.parts[-2:] == ("dev-guide", "analysis.md"):
        replace(
            DEV_GUIDE_ANALYSIS_GUI_RE,
            "software developers wanting to write new automation front ends or other higher-level tools for "
            "working with GCAM",
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

    def render_comment(content: str) -> str:
        normalized = content.replace("&nbsp;", " ")
        normalized = re.sub(r"\s+", " ", normalized).strip(" -")
        lowered = normalized.lower()
        if not normalized:
            return ""
        if "if gte mso" in lowered or "startfragment" in lowered or "[endif]" in lowered:
            return ""
        return f"Comment: {normalized}\n"

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
        attrs = match.group("attrs") or ""
        content = match.group("content")
        anchor_match = HTML_ID_OR_NAME_ATTR_RE.search(attrs)
        anchor_name = ""
        if anchor_match:
            anchor_name = (anchor_match.group("double") or anchor_match.group("single") or "").strip()
        if anchor_name:
            anchor = f'<a name="{anchor_name}"></a>'
            if content.strip():
                return f"{anchor}{content}"
            return anchor
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
    segment = HTML_COMMENT_RE.sub(lambda match: render_comment(match.group("content")), segment)
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

    def render_comment(content: str) -> str:
        normalized = content.replace("&nbsp;", " ")
        normalized = re.sub(r"\s+", " ", normalized).strip(" -")
        lowered = normalized.lower()
        if not normalized:
            return ""
        if "if gte mso" in lowered or "startfragment" in lowered or "[endif]" in lowered:
            return ""
        return f"Comment: {normalized}\n"

    segment = ESCAPED_MSO_EXPORT_BLOCK_RE.sub("", segment)
    segment = ESCAPED_HTML_STYLE_BLOCK_RE.sub("", segment)
    segment = ESCAPED_HTML_BR_RE.sub("\n", segment)
    segment = ESCAPED_HTML_BUTTON_RE.sub(unwrap_button, segment)
    segment = ESCAPED_HTML_COMMENT_RE.sub(
        lambda match: render_comment(match.group("content")),
        segment,
    )
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


def normalize_citation_markup(segment: str) -> str:
    def replace_wrapped(match: re.Match[str]) -> str:
        label = match.group("label").strip()
        label = re.sub(r",\s{2,}", ", ", label)
        label = re.sub(r"\s{2,}", " ", label)
        return f"[{label}]({match.group('target')})"

    def replace_broken(match: re.Match[str]) -> str:
        label = re.sub(r"\s{2,}", " ", match.group("label").strip())
        return f"[{label})]({match.group('target')})"

    segment = PAREN_WRAPPED_CITATION_LINK_RE.sub(replace_wrapped, segment)
    segment = BROKEN_ANCHOR_CITATION_LINK_RE.sub(replace_broken, segment)
    return segment


def apply_outside_inline_code(text: str, transform) -> str:
    parts: list[str] = []
    last = 0
    for match in INLINE_CODE_RE.finditer(text):
        parts.append(transform(text[last : match.start()]))
        parts.append(match.group(0))
        last = match.end()
    parts.append(transform(text[last:]))
    return "".join(parts)


def normalize_semantic_text(segment: str) -> str:
    def normalize_entities(text: str) -> str:
        text = text.replace("&nbsp;", " ")
        text = text.replace("&#160;", " ")
        text = text.replace("&#xa0;", " ")
        text = text.replace("&#xA0;", " ")
        previous = None
        while text != previous:
            previous = text
            text = text.replace("&amp;", "&")
        text = html.unescape(text)
        return text

    def normalize_reference_links(text: str) -> str:
        text = BROKEN_DOUBLE_BRACKET_LINK_RE.sub(
            lambda match: f"[{match.group('label').strip()}]({match.group('target').strip()})",
            text,
        )
        text = BROKEN_DOUBLE_BRACKET_LABEL_LINK_RE.sub(
            lambda match: f"[{match.group('label').strip()}]({match.group('target').strip()})",
            text,
        )
        return re.sub(r"(?<=\))(?=\[)", " ", text)

    def render_subscript(content: str) -> str:
        normalized = normalize_entities(content)
        normalized = re.sub(r"\s+", "", normalized)
        return normalized

    def render_superscript(content: str) -> str:
        normalized = normalize_reference_links(normalize_entities(content))
        normalized = re.sub(r"\s+", " ", normalized).strip()
        if not normalized:
            return ""
        if normalized.startswith("[") or "](" in normalized:
            return f" {normalized}"
        return f"^{normalized}"

    def transform(text: str) -> str:
        text = normalize_inline_html(normalize_entities(text))
        for _ in range(4):
            updated = re.sub(
                r"&lt;sub&gt;(?P<content>.*?)&lt;/sub&gt;",
                lambda match: f"<sub>{match.group('content')}</sub>",
                text,
                flags=re.IGNORECASE | re.DOTALL,
            )
            updated = re.sub(
                r"&lt;sup&gt;(?P<content>.*?)&lt;/sup&gt;",
                lambda match: f"<sup>{match.group('content')}</sup>",
                updated,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if updated == text:
                break
            text = updated
        text = re.sub(
            r"<sub>(?P<content>.*?)</sub>",
            lambda match: render_subscript(match.group("content")),
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        text = re.sub(
            r"<sup>(?P<content>.*?)</sup>",
            lambda match: render_superscript(match.group("content")),
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        text = normalize_reference_links(text)
        return text

    return apply_outside_inline_code(segment, transform)


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
    text = normalize_problem_unicode_whitespace(text)
    text = normalize_problem_unicode_punctuation(text)
    text = rewrite_images(text)
    text = MISATTACHED_CODE_FENCE_RE.sub("\n```", text)
    text = apply_outside_code_fences(
        text,
        lambda chunk: normalize_semantic_text(
            normalize_citation_markup(
                normalize_escaped_wiki_refs(
                    normalize_escaped_inline_html(
                        normalize_markdown_attribute_residue(
                            normalize_markdown_table_residue(
                                normalize_inline_html(
                                    rewrite_html_hrefs(rewrite_markdown_links(chunk, version), version)
                                )
                            )
                        )
                    )
                )
            )
        ),
    )
    text = strip_image_artifacts(text)
    text = normalize_omitted_image_lines(text)
    text = sanitize_absolute_paths(text)
    text = apply_agent_text_adaptations(text, rel_source)
    text = apply_outside_code_fences(
        text,
        lambda chunk: apply_outside_inline_code(chunk, normalize_figure_text_residue),
    )
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
    title = normalize_heading_text(title)
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
    if rel_source.name == "data-system.md":
        lines.append(
            "- Note: This adapted data-system page rewrites source-tool GUI export wording into dataset-shape requirements, filesystem targets, and text-first preprocessing steps."
        )
    if rel_source.name == "hector.md":
        lines.append(
            "- Note: This adapted Hector page rewrites IDE integration click paths into agent-readable dependency and build-setting summaries."
        )
    if rel_source.parts[-2:] == ("dev-guide", "test_framework.md"):
        lines.append(
            "- Note: This adapted testing-framework page preserves historical internal CI topology but rewrites pull-request/button/UI phrasing into repository events, webhook payloads, and status API concepts."
        )
    if rel_source.parts[-2:] == ("dev-guide", "git.md"):
        lines.append(
            "- Note: This adapted git page preserves historical forge examples but rewrites browser-specific actions into CLI/API-friendly repository workflow terms."
        )
    if rel_source.parts[-2:] == ("dev-guide", "getting_started.md"):
        lines.append(
            "- Note: This adapted getting-started page rewrites final submission steps as host-agnostic review-request workflow instead of browser-only pull-request actions."
        )
    if rel_source.parts[-2:] == ("dev-guide", "analysis.md"):
        lines.append(
            "- Note: This adapted analysis page prefers automation-oriented descriptions over GUI-centric wording where the original text listed tool categories."
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
