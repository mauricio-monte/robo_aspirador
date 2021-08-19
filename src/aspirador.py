import numpy as np

from exibicao import (
    concatenar_representacoes,
    colorir_celula,
    gerar_cabecalho_matriz
)
PISO_LIMPO = 0
OBSTACULO = 1
PISO_SUJO = 2


class Aspirador:
    posicao = [0, 0]
    
    def __init__(self, bateria, tamanho_sala):
        self.bateria = bateria
        self.piso = np.zeros(list(tamanho_sala), str)
        self.piso.fill("?")
        self.contadores = np.zeros(list(tamanho_sala), int)
        self.posicao_carregador = []
        self.possiveis_hotspots = []

    def program(self, estado_piso):
        linha = self.posicao[0]
        coluna = self.posicao[1]

        if estado_piso["cima"] in [0, 1, 2]:
            self.piso[linha - 1][coluna] = estado_piso["cima"]
        if estado_piso["direita"] in [0, 1, 2]:
            self.piso[linha][coluna + 1] = estado_piso["direita"]
        if estado_piso["baixo"] in [0, 1, 2]:
            self.piso[linha + 1][coluna] = estado_piso["baixo"] 
        if estado_piso["esquerda"] in [0, 1, 2]:
            self.piso[linha][coluna - 1] = estado_piso["esquerda"]
        if estado_piso["atual"] in [0, 1, 2]:
            self.piso[linha][coluna] = estado_piso["atual"]

        if estado_piso["atual"] == PISO_SUJO:
            return "limpar"
        return "mover"

    def mover(self, direcao="direita"):
        if self.bateria <= 0:
            return
        linha = self.posicao[0]
        coluna = self.posicao[1]
        
        if direcao == "direita":
            if coluna < len(self.piso[0]) - 1:
                self.posicao[1] += 1
            else:
                direcao = "baixo"
                self.mover("baixo")

        elif direcao == "esquerda": 
            if  coluna > 0:
                self.posicao[1] -= 1
            else:
                direcao = "cima"
                self.mover("cima")

        elif direcao == "cima": 
            if linha > 0:
                self.posicao[0] -= 1
            else:
                direcao = "direita"
                self.mover("direita")

        elif direcao == "baixo": 
            if linha < len(self.piso) - 1:
                self.posicao[0] += 1
            else:
                direcao = "esquerda"
                self.mover("esquerda")

        self.bateria -= 1
        return self.posicao, direcao

    def limpar(self, estado_do_piso):
        if self.bateria > 5:
            if estado_do_piso == PISO_SUJO:
                self.bateria -= 5

                linha = self.posicao[0]
                coluna = self.posicao[1]

                self.contadores[linha][coluna] += 1
                return True
        return False

    def get_bateria(self):
        return self.bateria

    # realizar busca heurística usando a avaliação heurística, o modelo do ambiente e a percepção corrente.
    # considerar que ele deve retornar à base quando a bateria estiver crítica

    def gerar_status(self, coordenadas_percepcao):
        """Cria representação da posição do agente, modelo interno do ambiente e os contadores"""
        representacao_modelo_interno = self.gerar_representacao_agente(coordenadas_percepcao)
        representacao_contadores = self.gerar_representacao_contadores()
        return concatenar_representacoes(representacao_modelo_interno, representacao_contadores)

    def gerar_representacao_agente(self, coordenadas_percepcao):
        representacao = gerar_cabecalho_matriz("Modelo Interno do Agente", len(self.piso[0]))

        for l, linha in enumerate(self.piso):
            representacao += f"{l}|"
            for c in range(len(linha)):
                valor_celula = self.piso[l][c]
                representacao_celula = colorir_celula(l, c, valor_celula,
                                                      self.posicao, self.posicao_carregador,
                                                      self.possiveis_hotspots, coordenadas_percepcao)
                representacao += representacao_celula
            representacao += "|\n"
        
        return representacao

    def gerar_representacao_contadores(self):
        representacao = gerar_cabecalho_matriz("Contadores", len(self.contadores[0]))

        for l, linha in enumerate(self.contadores):
            representacao += f"{l}|"
            for celula in linha:
                representacao += f"{celula:^3}"
            representacao += "|\n"
        
        return representacao
