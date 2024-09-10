from lexer import Lexer
from parser import Parser

class SemanticAnalyzer:
    def __init__(self, ast_root):
        self.ast_root = ast_root
        self.symbol_table = {}  # Tabela de símbolos global
        self.current_scope = self.symbol_table  # Escopo atual
        self.current_function_type = None  # Tipo da função atual

    def analyze(self):
        self.visit(self.ast_root)

    def visit(self, node):
        method_name = f'visit_{node.node_type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_DeclaracaoVariavel(self, node):
        tipo_variavel = node.value
        for id_node in node.children:
            if id_node.value in self.current_scope:
                raise SemanticError(f"Variável '{id_node.value}' já declarada.")
            self.current_scope[id_node.value] = tipo_variavel

    def visit_DeclaracaoFuncao(self, node):
        tipo_funcao = node.children[0].value
        nome_funcao = node.value
        parametros = node.children[1:-1]
        corpo = node.children[-1]

        if nome_funcao in self.symbol_table:
            raise SemanticError(f"Função '{nome_funcao}' já declarada.")

        self.symbol_table[nome_funcao] = {
            'type': tipo_funcao,
            'params': [(param.children[0].value, param.value) for param in parametros]
        }

        # Novo escopo para a função
        self.current_scope = {}
        for param in parametros:
            self.current_scope[param.value] = param.children[0].value

        # Atualiza o tipo da função atual
        self.current_function_type = tipo_funcao

        self.visit(corpo)

        # Volta ao escopo global e reseta o tipo da função atual
        self.current_scope = self.symbol_table
        self.current_function_type = None

    def visit_DeclaracaoProcedimento(self, node):
        nome_procedimento = node.value
        parametros = node.children[:-1]
        corpo = node.children[-1]

        if nome_procedimento in self.symbol_table:
            raise SemanticError(f"Procedimento '{nome_procedimento}' já declarado.")

        self.symbol_table[nome_procedimento] = {
            'type': 'void',
            'params': [(param.children[0].value, param.value) for param in parametros]
        }

        # Novo escopo para o procedimento
        self.current_scope = {}
        for param in parametros:
            self.current_scope[param.value] = param.children[0].value

        # Atualiza o tipo do procedimento atual
        self.current_function_type = 'void'

        self.visit(corpo)

        # Volta ao escopo global e reseta o tipo do procedimento atual
        self.current_scope = self.symbol_table
        self.current_function_type = None

    def visit_ComandoAtribuicao(self, node):
        id_node = node.children[0]
        expressao_node = node.children[1]

        if id_node.value not in self.current_scope:
            raise SemanticError(f"Variável '{id_node.value}' não declarada.")

        tipo_variavel = self.current_scope[id_node.value].value.lower()
        tipo_expressao = self.visit(expressao_node)

        if tipo_variavel != tipo_expressao:
            raise SemanticError(f"Tipo incompatível na atribuição para '{id_node.value}'.")

    def visit_ChamadaFuncaoOuProcedimento(self, node):
        nome = node.value
        argumentos = node.children

        if nome not in self.symbol_table:
            raise SemanticError(f"Função ou procedimento '{nome}' não declarado.")

        func_info = self.symbol_table[nome]
        if len(argumentos) != len(func_info['params']):
            raise SemanticError(f"Número incorreto de argumentos para '{nome}'.")

        for arg, (param_type, param_name) in zip(argumentos, func_info['params']):
            tipo_argumento = self.visit(arg)
            if tipo_argumento != param_type:
                raise SemanticError(f"Tipo do argumento '{param_name}' incompatível na chamada de '{nome}'.")

    def visit_ComandoCondicional(self, node):
        condicao = node.children[0]
        bloco_then = node.children[1]
        bloco_else = node.children[2] if len(node.children) > 2 else None

        tipo_condicao = self.visit(condicao)
        if tipo_condicao != 'bool':
            raise SemanticError("Condição do 'if' deve ser uma expressão booleana.")

        self.visit(bloco_then)
        if bloco_else:
            self.visit(bloco_else)

    def visit_ComandoLaco(self, node):
        condicao = node.children[0]
        bloco_laco = node.children[1]

        tipo_condicao = self.visit(condicao)
        if tipo_condicao != 'bool':
            raise SemanticError("Condição do 'while' deve ser uma expressão booleana.")

        self.visit(bloco_laco)

    def visit_ComandoImpressao(self, node):
        expressao = node.children[0]
        self.visit(expressao)

    def visit_ComandoRetorno(self, node):
        expressao_retorno = node.children[0]
        tipo_retorno = self.visit(expressao_retorno)
        
        if hasattr(tipo_retorno, 'value'):
            tipo_retorno = tipo_retorno.value

        if tipo_retorno != self.current_function_type:
            raise SemanticError(f"Tipo de retorno incompatível. Esperado '{self.current_function_type}', encontrado '{tipo_retorno}'.")

    def visit_ComandoBreak(self, node):
        pass  # 'break' não precisa de verificação semântica adicional

    def visit_Expressao(self, node):
        return self.visit(node.children[0])

    def visit_ExpressaoBooleana(self, node):
        esquerda = self.visit(node.children[0])
        direita = self.visit(node.children[1])

        if esquerda != direita:
            raise SemanticError("Operação booleana entre tipos incompatíveis.")

        return 'bool'

    def visit_ExpressaoAritmetica(self, node):
        esquerda = self.visit(node.children[0])
        direita = self.visit(node.children[1])

        print("Node:", node)
        print("ESQUERDA", esquerda)
        print("DIREITA", direita)

        if hasattr(esquerda, 'value'):
            esquerda = esquerda.value

        if hasattr(direita, 'value'):
            direita = direita.value

        if esquerda.lower() != 'int' or direita.lower() != 'int':
            raise SemanticError("Operação aritmética entre tipos incompatíveis.")

        return 'int'

    def visit_Termo(self, node):
        return self.visit(node.children[0])

    def visit_ID(self, node):
        if node.value not in self.current_scope:
            raise SemanticError(f"Variável '{node.value}' não declarada.")
        return self.current_scope[node.value]

    def visit_Numero(self, node):
        return 'int'

    def visit_String(self, node):
        return 'string'

    def visit_Booleano(self, node):
        return 'bool'

class SemanticError(Exception):
    pass

if __name__ == '__main__':
    code = '''
    int x, y, inteiro, elsewhen;
    bool z;

    int a;
    a = 10;
    
    int b;
    b = 1 + 2;

    z = false;

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
        print(ast_root) 

        semantic_analyzer = SemanticAnalyzer(ast_root)
        semantic_analyzer.analyze()
        print("Análise semântica concluída com sucesso.")
    except (SyntaxError, SemanticError) as e:
        print(e)