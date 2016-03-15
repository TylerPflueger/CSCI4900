# SPDX-License-Identifier: MIT
from treelib import Node, Tree
from dependency_node import DependencyNode
import subprocess
import re
from tempfile import mkdtemp
import os
import shutil

class DependencyReader:
    """DependencyReader object"""

    def __init__(self):
        self.tempDirectoryPath = mkdtemp(dir=".")
        self.tree = Tree()
        self.dependencies = {}
        self.graphRelationships = []

    def getPom(self, pomPath):
        shutil.copy(pomPath, self.tempDirectoryPath)
        os.chdir(self.tempDirectoryPath)

    def getDependencies(self):
        mavenTreeOutput = subprocess.Popen('mvn dependency:tree -DoutputType=tgf', stdout=subprocess.PIPE, shell=True)
        os.chdir(os.pardir)

        while True:
            line = mavenTreeOutput.stdout.readline().rstrip()

            if not line or re.search(r"BUILD SUCCESS", line):
                break

            match = re.match(r"\[INFO\]\s(\d*)\s*(.*):(.*):(\w+):([0-9\.]*)", line)

            if match:
                if not match.group(1) in self.dependencies.keys():
                    self.dependencies[match.group(1)] = DependencyNode(match.group(2), match.group(3), match.group(5), match.group(1))

                if not self.tree.leaves():
                    self.tree.create_node(match.group(1), match.group(1), data=self.dependencies[match.group(1)])

                self.dependencies[match.group(1)].get('jar', self.tempDirectoryPath)

            match = re.match(r"\[INFO\]\s(\d*)\s(\d*)", line)

            if match and match.group(2):
                self.graphRelationships.append((match.group(1), match.group(2)))

    def relateDependencies(self):
        while self.graphRelationships:
            for item in self.graphRelationships:
                node = self.tree.get_node(item[0])

                if node is not None:
                    parent = self.dependencies[item[0]]
                    child = self.dependencies[item[1]]
                    self.tree.create_node(child.referenceId, child.referenceId, parent=parent.referenceId, data=child)
                    self.graphRelationships.remove(item)

    def scanDependencies(self):
        subprocess.call('dosocs2 scan ' + self.tempDirectoryPath, shell=True)
