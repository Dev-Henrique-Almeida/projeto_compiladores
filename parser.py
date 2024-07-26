from lexer import Lexer, Token
from typing import List
from ASTNode import ASTNode

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.parsing_steps = []
        self.root = None

    def parse(self):
        self.parsing_steps.append("Iniciando a análise sintática...")
        self.root = self.programa()
        self.parsing_steps.append("Análise sintática concluída com sucesso!")
        return self.root

    def eat(self, token_type):
        current_token = self.current_token()
        if current_token.token_type == token_type:
            self.parsing_steps.append(f"Consumindo token: {current_token}")
            self.current_token_index += 1
            return current_token
        else:
            raise SyntaxError(f"Esperado token {token_type}, mas encontrado {current_token.token_type} na linha {current_token.line}")

    def current_token(self):
        return self.tokens[self.current_token_index]

    def programa(self):
        self.parsing_steps.append("Analisando programa...")
        programa_node = ASTNode("programa")
        while self.current_token_index < len(self.tokens):
            programa_node.add_child(self.declaracao_comando())
        return programa_node

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
                raise SyntaxError(f"Token inesperado {token_type} na linha {self.current_token().line}")
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
            raise SyntaxError(f"Token inesperado {token_type} na linha {self.current_token().line}")

    def declaracao_variaveis(self):
        self.parsing_steps.append("Analisando declaração de variáveis...")
        node = ASTNode("declaracao_variaveis")
        node.add_child(self.tipo())
        node.add_child(self.lista_identificadores())
        self.eat("SEMICOLON")
        return node

    def tipo(self):
        token_type = self.current_token().token_type
        if token_type in ["INT", "BOOL"]:
            self.parsing_steps.append(f"Tipo encontrado: {token_type}")
            token = self.eat(token_type)
            return ASTNode("tipo", token.value)
        else:
            raise SyntaxError(f"Tipo de variável inválido: {self.current_token().value}")

    def lista_identificadores(self):
        self.parsing_steps.append("Analisando lista de identificadores...")
        node = ASTNode("lista_identificadores")
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            node.add_child(ASTNode("identificador", self.eat("ID").value))
        return node

    def declaracao_procedimento(self):
        self.parsing_steps.append("Analisando declaração de procedimento...")
        node = ASTNode("declaracao_procedimento")
        self.eat("VOID")
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            node.add_child(self.lista_parametros())
        self.eat("RPAREN")
        node.add_child(self.bloco())
        return node

    def declaracao_funcao(self):
        self.parsing_steps.append("Analisando declaração de função...")
        node = ASTNode("declaracao_funcao")
        node.add_child(self.tipo())
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            node.add_child(self.lista_parametros())
        self.eat("RPAREN")
        node.add_child(self.bloco_retorno())
        return node

    def lista_parametros(self):
        self.parsing_steps.append("Analisando lista de parâmetros...")
        node = ASTNode("lista_parametros")
        node.add_child(self.parametro())
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            node.add_child(self.parametro())
        return node

    def parametro(self):
        self.parsing_steps.append("Analisando parâmetro...")
        node = ASTNode("parametro")
        node.add_child(self.tipo())
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        return node

    def bloco(self):
        self.parsing_steps.append("Analisando bloco...")
        node = ASTNode("bloco")
        self.eat("LBRACE")
        while self.current_token().token_type != "RBRACE":
            node.add_child(self.declaracao_comando())
        self.eat("RBRACE")
        return node

    def bloco_retorno(self):
        self.parsing_steps.append("Analisando bloco com retorno...")
        node = ASTNode("bloco_retorno")
        self.eat("LBRACE")
        while self.current_token().token_type != "RBRACE":
            if self.current_token().token_type == "RETURN":
                node.add_child(self.comando_retorno())
            else:
                node.add_child(self.declaracao_comando())
        self.eat("RBRACE")
        return node

    def comando_atribuicao(self):
        self.parsing_steps.append("Analisando comando de atribuição...")
        node = ASTNode("comando_atribuicao")
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        self.eat("ASSIGN")
        node.add_child(self.expressao())
        self.eat("SEMICOLON")
        return node

    def chamada_funcao_ou_procedimento(self):
        self.parsing_steps.append("Analisando chamada de função ou procedimento...")
        node = ASTNode("chamada_funcao_ou_procedimento")
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            node.add_child(self.lista_argumentos())
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        return node

    def chamada_procedimento(self):
        self.parsing_steps.append("Analisando chamada de procedimento...")
        node = ASTNode("chamada_procedimento")
        self.eat("PRC")
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            node.add_child(self.lista_argumentos())
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        return node

    def chamada_funcao(self):
        self.parsing_steps.append("Analisando chamada de função...")
        node = ASTNode("chamada_funcao")
        self.eat("FUN")
        node.add_child(ASTNode("identificador", self.eat("ID").value))
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            node.add_child(self.lista_argumentos())
        self.eat("RPAREN")
        return node

    def lista_argumentos(self):
        self.parsing_steps.append("Analisando lista de argumentos...")
        node = ASTNode("lista_argumentos")
        node.add_child(self.expressao())
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            node.add_child(self.expressao())
        return node

    def comando_condicional(self):
        self.parsing_steps.append("Analisando comando condicional...")
        node = ASTNode("comando_condicional")
        self.eat("IF")
        self.eat("LPAREN")
        node.add_child(self.expressao_booleana())
        self.eat("RPAREN")
        node.add_child(self.bloco())
        if self.current_token().token_type == "ELSE":
            self.eat("ELSE")
            node.add_child(self.bloco())
        return node

    def comando_laco(self):
        self.parsing_steps.append("Analisando comando de laço...")
        node = ASTNode("comando_laco")
        self.eat("WHILE")
        self.eat("LPAREN")
        node.add_child(self.expressao_booleana())
        self.eat("RPAREN")
        node.add_child(self.bloco())
        return node

    def comando_impressao(self):
        self.parsing_steps.append("Analisando comando de impressão...")
        node = ASTNode("comando_impressao")
        self.eat("PRINT")
        self.eat("LPAREN")
        node.add_child(self.expressao())
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        return node

    def comando_retorno(self):
        self.parsing_steps.append("Analisando comando de retorno...")
        node = ASTNode("comando_retorno")
        self.eat("RETURN")
        node.add_child(self.expressao())
        self.eat("SEMICOLON")
        return node

    def comando_break(self):
        self.parsing_steps.append("Analisando comando de break...")
        node = ASTNode("comando_break")
        self.eat("BREAK")
        self.eat("SEMICOLON")
        return node

    def expressao(self):
        return self.expressao_booleana()

    def expressao_booleana(self):
        node = ASTNode("expressao_booleana")
        node.add_child(self.expressao_aritmetica())
        while self.current_token().token_type in ["EQ", "NE", "GT", "GE", "LT", "LE"]:
            operator_node = ASTNode(self.eat(self.current_token().token_type).token_type)
            operator_node.add_child(self.expressao_aritmetica())
            node.add_child(operator_node)
        return node

    def expressao_aritmetica(self):
        node = ASTNode("expressao_aritmetica")
        node.add_child(self.termo())
        while self.current_token().token_type in ["PLUS", "MINUS"]:
            operator_node = ASTNode(self.eat(self.current_token().token_type).token_type)
            operator_node.add_child(self.termo())
            node.add_child(operator_node)
        return node

    def termo(self):
        node = ASTNode("termo")
        node.add_child(self.fator())
        while self.current_token().token_type in ["TIMES", "DIVIDE"]:
            operator_node = ASTNode(self.eat(self.current_token().token_type).token_type)
            operator_node.add_child(self.fator())
            node.add_child(operator_node)
        return node

    def fator(self):
        current_token = self.current_token()
        if current_token.token_type == "ID":
            return ASTNode("identificador", self.eat("ID").value)
        elif current_token.token_type == "NUMBER":
            return ASTNode("numero", self.eat("NUMBER").value)
        elif current_token.token_type in ["TRUE", "FALSE"]:
            return ASTNode("booleano", self.eat(current_token.token_type).value)
        elif current_token.token_type == "LPAREN":
            self.eat("LPAREN")
            expr_node = self.expressao()
            self.eat("RPAREN")
            return expr_node
        elif current_token.token_type == "FUN":
            return self.chamada_funcao()
        else:
            raise SyntaxError(f"Fator inválido: {self.current_token().value}")

    def print_parsing_steps(self):
        print("Etapas da análise sintática:")
        for step in self.parsing_steps:
            print(step)

    def print_ast(self, node, level=0):
        indent = "  " * level
        print(f"{indent}{node.node_type}: {node.value if node.value else ''}")
        for child in node.children:
            self.print_ast(child, level + 1)
