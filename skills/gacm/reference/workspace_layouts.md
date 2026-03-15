# Workspace Layouts

Guide to recognizing GCAM workspace structure from paths and files instead of guessing.

Open this file when the task is about:
- locating the executable, configuration files, queries, or policies
- deciding whether the user has a release package or a source checkout
- translating versioned documentation paths into the user's real workspace

## Hard Rule
Never assume a machine-specific absolute path.

Infer workspace type from the files that actually exist.

## Modern Release Workspace Pattern
Common top-level directories:
- `exe/`
- `input/`
- `output/`
- `libs/`

Typical contents:
- `exe/`: `configuration.xml`, `configuration_ref.xml`, `configuration_policy.xml`, wrapper scripts, logs
- `input/policy/`: policy XML examples
- `output/queries/`: query XML such as `Main_queries.xml`
- `output/gcam_diagnostics/batch_queries/`: example batch query and batch command files
- `libs/jars/`: Java dependencies for BaseX and related tooling

Use this pattern for most `v5.4+` and `v8.2` operational guidance.

## Modern Source Checkout Pattern
Common signs:
- `cvs/objects/build/linux`
- `cvs/objects/build/vc10`
- `cvs/objects/java/source`
- `output/modelInterface/`

Interpretation:
- this is a source-oriented workspace
- build files exist, but a ready-to-run `exe/` may not yet be populated
- compile guidance from `building_gcam.md` is probably relevant

## Legacy Release Packaging Pattern
Common signs in older docs:
- `Main_User_Workspace/`
- separate `ModelInterface/` directory
- older release-package path strings such as `<Release Package>/Main_User_Workspace/...`

Interpretation:
- treat the nested `Main_User_Workspace` as the effective runtime root
- do not silently rewrite those paths into modern `v8.2` assumptions

This pattern matters most for `v3.2` and some early `v4.x` guidance.

## Detection Checklist
When the user provides a path, classify it in this order:

1. If it contains `cvs/objects/build/`, treat it as a source checkout.
2. If it contains `Main_User_Workspace`, treat that directory as the runtime workspace root.
3. If it contains sibling `exe/`, `input/`, and `output/`, treat it as a release workspace.
4. If none of the above are clear, ask for a directory listing rather than guessing.

## Path Mapping Heuristics

### Runtime Files
- configuration files usually live in `exe/`
- logs usually live in `exe/logs/`
- XML databases usually live under `output/`

### Query Files
- modern line: `output/queries/Main_queries.xml`
- example batch query assets: `output/gcam_diagnostics/batch_queries/`

### Policy Files
- modern line: `input/policy/`

### Build Files
- POSIX Makefile flow: `cvs/objects/build/linux`
- Windows project file: `cvs/objects/build/vc10/objects.vcxproj`
- Java components: `cvs/objects/java/source`

## Command Translation

### If the user gives a release workspace
- run from `exe/`
- edit configuration files in `exe/`
- treat `input/` and `output/` as sibling directories

### If the user gives a source checkout
- compile first if no executable exists
- then switch to the built runtime workspace for scenario execution

### If the user gives a legacy nested workspace
- keep the nested root exactly as documented
- do not flatten paths in your answer

## Related References
- `configuration_workflows.md`
- `running_gcam.md`
- `building_gcam.md`
- `query_automation.md`
