# GCAM User Guide

Bundled adapted source page for GCAM `v5.1`.

- Source root: `gcam-doc/v5.1`
- Source path: `user-guide.md`
- Coverage mode: `full-tree page bundle`
- Bundle mode: `text-only page bundle; images omitted`
- Version page index: `version_pages/v5.1/BUNDLE_INDEX.md`
- Note: This adapted user-guide page rewrites interactive ModelInterface browsing into headless-agent guidance and omits screenshot-dependent UI steps.

Load this page when the user needs version-specific detail from this exact page family.

---

## Table Of Contents
  [1. Introduction](#gcam-intro)

  [2. Quickstart](#gcam-quickstart)

  [3. GCAM User's Guide](#gcam-users-guide)

* [Configuration File](#configuration-file)
* [GCAM Batch file](#gcam-batch-mode)
* [Target finder mode](#target-finder)
* [ModelInterface](#modelinterface)
* [Controlling the level of XML DB Output](#controlling-the-level-of-xml-db-output)

## <a name="gcam-intro"></a>1.Introduction
This document provides information on acquiring and running the GCAM model. Agent adaptation: the upstream source referenced website navigation for release downloads; in this skill, resolve the target release from repository contents, version route docs, or release archives instead of relying on page layout. There will typically be separate platform release packages plus a source archive for rebuild workflows.

* gcam-v5.1-Mac-Release-Package.zip contains the GCAM executable, supporting libraries, the ModelInterface, and input XML files for the Mac OS X platform.  **Note for most Mac users this is typically the only package required.**
* gcam-v5.1-Windows-Release-Package.zip contains the GCAM executable, supporting libraries, the ModelInterface, and input XML files for the Windows platform. **Note for most Windows users this is typically the only package required.**
* Source code (in zip or tar.gz format).  This is the core of the release and contains all model source code and data processing scripts.  Generally only needed if you need to compile the source code from scratch.  Users who will need to maintain changes to source code and/or data processing code for an extended period of time should strongly consider checking out the repository with Git instead.

The following instructions for users who want to use the pre-built GCAM executable and XML input files.  For instructions on compiling your own GCAM executable see [GCAM Compile Instructions](gcam-build.md).  For instructions on how to run the gcamdata R package to rebuild the XML input files from scratch see [Running the GCAM Data System](data-system.md).  Once built these users can proceed from the [Quickstart](#gcam-quickstart) guide.

To start users should download and unpack the Release Package appropriate for their platform to a location of their choosing.  Throughout this document that location will be referred to as `<GCAM Workspace>`.

The rest of this user's guide is divided into two parts. First a [GCAM "quickstart"](#gcam-quickstart) guide with basic instructions on running GCAM and viewing results, followed by a more detailed [GCAM User's Guide](#gcam-users-guide).

## 2. <a name="gcam-quickstart"></a>GCAM Quickstart

This section provides a brief introduction on how to use the GCAM Model and view model data using the GCAM model interface. The instructions in this Quickstart guide should work with a GCAM distribution release that has been downloaded and uncompressed to your local machine.

**Warning:** For GCAM 5.1 computational requirements have increased significantly.  A GCAM model simulation will utilize over 8 GB of system RAM and storing the full results of the simulation will take around 2 GB of disk space per scenario.

### 2.1. Running a reference case scenario

GCAM requires a valid `configuration.xml` file be present in the exe directory of the GCAM workspace. You can run a reference scenario by copying the `configuration_ref.xml` that is provided in the distribution and renaming it to `configuration.xml`. The configuration file is descried in more detail in the [User's Guide section](#3-gcam-users-guide), and should not need to be modified in order to run a reference case scenario. The User's Guide describes how to create additional scenarios.

A `log_conf.xml` file is also needed, but this file is provided in the
release package and should therefore already be present in the exe
directory.

Agent adaptation: invoke GCAM from the shell instead of desktop launch. Expect log messages as GCAM reads XML inputs and solves each model period; inspect `exe/logs/main_log.txt` for run diagnostics.

After a successful model run the log file will end with the following text (depending on your set-up and platform, you might also see this on your screen):
```
Starting output to XML Database.
Data Readin, Model Run & Write Time: 1273.42 seconds.
Model run completed.
Model exiting successfully.
```

#### 2.1.1 Common failures

The most common wrapper-launch failures when starting GCAM from packaged scripts typically relate to Java. Dealing with Java differs depending on your system.

#### 2.1.1.1 Windows

If a user sees a message similar to any of the following:

* Unable to locate `jvm.dll`
* A 64-bit Java is required to run GCAM
* Or sometimes a generic message about the application is unable to start correctly (referencing some memory address)

The most likely case is that the `run-gcam.bat` script was unable to detect the correct version of GCAM to use.  Either there is no 64-bit version of Java installed or both a 32-bit and 64-bit is installed and it didn't choose the right one.  In either case you should edit `run-gcam.bat` and update the `JAVA_HOME` manually to point to the correct location and delete the `REM` before the `SET`:
```
REM Users may set the following location to the appropriate Java Runtime installation location
REM instead of trying to detect the appropriate location.  This may be necessary if the default
REM Java version is the 32-bit runtime.
REM SET JAVA_HOME=<JAVA_HOME>
```

Another common problem on Windows is GCAM also relies on the [Microsoft Visual Studio 2015 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=48145) 64-bit package be installed as well.  Although the error message in this situation tends to be more reliable and descriptive.

#### 2.1.1.2 Mac

On the Mac a missing Java usually prompts an install of "legacy Java" from Apple.  Note this install is no longer supported by GCAM.  Instead users will need to install the Java Developer Kit from Oracle version 1.7 or newer.  The processes is a little bit more involved so users should follow the same instructions for setting up [Java when compiling GCAM](gcam-build.md#23-java).

##### 2.1.1.2.1 Troubleshooting Java on Mac
The`<GCAM Workspace>/exe/run-gcam.command`script attempts to put a symbolic link into the `libs/java` directory that points to the location of the necessary java libraries (e.g., `libjvm.dylib`).

If, when attempting to run GCAM, the libraries are not found, you will get an error message of:`dyld: Library not loaded: @rpath/libjvm.dylib`. In this case the problem may be that the symlink is not actually pointing to the directory that contains the needed library. This can occur if the `run-gcam.command`script gets out of sync with the java version (e.g. using an older version of GCAM or if java is updated).

To fix this, use `ls -l` or `readlink` within terminal to resolve the symlink path. If the path is incorrect, then create a new symlink that points to the java `sdk` directory that contains the libjvm.dylib library (please see [Java when compiling GCAM](gcam-build.md#23-java) for details on how to do this).

### 2.2 Viewing Model Results

Comprehensive model output from each scenario is stored in an XML database. (Note that the current BaseX database is not compatible with older versions of GCAM and the GCAM model interface that use the .dbxml format.)

Agent adaptation: result inspection should start from batch or file-based query automation, not interactive ModelInterface browsing. The underlying ModelInterface tooling is still Java-based, so Java remains required when those query tools are used.

Agent adaptation: the upstream source described interactive ModelInterface browsing here. For agent use, prefer headless query automation via `ModelInterface/InterfaceMain -b <batch.xml>`, post-run `XMLDBDriver.properties` batch queries, or the shared `reference/query_automation.md` guide.

Agent adaptation: older macOS packaging notes about `ModelInterface.app` bundle metadata are not the primary workflow for agents. Prefer invoking the jar from the shell or editing `model_interface.properties` directly in a text-accessible working directory.

The XML files within each `FileSet` block will be read in after the `ScenarioComponents` in the configuration file and then run. The scenario name of the run will be the name of each `FileSet` appended to the `scenarioName` in the configuration file.

If there are multiple `ComponentSet` blocks, then all permutations of `FileSets` within each `ComponentSet` will be run.

Note that there is also a [batch functionality](#modelinterface-batch-modes) within the `ModelInterface`, which has a different format.

### 3.3 <a name="target-finder"></a>Target finder

Enabling this mode for running GCAM involves specifying a [policy target file](#312-files-input-options) and enabling [find-path](#314-bools-input-options).  In addition when a user is running target finder with a negative emissions budget constraint they should be sure to set up the market, for example by reading in the policy file `carbon_tax_0.xml`.  When run in this mode GCAM will run a scenario several times to find the optimal path to satisfy the configured climate goal.  Running GCAM in such a mode can take quite a bit of time, one option to speed this up is to set `restart-period` to 22 in the [configuration file as noted above](#315-ints-input-options).  Example policy target files are supplied in `input/policy` and are self documented:
```XML
<policy-target-runner name="forcing_4p5">
    <!-- tax-name | default: CO2 | The market name to change the price on -->
	<tax-name>CO2</tax-name>

    <!-- target-value | no default | The target value such as concentration
         or forcing.
     -->
    <target-value>4.5</target-value>

    <!-- target-tolerance | default: 0.01 | The solution tolerance -->
    <target-tolerance>0.005</target-tolerance>

    <!-- path-discount-rate | default: 0.05 | The hotelling rate -->
    <path-discount-rate>0.05</path-discount-rate>

    <!-- max-iterations | default: 100 | The maximum  number of attempts to
         solve any given period.
     -->
     <max-iterations>100</max-iterations>

    <!-- target-type | default: concentration | The climate parameter which
         we are targeting.  The available ones are:
            concentration | CO2 (or possibly other gasses via the configuration
                            string: concentration-target-gas)
            forcing | Total radiative forcing
            stabilization | Stabilize CO2 (or possibly other gasses via the
                           configuration string: concentration-target-gas)
                           with disregards to what that concentration might be
            kyoto-forcing | Radiative forcing from Kyoto GHGs only
            rcp-forcing | Radiative forcing using the RCP definition
            temperature | Global mean temperature
            cumulative-emissions | Reach a cumulative emission goal for CO2
                                   emissions (or possibly other gasses via the
                                   configuration string: cumulative-target-gas)
     -->
    <target-type>forcing</target-type>

    <!-- first-tax-year | default: 2020 | The first year to start a tax in -->
    <first-tax-year>2020</first-tax-year>

    <!-- forward-look | default: 0 | Allow forward looking behavior by skipping
         this many periods.
     -->
    <forward-look>1</forward-look>

    <!-- stabilization | This is the default behavior is to stabilize the target
         overshoot year="2100" | Allow for an overshoot to hit in the target in
                                 given year.  If the year is not provided the
                                 last model year will be assumed.  If it is
                                 provided and before the last model year then
                                 it will have to stay on target after that year.
     -->
     <stabilization />

    <!-- max-tax | default: 4999 | Set a maximum tax to try in any given period
                                   to avoid extremely large taxes for which GCAM
                                   may have trouble solving.  Note that it may
                                   be possible the algorithm finds a solution
                                   with tax values capped at max-target for some
                                   years in which case the user should increase
                                   the max-tax.  If the actual solution price
                                   lies above max-tax the algorithm will fail.
     -->
    <max-tax>4999</max-tax>
</policy-target-runner>
```

Note that target finder runs can also be configured in [Batch mode](#gcam-batch-mode).  In this case you should leave the `find-path` bool to `0`.  Note the `policy-target-file` are specified in their own section, and `<single-scenario-runner />` indicates to run a permutation with no target finding, e.g. the reference scenario:
```XML
<BatchRunner>
    <ComponentSet name="Policy scenarios">
        <FileSet name="FFICT_">
            <Value name="land-policy">../input/policy/global_ffict.xml</Value>
        </FileSet>
        <FileSet name="UCT_">
            <Value name="land-policy">../input/policy/global_uct.xml</Value>
        </FileSet>
    </ComponentSet>
    <runner-set name="policy-target-runner">
        <Value name="6p0target">../input/policy/forcing_target_3p7.xml</Value>
        <Value name="4p5target">../input/policy/forcing_target_4p5.xml</Value>
        <Value name="2p6target">../input/policy/forcing_target_2p6_overshoot.xml</Value>
        <single-scenario-runner />
    </runner-set>
</BatchRunner>
```

### 3.4 <a name="modelinterface"></a>ModelInterface

The model interface is the historical GCAM tool for querying [BaseX](http://basex.org) XML databases and converting CSV files to XML.

Agent adaptation: the packaged `ModelInterface.jar` / `ModelInterface.app` is not the default workflow in this bundle. Prefer direct batch execution, query-file editing, and scripted CSV/XLS export.

Agent adaptation: treat the `interactive mode` subsection below as historical context and prefer batch or direct file-based workflows.

Agent adaptation: older macOS packaging notes about `ModelInterface.app` bundle metadata are not the primary workflow for agents. Prefer invoking the jar from the shell or editing `model_interface.properties` directly in a text-accessible working directory.

#### <a name="interactive-mode"></a>3.4.1 Interactive Mode

Agent adaptation: interactive mode is preserved only as historical context. For agent work, read scenario names from the database, region names from results or batch query files, and query definitions from XML files directly. Inspect `model_interface.properties` as plain text to locate the active query file, for example:
```
<entry key="queryFile">../output/queries/Main_queries.xml</entry>
```

Note if the query file is not found the ModelInterface will ask you to select a new one.  Each query is represented in it's own XML syntax such as:
```XML
<emissionsQueryBuilder title="GHG emissions by region">
    <axis1 name="GHG">GHG</axis1>
    <axis2 name="Year">emissions</axis2>
    <xPath buildList="true" dataName="emissions" group="false" sumAll="false">*[@type = 'sector' (:collapse:) or @type = 'resource' (: collapse :)]//*[@type = 'GHG']/emissions/node()</xPath>
    <comments/>
</emissionsQueryBuilder>
```

Agent adaptation: query XML is plain text. Copy it between files, repositories, or messages as needed, then edit and save the underlying query file directly instead of relying on GUI copy/paste or interactive save-menu actions.

#### <a name="modelinterface-batch-modes"></a>3.4.2 ModelInterface Batch Modes

When doing scenario analysis on GCAM results it is often very useful to predefine the set of queries you would like to look at and automatically save the results to CSV or XLS format for plotting or making tables, etc.  Setting up the Model Interface to do this is done in one or two steps depending on the level of automation you would like.

First you must set up a "batch query" file.  An example of such a file can be found in `output/gcam_diagnostics/batch_queries/Model_verification_queries.xml`.  The idea of such a file is you list the queries you would like to run one after the other and for each query you include the regions (which can be any of the region names available in the database or query context) you would like to query.
```
<queries>
    <aQuery>
        <region name="USA" />
        <region name="Canada" />
        <gdpQueryBuilder title="GDP by region">
            <axis1 name="region">region</axis1>
            <axis2 name="Year">gdp-mer</axis2>
            <xPath buildList="true" dataName="gdp-mer" group="false" sumAll="false">GDP/gdp-mer/text()</xPath>
            <comments/>
        </gdpQueryBuilder>
    </aQuery>
```

The actual queries are the same XML definitions described [above](#interactive-mode) and can be copied between query files, repositories, or batch command files.

Agent adaptation: the interactive batch-file menu path is omitted. The portable workflow is to reference the batch query file from a ModelInterface batch command file and execute it from the shell, setting output paths and scenario names in XML rather than interactive dialogs.

Alternatively if users prefer to set up a workflow that does not require any manual user interaction they may prefer to set up a "batch command" file as well (and even collapse the "batch query" to be defined with in the "batch command" itself).  An example of such a file can be found at `output/gcam_diagnostics/batch_queries/xmldb_batch.xml`:
```XML
<ModelInterfaceBatch>
    <!-- Note multiple sets of the following are allowed to run several
         batch queries sequentially.
      -->
    <class name="ModelInterface.ModelGUI2.DbViewer">
        <command name="XMLDB Batch File">
            <!-- List all the scenarios to query, if no scenario are given then
                 the last scenario in the database will be queries. Note that if
                 multiple scenarios have the same name the latest one will be used,
                 to differentiate explicitly define the date with date="..." in the
                 scenario tag.
              -->
            <scenario name="Core_Ref"/>

            <!-- The Batch queries file to run.  Alternatively users could specify the
                 queries to run here contained with in <queries> ... </queries> tags
            -->
            <queryFile>batch_queries/Model_verification_queries.xml</queryFile>
            <!-- Where to write results -->
            <outFile>gcam_data/Core/reference.csv</outFile>
            <!-- Which database to query -->
            <xmldbLocation>../database_basexdb</xmldbLocation>
            <!-- Additinoal query options which will be ignored when saving to CSV -->
            <batchQueryResultsInDifferentSheets>false</batchQueryResultsInDifferentSheets>
            <batchQueryIncludeCharts>false</batchQueryIncludeCharts>
            <batchQuerySplitRunsInDifferentSheets>false</batchQuerySplitRunsInDifferentSheets>
            <batchQueryReplaceResults>true</batchQueryReplaceResults>
        </command>
    </class>
</ModelInterfaceBatch>
```

Users can the invoke the Model Interface from the command line as follows to call their batch file and no user interface will be presented.  Note if a batch file named `-` is specified then the "batch commands" are read from the STDIN.  Users can also instruct the ModelInterface to save log output to a file by using the flags `-l path/to/log/output.txt`.
```
CLASSPATH=<GCAM Workspace>/libs/jars*:<GCAM Workspace>/output/modelInterface/ModelInterface.jar
java -cp $CLASSPATH ModelInterface/InterfaceMain -b batch_queries/xmldb_batch.xml
```

#### 3.4.3 Importing data into R

If you use the R programming language to do your data analysis, then
you can use the rgcam package to make analysis tasks more convenient.
This package provides R functions for extracting results from GCAM
databases and importing them as R structures.  They take your GCAM
output database, along with the same batch query file described in the
last section, and run them through the Model Interface, making the
results available in your R session for analysis.  The imported data
is also stored in a project data file for future use.

The rgcam package is available on github at
[JGCRI/rgcam](https://github.com/JGCRI/rgcam).  Installation and
quick-start usage instructions are available on the repository's front
page.  Detailed documentation of the functions provided by the package
is available through the R help system once the package is installed.

#### 3.4.4 Importing data into python

The [gcam_reader](https://github.com/JGCRI/gcam_reader) python package
for importing GCAM data is currently in beta testing.  Although not
yet as complete as the R package, the python package supports basic
functionality including importing individual or batched queries as
pandas data frames for analysis or use in other python programs.

### 3.5 <a name="controlling-the-level-of-xml-db-output"></a>Controlling the level of XML DB Output

The GCAM XML database output is verbose and can consume a lot of disk space.  Users may seek to limit or even query and discard these results, particularly when doing a large number of runs, to save space and time.  To do this they can configure in `<GCAM Workspace>/exe/XMLDBDriver.poperties` the following options:
```XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
<comment>Configuration properties to control the behavior of storing GCAM output into the XML database.</comment>
<!-- If the results should put into an in memory database.
     WARNING: this means the data will be lost once the DB is closed.
     This option would be useful if the user wanted to run queries on the results then
     discard them.  Also note that GCAM will still be holding it's memory while this DB
     is created.
-->
<entry key="in-memory">false</entry>
<!-- A timeout, in seconds, to wait in case a user tries to write to an already open DB.
     A negative value indicates to wait indefinately.  Once the timeout has expired or
     once the wait condition ends it will attempt to open the DB once more, and if that second attempt still fails then the results will be lost.
-->
<entry key="open-db-wait">-1</entry>
<!-- The path to an STX style script to filter GCAM results before writing them to the
     DB.  If empty no filters will be applied.
-->
<entry key="filter-script"></entry>
<!-- The path to a Model Interface batch file to run queries after a GCAM run has
     finished.  If a value of - is specified this instructs the Model Interface
     to read the batch file from STDIN which could be useful when being run by some
     other controlling program that wants to dynamically generate the queries to run.
     Note that GCAM will wait to run these queries until after the scenario
     has cleaned up it's memory to create more space for the Model Interface and to
     ensure all results (including cost curves) are available.  If empty no queries
     will be run.
-->
<entry key="batch-queries"></entry>
<!-- Redirect the log messages from running batch queries to the specified log file.
     Note that an empty value will keep the messages printing to the standard output.
-->
<entry key="batch-logfile">logs/batch_queries.log</entry>
</properties>
```

#### 3.5.1 In memory database
Setting this option will instruct BaseX to keep the entire database in memory instead of writing the results to permanent storage.  In memory databases can be faster to write and much faster to query.  However this will consume much more memory and as soon as GCAM exits the results are lost.  As noted above this would only be useful if a user wanted to run a set of queries against the database and save those select CSV (or XLS) results instead of the XML database.

#### 3.5.2 Filtering results
Specifying a filter script will filter the GCAM results as it is produced by GCAM and only ever writing the filtered results.  We used the Joost library to do this which is reminiscent of the XSLT standard however imposes some limitations in order to processes XML as it is generated (as apposed to XSLT which needs to store the full results before it can process them which is unrealistic given the size of the GCAM XML results). A good introduction to the concept can be found [here](http://www2.informatik.hu-berlin.de/~obecker/Docs/EML2003/script.html)

The specification for how to write the filter scripts using the Streaming Transformation for XML (STX) sytanx can be found [here](http://stx.sourceforge.net/documents/spec-stx-20070427.html)

A number of example filter scripts are provided in the GCAM workspace under `<GCAM Workspace>/output/queries/filters`.  As mentioned earlier the syntax is very similar to XSLT where the bulk of the work is done with template filters that match XML using an XPath syntax with the exception the XPath expressions can not look ahead.  Meaning for instance that you could not filter a technology by inspecting the value of any of it's child nodes such as physical-output.  The reason for this is STX must be able to process the XML as it is generated and the child XML would not yet been generated. However STX does provide some workaround to accomplish this using XSLT!  More specifically it allows you to collect the results at a given node of interest and apply a sub-filter script once all of the XML for that node has been collected and that sub-filter can be written using XSLT which does allow looking ahead in it's template definitions.  An example script which takes advantage of this feature can be found in `GCAM Workspace/output/queries/filters/results_2020_to_2035.xml`.

#### 3.5.3 Running batch queries
Runs the Model Interface in [batch mode](#modelinterface-batch-modes) if in the configuration a "batch-queries" file is specified.  Note that the "batch-queries" will be read and processed as normal ["batch command"](#modelinterface-batch-modes) except that the `<xmldbLocation>` will be ignored and use the database opened by GCAM instead.  If no batch queries file is specified the Model Interface will not be loaded and no queries will be run.  Note: batch queries will wait until the last moment for any given scenario to exist before running.  This is to ensure any target finding and/or cost calculations have been run an written to the database so that information would be available to the queries.

#### 3.5.4 Using these features on an exported XML results file
The tools that provide these features can be run independently from GCAM via the command line.  This can be useful for working with .xml files exported from the XML DB or the [debug_db.xml file](gcam-build.md#231-disable-java).  A user could programmatically load them back into a new XML DB using any of the aforementioned features.  This is done by calling the `<GCAM Workspace>/exe/XMLDBDriver.jar` directly:
```
CLASSPATH=<GCAM Workspace>/libs/jars*:<GCAM Workspace>/output/modelInterface/ModelInterface.jar
java -cp ${CLASSPATH}:XMLDBDriver.jar XMLDBDriver --help
USAGE:
   java -cp XMLDBDriver.jar XMLDBDriver --db-path=PATH --doc-name=NAME --xml=FILE
or
   java -cp XMLDBDriver.jar XMLDBDriver --print-java-path

NOTE: If the first form is used, the arguments -db-path, --doc-name, and --xml are all required.
      Options can be abbreviated using any unique prefix, e.g., --db=XXX --doc=YYY -x foo.xml

Option             Description
------             -----------
--db-path          Path to XML database
--doc-name         The unique name to call the document
                     in the DB
--help             Print this message
--print-java-home  Print the path to the Java home
                     directory and exit
--xml              The exported GCAM results XML file to
                     load
```
