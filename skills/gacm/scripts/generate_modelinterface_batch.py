#!/usr/bin/env python3
"""
Generate a minimal ModelInterface batch-command XML file for headless GCAM queries.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.dom import minidom
import xml.etree.ElementTree as ET


def str_to_bool(value: bool) -> str:
    return "true" if value else "false"


def build_xml(
    scenario: str | None,
    query_file: str,
    out_file: str,
    xmldb_location: str,
    results_in_different_sheets: bool,
    include_charts: bool,
    split_runs_in_different_sheets: bool,
    replace_results: bool,
) -> str:
    root = ET.Element("ModelInterfaceBatch")
    class_node = ET.SubElement(root, "class", {"name": "ModelInterface.ModelGUI2.DbViewer"})
    command = ET.SubElement(class_node, "command", {"name": "XMLDB Batch File"})

    if scenario:
        ET.SubElement(command, "scenario", {"name": scenario})

    ET.SubElement(command, "queryFile").text = query_file
    ET.SubElement(command, "outFile").text = out_file
    ET.SubElement(command, "xmldbLocation").text = xmldb_location
    ET.SubElement(command, "batchQueryResultsInDifferentSheets").text = str_to_bool(
        results_in_different_sheets
    )
    ET.SubElement(command, "batchQueryIncludeCharts").text = str_to_bool(include_charts)
    ET.SubElement(command, "batchQuerySplitRunsInDifferentSheets").text = str_to_bool(
        split_runs_in_different_sheets
    )
    ET.SubElement(command, "batchQueryReplaceResults").text = str_to_bool(replace_results)

    raw = ET.tostring(root, encoding="utf-8")
    pretty = minidom.parseString(raw).toprettyxml(indent="    ", encoding="utf-8")
    return pretty.decode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a ModelInterface batch-command XML file for headless GCAM queries."
    )
    parser.add_argument("--scenario", help="Optional GCAM scenario name to embed in the batch file.")
    parser.add_argument("--query-file", required=True, help="Path to the GCAM query XML file.")
    parser.add_argument("--out-file", required=True, help="Output CSV or XLS path written by ModelInterface.")
    parser.add_argument("--xmldb-location", required=True, help="Path to the GCAM XML database.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the generated XML to this path. If omitted, print to stdout.",
    )
    parser.add_argument(
        "--results-in-different-sheets",
        action="store_true",
        help="Set batchQueryResultsInDifferentSheets=true.",
    )
    parser.add_argument(
        "--include-charts",
        action="store_true",
        help="Set batchQueryIncludeCharts=true.",
    )
    parser.add_argument(
        "--split-runs-in-different-sheets",
        action="store_true",
        help="Set batchQuerySplitRunsInDifferentSheets=true.",
    )
    parser.add_argument(
        "--no-replace-results",
        action="store_true",
        help="Set batchQueryReplaceResults=false.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    xml_text = build_xml(
        scenario=args.scenario,
        query_file=args.query_file,
        out_file=args.out_file,
        xmldb_location=args.xmldb_location,
        results_in_different_sheets=args.results_in_different_sheets,
        include_charts=args.include_charts,
        split_runs_in_different_sheets=args.split_runs_in_different_sheets,
        replace_results=not args.no_replace_results,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(xml_text, encoding="utf-8")
    else:
        print(xml_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
