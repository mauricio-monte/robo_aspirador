import time
import numpy as np
from random import random
from constantes import OBSTACULO, PISO_SUJO

from exibicao import (
    concatenar_representacoes,
    colorir_celula,
    gerar_cabecalho_matriz,
    gerar_titulo
)


class Sala:
    probabilidade_de_sujeira = 0.0005
    probabilidade_de_sujeira_hot_spot = 0.15

    def __init__(self, tamanho_sala, posicoes_obstaculos, posicoes_hot_spots,
                 aspirador, posicao_aspirador, posicao_carregador):
        self.agente = aspirador
        self.piso = np.zeros(tamanho_sala, int)
        self.posicao_agente = posicao_aspirador
        self.posicoes_hot_spots = posicoes_hot_spots
        self.posicao_carregador = posicao_carregador
        self.agente.adiciona_posicao_carregador(posicao_carregador[0], posicao_carregador[1])
        self.adicionar_obstaculos(posicoes_obstaculos)

    def recuperar_estado_celula(self, linha, coluna):
        """Mostra o que tem uma célula da sala em uma determinada posição"""       
        if coluna >= 0 and linha >= 0:
            if len(self.piso) > linha and len(self.piso[0]) > coluna:
                return self.piso[linha][coluna]
        return -1
    
    def sujar_sala(self):
        """Coloca sujeira nas células da sala aleatoriamente"""
        for l in range(len(self.piso)):
            for c in range(len(self.piso[0])):
                celula_eh_obstaculo = self.piso[l][c] == OBSTACULO
                eh_hot_spot = (l, c) in self.posicoes_hot_spots
                if not celula_eh_obstaculo:
                    if self.celula_vai_ter_sujeira(eh_hot_spot):
                        self.adicionar_sujeira(l, c)

    def celula_vai_ter_sujeira(self, hot_spot):
        """Sorteia se uma celula terá sujeira ou não"""
        numero_sorteado = random()
        if hot_spot:
            return numero_sorteado <= self.probabilidade_de_sujeira_hot_spot
        else:
            return numero_sorteado <= self.probabilidade_de_sujeira

    def adicionar_sujeira(self, linha, coluna):
        """Adiciona sujeira em uma determinada célula da sala"""
        self.piso[linha][coluna] = 2

    def adicionar_obstaculos(self, posicoes_obstaculos):
        """Marca as células das sala que devem ser obstáculos"""
        for coordenada in posicoes_obstaculos:
            linha = coordenada[0]
            coluna = coordenada[1]
            self.piso[linha][coluna] = 1

    def remover_sujeira(self, linha, coluna):
        """Remove sujeira de uma determinada célula da sala"""
        self.piso[linha][coluna] = 0

    def percept(self, posicao_agente):
        """Mostra para o agente o estado do piso na posição dele"""
        linha = posicao_agente[0]
        coluna = posicao_agente[1]
        
        return {
            "atual": self.recuperar_estado_celula(linha, coluna),
            "cima": self.recuperar_estado_celula(linha - 1, coluna),
            "direita": self.recuperar_estado_celula(linha, coluna + 1),
            "baixo": self.recuperar_estado_celula(linha + 1, coluna),
            "esquerda": self.recuperar_estado_celula(linha, coluna - 1)
        }

    def step(self):
        """Executa um passo da simulação do ambiente"""
        estado_pisos_percepcao = self.percept(self.posicao_agente)
        acao_agente = self.agente.program(estado_pisos_percepcao)
        self.executar_acao(self.agente, acao_agente)
        self.sujar_sala()


    def run(self, steps=50):
        """Chama step N vezes para simular o agente e o seu ambiente"""
        self.imprimir_estado_simulacao("Estado Inicial")

        for step in range(steps):
            if self.agente.bateria <= 0:
                return
            
            self.step()
            self.imprimir_estado_simulacao(step)

    def executar_acao(self, agente, action):
        """Muda o estado do ambiente de acordo com as ações executadas pelo agente"""
        if action == "cima":
            self.posicao_agente = list(agente.mover(action))
        elif action == "baixo":
            self.posicao_agente = list(agente.mover(action))
        elif action == "esquerda":
            self.posicao_agente = list(agente.mover(action))
        elif action == "direita":
            self.posicao_agente = list(agente.mover(action))

        elif action == "limpar":
            linha = agente.linha
            coluna = agente.coluna
            estado_do_piso = self.recuperar_estado_celula(linha, coluna)
            if estado_do_piso == PISO_SUJO:
                self.remover_sujeira(linha, coluna)
                agente.limpar(estado_do_piso)
        
        elif action == "recarregar":
            self.agente.recarregar()

    def imprimir_estado_simulacao(self, step):
        sala = self.gerar_representacao_sala()
        agente = self.agente.gerar_status()
        print(gerar_titulo(f"Step {step}", (len(self.piso[0]) + 2) * 3))
        print(f'Agente: (Linha = {self.posicao_agente[0]}, Coluna = {self.posicao_agente[1]}) / Modo = {self.agente.modo_operacao} / Bateria = {self.agente.bateria}')
        print(concatenar_representacoes(sala, agente))
        time.sleep(0.1)

    def gerar_representacao_sala(self):
        representacao = gerar_cabecalho_matriz("Sala", len(self.piso[0]))

        for l, linha in enumerate(self.piso):
            representacao += f"{l}|"
            for c in range(len(linha)):
                valor_celula = self.piso[l][c]
                representacao_celula = colorir_celula(
                    l, c, valor_celula,
                    self.posicao_agente, self.posicao_carregador,
                    self.posicoes_hot_spots)
                representacao += representacao_celula
            representacao += "|\n"

        return representacao
