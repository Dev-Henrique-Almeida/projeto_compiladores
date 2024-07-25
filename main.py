from compiler import Compiler

def main (file):
    with open(file, "r") as file:
        codigo = file.read()

    compiler = Compiler(codigo)
    compiler.compile()


if __name__ == "__main__":
    main(r"C:\\Users\\pedro.alves\\Desktop\\Compiladores\\projeto_compiladores\\codigo.txt")