from z3 import Bool, And, Or, Not, Sum, If, Implies, Xor
from utils import posicao_1D_para_2D, jogador_posicao_turno, caixa_numero_posicao_turno
from itertools import combinations

# O jogador ocupa exatamente uma celula no turno i, para i >= 0

def jogador_ocupa_exatamente_uma_celula(turno,posicoes,colunas): 
  bools = [Bool(jogador_posicao_turno(posicao_1D_para_2D(posicao,colunas),turno)) for posicao in range(posicoes)]
  soma = Sum([If(b,1,0) for b in bools])
  return soma == 1
  
# A caixa c ocupa exatamente uma celula no turno i, para c >= 0 e i >= 0

def caixa_ocupa_exatamente_uma_celula(turno,numero_caixas,posicoes,colunas):
  ands = []
  for numero in range(numero_caixas):
    bools = [Bool(caixa_numero_posicao_turno(numero,posicao_1D_para_2D(posicao,colunas),turno)) for posicao in range(posicoes)]
    soma = Sum([If(b,1,0) for b in bools]) 
    ands.append(soma == 1)
  return And(*ands)

# O jogador nao pode ocupar a mesma celula que uma parede.

def jogador_nao_ocupa_parede(turno,paredes):
  ands = [Not(Bool(jogador_posicao_turno(parede,turno))) for parede in paredes]
  return And(*ands)

# Uma caixa nao pode ocupar a mesma celula que uma parede.

def caixa_nao_ocupa_parede(turno,numero_caixas,paredes):
  ands = []
  for numero in range(numero_caixas): ands.append(And(*[Not(Bool(caixa_numero_posicao_turno(numero,parede,turno))) for parede in paredes]))   
  return And(*ands)

# Duas caixas nao podem ocupar a mesma celula. 

def caixa_nao_ocupa_caixa(turno,numero_caixas,posicoes,colunas):
  numeros_caixas = list(range(numero_caixas))
  pares_numeros_caixas = list(combinations(numeros_caixas,2))
  ands = []
  for par in pares_numeros_caixas: 
    for posicao in range(posicoes):
      ands.append(
        Not(
          And(
            Bool(caixa_numero_posicao_turno(par[0],posicao_1D_para_2D(posicao,colunas),turno)),
            Bool(caixa_numero_posicao_turno(par[1],posicao_1D_para_2D(posicao,colunas),turno)))))
  return And(*ands)

# O jogador se move exatamente uma celula por turno.

def jogador_move_exatamente_uma_celula(turno,linhas,colunas):
  ands = []
  for linha in range(linhas):
    for coluna in range(colunas):
      movimentos_validos = []
      if (linha - 1 >= 0): movimentos_validos.append(Bool(jogador_posicao_turno((linha-1,coluna),turno+1)))
      if (linha + 1 < linhas): movimentos_validos.append(Bool(jogador_posicao_turno((linha+1,coluna),turno+1)))
      if (coluna - 1 >= 0): movimentos_validos.append(Bool(jogador_posicao_turno((linha,coluna-1),turno+1)))
      if (coluna + 1 < colunas): movimentos_validos.append(Bool(jogador_posicao_turno((linha,coluna+1),turno+1)))
      ands.append(
        Implies(
          Bool(jogador_posicao_turno((linha,coluna),turno)),
          Or(*movimentos_validos)))
  return And(*ands) if ands else True

# Ou uma caixa permanece parada durante dois turnos consecutivos Ou o jogador empurra a caixa. (Consertadad)

def caixa_repouso_ou_empurrada(numero_caixas,turno,posicoes,colunas):
    ands = []
    for numero in range(numero_caixas):
      for posicao in range(posicoes):
        ands.append(
          Implies(
            Bool(caixa_numero_posicao_turno(numero,posicao_1D_para_2D(posicao,colunas),turno)),
            Xor(
              Bool(caixa_numero_posicao_turno(numero,posicao_1D_para_2D(posicao,colunas),turno+1)),
              Bool(jogador_posicao_turno(posicao_1D_para_2D(posicao,colunas),turno+1)))))
    return And(*ands) if ands else True

# Se o jogador empurra a caixa para baixo entao a caixa se move exatamente uma celula para baixo.

def jogador_empurra_caixa_para_baixo(numero_caixas, turno, linhas, colunas):
    ands = []
    for numero in range(numero_caixas):
      for linha in range(1, linhas - 1):
          for coluna in range(colunas):
              ands.append(
                Implies(
                  And(
                    Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
                    Bool(jogador_posicao_turno((linha - 1, coluna), turno)),
                    Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
                  Bool(caixa_numero_posicao_turno(numero, (linha + 1, coluna), turno + 1))))
    return And(*ands) if ands else True

# Se o jogador empurra a caixa para cima entao a caixa se move exatamente uma celula para cima.

def jogador_empurra_caixa_para_cima(numero_caixas, turno, linhas, colunas):
  ands = []
  for numero in range(numero_caixas):
    for linha in range(1, linhas - 1):
      for coluna in range(colunas):
        ands.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
              Bool(jogador_posicao_turno((linha + 1, coluna), turno)),
              Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
            Bool(caixa_numero_posicao_turno(numero, (linha - 1, coluna), turno + 1))))
  return And(*ands) if ands else True

# Se o jogador empurra a caixa para a esquerda entao a caixa se move exatamente uma celula para a esquerda.

def jogador_empurra_caixa_para_esquerda(numero_caixas,turno,linhas,colunas):
  ands = []
  for numero in range(numero_caixas):
    for linha in range(linhas):
      for coluna in range(1, colunas - 1):
        ands.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
              Bool(jogador_posicao_turno((linha, coluna + 1), turno)),
              Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
            Bool(caixa_numero_posicao_turno(numero, (linha, coluna - 1), turno + 1))))
  return And(*ands) if ands else True

# Se o jogador empurra a caixa para a direita entao a caixa se move exatamente uma celula para a direita.

def jogador_empurra_caixa_para_direita(numero_caixas,turno,linhas,colunas):
  ands = []
  for numero in range(numero_caixas):
    for linha in range(linhas):
      for coluna in range(1, colunas - 1):
        ands.append(
          Implies(
            And(
              Bool(caixa_numero_posicao_turno(numero, (linha, coluna), turno)),
              Bool(jogador_posicao_turno((linha, coluna - 1), turno)),
              Bool(jogador_posicao_turno((linha, coluna), turno + 1))),
            Bool(caixa_numero_posicao_turno(numero, (linha, coluna + 1), turno + 1))))
  return And(*ands) if ands else True

# Existe pelo menos um turno i onde o jogo termina.

def existe_pelo_menos_um_turno_onde_jogo_termina(turno,numero_caixas,metas):
  ands = []
  for meta in metas:
    ors = [Bool(caixa_numero_posicao_turno(numero,meta,turno)) for numero in range(numero_caixas)]
    ands.append(Or(*ors))
  return And(*ands) 