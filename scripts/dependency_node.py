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
        self.jarName = self.artifactId + '-' + self.version + '.jar'

    def get(self, type, tempDirectoryPath):
        command = "mvn -q org.apache.maven.plugins:maven-dependency-plugin:RELEASE:copy -Dartifact=" + self.groupId + ":" + self.artifactId + ":" + self.version + ":" + type + " -DoutputDirectory=."
        call(command, shell=True)

    def get_relationships(self):
        command = "dosocs2 dependencies " +\
            self.jarName
        call(command, shell=True)
