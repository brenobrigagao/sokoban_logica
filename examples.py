from sys import argv
from solve import solve
from maps import maps
from utils import imprimir_solucao

def example(number,turnos=50):
    print(f"=== Example {number+1} ===")
    imprimir_solucao(solve(maps[number],turnos))

def examples(turnos=50):
   for number in range(len(maps)): example(number,turnos)
       
if __name__ == "__main__":
    if len(argv) == 1:
        examples()
    elif len(argv) == 2:
        examples(turnos=int(argv[1]))
    elif len(argv) == 3:
        example(int(argv[2]),int(argv[1]))
    else:
        print("Uso: python examples.py [turnos_maximos] [numero_exemplo]")
