from lexer import Lexer
from parser import Parser

class Compiler:
    def __init__(self, code: str):
        if not code:
            raise ValueError("Código vazio!")
        self.lexer = Lexer(code)
        self.parser = None

    def compile(self):
        self.lexer.tokenize()
        
        self.lexer.print_tokens()
        self.lexer.print_symbol_table()

        self.parser = Parser(self.lexer.tokens)
        self.parser.parse()
        self.parser.print_parsing_steps()


        print("Compilação bem sucedida")
