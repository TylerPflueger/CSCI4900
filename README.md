# CSCI4900 [![Build Status](https://travis-ci.org/tpflueger/CSCI4900.svg?branch=master)](https://travis-ci.org/tpflueger/CSCI4900)

## To install
`pip install .` within top-level of project

Note - Current setup doesn't install branch of [DoSOCSv2/feature/relationships](https://github.com/tpflueger/DoSOCSv2/tree/feature/relationships) that domaven relies on. You will need to follow the instructions first before trying to install current project for it to work.

## Usage
Pass pom.xml to be parsed, domaven will then pass all the parsed dependencies to DoSOCSv2 with relationship info:

    $ domaven scan ./path/to/pom.xml

Pass jar file that has already been scanned and displays dependency tree:

    $ domaven dependencies ./path/to/file.jar

## System Description
Python script that connects Maven to DoSOCS. Uses Maven to find out project-level dependencies based on passed pom.xml. A tree is constructed of the hierarchy from parent package downward. All the packages are then given to DoSOCSv2 to be stored into the the database along with the relationship info information which pertains to the SPDX schema.

## Development Environment
- UBUNTU 14.04
- Python 2.7
- DoSOCSv2

## Communication Management Plan
- Email
- Github
- 2 meetings a week (Tuesdays/Thursdays)

## Dataflow diagram of the system
![dataflow-diagram](https://cloud.githubusercontent.com/assets/8797790/13802073/12b5a7e4-eb06-11e5-9f14-55f73c22a777.png)

## SPDX diagram of database
![SPDX-diagram](https://cloud.githubusercontent.com/assets/2850506/13796701/2f0e8508-ead6-11e5-86c9-62c93beed600.png)

## USE CASE
Title: Dependency relationship creation in SPDX
Primary Actor: Developer
Goal in context: Discover dependencies for a prject and store relationship in an SPDX schema
Stakeholders and Interests: Developers
Preconditions: Maven, DOSOCS, environment setup
Main success scenario: Created dependency tree and stored relationships in the SPDX schema
Failed end conditions: unsuitable POM xml file
Trigger: "domaven", pom file

## TEST CASES

### scan
1. Does scan accept a pom file?
2. Is scan able to grab all dependencies from Maven with pom file?
3. After grabbing all dependencies, is it able to create the tree?
4. Does it send each package to be scanned and related and stored in the database?
5. Does it get tgf output from DoSOCS2 of dependencies?
6. Does it show a tree view of all the dependencies?

### dependencies
1. Does dependencies accept a jar file?
2. Is it able to connect to DoSOCS2 by passing the jar file to it?
3. Does it return tgf output from DoSOCS2 of child dependencies?
4. Does it show a tree view of current and child dependencies based on jar file given?

## License

MIT © Aarjav Chauhan, Tyler Pflueger

CC-BY-SA-4.0 © Aarjav Chauhan, Tyler Pflueger
