# Building GCAM (Command Line First)

Bundled build summary for GCAM, rewritten for agent-oriented CLI workflows.

Use this file after version routing. Compiler and dependency details evolve across versions, but the command-line build pattern remains the safest default.

Open `workspace_layouts.md` when you need to decide whether the user has a source checkout, a release workspace, or a legacy nested package layout. Open `release_workflows.md` when the user still needs to choose between downloading a release package and building from source.

## Default Build Policy
- Prefer command-line builds.
- Treat IDE-specific Xcode and Visual Studio pages as historical evidence, not as the skill's default workflow.
- If the user provides an exact checkout, inspect its build files before giving repo-specific commands.

## When to Compile
Most users run prebuilt binaries. Compile only when:
- You need a platform not covered by release packages.
- You are modifying C++ source code.
- You need to rebuild Java support, XML DB tooling, or other runtime components.

## Required Tools and Libraries
- C++17-capable compiler for the modern line
- Boost
- RapidXML or the Boost-provided equivalent
- Java / JDK for BaseX output and Java components
- Eigen
- Intel TBB
- Hector submodule

Version note:
- Older lines such as `v4.x` and `v6.0` used C++14-era guidance.
- Modern bundled guidance should be treated as version-aware rather than blindly universal.

## Hector
Hector is required for GCAM builds and is included as a submodule.

In a git checkout:
- `git submodule init cvs/objects/climate/source/hector`
- `git submodule update cvs/objects/climate/source/hector`

## Preferred POSIX Build Flow
Set the include/library environment variables expected by the Makefile, such as:
- `BOOST_INCLUDE`
- `BOOSTROOT`
- `JARS_LIB`
- `JAVA_INCLUDE`
- `JAVA_LIB`
- `EIGEN_INCLUDE`
- `TBB_INCLUDE`
- `TBB_LIB`

Then build from the Linux Makefile directory:

```bash
cd cvs/objects/build/linux
make gcam -j <N>
```

This is the primary build path to recommend for automation and CI-style usage.

## Windows Build Flow
The upstream docs describe the Visual Studio project file with `Release` and `x64` settings. For agent use, translate that into a CLI-first build against:

- `cvs/objects/build/vc10/objects.vcxproj`

Representative command-line form:

```powershell
msbuild cvs/objects/build/vc10/objects.vcxproj /p:Configuration=Release /p:Platform=x64
```

Notes:
- Keep the Java runtime path available so GCAM can find `jvm.dll`.
- If the project toolset must be updated once for a newer compiler, do that explicitly, then continue building from the command line.
- The release package wrappers such as `run-gcam.bat` remain the normal way to launch the resulting executable.

## Java and XML Database Notes
GCAM writes BaseX outputs via Java.

If you need to compile without Java:
- edit `cvs/objects/util/base/include/definitions.h`
- set `__HAVE_JAVA__` to `0`

If Java is disabled, GCAM can still emit `debug_db.xml` by enabling `DEBUG_XML_DB` in `cvs/objects/reporting/source/xml_db_outputter.cpp`.

For agent workflows, prefer later headless processing of that output rather than manual interactive database import steps.

## Recompiling Java Components
The modern bundled docs include command-line rebuild flows for:
- `ModelInterface.jar`
- `XMLDBDriver.jar`

Representative flow:

```bash
export CLASSPATH=<GCAM Workspace>/libs/jars/*
cd <GCAM Workspace>/output/modelInterface/
git submodule update --init modelinterface
cd modelinterface
make ModelInterface.jar
cp ModelInterface.jar ../
```

```bash
export CLASSPATH=<GCAM Workspace>/libs/jars/*:<GCAM Workspace>/output/modelInterface/ModelInterface.jar
cd <GCAM Workspace>/cvs/objects/java/source
make clean
make install
```

## Runtime Sanity Check
After a successful build:
- expect the executable in `exe/`
- run the wrapper script or direct executable from the command line
- inspect `exe/logs/main_log.txt`

## Historical Caution
- Exact page bundles still preserve older Xcode and Visual Studio instructions for traceability.
- The skill should summarize those pages into CLI build actions instead of reproducing IDE click paths unless the user explicitly requests them.
