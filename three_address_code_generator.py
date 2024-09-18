class ThreeAddressCodeGenerator:
    def __init__(self, ast_root):
        self.ast_root = ast_root
        self.temp_count = 0
        self.instructions = []
        self.indentation_level = 0
    
    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def indent(self):
        return '    ' * self.indentation_level

    def generate(self):
        self.traverse(self.ast_root)
        return self.instructions

    def traverse(self, node):
        if node is None:
            return

        if node.node_type == "Programa":
            for child in node.children:
                self.traverse(child)
        elif node.node_type == "DeclaracaoVariavel":
            pass 
        elif node.node_type == "DeclaracaoFuncao":
            func_name = node.value
            self.instructions.append(f"\n{self.indent()}# Início da função '{func_name}'")
            self.instructions.append(f"{self.indent()}function {func_name} begin")
            self.indentation_level += 1
            for param in node.children[1:-1]:
                if param.node_type == "Parametro":
                    param_name = param.value
                    self.instructions.append(f"{self.indent()}param {param_name}")
            self.traverse(node.children[-1])
            self.indentation_level -= 1
            self.instructions.append(f"{self.indent()}function {func_name} end")
        elif node.node_type == "DeclaracaoProcedimento":
            proc_name = node.value
            self.instructions.append(f"\n{self.indent()}# Início do procedimento '{proc_name}'")
            self.instructions.append(f"{self.indent()}procedure {proc_name} begin")
            self.indentation_level += 1
            for param in node.children[1:-1]:
                if param.node_type == "Parametro":
                    param_name = param.value
                    self.instructions.append(f"{self.indent()}param {param_name}")
            self.traverse(node.children[-1])
            self.indentation_level -= 1
            self.instructions.append(f"{self.indent()}procedure {proc_name} end")
        elif node.node_type == "ComandoAtribuicao":
            temp = self.traverse(node.children[1])
            self.instructions.append(f"{self.indent()}{node.children[0].value} = {temp}")
        elif node.node_type == "ComandoImpressao":
            temp = self.traverse(node.children[0])
            self.instructions.append(f"{self.indent()}print {temp}")
        elif node.node_type == "ComandoLaco":
            start_label = f"L{self.temp_count}"
            self.temp_count += 1
            end_label = f"L{self.temp_count}"
            self.temp_count += 1

            self.instructions.append(f"\n{self.indent()}{start_label}:  # Início do laço 'while'")
            cond = self.traverse(node.children[0])
            self.instructions.append(f"{self.indent()}if {cond} == false goto {end_label}")
            self.traverse(node.children[1])
            self.instructions.append(f"{self.indent()}goto {start_label}")
            self.instructions.append(f"{self.indent()}{end_label}:  # Fim do laço 'while'")
        elif node.node_type == "ComandoCondicional":
            cond = self.traverse(node.children[0])
            else_label = f"L{self.temp_count}"
            self.temp_count += 1
            end_label = f"L{self.temp_count}"
            self.temp_count += 1

            self.instructions.append(f"\n{self.indent()}if {cond} == false goto {else_label}")
            self.traverse(node.children[1])
            self.instructions.append(f"{self.indent()}goto {end_label}")
            self.instructions.append(f"{self.indent()}{else_label}:  # Bloco 'else'")
            if len(node.children) == 3:
                self.traverse(node.children[2])
            self.instructions.append(f"{self.indent()}{end_label}:  # Fim do if-else")
        elif node.node_type == "ComandoBreak":
            self.instructions.append(f"{self.indent()}break")
        elif node.node_type == "ChamadaFuncao":
            args = [self.traverse(arg) for arg in node.children]
            temp = self.new_temp()
            self.instructions.append(f"{self.indent()}{temp} = call {node.value}, {', '.join(args)}")
            return temp
        elif node.node_type == "ChamadaProcedimento":
            self.instructions.append(f"\n{self.indent()}# Início da chamada de 'prc'")
            args = [self.traverse(arg) for arg in node.children]
            self.instructions.append(f"{self.indent()}call {node.value}, {', '.join(args)}")
            self.instructions.append(f"{self.indent()}# Fim da chamada de 'prc'")

        elif node.node_type == "ExpressaoBooleana":
            left = self.traverse(node.children[0])
            right = self.traverse(node.children[1])
            temp = self.new_temp()
            self.instructions.append(f"{self.indent()}{temp} = {left} {node.value} {right}")
            return temp
        elif node.node_type == "ExpressaoAritmetica" or node.node_type == "Termo":
            left = self.traverse(node.children[0])
            right = self.traverse(node.children[1])
            temp = self.new_temp()
            self.instructions.append(f"{self.indent()}{temp} = {left} {node.value} {right}")
            return temp
        elif node.node_type == "Numero":
            return node.value
        elif node.node_type == "ID":
            return node.value
        elif node.node_type == "Booleano":
            return node.value
        elif node.node_type == "String":  
            return f'"{node.value}"'  
        elif node.node_type == "ComandoRetorno":
            temp = self.traverse(node.children[0])
            self.instructions.append(f"{self.indent()}return {temp}")
        elif node.node_type == "Bloco":
            for child in node.children:
                self.traverse(child)
        elif node.node_type == "BlocoComRetorno":
            for child in node.children:
                self.traverse(child)
        else:
            raise NotImplementedError(f"Node type {node.node_type} not implemented in code generation")

if __name__ == '__main__':
    from lexer import Lexer
    from parser import Parser

    code = '''
    int x, y, inteiro, elsewhen;
    bool z;

    int soma(int a, int b) {
        int resultado;
        resultado = a + b;
        return resultado;
    }

    '''
    lexer = Lexer(code)
    lexer.tokenize()

    parser = Parser(lexer.tokens)
    try:
        ast_root = parser.parse()

        codegen = ThreeAddressCodeGenerator(ast_root)
        instructions = codegen.generate()
        for instr in instructions:
            print(instr)

    except SyntaxError as e:
        print(e)
