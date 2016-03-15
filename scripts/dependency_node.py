# SPDX-License-Identifier: MIT
from subprocess import call


class DependencyNode:
    """DependencyNode object"""

    def __init__(self, groupId, artifactId, version, referenceId):
        """Pass artifact values to create node."""
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.referenceId = referenceId

    def get(self, type, tempDirectoryPath):
        command = "mvn -q dependency:copy " +\
            "-Dartifact=" + self.groupId + ':' + self.artifactId + ':' +\
            self.version + ':' + type +\
            " -DoutputDirectory=" + tempDirectoryPath
        call(command, shell=True)
