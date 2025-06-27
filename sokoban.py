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

jogador_ocupa_exatamente_uma_celula = []

for turno in range(turnos+1):
  bools = [Bool(jogador_posicao_turno(posicao_1D_para_posicao_2D(posicao,colunas),turno)) for posicao in range(posicoes)]
  soma = Sum([If(b,1,0) for b in bools])
  jogador_ocupa_exatamente_uma_celula.append(soma == 1)

jogador_ocupa_exatamente_uma_celula = And(*jogador_ocupa_exatamente_uma_celula)
  
# A caixa c ocupa exatamente uma celula no turno i, para c >= 0 e i >= 0

caixa_ocupa_exatamente_uma_celula = []

for numero in range(len(caixas)):
  for turno in range(turnos+1):
    bools = [Bool(caixa_numero_posicao_turno(numero,posicao_1D_para_posicao_2D(posicao,colunas),turno)) for posicao in range(posicoes)]
    soma = Sum([If(b,1,0) for b in bools]) 
    caixa_ocupa_exatamente_uma_celula.append(soma == 1)

caixa_ocupa_exatamente_uma_celula = And(*caixa_ocupa_exatamente_uma_celula)

# O jogador nao pode ocupar a mesma celula que uma caixa.

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

# O jogador nao pode ocupar a mesma celula que uma parede.

jogador_nao_ocupa_parede = []

for parede in paredes:
  for turno in range(turnos+1):
    jogador_nao_ocupa_parede.append(
      Not(
        Bool(jogador_posicao_turno((parede[0],parede[1]),turno)))) 

jogador_nao_ocupa_parede = And(*jogador_nao_ocupa_parede)

# Duas caixas nao podem ocupar a mesma celula.

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

# Uma caixa nao pode ocupar a mesma celula que uma parede.

caixa_nao_ocupa_parede = []

for numero in range(len(caixas)):
  for parede in paredes:
    for turno in range(turnos+1):
       caixa_nao_ocupa_parede.append(
          Not(
            Bool(caixa_numero_posicao_turno(numero,(parede[0],parede[1]),turno))))

caixa_nao_ocupa_parede = And(*caixa_nao_ocupa_parede)

# O jogador se move exatamente uma celula por turno.

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

# Ou uma caixa permanece parada durante dois turnos consecutivos Ou o jogador empurra a caixa.

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

# Se o jogador empurra a caixa para baixo entao a caixa se move exatamente uma celula para baixo.

jogador_empurra_caixa_para_baixo = []

for numero in range(len(caixas)):
  for turno in range(turnos):
    for linha in range(1,linhas-1):
      for coluna in range(colunas):
        jogador_empurra_caixa_para_baixo.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)),
              Bool(jogador_posicao_turno((linha-1,coluna),turno)),
              Bool(jogador_posicao_turno((linha,coluna),turno+1))), 
            Bool(caixa_numero_posicao_turno(numero,(linha+1,coluna),turno+1))))

jogador_empurra_caixa_para_baixo = And(*jogador_empurra_caixa_para_baixo)

# Se o jogador empurra a caixa para cima entao a caixa se move exatamente uma celula para cima.

jogador_empurra_caixa_para_cima = []

for numero in range(len(caixas)):
  for turno in range(turnos):
    for linha in range(1,linhas-1):
      for coluna in range(colunas):
        jogador_empurra_caixa_para_cima.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)),
              Bool(jogador_posicao_turno((linha+1,coluna),turno)),
              Bool(jogador_posicao_turno((linha,coluna),turno+1))), 
            Bool(caixa_numero_posicao_turno(numero,(linha-1,coluna),turno+1))))

jogador_empurra_caixa_para_cima = And(*jogador_empurra_caixa_para_cima)

# Se o jogador empurra a caixa para a esquerda entao a caixa se move exatamente uma celula para a esquerda.

jogador_empurra_caixa_para_esquerda = []

for numero in range(len(caixas)):
  for turno in range(turnos):
    for linha in range(linhas):
      for coluna in range(1,colunas-1):
        jogador_empurra_caixa_para_esquerda.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)),
              Bool(jogador_posicao_turno((linha,coluna+1),turno)),
              Bool(jogador_posicao_turno((linha,coluna),turno+1))), 
            Bool(caixa_numero_posicao_turno(numero,(linha,coluna-1),turno+1))))

jogador_empurra_caixa_para_esquerda = And(*jogador_empurra_caixa_para_esquerda)

# Se o jogador empurra a caixa para a direita entao a caixa se move exatamente uma celula para a direita.

jogador_empurra_caixa_para_direita = []

for numero in range(len(caixas)):
  for turno in range(turnos):
    for linha in range(linhas):
      for coluna in range(1,colunas-1):
        jogador_empurra_caixa_para_direita.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)),
              Bool(jogador_posicao_turno((linha,coluna-1),turno)),
              Bool(jogador_posicao_turno((linha,coluna),turno+1))), 
            Bool(caixa_numero_posicao_turno(numero,(linha,coluna+1),turno+1))))

jogador_empurra_caixa_para_direita = And(*jogador_empurra_caixa_para_direita)

# Existe pelo menos um turno i onde o jogo termina.

indices_caixas = list(range(len(caixas)))

permutacoes_indices_caixas = list(permutations(indices_caixas))

existe_pelo_menos_um_turno_onde_jogo_termina = []

for turno in range(turnos+1):
  for permutacao in permutacoes_indices_caixas:
    combinacoes_indices_caixas_metas = []
    for meta in range(len(metas)):
      combinacoes_indices_caixas_metas.append(caixa_numero_posicao_turno(permutacao[meta],(metas[meta][0],metas[meta][1]),turno))
    existe_pelo_menos_um_turno_onde_jogo_termina.append(And(*combinacoes_indices_caixas_metas))

existe_pelo_menos_um_turno_onde_jogo_termina = Or(*existe_pelo_menos_um_turno_onde_jogo_termina)
    
