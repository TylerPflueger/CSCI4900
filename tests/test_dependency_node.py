from scripts import dependency_node
from tempfile import mkdtemp
import shutil
import os
import glob

class TestDependencyNode:
    def setup_class(self):
        self.node = dependency_node.DependencyNode('org.joda', 'joda-money', '0.11', '1')
        os.chdir(os.path.abspath('./tests'))
        self.tempDirectoryPath = mkdtemp(dir=".")

    def teardown_class(self):
        os.chdir(os.pardir)
        shutil.rmtree(self.tempDirectoryPath)

    def test_should_create_dependency_node(self):
        assert 'org.joda' in self.node.groupId
        assert 'joda-money' in self.node.artifactId
        assert '0.11' in self.node.version
        assert '1' in self.node.referenceId

    def test_should_get_file(self):
        self.node.get('jar', self.tempDirectoryPath)
        os.chdir(self.tempDirectoryPath)
        filePath = glob.glob('*.jar')[0]
        assert filePath != None
