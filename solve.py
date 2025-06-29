from z3 import Solver, sat
from restrictions import *
from utils import processar_matriz, extrair_mapas_do_modelo
import time

def solve(mapa,turnos_maximos=30):
    jogador, caixas, paredes, metas, tamanho = processar_matriz(mapa)
    linhas, colunas = tamanho
    posicoes = linhas * colunas
    numero_caixas = len(caixas)

    solver = Solver()

    jogador_input = Bool(jogador_posicao_turno((jogador), 0))
    caixas_input = And([Bool(caixa_numero_posicao_turno(numero, (caixas[numero]), 0)) for numero in range(len(caixas))])
    solver.add(jogador_input)
    solver.add(caixas_input)

    for turnos in range(turnos_maximos + 1):
        print(f"\nTentando resolver com {turnos} turnos...")

        start = time.time()

        
        solver.add(
            jogador_ocupa_exatamente_uma_celula(turnos,posicoes,colunas),
            caixa_ocupa_exatamente_uma_celula(turnos,numero_caixas,posicoes,colunas),
            jogador_nao_ocupa_parede(turnos, paredes),
            caixa_nao_ocupa_caixa(turnos,numero_caixas,posicoes,colunas),
            caixa_nao_ocupa_parede(turnos,numero_caixas,paredes),
            jogador_move_exatamente_uma_celula(turnos - 1, linhas, colunas),
            caixa_repouso_ou_empurrada(numero_caixas, turnos - 1, posicoes, colunas),
            jogador_empurra_caixa_para_baixo(numero_caixas, turnos - 1, linhas, colunas),
            jogador_empurra_caixa_para_cima(numero_caixas, turnos - 1, linhas, colunas),
            jogador_empurra_caixa_para_esquerda(numero_caixas, turnos - 1, linhas, colunas),
            jogador_empurra_caixa_para_direita(numero_caixas, turnos - 1, linhas, colunas)
        )

        end = time.time()
        print(f"Tempo para processar as restrições até turno {turnos}: {end - start:.4f}")

        solver.push()
        solver.add(existe_pelo_menos_um_turno_onde_jogo_termina(turnos,numero_caixas,metas))

        start = time.time()

        if solver.check() == sat:
            modelo = solver.model()
            print(f"\n✅ Solução encontrada com {turnos} turnos!")
            mapas = extrair_mapas_do_modelo(modelo, turnos, linhas, colunas, len(caixas), paredes, metas)
            return mapas

        end = time.time()
        print(f"Tempo para fazer o check() no turno {turnos}: {end - start:.4f}")

        solver.pop()  

    print("\n❌ Nenhuma solução encontrada até o limite de turnos máximos.")
    return None


