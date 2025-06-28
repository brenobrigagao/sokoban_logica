from sys import argv
from solve import solve
from maps import maps
from utils import imprimir_solucao

def example(number,turnos=50):
    print(f"=== Example {number} ===")
    imprimir_solucao(solve(maps[number],turnos))

def examples():
   for number in range(len(maps)): example(number)
       
if __name__ == "__main__":
    if len(argv) == 1:
        examples()
    elif len(argv) == 2:
        example(int(argv[1]))
    elif len(argv) == 3:
        example(int(argv[1]), int(argv[2]))
    else:
        print("Uso: python examples.py [numero_exemplo] [turnos_maximos]")
