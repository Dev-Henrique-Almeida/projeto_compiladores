from lexer import Lexer, Token
from typing import List
from ast_node import ASTNode  

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_index = 0  
        self.parsing_steps = []  
        self.current_function_type = None  

    def parse(self):
        ast_root = ASTNode("Programa")
        while self.current_token_index < len(self.tokens): 
            ast_root.add_child(self.declaracao_comando())  
        return ast_root

    def eat(self, token_type):
        current_token = self.current_token()
        if current_token.token_type == token_type:
            self.parsing_steps.append(f"Consumindo token: {current_token}")
            self.current_token_index += 1
            return current_token
        else:
            raise SyntaxError(f"Esperado token {token_type}, mas encontrado {current_token.token_type} `{current_token.value}` na linha {current_token.line}")

    def current_token(self):
        return self.tokens[self.current_token_index]

    def declaracao_comando(self):
        token_type = self.current_token().token_type
        self.parsing_steps.append(f"Analisando declaração/comando: {token_type}")
        if token_type in ["INT", "BOOL"]:
            if self.tokens[self.current_token_index + 2].token_type == "LPAREN":
                return self.declaracao_funcao()
            else:
                return self.declaracao_variaveis()
        elif token_type == "VOID":
            return self.declaracao_procedimento()
        elif token_type == "ID":
            if self.tokens[self.current_token_index + 1].token_type == "ASSIGN":
                return self.comando_atribuicao()
            elif self.tokens[self.current_token_index + 1].token_type == "LPAREN":
                return self.chamada_funcao_ou_procedimento()
            else:
                raise SyntaxError(f"Token inesperado `{token_type}`, esperado (INT, BOOL ou VOID) na linha {self.current_token().line}")
        elif token_type == "PRC":
            return self.chamada_procedimento()
        elif token_type == "FUN":
            return self.chamada_funcao()
        elif token_type == "IF":
            return self.comando_condicional()
        elif token_type == "WHILE":
            return self.comando_laco()
        elif token_type == "PRINT":
            return self.comando_impressao()
        elif token_type == "BREAK":
            return self.comando_break()
        elif token_type == "RETURN":
            return self.comando_retorno()
        else:
            raise SyntaxError(f"Token inesperado {token_type}, esperado (PRC, FUN, IF, WHILE, PRINT, BREAK ou RETURN) na linha {self.current_token().line}")

    def declaracao_variaveis(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando declaração de variáveis...")
        
        tipo_variavel = self.tipo() 
        identificadores = self.lista_identificadores() 
        
        self.eat("SEMICOLON")  
        self.parsing_steps.append("}")
        
        return ASTNode("DeclaracaoVariavel", value=tipo_variavel, children=identificadores)

    def tipo(self):
        token_type = self.current_token().token_type
        if token_type in ["INT", "BOOL"]:
            self.parsing_steps.append(f"Tipo encontrado: {token_type}")
            self.eat(token_type)
            return ASTNode("Tipo", value=token_type) 
        else:
            raise SyntaxError(f"Tipo de variável inválido: '{self.current_token().value}' na linha {self.current_token().line}. Esperado INT ou BOOL.")

    def lista_identificadores(self):
        self.parsing_steps.append("Analisando lista de identificadores...")
        
        ids = [ASTNode("ID", value=self.current_token().value)]  
        self.eat("ID")
        
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA") 
            ids.append(ASTNode("ID", value=self.current_token().value))  
            self.eat("ID")  
        
        return ids  

    def declaracao_procedimento(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando declaração de procedimento...")
        
        self.eat("VOID")
        nome_procedimento = self.eat("ID").value  
        self.eat("LPAREN")
        
        parametros = []
        if self.current_token().token_type != "RPAREN":
            parametros = self.lista_parametros()  
        
        self.eat("RPAREN")
        corpo = self.bloco()
        
        self.current_function_type = None
        self.parsing_steps.append("}")
        
        return ASTNode("DeclaracaoProcedimento", value=nome_procedimento, children=parametros + [corpo])

    def declaracao_funcao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando declaração de função...")
        
        tipo_funcao = self.tipo()  
        nome_funcao = self.eat("ID").value 
        self.eat("LPAREN")
        
        parametros = []
        if self.current_token().token_type != "RPAREN":
            parametros = self.lista_parametros()  
        
        self.eat("RPAREN")
        corpo = self.bloco_retorno()  
        
        self.current_function_type = None
        self.parsing_steps.append("}")
        
        return ASTNode("DeclaracaoFuncao", value=nome_funcao, children=[tipo_funcao] + parametros + [corpo])

    def lista_parametros(self):
        self.parsing_steps.append("Analisando lista de parâmetros...")
        
        parametros = [self.parametro()]  
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            parametros.append(self.parametro()) 
        
        return parametros

    def parametro(self):
        self.parsing_steps.append("Analisando parâmetro...")
        tipo_parametro = self.tipo()
        nome_parametro = self.eat("ID").value
        return ASTNode("Parametro", value=nome_parametro, children=[tipo_parametro])

    def bloco(self):
        self.parsing_steps.append("Analisando bloco...")
        self.eat("LBRACE")  
        
        comandos = []
        while self.current_token().token_type != "RBRACE":
            comandos.append(self.declaracao_comando()) 
        
        self.eat("RBRACE")  
        
        return ASTNode("Bloco", children=comandos)

    def bloco_retorno(self):
        self.parsing_steps.append("Analisando bloco com retorno...")
        self.eat("LBRACE")
        
        has_return = False
        comandos = []
        while self.current_token().token_type != "RBRACE":
            if self.current_token().token_type == "RETURN":
                has_return = True
                comandos.append(self.comando_retorno()) 
            else:
                comandos.append(self.declaracao_comando())  
        
        self.eat("RBRACE")
        
        if self.current_function_type in ["INT", "BOOL"] and not has_return:
            raise SyntaxError(f"Função do tipo {self.current_function_type} deve ter um comando 'return'.")
        
        return ASTNode("BlocoComRetorno", children=comandos)

    def comando_atribuicao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de atribuição...")
        
        identificador = ASTNode("ID", value=self.eat("ID").value)  
        self.eat("ASSIGN")  
        expressao = self.expressao()  
        
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")
        
        return ASTNode("ComandoAtribuicao", children=[identificador, expressao])

    def chamada_funcao_ou_procedimento(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando chamada de função ou procedimento...")
        
        nome = self.eat("ID").value
        self.eat("LPAREN")
        
        argumentos = []
        if self.current_token().token_type != "RPAREN":
            argumentos = self.lista_argumentos()
        
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")
        
        return ASTNode("ChamadaFuncaoOuProcedimento", value=nome, children=argumentos)

    def chamada_procedimento(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando chamada de procedimento...")
        self.eat("PRC")
        nome_procedimento = self.eat("ID").value
        self.eat("LPAREN")
        
        argumentos = []
        if self.current_token().token_type != "RPAREN":
            argumentos = self.lista_argumentos()
        
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")
        
        return ASTNode("ChamadaProcedimento", value=nome_procedimento, children=argumentos)

    def chamada_funcao(self):
        self.parsing_steps.append("Analisando chamada de função com 'fun'...")
        
        nome_funcao = self.eat("ID").value
        self.eat("LPAREN") 

        argumentos = []
        if self.current_token().token_type != "RPAREN":
            argumentos = self.lista_argumentos()

        self.eat("RPAREN")
        self.parsing_steps.append("}")
        
        return ASTNode("ChamadaFuncao", value=nome_funcao, children=argumentos)

    def lista_argumentos(self):
        self.parsing_steps.append("Analisando lista de argumentos...")
        argumentos = [self.expressao()]
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            argumentos.append(self.expressao())
        return argumentos

    def comando_condicional(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando condicional...")
        self.eat("IF")
        self.eat("LPAREN")
        condicao = self.expressao_booleana()  
        self.eat("RPAREN")
        bloco_then = self.bloco()  
        
        bloco_else = None
        if self.current_token().token_type == "ELSE":
            self.eat("ELSE")
            bloco_else = self.bloco() 
        
        self.parsing_steps.append("}")
        return ASTNode("ComandoCondicional", children=[condicao, bloco_then, bloco_else])

    def comando_laco(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de laço...")
        self.eat("WHILE")
        self.eat("LPAREN")
        condicao = self.expressao_booleana()
        self.eat("RPAREN")
        bloco_laco = self.bloco()
        self.parsing_steps.append("}")
        
        return ASTNode("ComandoLaco", children=[condicao, bloco_laco])

    def comando_impressao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de impressão...")
        self.eat("PRINT")
        self.eat("LPAREN")
        expressao_impressao = self.expressao()
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")
        
        return ASTNode("ComandoImpressao", children=[expressao_impressao])

    def comando_retorno(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de retorno...")
        self.eat("RETURN")
        expressao_retorno = self.expressao()
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")
        
        return ASTNode("ComandoRetorno", children=[expressao_retorno])

    def comando_break(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de break...")
        self.eat("BREAK")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")
        
        return ASTNode("ComandoBreak")

    def expressao(self):
        return self.expressao_booleana()

    def expressao_booleana(self):
        esquerda = self.expressao_aritmetica() 
        while self.current_token().token_type in ["EQ", "NE", "GT", "GE", "LT", "LE"]:
            operador = self.eat(self.current_token().token_type).value
            direita = self.expressao_aritmetica()  
            esquerda = ASTNode("ExpressaoBooleana", value=operador, children=[esquerda, direita])
        return esquerda

    def expressao_aritmetica(self):
        esquerda = self.termo()
        while self.current_token().token_type in ["PLUS", "MINUS"]:
            operador = self.eat(self.current_token().token_type).value
            direita = self.termo()
            esquerda = ASTNode("ExpressaoAritmetica", value=operador, children=[esquerda, direita])
        return esquerda

    def termo(self):
        esquerda = self.fator()
        while self.current_token().token_type in ["TIMES", "DIVIDE"]:
            operador = self.eat(self.current_token().token_type).value
            direita = self.fator()
            esquerda = ASTNode("Termo", value=operador, children=[esquerda, direita])
        return esquerda

    def fator(self):
        current_token = self.current_token()
        
        if current_token.token_type == "FUN":
            self.eat("FUN")
            return self.chamada_funcao()
        
        elif current_token.token_type == "ID":
            return ASTNode("ID", value=self.eat("ID").value)
        
        elif current_token.token_type == "NUMBER":
            return ASTNode("Numero", value=self.eat("NUMBER").value)
        
        elif current_token.token_type == "STRING":  
            return ASTNode("String", value=self.eat("STRING").value)
        
        elif current_token.token_type in ["TRUE", "FALSE"]:
            return ASTNode("Booleano", value=self.eat(current_token.token_type).value)
        
        elif current_token.token_type == "LPAREN":
            self.eat("LPAREN")
            expressao = self.expressao()
            self.eat("RPAREN")
            return expressao
        
        else:
            raise SyntaxError(f"Esperado valor (ID, NUMBER, TRUE, FALSE, STRING ou expressão), mas encontrado {self.current_token().token_type} `{self.current_token().value}` na linha {current_token.line}")

if __name__ == '__main__':
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
        print(ast_root) 
    except SyntaxError as e:
        print(e)
