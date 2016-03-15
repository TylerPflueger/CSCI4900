# SPDX-License-Identifier: MIT
import shutil
import sys
import os
from dependency_reader import DependencyReader

def main():
    dependencyReader = DependencyReader()

    dependencyReader.getPom(os.path.abspath(sys.argv[1]))
    dependencyReader.getDependencies()
    dependencyReader.relateDependencies()
    dependencyReader.scanDependencies()

    dependencyReader.tree.show()
    shutil.rmtree(dependencyReader.tempDirectoryPath)

if __name__ == "__main__":
    main()
