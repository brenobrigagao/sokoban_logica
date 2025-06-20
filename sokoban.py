from z3 import *
from z3 import Solver, Bool, And, Or, Not, Implies, Exactly, sat


def inicializar(n,m,T):
    #Definindo as variáveis atômicas, o P representa o Jogador, C uma caixa, M o objetivo e W uma parede
    P = [[[Bool(f"P_{i}_{j}_{t}") for t in range(T+1)] for j in range(m)] for i in range(n)]
    C = [[[Bool(f"C_{i}_{j}_{t}") for t in range(T+1)] for j in range(m)] for i in range(n)]
    M = [[Bool(f"M_{i}_{j}") for j in range(m)] for i in range(n)]
    W = [[Bool(f"W_{i}_{j}") for j in range(m)] for i in range(n)]
    return Solver(), P, C, M, W
def ler_tabuleiro():
    #Essa é a função que constroi o tabuleiro onde '#' é uma parede,'S' é o jogador,'B' é a caixa e 'M' é a meta
    print("\n Insira o tabuleiro linha por linha e digite 'f' para terminar:")
    tabuleiro = []
    caracteres_validos = {'#','S','B','M',' ','X'}
    comprimento_referencia = None
    while True:
        linha = input().strip()
        if linha.lower() == 'f':
            break
        if not linha:
            print("Linha vazia ignorada, digite 'f' para terminar.")
            continue
        if not all(caractere in caracteres_validos for caractere in linha):
            print(f"Erro: Use apenas os caracteres válidos: {', '.join(caracteres_validos)}")
            continue
        if comprimento_referencia is None:
            comprimento_referencia = len(linha)
        elif len(linha) != comprimento_referencia:
            print(f"Erro: Todas as linhas devem ter {comprimento_referencia} colunas.")
            continue
        tabuleiro.append(linha)
    return tabuleiro
def restricoes(solver, P,C,M,W,tabuleiro,m,n,T):
    #Configurando o tabuleiro
    for i in range(n):
        for j in range(m):
            char = tabuleiro[i][j]
            if char == '#':
                solver.add(W[i][j])
            elif char == 'M':
                solver.add(M[i][j])
            elif char in ['S','X']:
                solver.add(P[i][j][0])
            elif char == 'B':
                solver.add(C[i][j][0])
    #Exatamente um jogador em cada tempo
    for t in range(T + 1):
       solver.add(Exactly(*[P[i][j][t] for i in range(n) for j in range(m)],1)) 
       #Nenhuma sobreposição de jogador e caixa
       for i in range(n):
           for j in range(m):
               if tabuleiro == '#':
                   for t in range(T + 1):
                       solver.add(Not(P[i][j][t]))
                       solver.add(Not(C[i][j][t]))
    #Movimentação do jogador e das caixas
    direcoes = [(0,1),(1,0),(0,-1),(-1,0)]
    for t in range(T):
        for i in range(n):
            for j in range(m):
                movimentos = []

                for di, dj, in direcoes:
                    ni, nj = i + di, j + dj

                    if 0 <= ni < n and 0 <= nj < m:
                        #Movimentos simples, sem empurrar uma caixa
                        movimentos.append(And(
                            P[i][j][t],
                            Not(W[ni][nj]),
                            Not(C[ni][nj][t]),
                            P[ni][nj][t + 1],
                            *[C[x][y][t] == C[x][y][t + 1] for x in range(n) for y in range(m)]
                        ))

                        #Movimentos empurrando uma caixa
                        ni2, nj2, = ni + di , nj + dj
                        if 0 <= ni2 < n and 0 <= nj2 < m:
                            movimentos.append(And(
                                P[i][j][t],
                                C[ni][nj][t],
                                Not(W[ni2][nj2]),
                                Not(C[ni2][nj2][t]),
                                P[ni][nj][t+1],
                                C[ni2][nj2][t + 1],
                                Not(C[ni][nj][t + 1]),
                                *[C[x][y][t] == C[x][y][t + 1] for x in range(n) for y in range(m)
                                if (x,y) not in [(ni,nj), (ni2,nj2)]]
                            ))
                if movimentos:
                    solver.add(Implies(P[i][j][t], Or(*movimentos)))
    #Todas as metas devem ter uma caixa!!
    solver.add(And([
        Implies(M[i][j], C[i][j][T])
        for i in range(n) for j in range(m)
    ]))

