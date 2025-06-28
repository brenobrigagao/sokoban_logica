from z3 import Bool

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

# Função para ler matriz retangular

def ler_matriz():
  matriz = []
  print("Digite as linhas da matriz (pressione ENTER em branco para terminar):")
  while True:
    linha = input()
    if not linha: break
    matriz.append(list(linha))
    if len(set(len(l) for l in matriz)) > 1: raise ValueError("A matriz não é retangular! Todas as linhas devem ter o mesmo número de caracteres.")
    return matriz
  
# Função para extrair jogador, caixas, paredes e metas da matriz lida

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
            elif char == '.' or char == ' ':
                pass  # espaço vazio
            elif char == 'S':
                jogador = [linha_idx, coluna_idx]
            elif char == 'B':
                caixas.append([linha_idx, coluna_idx])
            elif char == 'm':
                metas.append([linha_idx, coluna_idx])
            elif char == 'x':
                jogador = [linha_idx, coluna_idx]
                metas.append([linha_idx, coluna_idx])
            else:
                raise ValueError(f"Caractere inválido encontrado: '{char}' na posição ({linha_idx}, {coluna_idx})")

    return jogador, caixas, paredes, metas, tamanho

# Função para extrair a sequencia de matrizes que representa a solucao do sokoban

def extrair_mapas_do_modelo(modelo, turnos, linhas, colunas, num_caixas, paredes=[], metas=[]):
    mapas = []

    for turno in range(turnos+1):
        # cria o mapa base (pontos)
        mapa = [['.' for _ in range(colunas)] for _ in range(linhas)]

        # coloca paredes
        for (linha, coluna) in paredes:
            mapa[linha][coluna] = '#'

        # coloca metas (se quiser diferenciar, opcional)
        for (linha, coluna) in metas:
            if mapa[linha][coluna] == '.':
                mapa[linha][coluna] = 'm'

        # procura jogador
        for linha in range(linhas):
            for coluna in range(colunas):
                nome_bool = f'jogador({linha},{coluna},{turno})'
                if modelo.eval(Bool(nome_bool), False):
                    if mapa[linha][coluna] == 'm':
                        mapa[linha][coluna] = 'x'  # jogador em cima de meta
                    else:
                        mapa[linha][coluna] = 'S'

        # procura caixas
        for numero in range(num_caixas):
            for linha in range(linhas):
                for coluna in range(colunas):
                    nome_bool = f'caixa_{numero}({linha},{coluna},{turno})'
                    if modelo.eval(Bool(nome_bool), False):
                        if mapa[linha][coluna] == 'm':
                            mapa[linha][coluna] = 'b'  # caixa em cima de meta
                        else:
                            mapa[linha][coluna] = 'B'

        mapas.append(mapa)

    return mapas

# Função que imprime de forma elegante a solução do sokoban

def imprimir_solucao(mapas_turnos):
    """
    Recebe uma lista de mapas (listas de listas de chars) e imprime cada mapa
    representando o estado do Sokoban em cada turno, de forma elegante.
    """
    if mapas_turnos is None:
        return
    for turno, mapa in enumerate(mapas_turnos):
        print(f"\n{'='*10} Turno {turno} {'='*10}")
        for linha in mapa:
            print(''.join(linha))
    print(f"\n{'='*30}\n")