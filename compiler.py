from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer  # Supondo que semantic_analyzer está implementado

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
        self.semantic_analyzer = None

    def compile(self):
        # Etapa 1: Analisador Léxico
        try:
            print(f"{Colors.GREEN}Iniciando Analisador Léxico!{Colors.RESET}")

            self.lexer.tokenize()
            self.lexer.print_tokens()
            self.lexer.print_symbol_table()
            self.parser = Parser(self.lexer.tokens)
            print(f"{Colors.GREEN}Analisador Léxico bem sucedido!{Colors.RESET}")
        except SyntaxError as e:
            print(f"{Colors.RED}Erro no léxico: {e}{Colors.RESET}")
            return  
        except Exception as e:
            print(f"{Colors.RED}Erro: {e}{Colors.RESET}")
            return  

        # Etapa 2: Analisador Sintático
        try:
            print(f"{Colors.GREEN}Iniciando Analisador Sintático!{Colors.RESET}")

            self.parser.parse()
            self.parser.print_parsing_steps()
            print(f"{Colors.GREEN}Analisador Sintático bem sucedido!{Colors.RESET}")
        except SyntaxError as e:
            print(f"{Colors.RED}Erro de sintaxe: {e}{Colors.RESET}")
            return 
        except Exception as e:
            print(f"{Colors.RED}Erro: {e}{Colors.RESET}")
            return

        # Etapa 3: Analisador Semântico
        try:
            print(f"{Colors.GREEN}Iniciando Analisador Semântico!{Colors.RESET}")

            self.semantic_analyzer = SemanticAnalyzer(self.lexer.tokens, self.lexer.symbol_table)
            self.semantic_analyzer.analyze()

            if self.semantic_analyzer.errors:
                for error in self.semantic_analyzer.errors:
                    print(f"{Colors.RED}Erro semântico: {error}{Colors.RESET}")
                return  
            print(f"{Colors.GREEN}Analisador Semântico bem sucedido!{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Erro no analisador semântico: {e}{Colors.RESET}")
            return
