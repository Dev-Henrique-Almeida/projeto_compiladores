import re

# Definição dos tokens e suas expressões regulares correspondentes
token_specification = [
    ('NUMBER',      r'\d+'),                  # Inteiros
    ('ID',          r'[a-zA-Z_][a-zA-Z_0-9]*'), # Identificadores
    ('ASSIGN',      r'='),                    # Atribuição
    ('SEMICOLON',   r';'),                    # Ponto e vírgula
    ('COMMA',       r','),                    # Vírgula
    ('LPAREN',      r'\('),                   # Parêntese esquerdo
    ('RPAREN',      r'\)'),                   # Parêntese direito
    ('LBRACE',      r'\{'),                   # Chave esquerda
    ('RBRACE',      r'\}'),                   # Chave direita
    ('PLUS',        r'\+'),                   # Operador de adição
    ('MINUS',       r'-'),                    # Operador de subtração
    ('TIMES',       r'\*'),                   # Operador de multiplicação
    ('DIVIDE',      r'/'),                    # Operador de divisão
    ('EQ',          r'=='),                   # Igualdade
    ('NE',          r'!='),                   # Diferente
    ('GT',          r'>'),                    # Maior que
    ('GE',          r'>='),                   # Maior ou igual
    ('LT',          r'<'),                    # Menor que
    ('LE',          r'<='),                   # Menor ou igual
    ('AND',         r'&&'),                   # E lógico
    ('OR',          r'\|\|'),                 # Ou lógico
    ('NOT',         r'not'),                  # Negação lógica
    ('IF',          r'if'),                   # Palavra-chave if
    ('ELSE',        r'else'),                 # Palavra-chave else
    ('WHILE',       r'while'),                # Palavra-chave while
    ('RETURN',      r'return'),               # Palavra-chave return
    ('PRINT',       r'print'),                # Palavra-chave print
    ('VOID',        r'void'),                 # Palavra-chave void
    ('INT',         r'int'),                  # Palavra-chave int
    ('BOOL',        r'bool'),                 # Palavra-chave bool
    ('TRUE',        r'true'),                 # Palavra-chave true
    ('FALSE',       r'false'),                # Palavra-chave false
    ('PROC',        r'prc'),                  # Palavra-chave prc
    ('FUNC',        r'fun'),                  # Palavra-chave fun
    ('SKIP',        r'[ \t]+'),               # Espaços e tabulações
    ('NEWLINE',     r'\n'),                   # Quebras de linha
    ('MISMATCH',    r'.'),                    # Qualquer outro caractere
]

# Compilação das expressões regulares
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

# Função para gerar tokens
def tokenize(code):
    line_num = 1
    line_start = 0
    match = get_token(code)
    while match is not None:
        typ = match.lastgroup
        if typ == 'NEWLINE':
            line_start = match.end()
            line_num += 1
        elif typ != 'SKIP' and typ != 'MISMATCH':
            val = match.group(typ)
            yield typ, val, line_num
        match = get_token(code, match.end())
    if match is None:
        yield 'MISMATCH', code[line_start:], line_num

# Exemplo de uso
if __name__ == '__main__':
    code = '''
    int x, y;
    bool z;

    int soma(int a, int b) {
        int resultado;
        resultado = a + b;
        return resultado;
    }
    '''
    for token in tokenize(code):
        print(token)