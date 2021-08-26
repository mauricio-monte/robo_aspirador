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
    acoes = ["cima", "baixo", "esquerda", "direita", "aspirar", "recarregar"]
    direcao = "baixo" # Diz se o robo está subindo ou descendo no zig zague
    ultima_movimentacao_executada = ""

    def __init__(self, bateria, tamanho_sala):
        self.bateria = bateria
        self.piso = np.zeros(list(tamanho_sala), str)
        self.piso.fill("?")
        self.contadores = np.zeros(list(tamanho_sala), int)
        self.posicao_carregador = []
        self.possiveis_hotspots = []

    def atualiza_modelo_interno(self, percepcao):
        """Atualiza o modelo interno do ambiente que o agente possui"""
        linha = self.posicao[0]
        coluna = self.posicao[1]

        if percepcao["cima"] == OBSTACULO:
            self.piso[linha - 1][coluna] = percepcao["cima"]
        if percepcao["direita"] == OBSTACULO:
            self.piso[linha][coluna + 1] = percepcao["direita"]
        if percepcao["baixo"] == OBSTACULO:
            self.piso[linha + 1][coluna] = percepcao["baixo"] 
        if percepcao["esquerda"] == OBSTACULO:
            self.piso[linha][coluna - 1] = percepcao["esquerda"]
        if percepcao["atual"] in {PISO_LIMPO, PISO_SUJO, OBSTACULO}:
            self.piso[linha][coluna] = percepcao["atual"]
    
    def program(self, estado_piso):
        """Retorna a próxima ação do agente com nas suas percepções
        e no seu estado atual"""
        self.atualiza_modelo_interno(estado_piso)

        if estado_piso["atual"] == PISO_SUJO:
            return "limpar"
        else:
            movimento = self.zigue_zague()
            return movimento
    

    def zigue_zague(self):
        """Retorna o próximo movimento que o aspirador deve fazer para
        executar um movimento de zigue zague"""
        linha = self.posicao[0]
        coluna = self.posicao[1]
        
        atingiu_limite_cima = (linha <= 0) or (self.piso[linha - 1][coluna] == '1')
        atingiu_limite_baixo = (linha == len(self.piso) - 1) or (self.piso[linha + 1][coluna] == '1')
        atingiu_limite_esquerda = (coluna <= 0) or (self.piso[linha][coluna - 1] == '1')
        atingiu_limite_direita = (coluna == len(self.piso[0]) - 1) or (self.piso[linha][coluna + 1] == '1')
        
        # Primeiro movimento da simulação
        if self.ultima_movimentacao_executada == "":
            if not atingiu_limite_direita:
                return "direita"
            if not atingiu_limite_esquerda:
                return "esquerda"
            if not atingiu_limite_baixo:
                return "baixo"
            if not atingiu_limite_cima:
                return "cima"

        # Zigue zague
        movimento = "direita"
        if self.ultima_movimentacao_executada == "direita":
            if atingiu_limite_direita:
                movimento = self.direcao
            else:
                movimento = "direita"

        elif self.ultima_movimentacao_executada == "esquerda":
            if atingiu_limite_esquerda:
                movimento = self.direcao
            else:
                movimento = "esquerda"

        elif self.ultima_movimentacao_executada == self.direcao:
            if not atingiu_limite_direita:
                movimento = "direita"
            elif not atingiu_limite_esquerda:
                movimento = "esquerda"
            elif not atingiu_limite_cima:
                movimento = "cima"
            elif not atingiu_limite_baixo:
                movimento = "baixo"

        if movimento == "baixo" and atingiu_limite_baixo:
            self.direcao = "cima"
            if self.ultima_movimentacao_executada == "esquerda":
                movimento = "direita"
            elif self.ultima_movimentacao_executada == "direita":
                movimento = "esquerda"

        if movimento == "cima" and atingiu_limite_cima:
            self.direcao = "baixo"
            if self.ultima_movimentacao_executada == "esquerda":
                movimento = "direita"
            elif self.ultima_movimentacao_executada == "direita":
                movimento = "esquerda"

        return movimento
        
    def mover(self, acao):
        if self.bateria <= 0:
            return
        
        if acao == "direita":
            self.posicao[1] += 1

        elif acao == "esquerda": 
            self.posicao[1] -= 1

        elif acao == "cima": 
            self.posicao[0] -= 1

        elif acao == "baixo": 
            self.posicao[0] += 1

        if not self.desviando:
            self.ultima_movimentacao_executada = acao
        self.bateria -= 1
        return self.posicao, acao

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

    def adiciona_posicao_carregador(self, linha, coluna):
        self.posicao_carregador = [linha, coluna]

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
