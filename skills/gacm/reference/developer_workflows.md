# Developer Workflows

Skill-bundled topic reference for GCAM development practices, debugging patterns, Fusion, and the broader ecosystem of companion tools.

Use this file after version routing when the user is modifying source code, debugging a run, asking about GCAM Fusion, or trying to place companion tools in the GCAM workflow.

## When to Open This File
Open this file for:
- source-code modification workflows
- development and debugging questions
- GCAM Fusion coupling questions
- broader ecosystem and workflow-tool selection

Open `building_gcam.md` for compiler and dependency setup. Open `tools.md` for focused `gcamreader` and `gcamextractor` usage.

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
- extraction and reporting: `modelinterface`, `rgcam`, `gcam_reader`, `gcamrpt`
- execution and workflow: `pygcam`
- data development: `gcamdata`, `moirai`
- single-system companions: `hector`, `xanthos`, `persephone`, `gcamfd`, `gcamland`
- disaggregation: `tethys`, `demeter`
- visualization: `gcammaptools`, dashboard tooling
- integration: `cassandra`

## Runtime Rule
These tools are conceptual context, not runtime dependencies of the `gacm` skill.

If the user provides a real checkout or asks for exact tool commands tied to a specific repo state, inspect that context directly instead of guessing from the bundled summary.
