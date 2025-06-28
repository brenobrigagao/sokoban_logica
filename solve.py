from z3 import Solver, sat
from restrictions import *
from utils import processar_matriz, extrair_mapas_do_modelo

def solve(mapa, turnos_maximos=30):
    jogador, caixas, paredes, metas, tamanho = processar_matriz(mapa)
    linhas, colunas = tamanho
    posicoes = linhas * colunas

    for turnos in range(turnos_maximos + 1):
        print(f"Tentando resolver com {turnos} turnos...")

        solver = Solver()

        jogador_input = Bool(jogador_posicao_turno((jogador),0))
        caixas_input = And([Bool(caixa_numero_posicao_turno(numero,(caixas[numero]),0)) for numero in range(len(caixas))])

        # Adiciona Input

        solver.add(jogador_input)
        solver.add(caixas_input)

        # Adiciona todas as restrições ao solver
        solver.add(
            jogador_ocupa_exatamente_uma_celula(turnos, posicoes, colunas),
            caixa_ocupa_exatamente_uma_celula(caixas, turnos, posicoes, colunas),
            jogador_nao_ocupa_caixa(caixas, turnos, posicoes, colunas),
            jogador_nao_ocupa_parede(turnos, paredes),
            caixa_nao_ocupa_caixa(caixas, turnos, posicoes,colunas),
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
            mapas = extrair_mapas_do_modelo(modelo,turnos,linhas,colunas,len(caixas),paredes,metas)
            return mapas

    print("Não foi possível encontrar solução dentro do limite de turnos.")
    return None

