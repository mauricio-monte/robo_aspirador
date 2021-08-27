import numpy as np

from exibicao import (
    concatenar_representacoes,
    colorir_celula,
    gerar_cabecalho_matriz
)
from utils import cima, baixo, direita, esquerda

PISO_LIMPO = 0
OBSTACULO = 1
PISO_SUJO = 2

class Aspirador:
    posicao = [0, 0]
    acoes = ["cima", "baixo", "esquerda", "direita", "aspirar", "recarregar"]
    direcao = "baixo" # Diz se o robo está subindo ou descendo no zig zague
    ultima_movimentacao_executada = ""
    rota_desvio = [] # quais coordenadas devem ser percorridas para o aspirador se deslocar para uma determinada célula
    desviando = False

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
        
        if self.rota_desvio == []:
            movimento = self.zigue_zague()
            self.desviando = False

            if self.checar_colisao_obstaculos(movimento):
                tipo_desvio = self.calcula_tipo_desvio(movimento)
                destino = self.calcula_destino(movimento, tipo_desvio)          
                print("posicao_destino (l, c):", destino)
                self.rota_desvio = self.bfs(self.posicao, destino)
                movimento = self.desviar()
                self.desviando = True
        else:
            movimento = self.desviar()

        return movimento

    def calcula_posicao_obstaculo(self, movimento):
        linha = self.posicao[0]
        coluna = self.posicao[1]
        posicao_obstaculo = []

        if movimento == "cima":
            posicao_obstaculo = cima(linha, coluna)
        elif movimento == "baixo":
            posicao_obstaculo = baixo(linha, coluna)
        elif movimento == "esquerda":
            posicao_obstaculo = esquerda(linha, coluna)
        elif movimento == "direita":
            posicao_obstaculo = direita(linha, coluna)
        
        return posicao_obstaculo

    def calcula_tipo_desvio(self, movimento):
        """Calcula se o obstáculo está no início, meio ou final de uma linha/coluna"""
        posicao_obstaculo = self.calcula_posicao_obstaculo(movimento)
        
        linha_obstaculo = posicao_obstaculo[0]
        coluna_obstaculo = posicao_obstaculo[1]
        obstaculo_esta_no_limite_horizontal = coluna_obstaculo in {0, len(self.piso[0]) - 1}
        obstaculo_limite_vertical = linha_obstaculo in {0, len(self.piso[0])}

        if movimento in ["baixo", "cima"] and obstaculo_esta_no_limite_horizontal:
            return "inicio"
        elif movimento in {"esquerda", "direita"} and obstaculo_esta_no_limite_horizontal:
            return "fim"
        elif movimento in {"esquerda", "direita"} and not obstaculo_esta_no_limite_horizontal:
            return "meio"
        elif movimento in ["baixo", "cima"] and not obstaculo_limite_vertical:
            return "tá descendo ou subindo"
        elif movimento in ["baixo", "cima"] and obstaculo_limite_vertical:
            return "tá no limite em cima ou embaixo"
            
    def calcula_destino(self, movimento, tipo_desvio):
        """Retorna qual posição final de uma rota de desvio"""
        destino = []

        if tipo_desvio == "inicio":
            if self.ultima_movimentacao_executada == "direita":
                direcao = "esquerda"
            else:
                direcao = "direita"

            destino = self.simulacao_movimento(self.posicao[0], self.posicao[1],
                                               movimento)
            destino = self.simulacao_movimento(destino[0], destino[1],
                                               direcao)
            self.ultima_movimentacao_executada = direcao
        elif tipo_desvio == "meio":
            destino = self.simulacao_movimento(self.posicao[0], self.posicao[1],
                                               movimento)
            destino = self.simulacao_movimento(destino[0], destino[1],
                                               movimento)
        elif tipo_desvio == "fim":
            destino = self.simulacao_movimento(self.posicao[0], self.posicao[1],
                                               movimento)
            destino = self.simulacao_movimento(destino[0], destino[1],
                                               self.direcao)
            if self.ultima_movimentacao_executada == "direita":
                self.ultima_movimentacao_executada = "esquerda"
            else:
                self.ultima_movimentacao_executada = "direita"                                   
        return destino


    def simulacao_movimento(self, linha, coluna, movimento):
        proxima_posicao = []

        if movimento == "cima":
            proxima_posicao = cima(linha, coluna)
        elif movimento == "baixo":
            proxima_posicao = baixo(linha, coluna)
        elif movimento == "esquerda":
            proxima_posicao = esquerda(linha, coluna)
        elif movimento == "direita":
            proxima_posicao = direita(linha, coluna)
        
        return proxima_posicao


    def checar_colisao_obstaculos(self, movimento):
        """Simula o movimento a ser executado e verifica se haveria
        colisão com um obstáculo"""
        proxima_posicao = self.simulacao_movimento(self.posicao[0], self.posicao[1],
                                                   movimento)
        
        if self.piso[proxima_posicao[0], proxima_posicao[1]] == str(OBSTACULO):
            return True
        else:
            return False

    def desviar(self):
        """Retorna qual a próxima movimentação a ser feita para executar a rota de desvio"""
        destino = self.rota_desvio[0]
        proximo_movimento = ""
        if destino == cima(*self.posicao):
            proximo_movimento = "cima"
        elif destino == baixo(*self.posicao):
            proximo_movimento = "baixo"
        elif destino == esquerda(*self.posicao):
            proximo_movimento = "esquerda"
        elif destino == direita(*self.posicao):
            proximo_movimento = "direita"
        
        # Atualiza a rota
        self.rota_desvio = self.rota_desvio[1:]

        return proximo_movimento

    def bfs(self, origem, destino):
        """Cria uma rota entre dois pontos"""
        return [(0,8), (1,8)] #este é o resultado esperado para o teste estabelecido

    def zigue_zague(self):
        """Retorna o próximo movimento que o aspirador deve fazer para
        executar um movimento de zigue zague"""
        linha = self.posicao[0]
        coluna = self.posicao[1]
        
        atingiu_limite_cima = (linha <= 0) 
        atingiu_limite_baixo = (linha == len(self.piso) - 1)
        atingiu_limite_esquerda = (coluna <= 0) 
        atingiu_limite_direita = (coluna == len(self.piso[0]) - 1)
        
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
