# Importações necessárias
from lexer import Lexer, Token
from typing import List

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_index = 0  
        self.parsing_steps = []  

    def parse(self):
        while self.current_token_index < len(self.tokens): 
            self.declaracao_comando() 
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
                self.declaracao_funcao() 
            else:
                self.declaracao_variaveis() 
        elif token_type == "VOID":
            self.declaracao_procedimento()  
        elif token_type == "ID":
            if self.tokens[self.current_token_index + 1].token_type == "ASSIGN":
                self.comando_atribuicao() 
            elif self.tokens[self.current_token_index + 1].token_type == "LPAREN":
                self.chamada_funcao_ou_procedimento() 
            else:
                raise SyntaxError(f"Token inesperado {token_type}, esperado (INT, BOOL ou VOID) na linha {self.current_token().line}")
        elif token_type == "PRC":
            self.chamada_procedimento()  
        elif token_type == "FUN":
            self.chamada_funcao() 
        elif token_type == "IF":
            self.comando_condicional()  
        elif token_type == "WHILE":
            self.comando_laco()  
        elif token_type == "PRINT":
            self.comando_impressao()  
        elif token_type == "BREAK":
            self.comando_break() 
        elif token_type == "RETURN":
            self.comando_retorno() 
        else:
            raise SyntaxError(f"Token inesperado {token_type}, esperado (PRC, FUN, IF, WHILE, PRINT, BREAK ou RETURN) na linha {self.current_token().line}")

    def declaracao_variaveis(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando declaração de variáveis...")
        self.tipo() 
        self.lista_identificadores()   
        self.eat("SEMICOLON")  
        self.parsing_steps.append("}")

    def tipo(self):
        
        token_type = self.current_token().token_type
        if token_type in ["INT", "BOOL"]:
            self.parsing_steps.append(f"Tipo encontrado: {token_type}")
            self.eat(token_type)
        else:
            raise SyntaxError(f"Tipo de variável inválido: {self.current_token().value} na linha {self.current_token().line}")

    def lista_identificadores(self):
     
        self.parsing_steps.append("Analisando lista de identificadores...")
        self.eat("ID")   
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")  
            self.eat("ID")  

    def declaracao_procedimento(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando declaração de procedimento...")
        self.eat("VOID")
        self.eat("ID")  
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            self.lista_parametros()  
        self.eat("RPAREN")
        self.bloco() 
        self.parsing_steps.append("}")

    def declaracao_funcao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando declaração de função...")
        self.tipo()  
        self.eat("ID") 
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            self.lista_parametros() 
        self.eat("RPAREN")
        self.bloco_retorno()
        self.parsing_steps.append("}")

    def lista_parametros(self):
        self.parsing_steps.append("Analisando lista de parâmetros...")
        self.parametro()  
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            self.parametro()  

    def parametro(self):
        self.parsing_steps.append("Analisando parâmetro...")
        self.tipo() 
        self.eat("ID") 

    def bloco(self):
        self.parsing_steps.append("Analisando bloco...")
        self.eat("LBRACE") 
        while self.current_token().token_type != "RBRACE":
            self.declaracao_comando()  
        self.eat("RBRACE")  

    def bloco_retorno(self):
        self.parsing_steps.append("Analisando bloco com retorno...")
        self.eat("LBRACE")
        while self.current_token().token_type != "RBRACE":
            if self.current_token().token_type == "RETURN":
                self.comando_retorno()  
            else:
                self.declaracao_comando()  
        self.eat("RBRACE")

    def comando_atribuicao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de atribuição...")
        self.eat("ID")  
        self.eat("ASSIGN")
        self.expressao()  
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")

    def chamada_funcao_ou_procedimento(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando chamada de função ou procedimento...")
        self.eat("ID")  
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            self.lista_argumentos() 
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")

    def chamada_procedimento(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando chamada de procedimento...")
        self.eat("PRC")
        self.eat("ID") 
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            self.lista_argumentos() 
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")

    def chamada_funcao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando chamada de função...")
        self.eat("FUN")
        self.eat("ID")  
        self.eat("LPAREN")
        if self.current_token().token_type != "RPAREN":
            self.lista_argumentos() 
        self.eat("RPAREN")
        self.parsing_steps.append("}")

    def lista_argumentos(self):
        self.parsing_steps.append("Analisando lista de argumentos...")
        self.expressao()  
        while self.current_token().token_type == "COMMA":
            self.eat("COMMA")
            self.expressao()  

    def comando_condicional(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando condicional...")
        self.eat("IF")
        self.eat("LPAREN")
        self.expressao_booleana()  
        self.eat("RPAREN")
        self.bloco()  
        if self.current_token().token_type == "ELSE":
            self.eat("ELSE")
            self.bloco() 
        self.parsing_steps.append("}")

    def comando_laco(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de laço...")
        self.eat("WHILE")
        self.eat("LPAREN")
        self.expressao_booleana() 
        self.eat("RPAREN")
        self.bloco() 
        self.parsing_steps.append("}")

    def comando_impressao(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de impressão...")
        self.eat("PRINT")
        self.eat("LPAREN")
        self.expressao()  
        self.eat("RPAREN")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")

    def comando_retorno(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de retorno...")
        self.eat("RETURN")
        self.expressao()  
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")

    def comando_break(self):
        self.parsing_steps.append("{")
        self.parsing_steps.append("Analisando comando de break...")
        self.eat("BREAK")
        self.eat("SEMICOLON")
        self.parsing_steps.append("}")

    def expressao(self):
        self.expressao_booleana()

    def expressao_booleana(self):
        self.expressao_aritmetica()  
        while self.current_token().token_type in ["EQ", "NE", "GT", "GE", "LT", "LE"]:
            self.eat(self.current_token().token_type)  
            self.expressao_aritmetica() 

    def expressao_aritmetica(self):
        self.termo()
        while self.current_token().token_type in ["PLUS", "MINUS"]:
            self.eat(self.current_token().token_type) 
            self.termo() 

    def termo(self):
        
        self.fator() 
        while self.current_token().token_type in ["TIMES", "DIVIDE"]:
            self.eat(self.current_token().token_type) 
            self.fator()  

    def fator(self):
        
        current_token = self.current_token()
        if current_token.token_type == "ID":
            self.eat("ID")  
        elif current_token.token_type == "NUMBER":
            self.eat("NUMBER") 
        elif current_token.token_type in ["TRUE", "FALSE"]:
            self.eat(current_token.token_type)  
        elif current_token.token_type == "LPAREN":
            self.eat("LPAREN")
            self.expressao()  
            self.eat("RPAREN")
        elif current_token.token_type == "FUN":
            self.chamada_funcao() 
        else:
            raise SyntaxError(f"Esperado valor (ID, NUMBER, TRUE, FALSE ou expressão), mas encontrado {self.current_token().token_type} `{self.current_token().value}` na linha {current_token.line}")

    def print_parsing_steps(self):
        print("Etapas da análise sintática:")
        indent = 0
        for step in self.parsing_steps:
            if step == "{":
                print("  " * indent + step)
                indent += 1
            elif step == "}":
                indent -= 1
                print("  " * indent + step)
            else:
                print("  " * indent + step)

# Exemplo de uso para rodar sem precisar do main
if __name__ == '__main__':
    code = '''
        int a, b;
        print(a == b);
        print(a + b);
    '''
    lexer = Lexer(code)  
    lexer.tokenize()  
    # lexer.print_tokens() 
    # lexer.print_symbol_table() 

    parser = Parser(lexer.tokens) 
    try:
        parser.parse()  
        parser.print_parsing_steps()  
    except SyntaxError as e:
        print(e) 
