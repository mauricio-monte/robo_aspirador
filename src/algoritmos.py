from queue import Queue
import numpy as np
from pprint import pprint # Debug

from constantes import OBSTACULO


def zigue_zague(posicao_atual, ultima_movimentacao_executada, direcao, modelo_interno):
    """Retorna o próximo movimento que o aspirador deve fazer para
    executar um movimento de zigue zague
    
    Parâmetros:
    posicao_atual: tuple
    ultima_movimentacao_executada: str - "cima", "baixo", "direita", "esquerda"
    direcao: str - "cima", "baixo"
    modelo_interno: np.darray
    """
    linha = posicao_atual[0]
    coluna = posicao_atual[1]
    nova_direcao = direcao

    atingiu_limite_cima = (linha <= 0) 
    atingiu_limite_baixo = (linha == len(modelo_interno) - 1)
    atingiu_limite_esquerda = (coluna <= 0) 
    atingiu_limite_direita = (coluna == len(modelo_interno[0]) - 1)
    
    # Primeiro movimento da simulação
    if ultima_movimentacao_executada == "":
        if not atingiu_limite_direita:
            return nova_direcao, "direita"
        if not atingiu_limite_esquerda:
            return  nova_direcao, "esquerda"
        if not atingiu_limite_baixo:
            return  nova_direcao, "baixo"
        if not atingiu_limite_cima:
            return  nova_direcao, "cima"

    # Zigue zague
    movimento = "direita"
    if ultima_movimentacao_executada == "direita":
        if atingiu_limite_direita:
            movimento = direcao
        else:
            movimento = "direita"

    elif ultima_movimentacao_executada == "esquerda":
        if atingiu_limite_esquerda:
            movimento = direcao
        else:
            movimento = "esquerda"

    elif ultima_movimentacao_executada == direcao:
        if not atingiu_limite_direita:
            movimento = "direita"
        elif not atingiu_limite_esquerda:
            movimento = "esquerda"
        elif not atingiu_limite_cima:
            movimento = "cima"
        elif not atingiu_limite_baixo:
            movimento = "baixo"

    if movimento == "baixo" and atingiu_limite_baixo:
        nova_direcao = "cima"
        if ultima_movimentacao_executada == "esquerda":
            movimento = "direita"
        elif ultima_movimentacao_executada == "direita":
            movimento = "esquerda"

    if movimento == "cima" and atingiu_limite_cima:
        nova_direcao = "baixo"
        if ultima_movimentacao_executada == "esquerda":
            movimento = "direita"
        elif ultima_movimentacao_executada == "direita":
            movimento = "esquerda"

    return nova_direcao, movimento


def algoritmo_bfs(inicio, destino, sala):
    print("inicio", inicio)
    print("destino", destino)

    # sr = source row (linha do node inicio) sc = source column
    sr, sc = inicio[0], inicio[1]
    prev = solve(sr, sc, destino, sala)
    return reconstruir_rota(inicio, destino, prev)


def reconstruir_rota(inicio, destino, prev):
    caminho = [destino]
    
    celula = destino

    while not (celula[0] == inicio[0] and celula[1] == inicio[1]): # celula != inicio
        caminho.append(prev[celula])
        celula = prev[celula]
    
    caminho.reverse()
    return caminho[1:]


def explore_neighbours(r, c, celulas_visitadas, rq, cq, prev, sala):
    # Vetores de Direção (norte, sul, leste, oeste)
    dr = [-1, +1, 0, 0]
    dc = [0, 0, +1, -1]

    for i in range(len(dr)): # podia ser len(dc)
        rr = r + dr[i]
        cc = c + dc[i]
    
        # Não explorar casas fora dos limites da sala
        if rr < 0 or cc < 0: continue
        if rr >= len(sala) or cc >= len(sala[0]): continue
        
        # Não explorar células em que não é possível andar
        if sala[rr][cc] == OBSTACULO: continue
        
        # Não explorar células já visitadas
        if celulas_visitadas[rr][cc]: continue

        # Se passou pelos ifs, então a célula é válida, adicionar ela na lista de exploração
        rq.put(rr)
        cq.put(cc)
        prev[(rr,cc)] = (r, c)
        celulas_visitadas[rr][cc] = True           


def solve(sr, sc, fim, sala):
    chegou_ao_fim = False
    # Tem que ser do tamanho da sala
    celulas_visitadas = np.zeros([len(sala),len(sala[0])])
    # rq = fila_linha, cq = fila_coluna
    fila_linha = Queue()
    fila_coluna = Queue()

    fila_linha.put(sr)
    fila_coluna.put(sc)

    celulas_visitadas[sr][sc] = True
    
    # Cada chave é uma célula e o valor é a célula anterior que levou a exploração da célula da chave
    prev = {(lin, col): None for lin in range(len(sala)) for col in range(len(sala[0]))}    

    while fila_linha.qsize() > 0:
        lin = fila_linha.get()
        col = fila_coluna.get()

        if (lin, col) == fim:
            chegou_ao_fim = True
            break
        
        # Caso não tenha chegado ao fim, continuar exploração
        explore_neighbours(lin, col,
                           celulas_visitadas,
                           fila_linha, fila_coluna,
                           prev, sala)
        
    if chegou_ao_fim:
        return prev

    return None
