# SPDX-License-Identifier: MIT
'''Usage:
{0} scan (FILE)
{0} dependencies (JARNAME)
{0} (--help | --version)

Arguments:
    scan            Scan pom file for dependencies
    dependencies    Show dependency tree for jarFile
'''
import shutil
import sys
import os
from dependency_reader import DependencyReader
from docopt import docopt

__version__ = '0.0.1'

def main():
    argv = docopt(
        doc=__doc__.format(os.path.basename(sys.argv[0])),
        argv=sys.argv[1:],
        version=__version__
    )

    dependencyReader = DependencyReader()
    if argv['scan']:
        dependencyReader.getPom(os.path.abspath(argv['FILE']))
        dependencyReader.getDependencies()
        dependencyReader.relateDependencies()
        dependencyReader.scanDependencies()
        dependencyReader.createRelationships()
        dependencyReader.retrieve_dependencies(None)
        shutil.rmtree(dependencyReader.tempDirectoryPath)
    elif argv['dependencies']:
        dependencyReader.retrieve_dependencies(argv['JARNAME'])

if __name__ == "__main__":
    sys.exit(main())
