from compiler import Compiler

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def main(file):
    try:
        with open(file, "r") as file:
            codigo = file.read()
            print(f"Código lido do arquivo:\n{codigo}")

        compiler = Compiler(codigo)
        compiler.compile()
    except FileNotFoundError:
        print(f"{Colors.RED}Erro: O arquivo {file} não foi encontrado.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Erro: {e}{Colors.RESET}")

if __name__ == "__main__":
    main("tests/codigo.txt")
