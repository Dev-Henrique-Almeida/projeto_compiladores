class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type  
        self.value = value  
        self.children = children if children is not None else []  

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return self.pretty_print()

    def pretty_print(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.node_type}"
        if self.value:
            result += f" (value: {self.value})"
        if self.children:
            result += ":\n" + "\n".join(
                child.pretty_print(level + 1) if isinstance(child, ASTNode) else f"{indent}  {child}"
                for child in self.children
            )
        return result
