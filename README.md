### **Projeto Compiladores**

#### **1. Analisador Léxico (`lexer.py`)**

**Função:**
O analisador léxico é responsável por transformar o código fonte em uma sequência de tokens. Tokens são unidades básicas de significado na linguagem, como palavras-chave, identificadores e operadores.

**Componentes Principais:**

- **Lista de Tokens:** Define os padrões regex para diferentes tipos de tokens, como palavras-chave (`int`, `bool`, `void`), operadores (`+`, `-`, `*`, `==`, `!=`), e outros (`ID`, `NUMBER`).

- **Classe `Lexer`:**
  - **Método `__init__`:** Inicializa o lexer com o código fonte e começa a tokenização.
  - **Método `tokenize`:** Processa o código fonte, reconhecendo tokens baseados nos padrões regex definidos. Ignora espaços em branco e emite um erro para caracteres inválidos.
  - **Método `print_tokens`:** Imprime a lista de tokens gerada.
  - **Método `print_symbol_table`:** Imprime a tabela de símbolos.

**Exemplo de Uso:**
O arquivo inclui um bloco de código que lê arquivos de teste e imprime os tokens gerados e a tabela de símbolos.

```bash
from lexer import Lexer

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

```

---

#### **2. Analisador Sintático (`parser.py`)**

**Função:**
**Função:**
O analisador sintático utiliza a sequência de tokens fornecida pelo analisador léxico para verificar se o código está corretamente estruturado segundo as regras gramaticais.

**Componentes Principais:**

- **Classe `Parser`:**
  - **Método `__init__`:** Inicializa o parser com o lexer e define o token atual.
  - **Método `parse`:** Inicia o processo de análise sintática.
  - **Método `eat`:** Consome o token atual se ele corresponder ao tipo esperado, avançando para o próximo token.
  - **Métodos de Análise (`programa`, `declaracao_comando`, `declaracao_variaveis`, `etc`):** Processam diferentes estruturas do código e verificam se estão de acordo com as regras gramaticais.

**Exemplo de Uso:**
O arquivo inclui um bloco de código que lê um arquivo de teste, gera tokens, e então usa o parser para imprimir os tokens consumidos.

```bash
from lexer import Lexer
from parser import Parser

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

    parser = Parser(lexer.tokens)
    try:
        parser.parse()
        parser.print_parsing_steps()
    except SyntaxError as e:
        print(e)


```

---

#### **3. Compilador (`compiler.py`)**

**Função:**
O compilador integra o analisador léxico e o analisador sintático, gerencia a execução dos testes e apresenta os resultados.

**Componentes Principais:**

- **Classe `Compiler`:**
  - **Método `__init__`:** Inicializa o compilador com o código fonte.
  - **Método `compile`:** Realiza a tokenização, análise sintática e impressão dos resultados.

**Exemplo de Uso:**
O arquivo inclui um bloco de código que lê o código fonte, cria instâncias de Lexer e Parser, e executa o processo de compilação.

```bash
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

```

#### **4. Programa Principal (`main.py`)**

**Função:**
O programa principal gerencia a execução do compilador e apresenta os resultados.

**Componentes Principais:**

- **Função `main`:**
  - **Leitura dos Arquivos de Teste:** Lê o código fonte de um arquivo especificado e executa o processo de compilação.
  - **Tratamento de Erros:** Captura e exibe erros, como arquivo não encontrado ou erros de sintaxe.

**Exemplo de Uso:**
O arquivo inclui um bloco de código que lê um arquivo de teste, cria uma instância de Compiler, e executa o processo de compilação.

```bash
from compiler import Compiler

def main(file):
    try:
        with open(file, "r") as file:
            codigo = file.read()
            print(f"Código lido do arquivo:\n{codigo}")

        compiler = Compiler(codigo)
        compiler.compile()
    except FileNotFoundError:
        print(f"Erro: O arquivo {file} não foi encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main("tests/codigo.txt")

```
