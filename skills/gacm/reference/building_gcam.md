# Building GCAM (Compile)

Bundled build summary for the GCAM line.

Use this file after version routing. Compiler and dependency details evolve across versions, but the general build pattern remains useful.

## When to Compile
Most users run prebuilt binaries. Compile only when:
- You need a platform not covered by release packages.
- You are modifying C++ source code.

## Required Tools and Libraries
- C++17-capable compiler
- Boost (headers)
- RapidXML (usually via Boost)
- Java (1.7+; required for BaseX output)
- Eigen (header-only)
- Intel TBB (parallelism)
- Hector submodule

## Hector
Hector is required for GCAM builds and is included as a submodule.
In a git checkout:
- `git submodule init cvs/objects/climate/source/hector`
- `git submodule update cvs/objects/climate/source/hector`

## Makefile Build (POSIX)
Set env variables (examples in doc):
- `BOOST_INCLUDE`
- `JARS_LIB`
- `JAVA_INCLUDE`
- `JAVA_LIB`
- `EIGEN_INCLUDE`
- `TBB_INCLUDE`
- `TBB_LIB`

Then build:
- `make gcam -j <N>` in `cvs/objects/build/linux`

## Xcode Build (macOS)
Open `cvs/objects/build/xcode3/objects.xcodeproj`.
Set scheme to Release and build. Output goes to `exe/`.

## Visual Studio Build (Windows)
Open `cvs/objects/build/vc10/objects.vcxproj`.
Set `Release` + `x64`, update toolset as needed, build solution.

## Java Notes
GCAM writes BaseX outputs via Java. You can disable Java in
`cvs/objects/util/base/include/definitions.h` by setting `__HAVE_JAVA__` to `0`.
With Java disabled, GCAM can still write `debug_db.xml` for later import.
