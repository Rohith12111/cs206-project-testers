## Prerequisites

### Python Installation

This project requires Python to be installed on your system. It has been developed and tested with Python 3.8 and newer versions. If Python is not already installed on your computer, you need to install it on the system that you are running it on.

### Standard Library Dependencies

This project utilizes several Python Standard Library modules: os, subprocess, json, sys, and argparse. These modules come pre-installed with Python, so no additional installation is required.
Verifying Standard Library Modules. These modules should be available in any standard Python installation. If you encounter an error related to missing modules, ensure your Python installation is correctly set up and up to date. Python Standard Library modules are not installed via pip, as they are inherently part of the Python installation.


### Directory Structure and Scripts Overview

Each benchmark program directory is structured to include three key Python scripts: random_coverage.py, total_coverage.py, and additional_coverage.py. These scripts are designed to generate minimal test suites using different prioritization methods: random prioritization, total coverage, and additional coverage, respectively.

### Key Python Files
random_coverage.py: Implements the random prioritization method for test suite generation.
total_coverage.py: Utilizes the total coverage prioritization method to generate the test suite.
additional_coverage.py: Generates the test suite based on additional coverage prioritization.

Each script supports two types of coverage analysis:

- 'Statement Coverage': Analyzes the statements covered by the test suite.
- 'Branch Coverage': Focuses on the branches covered by the test suite.

### Running the Scripts

To execute any of the scripts and generate a test suite, you need to use the following command-line arguments, depending on your coverage analysis preference:
For Statement Coverage use “-s” command line option
To generate a test suite with statement coverage analysis, use the following command, substituting file-name.py with the appropriate script name (random_coverage.py, total_coverage.py, or additional_coverage.py):

$ python file-name.py -s

For Branch Coverage use “-b” command line option
For test suite generation focusing on branch coverage, the command is similar, with a slight modification to use the -b option:
$ python file-name.py -b
Note: Ensure to replace file-name.py with the specific script you wish to run (random_coverage.py, total_coverage.py, or additional_coverage.py).

### Location of Test Suites:
#### * Benchmark_program/testsuites (Ex: tcas/testsuites)

Upon execution, each script generates a .txt file containing the test suite. All the .txt files generated are for the benchmark program are stored in “testsuite” directory. The content of this file will satisfy either the statement or branch coverage criteria, depending on the options you've selected during the run



### Fault Exposure Analysis

In addition to the coverage-based test suite generation scripts, each directory contains a script named fault_exposure.py. This script is designed to execute the test suites generated by the aforementioned scripts against multiple versions of the target codebase.

## Purpose
The primary function of fault_exposure.py is to identify and expose faults within different code versions. It achieves this by running the test cases from the generated test suites and monitoring their execution outcomes across all provided code versions.

## Output
Upon completion, the script reports which versions of the program each test case failed on, effectively highlighting the faults uncovered by the test suite. This program generates a ‘.txt’ file which is stored inside the “faults” directory. This information is invaluable for understanding the fault resilience of the codebase and pinpointing specific areas requiring attention.

## Running the Script:
Within the respective benchmark directory, the fault_exposure.py script is executed to evaluate fault exposure across different versions of the code, using test suites generated for various coverage criteria.
To run the fault_exposure.py script, in the respective benchmark folder run the below command with appropriate command line flag:	

$ python fault_exposure.py -option

Here, replace -option with the specific coverage criterion flag you wish to apply:

- 'tsc': Total Statement Coverage

- 'tbc': Total Branch Coverage

- 'rsc': Random Statement Coverage

- 'rbc': Random Branch Coverage

- 'asc': Additional Statement Coverage

- 'abc': Additional Branch Coverage

- '-u': Original Test Suite

Each flag corresponds to a different test suite prioritization method, directing the script to run the associated test suite against all versions of the benchmark program. The script then reports which code versions were revealed to contain faults by the test suite.

Also, you can give “-u” to get the faults exposed by the original testsuite on all the versions of the certain benchmark program.

Example:

For example, to analyze faults using the test suite generated for total statement coverage, run:

$ python fault_exposure.py -tsc

Ensure that you have the generated test suites and the different code versions available in the specified directory structure for the script to function as intended.
