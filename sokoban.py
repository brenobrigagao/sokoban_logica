# Importacoes

from z3 import *

from itertools import permutations

# Transforma um numero inteiro em um par ordenado de uma matriz n x m

def inteiro_para_posicao(numero, colunas):
  i = numero // colunas  
  j = numero % colunas  
  return (i, j)

# Input 

tamanho = [10,10] # [n,m]
jogador = [0,0,0] # [i,j,t]
caixas = [[1,1,0], [2,2,0], [3,3,0]] # [i,j,t]
paredes = [[4,4], [5,5], [6,6]] # [i,j]
metas = [[7,7], [8,8], [9,9]] # [i,j]
movimentos = 50

# O Jogador ocupa exatamente uma celula no turno i, para i >= 0.

jogador_ocupa_uma_celula = []

for t in range(movimentos+1):
  lista_1 = []
  for k in range(tamanho[0] * tamanho[1]):
    lista_2 = []
    for i in range(tamanho[0]):
      for j in range(tamanho[1]):
        if (inteiro_para_posicao(k,tamanho[1]) == (i,j)):
          lista_2.append(Bool(f'jogador_{i}_{j}_{t}'))
        else:
          lista_2.append(Not(Bool(f'jogador_{i}_{j}_{t}')))
    lista_1.append(And(*lista_2))
  jogador_ocupa_uma_celula.append(Or(*lista_1))

jogador_ocupa_uma_celula = And(*jogador_ocupa_uma_celula)

# A caixa c ocupa exatamente uma celula no turno i, para c >= 0 e i >= 0.

caixa_ocupa_uma_celula = []

for caixa in range(len(caixas)):
  for t in range(movimentos+1):
    lista_1 = []
    for k in range(tamanho[0] * tamanho[1]):
      lista_2 = []
      for i in range(tamanho[0]):
        for j in range(tamanho[1]):
          if (inteiro_para_posicao(k,tamanho[1]) == (i,j)):
            lista_2.append(Bool(f'caixa_{i}_{j}_{t}'))
          else:
            lista_2.append(Not(Bool(f'caixa_{i}_{j}_{t}')))
      lista_1.append(And(*lista_2))
    caixa_ocupa_uma_celula.append(Or(*lista_1))

caixa_ocupa_uma_celula = And(*caixa_ocupa_uma_celula)

# O jogador nao pode ocupar a mesma celula que uma caixa.

jogador_nao_ocupa_caixa = []

for caixa in range(len(caixas)):
  for t in range(movimentos+1): 
    for k in range(tamanho[0] * tamanho[1]):
      jogador_nao_ocupa_caixa.append(Not(And(Bool(f'jogador({i},{j},{t})'), Bool(f'caixa_{caixa}({i},{j},{t})')))) # ajeitar 

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

# Existe exatamente um turno i onde cada caixa c ocupa exatamente uma meta, para c >= 0.

existe_um_turno_onde_cada_caixa_ocupa_uma_meta = []

permutacoes = [list(p) for p in permutations(range(len(caixas)))] # as caixas sao numeradas de 0 a len(caixas) - 1, permuto essa lista de numeros distintos.

for t1 in range(movimentos+1):
  for t2 in range(t1,movimentos+1):
    for permutacao in permutacoes:
      lista = []
      for p in range(len(permutacao)): 
        lista.append(Bool(f'caixa_{permutacao[p]}({metas[p][0]},{metas[p][1]},{t2})'))
    if (t1 == t2):
      existe_um_turno_onde_cada_caixa_ocupa_uma_meta.append((And(*lista)))
    else:
      existe_um_turno_onde_cada_caixa_ocupa_uma_meta.append(Not(And(*lista)))

existe_um_turno_onde_cada_caixa_ocupa_uma_meta = Or(*existe_um_turno_onde_cada_caixa_ocupa_uma_meta)