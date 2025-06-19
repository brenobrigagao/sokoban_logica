from z3 import *

def inicializar(n,m,T):
    #Definindo as variáveis atômicas, o P representa o Jogador, C uma caixa, M o objetivo e W uma parede
    P = [[[Bool(f"P_{i}_{j}_{t}") for t in range(T+1)] for j in range(m)] for i in range(n)]
    C = [[[Bool(f"C_{i}_{j}_{t}") for t in range(T+1)] for j in range(m)] for i in range(n)]
    M = [[Bool(f"M_{i}_{j}") for j in range(m)] for i in range(n)]
    W = [[Bool(f"W_{i}_{j}") for j in range(m)] for i in range(n)]
    return Solver(), P, C, M, W
def ler_tabuleiro():
    print("\n Insira o tabuleiro linha por linha e digite 'f' para terminar:")
    tabuleiro = []
    comprimento_referencia = None
    while True:
        linha = input().strip()
        if linha.lower() == 'f':
            break
        if not linha:
            print("Linha vazia ignorada, digite 'f' para terminar.")
            continue
        if comprimento_referencia is None:
            comprimento_referencia = len(linha)
        elif len(linha) != comprimento_referencia:
            print(f"Erro: Todas as linhas devem ter {comprimento_referencia} colunas.")
            continue
        tabuleiro.append(linha)
    return tabuleiro
