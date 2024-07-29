class ASTNode:
    def __init__(self, node_type, value=None, line=None):
        self.node_type = node_type
        self.value = value
        self.line = line
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"ASTNode({self.node_type}, {self.value}, {self.line}, {self.children})"
