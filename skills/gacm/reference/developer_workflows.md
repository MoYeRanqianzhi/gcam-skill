# Developer Workflows

Skill-bundled topic reference for GCAM development practices, debugging patterns, Fusion, and the broader ecosystem of companion tools.

Use this file after version routing when the user is modifying source code, debugging a run, asking about GCAM Fusion, or trying to place companion tools in the GCAM workflow.

## When to Open This File
Open this file for:
- source-code modification workflows
- development and debugging questions
- GCAM Fusion coupling questions
- broader ecosystem and workflow-tool selection

Open `building_gcam.md` for compiler and dependency setup. Open `tools.md` for focused `gcamreader`, `rgcam`, and `gcamextractor` usage. Open `workspace_layouts.md` when you need to map these workflows onto a real repository or release package.

## Agent Bias
For this skill, prefer tools that support:
- scripted execution
- text outputs
- repeatable configuration edits
- headless extraction

Visualization and point-and-click tooling are part of the broader ecosystem, but they are not the default recommendation path here.

## Common Development Concerns
Recurring developer topics in the bundled authoring sources include:
- getting started with the repository and branch workflow
- rapid parse and test workflows
- code review and style guidance
- debugging XML parsing, configuration, and solver failures
- selecting the right downstream analysis or extraction tool

## Debugging Pattern
Typical debugging order:
1. Confirm input paths and XML validity.
2. Confirm `ScenarioComponents` ordering.
3. Distinguish parse failure, calibration failure, and solver failure.
4. Separate Java/BaseX problems from core model problems.
5. Reproduce on the smallest scenario or shortest relevant period set you can.

## GCAM Fusion
GCAM Fusion is the high-level query and feedback interface for coupling external models to a running GCAM simulation.

Core ideas:
- expose GCAM internals through a higher-level query surface closer to XML tag semantics
- permit feedback callbacks only at controlled points
- support two-way coupling without making every model object effectively global

Key callback phases:
- before a model period begins solving
- after a model period solves and climate results are available

Fusion is an advanced C++-level developer topic. Use it only when the user is clearly asking about coupling or model-internal feedbacks.

## Ecosystem Map
The bundled authoring sources group companion tooling roughly like this:
- extraction and reporting: `rgcam`, `gcam_reader`, `gcamrpt`, headless `modelinterface` batch usage
- execution and workflow: `pygcam`
- data development: `gcamdata`, `moirai`
- single-system companions: `hector`, `xanthos`, `persephone`, `gcamfd`, `gcamland`
- disaggregation: `tethys`, `demeter`
- visualization: `gcammaptools`, dashboard tooling
- integration: `cassandra`

## Recommended Tool Order
When the user wants to automate work around GCAM:
1. Use native GCAM configuration and batch files first.
2. Use `pygcam` when the task is scenario orchestration, workflow automation, or repeated execution.
3. Use `gcamreader`, `rgcam`, or `gcamextractor` when the task is output extraction.
4. Use Fusion only for true coupling or callback-style model integration.

## Runtime Rule
These tools are conceptual context, not runtime dependencies of the `gacm` skill.

If the user provides a real checkout or asks for exact tool commands tied to a specific repo state, inspect that context directly instead of guessing from the bundled summary.
