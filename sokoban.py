# Importações

from z3 import *

from itertools import permutations

# Transforma um numero inteiro em um par ordenado de uma matriz n x m

def posicao_1D_para_posicao_2D(posicao_1D, colunas):
  i = posicao_1D // colunas  
  j = posicao_1D % colunas  
  return (i,j)

# Função para criar um Bool que representa a coordenada espaço-temporal do jogador (i,j,t).

def jogador_posicao_turno(posicao, turno):
  return f'jogador({posicao[0]},{posicao[1]},{turno})'

# Função para criar um Bool que representa a coordenada espaço-temporal de uma caixa (i,j,t).

def caixa_numero_posicao_turno(numero, posicao, turno):
  return f'caixa_{numero}({posicao[0]},{posicao[1]},{turno})'

# Input 

tamanho = [10,10]
posicoes = linhas * colunas 
jogador = [0,0,0]
caixas = [[1,1,0], [2,2,0], [3,3,0]]
paredes = [[4,4], [5,5], [6,6]] 
metas = [[7,7], [8,8], [9,9]] 
movimentos = 50
turnos = 50


# O Jogador ocupa exatamente uma celula no turno i, para i >= 0.

jogador_ocupa_exatamente_uma_celula = []

for turno in range(movimentos+1):
  bools = [Bool(jogador_posicao_turno((posicao_1D_para_posicao_2D(posicao)[0],posicao_1D_para_posicao_2D(posicao)[1]),turno)) for posicao in range(posicoes)]
  soma = Sum([If(b,1,0) for b in bools])
  jogador_ocupa_exatamente_uma_celula.append(soma == 1)

jogador_ocupa_exatamente_uma_celula = And(*jogador_ocupa_exatamente_uma_celula)
  
# A caixa c ocupa exatamente uma celula no turno i, para c >= 0 e i >= 0.

caixa_ocupa_exatamente_uma_celula = []

for numero in range(len(caixas)):
  for turno in range(movimentos+1):
    bools = [Bool(caixa_numero_posicao_turno(numero,(posicao_1D_para_posicao_2D(posicao)[0],posicao_1D_para_posicao_2D(posicao)[1]),turno)) for posicao in range(posicoes)]
    soma = Sum([If(b,1,0) for b in bools]) 
    caixa_ocupa_exatamente_uma_celula.append(soma == 1)

caixa_ocupa_exatamente_uma_celula = And(*caixa_ocupa_exatamente_uma_celula)

# O jogador nao pode ocupar a mesma celula que uma caixa.

jogador_nao_ocupa_caixa = []

for numero in range(len(caixas)):
  for turno in range(movimentos+1): 
    for posicao in range(posicoes):
      jogador_nao_ocupa_caixa.append(Not(And(Bool(jogador_posicao_turno(posicao_1D_para_posicao_2D(), posicao_1D_para_posicao_2D),turno))) 

jogador_nao_ocupa_caixa = And(*jogador_nao_ocupa_caixa)

# O jogador nao pode ocupar a mesma celula que uma parede.

jogador_nao_ocupa_parede = []

for parede in paredes:
  for t in range(movimentos+1):
         jogador_nao_ocupa_parede.append(Not(Bool(f'jogador({parede[0]},{parede[1]},{t})'))) 

jogador_nao_ocupa_parede = And(*jogador_nao_ocupa_parede)

# Duas caixas nao podem ocupar a mesma celula.

caixa_nao_ocupa_caixa = []

for caixa in range(len(caixas)):
  for t in range(movimentos+1):
   for k in range(tamanho[0] * tamanho[1]):
    caixa_nao_ocupa_caixa.append(Not(And(Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'caixa_{caixa}({i},{j},{t})'))))

# Uma caixa nao pode ocupar a mesma celula que uma parede.

caixa_nao_ocupa_parede = []

for caixa in len(caixas):
  for parede in paredes:
    for t in range(movimentos+1):
       caixa_nao_ocupa_parede.append(Not(Bool(f'caixa({parede[0]},{parede[1]},{t})'))) 

caixa_nao_ocupa_parede = And(*caixa_nao_ocupa_parede)

# O jogador se move exatamente uma celula por turno.

jogador_move_uma_celula = []

for t in range(movimentos):
  lista_1 = []
  for k in range(tamanho[0] * tamanho[1]):
    lista_2 = []
    for l in range(tamanho[0] * tamanho[1]):
      if (abs(inteiro_para_posicao(k) - inteiro_para_posicao(l)) in [(0,1), (1,0)]):
        lista_2.append(Not(And(Bool(f'jogador({inteiro_para_posicao(k)[0]},{inteiro_para_posicao(k)[1]},{t})'), Bool(f'jogador({inteiro_para_posicao(l)[0]},{inteiro_para_posicao(l)[1]},{t+1})'))))


# Ou uma caixa permanece em repouso durante dois turnos consecutivos Ou o jogador empurra a caixa.

caixa_repouso_ou_empurrada = []

for caixa in range(len(caixas)):
  for t in range(movimentos):
    for i in range(tamanho[0]):
      for j in range(tamanho[1]):
        caixa_repouso_ou_empurrada.append(Xor(And(Bool(f'jogador({i},{j},{t+1})'), Bool(f'caixa_{caixa}({i},{j},{t})')), And(Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'caixa_{caixa}({i},{j},{t+1})')))) # type: ignore

caixa_repouso_ou_empurrada = And(*caixa_repouso_ou_empurrada)

# Se o jogador empurra a caixa para cima entao ela se move exatamente uma celula para cima.

caixa_empurrada_cima = []

for caixa in range(len(caixas)):
  for t in range(movimentos):
    for i in range(1,tamanho[0]-1):
      for j in range(tamanho[1]):
        caixa_empurrada_cima.append(Implies(And(Bool(f'jogador({i},{j},{t+1})'), Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'jogador({i},{j},{t+1})')), Bool()))

caixa_empurrada_cima = And(*caixa_empurrada_cima)

# Se o jogador empurra a caixa para cima entao ela se move exatamente uma celula para cima.


caixa_empurrada_baixo = []

for caixa in range(len(caixas)):
  for t in range(movimentos):
    for i in range(1,tamanho[0]-1):
      for j in range(tamanho[1]):
        caixa_empurrada_baixo.append(Implies(And(Bool(f'jogador({i},{j},{t+1})'), Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'jogador({i},{j},{t+1})')), Bool()))

caixa_empurrada_baixo = And(*caixa_empurrada_baixo)

# Se o jogador empurra a caixa para cima entao ela se move exatamente uma celula para cima.


caixa_empurrada_esquerda = []

for caixa in range(len(caixas)):
  for t in range(movimentos):
    for i in range(1,tamanho[0]-1):
      for j in range(tamanho[1]):
        caixa_empurrada_baixo.append(Implies(And(Bool(f'jogador({i},{j},{t+1})'), Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'jogador({i},{j},{t+1})')), Bool())) # type: ignore

caixa_empurrada_esquerda = And(*caixa_empurrada_esquerda)

# Se o jogador empurra a caixa para cima entao ela se move exatamente uma celula para cima.


caixa_empurrada_direita = []

for caixa in range(len(caixas)):
  for t in range(movimentos):
    for i in range(1,tamanho[0]-1):
      for j in range(tamanho[1]):
        caixa_empurrada_baixo.append(Implies(And(Bool(f'jogador({i},{j},{t+1})'), Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'jogador({i},{j},{t+1})')), Bool()))

caixa_empurrada_direita = And(*caixa_empurrada_direita)

