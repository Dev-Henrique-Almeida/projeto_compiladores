from ast_node import ASTNode  
class SemanticAnalyzer:
    def __init__(self, ast_root, symbol_table):
        self.ast_root = ast_root  
        self.symbol_table = symbol_table
        self.errors = []

    def analyze(self):
        print("Iniciando a análise semântica...")  
        self.visit(self.ast_root) 

        if self.errors:
            print("Erros Semânticos:")
            for error in self.errors:
                print(error)
        else:
            print("Análise Semântica concluída sem erros.")

    def visit(self, node):
        if not isinstance(node, ASTNode):
            return  

        if node.value:
            print(f"- {node.node_type} com valor: {node.value}")
        else:
            print(f"- {node.node_type} ")

        if node.node_type == "variable_declaration":
            self.declare_variable(node)
        elif node.node_type == "function_declaration":
            self.declare_function(node)
        elif node.node_type == "assignment":
            self.check_assignment(node)

        for child in node.children:
            self.visit(child)

    def declare_variable(self, node):
        var_name = node.value
        var_type = node.children[0].value 

        print(f"Declarando variável '{var_name}' com tipo '{var_type}'")

        if var_name in self.symbol_table:
            self.errors.append(f"Erro: Variável '{var_name}' já foi declarada.")
        else:
            self.symbol_table[var_name] = {"type": var_type, "scope": "local"}

    def declare_function(self, node):
        func_name = node.value
        func_type = node.children[0].value  
        params = node.children[1].children  

        print(f"Declarando função '{func_name}' com tipo '{func_type}'")

        if func_name in self.symbol_table:
            self.errors.append(f"Erro: Função '{func_name}' já foi declarada.")
        else:
            self.symbol_table[func_name] = {"type": func_type, "parameters": []}

        for param in params:
            param_name = param.value
            param_type = param.children[0].value
            print(f"Registrando parâmetro '{param_name}' com tipo '{param_type}'")

            self.symbol_table[func_name]["parameters"].append({"name": param_name, "type": param_type})

    def check_assignment(self, node):
        var_name = node.children[0].value  
        assigned_value = node.children[1].value  

        print(f"Atribuindo valor '{assigned_value}' à variável '{var_name}'")

        if var_name not in self.symbol_table:
            self.errors.append(f"Erro: Variável '{var_name}' não foi declarada.")
        else:
            var_type = self.symbol_table[var_name]["type"]
            if var_type == "int" and not isinstance(assigned_value, int):
                self.errors.append(f"Erro: Atribuição inválida para a variável '{var_name}' do tipo 'int'.")
            elif var_type == "bool" and assigned_value not in ["TRUE", "FALSE"]:
                self.errors.append(f"Erro: Atribuição inválida para a variável '{var_name}' do tipo 'bool'.")
