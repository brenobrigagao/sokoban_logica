def ler_matriz(n, m):
    validos = {'S', '#', 'X', 'B', 'M', '.'}

    print(f"Digite uma matriz {n}x{m}, com caracteres separados por espaço.")
    print("Caracteres válidos: S, #, X, B, M. Use '.' para espaço em branco.")

    matriz = []
    for i in range(n):
        while True:
            entrada = input(f"Linha {i+1}: ").strip().split()
            if not all(c in validos for c in entrada):
                print("Erro: só são permitidos os caracteres S, #, X, B, M e .")
                continue
            # Substitui '.' por espaço
            entrada = [c if c != '.' else ' ' for c in entrada]
            # Preenche ou corta para garantir m elementos
            linha = entrada[:m] + [' '] * (m - len(entrada))
            matriz.append(linha)
            break

    return matriz
 
###########################################################################################################

def extrair_info(matriz):
    n = len(matriz)
    m = len(matriz[0]) if n > 0 else 0

    tamanho = (n, m)
    jogador = None
    caixas = []
    paredes = []
    metas = []

    for i in range(n):
        for j in range(m):
            valor = matriz[i][j]
            if valor == 'S':
                if jogador is not None:
                    raise ValueError("Erro: Mais de um jogador detectado (S ou X).")
                jogador = [i, j, 0]
            elif valor == 'X':  # jogador sobre meta
                if jogador is not None:
                    raise ValueError("Erro: Mais de um jogador detectado (S ou X).")
                jogador = [i, j, 0]
                metas.append([i, j])
            elif valor == 'B':
                caixas.append([i, j, 0])
            elif valor == '#':
                paredes.append([i, j])  # fixas, sem tempo
            elif valor == 'M':
                metas.append([i, j])
            # espaços ignorados

    if jogador is None:
        raise ValueError("Erro: Nenhum jogador (S ou X) encontrado na matriz.")

    return tamanho, jogador, caixas, paredes, metas

###########################################################################################################
