from z3 import Bool, And, Or, Not, Sum, If, Implies
from utils import posicao_1D_para_posicao_2D, jogador_posicao_turno, caixa_numero_posicao_turno
from itertools import permutations

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

def caixa_nao_ocupa_caixa(caixas,turnos,posicoes,colunas):
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

# Ou uma caixa permanece parada durante dois turnos consecutivos Ou o jogador empurra a caixa. (Consertadad)

def caixa_repouso_ou_empurrada(caixas,turnos,linhas,colunas):
    restricoes = []
    for numero in range(len(caixas)):
        for turno in range(turnos):
            for linha in range(linhas):
                for coluna in range(colunas):
                    # Se a caixa está em (linha,coluna) no turno t
                    # então no turno t+1 ela deve:
                    # 1) permanecer no mesmo lugar, OU
                    # 2) ter sido empurrada pelo jogador
                    restricoes.append(
                        Implies(
                            Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno)),
                            Or(
                                Bool(caixa_numero_posicao_turno(numero,(linha,coluna),turno+1)),
                                And(
                                    Bool(jogador_posicao_turno((linha,coluna),turno+1)),
                                    Or(
                                        # Empurrada para cima
                                        And(linha > 0, 
                                            Bool(caixa_numero_posicao_turno(numero,(linha-1,coluna),turno+1))),
                                        # Empurrada para baixo
                                        And(linha < linhas-1, 
                                            Bool(caixa_numero_posicao_turno(numero,(linha+1,coluna),turno+1))),
                                        # Empurrada para esquerda
                                        And(coluna > 0, 
                                            Bool(caixa_numero_posicao_turno(numero,(linha,coluna-1),turno+1))),
                                        # Empurrada para direita
                                        And(coluna < colunas-1, 
                                            Bool(caixa_numero_posicao_turno(numero,(linha,coluna+1),turno+1)))
                                    )
                                )
                            )
                        )
                    )
    return And(*restricoes)

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