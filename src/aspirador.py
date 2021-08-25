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

    def program(self, estado_piso):
        linha = self.posicao[0]
        coluna = self.posicao[1]

        # Atualiza o modelo interno
        if estado_piso["cima"] == OBSTACULO:
            self.piso[linha - 1][coluna] = estado_piso["cima"]
        if estado_piso["direita"] == OBSTACULO:
            self.piso[linha][coluna + 1] = estado_piso["direita"]
        if estado_piso["baixo"] == OBSTACULO:
            self.piso[linha + 1][coluna] = estado_piso["baixo"] 
        if estado_piso["esquerda"] == OBSTACULO:
            self.piso[linha][coluna - 1] = estado_piso["esquerda"]
        if estado_piso["atual"] in [0, 1, 2]:
            self.piso[linha][coluna] = estado_piso["atual"]

        # Retorna ação
        if estado_piso["atual"] == PISO_SUJO:
            return "limpar"
        else:
            atingiu_limite_cima = linha == 0
            atingiu_limite_baixo = linha == len(self.piso) - 1
            atingiu_limite_esquerda = coluna == 0
            atingiu_limite_direita = coluna == len(self.piso[0]) - 1
           
            # Primeiro movimento da simulação
            if self.ultima_movimentacao_executada == "":
                return "direita"

            # Zigue zague
            movimento = "?"            
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
                if atingiu_limite_direita:
                    movimento = "esquerda"
                elif atingiu_limite_esquerda:
                    movimento = "direita"

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

            print({
                "direcao": self.direcao,
                "ultima mov": self.ultima_movimentacao_executada,
                "lim direita": atingiu_limite_direita,
                "lim esquerda": atingiu_limite_esquerda,
                "lim baixo": atingiu_limite_baixo,
                "lim cima": atingiu_limite_cima,
                "coluna": coluna,
                "linha": linha,
                "movimento": movimento
            })
            return movimento


    def mover(self, acao):
        if self.bateria <= 0:
            return
        linha = self.posicao[0]
        coluna = self.posicao[1]
        
        if acao == "direita":
            self.posicao[1] += 1

        elif acao == "esquerda": 
            self.posicao[1] -= 1

        elif acao == "cima": 
            self.posicao[0] -= 1

        elif acao == "baixo": 
            self.posicao[0] += 1

        self.ultima_movimentacao_executada = acao
        self.bateria -= 1
        return self.posicao, acao

    def mover_para_cima(self):
        pass
    def mover_para_baixo(self):
        pass
    def mover_para_esquerda(self):
        pass
    def mover_para_direita(self):
        pass

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
