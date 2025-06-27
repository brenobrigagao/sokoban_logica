# Importações

from z3 import *

from itertools import permutations

# Função para transformar uma coordenada 1D em uma coordenada 2D

def posicao_1D_para_posicao_2D(posicao_1D, colunas):
  i = posicao_1D // colunas  
  j = posicao_1D % colunas  
  return (i,j)

# Função para criar uma string que representa a coordenada no espaço tempo do jogador

def jogador_posicao_turno(posicao,turno):
  return f'jogador({posicao[0]},{posicao[1]},{turno})'

# Função para criar uma string que representa a coordenada no espaço tempo de uma caixa

def caixa_numero_posicao_turno(numero,posicao,turno):
  return f'caixa_{numero}({posicao[0]},{posicao[1]},{turno})'

# Input 

tamanho = [10,10]
linhas = tamanho[0]
colunas = tamanho[1]
posicoes = linhas * colunas

jogador = [0,0,0]
caixas = [[1,1,0], [2,2,0], [3,3,0]]
paredes = [[4,4], [5,5], [6,6]] 
metas = [[7,7], [8,8], [9,9]] 

turnos = 50

# O jogador ocupa exatamente uma celula no turno i, para i >= 0

def jogador_ocupa_exatamente_uma_celula(turnos,posicoes,colunas): 
  jogador_ocupa_exatamente_uma_celula = []

  for turno in range(turnos+1):
    bools = [Bool(jogador_posicao_turno(posicao_1D_para_posicao_2D(posicao,colunas),turno)) for posicao in range(posicoes)]
    soma = Sum([If(b,1,0) for b in bools])
    jogador_ocupa_exatamente_uma_celula.append(soma == 1)

  jogador_ocupa_exatamente_uma_celula = And(*jogador_ocupa_exatamente_uma_celula)

  return jogador_ocupa_exatamente_uma_celula
  
# A caixa c ocupa exatamente uma celula no turno i, para c >= 0 e i >= 0

def caixa_ocupa_exatamente_uma_celula(caixas,turnos,posicoes,colunas):
  caixa_ocupa_exatamente_uma_celula = []

  for numero in range(len(caixas)):
    for turno in range(turnos+1):
      bools = [Bool(caixa_numero_posicao_turno(numero,posicao_1D_para_posicao_2D(posicao,colunas),turno)) for posicao in range(posicoes)]
      soma = Sum([If(b,1,0) for b in bools]) 
      caixa_ocupa_exatamente_uma_celula.append(soma == 1)

  caixa_ocupa_exatamente_uma_celula = And(*caixa_ocupa_exatamente_uma_celula)

  return caixa_ocupa_exatamente_uma_celula

# O jogador nao pode ocupar a mesma celula que uma caixa.

def jogador_nao_ocupa_caixa(caixas,turnos,posicoes,colunas):
  jogador_nao_ocupa_caixa = []

  for numero in range(len(caixas)):
    for turno in range(turnos+1): 
      for posicao in range(posicoes):
        jogador_nao_ocupa_caixa.append(
          Not(
            And(
              Bool(jogador_posicao_turno(posicao_1D_para_posicao_2D(posicao,colunas),turno)),
              Bool(caixa_numero_posicao_turno(numero,posicao_1D_para_posicao_2D(posicao,colunas),turno))))) 

  jogador_nao_ocupa_caixa = And(*jogador_nao_ocupa_caixa)

  return jogador_nao_ocupa_caixa

# O jogador nao pode ocupar a mesma celula que uma parede.

def jogador_nao_ocupa_parede(turnos,paredes):
  jogador_nao_ocupa_parede = []

  for parede in paredes:
    for turno in range(turnos+1):
      jogador_nao_ocupa_parede.append(
        Not(
          Bool(jogador_posicao_turno((parede[0],parede[1]),turno)))) 

  jogador_nao_ocupa_parede = And(*jogador_nao_ocupa_parede)

  return jogador_nao_ocupa_parede

# Duas caixas nao podem ocupar a mesma celula.

def caixa_nao_ocupa_caixa(caixas,turnos,posicoes):
  caixa_nao_ocupa_caixa = []

  for numero_1 in range(len(caixas)):
    for numero_2 in range(numero_1+1,len(caixas)):
      for turno in range(turnos+1):
        for posicao in range(posicoes):
          caixa_nao_ocupa_caixa.append(
            Not(
              And(
                Bool(caixa_numero_posicao_turno(numero_1,posicao_1D_para_posicao_2D(posicao,colunas),turno)),
                Bool(caixa_numero_posicao_turno(numero_2,posicao_1D_para_posicao_2D(posicao,colunas),turno)))))
          
  caixa_nao_ocupa_caixa = And(*caixa_nao_ocupa_caixa)

  return caixa_nao_ocupa_caixa

# Uma caixa nao pode ocupar a mesma celula que uma parede.

def caixa_nao_ocupa_parede(caixas,turnos,paredes):
  caixa_nao_ocupa_parede = []

  for numero in range(len(caixas)):
    for parede in paredes:
      for turno in range(turnos+1):
        caixa_nao_ocupa_parede.append(
            Not(
              Bool(caixa_numero_posicao_turno(numero,(parede[0],parede[1]),turno))))

  caixa_nao_ocupa_parede = And(*caixa_nao_ocupa_parede)

  return caixa_nao_ocupa_parede

# O jogador se move exatamente uma celula por turno.

def jogador_move_exatamente_uma_celula(turnos,linhas,colunas):
  jogador_move_exatamente_uma_celula = []

  for turno in range(turnos):
    for linha in range(linhas):
      for coluna in range(colunas):
        movimentos_validos = []
        if (linha - 1 >= 0): movimentos_validos.append(Bool(jogador_posicao_turno((linha-1,coluna),turno+1)))
        if (linha + 1 < linhas): movimentos_validos.append(Bool(jogador_posicao_turno((linha+1,coluna),turno+1)))
        if (coluna - 1 >= 0): movimentos_validos.append(Bool(jogador_posicao_turno((linha,coluna-1),turno+1)))
        if (coluna + 1 < colunas): movimentos_validos.append(Bool(jogador_posicao_turno((linha,coluna+1),turno+1)))
        jogador_move_exatamente_uma_celula.append(
          Implies(
            Bool(jogador_posicao_turno((linha,coluna),turno)),
            Or(*movimentos_validos)))
        
  jogador_move_exatamente_uma_celula = And(*jogador_move_exatamente_uma_celula)

  return jogador_move_exatamente_uma_celula

# Ou uma caixa permanece parada durante dois turnos consecutivos Ou o jogador empurra a caixa.
def caixa_repouso_ou_empurrada(caixas,turnos,linhas,colunas):
  caixa_repouso_ou_empurrada = []

  for numero in range(len(caixas)):
    for turno in range(turnos):
      for linha in range(linhas):
        for coluna in range(colunas):
          caixa_repouso_ou_empurrada.append(
            Or(
              And(
                Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)), 
                Bool(jogador_posicao_turno((linha,coluna),turno+1))),
              And(
                Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)), 
                Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno+1)))))

  caixa_repouso_ou_empurrada = And(*caixa_repouso_ou_empurrada)

  return caixa_repouso_ou_empurrada

# Se o jogador empurra a caixa para baixo entao a caixa se move exatamente uma celula para baixo.

def jogador_empurra_caixa_para_baixo(caixas, turnos, linhas, colunas):
    restricoes = []

    for numero in range(len(caixas)):
        for turno in range(turnos):
            for linha in range(1, linhas - 1):
                for coluna in range(colunas):
                    restricoes.append(
                        Implies(
                            And(
                                Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
                                Bool(jogador_posicao_turno((linha - 1, coluna), turno)),
                                Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
                            Bool(caixa_numero_posicao_turno(numero, (linha + 1, coluna), turno + 1))
                        )
                    )
    return And(*restricoes)


def jogador_empurra_caixa_para_cima(caixas, turnos, linhas, colunas):
    restricoes = []

    for numero in range(len(caixas)):
        for turno in range(turnos):
            for linha in range(1, linhas - 1):
                for coluna in range(colunas):
                    restricoes.append(
                        Implies(
                            And(
                                Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
                                Bool(jogador_posicao_turno((linha + 1, coluna), turno)),
                                Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
                            Bool(caixa_numero_posicao_turno(numero, (linha - 1, coluna), turno + 1))
                        )
                    )
    return And(*restricoes)


def jogador_empurra_caixa_para_esquerda(caixas, turnos, linhas, colunas):
    restricoes = []

    for numero in range(len(caixas)):
        for turno in range(turnos):
            for linha in range(linhas):
                for coluna in range(1, colunas - 1):
                    restricoes.append(
                        Implies(
                            And(
                                Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
                                Bool(jogador_posicao_turno((linha, coluna + 1), turno)),
                                Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
                            Bool(caixa_numero_posicao_turno(numero, (linha, coluna - 1), turno + 1))
                        )
                    )
    return And(*restricoes)


def jogador_empurra_caixa_para_direita(caixas, turnos, linhas, colunas):
    restricoes = []

    for numero in range(len(caixas)):
        for turno in range(turnos):
            for linha in range(linhas):
                for coluna in range(1, colunas - 1):
                    restricoes.append(
                        Implies(
                            And(
                                Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
                                Bool(jogador_posicao_turno((linha, coluna - 1), turno)),
                                Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
                            Bool(caixa_numero_posicao_turno(numero, (linha, coluna + 1), turno + 1))
                        )
                    )
    return And(*restricoes)

# Existe pelo menos um turno i onde o jogo termina.

def existe_pelo_menos_um_turno_onde_jogo_termina(caixas,turnos,metas):
  indices_caixas = list(range(len(caixas)))

  permutacoes_indices_caixas = list(permutations(indices_caixas))

  existe_pelo_menos_um_turno_onde_jogo_termina = []

  for turno in range(turnos+1):
    for permutacao in permutacoes_indices_caixas:
      combinacoes_indices_caixas_metas = []
      for meta in range(len(metas)):
        combinacoes_indices_caixas_metas.append(Bool(caixa_numero_posicao_turno(permutacao[meta],(metas[meta][0],metas[meta][1]),turno)))
      existe_pelo_menos_um_turno_onde_jogo_termina.append(And(*combinacoes_indices_caixas_metas))

  existe_pelo_menos_um_turno_onde_jogo_termina = Or(*existe_pelo_menos_um_turno_onde_jogo_termina)

  return existe_pelo_menos_um_turno_onde_jogo_termina
    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def ler_matriz():
  matriz = []
  print("Digite as linhas da matriz (pressione ENTER em branco para terminar):")
    
  while True:
    linha = input()
    if not linha: break
    matriz.append(list(linha))

    if len(set(len(l) for l in matriz)) > 1: raise ValueError("A matriz não é retangular! Todas as linhas devem ter o mesmo número de caracteres.")
    
    return matriz
  
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def processar_matriz(matriz):
    jogador = []
    caixas = []
    paredes = []
    metas = []

    linhas = len(matriz)
    if linhas == 0: raise ValueError("A matriz não pode ser vazia.")
    colunas = len(matriz[0])
    tamanho = [linhas, colunas]

    for linha_idx, linha in enumerate(matriz):
        if len(linha) != colunas:
            raise ValueError(f"A matriz não é retangular: linha {linha_idx} tem tamanho diferente.")
        for coluna_idx, char in enumerate(linha):
            if char == '#':
                paredes.append([linha_idx, coluna_idx])
            elif char == '.':
                pass  # espaço vazio
            elif char == 'S':
                jogador = [linha_idx, coluna_idx, 0]
            elif char == 'B':
                caixas.append([linha_idx, coluna_idx, 0])
            elif char == 'm':
                metas.append([linha_idx, coluna_idx])
            elif char == 'x':
                jogador = [linha_idx, coluna_idx, 0]
                metas.append([linha_idx, coluna_idx])
            else:
                raise ValueError(f"Caractere inválido encontrado: '{char}' na posição ({linha_idx}, {coluna_idx})")

    return jogador, caixas, paredes, metas, tamanho

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def solucionar_sokoban(mapa, turnos_maximos=50):
    """
    Tenta encontrar a menor quantidade de turnos necessária para resolver o mapa.
    Retorna o modelo do solver se encontrar solução, ou None se não houver solução.
    """
    jogador, caixas, paredes, metas, tamanho = processar_matriz(mapa)
    linhas, colunas = tamanho
    posicoes = linhas * colunas

    for turnos in range(turnos_maximos + 1):
        print(f"Tentando resolver com {turnos} turnos...")

        solver = Solver()

        # Adiciona todas as restrições ao solver
        solver.add(
            jogador_ocupa_exatamente_uma_celula(turnos, posicoes, colunas),
            caixa_ocupa_exatamente_uma_celula(caixas, turnos, posicoes, colunas),
            jogador_nao_ocupa_caixa(caixas, turnos, posicoes, colunas),
            jogador_nao_ocupa_parede(turnos, paredes),
            caixa_nao_ocupa_caixa(caixas, turnos, posicoes),
            caixa_nao_ocupa_parede(caixas, turnos, paredes),
            jogador_move_exatamente_uma_celula(turnos, linhas, colunas),
            caixa_repouso_ou_empurrada(caixas, turnos, linhas, colunas),
            jogador_empurra_caixa_para_baixo(caixas, turnos, linhas, colunas),
            jogador_empurra_caixa_para_cima(caixas, turnos, linhas, colunas),
            jogador_empurra_caixa_para_esquerda(caixas, turnos, linhas, colunas),
            jogador_empurra_caixa_para_direita(caixas, turnos, linhas, colunas),
            existe_pelo_menos_um_turno_onde_jogo_termina(caixas, turnos, metas)
        )

        if solver.check() == sat:
            modelo = solver.model()
            print(f"Solução encontrada com {turnos} turnos!")
            return modelo

    print("Não foi possível encontrar solução dentro do limite de turnos.")
    return None

mapa_nivel1 = [
    list("#######"),
    list("#..m..#"),
    list("#.B.B.#"),
    list("#.B.S.#"),
    list("#...m.#"),
    list("#######"),
]

solucao = solucionar_sokoban(mapa_nivel1,100)