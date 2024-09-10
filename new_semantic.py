from lexer import Lexer
from parser import Parser

class SemanticAnalyzer:
    def __init__(self, ast_root, symbol_table):
        self.ast_root = ast_root
        self.symbol_table = symbol_table  # Tabela de símbolos global
        self.current_scope = self.symbol_table  # Escopo atual
        self.current_function_type = None  # Tipo da função atual
        self.errors = []

    def analyze(self):
        self.visit(self.ast_root)

        if self.errors:
            print("Erros Semânticos:")
            for error in self.errors:
                print(error)
        else:
            print("Análise Semântica concluída sem erros.")

    def visit(self, node):
        print(f"- {node.node_type} com valor: {node.value}")
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
                self.errors.append(f"Erro: Variável '{id_node.value}' já declarada.")
            else:
                self.current_scope[id_node.value] = tipo_variavel

    def visit_DeclaracaoFuncao(self, node):
        tipo_funcao = node.children[0].value
        nome_funcao = node.value
        parametros = node.children[1:-1]
        corpo = node.children[-1]

        if nome_funcao in self.symbol_table:
            self.errors.append(f"Erro: Função '{nome_funcao}' já declarada.")
        else:
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
            self.errors.append(f"Erro: Procedimento '{nome_procedimento}' já declarado.")
        else:
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
            self.errors.append(f"Erro: Variável '{id_node.value}' não declarada.")
        else:
            tipo_variavel = self.current_scope[id_node.value]
            tipo_expressao = self.visit(expressao_node)

            if hasattr(tipo_variavel, 'value'):
                tipo_variavel = tipo_variavel.value

            if hasattr(tipo_expressao, 'value'):
                tipo_expressao = tipo_expressao.value

            if tipo_variavel.lower() != tipo_expressao.lower():
                self.errors.append(f"Erro: Tipo incompatível na atribuição para '{id_node.value}'.")

    def visit_ChamadaFuncao(self, node):
        nome = node.value
        argumentos = node.children

        if nome not in self.symbol_table:
            self.errors.append(f"Erro: Função '{nome}' não declarada.")
        else:
            func_info = self.symbol_table[nome]
            if len(argumentos) != len(func_info['params']):
                self.errors.append(f"Erro: Número incorreto de argumentos para '{nome}'.")
            else:
                for arg, (param_type, param_name) in zip(argumentos, func_info['params']):
                    tipo_argumento = self.visit(arg)

                    if hasattr(tipo_argumento, 'value'):
                        tipo_argumento = tipo_argumento.value

                    if hasattr(param_type, 'value'):
                        param_type = param_type.value 

                    if tipo_argumento.lower() != param_type.lower():
                        self.errors.append(f"Erro: Tipo do argumento '{param_name}' incompatível na chamada de '{nome}'.")

                return func_info['type']  # Retorna o tipo da função chamada

    def visit_ChamadaProcedimento(self, node):
        nome = node.value
        argumentos = node.children

        if nome not in self.symbol_table:
            self.errors.append(f"Erro: Procedimento '{nome}' não declarado.")
        else:
            proc_info = self.symbol_table[nome]
            if len(argumentos) != len(proc_info['params']):
                self.errors.append(f"Erro: Número incorreto de argumentos para '{nome}'.")
            else:
                for arg, (param_type, param_name) in zip(argumentos, proc_info['params']):
                    tipo_argumento = self.visit(arg)

                    if hasattr(tipo_argumento, 'value'):
                        tipo_argumento = tipo_argumento.value

                    if hasattr(param_type, 'value'):
                        param_type = param_type.value 
                        
                    if tipo_argumento.lower() != param_type.lower():
                        self.errors.append(f"Erro: Tipo do argumento '{param_name}' incompatível na chamada de '{nome}'.")

                return proc_info['type']  # Retorna o tipo do procedimento chamado

    def visit_ComandoCondicional(self, node):
        condicao = node.children[0]
        bloco_then = node.children[1]
        bloco_else = node.children[2] if len(node.children) > 2 else None

        tipo_condicao = self.visit(condicao)
        if tipo_condicao != 'bool':
            self.errors.append("Erro: Condição do 'if' deve ser uma expressão booleana.")
        else:
            self.visit(bloco_then)
            if bloco_else:
                self.visit(bloco_else)

    def visit_ComandoLaco(self, node):
        condicao = node.children[0]
        bloco_laco = node.children[1]

        tipo_condicao = self.visit(condicao)
        if tipo_condicao != 'bool':
            self.errors.append("Erro: Condição do 'while' deve ser uma expressão booleana.")
        else:
            self.visit(bloco_laco)

    def visit_ComandoImpressao(self, node):
        expressao = node.children[0]
        self.visit(expressao)

    def visit_ComandoRetorno(self, node):
        expressao_retorno = node.children[0]
        tipo_retorno = self.visit(expressao_retorno)
        
        if hasattr(tipo_retorno, 'value'):
            tipo_retorno = tipo_retorno.value

        if tipo_retorno.lower() != self.current_function_type.lower():
            self.errors.append(f"Erro: Tipo de retorno incompatível. Esperado '{self.current_function_type}', encontrado '{tipo_retorno}'.")

    def visit_ComandoBreak(self, node):
        pass  # 'break' não precisa de verificação semântica adicional

    def visit_Expressao(self, node):
        return self.visit(node.children[0])

    def visit_ExpressaoBooleana(self, node):
        esquerda = self.visit(node.children[0])
        direita = self.visit(node.children[1])

        if hasattr(esquerda, 'value'):
            esquerda = esquerda.value

        if hasattr(direita, 'value'):
            direita = direita.value

        if esquerda.lower() != direita.lower():
            self.errors.append("Erro: Operação booleana entre tipos incompatíveis.")
        else:
            return 'bool'

    def visit_ExpressaoAritmetica(self, node):
        esquerda = self.visit(node.children[0])
        direita = self.visit(node.children[1])

        if hasattr(esquerda, 'value'):
            esquerda = esquerda.value

        if hasattr(direita, 'value'):
            direita = direita.value

        if esquerda.lower() != 'int' or direita.lower() != 'int':
            self.errors.append("Erro: Operação aritmética entre tipos incompatíveis.")
        else:
            return 'int'

    def visit_Termo(self, node):
        return self.visit(node.children[0])

    def visit_ID(self, node):
        if node.value not in self.current_scope:
            self.errors.append(f"Erro: Variável '{node.value}' não declarada.")
        else:
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

    bool atribui () {
        return true;
    }

    if(z == false){
        print("hehe");
    }
    
    void procedimento ( int a, int b) {
        int c, d, e, f;
        c = a + 1 / 1 * 2;
        print(c);
    }

    prc procedimento(a, b);

    int res;

    print(1);

    res = fun soma(1, 2);
    
    bool resp, c;

    resp = fun atribui();


    if (c == true) {
        b = fun soma(1, 2);
        print(b);
    } else {
        print(a);
    }

    int g, h;
    bool i;

    a = 1;

    c = true;

    int funcao ( int a) {
        int c;
        c = a + 1;
        return c;
    }

    while (c == true){
        b = b + 1;
        
        if (b <= 5) {
            break;
        }
    }

    prc procedimento(a, b);

    if (c == true) {
        b = fun funcao(1);

        print(b);
    }
    else {
        print(a);
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