import re
from typing import Any, Dict, List

class Token:
    def __init__(self, token_type: str, value: str, line: int, column: int):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.token_type}, '{self.value}', line={self.line}, column={self.column})"
    
class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Dict[str, Any]] = {}

    def add_symbol(self, name: str, line: int, column: int):
        if name not in self.symbols:
            self.symbols[name] = {
                "type": "undefined",
                "value": None,
                "scope": "global",
                "line": line,
                "column": column
            }

    def get_symbol(self, name: str):
        return self.symbols.get(name)

    def __repr__(self):
        return f"SymbolTable({self.symbols})"

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.current_line = 1
        self.tokens: List[Token] = []
        self.symbol_table = SymbolTable()
        self.token_specification = [
            ('EQ', r'=='),                          # Igualdade
            ('LE', r'<='),                          # Menor ou igual
            ('GE', r'>='),                          # Maior ou igual
            ('NE', r'!='),                          # Diferente
            ('ASSIGN', r'='),                       # Atribuição
            ('LT', r'<'),                           # Menor que
            ('GT', r'>'),                           # Maior que
            ('SEMICOLON', r';'),                    # Ponto e vírgula
            ('COMMA', r','),                        # Vírgula
            ('LPAREN', r'\('),                      # Parêntese esquerdo
            ('RPAREN', r'\)'),                      # Parêntese direito
            ('LBRACE', r'\{'),                      # Chave esquerda
            ('RBRACE', r'\}'),                      # Chave direita
            ('PLUS', r'\+'),                        # Operador de adição
            ('MINUS', r'-'),                        # Operador de subtração
            ('TIMES', r'\*'),                       # Operador de multiplicação
            ('DIVIDE', r'/'),                       # Operador de divisão
            ('AND', r'&&'),                         # E lógico
            ('OR', r'\|\|'),                        # Ou lógico
            ('NOT', r'\bnot\b'),                    # Negação lógica
            ('IF', r'\bif\b'),                      # Palavra-chave if
            ('ELSE', r'\belse\b'),                  # Palavra-chave else
            ('WHILE', r'\bwhile\b'),                # Palavra-chave while
            ('RETURN', r'\breturn\b'),              # Palavra-chave return
            ('PRINT', r'\bprint\b'),                # Palavra-chave print
            ('VOID', r'\bvoid\b'),                  # Palavra-chave void
            ('INT', r'\bint\b'),                    # Palavra-chave int
            ('BOOL', r'\bbool\b'),                  # Palavra-chave bool
            ('TRUE', r'\btrue\b'),                  # Palavra-chave true
            ('FALSE', r'\bfalse\b'),                # Palavra-chave false
            ('BREAK', r'\bbreak\b'),                # Palavra-chave break
            ('CONTINUE', r'\bcontinue\b'),          # Palavra-chave continue
            ('PRC', r'\bprc\b'),                    # Palavra-chave prc
            ('FUN', r'\bfun\b'),                    # Palavra-chave fun
            ('SKIP', r'[ \t]+'),                    # Espaços e tabulações
            ('NEWLINE', r'\n'),                     # Quebras de linha
            ('STRING', r'"(?:\\.|[^"\\])*"'),       # Literais de string
            ('NUMBER', r'\d+'),                     # Inteiros
            ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),      # Identificadores
            ('MISMATCH', r'.'),                     # Qualquer outro caractere
        ]

        #tem que ver se dá pra melhorar a diferença entre chamada de função e procedimento
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        self.get_token = re.compile(self.tok_regex).match

    def tokenize(self):
        line_start = 0
        match = self.get_token(self.code)
        while match is not None:
            typ = match.lastgroup
            start = match.start()
            end = match.end()
            column = start - line_start
            if typ == 'NEWLINE':
                line_start = end
                self.current_line += 1
            elif typ == 'SKIP':
                pass
            elif typ == 'ID':
                val = match.group(typ)
                if val in {'int', 'bool', 'void', 'true', 'false', 'if', 'else', 'while', 'return', 'print', 'prc', 'fun'}:
                    typ = val.upper()
                else:
                    self.symbol_table.add_symbol(val, self.current_line, column)
                self.tokens.append(Token(typ, val, self.current_line, column))
            elif typ != 'MISMATCH':
                val = match.group(typ)
                self.tokens.append(Token(typ, val, self.current_line, column))
            else:
                raise RuntimeError(f'{match.group(typ)!r} inesperado na linha {self.current_line}')
            match = self.get_token(self.code, end)

    def print_tokens(self):
        print("Lista de Tokens:")
        for token in self.tokens:
            print(token)

    def print_symbol_table(self):
        print("Tabela de Símbolos:")
        for name, attributes in self.symbol_table.symbols.items():
            print(f"{name}: {attributes}")

# Exemplo de uso para rodar sem precisar do main
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
    lexer.print_tokens()
    lexer.print_symbol_table()
