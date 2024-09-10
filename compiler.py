from lexer import Lexer
from parser import Parser
from new_semantic import SemanticAnalyzer
from three_address_code_generator import ThreeAddressCodeGenerator  

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
            ast_root = self.parser.parse()  # Arvore retornada pelo parser
            print(ast_root)
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
            self.semantic_analyzer = SemanticAnalyzer(ast_root, {})
            self.semantic_analyzer.analyze()

            if self.semantic_analyzer.errors:
                for error in self.semantic_analyzer.errors:
                    print(f"{Colors.RED}Erro semântico: {error}{Colors.RESET}")
                return  
            print(f"{Colors.GREEN}Analisador Semântico bem sucedido!{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Erro no analisador semântico: {e}{Colors.RESET}")
            return

        # Etapa 4: Geração de Código de Três Endereços
        try:
            print(f"{Colors.GREEN}Iniciando Geração de Código de Três Endereços!{Colors.RESET}")
            codegen = ThreeAddressCodeGenerator(ast_root)
            instructions = codegen.generate()


            for instr in instructions:
                print(instr)
            

            print(f"{Colors.GREEN}Código de Três Endereços Gerado com Sucesso!{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}Erro na geração de código: {e}{Colors.RESET}")
            return
