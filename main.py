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
    main("codigo.txt")
