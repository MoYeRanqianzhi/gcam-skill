# Release Workflows (Download, Unpack, Upgrade)

Agent-first guide to acquiring a runnable GCAM workspace without falling back to GUI instructions.

Use this file after version routing when the user asks how to download, unpack, install, upgrade, or choose between a release package and a source checkout.

## Decision Rule
Prefer release packages when the user only needs to:
- run scenarios
- edit XML and configuration files
- inspect outputs
- execute headless query and export workflows

Prefer a source checkout when the user needs to:
- modify C++ or Java source
- rebuild GCAM
- maintain a long-lived fork
- change data-system code rather than only runtime XML inputs

If the user is unsure, default to a release package first.

## Release Package Workflow

### 1. Pick the exact version
- Use the exact version the user asked for.
- If the user does not specify one, the skill baseline is `v8.2`, but do not silently fetch a different release on the user's behalf.

### 1a. Official upstream entry points
Use stable official URLs instead of inventing asset names:
- source repository: `https://github.com/JGCRI/gcam-core`
- release page with downloadable assets: `https://github.com/JGCRI/gcam-core/releases`
- latest tagged release redirect: `https://github.com/JGCRI/gcam-core/releases/latest`

If the user wants an exact direct package URL instead of the generic release page, open `release_assets/direct_download_links.md`.

Operational rule:
- If the user asks to "download GCAM", send the releases page first.
- If the user asks for an exact known package URL by version and platform, use `release_assets/direct_download_links.md`.
- If the user asks for the latest GCAM release, send the `releases/latest` URL.
- If the user asks to clone source, use the repository URL or `https://github.com/JGCRI/gcam-core.git`.

### 2. Pick the correct asset class
Typical release assets documented in the upstream user guide:
- platform-specific release packages for running GCAM
- source code archives for building or maintaining source

Do not invent release asset names or platform packages; use the exact asset names visible in the provided release context.

### 3. Unpack to a workspace root
Treat the unpacked directory as `<GCAM Workspace>`.

Immediately verify that it contains the expected runtime structure:
- `exe/`
- `input/`
- `output/`
- wrapper scripts such as `run-gcam`, `run-gcam.bat`, or `run-gcam.command`

If the unpacked workspace lacks `exe/`, `input/`, or wrapper scripts such as `run-gcam`, `run-gcam.bat`, or `run-gcam.command`, you probably downloaded source code rather than a release package.

### 4. Verify runnable config files
Look for:
- `configuration_ref.xml`
- `configuration_policy.xml`
- `log_conf.xml`

Then switch to:
- `running_gcam.md` for execution
- `configuration_workflows.md` for scenario edits
- `query_automation.md` for extraction

## Source Checkout Workflow
Use a source checkout when the user needs code changes or source builds.

Typical pattern:
```bash
git clone <official gcam-core repo>
cd gcam-core
git checkout <tag-or-commit>
```

Then:
- inspect the checkout with `workspace_layouts.md`
- use `building_gcam.md` for compiler, dependency, and submodule steps

Important:
- do not describe a source checkout as if it were already a runnable release workspace
- source archives may require later dependency staging, submodule init, and compilation before `exe/` is usable

For source builds or long-lived code changes, switch to `building_gcam.md`.

## Companion Tool Installation
These tools are optional and should only be installed when the user needs them.

### Python
```bash
pip install gcamreader
```

### R
```r
install.packages("devtools")
devtools::install_github("JGCRI/gcamextractor")
```

Do not imply these packages are bundled into a GCAM release package by default.

## Upgrade and Multi-Version Hygiene
- Keep separate workspaces per version.
- Do not mix `exe/` from one version with `input/` or `output/queries/` from another.
- When the user upgrades, re-check wrapper scripts, config files, and query paths before reusing automation.
- If the user says "root docs" or "current docs", that is a documentation routing rule inside this skill, not proof that their local executable workspace is `v8.2`.

## Failure Cues
- wrong asset downloaded:
  runtime directories are missing after unpack
- wrapper script fails immediately:
  switch to `running_gcam.md` and inspect Java and log-path issues
- user wants compilation after unpacking a release package:
  confirm whether they actually need source code instead
- user wants `gcamdata` regeneration:
  a runnable release package alone is often not enough; they may need a source-oriented workflow and additional R tooling

## Next Docs To Load
- `workspace_layouts.md` to classify the unpacked tree
- `running_gcam.md` to execute GCAM
- `building_gcam.md` for source builds
- `query_automation.md` for extraction and post-run export

## Authoring Basis
- `gcam-doc/user-guide.md`
- `gcam-doc/gcam-build.md`
- `gcam-core/README.md`
