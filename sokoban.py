# Instala e Importa o Z3

!pip install z3-solver
from z3 import *

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

# Variaveis
 
jogador_i_j_t = []

for t in range(movimentos+1):
  for i in range(tamanho[0]):
    for j in range(tamanho[1]):
      jogador_i_j_t.append(Bool(f'jogador({i},{j},{t})'))

caixa_id_i_j_t = []

for caixa in range(len(caixas)):
  for t in range(movimentos+1):
    for i in range(tamanho[0]):
      for j in range(tamanho[1]):
        caixa_id_i_j_t.append(Bool(f'caixa_{caixa}({i},{j},{t})'))

# O Jogador ocupa exatamente uma celula em ti, para i >= 0.

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

#  A caixa c ocupa exatamente uma celula em ti, para i >= 0, c >= 0.

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

caixa_ocupa_uma_celula = And(*jogador_ocupa_uma_celula)

# O jogador nao pode ocupar a mesma celula que uma caixa

jogador_nao_ocupa_caixa = []

for caixa in range(len(caixas)):
  for t in range(movimentos+1): 
    for k in range(tamanho[0] * tamanho[1]):
      jogador_nao_ocupa_caixa.append(Not(And(Bool(f'jogador({i},{j},{t})'), Bool(f'caixa_{caixa}({i},{j},{t})')))) # ajeitar 

jogador_nao_ocupa_caixa = And(*jogador_nao_ocupa_caixa)

# O jogador nao pode ocupar a mesma celula que uma parede

jogador_nao_ocupa_parede = []

for parede in paredes:
  for t in range(movimentos+1):
         jogador_nao_ocupa_parede.append(Not(Bool(f'jogador({parede[0]},{parede[1]},{t})'))) 

jogador_nao_ocupa_parede = And(*jogador_nao_ocupa_parede)

# Duas caixas nao podem ocupar o mesmo espaco

caixa_nao_ocupa_caixa = []

for caixa in range(len(caixas)):
  for t in range(movimentos+1):
   for k in range(tamanho[0] * tamanho[1]):
    caixa_nao_ocupa_caixa.append(Not(And(Bool(f'caixa_{caixa}({i},{j},{t})'), Bool(f'caixa_{caixa}({i},{j},{t})'))))

# Uma caixa nao pode ocupar uma celula com uma parede

caixa_nao_ocupa_parede = []

for caixa in len(caixas):
  for parede in paredes:
    for t in range(movimentos+1):
       caixa_nao_ocupa_parede.append(Not(Bool(f'caixa({parede[0]},{parede[1]},{t})'))) 

caixa_nao_ocupa_parede = And(*caixa_nao_ocupa_parede)

# Um jogador se move uma unica celula por turno.

jogador_move_uma_celula = []

for t in range(movimentos):
  lista_1 = []
  for k in range(tamanho[0] * tamanho[1]):
    lista_2 = []
    for l in range(tamanho[0] * tamanho[1]):
      if (abs(inteiro_para_posicao(k) - inteiro_para_posicao(l)) in [(0,1), (1,0)]):
        lista_2.append(Not(And(Bool(f'jogador({inteiro_para_posicao(k)[0]},{inteiro_para_posicao(k)[1]},{t})'), Bool(f'jogador({inteiro_para_posicao(l)[0]},{inteiro_para_posicao(l)[1]},{t+1})'))))


# Uma caixa se move se e somente se um jogador se move para sua celula, ela se move para aonde o joagdor anda.

# ????????????

# Existe pelo menos um ti onde cada caixa c ocupa uma meta, para i >= 0.

