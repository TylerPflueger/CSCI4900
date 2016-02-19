from treelib import Node, Tree
import subprocess
import re
from dependency_node import DependencyNode

tree = Tree()

value = subprocess.Popen('mvn dependency:tree', stdout=subprocess.PIPE, shell=True)

def getInitialPomValue(lines):
    parent = ''
    dependencies = []

    while True:
        line = lines.stdout.readline().rstrip()

        if not line:
            break

        match = re.match(r"\[INFO\][^\|\\]([/+/-]*)?\s?([a-zA-Z\.\-0-9]*?):([a-zA-Z\.\-0-9]*?):([a-zA-Z\.\-0-9]*?):([0-9\.]*)", line)

        if match:
            print line
            if match.group(1) != '+-':
                parent = match
            else:
                dependencies.append(match)

    tree.create_node(parent.group(3), parent.group(3), data=DependencyNode(parent.group(2), parent.group(3), parent.group(4)))
    for dep in dependencies:
        tree.create_node(dep.group(3), dep.group(3), parent=parent.group(3), data=DependencyNode(dep.group(2), dep.group(3), dep.group(4)))

    tree.show()

getInitialPomValue(value)
