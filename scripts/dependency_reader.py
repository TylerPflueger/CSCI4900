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
        # Need to run on each package with oneshot to get identifiers
        # unless update dosocsv2 to create identifiers on scan
        # or fix up dosocsv2 to create identifiers on scan instead
        for node in self.tree.expand_tree(mode=Tree.DEPTH):
            treeNode = self.tree.get_node(node)
            subprocess.call('dosocs2 oneshot ' + treeNode.data.jarName, shell=True)

    def createRelationships(self):
        # Pass packages as relationships to new dosocsv2 command created
        self.recursiveRelationship(self.tree.root)

    def recursiveRelationship(self, parent):
        for node in self.tree.is_branch(parent):
            parentNode = self.tree.get_node(parent)
            childNode = self.tree.get_node(node)
            subprocess.call('dosocs2 packagerelate ' + parentNode.data.jarName + ' ' + childNode.data.jarName, shell=True)
            self.recursiveRelationship(node)

    def retrieve_dependencies(self, jarName):
        if jarName is None:
            root = self.tree.get_node(self.tree.root)
            root = root.data.jarName
        else:
            root = jarName

        tgfOutput = subprocess.Popen('dosocs2 dependencies ' + root, stdout=subprocess.PIPE, shell=True)
        count = 0
        tree = Tree()
        dependencies = []
        relationships = []
        while True:
            line = tgfOutput.stdout.readline()

            if not line:
                break

            match = re.match(r"(\d+) - (.*)", line)
            if match:
                if count == 0:
                    count = count + 1
                    tree.create_node(match.group(2), match.group(1))
                else:
                    dependencies.append((match.group(2), match.group(1)))

            match = re.match(r"(\d+) (\d+)", line)

            if match:
                relationships.append((match.group(1), match.group(2)))

        if not relationships:
            print("No child relationships for " + jarName)
            return None

        while relationships:
            for item in relationships:
                node = tree.get_node(item[0])

                if node is not None:
                    rel = [item for item in relationships if int(item[0]) == int(node.identifier)]
                    if rel is not None:
                        rel = rel[0]
                        dep = [item for item in dependencies if int(item[1]) == int(rel[1])]
                        if dep is not None:
                            dep = dep[0]
                            tree.create_node(dep[0], dep[1], parent=node.identifier)
                            relationships.remove(rel)
                            dependencies.remove(dep)

        tree.show()
        if jarName is None:
            os.chdir(os.pardir)
