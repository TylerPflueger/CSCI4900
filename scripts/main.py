# SPDX-License-Identifier: MIT
'''Usage:
{0} FILE
{0} (--help | --version)

Arguments:
    FILE    path to pom.xml
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

    if argv['FILE']:
        dependencyReader = DependencyReader()

        dependencyReader.getPom(os.path.abspath(argv['FILE']))
        dependencyReader.getDependencies()
        dependencyReader.relateDependencies()
        dependencyReader.scanDependencies()
        dependencyReader.createRelationships()

        dependencyReader.tree.show()
        shutil.rmtree(dependencyReader.tempDirectoryPath)

if __name__ == "__main__":
    sys.exit(main())
