from treelib import Node, Tree
import subprocess
import re
from dependency_node import DependencyNode
from tempfile import mkdtemp
import shutil

tempDirectoryPath = mkdtemp(dir=".")

value = subprocess.Popen('mvn dependency:tree -DoutputType=tgf', stdout=subprocess.PIPE, shell=True)

tree = Tree()
dependencies = {}
val = []

def getDependencies():
    while True:
        line = value.stdout.readline().rstrip()

        if not line or re.search(r"BUILD SUCCESS", line):
            break

        # This isn't working for output with version:compile(or whatever else)
        match = re.match(r"\[INFO\]\s(\d*)\s*(.*):(.*):(\w+):([0-9\.]*)", line)

        if match:
            if not match.group(1) in dependencies.keys():
                dependencies[match.group(1)] = DependencyNode(match.group(2), match.group(3), match.group(5), match.group(1))

            if not tree.leaves():
                tree.create_node(match.group(1), match.group(1), data=dependencies[match.group(1)])

            dependencies[match.group(1)].get('jar', tempDirectoryPath)

        match = re.match(r"\[INFO\]\s(\d*)\s(\d*)", line)

        if match and match.group(2):
            val.append((match.group(1), match.group(2)))

getDependencies()

while val:
    for item in val:
        node = tree.get_node(item[0])

        if node is not None:
            parent = dependencies[item[0]]
            dependency = dependencies[item[1]]
            tree.create_node(dependency.referenceId, dependency.referenceId, parent=parent.referenceId, data=dependency)
            val.remove(item)

tree.show()
shutil.rmtree(tempDirectoryPath)
