class DependencyNode:
    """DependencyNode object"""

    def __init__(self, groupId, artifactId, version):
        """Pass artifact values to create node."""
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
