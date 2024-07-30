from lexer import Lexer
from parser import Parser

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

class Compiler:
    def __init__(self, code: str):
        if not code:
            raise ValueError(f"{Colors.RED}Código vazio!{Colors.RESET}")
        self.lexer = Lexer(code)
        self.parser = None

    def compile(self):
        try:
            self.lexer.tokenize()
            self.lexer.print_tokens()
            self.lexer.print_symbol_table()
            self.parser = Parser(self.lexer.tokens)
            print(f"{Colors.GREEN}Analisador Léxico bem sucedido!{Colors.RESET}")
        except SyntaxError as e:
            print(f"{Colors.RED}Erro no léxico: {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Erro: {e}{Colors.RESET}")
            return  # Se ocorrer um erro no léxico, interrompe a compilação

        try:
            ast = self.parser.parse()
            """ self.parser.print_parsing_steps() """
            self.parser.print_ast(ast)
            print(f"{Colors.GREEN}Analisador Sintático bem sucedido!{Colors.RESET}")
        except SyntaxError as e:
            print(f"{Colors.RED}Erro de sintaxe: {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Erro: {e}{Colors.RESET}")
