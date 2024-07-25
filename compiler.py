from lexer import Lexer, SymbolTable



class Compiler:
    def __init__(self, code: str):
        if not code:
            raise ValueError("Código vazio!")
        self.lexer = Lexer(code)
        #Criação do parser

    def compile(self):
        self.lexer.tokenize()
        
        self.lexer.print_tokens()
        self.lexer.print_symbol_table()

        #Chamada do parser com tokens e tabela de simbolos

        print("Compilação bem sucedida")